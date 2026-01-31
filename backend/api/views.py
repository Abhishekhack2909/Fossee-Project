"""
API Views for the Chemical Equipment Parameter Visualizer.

Endpoints:
1. POST /api/upload/     - Upload CSV, compute summary, store in DB
2. GET  /api/history/    - Get last 5 uploaded datasets
3. GET  /api/report/<id>/ - Generate PDF report for a dataset
4. POST /api/auth/login/ - Simple token authentication
"""

import json
import pandas as pd
from io import BytesIO

from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from .models import DatasetSummary
from .serializers import DatasetSummarySerializer


# Maximum number of datasets to keep in history
MAX_HISTORY = 5


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow uploads without auth for simplicity
def upload_csv(request):
    """
    POST /api/upload/
    
    Accept CSV file, parse with Pandas, compute summary, store in SQLite.
    Expected CSV columns: Equipment Name, Type, Flowrate, Pressure, Temperature
    
    Returns: JSON summary of the uploaded data
    """
    # Check if file was uploaded
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file uploaded. Use "file" field in multipart/form-data.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    csv_file = request.FILES['file']
    
    # Validate file extension
    if not csv_file.name.endswith('.csv'):
        return Response(
            {'error': 'File must be a CSV file.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Read CSV with Pandas
        df = pd.read_csv(csv_file)
        
        # Validate required columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return Response(
                {'error': f'Missing columns: {missing_columns}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Compute summary statistics
        total_count = len(df)
        avg_flowrate = round(df['Flowrate'].mean(), 2)
        avg_pressure = round(df['Pressure'].mean(), 2)
        avg_temperature = round(df['Temperature'].mean(), 2)
        
        # Count per Type (e.g., {"Pump": 5, "Valve": 3})
        type_distribution = df['Type'].value_counts().to_dict()
        
        # Store original data for PDF report generation
        original_data = df.to_dict(orient='records')
        
        # Create new summary record
        summary = DatasetSummary.objects.create(
            total_count=total_count,
            avg_flowrate=avg_flowrate,
            avg_pressure=avg_pressure,
            avg_temperature=avg_temperature,
            type_distribution=json.dumps(type_distribution),
            original_data=json.dumps(original_data),
        )
        
        # Keep only last 5 datasets (delete older ones)
        all_summaries = DatasetSummary.objects.all()
        if all_summaries.count() > MAX_HISTORY:
            # Get IDs of records to keep (newest 5)
            ids_to_keep = all_summaries[:MAX_HISTORY].values_list('id', flat=True)
            # Delete older records
            DatasetSummary.objects.exclude(id__in=ids_to_keep).delete()
        
        # Return the summary
        serializer = DatasetSummarySerializer(summary)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except pd.errors.EmptyDataError:
        return Response(
            {'error': 'CSV file is empty.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Error processing CSV: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_history(request):
    """
    GET /api/history/
    
    Return list of last 5 uploaded datasets with summary and timestamp.
    """
    summaries = DatasetSummary.objects.all()[:MAX_HISTORY]
    serializer = DatasetSummarySerializer(summaries, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def generate_report(request, pk):
    """
    GET /api/report/<id>/
    
    Generate and return a PDF report for the selected dataset.
    Uses ReportLab to create the PDF.
    """
    try:
        summary = DatasetSummary.objects.get(pk=pk)
    except DatasetSummary.DoesNotExist:
        return Response(
            {'error': 'Dataset not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Create PDF in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Title
    title = Paragraph(f"Chemical Equipment Report - Dataset #{summary.id}", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 20))
    
    # Upload timestamp
    timestamp = Paragraph(f"Uploaded: {summary.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
    elements.append(timestamp)
    elements.append(Spacer(1, 20))
    
    # Summary statistics
    summary_title = Paragraph("Summary Statistics", styles['Heading2'])
    elements.append(summary_title)
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Equipment Count', str(summary.total_count)],
        ['Average Flowrate', f"{summary.avg_flowrate:.2f}"],
        ['Average Pressure', f"{summary.avg_pressure:.2f}"],
        ['Average Temperature', f"{summary.avg_temperature:.2f}"],
    ]
    
    summary_table = Table(summary_data, colWidths=[200, 150])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))
    
    # Type distribution
    type_title = Paragraph("Equipment Type Distribution", styles['Heading2'])
    elements.append(type_title)
    
    type_dist = summary.get_type_distribution()
    type_data = [['Type', 'Count']] + [[k, str(v)] for k, v in type_dist.items()]
    
    type_table = Table(type_data, colWidths=[200, 150])
    type_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(type_table)
    elements.append(Spacer(1, 20))
    
    # Original data table (first 20 rows for brevity)
    data_title = Paragraph("Equipment Data (First 20 rows)", styles['Heading2'])
    elements.append(data_title)
    
    original_data = summary.get_original_data()[:20]
    if original_data:
        headers = list(original_data[0].keys())
        data_rows = [headers] + [[str(row.get(h, '')) for h in headers] for row in original_data]
        
        data_table = Table(data_rows, colWidths=[100, 60, 60, 60, 80])
        data_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(data_table)
    
    # Build PDF
    doc.build(elements)
    
    # Return PDF response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_dataset_{pk}.pdf"'
    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    POST /api/auth/login/
    
    Simple token-based authentication.
    Request body: {"username": "...", "password": "..."}
    Returns: {"token": "...", "user_id": ..., "username": "..."}
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid credentials.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Get or create token for the user
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
    })
