"""Basic workflow example for dronelytics."""

import logging
from dronelytics import Orthomosaic, VegetationIndicesExtended, PlotSegmentation, PixelExtraction
from dronelytics.utils import setup_logger

logger = setup_logger(__name__)


def basic_analysis():
    """
    Basic workflow: Load orthomosaic, calculate vegetation indices, segment plots.
    """

    logger.info("Starting basic dronelytics workflow")

    try:
        band_config = {
            'red': 1,
            'green': 2,
            'blue': 3,
            'nir': 4
        }

        ortho = Orthomosaic('path/to/field.tif', band_config=band_config)
        logger.info(f"Loaded orthomosaic: {ortho}")

        vi = VegetationIndicesExtended(ortho)
        ndvi = vi.ndvi()
        logger.info(f"NDVI calculated - Mean: {ndvi.mean:.4f}, Std: {ndvi.std:.4f}")

        gndvi = vi.gndvi()
        logger.info(f"GNDVI calculated - Mean: {gndvi.mean:.4f}")

        exg = vi.exg()
        logger.info(f"ExG calculated - Mean: {exg.mean:.4f}")

        segmentation = PlotSegmentation(ortho)
        seg_result = segmentation.segment_by_ndvi(ndvi.data, threshold=0.3)
        logger.info(f"Detected {seg_result.num_features} plot segments")

        extraction = PixelExtraction(ortho)
        extract_result = extraction.extract_spectra()
        logger.info("Extracted spectral data")

        stats = extraction.get_statistics()
        for band_name, band_stats in stats.items():
            logger.info(f"{band_name}: mean={band_stats['mean']:.2f}, std={band_stats['std']:.2f}")

        logger.info("Basic workflow completed successfully")

    except FileNotFoundError:
        logger.error("Orthomosaic file not found - please provide valid path")
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        raise


def custom_index_example():
    """
    Example: Calculate custom vegetation index.
    """

    logger.info("Custom index example")

    try:
        band_config = {
            'red': 1,
            'green': 2,
            'blue': 3,
            'nir': 4
        }

        ortho = Orthomosaic('path/to/field.tif', band_config=band_config)

        vi = VegetationIndicesExtended(ortho)

        def custom_formula(ortho):
            nir = ortho.get_band('nir')
            red = ortho.get_band('red')
            return (nir - red) / (nir + red + 1e-10)

        custom_result = vi.custom(
            formula_func=custom_formula,
            name='CUSTOM_NDVI',
            description='Custom NDVI with offset',
            value_range=(-1, 1)
        )

        logger.info(f"Custom index calculated - Mean: {custom_result.mean:.4f}")

    except Exception as e:
        logger.error(f"Custom index example failed: {e}")


if __name__ == '__main__':
    basic_analysis()
    custom_index_example()
