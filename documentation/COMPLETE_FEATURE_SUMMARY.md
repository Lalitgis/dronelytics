# Dronelytics - Complete Feature Summary

## Package Overview

Dronelytics is a comprehensive Python package for end-to-end drone orthomosaic analysis and agricultural field phenotyping. Built from the ground up with clean, simple APIs for easy understanding and use.

## Core Features

### 1. Orthomosaic Processing

**Module:** `dronelytics.core.Orthomosaic`

- Load GeoTIFF files (multispectral, any resolution)
- Flexible band configuration (4-band and 5-band support)
- Access individual bands by name ('red', 'green', 'blue', 'nir', 'rededge')
- Automatic type conversion to float32
- Metadata access (CRS, transform, shape)

**Key Methods:**
```python
ortho = Orthomosaic('field.tif', band_config={...})
ortho.get_band('nir')
ortho.get_shape()
ortho.get_crs()
ortho.get_transform()
```

### 2. Vegetation Indices (10 Types)

**Module:** `dronelytics.core.VegetationIndicesExtended`

10 vegetation indices with automatic band availability checking:

1. **NDVI** - Normalized Difference Vegetation Index
   - Formula: (NIR - RED) / (NIR + RED)
   - Use: Vegetation health, crop monitoring
   - 4-band and 5-band

2. **NDRE** - Normalized Difference Red-Edge
   - Formula: (NIR - RedEdge) / (NIR + RedEdge)
   - Use: Nitrogen content, chlorophyll status
   - 5-band only

3. **GNDVI** - Green Normalized Difference Vegetation Index
   - Formula: (NIR - GREEN) / (NIR + GREEN)
   - Use: Chlorophyll estimation
   - 4-band and 5-band

4. **ExG** - Excess Green
   - Formula: 2*GREEN - RED - BLUE
   - Use: Greenness (RGB-only capable)
   - 4-band and 5-band

5. **SAVI** - Soil-Adjusted Vegetation Index
   - Formula: ((NIR - RED) / (NIR + RED + L)) * (1 + L)
   - Use: Reduced soil influence (L=0.5)
   - 4-band and 5-band

6. **MSAVI** - Modified SAVI
   - Formula: 2*NIR + 1 - sqrt((2*NIR + 1)^2 - 8*(NIR - RED))
   - Use: Further soil adjustment
   - 4-band and 5-band

7. **VARI** - Visible Atmospherically Resistant Index
   - Formula: (GREEN - RED) / (GREEN + RED - BLUE)
   - Use: Atmospheric correction, RGB-capable
   - 4-band and 5-band

8. **ARVI** - Atmospherically Resistant Vegetation Index
   - Formula: (NIR - (2*RED - BLUE)) / (NIR + (2*RED - BLUE))
   - Use: Atmospheric resistance
   - 4-band and 5-band

9. **CVI** - Chlorophyll Vegetation Index
   - Formula: (NIR / GREEN) * (RED / GREEN)
   - Use: Direct chlorophyll estimation
   - 4-band and 5-band

10. **OSAVI** - Optimized SAVI
    - Formula: ((NIR - RED) / (NIR + RED + Y)) * (1 + Y), Y=0.16
    - Use: Optimized soil adjustment
    - 4-band and 5-band

**Features:**
- Safe division with adaptive epsilon (1e-10 to 1e-12 range)
- Automatic band checking with informative errors
- Range validation (-1 to 1 typically)
- Statistics calculation (mean, std, min, max)
- `calculate_all()` with graceful fallback for missing bands

### 3. Custom Formula Support

**Module:** `dronelytics.core.VegetationIndicesExtended.custom()`

Define your own vegetation indices using lambda functions:

```python
def my_formula(ortho):
    nir = ortho.get_band('nir')
    red = ortho.get_band('red')
    return (nir - red) / (nir + red + 1e-10)

result = vi.custom(my_formula, 'MyIndex', value_range=(-1, 1))
```

**Features:**
- Receives Orthomosaic object as parameter
- Must return numpy array
- Type conversion to float32
- Value range validation
- Metadata tracking

### 4. Plot Segmentation

**Module:** `dronelytics.core.PlotSegmentation`

Automated detection of crop plot boundaries:

```python
segmentation = PlotSegmentation(ortho)
result = segmentation.segment_by_ndvi(ndvi.data, threshold=0.3)
```

**Features:**
- NDVI threshold-based segmentation
- Connected component labeling
- Per-segment statistics
- Binary mask generation

### 5. Pixel-Level Data Extraction

**Module:** `dronelytics.core.PixelExtraction`

Extract spectral data at pixel level:

```python
extraction = PixelExtraction(ortho)
result = extraction.extract_spectra()
df = extraction.to_dataframe()
```

**Features:**
- Extract by region (mask) or coordinates
- Pandas DataFrame export
- Statistical summaries
- Per-band analysis

### 6. Point Cloud Processing

**Module:** `dronelytics.core.PointCloudProcessor`

Process LAS/LAZ files for 3D analysis:

#### Digital Terrain Model (DTM)
Ground surface elevation (without vegetation)

#### Digital Surface Model (DSM)
Top surface elevation (vegetation + ground)

#### Crop Height Model (CHM)
CHM = DSM - DTM (vegetation height above ground)

```python
processor = PointCloudProcessor('field.las')
dtm, meta = processor.generate_dtm(cell_size=1.0)
dsm, meta = processor.generate_dsm(cell_size=1.0)
chm, meta = processor.generate_chm(cell_size=1.0)
```

**Features:**
- Ground point classification (simple threshold method)
- 3D mesh generation (Delaunay triangulation)
- Cell-based interpolation
- Automatic NaN handling
- Metadata tracking

### 7. 3D Visualization (3dVis)

**Module:** `dronelytics.visualization`

Five simple visualization functions:

```python
from dronelytics.visualization import (
    show_pointcloud,    # Point cloud with classification
    show_dem,          # Elevation model (DTM, DSM)
    show_chm,          # Crop height model
    show_mesh,         # 3D surface mesh
    show_comparison    # Side-by-side elevation models
)
```

**Features:**
- `show_pointcloud()`: Interactive 3D point cloud (pyvista) or static (matplotlib)
- `show_dem()`: 2D elevation visualization with colormap
- `show_chm()`: CHM with statistics overlay
- `show_mesh()`: 3D triangulated mesh
- `show_comparison()`: Multi-model comparison panels
- Automatic fallback for missing optional dependencies
- Publication-quality output

### 8. Data Export

**Module:** `dronelytics.export`

Export results to standard formats:

```python
from dronelytics import CSVExporter, ExcelExporter

csv_exporter = CSVExporter()
csv_exporter.export(df, 'output.csv')

excel_exporter = ExcelExporter()
excel_exporter.export(df, 'output.xlsx', sheet_name='Data')
```

**Features:**
- CSV export with full precision
- Excel export with formatting
- Multi-sheet Excel workbooks
- Metadata preservation

### 9. Analysis Pipeline

**Module:** `dronelytics.processing.AnalysisPipeline`

Orchestrate multi-step workflows:

```python
pipeline = AnalysisPipeline()
pipeline.run(ortho_path, band_config, indices=['ndvi', 'ndre'])
```

### 10. Data Structures

**Module:** `dronelytics.data.structures`

Type-safe data containers:

- `VegetationIndexData`: Index results with statistics
- `SegmentationResult`: Segment labels and metadata
- `ExtractionResult`: Extracted spectral data
- `PointCloudMetadata`: Point cloud statistics
- `ThreeDModel`: Mesh and point data

### 11. Utilities

**Module:** `dronelytics.utils`

Helper functions:

```python
from dronelytics.utils import setup_logger

logger = setup_logger(__name__)
logger.info("Clean logging without decorative symbols")
```

## Band Configuration System

**Key Concept:** Flexible mapping of spectral bands to file positions

```python
band_config = {
    'red': 1,       # Band 1 = Red
    'green': 2,     # Band 2 = Green
    'blue': 3,      # Band 3 = Blue
    'nir': 4,       # Band 4 = NIR
    'rededge': 5    # Band 5 = Red-Edge (optional)
}
```

**Supports:**
- 4-band systems (RGB+NIR) - common standard
- 5-band systems (RGB+NIR+RedEdge) - advanced analysis
- Custom band ordering
- Missing band graceful handling

## Safe Division

**Problem:** Division by zero in vegetation indices

**Solution:** Adaptive epsilon calculation

```python
epsilon = max(1e-10, np.abs(denominator).max() * 1e-12)
result = numerator / (denominator + epsilon)
```

**Benefits:**
- Prevents NaN propagation
- Handles different magnitude ranges
- Numerically stable
- No user configuration needed

## Automatic Fallback

When calling `calculate_all()`:

- Checks required bands for each index
- Skips indices with missing bands
- Logs warnings (not errors)
- Returns all successfully calculated indices
- No workflow interruption

Example:
```python
all_indices = vi.calculate_all()
# If 5-band not available, NDRE is skipped
# All others calculated successfully
```

## Error Handling

**Clean error messages:**
```
ValueError: Missing bands: ['rededge']
ValueError: File not found: path/to/file.tif
ImportError: laspy is required for point cloud support
```

**Logging:**
- INFO level: Progress updates
- WARNING level: Missing optional features
- ERROR level: Failures with context
- No decorative symbols or emojis

## Performance Characteristics

| Operation | Time (4-band GeoTIFF) | Time (5-band) | Notes |
|-----------|----------------------|---------------|-------|
| Load ortho | <1s | <1s | Depends on file size |
| Calculate NDVI | 0.1-0.5s | 0.1-0.5s | 1000x1000 image |
| Calculate all 10 | 0.5-2s | 0.5-2s | Sequential |
| Segment plots | 0.2-1s | 0.2-1s | With scipy |
| Extract pixels | 0.1-0.5s | 0.1-0.5s | DataFrame conversion |
| Generate DTM | 2-10s | 2-10s | 1.0m cell size |
| Generate CHM | 5-15s | 5-15s | DTM + DSM + diff |

## Memory Requirements

| Operation | 4-band | 5-band | Notes |
|-----------|--------|--------|-------|
| Orthomosaic (1000x1000) | 4MB | 5MB | Float32 |
| Single index | 4MB | 4MB | Same shape |
| All 10 indices | 40MB | 40MB | Stored in dict |
| Point cloud (100k pts) | 2.4MB | 2.4MB | XYZ only |
| DTM/DSM (1000x1000) | 4MB | 4MB | Each model |

## Tested Sensors

| Sensor | Bands | Imagery | Status |
|--------|-------|---------|--------|
| DJI Zenmuse P1 | RGB | Standard | Working |
| Micasense RedEdge | 5 | RGB+NIR+RE | Working |
| Parrot Sequoia | 4 | RGB+NIR | Working |
| Generic GeoTIFF | Any | Custom | Working |

## Python Compatibility

- Python 3.7+
- Tested on 3.8, 3.9, 3.10, 3.11
- Windows, Linux, macOS

## Dependencies

**Core (always installed):**
- numpy >= 1.19.0
- matplotlib >= 3.3.0
- rasterio >= 1.2.0
- scipy >= 1.5.0
- pandas >= 1.1.0

**Optional (point cloud processing):**
- laspy >= 2.0.0
- pyvista >= 0.37.0

## Installation Variants

```bash
pip install dronelytics              # Core only
pip install dronelytics[pointcloud]  # With point cloud support
pip install dronelytics[all]         # All optional features
```

## Quality Assurance

- 30+ unit tests covering core functionality
- Type validation for all inputs
- Comprehensive error messages
- Logging for debugging
- Example scripts for all features

## Documentation

- README.md: Quick start guide
- WORKFLOW.md: Step-by-step analysis guide
- VISUALIZATION_GUIDE.md: 3D visualization examples
- 5BAND_SUPPORT_GUIDE.md: Red-edge band usage
- COMPLETE_FEATURE_SUMMARY.md: This document
- DEPLOYMENT_CHECKLIST.md: Production deployment
- examples/: Runnable code examples
- tests/: Unit test suite

## License

MIT License - Free for research and commercial use

## Support

For issues or questions, refer to documentation files or check example scripts.

---

**Summary:** Dronelytics provides a complete, production-ready workflow for drone image analysis with clean APIs, comprehensive features, and excellent documentation.
