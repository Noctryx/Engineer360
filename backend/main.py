from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from skill_data import ROLES, BRANCHES
from skill_engine import analyze_skill_gap
from burnout_engine import analyze_burnout
from recommendation_engine import generate_recommendation

from database import engine, SessionLocal
from models import Base, StudentRecord

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserInput(BaseModel):
    name: str
    branch: str
    target_role: str
    skills: List[str]
    sleep_hours: float
    focus_score: int
    stress_level: int
    study_hours: float


@app.get("/")
def home():
    return {"message": "Engineer360 Backend Running"}


@app.get("/branches")
def get_branches():
    return BRANCHES


@app.get("/roles")
def get_roles():
    return ROLES


@app.post("/analyze")
def analyze(user: UserInput):

    # Skill Analysis
    skill_result = analyze_skill_gap(
        user.target_role,
        user.skills
    )

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
            recommendation=recommendation
        )

        db.add(record)
        db.commit()
    finally:
        db.close()

    return {
        "skill_analysis": skill_result,
        "burnout_analysis": burnout_result,
        "final_recommendation": recommendation
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