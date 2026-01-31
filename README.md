# Chemical Equipment Parameter Visualizer

A hybrid system with Django backend, React web frontend, and PyQt5 desktop frontend.
Both frontends consume the same REST API.

## Project Structure

```
Fossee_project/
├── backend/              # Django REST API
├── frontend-web/         # React web application
├── frontend-desktop/     # PyQt5 desktop application
└── sample_data.csv       # Sample CSV for testing
```

---

## Step 5: How to Run

### Prerequisites

- Python 3.9+ installed
- Node.js 16+ installed (for React)
- pip and npm available in PATH

---

### 1. Run Django Backend

```bash
# Open terminal and navigate to backend folder
cd d:\Fossee_project\backend

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations (creates SQLite database)
python manage.py migrate

# Create a superuser (optional, for admin access)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

**Backend will be running at: http://localhost:8000**

Test the API:

- http://localhost:8000/api/history/ (should return empty list)
- http://localhost:8000/admin/ (Django admin)

---

### 2. Run React Web Frontend

```bash
# Open NEW terminal and navigate to frontend-web
cd d:\Fossee_project\frontend-web

# Install dependencies
npm install

# Start development server
npm start
```

**React app will be running at: http://localhost:3000**

The browser should open automatically. If not, visit http://localhost:3000

---

### 3. Run PyQt5 Desktop App

```bash
# Open NEW terminal and navigate to frontend-desktop
cd d:\Fossee_project\frontend-desktop

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

A desktop window will open with the application.

---

## How to Use

### Web App (React)

1. Open http://localhost:3000 in browser
2. Drag & drop or click to select a CSV file
3. View summary statistics and bar chart
4. Click history items to view previous uploads
5. Click "Download PDF" for reports

### Desktop App (PyQt5)

1. Click "Select CSV File" button
2. Choose a CSV file (use sample_data.csv for testing)
3. View summary statistics and bar chart
4. Click history items to view previous uploads

---

## API Endpoints

| Method | Endpoint            | Description                      |
| ------ | ------------------- | -------------------------------- |
| POST   | `/api/upload/`      | Upload CSV, returns summary JSON |
| GET    | `/api/history/`     | Get last 5 uploaded datasets     |
| GET    | `/api/report/<id>/` | Download PDF report              |
| POST   | `/api/auth/login/`  | Get auth token                   |

### CSV Format Required

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-001,Pump,150.5,25.3,45.2
Valve-001,Valve,0,15.6,42.1
```

---

## Architecture Flow

```
┌─────────────────────┐
│   React Frontend    │──────┐
│   (Port 3000)       │      │
└─────────────────────┘      │     HTTP/JSON
                             ├────────────────┐
┌─────────────────────┐      │                │
│  PyQt5 Desktop App  │──────┘                ▼
│   (Local)           │            ┌─────────────────────┐
└─────────────────────┘            │   Django Backend    │
                                   │   (Port 8000)       │
                                   │   - REST API        │
                                   │   - SQLite DB       │
                                   │   - PDF Generation  │
                                   └─────────────────────┘
```

---

## Key Files Explained

### Backend

- `backend/settings.py` - Django configuration (CORS, DRF, database)
- `api/models.py` - DatasetSummary model for storing uploads
- `api/views.py` - API logic (upload, history, report generation)
- `api/urls.py` - URL routing for API endpoints

### React Frontend

- `src/App.js` - Main component, state management
- `src/components/FileUpload.js` - Drag & drop file upload
- `src/components/TypeChart.js` - Chart.js bar chart
- `src/components/History.js` - Upload history list

### Desktop Frontend

- `main.py` - Single file with PyQt5 window, Matplotlib chart, API calls

---

## Troubleshooting

**"Cannot connect to server" error:**

- Make sure Django backend is running on port 8000
- Check if CORS is enabled in Django settings

**"Missing columns" error:**

- Ensure CSV has exact column names: Equipment Name, Type, Flowrate, Pressure, Temperature

**React build errors:**

- Delete `node_modules` folder and run `npm install` again

**PyQt5 import errors:**

- Make sure virtual environment is activated
- Run `pip install PyQt5 matplotlib requests`

---

## Quick Test

1. Start Django backend (terminal 1)
2. Start React frontend (terminal 2)
3. Upload `sample_data.csv` from project root
4. Verify:
   - Summary shows: Total Count = 15
   - Chart shows: Pump (4), Valve (4), Compressor (3), Heat Exchanger (2), Reactor (2)
