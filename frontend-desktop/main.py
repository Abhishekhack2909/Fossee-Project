"""
Chemical Equipment Parameter Visualizer - Desktop Application
PyQt5 + Matplotlib frontend that consumes the same Django REST API

Features:
- Upload CSV file to /api/upload/
- Display summary statistics
- Show bar chart of type distribution using Matplotlib
- View upload history
"""

import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QListWidget, QListWidgetItem,
    QMessageBox, QGroupBox, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# API Configuration
API_BASE = 'http://localhost:8000/api'


class ChartCanvas(FigureCanvas):
    """
    Matplotlib canvas widget for embedding charts in PyQt5.
    Displays a bar chart of equipment type distribution.
    """
    
    def __init__(self, parent=None):
        # Create figure with white background
        self.figure = Figure(figsize=(5, 4), facecolor='white')
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.setParent(parent)
        
        # Initial empty state
        self.axes.set_title('Upload a CSV to see the chart')
        self.axes.set_xlabel('Equipment Type')
        self.axes.set_ylabel('Count')
    
    def update_chart(self, distribution):
        """
        Update the bar chart with new type distribution data.
        
        Args:
            distribution: dict like {"Pump": 5, "Valve": 3}
        """
        self.axes.clear()
        
        if not distribution:
            self.axes.set_title('No data')
            self.draw()
            return
        
        # Prepare data
        types = list(distribution.keys())
        counts = list(distribution.values())
        
        # Create bar chart with colors
        colors = ['#667eea', '#764ba2', '#28a745', '#ffc107', '#dc3545', '#17a2b8']
        bar_colors = colors[:len(types)]
        
        bars = self.axes.bar(types, counts, color=bar_colors, edgecolor='black', linewidth=0.5)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            self.axes.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                str(int(count)),
                ha='center', va='bottom',
                fontsize=10, fontweight='bold'
            )
        
        # Styling
        self.axes.set_title('Equipment Type Distribution', fontsize=12, fontweight='bold')
        self.axes.set_xlabel('Type', fontsize=10)
        self.axes.set_ylabel('Count', fontsize=10)
        self.axes.set_ylim(0, max(counts) * 1.2)  # Add some headroom
        
        # Rotate labels if many types
        if len(types) > 4:
            self.axes.tick_params(axis='x', rotation=45)
        
        self.figure.tight_layout()
        self.draw()


class MainWindow(QMainWindow):
    """
    Main application window.
    
    Layout:
    ┌─────────────────────────────────────────┐
    │              Header                      │
    ├───────────────────┬─────────────────────┤
    │   Upload Button   │                     │
    │   Summary Stats   │   Bar Chart         │
    │   History List    │                     │
    └───────────────────┴─────────────────────┘
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chemical Equipment Visualizer')
        self.setMinimumSize(900, 600)
        
        # Store current summary data
        self.current_summary = None
        
        # Setup UI
        self.setup_ui()
        
        # Load initial history
        self.load_history()
    
    def setup_ui(self):
        """Create and arrange all UI components."""
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header = QLabel('Chemical Equipment Parameter Visualizer')
        header.setFont(QFont('Arial', 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet('color: #667eea; padding: 10px;')
        main_layout.addWidget(header)
        
        # Content area (horizontal split)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        
        # Left panel
        left_panel = QVBoxLayout()
        left_panel.setSpacing(10)
        
        # Upload section
        upload_group = QGroupBox('Upload CSV')
        upload_layout = QVBoxLayout(upload_group)
        
        self.upload_btn = QPushButton('📁 Select CSV File')
        self.upload_btn.setMinimumHeight(50)
        self.upload_btn.setStyleSheet('''
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6fd6;
            }
            QPushButton:pressed {
                background-color: #4a5fc6;
            }
        ''')
        self.upload_btn.clicked.connect(self.upload_file)
        upload_layout.addWidget(self.upload_btn)
        
        self.status_label = QLabel('Select a CSV file to upload')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet('color: #666; font-size: 11px;')
        upload_layout.addWidget(self.status_label)
        
        left_panel.addWidget(upload_group)
        
        # Summary section
        summary_group = QGroupBox('Summary Statistics')
        summary_layout = QGridLayout(summary_group)
        
        # Create labels for stats
        self.stat_labels = {}
        stats = [
            ('total_count', 'Total Count'),
            ('avg_flowrate', 'Avg Flowrate'),
            ('avg_pressure', 'Avg Pressure'),
            ('avg_temperature', 'Avg Temperature')
        ]
        
        for i, (key, label) in enumerate(stats):
            row = i // 2
            col = i % 2
            
            stat_frame = QFrame()
            stat_frame.setStyleSheet('''
                QFrame {
                    background-color: #f8f9fa;
                    border-radius: 5px;
                    padding: 5px;
                }
            ''')
            stat_layout = QVBoxLayout(stat_frame)
            stat_layout.setContentsMargins(10, 5, 10, 5)
            
            value_label = QLabel('--')
            value_label.setFont(QFont('Arial', 18, QFont.Bold))
            value_label.setAlignment(Qt.AlignCenter)
            value_label.setStyleSheet('color: #667eea;')
            self.stat_labels[key] = value_label
            
            name_label = QLabel(label)
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setStyleSheet('color: #666; font-size: 10px;')
            
            stat_layout.addWidget(value_label)
            stat_layout.addWidget(name_label)
            
            summary_layout.addWidget(stat_frame, row, col)
        
        left_panel.addWidget(summary_group)
        
        # History section
        history_group = QGroupBox('Upload History (Last 5)')
        history_layout = QVBoxLayout(history_group)
        
        self.history_list = QListWidget()
        self.history_list.setStyleSheet('''
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e8e8ff;
                color: #333;
            }
            QListWidget::item:hover {
                background-color: #f5f5ff;
            }
        ''')
        self.history_list.itemClicked.connect(self.on_history_item_clicked)
        history_layout.addWidget(self.history_list)
        
        # Refresh button
        refresh_btn = QPushButton('🔄 Refresh History')
        refresh_btn.clicked.connect(self.load_history)
        history_layout.addWidget(refresh_btn)
        
        left_panel.addWidget(history_group)
        
        # Add left panel to content
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        left_widget.setMaximumWidth(350)
        content_layout.addWidget(left_widget)
        
        # Right panel - Chart
        chart_group = QGroupBox('Type Distribution Chart')
        chart_layout = QVBoxLayout(chart_group)
        
        self.chart = ChartCanvas()
        chart_layout.addWidget(self.chart)
        
        content_layout.addWidget(chart_group, stretch=1)
        
        main_layout.addLayout(content_layout)
    
    def upload_file(self):
        """
        Open file dialog, select CSV, upload to backend API.
        """
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Select CSV File',
            '',
            'CSV Files (*.csv);;All Files (*)'
        )
        
        if not file_path:
            return  # User cancelled
        
        self.status_label.setText('Uploading...')
        self.upload_btn.setEnabled(False)
        
        try:
            # Upload file to API
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f'{API_BASE}/upload/', files=files)
            
            if response.status_code == 201:
                # Success
                data = response.json()
                self.current_summary = data
                self.update_summary_display(data)
                self.chart.update_chart(data.get('type_distribution', {}))
                self.status_label.setText('✅ Upload successful!')
                self.load_history()  # Refresh history
            else:
                # Error from server
                error = response.json().get('error', 'Unknown error')
                self.status_label.setText(f'❌ Error: {error}')
                QMessageBox.warning(self, 'Upload Error', error)
                
        except requests.exceptions.ConnectionError:
            self.status_label.setText('❌ Cannot connect to server')
            QMessageBox.critical(
                self, 
                'Connection Error',
                'Cannot connect to the backend server.\n'
                'Make sure Django is running on localhost:8000'
            )
        except Exception as e:
            self.status_label.setText(f'❌ Error: {str(e)}')
            QMessageBox.critical(self, 'Error', str(e))
        finally:
            self.upload_btn.setEnabled(True)
    
    def update_summary_display(self, data):
        """
        Update the summary statistics display with new data.
        """
        self.stat_labels['total_count'].setText(str(data.get('total_count', '--')))
        self.stat_labels['avg_flowrate'].setText(f"{data.get('avg_flowrate', 0):.2f}")
        self.stat_labels['avg_pressure'].setText(f"{data.get('avg_pressure', 0):.2f}")
        self.stat_labels['avg_temperature'].setText(f"{data.get('avg_temperature', 0):.2f}")
    
    def load_history(self):
        """
        Fetch upload history from backend API.
        """
        self.history_list.clear()
        
        try:
            response = requests.get(f'{API_BASE}/history/')
            
            if response.status_code == 200:
                history = response.json()
                
                for item in history:
                    # Format display text
                    timestamp = item.get('uploaded_at', '')[:19].replace('T', ' ')
                    count = item.get('total_count', 0)
                    text = f"#{item['id']} - {timestamp}\n{count} records"
                    
                    list_item = QListWidgetItem(text)
                    list_item.setData(Qt.UserRole, item)  # Store full data
                    self.history_list.addItem(list_item)
                    
        except requests.exceptions.ConnectionError:
            # Server not running - that's okay for history
            pass
        except Exception as e:
            print(f'Error loading history: {e}')
    
    def on_history_item_clicked(self, item):
        """
        When user clicks a history item, display its summary and chart.
        """
        data = item.data(Qt.UserRole)
        if data:
            self.current_summary = data
            self.update_summary_display(data)
            self.chart.update_chart(data.get('type_distribution', {}))
            self.status_label.setText(f"Viewing dataset #{data['id']}")


def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run event loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
