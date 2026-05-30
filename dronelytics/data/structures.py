"""Data structure definitions."""
from dataclasses import dataclass
from typing import Optional, Dict, Any
import numpy as np

@dataclass
class VegetationIndexData:
    name: str
    values: np.ndarray
    mean: float
    std: float
    min: float
    max: float
    pixel_count: int

@dataclass
class SegmentationResult:
    labels: np.ndarray
    num_features: int
    metadata: Dict[str, Any]

@dataclass
class ExtractionResult:
    data: np.ndarray
    mask: np.ndarray
    metadata: Dict[str, Any]

@dataclass
class PointCloudMetadata:
    filepath: str
    num_points: int
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    z_min: float
    z_max: float
    las_version: str

@dataclass
class ThreeDModel:
    mesh: Any
    vertices: np.ndarray
    faces: np.ndarray
    model_type: str
    height_range: tuple
    metadata: Dict
