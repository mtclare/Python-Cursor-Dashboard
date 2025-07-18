# Project Structure

## Root Directory Layout
```
├── .git/                   # Git version control
├── .kiro/                  # Kiro AI assistant configuration
├── __pycache__/            # Python bytecode cache
├── .python-version         # Python version specification (3.10.7)
├── app.py                  # Main application file - entry point
├── requirements.txt        # Python dependencies
├── runtime.txt            # Python runtime for deployment
├── Procfile               # Heroku deployment configuration
├── DEPLOYMENT.md          # Deployment instructions
└── README.md              # Project documentation
```

## Key Files

### Core Application
- **app.py**: Single-file application containing all dashboard logic
  - Data generation functions
  - Chart configurations
  - Layout definitions
  - Dash app initialization

### Configuration Files
- **requirements.txt**: Pinned dependency versions for reproducible builds
- **runtime.txt**: Specifies Python 3.11.7 for deployment
- **Procfile**: Heroku deployment with `gunicorn dashboard:server`
- **.python-version**: Local Python version (3.10.7)

### Documentation
- **README.md**: Comprehensive project documentation with setup instructions
- **DEPLOYMENT.md**: Specific deployment guide for Render platform

## Code Organization (within app.py)

### Data Generation Functions
- `generate_sales_data()`, `generate_website_traffic()`, etc.
- Each function uses seeded random data for consistent results
- Returns time series data for visualization

### Configuration Arrays
- `summary_metrics`: Executive KPI card definitions
- `charts_data`: Chart configuration with titles, colors, and data functions

### Layout Components
- Summary cards generation
- Chart creation with professional styling
- Grid layout assembly
- Main app layout with header and footer

## Development Patterns
- Single-file architecture for simplicity
- Functional approach for data generation
- Configuration-driven chart creation
- Embedded CSS styling within Python
- Responsive design using flexbox layouts