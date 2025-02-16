# Federal AI Use Case Dashboard

A web application that displays a live dashboard of Federal AI Use Cases. The dashboard provides filtering capabilities by agency, domain, status, and includes a search functionality for finding specific use cases.

## Features
- Interactive data table with sorting and filtering
- Search functionality for use case descriptions and names
- Agency and domain filters
- Active/Inactive status filter
- Responsive design for all devices

## Setup

### Backend
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask server:
```bash
python app.py
```

### Frontend
1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm start
```

The application will be available at http://localhost:3000
