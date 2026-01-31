"""
Database models for storing uploaded dataset summaries.

DatasetSummary model stores:
- Computed statistics (averages, counts)
- Type distribution as JSON
- Original data as JSON (for report generation)
- Upload timestamp
"""

from django.db import models
import json


class DatasetSummary(models.Model):
    """
    Stores the summary of each uploaded CSV dataset.
    Only the last 5 records are kept (older ones are deleted automatically).
    """
    # Upload timestamp
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Computed statistics
    total_count = models.IntegerField(help_text="Number of rows in CSV")
    avg_flowrate = models.FloatField(help_text="Average flowrate")
    avg_pressure = models.FloatField(help_text="Average pressure")
    avg_temperature = models.FloatField(help_text="Average temperature")
    
    # Type distribution stored as JSON string
    # Example: {"Pump": 5, "Valve": 3, "Compressor": 2}
    type_distribution = models.TextField(help_text="JSON: count per equipment type")
    
    # Store original data for PDF report generation
    original_data = models.TextField(help_text="JSON: original CSV data")
    
    class Meta:
        ordering = ['-uploaded_at']  # Newest first
        verbose_name_plural = "Dataset Summaries"
    
    def get_type_distribution(self):
        """Return type_distribution as Python dict."""
        return json.loads(self.type_distribution)
    
    def get_original_data(self):
        """Return original_data as Python list of dicts."""
        return json.loads(self.original_data)
    
    def __str__(self):
        return f"Dataset #{self.id} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
