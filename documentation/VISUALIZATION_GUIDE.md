# 3D Visualization Guide (3dVis)

The dronelytics visualization module (3dVis) provides five simple functions for visualizing orthomosaic and point cloud data.

## Visualization Functions

### 1. show_pointcloud()

Visualize point cloud data with optional classification.

```python
from dronelytics.visualization import show_pointcloud

processor = PointCloudProcessor('field.las')

# Simple point cloud
show_pointcloud(processor.points, title="Point Cloud")

# With classification labels
show_pointcloud(
    processor.points,
    labels=processor.las.classification,
    title="Point Cloud with Classification"
)
```

**Features:**
- Interactive 3D visualization with pyvista (if installed)
- Falls back to matplotlib 3D scatter plot
- Color by classification or labels
- Rotate, zoom, pan controls

### 2. show_dem()

Visualize Digital Elevation Models (DTM or DSM).

```python
from dronelytics.visualization import show_dem

dtm, _ = processor.generate_dtm(cell_size=1.0)
dsm, _ = processor.generate_dsm(cell_size=1.0)

show_dem(dtm, title="Digital Terrain Model (Ground)")
show_dem(dsm, title="Digital Surface Model (Vegetation)")
show_dem(dtm, cmap='viridis', title="DTM with Viridis")
```

**Parameters:**
- `dem`: 2D elevation array
- `title`: Plot title
- `cmap`: Colormap (default: 'terrain')

**Colormaps:**
- 'terrain': Brown to green
- 'viridis': Purple to yellow
- 'hot': Black to red
- 'cool': Cyan to magenta

### 3. show_chm()

Visualize Crop Height Model with statistics.

```python
from dronelytics.visualization import show_chm

chm, chm_meta = processor.generate_chm(cell_size=1.0)

show_chm(chm, title="Crop Height Model")
show_chm(chm, cmap='RdYlGn', title="CHM - Green Yellow Red")
```

**Features:**
- Color-coded height values
- Displays min/max/mean statistics
- RdYlGn colormap (red for low, green for high)
- Handles NaN values automatically

### 4. show_mesh()

Visualize 3D surface mesh generated from point cloud.

```python
from dronelytics.visualization import show_mesh

mesh = processor.generate_mesh()

show_mesh(mesh, title="3D Surface Mesh")
```

**Features:**
- Interactive 3D rotation
- Requires pyvista (install with: pip install pyvista)
- Delaunay triangulation of point cloud
- Gray edges show mesh structure

### 5. show_comparison()

Compare multiple elevation models side-by-side.

```python
from dronelytics.visualization import show_comparison

dtm, _ = processor.generate_dtm(cell_size=1.0)
dsm, _ = processor.generate_dsm(cell_size=1.0)
chm, _ = processor.generate_chm(cell_size=1.0)

show_comparison(
    {'DTM': dtm, 'DSM': dsm},
    title="Ground vs Top Surface"
)

show_comparison(
    {'DTM': dtm, 'DSM': dsm, 'CHM': chm},
    title="Elevation Models Comparison"
)
```

**Features:**
- Side-by-side visualization
- Same colormap for all models
- Individual colorbars
- Automatic layout based on number of models

## Complete Visualization Workflow

```python
from dronelytics import PointCloudProcessor
from dronelytics.visualization import (
    show_pointcloud, show_dem, show_chm,
    show_mesh, show_comparison
)

processor = PointCloudProcessor('field.las')

# 1. Classify ground points
processor.classify_ground()

# 2. Generate elevation models
dtm, _ = processor.generate_dtm(cell_size=1.0)
dsm, _ = processor.generate_dsm(cell_size=1.0)
chm, _ = processor.generate_chm(cell_size=1.0)

# 3. Generate mesh
mesh = processor.generate_mesh()

# 4. Visualize
show_pointcloud(
    processor.points,
    labels=processor.las.classification,
    title="Point Cloud with Classification"
)

show_dem(dtm, title="Ground Surface (DTM)")
show_dem(dsm, title="Top Surface (DSM)")
show_chm(chm, title="Crop Height Model")
show_mesh(mesh)
show_comparison(
    {'DTM': dtm, 'DSM': dsm, 'CHM': chm},
    title="All Elevation Models"
)

processor.close()
```

## Customization Options

### Point Cloud Visualization

```python
# Interactive (pyvista)
show_pointcloud(points, labels=labels)

# Static with matplotlib
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=labels, s=1)
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
plt.show()
```

### DEM with Custom Colormap

```python
show_dem(dtm, cmap='coolwarm')
show_dem(dsm, cmap='gray')
show_dem(chm, cmap='YlGn')
```

### Multi-Model Comparison

```python
# Compare many models
data_dict = {
    'DTM': dtm,
    'DSM': dsm,
    'CHM': chm,
    'Slope': np.gradient(dtm)[0]
}
show_comparison(data_dict, title="Complete Analysis")
```

## Installation Requirements

### Basic Visualization (Matplotlib)

```bash
pip install dronelytics
```

Includes: matplotlib for 2D elevation visualization

### Interactive 3D (PyVista)

```bash
pip install dronelytics[pointcloud]
```

Includes: laspy + pyvista for interactive 3D visualization

### Manual Installation

If you need to install visualization separately:

```bash
pip install matplotlib
pip install pyvista  # Optional for interactive 3D
```

## Output Examples

### DTM Visualization
- Brown/low terrain in valleys
- Green/high terrain on ridges
- Colorbar shows elevation in meters

### CHM Visualization
- Green: Low vegetation height (0-1m)
- Yellow: Medium vegetation (1-2m)
- Red: High vegetation (>2m)
- Statistics panel shows min/max/mean

### Comparison Layout
- 2 models: side-by-side
- 3 models: left-center-right
- 4+ models: grid layout

## Tips

1. **Large files**: Downsample for faster visualization
2. **Color schemes**: Use terrain for DEMs, RdYlGn for CHM
3. **Interactive viewing**: Use pyvista for rotation/zoom
4. **Batch visualization**: Save figures with matplotlib's savefig()
5. **Publication quality**: Adjust figure size and DPI

## Troubleshooting

**Blank window**: Try different figure size or colormap
**Import error for pyvista**: Install with `pip install pyvista`
**Memory error**: Reduce point cloud resolution or use smaller tiles
**No colorbar**: Ensure data is not all NaN

## See Also

- `WORKFLOW.md`: Complete analysis workflow
- `5BAND_SUPPORT_GUIDE.md`: Red-edge band analysis
- `examples/visualization_example.py`: Runnable examples
