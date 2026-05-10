"""Advanced workflow example with 5-band imagery and point cloud processing."""

import logging
import numpy as np
from dronelytics import Orthomosaic, VegetationIndicesExtended
from dronelytics.core.pointcloud import PointCloudProcessor
from dronelytics.utils import setup_logger

logger = setup_logger(__name__)


def five_band_analysis():
    """
    Advanced workflow: Process 5-band imagery with red-edge band.
    """

    logger.info("Starting 5-band imagery analysis")

    try:
        band_config = {
            'red': 1,
            'green': 2,
            'blue': 3,
            'nir': 4,
            'rededge': 5
        }

        ortho = Orthomosaic('path/to/field_5band.tif', band_config=band_config)
        logger.info(f"Loaded 5-band orthomosaic: {ortho}")

        vi = VegetationIndicesExtended(ortho)

        logger.info("Calculating 4-band indices...")
        ndvi = vi.ndvi()
        gndvi = vi.gndvi()
        savi = vi.savi(L=0.5)
        msavi = vi.msavi()
        logger.info(f"Calculated NDVI, GNDVI, SAVI, MSAVI")

        logger.info("Calculating red-edge index...")
        ndre = vi.ndre()
        logger.info(f"NDRE calculated - Mean: {ndre.mean:.4f} (5-band only)")

        logger.info("Calculating remaining indices...")
        all_results = vi.calculate_all()

        logger.info(f"Total indices calculated: {len(all_results)}")
        for idx_name in all_results.keys():
            idx_data = all_results[idx_name]
            logger.info(f"  {idx_data.name}: mean={idx_data.mean:.4f}, std={idx_data.std:.4f}")

    except FileNotFoundError:
        logger.error("5-band orthomosaic file not found")
    except Exception as e:
        logger.error(f"5-band analysis failed: {e}")


def point_cloud_processing():
    """
    Advanced workflow: Process LAS point cloud and generate CHM.
    """

    logger.info("Starting point cloud processing")

    try:
        processor = PointCloudProcessor('path/to/field.las')
        logger.info(f"Loaded point cloud: {processor.get_metadata()}")

        logger.info("Classifying ground points...")
        ground_count = processor.classify_ground()
        logger.info(f"Classified {ground_count} ground points")

        logger.info("Generating DTM (ground surface)...")
        dtm, dtm_meta = processor.generate_dtm(cell_size=1.0)
        logger.info(f"DTM generated: {dtm.shape}, range: {dtm_meta['x_range']}")

        logger.info("Generating DSM (top surface)...")
        dsm, dsm_meta = processor.generate_dsm(cell_size=1.0)
        logger.info(f"DSM generated: {dsm.shape}")

        logger.info("Generating CHM (DSM - DTM)...")
        chm, chm_meta = processor.generate_chm(cell_size=1.0)
        logger.info(f"CHM statistics:")
        logger.info(f"  Min height: {chm_meta['min_height']:.2f}m")
        logger.info(f"  Max height: {chm_meta['max_height']:.2f}m")
        logger.info(f"  Mean height: {chm_meta['mean_height']:.2f}m")

        logger.info("Generating 3D mesh...")
        mesh = processor.generate_mesh()
        logger.info(f"Mesh generated with {mesh.mesh.n_cells} cells")

        processor.close()

    except ImportError:
        logger.error("Point cloud support not installed. Install with: pip install dronelytics[pointcloud]")
    except FileNotFoundError:
        logger.error("LAS file not found")
    except Exception as e:
        logger.error(f"Point cloud processing failed: {e}")


def multi_index_comparison():
    """
    Advanced: Compare multiple vegetation indices for crop health monitoring.
    """

    logger.info("Multi-index comparison analysis")

    try:
        band_config = {
            'red': 1,
            'green': 2,
            'blue': 3,
            'nir': 4
        }

        ortho = Orthomosaic('path/to/field.tif', band_config=band_config)

        vi = VegetationIndicesExtended(ortho)

        indices_to_calculate = [
            ('ndvi', vi.ndvi),
            ('gndvi', vi.gndvi),
            ('exg', vi.exg),
            ('savi', vi.savi),
            ('msavi', vi.msavi),
            ('vari', vi.vari),
            ('arvi', vi.arvi),
            ('cvi', vi.cvi),
            ('osavi', vi.osavi)
        ]

        results = {}
        for name, func in indices_to_calculate:
            try:
                result = func()
                results[name] = result
                logger.info(f"{name}: mean={result.mean:.4f}, range=[{result.min:.4f}, {result.max:.4f}]")
            except ValueError:
                logger.warning(f"{name} skipped (missing bands)")

        logger.info(f"Comparison complete: {len(results)} indices analyzed")

    except Exception as e:
        logger.error(f"Multi-index comparison failed: {e}")


if __name__ == '__main__':
    five_band_analysis()
    point_cloud_processing()
    multi_index_comparison()
