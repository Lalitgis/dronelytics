"""Setup configuration for dronelytics package."""

from setuptools import setup, find_packages
from pathlib import Path

readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

install_requires = [
    'numpy>=1.20.0',
    'pandas>=1.3.0',
    'scipy>=1.7.0',
    'rasterio>=1.2.0',
    'geopandas>=0.10.0',
    'shapely>=1.7.0',
    'scikit-image>=0.18.0',
    'openpyxl>=3.0.0',
    'matplotlib>=3.3.0',
]

extras_require = {
    'pointcloud': ['laspy>=2.0.0', 'pyvista>=0.40.0'],
    'dev': ['pytest>=6.0', 'pytest-cov', 'black', 'flake8', 'sphinx'],
    'all': ['laspy>=2.0.0', 'pyvista>=0.40.0'],
}

setup(
    name='dronelytics',
    version='1.0.0',
    author='Research Development',
    author_email='lalitiaas@gmail.com',
    description='Comprehensive drone orthomosaic analysis and agricultural field phenotyping',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Lalitgis/dronelytics',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=install_requires,
    extras_require=extras_require,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Agriculture',
    ],
    keywords='drone agriculture phenotyping orthomosaic GIS remote-sensing',
    project_urls={
        'Documentation': 'https://github.com/Lalitgis/dronelytics/wiki',
        'Source': 'https://github.com/Lalitgis/dronelytics',
        'Tracker': 'https://github.com/Lalitgis/dronelytics/issues',
    },
)
