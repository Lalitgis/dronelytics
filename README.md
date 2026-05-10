# Dronelytics

Comprehensive Python package for end-to-end drone orthomosaic analysis and agricultural field phenotyping.

## Features

Dronelytics provides a complete workflow for processing multispectral drone imagery and point clouds:

- **Multispectral Orthomosaic Processing**: Load and manage 4-band (RGB+NIR) and 5-band (RGB+NIR+RedEdge) GeoTIFF files
- **10 Vegetation Indices**: NDVI, NDRE, GNDVI, ExG, SAVI, MSAVI, VARI, ARVI, CVI, OSAVI
- **Custom Formula Support**: Define your own vegetation index formulas using lambda functions
- **Plot Segmentation**: Automated detection and boundary extraction of crop plots
- **Pixel-Level Extraction**: Extract spectral data by plot or region
- **3D Canopy Modeling**: Generate DTM, DSM, and CHM from point clouds
- **3D Visualization**: Interactive and static visualization of point clouds, elevation models, and meshes
- **Data Export**: Save results to CSV and Excel formats

## Installation

Install from PyPI:

```bash
pip install dronelytics
```

For point cloud processing support (optional):

```bash
pip install dronelytics[pointcloud]
```

This installs additional dependencies for LAS file handling and 3D mesh generation.

## Quick Start

### Load Orthomosaic and Calculate Vegetation Indices

```python
from dronelytics import Orthomosaic, VegetationIndicesExtended

ortho = Orthomosaic('field.tif', band_config={
    'red': 1, 'green': 2, 'blue': 3, 'nir': 4
})

vi = VegetationIndicesExtended(ortho)
ndvi = vi.ndvi()
gndvi = vi.gndvi()
exg = vi.exg()

print(f"NDVI Mean: {ndvi.mean:.4f}")
print(f"GNDVI Mean: {gndvi.mean:.4f}")
```

### Process 5-Band Imagery with Red-Edge

```python
ortho = Orthomosaic('field_5band.tif', band_config={
    'red': 1, 'green': 2, 'blue': 3, 'nir': 4, 'rededge': 5
})

vi = VegetationIndicesExtended(ortho)
ndvi = vi.ndvi()
ndre = vi.ndre()
all_indices = vi.calculate_all()
```

### Detect Plots and Extract Data

```python
from dronelytics import PlotSegmentation, PixelExtraction

segmentation = PlotSegmentation(ortho)
seg_result = segmentation.segment_by_ndvi(ndvi.data, threshold=0.3)

extraction = PixelExtraction(ortho)
extract_result = extraction.extract_spectra()
df = extraction.to_dataframe()
```

### Process Point Cloud and Generate CHM

```python
from dronelytics import PointCloudProcessor

processor = PointCloudProcessor('field.las')

chm, meta = processor.generate_chm(cell_size=1.0)
dtm, _ = processor.generate_dtm(cell_size=1.0)
dsm, _ = processor.generate_dsm(cell_size=1.0)

print(f"Mean crop height: {meta['mean_height']:.2f}m")
```

### Visualize Results

```python
from dronelytics.visualization import show_chm, show_comparison

show_chm(chm, title="Crop Height Model")
show_comparison({'DTM': dtm, 'DSM': dsm, 'CHM': chm})
```

### Custom Vegetation Index

```python
def my_formula(ortho):
    nir = ortho.get_band('nir')
    red = ortho.get_band('red')
    return (nir - red) / (nir + red + 1e-10)

custom = vi.custom(my_formula, 'MyIndex')
```

## Band Configuration

Specify how bands are mapped in your GeoTIFF file:

```python
band_config = {
    'red': 1,       # Band 1 is red
    'green': 2,     # Band 2 is green
    'blue': 3,      # Band 3 is blue
    'nir': 4,       # Band 4 is NIR
    'rededge': 5    # Band 5 is red-edge (optional, 5-band only)
}

ortho = Orthomosaic('field.tif', band_config=band_config)
```

## Vegetation Indices

10 vegetation indices are implemented:

| Index | Formula | Use Case |
|-------|---------|----------|
| NDVI | (NIR - RED) / (NIR + RED) | Vegetation health, stress detection |
| NDRE | (NIR - RedEdge) / (NIR + RedEdge) | Nitrogen content (5-band only) |
| GNDVI | (NIR - GREEN) / (NIR + GREEN) | Chlorophyll content |
| ExG | 2*GREEN - RED - BLUE | Greenness index for RGB imagery |
| SAVI | ((NIR - RED) / (NIR + RED + L)) * (1 + L) | Soil adjustment (L=0.5) |
| MSAVI | Modified SAVI | Improved soil adjustment |
| VARI | (GREEN - RED) / (GREEN + RED - BLUE) | Visible atmospherically resistant |
| ARVI | (NIR - (2*RED - BLUE)) / (NIR + (2*RED - BLUE)) | Atmospheric correction |
| CVI | (NIR / GREEN) * (RED / GREEN) | Chlorophyll |
| OSAVI | Optimized SAVI with Y=0.16 | Better soil adjustment |

## 3D Visualization Functions

The visualization module (3dVis) provides 5 simple functions:

```python
from dronelytics.visualization import (
    show_pointcloud,    # Visualize point cloud with classification
    show_dem,          # Visualize elevation models (DTM, DSM)
    show_chm,          # Visualize crop height model
    show_mesh,         # Visualize 3D surface mesh
    show_comparison    # Compare multiple elevation models
)
```

## File Structure

```
dronelytics/
├── core/                      # Core modules
│   ├── orthomosaic.py        # Orthomosaic loading and management
│   ├── indices.py            # Standard vegetation indices
│   ├── vegetation_indices_extended.py  # 10 indices + custom formulas
│   ├── segmentation.py       # Plot boundary detection
│   ├── extraction.py         # Pixel-level data extraction
│   └── pointcloud.py         # Point cloud processing, DTM/DSM/CHM
│
├── visualization/            # 3D visualization (3dVis)
│   └── vis3d.py             # 5 visualization functions
│
├── export/                  # Data export
│   ├── csv_export.py        # CSV export
│   └── excel_export.py      # Excel export
│
├── processing/              # Analysis pipelines
│   └── pipeline.py          # Orchestrate analysis workflow
│
├── data/                    # Data structures
│   └── structures.py        # VegetationIndexData, SegmentationResult, etc.
│
└── utils/                   # Utilities
    └── logger.py            # Clean logging (no decorative symbols)
```

## Examples

### Basic Workflow

```bash
python examples/basic_workflow.py
```

### Advanced Workflow (5-band, Point Cloud)

```bash
python examples/advanced_workflow.py
```

### 3D Visualization

```bash
python examples/visualization_example.py
```

## Requirements

- Python 3.7+
- numpy
- rasterio (GeoTIFF support)
- matplotlib (visualization)
- scipy (segmentation)
- pandas (data extraction)

Optional dependencies:
- laspy (LAS/LAZ file support)
- pyvista (3D mesh and interactive visualization)

## Testing

Run unit tests:

```bash
python -m pytest tests/test_core.py
```

Or use the test module directly:

```bash
python tests/test_core.py
```

## CHM Calculation

Crop Height Model (CHM) is calculated as:

```
CHM = DSM - DTM
```

Where:
- DSM: Digital Surface Model (top of vegetation)
- DTM: Digital Terrain Model (ground surface)
- CHM: Height of vegetation above ground

## Documentation

- `WORKFLOW.md`: Complete analysis workflow guide
- `VISUALIZATION_GUIDE.md`: 3D visualization usage
- `5BAND_SUPPORT_GUIDE.md`: Red-edge band support
- `COMPLETE_FEATURE_SUMMARY.md`: Feature overview
- `DEPLOYMENT_CHECKLIST.md`: Production deployment guide

## License

MIT License. See LICENSE file for details.

## Citation

If you use Dronelytics in your research, please cite:

```
Dronelytics v1.0.0 - Comprehensive drone orthomosaic analysis package
```

## Support

For issues, feature requests, or questions, please refer to the documentation files or create an issue on GitHub.

---

Made for agricultural field phenotyping and precision agriculture research.
