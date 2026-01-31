# Chemical Equipment Parameter Visualizer

A hybrid application for analyzing and visualizing chemical equipment data through both web and desktop interfaces. Upload CSV files containing equipment parameters and get instant analytics with interactive charts.

## Overview

This project demonstrates a full-stack hybrid application with:
- **Web Interface**: React-based web application with Chart.js visualizations
- **Desktop Interface**: PyQt5 native application with Matplotlib charts
- **Backend API**: Django REST Framework handling data processing and storage
- **Shared Database**: SQLite storing upload history and analytics

Both frontends consume the same REST API, ensuring consistent functionality across platforms.

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend (Web) | React.js + Chart.js | Interactive web interface with charts |
| Frontend (Desktop) | PyQt5 + Matplotlib | Native desktop application |
| Backend | Django + Django REST Framework | REST API for data processing |
| Data Processing | Pandas | CSV parsing and analytics |
| Database | SQLite | Store upload history (last 5 datasets) |
| Version Control | Git + GitHub | Source code management |

---

## Features

✅ **CSV Upload** - Upload equipment data files through web or desktop interface  
✅ **Data Analysis** - Automatic calculation of averages and statistics  
✅ **Visualization** - Interactive bar charts showing equipment type distribution  
✅ **History Management** - View and access last 5 uploaded datasets  
✅ **PDF Reports** - Generate downloadable PDF reports with full analytics  
✅ **Authentication** - Token-based API authentication system  

---

## Project Structure

```
chemical-equipment-visualizer/
├── backend/                    # Django REST API
│   ├── api/                    # API application
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API endpoints
│   │   ├── serializers.py     # Data serialization
│   │   └── urls.py            # URL routing
│   ├── backend/               # Django settings
│   ├── manage.py              # Django CLI
│   └── requirements.txt       # Python dependencies
│
├── frontend-web/              # React web application
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── App.js            # Main component
│   │   └── App.css           # Styling
│   └── package.json          # Node dependencies
│
├── frontend-desktop/          # PyQt5 desktop application
│   ├── main.py               # Desktop app (single file)
│   └── requirements.txt      # Python dependencies
│
└── sample_data.csv           # Sample CSV for testing
```

---

## Installation & Setup

### Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- pip and npm

### 1. Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start Django server
python manage.py runserver
```

Backend will run at: **http://127.0.0.1:8000**

### 2. Web Frontend Setup (React)

Open a new terminal:

```bash
# Navigate to frontend-web directory
cd frontend-web

# Install dependencies
npm install

# Start development server
npm start
```

Web app will open at: **http://localhost:3000**

### 3. Desktop Application Setup (PyQt5)

Open a new terminal:

```bash
# Navigate to frontend-desktop directory
cd frontend-desktop

# Install dependencies
pip install -r requirements.txt

# Run desktop application
python main.py
```

---

## Usage

### Web Application

1. Open http://localhost:3000 in your browser
2. Click "Choose File" or drag and drop a CSV file
3. View summary statistics and charts
4. Access previous uploads from "Recent Uploads" section
5. Download PDF reports for any dataset

### Desktop Application

1. Launch the application with `python main.py`
2. Click "Choose CSV File" button
3. Select your CSV file
4. View statistics and charts
5. Access upload history and download reports

### CSV Format

Your CSV file must include these columns:
- Equipment Name
- Type
- Flowrate
- Pressure
- Temperature

Example:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-001,Pump,150.5,25.3,45.2
Valve-001,Valve,0,15.6,42.1
```

Use the included `sample_data.csv` for testing.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload/` | Upload CSV and get analysis |
| GET | `/api/history/` | Get last 5 uploaded datasets |
| GET | `/api/report/<id>/` | Download PDF report |
| POST | `/api/auth/login/` | Get authentication token |

### Example API Usage

**Upload CSV:**
```bash
curl -X POST http://127.0.0.1:8000/api/upload/ \
  -F "file=@sample_data.csv"
```

**Get History:**
```bash
curl http://127.0.0.1:8000/api/history/
```

---

## Architecture

```
┌─────────────────┐
│  React Web App  │────┐
│  (Port 3000)    │    │
└─────────────────┘    │
                       │    HTTP/JSON
┌─────────────────┐    │    Requests
│ PyQt5 Desktop   │────┼──────────────► ┌──────────────────┐
│ Application     │    │                │  Django Backend  │
└─────────────────┘    │                │  (Port 8000)     │
                       │                │                  │
                       │                │  - REST API      │
                       └────────────────│  - Pandas        │
                                        │  - SQLite DB     │
                                        │  - PDF Reports   │
                                        └──────────────────┘
```

Both frontends communicate with the same Django backend, ensuring data consistency and shared functionality.

---

## Key Implementation Details

### Backend (Django)
- **Data Processing**: Pandas reads and analyzes CSV files
- **Storage**: SQLite stores last 5 dataset summaries
- **PDF Generation**: ReportLab creates downloadable reports
- **Authentication**: Token-based auth using Django REST Framework

### Frontend (Web)
- **Framework**: React with functional components and hooks
- **Charts**: Chart.js for interactive bar charts
- **File Upload**: Drag-and-drop support with FormData API
- **State Management**: React useState and useEffect hooks

### Frontend (Desktop)
- **Framework**: PyQt5 for native GUI
- **Charts**: Matplotlib embedded in Qt widgets
- **API Communication**: Requests library for HTTP calls
- **Layout**: Grid and box layouts for responsive design

---

## Troubleshooting

**Backend won't start:**
- Ensure Python 3.9+ is installed
- Check if port 8000 is available
- Verify all dependencies are installed: `pip install -r requirements.txt`

**Web app won't start:**
- Ensure Node.js 16+ is installed
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is available

**Desktop app won't start:**
- Install PyQt5: `pip install PyQt5`
- Ensure backend is running first
- Check Python version compatibility

**CSV upload fails:**
- Verify CSV has required columns (Equipment Name, Type, Flowrate, Pressure, Temperature)
- Check file encoding (should be UTF-8)
- Ensure backend is running

**"Cannot connect to server" error:**
- Verify Django backend is running on port 8000
- Check CORS settings in `backend/backend/settings.py`
- Ensure firewall isn't blocking connections

---

## Development

### Running Tests
```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend-web
npm test
```

### Building for Production

**Web Frontend:**
```bash
cd frontend-web
npm run build
```

**Backend:**
```bash
cd backend
python manage.py collectstatic
```

---

## Contributing

This project was developed as part of an internship screening task. For questions or issues, please open an issue on GitHub.

---

## License

This project is for educational purposes.

---

## Author

Developed as part of FOSSEE Internship Screening Task

---

## Acknowledgments

- Django REST Framework for the excellent API framework
- React and Chart.js for web visualization
- PyQt5 and Matplotlib for desktop application
- Pandas for data processing capabilities
