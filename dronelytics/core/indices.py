"""Standard vegetation indices (legacy, use vegetation_indices_extended instead)."""

import logging
import numpy as np
from ..data.structures import VegetationIndexData

logger = logging.getLogger(__name__)


class VegetationIndices:
    """Calculate standard vegetation indices (4-band support)."""

    def __init__(self, orthomosaic):
        """Initialize with orthomosaic."""
        self.ortho = orthomosaic
        self.results = {}

    def _safe_divide(self, numerator, denominator):
        """Safely divide avoiding division by zero."""
        epsilon = max(1e-10, np.abs(denominator).max() * 1e-12)
        return np.divide(numerator, denominator + epsilon, where=denominator != 0)

    def _check_bands(self, required_bands):
        """Check if required bands exist."""
        missing = [b for b in required_bands if b not in self.ortho.band_config]
        if missing:
            raise ValueError(f"Missing bands: {missing}")

    def ndvi(self):
        """Normalized Difference Vegetation Index."""
        self._check_bands(['red', 'nir'])
        nir = self.ortho.get_band('nir')
        red = self.ortho.get_band('red')
        ndvi = self._safe_divide(nir - red, nir + red)
        self.results['ndvi'] = VegetationIndexData('NDVI', ndvi, ndvi.mean(), ndvi.std(), ndvi.min(), ndvi.max(), ndvi.size)
        return self.results['ndvi']

    def gndvi(self):
        """Green Normalized Difference Vegetation Index."""
        self._check_bands(['nir', 'green'])
        nir = self.ortho.get_band('nir')
        green = self.ortho.get_band('green')
        gndvi = self._safe_divide(nir - green, nir + green)
        self.results['gndvi'] = VegetationIndexData('GNDVI', gndvi, gndvi.mean(), gndvi.std(), gndvi.min(), gndvi.max(), gndvi.size)
        return self.results['gndvi']

    def get(self, name):
        """Get calculated index by name."""
        return self.results.get(name.lower())

    def get_all(self):
        """Get all calculated indices."""
        return self.results
