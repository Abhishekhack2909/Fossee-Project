# Chemical Equipment Parameter Visualizer

A hybrid application for analyzing and visualizing chemical equipment data through both web and desktop interfaces. Upload CSV files with chemical equipment data and get instant analytics with charts.

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

### Option 1: Use the Live Web App (No Setup Required)

Just go to https://fossee-project.vercel.app/ and upload your CSV file. Everything is already running in the cloud.

### Option 2: Run Everything Locally

#### Before You Start

Make sure you have these installed:
- **Python 3.9+**: https://www.python.org/downloads/
- **Node.js 16+**: https://nodejs.org/
- **Git**: https://git-scm.com/downloads

#### Clone the Repository

```bash
git clone https://github.com/Abhishekhack2909/Fossee-Project.git
cd Fossee-Project
```

#### Step 1: Set Up the Backend

Open your terminal and run these commands one by one:

```bash
# Go to the backend folder
cd backend

# Install all the required Python packages
pip install -r requirements.txt

# Set up the database (creates db.sqlite3 file)
python manage.py migrate

# Start the backend server
python manage.py runserver
```

The backend will start at `http://127.0.0.1:8000`. Keep this terminal window open.

#### Step 2: Set Up the Web Frontend

Open a new terminal window and run:

```bash
# Go to the web frontend folder
cd frontend-web

# Install all the required packages
npm install

# Start the web app
npm start
```

Your browser will automatically open to `http://localhost:3000`. If it doesn't, just type that URL in your browser.

#### Step 3: Run the Desktop App (Optional)

Open another new terminal window and run:

```bash
# Go to the desktop app folder
cd frontend-desktop

# Install the required packages
pip install -r requirements.txt

# Run the desktop application
python main.py
```

A window will pop up with the desktop version of the app.

**Important Notes:**
- The backend must be running for the web and desktop apps to work
- If you're running locally, the apps will use your local backend at `http://127.0.0.1:8000`
- The desktop app in this repo is already configured to use the live backend, so it works without running the local backend

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

## How the App Works

When you upload a CSV file:
1. The file goes to the Django backend
2. Pandas reads and analyzes the data
3. The backend calculates averages and counts equipment types
4. Results are saved in SQLite database (keeps last 5 uploads)
5. The frontend displays the statistics and chart
6. You can download a PDF report anytime

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
