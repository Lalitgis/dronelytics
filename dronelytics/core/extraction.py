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
