"""Setup configuration for proxmox-cli."""
from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="proxmox-cli",
    version="0.1.0",
    author="Ralph Brynard",
    author_email="ralph@thebrynards.me",
    description="A command-line interface for Proxmox Virtual Environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rwgb/proxmox.cli",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "proxmoxer>=2.0.0",
        "requests>=2.28.0",
        "pyyaml>=6.0",
        "rich>=13.0.0",
        "tabulate>=0.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
            "isort>=5.11.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "proxmox-cli=proxmox_cli.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
