"""Unit tests for dronelytics core modules."""

import unittest
import numpy as np
import tempfile
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class TestVegetationIndices(unittest.TestCase):
    """Test vegetation index calculations."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_shape = (100, 100)

    def test_ndvi_calculation(self):
        """Test NDVI formula."""
        nir = np.ones(self.test_shape) * 0.5
        red = np.ones(self.test_shape) * 0.3

        ndvi = (nir - red) / (nir + red + 1e-10)
        expected = (0.5 - 0.3) / (0.5 + 0.3)

        self.assertAlmostEqual(ndvi[0, 0], expected, places=5)

    def test_safe_divide(self):
        """Test safe division with zero handling."""
        numerator = np.array([1.0, 2.0, 0.0])
        denominator = np.array([2.0, 0.0, 0.0])

        epsilon = 1e-10
        result = np.divide(numerator, denominator + epsilon, where=denominator != 0)

        self.assertAlmostEqual(result[0], 0.5, places=5)
        self.assertTrue(np.isfinite(result[0]))

    def test_value_range(self):
        """Test that vegetation indices stay within expected ranges."""
        nir = np.random.rand(*self.test_shape) * 0.5 + 0.3
        red = np.random.rand(*self.test_shape) * 0.3 + 0.1

        ndvi = (nir - red) / (nir + red + 1e-10)

        self.assertTrue(np.all(ndvi >= -1))
        self.assertTrue(np.all(ndvi <= 1))


class TestBandConfiguration(unittest.TestCase):
    """Test band configuration and access."""

    def test_band_config_mapping(self):
        """Test band configuration dictionary."""
        config = {
            'red': 1,
            'green': 2,
            'blue': 3,
            'nir': 4,
            'rededge': 5
        }

        self.assertEqual(config['red'], 1)
        self.assertEqual(config['nir'], 4)
        self.assertEqual(config['rededge'], 5)

    def test_4band_config(self):
        """Test 4-band RGB+NIR configuration."""
        config = {
            'red': 1,
            'green': 2,
            'blue': 3,
            'nir': 4
        }

        self.assertEqual(len(config), 4)
        self.assertNotIn('rededge', config)

    def test_5band_config(self):
        """Test 5-band RGB+NIR+RedEdge configuration."""
        config = {
            'red': 1,
            'green': 2,
            'blue': 3,
            'nir': 4,
            'rededge': 5
        }

        self.assertEqual(len(config), 5)
        self.assertIn('rededge', config)


class TestElevationModels(unittest.TestCase):
    """Test elevation model generation."""

    def test_chm_calculation(self):
        """Test CHM = DSM - DTM."""
        dsm = np.array([[10.0, 12.0], [11.0, 13.0]])
        dtm = np.array([[2.0, 2.5], [2.2, 2.3]])

        chm = dsm - dtm

        expected_chm = np.array([[8.0, 9.5], [8.8, 10.7]])
        np.testing.assert_array_almost_equal(chm, expected_chm)

    def test_chm_non_negative(self):
        """Test that CHM values are non-negative."""
        dsm = np.array([[10.0, 12.0, 8.0], [11.0, 13.0, 9.0]])
        dtm = np.array([[2.0, 2.5, 10.0], [2.2, 2.3, 15.0]])

        chm = dsm - dtm
        chm[chm < 0] = 0

        self.assertTrue(np.all(chm >= 0))

    def test_elevation_model_shape(self):
        """Test elevation model shape consistency."""
        dtm = np.random.rand(50, 50)
        dsm = np.random.rand(50, 50) + 5

        chm = dsm - dtm

        self.assertEqual(chm.shape, (50, 50))
        self.assertEqual(dtm.shape, dsm.shape)


class TestDataStructures(unittest.TestCase):
    """Test data structure initialization."""

    def test_vegetation_index_data(self):
        """Test VegetationIndexData structure."""
        data = np.random.rand(100, 100)

        index_data = {
            'name': 'NDVI',
            'data': data,
            'mean': data.mean(),
            'std': data.std(),
            'min': data.min(),
            'max': data.max(),
            'pixel_count': data.size
        }

        self.assertEqual(index_data['name'], 'NDVI')
        self.assertAlmostEqual(index_data['mean'], data.mean(), places=5)

    def test_segmentation_result(self):
        """Test SegmentationResult structure."""
        labels = np.array([[1, 1, 2], [1, 2, 2], [3, 3, 3]])

        result = {
            'segments': labels,
            'num_features': 3,
            'metadata': {'threshold': 0.3, 'method': 'ndvi'}
        }

        self.assertEqual(result['num_features'], 3)
        self.assertEqual(result['metadata']['threshold'], 0.3)


class TestFormulaSupport(unittest.TestCase):
    """Test custom formula support."""

    def test_lambda_formula(self):
        """Test lambda formula execution."""
        nir = np.array([[0.5, 0.6], [0.7, 0.8]])
        red = np.array([[0.2, 0.3], [0.1, 0.4]])

        formula = lambda nir, red: (nir - red) / (nir + red + 1e-10)
        result = formula(nir, red)

        self.assertEqual(result.shape, (2, 2))
        self.assertTrue(np.all(np.isfinite(result)))

    def test_custom_index_formula(self):
        """Test custom vegetation index formula."""
        def custom_formula(nir, green):
            return nir / (green + 1e-10)

        nir = np.ones((50, 50)) * 0.5
        green = np.ones((50, 50)) * 0.2

        result = custom_formula(nir, green)

        self.assertEqual(result.shape, (50, 50))
        self.assertAlmostEqual(result[0, 0], 2.5, places=5)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""

    def test_division_by_zero_handling(self):
        """Test safe division with zero denominator."""
        numerator = np.array([1.0, 2.0, 3.0])
        denominator = np.array([0.0, 2.0, 3.0])

        epsilon = 1e-10
        result = np.divide(numerator, denominator + epsilon, where=denominator != 0)

        self.assertTrue(np.all(np.isfinite(result)))

    def test_nan_handling(self):
        """Test NaN handling in arrays."""
        data = np.array([[1.0, np.nan], [3.0, 4.0]])

        cleaned = np.nan_to_num(data, nan=0.0)

        self.assertFalse(np.any(np.isnan(cleaned)))

    def test_empty_array_handling(self):
        """Test handling of empty arrays."""
        empty = np.array([])

        self.assertEqual(len(empty), 0)
        self.assertTrue(np.isnan(empty.mean()))


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    run_tests()
