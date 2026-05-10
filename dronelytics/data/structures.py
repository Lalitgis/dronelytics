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
    num_plots: int
    boundaries: list

@dataclass
class ExtractionResult:
    pixels: list
    plot_stats: Dict[str, Any]

@dataclass
class PointCloudMetadata:
    filepath: str
    num_points: int
    bounds: Dict[str, tuple]
    classification_counts: Dict

@dataclass
class ThreeDModel:
    mesh: Any
    vertices: np.ndarray
    faces: np.ndarray
    model_type: str
    height_range: tuple
    metadata: Dict
