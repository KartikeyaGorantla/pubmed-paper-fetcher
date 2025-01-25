# PubMed Paper Fetcher

## Overview
A Python CLI tool to fetch research papers from PubMed, with advanced filtering for non-academic authors.

## Features
- Fetch papers via PubMed API
- Filter for non-academic authors
- Customizable search queries
- CSV output support

## Installation

```bash
# Install Poetry
pip install poetry

# Clone the repository
git clone https://github.com/yourusername/pubmed-paper-fetcher.git
cd pubmed-paper-fetcher

# Install dependencies
poetry install
```

## Usage

```bash
# Basic usage
poetry run get-papers-list "cancer immunotherapy"

# With debug logging
poetry run get-papers-list "cancer immunotherapy" -d

# Save to CSV
poetry run get-papers-list "cancer immunotherapy" -f results.csv
```

## Development
- Python 3.9+
- Dependencies managed via Poetry
- Testing with pytest
- Type checking with mypy

## Tools Used
- Requests for HTTP interactions
- Biopython for XML parsing
- Pandas for data manipulation
- Click for CLI interface