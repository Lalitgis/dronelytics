# 5-Band Imagery Support Guide

Dronelytics supports both 4-band (RGB+NIR) and 5-band (RGB+NIR+RedEdge) multispectral imagery for comprehensive crop analysis.

## 4-Band vs 5-Band

### 4-Band System (Standard)
- Band 1: Red (R)
- Band 2: Green (G)
- Band 3: Blue (B)
- Band 4: Near-Infrared (NIR)

**Available indices:** NDVI, GNDVI, ExG, SAVI, MSAVI, VARI, ARVI, CVI, OSAVI (9 indices)

### 5-Band System (Extended)
- Band 1: Red (R)
- Band 2: Green (G)
- Band 3: Blue (B)
- Band 4: Near-Infrared (NIR)
- Band 5: Red-Edge (RE)

**Additional index:** NDRE for advanced nitrogen/chlorophyll estimation
**Total available:** 10 indices

## Setting Up 5-Band Imagery

### Step 1: Configure Band Mapping

```python
from dronelytics import Orthomosaic

band_config = {
    'red': 1,
    'green': 2,
    'blue': 3,
    'nir': 4,
    'rededge': 5
}

ortho = Orthomosaic('field_5band.tif', band_config=band_config)
```

**Important:** Adjust band numbers to match your actual GeoTIFF structure.

### Step 2: Calculate 5-Band Indices

```python
from dronelytics import VegetationIndicesExtended

vi = VegetationIndicesExtended(ortho)

ndvi = vi.ndvi()
ndre = vi.ndre()

all_indices = vi.calculate_all()
```

When you call `calculate_all()` with 5-band data, it automatically includes NDRE.

## Red-Edge Band Applications

The red-edge band (700-750 nm) is sensitive to chlorophyll and nitrogen content, enabling:

| Application | Index | Formula |
|-------------|-------|---------|
| Nitrogen content | NDRE | (NIR - RE) / (NIR + RE) |
| Chlorophyll status | GNDVI | (NIR - GREEN) / (NIR + GREEN) |
| Stress detection | NDVI vs NDRE | Ratio of indices |

## NDRE Index Details

Normalized Difference Red-Edge Index

```
NDRE = (NIR - RedEdge) / (NIR + RedEdge)
```

### Characteristics
- Range: -1 to 1 (same as NDVI)
- More sensitive to nitrogen than NDVI
- 5-band imagery only
- Complements NDVI for precision agriculture

### Interpretation
- NDRE > 0.6: High nitrogen, healthy crop
- NDRE 0.4-0.6: Medium nitrogen status
- NDRE < 0.4: Low nitrogen, potential stress

### Use Cases
1. **Nitrogen management**: Optimize fertilizer application
2. **Crop monitoring**: Early stress detection
3. **Variety comparison**: Compare cultivar performance
4. **Field variability**: Identify problem areas

## Complete 5-Band Workflow

```python
from dronelytics import Orthomosaic, VegetationIndicesExtended
from dronelytics.export import ExcelExporter

band_config = {
    'red': 1,
    'green': 2,
    'blue': 3,
    'nir': 4,
    'rededge': 5
}

ortho = Orthomosaic('field_5band.tif', band_config=band_config)

vi = VegetationIndicesExtended(ortho)

print("Calculating 4-band indices...")
ndvi = vi.ndvi()
gndvi = vi.gndvi()
savi = vi.savi()

print("Calculating 5-band index...")
ndre = vi.ndre()

print("Calculating all indices...")
all_results = vi.calculate_all()

print("\nResults:")
print(f"NDVI: mean={ndvi.mean:.4f}, std={ndvi.std:.4f}")
print(f"NDRE: mean={ndre.mean:.4f}, std={ndre.std:.4f}")
print(f"GNDVI: mean={gndvi.mean:.4f}")

print(f"\nTotal indices: {len(all_results)}")
for name, result in all_results.items():
    print(f"  {name}: mean={result.mean:.4f}")
```

## Handling Mixed Band Data

### If your file only has 4 bands:

```python
band_config = {
    'red': 1,
    'green': 2,
    'blue': 3,
    'nir': 4
}

ortho = Orthomosaic('field.tif', band_config=band_config)
vi = VegetationIndicesExtended(ortho)

all_indices = vi.calculate_all()
```

NDRE will be skipped automatically with a warning. All other indices calculated successfully.

### If your file has extra bands:

```python
band_config = {
    'red': 1,
    'green': 2,
    'blue': 3,
    'nir': 4,
    'rededge': 5
    # 'thermal': 6   (not used, will be ignored)
}

ortho = Orthomosaic('field.tif', band_config=band_config)
```

Only configured bands are used. Extra bands are ignored.

## Processing Multiple Scenes

```python
import os
from dronelytics import Orthomosaic, VegetationIndicesExtended

band_config = {
    'red': 1, 'green': 2, 'blue': 3, 'nir': 4, 'rededge': 5
}

results = {}

for filename in os.listdir('data/'):
    if filename.endswith('.tif'):
        print(f"Processing {filename}...")
        ortho = Orthomosaic(f'data/{filename}', band_config=band_config)
        vi = VegetationIndicesExtended(ortho)

        all_indices = vi.calculate_all()
        results[filename] = {
            'ndvi': vi.get('ndvi').mean,
            'ndre': vi.get('ndre').mean,
            'gndvi': vi.get('gndvi').mean
        }

print("\nResults summary:")
for file, indices in results.items():
    print(f"{file}:")
    for idx_name, value in indices.items():
        print(f"  {idx_name}: {value:.4f}")
```

## Sensor Specifications

Common 5-band drone sensors:

| Sensor | Bands | Resolution |
|--------|-------|------------|
| Micasense RedEdge | R, G, B, NIR, RE | 5MP |
| Parrot Sequoia | R, G, B, NIR | 4MP (no RE) |
| DJI Zenmuse H20T | RGB + Thermal | Hybrid |
| WingDrone ZH8 | R, G, B, NIR, RE | 20MP |

Check your sensor documentation for exact band wavelengths.

## Troubleshooting

### "Missing bands: ['rededge']"

Your file is 4-band. Remove 'rededge' from band_config:

```python
band_config = {
    'red': 1, 'green': 2, 'blue': 3, 'nir': 4
}
```

### NDRE values all zero

Check band order. Red-edge band may not be in position 5.
Verify with your sensor documentation.

### "NDRE skipped (5-band imagery required)"

This is a warning (not an error). It means 5-band indices are unavailable.
All 4-band indices are still calculated.

## Performance Tips

1. **Memory**: 5-band files use ~25% more memory than 4-band
2. **Processing**: 5-band takes slightly longer to process
3. **Tiling**: Process large files by geographic tiles
4. **Export**: Use CSV/Excel for post-processing in GIS

## Advanced: Custom 5-Band Index

```python
def nitrogen_stress_index(ortho):
    ndvi = (ortho.get_band('nir') - ortho.get_band('red')) / \
           (ortho.get_band('nir') + ortho.get_band('red') + 1e-10)

    ndre = (ortho.get_band('nir') - ortho.get_band('rededge')) / \
           (ortho.get_band('nir') + ortho.get_band('rededge') + 1e-10)

    return ndre / (ndvi + 1e-10)

stress_index = vi.custom(
    nitrogen_stress_index,
    'NSI',
    'Nitrogen Stress Index = NDRE / NDVI'
)
```

## See Also

- `WORKFLOW.md`: General workflow guide
- `COMPLETE_FEATURE_SUMMARY.md`: All features overview
- `examples/advanced_workflow.py`: 5-band code examples
