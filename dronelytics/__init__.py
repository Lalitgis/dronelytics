"""
Dronelytics: Comprehensive package for end-to-end drone orthomosaic analysis
and agricultural field phenotyping.

Features:
- Load and process multispectral orthomosaics (4-band and 5-band)
- Calculate 10 vegetation indices with custom formula support
- Automated plot boundary detection
- Pixel-level data extraction
- 3D canopy modeling from point clouds (DTM, DSM, CHM)
- 3D visualization of point clouds, elevation models, and mesh surfaces
- CSV/Excel data export
"""

__version__ = "1.0.0"
__author__ = "Research Development"
__license__ = "MIT"

from .core.orthomosaic import Orthomosaic
from .core.indices import VegetationIndices
from .core.vegetation_indices_extended import VegetationIndicesExtended
from .core.segmentation import PlotSegmentation
from .core.extraction import PixelExtraction
from .core.pointcloud import PointCloudProcessor
from .processing.pipeline import AnalysisPipeline
from .export.csv_export import CSVExporter
from .export.excel_export import ExcelExporter
from .utils.logger import setup_logger
from . import visualization

logger = setup_logger(__name__)

__all__ = [
    'Orthomosaic',
    'VegetationIndices',
    'VegetationIndicesExtended',
    'PlotSegmentation',
    'PixelExtraction',
    'PointCloudProcessor',
    'AnalysisPipeline',
    'CSVExporter',
    'ExcelExporter',
    'setup_logger',
    'visualization',
]
