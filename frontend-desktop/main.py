"""
Chemical Equipment Parameter Visualizer - Desktop Application
Simple, clean PyQt5 interface
"""

import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QListWidget, QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


API_BASE = 'http://127.0.0.1:8000/api'


class ChartCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = Figure(figsize=(8, 4), facecolor='white')
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.setParent(parent)
        self.axes.set_title('Upload CSV to see chart')
    
    def update_chart(self, distribution):
        self.axes.clear()
        if not distribution:
            self.axes.set_title('No data')
            self.draw()
            return
        
        types = list(distribution.keys())
        counts = list(distribution.values())
        colors = ['#667eea', '#764ba2', '#28a745', '#ffc107', '#dc3545', '#17a2b8']
        
        bars = self.axes.bar(types, counts, color=colors[:len(types)], edgecolor='black', linewidth=0.5)
        
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            self.axes.text(bar.get_x() + bar.get_width() / 2, height, str(int(count)),
                          ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        self.axes.set_title('Equipment Type Distribution', fontsize=12, fontweight='bold')
        self.axes.set_ylabel('Count', fontsize=10)
        if len(types) > 4:
            self.axes.tick_params(axis='x', rotation=45)
        self.figure.tight_layout()
        self.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Equipment Data Analyzer')
        self.setMinimumSize(1400, 800)
        self.current_summary = None
        self.setup_ui()
        self.load_history()
    
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QLabel('Equipment Data Analyzer')
        header.setFont(QFont('Arial', 20, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet('background: #2c2c2c; color: white; padding: 25px;')
        main_layout.addWidget(header)
        
        # Content
        content = QWidget()
        content.setStyleSheet('background: #f5f5f5;')
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Left sidebar
        left = QWidget()
        left.setMaximumWidth(300)
        left_layout = QVBoxLayout(left)
        left_layout.setSpacing(15)
        
        # Upload button
        self.upload_btn = QPushButton('📁 Choose CSV File')
        self.upload_btn.setMinimumHeight(50)
        self.upload_btn.setStyleSheet('''
            QPushButton {
                background: #2c2c2c;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background: #1a1a1a; }
        ''')
        self.upload_btn.clicked.connect(self.upload_file)
        left_layout.addWidget(self.upload_btn)
        
        # Status
        self.status = QLabel('Ready to upload')
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet('color: #666; font-size: 11px; padding: 5px;')
        left_layout.addWidget(self.status)
        
        # History
        history_label = QLabel('Recent Uploads')
        history_label.setStyleSheet('color: #2c2c2c; font-size: 13px; font-weight: bold; padding: 10px 0;')
        left_layout.addWidget(history_label)
        
        self.history_list = QListWidget()
        self.history_list.setStyleSheet('''
            QListWidget {
                background: white;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background: #e8e8ff;
                color: #333;
            }
        ''')
        self.history_list.itemClicked.connect(self.on_history_click)
        left_layout.addWidget(self.history_list)
        
        # Download button
        self.download_btn = QPushButton('📄 Download PDF')
        self.download_btn.setEnabled(False)
        self.download_btn.setStyleSheet('''
            QPushButton {
                background: #2c2c2c;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 12px;
            }
            QPushButton:hover:enabled { background: #1a1a1a; }
            QPushButton:disabled { background: #ccc; color: #666; }
        ''')
        self.download_btn.clicked.connect(self.download_report)
        left_layout.addWidget(self.download_btn)
        
        left_layout.addStretch()
        content_layout.addWidget(left)
        
        # Right side
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Statistics (takes exactly half the height)
        stats_container = QWidget()
        stats_container.setStyleSheet('background: white; border-radius: 8px; padding: 15px;')
        stats_layout = QGridLayout(stats_container)
        stats_layout.setSpacing(15)
        stats_layout.setContentsMargins(15, 15, 15, 15)
        
        self.stat_labels = {}
        stats = [
            ('total_count', 'TOTAL'),
            ('avg_flowrate', 'AVG FLOW'),
            ('avg_pressure', 'AVG PRESSURE'),
            ('avg_temperature', 'AVG TEMP')
        ]
        
        for i, (key, label) in enumerate(stats):
            stat_widget = QWidget()
            stat_widget.setStyleSheet('background: #fafafa; border: 1px solid #e5e5e5; border-radius: 6px; padding: 20px;')
            stat_layout_inner = QVBoxLayout(stat_widget)
            stat_layout_inner.setSpacing(10)
            
            name = QLabel(label)
            name.setAlignment(Qt.AlignCenter)
            name.setStyleSheet('color: #666; font-size: 11px; font-weight: 600;')
            stat_layout_inner.addWidget(name)
            
            value = QLabel('--')
            value.setFont(QFont('Arial', 36, QFont.Bold))
            value.setAlignment(Qt.AlignCenter)
            value.setStyleSheet('color: #2c2c2c;')
            self.stat_labels[key] = value
            stat_layout_inner.addWidget(value)
            
            stats_layout.addWidget(stat_widget, 0, i)
        
        right_layout.addWidget(stats_container, stretch=1)
        
        # Chart (takes exactly half the height)
        chart_container = QWidget()
        chart_container.setStyleSheet('background: white; border-radius: 8px; padding: 15px;')
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(0, 0, 0, 0)
        
        self.chart = ChartCanvas()
        chart_layout.addWidget(self.chart)
        right_layout.addWidget(chart_container, stretch=1)
        
        content_layout.addWidget(right, stretch=1)
        main_layout.addWidget(content)
    
    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select CSV', '', 'CSV Files (*.csv)')
        if not file_path:
            return
        
        self.status.setText('Uploading...')
        self.upload_btn.setEnabled(False)
        
        try:
            with open(file_path, 'rb') as f:
                response = requests.post(f'{API_BASE}/upload/', files={'file': f})
            
            if response.status_code == 201:
                data = response.json()
                self.current_summary = data
                self.update_display(data)
                self.status.setText('✅ Upload successful!')
                self.load_history()
            else:
                error = response.json().get('error', 'Upload failed')
                self.status.setText(f'❌ {error}')
                QMessageBox.warning(self, 'Error', error)
        except Exception as e:
            self.status.setText(f'❌ Error')
            QMessageBox.critical(self, 'Error', str(e))
        finally:
            self.upload_btn.setEnabled(True)
    
    def update_display(self, data):
        self.stat_labels['total_count'].setText(str(data.get('total_count', '--')))
        self.stat_labels['avg_flowrate'].setText(f"{data.get('avg_flowrate', 0):.2f}")
        self.stat_labels['avg_pressure'].setText(f"{data.get('avg_pressure', 0):.2f}")
        self.stat_labels['avg_temperature'].setText(f"{data.get('avg_temperature', 0):.2f}")
        self.chart.update_chart(data.get('type_distribution', {}))
        self.download_btn.setEnabled(True)
    
    def load_history(self):
        self.history_list.clear()
        try:
            response = requests.get(f'{API_BASE}/history/')
            if response.status_code == 200:
                for item in response.json():
                    timestamp = item.get('uploaded_at', '')[:19].replace('T', ' ')
                    text = f"#{item['id']} - {timestamp}\n{item.get('total_count', 0)} records"
                    list_item = self.history_list.addItem(text)
                    self.history_list.item(self.history_list.count() - 1).setData(Qt.UserRole, item)
        except:
            pass
    
    def on_history_click(self, item):
        data = item.data(Qt.UserRole)
        if data:
            self.current_summary = data
            self.update_display(data)
            self.status.setText(f"Viewing dataset #{data['id']}")
    
    def download_report(self):
        if not self.current_summary:
            return
        
        dataset_id = self.current_summary.get('id')
        try:
            response = requests.get(f'{API_BASE}/report/{dataset_id}/', stream=True)
            if response.status_code == 200:
                file_path, _ = QFileDialog.getSaveFileName(
                    self, 'Save PDF', f'report_{dataset_id}.pdf', 'PDF Files (*.pdf)')
                if file_path:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    QMessageBox.information(self, 'Success', 'Report saved!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
