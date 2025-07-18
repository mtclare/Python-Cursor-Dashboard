# Technology Stack

## Core Framework
- **Dash 2.14.2**: Python web framework for building analytical web applications
- **Plotly 5.17.0**: Interactive visualization library for charts and graphs
- **Python 3.10.7**: Runtime environment (specified in .python-version)

## Data Processing
- **Pandas 2.0.3**: Data manipulation and analysis
- **NumPy 1.24.3**: Numerical computing and data generation

## Deployment
- **Gunicorn 21.2.0**: WSGI HTTP Server for production deployment
- **Heroku/Render**: Cloud platform deployment ready

## Styling & UI
- **Inter Font Family**: Professional typography via Google Fonts
- **Custom CSS**: Embedded styling with modern design principles
- **Responsive Grid Layout**: Flexbox-based responsive design

## Common Commands

### Local Development
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

### Deployment
```bash
# Heroku deployment
heroku create your-dashboard-app
git push heroku main
heroku open

# For Render: Use web interface with build command
# Build: pip install -r requirements.txt
# Start: gunicorn app:server
```

## Development Notes
- Main application entry point: `app.py`
- Server object exposed as `app.server` for deployment
- Debug mode enabled for local development
- Default port: 8050, host: 127.0.0.1