"""Setup script for Teams Translator."""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="teams-translator",
    version="1.0.0",
    author="Teams Translator Project",
    author_email="",
    description="Real-time translation tool for Microsoft Teams meetings using LibreTranslate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/teams-translator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Chat",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "teams-translator=main:main",
        ],
    },
    keywords="translation, teams, microsoft, libretranslate, real-time, captions",
    project_urls={
        "Bug Reports": "https://github.com/your-username/teams-translator/issues",
        "Source": "https://github.com/your-username/teams-translator",
        "Documentation": "https://github.com/your-username/teams-translator/blob/main/README.md",
    },
)