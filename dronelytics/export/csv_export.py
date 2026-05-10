"""CSV export functionality."""
import logging
logger = logging.getLogger(__name__)

class CSVExporter:
    """Export data to CSV format."""
    def export(self, data, output_path):
        """Export data to CSV."""
        logger.info(f"Exporting to {output_path}")
        data.to_csv(output_path, index=False)
        logger.info("Export complete")
