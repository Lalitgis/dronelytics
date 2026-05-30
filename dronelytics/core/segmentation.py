"""Plot boundary segmentation and detection."""

import logging
import numpy as np
from scipy import ndimage
from skimage import segmentation as skimage_seg
import geopandas as gpd
from shapely.geometry import shape
import rasterio.features
from ..data.structures import SegmentationResult

logger = logging.getLogger(__name__)


class PlotSegmentation:
    """Detect and segment plot boundaries in orthomosaic."""

    def __init__(self, orthomosaic):
        """Initialize with orthomosaic."""
        self.ortho = orthomosaic
        self.segments = None
        self.metadata = {}

    def segment_by_ndvi(self, ndvi_array=None, method='quickshift', threshold=0.3,
                       kernel_size=15, max_dist=40.0, min_plot_size=100):
        """Segment plots based on NDVI or other array.

        Parameters
        ----------
        ndvi_array : np.ndarray, optional
            Array to segment (e.g., NDVI values). If None, uses first band.
        method : str
            Segmentation algorithm: 'quickshift', 'watershed', 'felzenszwalb'
        threshold : float
            NDVI threshold for initial segmentation
        kernel_size : int
            Kernel size for quickshift
        max_dist : float
            Maximum distance for quickshift
        min_plot_size : int
            Minimum pixels per segment

        Returns
        -------
        SegmentationResult
            Segmentation results
        """
        try:
            if ndvi_array is None:
                ndvi_array = self.ortho.get_band(list(self.ortho.band_config.keys())[0])

            logger.info(f"Segmenting using {method} algorithm")

            # Normalize array to 0-1 range for consistency
            arr_min, arr_max = ndvi_array.min(), ndvi_array.max()
            if arr_max > arr_min:
                normalized = (ndvi_array - arr_min) / (arr_max - arr_min)
            else:
                normalized = np.zeros_like(ndvi_array)

            # Create initial binary mask
            binary = normalized > threshold

            # Apply segmentation algorithm
            if method == 'quickshift':
                labeled = skimage_seg.quickshift(
                    normalized,
                    kernel_size=kernel_size,
                    max_dist=max_dist,
                    sigma=0
                )
            elif method == 'watershed':
                # Use inverted normalized array as elevation map
                labeled = ndimage.label(binary)[0]
                labeled = skimage_seg.watershed(
                    1 - normalized,
                    markers=labeled,
                    compactness=0.001
                )
            elif method == 'felzenszwalb':
                labeled = skimage_seg.felzenszwalb(
                    normalized,
                    scale=max_dist,
                    sigma=0.5
                )
            else:
                raise ValueError(f"Unknown method: {method}")

            # Filter by minimum plot size
            unique, counts = np.unique(labeled, return_counts=True)
            small_segments = unique[counts < min_plot_size]
            for seg_id in small_segments:
                labeled[labeled == seg_id] = 0

            # Relabel to remove gaps
            labeled, num_features = ndimage.label(labeled > 0)

            logger.info(f"Detected {num_features} plot segments after filtering")

            self.segments = labeled
            self.metadata = {
                'threshold': threshold,
                'method': method,
                'kernel_size': kernel_size,
                'max_dist': max_dist,
                'min_plot_size': min_plot_size,
                'num_features': num_features
            }

            return SegmentationResult(labeled, num_features, self.metadata)

        except Exception as e:
            logger.error(f"Segmentation failed: {e}")
            raise

    def get_segment_stats(self, data, segment_id):
        """Get statistics for a specific segment."""
        if self.segments is None:
            raise ValueError("No segmentation performed yet")

        mask = self.segments == segment_id
        segment_data = data[mask]

        return {
            'segment_id': segment_id,
            'mean': float(segment_data.mean()),
            'std': float(segment_data.std()),
            'min': float(segment_data.min()),
            'max': float(segment_data.max()),
            'pixel_count': int(mask.sum())
        }

    def get_all_segments(self):
        """Get all segment labels."""
        return self.segments

    def get_segment_mask(self, segment_id):
        """Get binary mask for specific segment."""
        if self.segments is None:
            raise ValueError("No segmentation performed yet")
        return self.segments == segment_id

    def get_boundaries_geodataframe(self):
        """Get segment boundaries as GeoDataFrame for GeoJSON export.

        Returns
        -------
        gpd.GeoDataFrame
            GeoDataFrame with segment geometries
        """
        if self.segments is None:
            raise ValueError("No segmentation performed yet")

        features = []
        for geometry, value in rasterio.features.shapes(
            self.segments.astype('uint8'),
            transform=None
        ):
            if value > 0:  # Skip background (0)
                features.append({
                    'geometry': shape(geometry),
                    'segment_id': int(value),
                    'pixel_count': int((self.segments == value).sum())
                })

        if not features:
            raise ValueError("No valid segments to convert to GeoDataFrame")

        gdf = gpd.GeoDataFrame(features, crs=None)
        return gdf
