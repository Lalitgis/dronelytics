"""Excel export functionality."""

import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)


class ExcelExporter:
    """Export data to Excel format."""

    def export(self, output_path, **kwargs):
        """Export data to Excel.

        Parameters
        ----------
        output_path : str
            Output file path
        **kwargs : dict
            Sheet name -> DataFrame mapping
        """
        try:
            logger.info(f"Exporting to {output_path}")

            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                for sheet_name, data in kwargs.items():
                    if isinstance(data, pd.DataFrame):
                        data.to_excel(writer, sheet_name=sheet_name, index=False)
                    else:
                        # Convert to DataFrame if it's not already
                        df = pd.DataFrame(data)
                        df.to_excel(writer, sheet_name=sheet_name, index=False)

            logger.info("Export complete")

        except Exception as e:
            logger.error(f"Excel export failed: {e}")
            raise

    def export_multi_sheet(self, output_path, sheets_dict):
        """Export multiple sheets to Excel.

        Parameters
        ----------
        output_path : str
            Output file path
        sheets_dict : dict
            Dictionary of sheet_name -> DataFrame
        """
        try:
            logger.info(f"Exporting {len(sheets_dict)} sheets to {output_path}")

            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                for sheet_name, data in sheets_dict.items():
                    if isinstance(data, pd.DataFrame):
                        data.to_excel(writer, sheet_name=sheet_name, index=False)
                    else:
                        df = pd.DataFrame(data)
                        df.to_excel(writer, sheet_name=sheet_name, index=False)

            logger.info(f"Successfully exported {len(sheets_dict)} sheets")

        except Exception as e:
            logger.error(f"Multi-sheet export failed: {e}")
            raise

    def export_single_sheet(self, output_path, data, sheet_name='Sheet1'):
        """Export single sheet to Excel.

        Parameters
        ----------
        output_path : str
            Output file path
        data : pd.DataFrame
            Data to export
        sheet_name : str
            Sheet name
        """
        try:
            logger.info(f"Exporting {sheet_name} to {output_path}")

            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                if isinstance(data, pd.DataFrame):
                    data.to_excel(writer, sheet_name=sheet_name, index=False)
                else:
                    df = pd.DataFrame(data)
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

            logger.info("Single sheet export complete")

        except Exception as e:
            logger.error(f"Single sheet export failed: {e}")
            raise
