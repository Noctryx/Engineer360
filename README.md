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

## Quick Deployment Checklist

**For Replit Backend + GitHub Pages Frontend:**

1. **Create Replit repl** → https://replit.com/~
   - Import from GitHub: `https://github.com/Noctryx/Engineer360`
   - Replit runs `.replit` and installs `backend/requirements.txt`
   - Copy the public Replit URL (e.g., `https://your-replit-app.replit.app`)

2. **Enable GitHub Pages** → https://github.com/Noctryx/Engineer360/settings/pages
   - Source: Deploy from branch → `main` / `docs/` folder
   - Wait ~2 min for publication

3. **Connect Frontend to Backend** → Open GitHub Pages site with:
   ```
   https://<your-github-username>.github.io/Engineer360/?api=https://your-replit-app.replit.app
   ```
   - When prompted, confirm the backend URL (stored in localStorage)
   - Refresh the page and the app should work

## Deployment

The free deployment layout is:

- Backend API on Replit
- Frontend on GitHub Pages

### Step 1: Push Code to GitHub

```bash
git add .
git commit -m "Prepare free Replit deployment"
git push origin main
```

### Step 2: Deploy the Backend on Replit

1. Create a new Replit Python repl from this repository.
2. Let Replit install dependencies from `backend/requirements.txt`.
3. Use the run command in [.replit](.replit).
4. Copy the public Replit URL after the app starts.

### Step 3: Deploy the Frontend on GitHub Pages

1. In GitHub, open the repository settings.
2. Go to **Pages**.
3. Set the source to the `docs/` folder on the default branch.
4. Wait for GitHub Pages to publish the site.

### Step 4: Connect the Frontend to the Backend

1. Open the GitHub Pages site in your browser.
2. When prompted, enter the Replit backend URL once.
3. The app stores that backend URL in browser localStorage for later visits.

### Step 5: Verify the API

Test the backend directly with:

```text
https://your-replit-app.replit.app/branches
```

The frontend pages are mirrored in `docs/` for GitHub Pages, and the backend still serves the same app for local development and Replit.

## Verification

Run the smoke test from the `backend` folder to check the main API flow end to end:

```bash
python smoke_test.py
```

## Notes

- The frontend flow is stored in browser localStorage between pages.
- The dashboard depends on the `/analyze` API response, so backend validation and role data must stay in sync.
- Learning resource links fall back to a YouTube search when a direct link is missing.
