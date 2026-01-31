# Chemical Equipment Parameter Visualizer

A full-stack application for analyzing chemical equipment data with both web and desktop interfaces. Upload CSV files and get instant analytics with interactive visualizations.

## 🌐 Live Demo

**Web Application**: https://fossee-project.vercel.app/

Try it now! Upload the included `sample_data.csv` file to see it in action.

---

## Overview

This hybrid application provides:
- **Web Interface**: React app with Chart.js visualizations
- **Desktop Interface**: PyQt5 native application with Matplotlib charts
- **REST API Backend**: Django backend for data processing
- **Database**: SQLite for storing upload history

Both interfaces use the same API, ensuring consistent functionality.

---

## Features

✅ CSV file upload (drag & drop supported)  
✅ Automatic data analysis and statistics  
✅ Interactive bar charts  
✅ Upload history (last 5 datasets)  
✅ PDF report generation  
✅ Token-based authentication  

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend (Web) | React.js + Chart.js |
| Frontend (Desktop) | PyQt5 + Matplotlib |
| Backend | Django + Django REST Framework |
| Data Processing | Pandas |
| Database | SQLite |

---

## Quick Start

### Option 1: Use the Live Web App (Easiest)

Just visit: **https://fossee-project.vercel.app/**

No installation needed! Upload your CSV and start analyzing.

### Option 2: Run Locally

#### Prerequisites
- Python 3.9+
- Node.js 16+

#### Backend Setup (5 minutes)

```bash
# 1. Navigate to backend
cd backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup database
python manage.py migrate

# 4. Start server
python manage.py runserver
```

Backend runs at: http://127.0.0.1:8000

#### Web Frontend Setup (3 minutes)

```bash
# 1. Navigate to frontend-web (open new terminal)
cd frontend-web

# 2. Install dependencies
npm install

# 3. Start app
npm start
```

Web app opens at: http://localhost:3000

#### Desktop App Setup (2 minutes)

```bash
# 1. Navigate to frontend-desktop (open new terminal)
cd frontend-desktop

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run app
python main.py
```

---

## Usage

### Web Application

1. Visit https://fossee-project.vercel.app/
2. Click "Choose File" or drag & drop your CSV
3. View statistics and charts instantly
4. Access previous uploads from "Recent Uploads"
5. Download PDF reports

### Desktop Application

1. Launch with `python main.py`
2. Click "Choose CSV File"
3. Select your file
4. View results and charts
5. Access history and download reports

### CSV Format Required

Your CSV must have these columns:
```
Equipment Name, Type, Flowrate, Pressure, Temperature
```

**Example:**
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-001,Pump,150.5,25.3,45.2
Valve-001,Valve,0,15.6,42.1
```

Use `sample_data.csv` (included) for testing.

---

## Project Structure

```
chemical-equipment-visualizer/
├── backend/                    # Django REST API
│   ├── api/                    # API endpoints
│   ├── backend/               # Settings
│   ├── manage.py
│   └── requirements.txt
│
├── frontend-web/              # React web app
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   └── App.css
│   └── package.json
│
├── frontend-desktop/          # PyQt5 desktop app
│   ├── main.py
│   └── requirements.txt
│
└── sample_data.csv           # Sample data
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload/` | Upload CSV file |
| GET | `/api/history/` | Get last 5 uploads |
| GET | `/api/report/<id>/` | Download PDF report |
| POST | `/api/auth/login/` | Get auth token |

**Backend URL**: https://chemical-equipment-backend-oelr.onrender.com

**Example:**
```bash
curl https://chemical-equipment-backend-oelr.onrender.com/api/history/
```

---

## Deployment

### Live URLs

- **Frontend**: https://fossee-project.vercel.app/
- **Backend**: https://chemical-equipment-backend-oelr.onrender.com

### Hosting Platforms

- Frontend: Vercel
- Backend: Render
- Database: SQLite (file-based)

---

## Screenshots

### Web Interface
- Clean, modern design
- Drag & drop file upload
- Real-time statistics
- Colorful bar charts
- Upload history with PDF download

### Desktop Interface
- Native application window
- File picker dialog
- Matplotlib visualizations
- Same functionality as web

---

## Development

### Run Tests
```bash
# Backend
cd backend
python manage.py test

# Frontend
cd frontend-web
npm test
```

### Build for Production
```bash
# Web frontend
cd frontend-web
npm run build

# Backend
cd backend
python manage.py collectstatic
```

---

## Troubleshooting

**Backend won't start:**
- Check Python version (3.9+)
- Install dependencies: `pip install -r requirements.txt`
- Run migrations: `python manage.py migrate`

**Web app won't start:**
- Check Node.js version (16+)
- Delete `node_modules` and run `npm install`
- Check port 3000 availability

**Desktop app won't start:**
- Install PyQt5: `pip install PyQt5`
- Ensure backend is running
- Check Python compatibility

**CSV upload fails:**
- Verify required columns exist
- Check file encoding (UTF-8)
- Ensure backend is running

---

## Contributing

This project was developed as part of the FOSSEE Internship Screening Task.

---

## License

Educational purposes only.

---

## Author

Developed for FOSSEE Internship Screening Task

---

## Acknowledgments

- Django REST Framework
- React and Chart.js
- PyQt5 and Matplotlib
- Pandas for data processing
