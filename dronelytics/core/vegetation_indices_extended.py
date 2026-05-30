"""Extended vegetation indices (10 types) with custom formula support."""

import logging
import numpy as np
from typing import Callable, Optional, Tuple
from ..data.structures import VegetationIndexData

logger = logging.getLogger(__name__)


class VegetationIndicesExtended:
    """Calculate 10 vegetation indices with custom formula support."""

    def __init__(self, orthomosaic):
        """Initialize with orthomosaic."""
        self.ortho = orthomosaic
        self.results = {}

    def _safe_divide(self, numerator, denominator):
        """Safely divide avoiding division by zero."""
        epsilon = 1e-10 + np.abs(denominator).max() * 1e-12
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

    def ndre(self):
        """Normalized Difference Red-Edge (5-band only)."""
        self._check_bands(['nir', 'rededge'])
        nir = self.ortho.get_band('nir')
        rededge = self.ortho.get_band('rededge')
        ndre = self._safe_divide(nir - rededge, nir + rededge)
        self.results['ndre'] = VegetationIndexData('NDRE', ndre, ndre.mean(), ndre.std(), ndre.min(), ndre.max(), ndre.size)
        return self.results['ndre']

    def gndvi(self):
        """Green Normalized Difference Vegetation Index."""
        self._check_bands(['nir', 'green'])
        nir = self.ortho.get_band('nir')
        green = self.ortho.get_band('green')
        gndvi = self._safe_divide(nir - green, nir + green)
        self.results['gndvi'] = VegetationIndexData('GNDVI', gndvi, gndvi.mean(), gndvi.std(), gndvi.min(), gndvi.max(), gndvi.size)
        return self.results['gndvi']

    def exg(self):
        """Excess Green."""
        self._check_bands(['red', 'green', 'blue'])
        red = self.ortho.get_band('red')
        green = self.ortho.get_band('green')
        blue = self.ortho.get_band('blue')
        exg = 2 * green - red - blue
        self.results['exg'] = VegetationIndexData('ExG', exg, exg.mean(), exg.std(), exg.min(), exg.max(), exg.size)
        return self.results['exg']

    def savi(self, L=0.5):
        """Soil-Adjusted Vegetation Index."""
        self._check_bands(['red', 'nir'])
        nir = self.ortho.get_band('nir')
        red = self.ortho.get_band('red')
        savi = self._safe_divide((nir - red) / (nir + red + L), 1 + L)
        self.results['savi'] = VegetationIndexData('SAVI', savi, savi.mean(), savi.std(), savi.min(), savi.max(), savi.size)
        return self.results['savi']

    def msavi(self):
        """Modified SAVI."""
        self._check_bands(['red', 'nir'])
        nir = self.ortho.get_band('nir')
        red = self.ortho.get_band('red')
        msavi = 2 * nir + 1 - np.sqrt((2 * nir + 1) ** 2 - 8 * (nir - red))
        msavi = msavi / 2
        self.results['msavi'] = VegetationIndexData('MSAVI', msavi, msavi.mean(), msavi.std(), msavi.min(), msavi.max(), msavi.size)
        return self.results['msavi']

    def vari(self):
        """Visible Atmospherically Resistant Index."""
        self._check_bands(['red', 'green', 'blue'])
        red = self.ortho.get_band('red')
        green = self.ortho.get_band('green')
        blue = self.ortho.get_band('blue')
        vari = self._safe_divide(green - red, green + red - blue)
        self.results['vari'] = VegetationIndexData('VARI', vari, vari.mean(), vari.std(), vari.min(), vari.max(), vari.size)
        return self.results['vari']

    def arvi(self):
        """Atmospherically Resistant Vegetation Index."""
        self._check_bands(['red', 'blue', 'nir'])
        nir = self.ortho.get_band('nir')
        red = self.ortho.get_band('red')
        blue = self.ortho.get_band('blue')
        arvi = self._safe_divide(nir - (2 * red - blue), nir + (2 * red - blue))
        self.results['arvi'] = VegetationIndexData('ARVI', arvi, arvi.mean(), arvi.std(), arvi.min(), arvi.max(), arvi.size)
        return self.results['arvi']

    def cvi(self):
        """Chlorophyll Vegetation Index."""
        self._check_bands(['red', 'green', 'nir'])
        nir = self.ortho.get_band('nir')
        red = self.ortho.get_band('red')
        green = self.ortho.get_band('green')
        cvi = (nir / green) * (red / green)
        self.results['cvi'] = VegetationIndexData('CVI', cvi, cvi.mean(), cvi.std(), cvi.min(), cvi.max(), cvi.size)
        return self.results['cvi']

    def osavi(self, Y=0.16):
        """Optimized SAVI."""
        self._check_bands(['red', 'nir'])
        nir = self.ortho.get_band('nir')
        red = self.ortho.get_band('red')
        osavi = self._safe_divide((nir - red) / (nir + red + Y), 1 + Y)
        self.results['osavi'] = VegetationIndexData('OSAVI', osavi, osavi.mean(), osavi.std(), osavi.min(), osavi.max(), osavi.size)
        return self.results['osavi']

    def evi(self, G=2.5, C1=6.0, C2=7.5, L=1.0):
        """Enhanced Vegetation Index."""
        self._check_bands(['red', 'nir', 'blue'])
        nir = self.ortho.get_band('nir')
        red = self.ortho.get_band('red')
        blue = self.ortho.get_band('blue')
        evi = G * self._safe_divide(nir - red, nir + C1 * red - C2 * blue + L)
        self.results['evi'] = VegetationIndexData('EVI', evi, evi.mean(), evi.std(), evi.min(), evi.max(), evi.size)
        return self.results['evi']

    def custom(self, formula_func: Callable, name: str, description: str = None, value_range: Tuple = (-1, 1)):
        """Calculate custom vegetation index using user formula."""
        try:
            logger.info(f"Calculating custom index: {name}")
            result = formula_func(self.ortho).astype(np.float32)
            if not isinstance(result, np.ndarray):
                raise ValueError("Formula must return numpy array")
            veg_data = VegetationIndexData(name, result, result.mean(), result.std(), result.min(), result.max(), result.size)
            self.results[name.lower()] = veg_data
            return veg_data
        except Exception as e:
            logger.error(f"Custom index failed: {e}")
            raise

    # Alias methods for consistency with documentation
    def calculate_ndvi(self):
        """Alias for ndvi()."""
        return self.ndvi()

    def calculate_ndre(self):
        """Alias for ndre()."""
        return self.ndre()

    def calculate_gndvi(self):
        """Alias for gndvi()."""
        return self.gndvi()

    def calculate_evi(self):
        """Alias for evi()."""
        return self.evi()

    def calculate_all(self):
        """Calculate all available indices."""
        indices = [
            ('ndvi', self.ndvi),
            ('gndvi', self.gndvi),
            ('exg', self.exg),
            ('savi', self.savi),
            ('msavi', self.msavi),
            ('vari', self.vari),
            ('arvi', self.arvi),
            ('cvi', self.cvi),
            ('osavi', self.osavi),
            ('evi', self.evi),
        ]

        for name, func in indices:
            try:
                func()
                logger.info(f"✓ {name.upper()} calculated")
            except ValueError:
                logger.warning(f"⚠ {name.upper()} skipped (missing bands)")

        try:
            self.ndre()
            logger.info("✓ NDRE calculated")
        except ValueError:
            logger.warning("⚠ NDRE skipped (5-band imagery required)")

        return self.results

    def get(self, name):
        """Get calculated index by name."""
        return self.results.get(name.lower())

    def get_all(self):
        """Get all calculated indices."""
        return self.results

    def list_available(self):
        """List available calculated indices."""
        return list(self.results.keys())
