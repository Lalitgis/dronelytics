"""Orthomosaic loading and management."""

import logging
import numpy as np
import rasterio
from pathlib import Path

logger = logging.getLogger(__name__)


class Orthomosaic:
    """Load and manage multispectral orthomosaic data."""

    def __init__(self, filepath, band_config=None):
        """
        Initialize orthomosaic.

        Parameters
        ----------
        filepath : str
            Path to GeoTIFF file
        band_config : dict
            Band configuration mapping (e.g., {'red': 1, 'nir': 4})
        """
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        self.band_config = band_config or {}
        self._validate_band_config()
        self.data = None
        self.metadata = {}
        self._load()

    def _load(self):
        """Load GeoTIFF file."""
        try:
            with rasterio.open(self.filepath) as src:
                self.data = src.read()
                self.metadata = src.meta
                self.transform = src.transform
                self.crs = src.crs
                logger.info(f"Loaded {self.filepath}: shape {self.data.shape}")
        except Exception as e:
            logger.error(f"Failed to load {self.filepath}: {e}")
            raise

    def get_band(self, band_name):
        """Get band data by name."""
        if band_name not in self.band_config:
            raise ValueError(f"Band '{band_name}' not in config")

        band_idx = self.band_config[band_name]
        return self.data[band_idx - 1].astype(np.float32)

    def get_shape(self):
        """Get data shape."""
        return self.data.shape[1:]

    def get_transform(self):
        """Get geospatial transform."""
        return self.transform

    def get_crs(self):
        """Get coordinate reference system."""
        return self.crs

    def close(self):
        """Close and cleanup."""
        self.data = None
        logger.info("Orthomosaic closed")

    def clear_cache(self):
        """Clear cache."""
        self.data = None

    def __repr__(self):
        return f"Orthomosaic({self.filepath.name}, shape={self.data.shape})"
