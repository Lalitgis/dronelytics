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

Dronelytics is an open-source Python package for processing multispectral drone imagery and point clouds. It provides tools for vegetation index calculation, plot segmentation, spectral data extraction, crop height modeling, and visualization within a unified workflow.

The package is designed for:

* Precision agriculture
* Crop phenotyping
* Plant breeding experiments
* Remote sensing research
* Crop insurance monitoring
* UAV-based environmental analysis

## Features

### Orthomosaic Processing

* RGB, RGB+NIR, and RGB+NIR+RedEdge imagery support
* GeoTIFF-based workflows
* Flexible band configuration
* Metadata handling

### Vegetation Analysis

Implemented vegetation indices:

* NDVI
* NDRE
* GNDVI
* ExG
* SAVI
* MSAVI
* VARI
* ARVI
* CVI
* OSAVI

Additional capabilities:

* Custom vegetation index formulas
* Batch processing
* Statistical summaries

### Plot Segmentation

* Automated plot detection
* Boundary extraction
* Plot-level statistics
* Spectral data extraction

### Point Cloud Processing

* Digital Terrain Model (DTM)
* Digital Surface Model (DSM)
* Crop Height Model (CHM)
* Height statistics

### Visualization

* Point cloud visualization
* Elevation model visualization
* CHM visualization
* Surface mesh generation
* Multi-layer comparison tools

## Workflow

```text
Orthomosaic / Point Cloud
            │
            ▼
      Data Loading
            │
            ▼
 Vegetation Analysis
            │
            ▼
   Plot Segmentation
            │
            ▼
   Feature Extraction
            │
            ▼
   Statistical Analysis
            │
            ▼
     Export Results
```

## Installation

```bash
pip install dronelytics
```

Optional point cloud support:

```bash
pip install dronelytics[pointcloud]
```
# Citation

If you use Dronelytics in research:

BC, L. (2026).
Dronelytics: Comprehensive Drone Orthomosaic Analysis
and Agricultural Field Phenotyping Toolkit.
Version 1.0.0.

# Contributing

Contributions, bug reports, and feature requests are welcome.

Fork the repository
Create a feature branch
Submit a Pull Request
