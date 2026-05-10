# Dronelytics Complete Workflow Guide

This guide walks through a complete analysis workflow using dronelytics.

## Overview

Dronelytics provides an end-to-end workflow for:
1. Loading multispectral orthomosaics
2. Calculating vegetation indices
3. Detecting plot boundaries
4. Extracting pixel-level data
5. Processing point clouds
6. Visualizing results

## Step 1: Load Orthomosaic

Define band configuration for your GeoTIFF file:

```python
from dronelytics import Orthomosaic

band_config = {
    'red': 1,       # Red band
    'green': 2,     # Green band
    'blue': 3,      # Blue band
    'nir': 4,       # NIR band
    # 'rededge': 5  # Optional: red-edge for 5-band imagery
}

ortho = Orthomosaic('field.tif', band_config=band_config)
```

## Step 2: Calculate Vegetation Indices

Use the extended vegetation indices class:

```python
from dronelytics import VegetationIndicesExtended

vi = VegetationIndicesExtended(ortho)

ndvi = vi.ndvi()
gndvi = vi.gndvi()
exg = vi.exg()
savi = vi.savi()
msavi = vi.msavi()
vari = vi.vari()
arvi = vi.arvi()
cvi = vi.cvi()
osavi = vi.osavi()

# For 5-band imagery only:
# ndre = vi.ndre()

# Or calculate all at once:
all_indices = vi.calculate_all()
```

## Step 3: Detect Plot Boundaries

Segment plots using NDVI threshold:

```python
from dronelytics import PlotSegmentation

segmentation = PlotSegmentation(ortho)
seg_result = segmentation.segment_by_ndvi(ndvi.data, threshold=0.3)

print(f"Detected {seg_result.num_features} plots")

# Get statistics for a specific segment
stats = segmentation.get_segment_stats(ndvi.data, segment_id=1)
print(f"Plot 1 - Mean NDVI: {stats['mean']:.4f}")
```

## Step 4: Extract Pixel-Level Data

Extract spectral values by region:

```python
from dronelytics import PixelExtraction

extraction = PixelExtraction(ortho)
extract_result = extraction.extract_spectra()

# Convert to DataFrame for analysis
df = extraction.to_dataframe()

# Get statistics
stats = extraction.get_statistics()
for band, values in stats.items():
    print(f"{band}: mean={values['mean']:.2f}, std={values['std']:.2f}")
```

## Step 5: Process Point Cloud

Generate elevation models from LAS data:

```python
from dronelytics import PointCloudProcessor

processor = PointCloudProcessor('field.las')

# Classify ground points
ground_count = processor.classify_ground()

# Generate elevation models
dtm, dtm_meta = processor.generate_dtm(cell_size=1.0)
dsm, dsm_meta = processor.generate_dsm(cell_size=1.0)
chm, chm_meta = processor.generate_chm(cell_size=1.0)

print(f"Mean crop height: {chm_meta['mean_height']:.2f}m")
print(f"Max crop height: {chm_meta['max_height']:.2f}m")

# Generate 3D mesh
mesh = processor.generate_mesh()
```

## Step 6: Visualize Results

Use the 3dVis visualization module:

```python
from dronelytics.visualization import (
    show_pointcloud, show_dem, show_chm,
    show_mesh, show_comparison
)

# Visualize elevation models
show_dem(dtm, title="Ground Surface (DTM)")
show_dem(dsm, title="Top Surface (DSM)")
show_chm(chm, title="Crop Height Model (CHM)")

# Compare models side-by-side
show_comparison(
    {'DTM': dtm, 'DSM': dsm, 'CHM': chm},
    title="Elevation Models"
)

# Visualize 3D mesh
show_mesh(mesh)

# Visualize point cloud with classification
show_pointcloud(processor.points, labels=processor.las.classification)
```

## Complete Workflow Example

```python
from dronelytics import (
    Orthomosaic, VegetationIndicesExtended,
    PlotSegmentation, PixelExtraction,
    PointCloudProcessor
)
from dronelytics.visualization import (
    show_chm, show_dem, show_comparison
)

band_config = {
    'red': 1, 'green': 2, 'blue': 3, 'nir': 4
}

ortho = Orthomosaic('field.tif', band_config=band_config)

vi = VegetationIndicesExtended(ortho)
ndvi = vi.ndvi()
all_indices = vi.calculate_all()

segmentation = PlotSegmentation(ortho)
seg_result = segmentation.segment_by_ndvi(ndvi.data, threshold=0.3)

extraction = PixelExtraction(ortho)
extract_result = extraction.extract_spectra()
df = extraction.to_dataframe()

processor = PointCloudProcessor('field.las')
chm, chm_meta = processor.generate_chm(cell_size=1.0)
dtm, _ = processor.generate_dtm(cell_size=1.0)
dsm, _ = processor.generate_dsm(cell_size=1.0)
mesh = processor.generate_mesh()

print(f"Indices calculated: {list(all_indices.keys())}")
print(f"Plots detected: {seg_result.num_features}")
print(f"Mean NDVI: {ndvi.mean:.4f}")
print(f"Mean crop height: {chm_meta['mean_height']:.2f}m")

show_chm(chm)
show_comparison({'DTM': dtm, 'DSM': dsm, 'CHM': chm})
```

## 5-Band Workflow

For 5-band imagery with red-edge band:

```python
band_config = {
    'red': 1, 'green': 2, 'blue': 3, 'nir': 4, 'rededge': 5
}

ortho = Orthomosaic('field_5band.tif', band_config=band_config)

vi = VegetationIndicesExtended(ortho)
all_indices = vi.calculate_all()

ndvi = vi.ndvi()
ndre = vi.ndre()
gndvi = vi.gndvi()

print(f"NDVI: {ndvi.mean:.4f}")
print(f"NDRE (nitrogen content): {ndre.mean:.4f}")
```

## Custom Vegetation Index

Define your own vegetation index formula:

```python
def my_formula(ortho):
    nir = ortho.get_band('nir')
    red = ortho.get_band('red')
    green = ortho.get_band('green')
    return (nir - green) / (nir + green + 1e-10)

custom_index = vi.custom(
    formula_func=my_formula,
    name='MyCustomIndex',
    description='My custom vegetation formula'
)

print(f"Custom index mean: {custom_index.mean:.4f}")
```

## Data Export

Export results to CSV or Excel:

```python
from dronelytics import CSVExporter, ExcelExporter

csv_exporter = CSVExporter()
csv_exporter.export(df, 'output/extraction_results.csv')

excel_exporter = ExcelExporter()
excel_exporter.export(
    df,
    'output/field_analysis.xlsx',
    sheet_name='Spectral Data'
)
```

## Key Points

- Always specify correct band configuration for your data
- Use `calculate_all()` to skip missing bands automatically
- CHM = DSM - DTM (crop height above ground)
- NDVI ranges from -1 to 1 (vegetation only positive)
- Custom formulas receive Orthomosaic object as parameter
- Point cloud processing requires laspy (optional install)
- Visualization requires matplotlib and optionally pyvista

## Common Issues

**Missing band error**: Check band configuration matches your file structure

**Division by zero**: All methods use safe division automatically

**Memory issues**: Process large files by tiling or reducing resolution

**No ground points**: Adjust ground classification threshold if needed

## Next Steps

- See `VISUALIZATION_GUIDE.md` for interactive 3D visualization
- See `5BAND_SUPPORT_GUIDE.md` for red-edge band usage
- Check examples/ directory for complete runnable scripts
