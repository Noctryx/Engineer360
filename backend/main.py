from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic import Field
from typing import List

from skill_data import BRANCHES,ROLES
from skill_engine import analyze_skill_gap
from burnout_engine import analyze_burnout
from recommendation_engine import generate_recommendation

from database import engine, SessionLocal
from models import Base, StudentRecord
import json

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "Frontend"

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_index():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/dashboard")
def serve_dashboard():
    return FileResponse(FRONTEND_DIR / "dashboard.html")

allowed_origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:10000",
    "http://127.0.0.1:10000",
]

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    branch: str = Field(min_length=1)
    target_role: str = Field(min_length=1)
    skills: List[str] = Field(default_factory=list)
    sleep_hours: float = Field(ge=0, le=24)
    focus_score: int = Field(ge=1, le=10)
    stress_level: int = Field(ge=1, le=10)
    study_hours: float = Field(ge=0, le=24)



@app.get("/branches")
def get_branches():
    return {"branches": list(BRANCHES.keys())}

@app.get("/roles/{branch}")
def get_roles(branch: str):
    roles = BRANCHES.get(branch)
    if roles is None:
        raise HTTPException(status_code=404, detail="Invalid branch selected")
    return {"roles": roles}

@app.get("/skills/{role}")
def get_skills(role: str):
    skills = ROLES.get(role)
    if skills is None:
        raise HTTPException(status_code=404, detail="Invalid role selected")
    return {"skills": skills}

@app.post("/analyze")
def analyze(user: UserInput):
    if user.branch not in BRANCHES:
        raise HTTPException(status_code=400, detail="Invalid branch selected")

    if user.target_role not in ROLES:
        raise HTTPException(status_code=400, detail="Invalid role selected")

    # Skill Analysis
    skill_result = analyze_skill_gap(
        user.target_role,
        user.skills
    )

    if skill_result.get("error"):
        raise HTTPException(status_code=400, detail=skill_result["error"])

    # Burnout Analysis
    burnout_result = analyze_burnout(
        user.sleep_hours,
        user.focus_score,
        user.stress_level,
        user.study_hours
    )

    # Recommendation
    recommendation = generate_recommendation(
        skill_result,
        burnout_result
    )

    # Save to DB safely
    db = SessionLocal()
    try:
        record = StudentRecord(
            name=user.name,
            branch=user.branch,
            role=user.target_role,
            match_percentage=skill_result["match_percentage"],
            burnout_score=burnout_result["burnout_score"],
            burnout_risk=burnout_result["burnout_risk"],
            recommendation=json.dumps(recommendation)
        )

        db.add(record)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    return {
        "skill_analysis": skill_result,
        "burnout_analysis": burnout_result,
        "final_recommendation": recommendation["message"],
        "learning_resources": recommendation["resources"]
    }

@app.get("/records")
def get_records():
    db = SessionLocal()
    try:
        records = db.query(StudentRecord).all()

        return [
            {
                "id": r.id,
                "name": r.name,
                "branch": r.branch,
                "role": r.role,
                "match_percentage": r.match_percentage,
                "burnout_score": r.burnout_score,
                "burnout_risk": r.burnout_risk,
                "recommendation": r.recommendation,
                "created_at": r.created_at,
            }
            for r in records
        ]
    finally:
        db.close()