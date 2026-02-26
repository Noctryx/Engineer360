from roles.aerospace_roles import AEROSPACE_ROLES
from roles.biomedical_roles import BIOMEDICAL_ROLES
from roles.chemical_roles import CHEMICAL_ROLES
from roles.civil_roles import CIVIL_ROLES
from roles.cse_roles import CSE_ROLES
from roles.electrical_roles import ELECTRICAL_ROLES
from roles.ece_roles import ECE_ROLES
from roles.environmental_roles import ENVIRONMENTAL_ROLES
from roles.it_roles import IT_ROLES
from roles.mechanical_roles import MECHANICAL_ROLES


# =========================
# MERGE ALL ROLE DICTIONARIES
# =========================

ROLES = {}

ROLES.update(AEROSPACE_ROLES)
ROLES.update(BIOMEDICAL_ROLES)
ROLES.update(CHEMICAL_ROLES)
ROLES.update(CIVIL_ROLES)
ROLES.update(CSE_ROLES)
ROLES.update(ELECTRICAL_ROLES)
ROLES.update(ECE_ROLES)
ROLES.update(ENVIRONMENTAL_ROLES)
ROLES.update(IT_ROLES)
ROLES.update(MECHANICAL_ROLES)


# =========================
# BRANCH → ROLE MAPPING
# =========================

BRANCHES = {
    "AEROSPACE": list(AEROSPACE_ROLES.keys()),
    "BIOMEDICAL": list(BIOMEDICAL_ROLES.keys()),
    "CHEMICAL": list(CHEMICAL_ROLES.keys()),
    "CIVIL": list(CIVIL_ROLES.keys()),
    "CSE": list(CSE_ROLES.keys()),
    "ELECTRICAL": list(ELECTRICAL_ROLES.keys()),
    "ECE": list(ECE_ROLES.keys()),
    "ENVIRONMENTAL": list(ENVIRONMENTAL_ROLES.keys()),
    "IT": list(IT_ROLES.keys()),
    "MECHANICAL": list(MECHANICAL_ROLES.keys()),
}