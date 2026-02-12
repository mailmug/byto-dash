<h1 align="center">
  🚀 FastAPI + Svelte Dashboard (Byto-Dash)
</h1>
<div align="center">
  # 🚀 FastAPI + Svelte Dashboard (Byto-Dash)

  ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
  ![Svelte](https://img.shields.io/badge/SvelteKit-FF3E00?style=for-the-badge&logo=svelte&logoColor=white)
  ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
  ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

  **A modern, full-stack dashboard application with real-time capabilities**
</div>

A full-stack web application with **FastAPI** backend and **SvelteKit** frontend.  
This dashboard allows you to manage data, visualize metrics, and interact with APIs in real-time.

## Features

- FastAPI backend with RESTful API endpoints
- SvelteKit frontend for reactive and interactive UI
- JWT authentication and user sessions
- Form handling and validations
- Real-time updates via WebSockets (optional)
- Easy to extend with custom modules and components

## Tech Stack

- **Backend:** FastAPI, Pydantic, SQLAlchemy, PostgreSQL 
- **Frontend:** SvelteKit, TailwindCSS  
- **Authentication:** JWT / OAuth (optional)
- **Deployment:** Docker / Uvicorn / Nginx



  ## 📸 Screenshot

![byto‑dash overview](https://raw.githubusercontent.com/mailmug/byto-dash/9d70ebd632c85af33c0bb05957a4ed0b26d56653/Screenshot-1.png)
![byto‑dash overview](https://raw.githubusercontent.com/mailmug/byto-dash/9d70ebd632c85af33c0bb05957a4ed0b26d56653/Screenshot-2.png)

 ## How to Install Byto-Dash

### Step 1: Clone the Repository
```bash
git clone https://github.com/mailmug/byto-dash.git
cd byto-dash
```

### Step 2: Set Up the Python Backend
```bash
python3 -m venv .venv
source .venv/bin/activate
uv sync
```

Edit the .env file to update PostgreSQL credentials

### Step 3: Run the FastAPI Backend
```bash
uvicorn main:app --reload
```

### Step 4: Set Up the Frontend
#### Open a new terminal
```bash
cd byto-dash/frontend
npm install
npm run dev
```

### Open the browser at the address shown in the terminal

I am ready for projects. Feel free to PM: info@mailmug.net

