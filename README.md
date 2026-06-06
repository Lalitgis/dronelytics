# Dronelytics

<p align="center">
  <img src="icon.png" alt="Dronelytics Logo" width="180">
</p>

<p align="center">
  <strong>Drone Orthomosaic Analysis and Agricultural Field Phenotyping in Python</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/dronelytics/">
    <img src="https://img.shields.io/pypi/v/dronelytics.svg" alt="PyPI">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/dronelytics.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
</p>

---

Dronelytics is a comprehensive Python package for processing multispectral drone imagery and LAS/LAZ point clouds. It provides production-ready tools for vegetation analysis, automated plot detection, spectral data extraction, digital elevation modeling, and 3D visualization.

Built for researchers, agronomists, and GIS professionals who need fast, reliable analysis of drone data.

---

## 🎯 Use Cases

- **Precision Agriculture** - Crop health monitoring and variable-rate application mapping
- **Crop Phenotyping** - Automated trait extraction from experimental plots
- **Plant Breeding** - Large-scale genotype evaluation and selection
- **Environmental Monitoring** - Wetland and vegetation change detection
- **Crop Insurance** - Automated damage assessment and loss evaluation
- **Remote Sensing Research** - Multispectral algorithm development and validation

---

## ✨ Key Features

### Orthomosaic Processing
- ✅ RGB, RGB+NIR, and RGB+NIR+Red-Edge imagery support
- ✅ GeoTIFF-based workflows with metadata preservation
- ✅ Flexible multi-band configuration
- ✅ Efficient memory management for large files

### Vegetation Analysis
10+ vegetation indices including:
- **NDVI** - Normalized Difference Vegetation Index (general vegetation health)
- **NDRE** - Normalized Difference Red Edge Index (crop stress detection)
- **GNDVI** - Green NDVI (chlorophyll content)
- **VARI** - Visible Atmospherically Resistant Index (early season analysis)
- **EVI** - Enhanced Vegetation Index (canopy structure)
- Plus 5 more: SAVI, MSAVI, ARVI, CVI, OSAVI

### Automated Plot Segmentation
- Boundary detection from orthomosaics
- Three segmentation methods (watershed, quickshift, felzenszwalb)
- Plot-level statistics computation
- GeoJSON export for GIS integration

### Spectral Data Extraction
- Pixel-level vegetation index values
- Per-plot summary statistics (mean, std, min, max, median)
- Integration of multiple indices
- CSV and Excel export

### Point Cloud Processing
- Digital Terrain Model (DTM) generation
- Digital Surface Model (DSM) generation
- Canopy Height Model (CHM) calculation
- 3D mesh generation from LAS/LAZ files
- GeoTIFF and STL export formats

### Data Export
- CSV (pixel-level data)
- Excel with multiple sheets (pixel data + statistics + metadata)
- GeoJSON (vector boundaries)
- GeoTIFF (raster models)
- STL (3D mesh models)

---

## 📦 Installation

### Basic Installation (Orthomosaic & Vegetation Indices)
```bash
pip install dronelytics
```

### Full Installation (Includes Point Cloud Support)
```bash
pip install dronelytics[pointcloud]
```

### Development Installation
```bash
git clone https://github.com/Lalitgis/dronelytics.git
cd dronelytics
pip install -e ".[pointcloud]"
```

### Verify Installation
```bash
python -c "from dronelytics import Orthomosaic, VegetationIndices, PlotSegmentation; print('✓ Dronelytics installed successfully')"
```

---

## 🚀 Quick Start

### Example 1: Calculate Vegetation Indices

```python
from dronelytics import Orthomosaic, VegetationIndices

# Load orthomosaic with band configuration
band_config = {
    'red': 1,
    'green': 2,
    'blue': 3,
    'nir': 4,
    'red_edge': 5  # Optional: for 5-band imagery
}

ortho = Orthomosaic('field_image.tif', band_config=band_config)

# Calculate vegetation indices
vi = VegetationIndices(ortho)

ndvi = vi.calculate_ndvi()
print(f"NDVI Mean: {ndvi.mean:.4f} ± {ndvi.std:.4f}")
print(f"Valid Pixels: {ndvi.pixel_count}")

# Other indices
ndre = vi.calculate_ndre()
gndvi = vi.calculate_gndvi()
vari = vi.calculate_vari()
```

### Example 2: Detect Plot Boundaries

```python
from dronelytics import PlotSegmentation

segmentation = PlotSegmentation(ortho)

# Detect plots using watershed method (recommended for NDVI)
result = segmentation.segment_by_ndvi(
    method='watershed',
    min_plot_size=100
)

print(f"Detected {result.num_plots} plots")
print(f"Boundaries: {len(result.boundaries)}")

# Export as GeoJSON
gdf = segmentation.get_boundaries_geodataframe()
gdf.to_file('plot_boundaries.geojson', driver='GeoJSON')
```

### Example 3: Extract Plot-Level Statistics

```python
from dronelytics import PixelExtraction

extraction = PixelExtraction(ortho)

# Extract vegetation indices for each plot
result = extraction.extract_from_segmentation(
    segmentation_result=result,
    vegetation_indices={
        'ndvi': ndvi.values,
        'ndre': ndre.values,
        'gndvi': gndvi.values
    },
    raw_bands=['red', 'nir']
)

# Get summary statistics
summary = extraction.summarize_by_plot()
summary.to_csv('plot_statistics.csv', index=False)

# Export to Excel with multiple sheets
from dronelytics import ExcelExporter
exporter = ExcelExporter()
exporter.export(
    output_path='analysis_results.xlsx',
    pixel_data=extraction.to_dataframe(),
    plot_stats=extraction.get_plot_statistics(),
    vegetation_indices={'ndvi': ndvi, 'ndre': ndre}
)
```

### Example 4: Process Point Cloud Data

```python
from dronelytics import PointCloudProcessor

pc = PointCloudProcessor('lidar_data.las')

# Generate elevation models
dtm, dtm_meta = pc.generate_dem(resolution=0.1, method='ground')
dsm, dsm_meta = pc.generate_dem(resolution=0.1, method='all')

# Generate canopy height model
chm, chm_meta = pc.generate_chm(resolution=0.1)

# Export as GeoTIFF
pc.export_dem_as_tiff(dtm, 'dtm.tif', resolution=0.1)
pc.export_dem_as_tiff(chm, 'chm.tif', resolution=0.1)

# Create 3D mesh
mesh = pc.create_3d_mesh(point_type='vegetation')
pc.export_mesh_as_stl(mesh, 'canopy_3d.stl')
```

---

## 📋 Band Configuration Guide

The `band_config` parameter maps band names to their position in your image. 

### Common Configurations

**Multispectral Drone (4-band: RGB+NIR)**
```python
band_config = {
    'red': 1,
    'green': 2,
    'blue': 3,
    'nir': 4
}
```

**Multispectral Drone (5-band: RGB+NIR+Red-Edge)**
```python
band_config = {
    'red': 1,
    'green': 2,
    'blue': 3,
    'nir': 4,
    'red_edge': 5  # Use 'red_edge' (with underscore)
}
```

**Satellite Imagery (Landsat 8)**
```python
band_config = {
    'blue': 2,
    'green': 3,
    'red': 4,
    'nir': 5,
    'swir_1': 6,
    'swir_2': 7
}
```

### How to Find Your Band Order

```bash
# Using GDAL (command line):
gdalinfo your_file.tif | grep "Band"

# Using Python:
import rasterio
with rasterio.open('your_file.tif') as src:
    print(f"Number of bands: {src.count}")
    for i in range(1, src.count + 1):
        print(f"Band {i}: {src.descriptions[i-1]}")
```

---

## 🔬 Vegetation Indices Reference

| Index | Formula | Best For | Range |
|-------|---------|----------|-------|
| **NDVI** | (NIR - RED) / (NIR + RED) | General vegetation health | -1 to +1 |
| **NDRE** | (NIR - RedEdge) / (NIR + RedEdge) | Crop stress detection | -1 to +1 |
| **GNDVI** | (NIR - GREEN) / (NIR + GREEN) | Chlorophyll content | -1 to +1 |
| **VARI** | (GREEN - RED) / (GREEN + RED - BLUE) | Early season analysis | -1 to +1 |
| **EVI** | 2.5 * (NIR - RED) / (NIR + 6*RED - 7.5*BLUE + 1) | Canopy structure | -1 to +1 |
| **SAVI** | 1.5 * (NIR - RED) / (NIR + RED + 0.5) | Soil-adjusted | -1 to +1 |

---

## 📊 Segmentation Methods

### Choosing the Right Method

| Method | Input | Best For | Speed | Quality |
|--------|-------|----------|-------|---------|
| **watershed** | NDVI/index | Regular, distinct plots | Fast | Excellent |
| **felzenszwalb** | NDVI/index | Complex, irregular boundaries | Fast | Very Good |
| **quickshift** | RGB image (3-band) | Fine-scale details | Slow | Excellent |

### Quickshift (For RGB Images)

Use when you have RGB data and want fine-scale segmentation:

```python
# First, prepare RGB data (not NDVI)
import numpy as np
rgb = np.stack([ortho.get_band('red'),
                ortho.get_band('green'),
                ortho.get_band('blue')], axis=2)

# Normalize to 0-1 range
rgb = (rgb - rgb.min()) / (rgb.max() - rgb.min())

# Use custom implementation
from skimage import segmentation
labeled = segmentation.quickshift(rgb, kernel_size=15, max_dist=40)
```

### Watershed (Recommended for NDVI)

Use when you have NDVI or other vegetation indices:

```python
result = segmentation.segment_by_ndvi(
    method='watershed',
    min_plot_size=100  # Minimum pixels per plot
)
```

### Felzenszwalb (For Complex Boundaries)

Use for varying plot sizes or irregular boundaries:

```python
result = segmentation.segment_by_ndvi(
    method='felzenszwalb',
    scale=500,      # Larger = fewer, larger regions
    sigma=0.5       # Smoothing parameter
)
```

---

## 📈 Complete Workflow Example

```python
import logging
from dronelytics import (
    Orthomosaic, VegetationIndices, PlotSegmentation,
    PixelExtraction, ExcelExporter, setup_logger
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = setup_logger('field_analysis')

try:
    # 1. Load orthomosaic
    logger.info("Loading orthomosaic...")
    ortho = Orthomosaic('field_image.tif', band_config={
        'red': 1,
        'green': 2,
        'blue': 3,
        'nir': 4,
        'red_edge': 5
    })
  
    # 2. Calculate vegetation indices
    logger.info("Calculating vegetation indices...")
    vi = VegetationIndices(ortho)
    ndvi = vi.calculate_ndvi()
    ndre = vi.calculate_ndre()
    gndvi = vi.calculate_gndvi()
    logger.info(f"NDVI: Mean={ndvi.mean:.3f}, Std={ndvi.std:.3f}")
  
    # 3. Detect plot boundaries
    logger.info("Detecting plot boundaries...")
    segmentation = PlotSegmentation(ortho)
    seg_result = segmentation.segment_by_ndvi(method='watershed', min_plot_size=100)
    logger.info(f"Detected {seg_result.num_plots} plots")
  
    # 4. Extract spectral data
    logger.info("Extracting pixel values...")
    extraction = PixelExtraction(ortho)
    ext_result = extraction.extract_from_segmentation(
        segmentation_result=seg_result,
        vegetation_indices={'ndvi': ndvi.values, 'ndre': ndre.values, 'gndvi': gndvi.values},
        raw_bands=['red', 'nir']
    )
    logger.info(f"Extracted {len(ext_result.pixels)} pixels")
  
    # 5. Generate reports
    logger.info("Generating reports...")
    extraction.to_csv('pixel_data.csv')
    summary = extraction.summarize_by_plot()
    summary.to_csv('plot_summary.csv', index=False)
  
    exporter = ExcelExporter()
    exporter.export(
        output_path='field_analysis.xlsx',
        pixel_data=extraction.to_dataframe(),
        plot_stats=extraction.get_plot_statistics(),
        vegetation_indices={'ndvi': ndvi, 'ndre': ndre, 'gndvi': gndvi},
        orthomosaic_metadata=ortho.metadata
    )
  
    # 6. Export boundaries
    logger.info("Exporting boundaries...")
    gdf = segmentation.get_boundaries_geodataframe()
    gdf.to_file('plot_boundaries.geojson', driver='GeoJSON')
  
    logger.info("✓ Analysis complete!")
    
except Exception as e:
    logger.error(f"Analysis failed: {e}", exc_info=True)
finally:
    ortho.close()
```

---

## ⚙️ Advanced Configuration

### Handling Large Files

For files larger than 2GB, consider tiling:

```python
# Process in tiles to manage memory
ortho = Orthomosaic('large_file.tif', band_config=band_config)
try:
    # Your processing code here
    ...
finally:
    ortho.clear_cache()  # Free memory
    ortho.close()
```

### Batch Processing Multiple Files

```python
import glob
from pathlib import Path

tif_files = glob.glob('data/*.tif')

for tif_file in tif_files:
    logger.info(f"Processing {Path(tif_file).stem}...")
    
    ortho = Orthomosaic(tif_file, band_config=band_config)
    vi = VegetationIndices(ortho)
    ndvi = vi.calculate_ndvi()
    
    # Export results
    output_file = f"results/{Path(tif_file).stem}_ndvi.tif"
    # ... save results
    
    ortho.close()
```

### Custom Vegetation Index

```python
# Define your own formula
def custom_index(ortho):
    red = ortho.get_band('red').astype(float)
    nir = ortho.get_band('nir').astype(float)
    
    # Your custom formula
    index = (nir - red) / (nir + red + 1e-8)
    return index

custom = custom_index(ortho)
```

---

## 🐛 Troubleshooting

### ModuleNotFoundError: No module named 'skimage'

**Solution:** Install with point cloud support:
```bash
pip install dronelytics[pointcloud]
# or manually:
pip install scikit-image geopandas shapely openpyxl
```

### ValueError: Missing bands: ['red_edge']

**Problem:** Band named 'rededge' but code expects 'red_edge'

**Solution:** Use correct band name with underscore:
```python
band_config = {
    # ...
    'red_edge': 5  # Use 'red_edge' (with underscore)
}
```

### ValueError: Only RGB images can be converted to Lab space

**Problem:** Trying to use quickshift method with NDVI data (1-band)

**Solution:** Use watershed instead or prepare RGB data:
```python
# Option 1 (Recommended):
result = segmentation.segment_by_ndvi(method='watershed')

# Option 2: Use RGB data with quickshift
rgb = np.stack([ortho.get_band('red'),
                ortho.get_band('green'),
                ortho.get_band('blue')], axis=2)
```

### MemoryError on Large Files

**Solution 1:** Use smaller tile size
```python
ortho = Orthomosaic('file.tif', band_config=band_config)
ortho.clear_cache()  # Free memory between operations
```

**Solution 2:** Process in tiles or use a machine with more RAM

### FileNotFoundError: File not found

**Check:**
```python
from pathlib import Path
file = Path('your_file.tif')
print(f"File exists: {file.exists()}")
print(f"Absolute path: {file.absolute()}")
```

---

## 📚 API Reference

### Core Classes

**Orthomosaic**
```python
ortho = Orthomosaic(filepath, band_config)
ortho.get_band(name)           # Get single band as numpy array
ortho.close()                  # Free resources
ortho.clear_cache()            # Clear cached data
```

**VegetationIndices**
```python
vi = VegetationIndices(ortho)
ndvi = vi.calculate_ndvi()     # Returns IndexResult
ndre = vi.calculate_ndre()
gndvi = vi.calculate_gndvi()
# ... and more
```

**PlotSegmentation**
```python
seg = PlotSegmentation(ortho)
result = seg.segment_by_ndvi(method='watershed')
gdf = seg.get_boundaries_geodataframe()  # Export to GeoJSON
```

**PixelExtraction**
```python
ext = PixelExtraction(ortho)
result = ext.extract_from_segmentation(segmentation_result, vegetation_indices)
df = ext.to_dataframe()
ext.to_csv('output.csv')
```

**PointCloudProcessor**
```python
pc = PointCloudProcessor('data.las')
dtm, dtm_meta = pc.generate_dem(resolution=0.1, method='ground')
mesh = pc.create_3d_mesh()
pc.export_mesh_as_stl(mesh, 'output.stl')
```

---

## 📝 Data Export Formats

| Format | Use Case | Function |
|--------|----------|----------|
| **CSV** | Pixel-level data, easy to analyze | `extraction.to_csv()` |
| **Excel** | Summary reports, multi-sheet | `ExcelExporter.export()` |
| **GeoJSON** | GIS integration, vector boundaries | `gdf.to_file(..., 'GeoJSON')` |
| **GeoTIFF** | Raster models, elevation data | `pc.export_dem_as_tiff()` |
| **STL** | 3D visualization, 3D printing | `pc.export_mesh_as_stl()` |

---

## 🔗 Dependencies

### Core (Always Installed)
- numpy (numerical computing)
- pandas (data manipulation)
- rasterio (geospatial I/O)
- scipy (scientific computing)
- matplotlib (visualization)

### Segmentation & Geometry
- scikit-image (image processing algorithms)
- geopandas (vector data handling)
- shapely (geometry operations)

### Data Export
- openpyxl (Excel file handling)

### Point Cloud Support (Optional)
- laspy (LAS/LAZ file reading)
- pyvista (3D visualization)

---

## 💡 Best Practices

1. **Always define band_config explicitly** - Don't rely on defaults
2. **Use watershed for NDVI** - Quickshift requires RGB preprocessing
3. **Test on small files first** - Before processing large datasets
4. **Handle exceptions** - Use try/finally to ensure ortho.close() is called
5. **Enable logging** - Helps debug issues and monitor progress
6. **Export results** - Keep original data and generated indices separate

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 📧 Support

- **Documentation:** https://github.com/Lalitgis/dronelytics/wiki
- **Issues:** https://github.com/Lalitgis/dronelytics/issues
- **Email:** lalitiaas@gmail.com

---

## 🎓 Citation

If you use Dronelytics in your research, please cite:

```bibtex
@software{dronelytics2026,
  author = {BC, Lalit},
  title = {Dronelytics: Comprehensive Drone Orthomosaic Analysis and Agricultural Field Phenotyping Toolkit},
  year = {2026},
  version = {1.0.3},
  url = {https://github.com/Lalitgis/dronelytics}
}
```

---

## 🚀 Roadmap

- [ ] GPU acceleration for large-scale processing
- [ ] Web interface for remote processing
- [ ] Machine learning model integration
- [ ] Hyperspectral image support
- [ ] Real-time drone feed processing
- [ ] Cloud storage integration (AWS S3, Azure)

---

**Made with ❤️ for agricultural researchers and GIS professionals**
