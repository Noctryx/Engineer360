# Engineer360

Engineer360 is a FastAPI-based skill gap and burnout analysis app for engineering students. The backend serves the frontend assets and exposes endpoints for branches, roles, skills, and the final analysis report.

## Project Layout

- `backend/main.py` - FastAPI entrypoint
- `backend/database.py` - SQLAlchemy setup
- `backend/models.py` - database models
- `backend/skill_engine.py` - skill gap calculation
- `backend/burnout_engine.py` - burnout scoring
- `backend/recommendation_engine.py` - recommendation generation
- `backend/Frontend/` - HTML, CSS, and JavaScript for the UI
- `backend/roles/` - role definitions by branch

## Requirements

Use Python 3.10+.

The backend dependencies are listed in `backend/requirements.txt` and include:

- fastapi
- uvicorn
- sqlalchemy
- pydantic
- psycopg2-binary

## Local Setup

1. Open a terminal in the `backend` folder.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app locally:

```bash
uvicorn main:app --reload
```

4. Open the app in your browser at:

```text
http://127.0.0.1:8000
```

## Database

By default, the app uses a local SQLite database file named `local.db` in the backend folder.

To use PostgreSQL, set `DATABASE_URL` before starting the app:

```bash
set DATABASE_URL=postgresql://user:password@host:5432/dbname
```

On PowerShell:

```powershell
$env:DATABASE_URL = "postgresql://user:password@host:5432/dbname"
```

## Deployment to Render

### Step 1: Push Code to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Create PostgreSQL Database on Render
1. Go to [render.com](https://render.com) and log in
2. Click **"New +"** → **"PostgreSQL"**
3. Enter a name (e.g., `engineer360-db`)
4. Click **"Create Database"**
5. Copy the **Internal Database URL** (starts with `postgresql://`)

### Step 3: Deploy Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Set the following:
   - **Root Directory:** `.` (project root)
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Click **"Advanced"** and add Environment Variable:
   - **Key:** `DATABASE_URL`
   - **Value:** Paste the PostgreSQL URL from Step 2
5. Click **"Create Web Service"**

### Step 4: Monitor Deployment
- Check the logs in the Render dashboard
- The app should be live within 2-5 minutes
- Test it: `https://your-service.render.com/branches`

**Note:** The free tier on Render spins down after 15 minutes of inactivity. Upgrade to a paid plan for production use.

## Verification

Run the smoke test from the `backend` folder to check the main API flow end to end:

```bash
python smoke_test.py
```

## Notes

- The frontend flow is stored in browser localStorage between pages.
- The dashboard depends on the `/analyze` API response, so backend validation and role data must stay in sync.
- Learning resource links fall back to a YouTube search when a direct link is missing.
