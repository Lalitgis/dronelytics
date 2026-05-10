"""3D visualization examples using the 3dVis module."""

import logging
import numpy as np
from dronelytics import Orthomosaic, VegetationIndicesExtended
from dronelytics.core.pointcloud import PointCloudProcessor
from dronelytics.visualization import show_pointcloud, show_dem, show_chm, show_mesh, show_comparison
from dronelytics.utils import setup_logger

logger = setup_logger(__name__)


def visualize_vegetation_index():
    """
    Visualize CHM from crop height model.
    """

    logger.info("CHM Visualization example")

    try:
        processor = PointCloudProcessor('path/to/field.las')

        chm, chm_meta = processor.generate_chm(cell_size=1.0)

        show_chm(chm, title="Crop Height Model - CHM = DSM - DTM")

        processor.close()

    except ImportError:
        logger.error("Point cloud support required. Install with: pip install dronelytics[pointcloud]")
    except FileNotFoundError:
        logger.error("LAS file not found")
    except Exception as e:
        logger.error(f"Visualization failed: {e}")


def visualize_elevation_models():
    """
    Visualize DTM and DSM for comparison.
    """

    logger.info("Elevation models visualization")

    try:
        processor = PointCloudProcessor('path/to/field.las')

        dtm, _ = processor.generate_dtm(cell_size=1.0)
        dsm, _ = processor.generate_dsm(cell_size=1.0)

        show_dem(dtm, title="Digital Terrain Model (Ground)")

        show_dem(dsm, title="Digital Surface Model (Top)")

        show_comparison(
            {'DTM': dtm, 'DSM': dsm},
            title="DTM vs DSM Comparison"
        )

        processor.close()

    except ImportError:
        logger.error("Point cloud support required")
    except FileNotFoundError:
        logger.error("LAS file not found")
    except Exception as e:
        logger.error(f"Visualization failed: {e}")


def visualize_point_cloud():
    """
    Visualize point cloud with classification.
    """

    logger.info("Point cloud visualization")

    try:
        processor = PointCloudProcessor('path/to/field.las')

        processor.classify_ground()

        points = processor.points
        labels = processor.las.classification

        show_pointcloud(points, labels=labels, title="Point Cloud with Ground Classification")

        processor.close()

    except ImportError:
        logger.error("Point cloud support required")
    except FileNotFoundError:
        logger.error("LAS file not found")
    except Exception as e:
        logger.error(f"Visualization failed: {e}")


def visualize_3d_mesh():
    """
    Visualize 3D surface mesh.
    """

    logger.info("3D mesh visualization")

    try:
        processor = PointCloudProcessor('path/to/field.las')

        mesh = processor.generate_mesh()

        show_mesh(mesh, title="3D Surface Mesh - Delaunay Triangulation")

        processor.close()

    except ImportError:
        logger.error("Point cloud support and pyvista required")
    except FileNotFoundError:
        logger.error("LAS file not found")
    except Exception as e:
        logger.error(f"Visualization failed: {e}")


def visualize_all_models():
    """
    Complete visualization example: DTM, DSM, CHM, and mesh.
    """

    logger.info("Complete visualization workflow")

    try:
        processor = PointCloudProcessor('path/to/field.las')

        logger.info("Generating elevation models...")
        dtm, _ = processor.generate_dtm(cell_size=1.0)
        dsm, _ = processor.generate_dsm(cell_size=1.0)
        chm, _ = processor.generate_chm(cell_size=1.0)

        logger.info("Generating mesh...")
        mesh = processor.generate_mesh()

        logger.info("Displaying visualizations...")
        show_dem(dtm, title="DTM - Ground Surface")
        show_dem(dsm, title="DSM - Top Surface")
        show_chm(chm, title="CHM - Crop Height Model")
        show_mesh(mesh, title="3D Mesh")

        show_comparison(
            {'DTM': dtm, 'DSM': dsm, 'CHM': chm},
            title="Elevation Models Comparison"
        )

        processor.close()

    except ImportError:
        logger.error("Point cloud support required")
    except FileNotFoundError:
        logger.error("LAS file not found")
    except Exception as e:
        logger.error(f"Complete visualization failed: {e}")


if __name__ == '__main__':
    visualize_vegetation_index()
    visualize_elevation_models()
    visualize_point_cloud()
    visualize_3d_mesh()
    visualize_all_models()
