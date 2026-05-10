"""Plot boundary segmentation and detection."""

import logging
import numpy as np
from scipy import ndimage
from ..data.structures import SegmentationResult

logger = logging.getLogger(__name__)


class PlotSegmentation:
    """Detect and segment plot boundaries in orthomosaic."""

    def __init__(self, orthomosaic):
        """Initialize with orthomosaic."""
        self.ortho = orthomosaic
        self.segments = None

    def segment_by_ndvi(self, ndvi_array, threshold=0.3):
        """Segment plots based on NDVI threshold."""
        try:
            logger.info(f"Segmenting by NDVI threshold: {threshold}")

            binary = ndvi_array > threshold
            labeled, num_features = ndimage.label(binary)

            logger.info(f"Detected {num_features} plot segments")

            self.segments = labeled
            return SegmentationResult(labeled, num_features, {'threshold': threshold, 'method': 'ndvi'})

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
