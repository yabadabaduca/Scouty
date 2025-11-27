"""
Setup script for Scouty
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scouty",
    version="0.1.0",
    author="Scouty Team",
    description="A lightweight, modular analytics and strategy toolkit for Hattrick",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/scouty",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Add dependencies here as needed
    ],
    entry_points={
        "console_scripts": [
            "scouty=scouty.cli.main:main",
        ],
    },
)

