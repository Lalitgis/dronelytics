"""Point cloud processing and 3D model generation."""

import logging
import numpy as np
from pathlib import Path
from ..data.structures import PointCloudMetadata, ThreeDModel

logger = logging.getLogger(__name__)

try:
    import laspy
    LASPY_AVAILABLE = True
except ImportError:
    LASPY_AVAILABLE = False
    logger.warning("laspy not installed - point cloud support disabled")

try:
    import pyvista as pv
    PYVISTA_AVAILABLE = True
except ImportError:
    PYVISTA_AVAILABLE = False
    logger.warning("pyvista not installed - 3D visualization disabled")


class PointCloudProcessor:
    """Process LAS/LAZ point cloud files and generate 3D models."""

    def __init__(self, filepath):
        """Initialize with point cloud file."""
        if not LASPY_AVAILABLE:
            raise ImportError("laspy is required for point cloud processing. Install with: pip install dronelytics[pointcloud]")

        self.filepath = Path(filepath)
        if not self.filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        self.las = None
        self.points = None
        self.metadata = None
        self._load()

    def _load(self):
        """Load LAS/LAZ file."""
        try:
            self.las = laspy.read(str(self.filepath))
            self.points = np.vstack((self.las.x, self.las.y, self.las.z)).transpose()
            self.metadata = PointCloudMetadata(
                point_count=len(self.points),
                x_min=float(self.las.x.min()),
                x_max=float(self.las.x.max()),
                y_min=float(self.las.y.min()),
                y_max=float(self.las.y.max()),
                z_min=float(self.las.z.min()),
                z_max=float(self.las.z.max()),
                las_version=str(self.las.header.version)
            )
            logger.info(f"Loaded {len(self.points)} points from {self.filepath.name}")
        except Exception as e:
            logger.error(f"Failed to load point cloud: {e}")
            raise

    def classify_ground(self, max_angle=15.0, max_distance=2.5):
        """Simple ground classification by elevation."""
        try:
            logger.info("Classifying ground points")

            z_values = self.points[:, 2]
            threshold = np.percentile(z_values, 10)

            self.las.classification = np.where(z_values < threshold, 2, 0)

            ground_count = np.sum(self.las.classification == 2)
            logger.info(f"Classified {ground_count} ground points")

            return ground_count

        except Exception as e:
            logger.error(f"Classification failed: {e}")
            raise

    def generate_dtm(self, cell_size=1.0):
        """Generate Digital Terrain Model (ground surface)."""
        try:
            logger.info(f"Generating DTM with cell size {cell_size}m")

            ground_mask = self.las.classification == 2
            if not ground_mask.any():
                logger.warning("No ground points found, using lowest 10% of points")
                z_values = self.points[:, 2]
                threshold = np.percentile(z_values, 10)
                ground_mask = z_values < threshold

            ground_points = self.points[ground_mask]

            x_min, x_max = ground_points[:, 0].min(), ground_points[:, 0].max()
            y_min, y_max = ground_points[:, 1].min(), ground_points[:, 1].max()

            x_bins = np.arange(x_min, x_max + cell_size, cell_size)
            y_bins = np.arange(y_min, y_max + cell_size, cell_size)

            dtm = np.zeros((len(y_bins) - 1, len(x_bins) - 1))

            for i in range(len(y_bins) - 1):
                for j in range(len(x_bins) - 1):
                    mask = (ground_points[:, 0] >= x_bins[j]) & (ground_points[:, 0] < x_bins[j + 1]) & \
                           (ground_points[:, 1] >= y_bins[i]) & (ground_points[:, 1] < y_bins[i + 1])

                    if mask.any():
                        dtm[i, j] = ground_points[mask, 2].min()
                    else:
                        dtm[i, j] = np.nan

            logger.info(f"DTM generated with shape {dtm.shape}")
            return dtm, {'cell_size': cell_size, 'x_range': (x_min, x_max), 'y_range': (y_min, y_max)}

        except Exception as e:
            logger.error(f"DTM generation failed: {e}")
            raise

    def generate_dsm(self, cell_size=1.0):
        """Generate Digital Surface Model (top surface including vegetation)."""
        try:
            logger.info(f"Generating DSM with cell size {cell_size}m")

            x_min, x_max = self.points[:, 0].min(), self.points[:, 0].max()
            y_min, y_max = self.points[:, 1].min(), self.points[:, 1].max()

            x_bins = np.arange(x_min, x_max + cell_size, cell_size)
            y_bins = np.arange(y_min, y_max + cell_size, cell_size)

            dsm = np.zeros((len(y_bins) - 1, len(x_bins) - 1))

            for i in range(len(y_bins) - 1):
                for j in range(len(x_bins) - 1):
                    mask = (self.points[:, 0] >= x_bins[j]) & (self.points[:, 0] < x_bins[j + 1]) & \
                           (self.points[:, 1] >= y_bins[i]) & (self.points[:, 1] < y_bins[i + 1])

                    if mask.any():
                        dsm[i, j] = self.points[mask, 2].max()
                    else:
                        dsm[i, j] = np.nan

            logger.info(f"DSM generated with shape {dsm.shape}")
            return dsm, {'cell_size': cell_size, 'x_range': (x_min, x_max), 'y_range': (y_min, y_max)}

        except Exception as e:
            logger.error(f"DSM generation failed: {e}")
            raise

    def generate_chm(self, cell_size=1.0):
        """Generate Crop Height Model (CHM = DSM - DTM)."""
        try:
            logger.info(f"Generating CHM (DSM - DTM) with cell size {cell_size}m")

            dtm, dtm_meta = self.generate_dtm(cell_size)
            dsm, dsm_meta = self.generate_dsm(cell_size)

            chm = dsm - dtm

            chm[np.isnan(chm)] = 0
            chm[chm < 0] = 0

            logger.info(f"CHM generated - min: {np.nanmin(chm):.2f}m, max: {np.nanmax(chm):.2f}m, mean: {np.nanmean(chm):.2f}m")

            metadata = {
                'cell_size': cell_size,
                'min_height': float(np.nanmin(chm)),
                'max_height': float(np.nanmax(chm)),
                'mean_height': float(np.nanmean(chm)),
                'method': 'DSM - DTM'
            }

            return chm, metadata

        except Exception as e:
            logger.error(f"CHM generation failed: {e}")
            raise

    def generate_mesh(self):
        """Generate 3D surface mesh from point cloud."""
        if not PYVISTA_AVAILABLE:
            raise ImportError("pyvista is required for mesh generation. Install with: pip install dronelytics[pointcloud]")

        try:
            logger.info("Generating 3D surface mesh")

            cloud = pv.PolyData(self.points)

            surface = cloud.delaunay_2d(alpha=50.0)

            logger.info(f"Mesh generated with {surface.n_cells} cells and {surface.n_points} points")

            return ThreeDModel(surface, self.points, 'delaunay')

        except Exception as e:
            logger.error(f"Mesh generation failed: {e}")
            raise

    def get_metadata(self):
        """Get point cloud metadata."""
        return self.metadata

    def close(self):
        """Close and cleanup."""
        self.points = None
        self.las = None
        logger.info("Point cloud processor closed")
