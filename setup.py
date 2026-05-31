from setuptools import setup, find_packages

setup(
    name="dronelytics",
    version="1.1.1",
    author="Lalit BC",
    description="Drone orthomosaic analysis and agricultural phenotyping",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "rasterio",
        "matplotlib",
        "scipy",
        "pandas",
    ],
    extras_require={
        "pointcloud": [
            "laspy",
            "pyvista",
        ]
    },
    python_requires=">=3.8",
)
