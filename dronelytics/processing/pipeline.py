"""Analysis pipeline orchestration."""

import logging
import os
from pathlib import Path
import pandas as pd
from ..core.indices import VegetationIndices
from ..core.vegetation_indices_extended import VegetationIndicesExtended
from ..core.segmentation import PlotSegmentation
from ..core.extraction import PixelExtraction
from ..export.excel_export import ExcelExporter

logger = logging.getLogger(__name__)


class AnalysisPipeline:
    """Orchestrate complete analysis workflow."""

    def __init__(self):
        """Initialize pipeline."""
        logger.info("Pipeline initialized")
        self.results = {}
        self.indices = None
        self.segmentation = None
        self.extraction = None

    def run(self, ortho, method='standard', output_dir=None, export_excel=True):
        """Run complete analysis pipeline.

        Parameters
        ----------
        ortho : Orthomosaic
            Orthomosaic object
        method : str
            Analysis method: 'standard', 'extended', 'minimal'
        output_dir : str, optional
            Directory for output files
        export_excel : bool
            Whether to export results to Excel

        Returns
        -------
        dict
            Pipeline results
        """
        try:
            logger.info(f"Running {method} pipeline")

            # Step 1: Calculate vegetation indices
            logger.info("Step 1: Calculating vegetation indices...")
            if method == 'minimal':
                self.indices = VegetationIndices(ortho)
                try:
                    ndvi_data = self.indices.ndvi()
                    self.results['ndvi'] = ndvi_data
                except:
                    logger.warning("Could not calculate NDVI")
            elif method == 'standard':
                self.indices = VegetationIndices(ortho)
                try:
                    self.results['ndvi'] = self.indices.ndvi()
                except:
                    logger.warning("Could not calculate NDVI")
                try:
                    self.results['gndvi'] = self.indices.gndvi()
                except:
                    logger.warning("Could not calculate GNDVI")
            else:  # extended
                self.indices = VegetationIndicesExtended(ortho)
                self.results.update(self.indices.calculate_all())

            logger.info(f"Calculated {len(self.results)} indices")

            # Step 2: Detect plot boundaries
            logger.info("Step 2: Detecting plot boundaries...")
            self.segmentation = PlotSegmentation(ortho)

            # Use NDVI if available, otherwise use first band
            if 'ndvi' in self.results:
                ndvi_array = self.results['ndvi'].values
            else:
                ndvi_array = None

            seg_result = self.segmentation.segment_by_ndvi(
                ndvi_array=ndvi_array,
                method='quickshift',
                threshold=0.3,
                kernel_size=15,
                max_dist=40.0,
                min_plot_size=100
            )

            self.results['segmentation'] = seg_result
            logger.info(f"Detected {seg_result.num_features} plot segments")

            # Step 3: Extract pixel values from segments
            logger.info("Step 3: Extracting pixel data from segments...")
            self.extraction = PixelExtraction(ortho)

            self.extraction.extract_from_segmentation(
                self.segmentation,
                seg_result.labels
            )

            # Get summary by plot
            if 'ndvi' in self.results:
                ndvi_for_stats = self.results['ndvi'].values
            else:
                ndvi_for_stats = None

            plot_summary = self.extraction.summarize_by_plot(
                self.segmentation,
                seg_result.labels,
                vegetation_index=ndvi_for_stats
            )

            self.results['plot_summary'] = plot_summary
            logger.info(f"Extracted data for {len(plot_summary)} plots")

            # Step 4: Export results
            logger.info("Step 4: Exporting results...")
            self._export_results(output_dir, export_excel)

            logger.info("Pipeline completed successfully")
            return self.results

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise

    def _export_results(self, output_dir=None, export_excel=True):
        """Export pipeline results to files.

        Parameters
        ----------
        output_dir : str, optional
            Output directory path
        export_excel : bool
            Whether to export to Excel
        """
        try:
            if output_dir is None:
                output_dir = Path.cwd() / 'analysis_results'

            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Export CSV
            if 'plot_summary' in self.results:
                csv_path = output_dir / 'plot_summary.csv'
                self.results['plot_summary'].to_csv(csv_path, index=False)
                logger.info(f"Exported CSV to {csv_path}")

            # Export Excel
            if export_excel and 'plot_summary' in self.results:
                excel_path = output_dir / 'analysis_results.xlsx'
                exporter = ExcelExporter()

                sheets = {
                    'Plot_Summary': self.results['plot_summary']
                }

                # Add vegetation indices if available
                for idx_name, idx_data in self.results.items():
                    if hasattr(idx_data, 'values') and hasattr(idx_data, 'name'):
                        # Create a summary dataframe for the index
                        idx_summary = pd.DataFrame({
                            'Metric': ['Mean', 'Std', 'Min', 'Max', 'Pixels'],
                            'Value': [
                                idx_data.mean,
                                idx_data.std,
                                idx_data.min,
                                idx_data.max,
                                idx_data.pixel_count
                            ]
                        })
                        sheets[idx_data.name] = idx_summary

                exporter.export_multi_sheet(str(excel_path), sheets)
                logger.info(f"Exported Excel to {excel_path}")

        except Exception as e:
            logger.error(f"Export failed: {e}")
            raise

    def get_results(self):
        """Get pipeline results.

        Returns
        -------
        dict
            All calculated results
        """
        return self.results
