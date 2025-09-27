"""
Setup script for Parametric Sign Generator
"""

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="signgen",
    version="1.0.2",
    author="SignGen Contributors",
    description="Parametric Sign Generator for 3D Printing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maxwhitby/signgen",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "cadquery>=2.0",
        "trimesh>=3.9.0",
        "numpy>=1.19.0",
        "shapely>=1.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
        "preview": [
            "matplotlib>=3.3.0",
            "Pillow>=8.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "signgen=src.cli:main",
            "signgen-gui=src.gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": ["*.json"],
    },
)