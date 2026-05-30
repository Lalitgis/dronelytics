"""Pixel-level data extraction from orthomosaic."""

import logging
import numpy as np
import pandas as pd
from ..data.structures import ExtractionResult

logger = logging.getLogger(__name__)


class PixelExtraction:
    """Extract pixel-level spectral and derived data."""

    def __init__(self, orthomosaic):
        """Initialize with orthomosaic."""
        self.ortho = orthomosaic
        self.extracted_data = None

    def extract_spectra(self, mask=None):
        """Extract spectral values for all bands."""
        try:
            logger.info("Extracting spectral data")

            if mask is None:
                mask = np.ones(self.ortho.get_shape(), dtype=bool)

            extracted = {}
            for band_name in self.ortho.band_config.keys():
                band_data = self.ortho.get_band(band_name)
                extracted[band_name] = band_data[mask]

            logger.info(f"Extracted {mask.sum()} pixels")
            self.extracted_data = extracted

            return ExtractionResult(extracted, mask, {'method': 'spectra'})

        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            raise

    def extract_by_coordinates(self, x_coords, y_coords):
        """Extract values at specific pixel coordinates."""
        try:
            logger.info(f"Extracting {len(x_coords)} pixel locations")

            extracted = {}
            for band_name in self.ortho.band_config.keys():
                band_data = self.ortho.get_band(band_name)
                extracted[band_name] = band_data[y_coords, x_coords]

            return ExtractionResult(extracted, None, {'method': 'coordinates', 'count': len(x_coords)})

        except Exception as e:
            logger.error(f"Coordinate extraction failed: {e}")
            raise

    def to_dataframe(self):
        """Convert extracted data to pandas DataFrame."""
        if self.extracted_data is None:
            raise ValueError("No data extracted yet")

        df = pd.DataFrame(self.extracted_data)
        logger.info(f"Created DataFrame with shape {df.shape}")
        return df

    def get_statistics(self):
        """Get statistics of extracted data."""
        if self.extracted_data is None:
            raise ValueError("No data extracted yet")

        stats = {}
        for band_name, values in self.extracted_data.items():
            stats[band_name] = {
                'mean': float(np.mean(values)),
                'std': float(np.std(values)),
                'min': float(np.min(values)),
                'max': float(np.max(values)),
                'count': int(len(values))
            }

        return stats

    def extract_from_segmentation(self, segmentation, segments_array):
        """Extract pixel data from segmented regions.

        Parameters
        ----------
        segmentation : PlotSegmentation
            PlotSegmentation instance with performed segmentation
        segments_array : np.ndarray
            Labeled segments array

        Returns
        -------
        ExtractionResult
            Extracted data from segments
        """
        try:
            logger.info("Extracting data from segmented regions")

            # Extract all spectral data
            extracted = {}
            for band_name in self.ortho.band_config.keys():
                band_data = self.ortho.get_band(band_name)
                extracted[band_name] = band_data.flatten()

            mask = segments_array.flatten() > 0
            self.extracted_data = extracted

            return ExtractionResult(
                np.column_stack([extracted[b] for b in extracted.keys()]),
                mask,
                {'method': 'segmentation', 'num_segments': len(np.unique(segments_array)) - 1}
            )

        except Exception as e:
            logger.error(f"Segmentation extraction failed: {e}")
            raise

    def summarize_by_plot(self, segmentation, segments_array, vegetation_index=None):
        """Create summary statistics by plot (segment).

        Parameters
        ----------
        segmentation : PlotSegmentation
            PlotSegmentation instance
        segments_array : np.ndarray
            Labeled segments array
        vegetation_index : np.ndarray, optional
            Vegetation index values for statistics

        Returns
        -------
        pd.DataFrame
            Summary statistics by plot
        """
        try:
            logger.info("Summarizing data by plot")

            summaries = []
            unique_segments = np.unique(segments_array)
            unique_segments = unique_segments[unique_segments > 0]  # Remove background

            for seg_id in unique_segments:
                mask = segments_array == seg_id
                stats = self._calculate_plot_stats(mask, seg_id, vegetation_index)
                summaries.append(stats)

            df = pd.DataFrame(summaries)
            logger.info(f"Created summary for {len(summaries)} plots")
            return df

        except Exception as e:
            logger.error(f"Plot summarization failed: {e}")
            raise

    def _calculate_plot_stats(self, mask, plot_id, vegetation_index=None):
        """Calculate statistics for a single plot.

        Parameters
        ----------
        mask : np.ndarray
            Boolean mask for plot pixels
        plot_id : int
            Plot identifier
        vegetation_index : np.ndarray, optional
            Vegetation index array

        Returns
        -------
        dict
            Statistics dictionary
        """
        stats = {
            'plot_id': int(plot_id),
            'pixel_count': int(mask.sum()),
        }

        # Band statistics
        for band_name in self.ortho.band_config.keys():
            band_data = self.ortho.get_band(band_name)
            pixels = band_data[mask]
            if len(pixels) > 0:
                stats[f'{band_name}_mean'] = float(np.mean(pixels))
                stats[f'{band_name}_std'] = float(np.std(pixels))
                stats[f'{band_name}_min'] = float(np.min(pixels))
                stats[f'{band_name}_max'] = float(np.max(pixels))

        # Vegetation index statistics if provided
        if vegetation_index is not None:
            vi_pixels = vegetation_index[mask]
            if len(vi_pixels) > 0:
                stats['vi_mean'] = float(np.mean(vi_pixels))
                stats['vi_std'] = float(np.std(vi_pixels))
                stats['vi_min'] = float(np.min(vi_pixels))
                stats['vi_max'] = float(np.max(vi_pixels))

        return stats

    def get_plot_statistics(self, plot_id, segmentation, segments_array):
        """Get statistics for a specific plot.

        Parameters
        ----------
        plot_id : int
            Plot identifier
        segmentation : PlotSegmentation
            PlotSegmentation instance
        segments_array : np.ndarray
            Labeled segments array

        Returns
        -------
        dict
            Statistics for the plot
        """
        mask = segments_array == plot_id
        return self._calculate_plot_stats(mask, plot_id)

    def to_csv(self, filepath):
        """Export extracted data to CSV file.

        Parameters
        ----------
        filepath : str
            Output CSV file path
        """
        try:
            df = self.to_dataframe()
            df.to_csv(filepath, index=False)
            logger.info(f"Data exported to {filepath}")
        except Exception as e:
            logger.error(f"CSV export failed: {e}")
            raise
