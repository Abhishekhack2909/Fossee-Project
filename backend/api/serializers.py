"""
DRF Serializers for converting model instances to JSON.
"""

from rest_framework import serializers
from .models import DatasetSummary


class DatasetSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for DatasetSummary model.
    Converts type_distribution from JSON string to dict for API response.
    """
    type_distribution = serializers.SerializerMethodField()
    
    class Meta:
        model = DatasetSummary
        fields = [
            'id',
            'uploaded_at',
            'total_count',
            'avg_flowrate',
            'avg_pressure',
            'avg_temperature',
            'type_distribution',
        ]
    
    def get_type_distribution(self, obj):
        """Convert JSON string to dict."""
        return obj.get_type_distribution()


class DatasetSummaryDetailSerializer(DatasetSummarySerializer):
    """
    Extended serializer that includes original data (for reports).
    """
    original_data = serializers.SerializerMethodField()
    
    class Meta(DatasetSummarySerializer.Meta):
        fields = DatasetSummarySerializer.Meta.fields + ['original_data']
    
    def get_original_data(self, obj):
        """Convert JSON string to list of dicts."""
        return obj.get_original_data()
