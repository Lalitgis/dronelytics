"""Excel export functionality."""
import logging
logger = logging.getLogger(__name__)

class ExcelExporter:
    """Export data to Excel format."""
    def export(self, output_path, **kwargs):
        """Export data to Excel."""
        logger.info(f"Exporting to {output_path}")
        with __import__('openpyxl').load_workbook() as wb:
            for sheet_name, data in kwargs.items():
                if sheet_name in wb.sheetnames:
                    del wb[sheet_name]
                ws = wb.create_sheet(sheet_name)
                for r_idx, row in enumerate(data.values, 1):
                    for c_idx, val in enumerate(row, 1):
                        ws.cell(r_idx, c_idx, val)
            wb.save(output_path)
        logger.info("Export complete")
