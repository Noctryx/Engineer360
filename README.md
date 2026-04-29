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

## Fresh Deployment Steps

Use this exact flow when you want to deploy from scratch again.

1. **Push the latest code** to GitHub.

   ```bash
   git add .
   git commit -m "Prepare Engineer360 deployment"
   git push origin main
   ```

2. **Create or refresh the Replit app** from this repo.
   - Open https://replit.com/~
   - Import `https://github.com/Noctryx/Engineer360`
   - Replit uses [.replit](.replit) and installs `backend/requirements-replit.txt`
   - Copy the public Replit URL, for example `https://your-replit-app.replit.app`

3. **Let GitHub Actions deploy Pages**.
   - The Pages workflow is [`.github/workflows/pages.yml`](.github/workflows/pages.yml)
   - In repo settings, set **Pages** to use **GitHub Actions**
   - Wait for the workflow to finish, then open the published site

4. **Open the frontend with the backend URL once**.

   ```text
   https://<your-github-username>.github.io/Engineer360/?api=https://your-replit-app.replit.app
   ```

   - Confirm the backend URL when prompted
   - The app stores it in browser localStorage

5. **Verify the backend directly**.
   ```text
   https://your-replit-app.replit.app/branches
   ```

The static frontend also lives in [docs/](docs/index.html) for reference, and the root [index.html](index.html) redirects into it if Pages is pointed at the repository root.

## Verification

Run the smoke test from the `backend` folder to check the main API flow end to end:

```bash
python smoke_test.py
```

## Notes

- The frontend flow is stored in browser localStorage between pages.
- The dashboard depends on the `/analyze` API response, so backend validation and role data must stay in sync.
- Learning resource links fall back to a YouTube search when a direct link is missing.
