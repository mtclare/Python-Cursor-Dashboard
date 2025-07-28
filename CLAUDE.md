# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python dashboard application built with Dash and Plotly, designed as an executive business intelligence dashboard for board presentations. The application creates an interactive web interface with 8 business analytics charts and executive summary KPI cards.

## Architecture

### Core Application Structure
- **Main application**: `app.py` - Contains the complete Dash application with all UI components, data generation functions, and layout definitions
- **Entry point**: `main.py` - Simple entry point that just prints a hello message
- **Configuration**: Uses `pyproject.toml` for Python project metadata

### Key Components
- **Data Generation**: Multiple seed-based functions generate realistic business data (revenue, profit margins, customer metrics, etc.)
- **Visualization**: 8 interactive charts using Plotly with professional styling and consistent color schemes
- **Dashboard Layout**: Executive summary cards with KPIs plus a 4x2 grid of charts
- **Styling**: Custom CSS with Inter font family, gradient headers, and modern card-based design

## Development Commands

### Running the Application
```bash
python app.py
```
The application runs on `http://127.0.0.1:8050` by default.

### Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies
The application requires:
- dash==2.14.2
- plotly==5.17.0
- numpy==1.24.3
- pandas==2.0.3
- gunicorn==21.2.0 (for deployment)

## Deployment Configuration

### Heroku/Render Deployment
- **Procfile**: Configured for web deployment with gunicorn
- **Runtime**: Python 3.11.7 specified in `runtime.txt`
- **Server reference**: The Dash app exposes `server = app.server` for WSGI deployment

### Important Note on Procfile
The current Procfile references `dashboard:server` but the main file is `app.py`. For proper deployment, either:
1. Rename `app.py` to `dashboard.py`, or
2. Update Procfile to `web: gunicorn app:server`

## Code Patterns

### Data Generation Pattern
All chart data uses seeded random generation functions that create realistic business trends with:
- Base trend lines
- Seasonal variations
- Random noise for realism
- Consistent time series (100 days from 2023-01-01)

### Color Scheme
Professional color palette used throughout:
- Primary: #1e40af (blue)
- Success: #059669 (green)  
- Warning: #dc2626 (red)
- Purple: #7c3aed
- Additional chart colors for variety

### Chart Configuration
All charts follow consistent patterns:
- Line charts with area fills
- Professional hover templates
- Consistent grid styling
- Modern typography with Inter font
- Responsive design principles

## File Structure Notes

There's a merge conflict in README.md indicating this repository has been synced with a remote. The README contains comprehensive documentation about the executive dashboard features and deployment instructions.