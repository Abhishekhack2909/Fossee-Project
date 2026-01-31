# Chemical Equipment Parameter Visualizer

Upload CSV files with chemical equipment data and get instant analytics with charts. Works as both a web app and desktop app.

## Live Demo

**Try it here**: https://fossee-project.vercel.app/

Just upload a CSV file and see the magic happen.

## What This Does

This app helps you analyze chemical equipment data quickly. You upload a CSV file with equipment info (like pumps, valves, reactors), and it shows you:
- Total equipment count
- Average flowrate, pressure, and temperature
- A colorful chart showing equipment types
- Your last 5 uploads
- PDF reports you can download

You can use it in your browser or as a desktop application. Both connect to the same backend, so your data is always in sync.

## Tech Stack

- **Web**: React + Chart.js
- **Desktop**: PyQt5 + Matplotlib  
- **Backend**: Django REST Framework
- **Database**: SQLite
- **Data**: Pandas

## How to Use

### Easiest Way - Web App

Go to https://fossee-project.vercel.app/ and upload your CSV. That's it.

### Run It Locally

Need Python 3.9+ and Node.js 16+

**Start the Backend:**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Start the Web App:**
```bash
cd frontend-web
npm install
npm start
```

**Run the Desktop App:**
```bash
cd frontend-desktop
pip install -r requirements.txt
python main.py
```

## CSV Format

Your CSV needs these columns:
```
Equipment Name, Type, Flowrate, Pressure, Temperature
```

Example:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-001,Pump,150.5,25.3,45.2
Valve-001,Valve,0,15.6,42.1
Heat-Exchanger-001,Heat Exchanger,200.3,30.5,85.4
```

## Project Structure

```
├── backend/              # Django API
├── frontend-web/         # React web app
├── frontend-desktop/     # PyQt5 desktop app
└── README.md
```

## API Endpoints

The backend is live at: https://chemical-equipment-backend-oelr.onrender.com

- `POST /api/upload/` - Upload CSV
- `GET /api/history/` - Get last 5 uploads
- `GET /api/report/<id>/` - Download PDF

## Deployment

- **Web**: Hosted on Vercel
- **Backend**: Hosted on Render
- **Database**: SQLite

## Common Issues

**Backend not starting?**  
Make sure you have Python 3.9+ and ran `pip install -r requirements.txt`

**Web app not loading?**  
Check Node.js version and try deleting `node_modules` then run `npm install` again

**Desktop app crashes?**  
Install PyQt5 with `pip install PyQt5`

**Upload fails?**  
Check your CSV has the right columns and is UTF-8 encoded

## About

Built for the FOSSEE Internship Screening Task. This project demonstrates full-stack development with Django, React, and PyQt5.
