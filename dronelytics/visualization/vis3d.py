"""3D visualization module (3dVis) for orthomosaic and point cloud data."""

import logging
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D

logger = logging.getLogger(__name__)

try:
    import pyvista as pv
    PYVISTA_AVAILABLE = True
except ImportError:
    PYVISTA_AVAILABLE = False
    logger.warning("pyvista not installed - interactive 3D visualization disabled")


def show_pointcloud(points, labels=None, title="Point Cloud"):
    """Visualize point cloud data.

    Parameters
    ----------
    points : ndarray
        Nx3 array of (x, y, z) coordinates
    labels : ndarray, optional
        Array of labels for coloring points
    title : str
        Plot title
    """
    try:
        if PYVISTA_AVAILABLE:
            cloud = pv.PolyData(points)

            if labels is not None:
                cloud['labels'] = labels

            plotter = pv.Plotter(window_size=(1000, 800))
            if labels is not None:
                plotter.add_mesh(cloud, scalars='labels', cmap='viridis')
            else:
                plotter.add_mesh(cloud, color='lightblue')
            plotter.set_background('white')
            plotter.show()

        else:
            fig = plt.figure(figsize=(12, 9))
            ax = fig.add_subplot(111, projection='3d')

            if labels is not None:
                scatter = ax.scatter(points[:, 0], points[:, 1], points[:, 2],
                                   c=labels, cmap='viridis', s=1)
                plt.colorbar(scatter, ax=ax, label='Classification')
            else:
                ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=1, c='lightblue')

            ax.set_xlabel('X (m)')
            ax.set_ylabel('Y (m)')
            ax.set_zlabel('Z (m)')
            ax.set_title(title)
            plt.tight_layout()
            plt.show()

        logger.info(f"Displayed {len(points)} points")

    except Exception as e:
        logger.error(f"Point cloud visualization failed: {e}")
        raise


def show_dem(dem, title="Digital Elevation Model", cmap='terrain'):
    """Visualize Digital Elevation Model (DTM or DSM).

    Parameters
    ----------
    dem : ndarray
        2D array of elevation values
    title : str
        Plot title
    cmap : str
        Colormap name
    """
    try:
        fig, ax = plt.subplots(figsize=(12, 9))

        im = ax.imshow(dem, cmap=cmap, origin='upper')
        plt.colorbar(im, ax=ax, label='Elevation (m)')

        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        ax.set_title(title)

        plt.tight_layout()
        plt.show()

        logger.info(f"Displayed DEM with shape {dem.shape}")

    except Exception as e:
        logger.error(f"DEM visualization failed: {e}")
        raise


def show_chm(chm, title="Crop Height Model", cmap='RdYlGn'):
    """Visualize Crop Height Model.

    Parameters
    ----------
    chm : ndarray
        2D array of crop height values
    title : str
        Plot title
    cmap : str
        Colormap name
    """
    try:
        fig, ax = plt.subplots(figsize=(12, 9))

        im = ax.imshow(chm, cmap=cmap, origin='upper')
        cbar = plt.colorbar(im, ax=ax, label='Height (m)')

        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        ax.set_title(title)

        stats_text = f"Min: {np.nanmin(chm):.2f}m | Max: {np.nanmax(chm):.2f}m | Mean: {np.nanmean(chm):.2f}m"
        ax.text(0.5, -0.1, stats_text, transform=ax.transAxes, ha='center', fontsize=10)

        plt.tight_layout()
        plt.show()

        logger.info(f"Displayed CHM with shape {chm.shape}")

    except Exception as e:
        logger.error(f"CHM visualization failed: {e}")
        raise


def show_mesh(mesh, title="3D Surface Mesh"):
    """Visualize 3D surface mesh.

    Parameters
    ----------
    mesh : pyvista.PolyData or ThreeDModel
        3D mesh object
    title : str
        Plot title
    """
    try:
        if PYVISTA_AVAILABLE:
            if hasattr(mesh, 'mesh'):
                mesh_obj = mesh.mesh
            else:
                mesh_obj = mesh

            plotter = pv.Plotter(window_size=(1000, 800))
            plotter.add_mesh(mesh_obj, color='lightblue', edge_color='gray', line_width=0.1)
            plotter.set_background('white')
            plotter.add_title(title)
            plotter.show()

            logger.info(f"Displayed mesh with {mesh_obj.n_cells} cells")

        else:
            raise ImportError("pyvista required for mesh visualization")

    except Exception as e:
        logger.error(f"Mesh visualization failed: {e}")
        raise


def show_comparison(data_dict, title="Data Comparison"):
    """Visualize multiple elevation models for comparison.

    Parameters
    ----------
    data_dict : dict
        Dictionary of {name: array} pairs to compare
    title : str
        Overall title
    """
    try:
        n_models = len(data_dict)
        fig, axes = plt.subplots(1, n_models, figsize=(5*n_models, 5))

        if n_models == 1:
            axes = [axes]

        for ax, (name, data) in zip(axes, data_dict.items()):
            im = ax.imshow(data, cmap='terrain', origin='upper')
            plt.colorbar(im, ax=ax, label='Elevation (m)')
            ax.set_title(name)
            ax.set_xlabel('X (pixels)')
            ax.set_ylabel('Y (pixels)')

        fig.suptitle(title, fontsize=14)
        plt.tight_layout()
        plt.show()

        logger.info(f"Displayed comparison of {n_models} models")

    except Exception as e:
        logger.error(f"Comparison visualization failed: {e}")
        raise
