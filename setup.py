#!/usr/bin/env python
"""
Amazon Price Scraper setup script
"""

from setuptools import setup, find_packages

setup(
    name="amazon-price-scraper",
    version="1.0.0",
    description="A tool to scrape Amazon product prices and display them in a user-friendly interface",
    author="Krishnamathi2",
    author_email="your.email@example.com",  # Replace with your email
    url="https://github.com/krishnamathi2/amazon-price-scraper",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.10.0",
        "pandas>=2.0.0",
        "PySimpleGUI>=5.0.0",
        "openpyxl>=3.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "amazon-price-scraper=aps:run_command_line",
        ],
    },
)
