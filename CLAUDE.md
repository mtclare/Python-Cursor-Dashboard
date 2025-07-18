can yo# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based Executive Business Dashboard built with Dash and Plotly. It provides interactive business intelligence visualizations for executive presentations and board meetings.

## Development Commands

### Running the Application
```bash
python app.py
```
The dashboard will be available at `http://127.0.0.1:8050`

### Package Management
- Dependencies are managed via `requirements.txt` and `pyproject.toml`
- Install dependencies: `pip install -r requirements.txt`
- Python version: 3.10+ (specified in pyproject.toml)

### Deployment
- Configured for Heroku deployment via `Procfile`
- Procfile expects a `dashboard:server` entry point (note: current Procfile may need adjustment as main app is in `app.py`)

## Architecture

### Core Components
- `app.py` - Main Dash application with 8 interactive charts and executive summary cards
- `color_palette.py` - Centralized color scheme and theming system
- `filters.py` - Interactive filtering components and utilities
- `main.py` - Simple entry point (minimal functionality)

### Key Features
- 8 interactive business charts (revenue, profit margins, customer metrics, etc.)
- Executive summary KPI cards
- Professional color scheme with accessibility considerations
- Real-time data visualization using simulated business data
- Responsive grid layout optimized for presentations

### Data Generation
- Uses NumPy/Pandas for simulated business data
- Includes realistic trends, seasonality, and noise
- Data can be filtered by date range, categories, and value ranges
- Supports multiple business dimensions (regions, products, time periods)

### Styling System
- Custom color palette with accessibility variants
- Gradient headers and professional card designs
- Uses Inter font family for typography
- Bootstrap components via dash-bootstrap-components

## Development Notes

- No testing framework currently configured
- No linting tools (flake8, black, ruff) installed
- The Procfile references `dashboard:server` but the main app is in `app.py` - this may need adjustment for Heroku deployment
- Data is currently simulated - can be extended to connect to real data sources (databases, APIs, files)