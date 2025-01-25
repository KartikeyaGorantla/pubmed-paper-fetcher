# PubMed Paper Fetcher

## Overview
A Python CLI tool to fetch and filter research papers from PubMed, focusing on non-academic author identification.

## Features
- Fetch papers via PubMed API
- Advanced non-academic author filtering
- Customizable search queries
- CSV export capabilities
- Debug logging

## Prerequisites
- Python 3.9+
- Poetry (Python dependency management)

## Installation

### 1. Install Poetry
```bash
pip install poetry
# Check if poetry is installed
poetry --version
# if not installed, add poetry to PATH
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";C:\Users\<username>\AppData\Roaming\Python\Scripts", "User")
```

### 2. Clone Repository
```bash
git clone https://github.com/KartikeyaGorantla/pubmed-paper-fetcher.git
cd pubmed-paper-fetcher
```

### 3. Install Dependencies
```bash
poetry install
```

## API Key Configuration
1. Open `pubmed_paper_fetcher/config.py`
2. Add your PubMed API key


## Usage

### Basic Search
```bash
poetry run get-papers-list "cancer drug discovery"
```

### Advanced Options
```bash
# Save results to CSV
poetry run get-papers-list "cancer research" -f results.csv

# Enable debug logging
poetry run get-papers-list "biotechnology" -d

# Limit results
poetry run get-papers-list "pharmaceutical research" -m 50
```

### Command-Line Options
- `-h, --help`: Display usage instructions
- `-d, --debug`: Enable detailed logging
- `-f, --file`: Specify output CSV filename
- `-m, --max-results`: Set maximum number of papers to fetch

## Project Structure
- `pubmed_paper_fetcher/`
  - `pubmed_api.py`: PubMed API interaction
  - `author_filter.py`: Non-academic author detection
  - `cli.py`: Command-line interface

## Dependencies
- requests
- biopython
- pandas
- click
