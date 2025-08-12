import pandas as pd
from typing import List, Dict

def load_curriculum_df() -> pd.DataFrame:
    # Core subjects (codes + names + credits; prereqs where known)
    data = [
        {"Subject Code": "MIS501", "Subject Name": "Principles of Programming", "Type": "Core", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "SBD403", "Subject Name": "Secure by Design", "Type": "Core", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "SEP401", "Subject Name": "Software Engineering Principles", "Type": "Core", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "SDM404", "Subject Name": "Software Development Management", "Type": "Core", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "CCF501", "Subject Name": "Cloud Computing Fundamentals", "Type": "Core", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "MIS605", "Subject Name": "System Analysis and Design", "Type": "Core", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "ISY503", "Subject Name": "Intelligent Systems", "Type": "Core", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "REM502", "Subject Name": "Research Methodologies", "Type": "Core", "Credit Points": 10, "Prerequisites": ""},

        # WIL subjects with prereqs:
        {"Subject Code": "ITW601", "Subject Name": "Information Technology - WIL", "Type": "Core", "Credit Points": 20, "Prerequisites": "REM502"},  # +70CP rule (handle separately)
        {"Subject Code": "ITA602", "Subject Name": "Advanced IT - WIL", "Type": "Core", "Credit Points": 30, "Prerequisites": "ITW601"},
        
        # Elective slots (no code, just placeholders to be "filled"):
        {"Subject Code": "ELECTIVE_SLOT_1", "Subject Name": "Elective 1", "Type": "Elective", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "ELECTIVE_SLOT_2", "Subject Name": "Elective 2", "Type": "Elective", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "ELECTIVE_SLOT_3", "Subject Name": "Elective 3", "Type": "Elective", "Credit Points": 10, "Prerequisites": ""},
    ]
    return pd.DataFrame(data)

def load_elective_bank_df() -> pd.DataFrame:
    # Elective Bank (subset shown; extend if you have the full list)
    # Credits default to 10 unless noted; add prereqs where listed in your doc
    bank = [
        {"Subject Code": "MFA501", "Subject Name": "Mathematical Foundations of AI", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "BDA601", "Subject Name": "Big Data and Analytics", "Credit Points": 10, "Prerequisites": "CCF501"},
        {"Subject Code": "DDE602", "Subject Name": "Distributed Development", "Credit Points": 10, "Prerequisites": "CCF501"},
        {"Subject Code": "DID602A", "Subject Name": "DevOp Tools", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "MIS608", "Subject Name": "Database Modelling and Database Design", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "MIS609", "Subject Name": "Cybersecurity", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "DLE602", "Subject Name": "Deep Learning", "Credit Points": 10, "Prerequisites": "MFA501"},
        {"Subject Code": "MLN601", "Subject Name": "Machine Learning", "Credit Points": 10, "Prerequisites": "MFA501"},
        {"Subject Code": "MIS607", "Subject Name": "User Experience Design", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "MGT501", "Subject Name": "Management, People and Teams", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "DOT503", "Subject Name": "Agile Project Management", "Credit Points": 10, "Prerequisites": "SDM404"},
        {"Subject Code": "MIS602", "Subject Name": "Data Management and Analytics", "Credit Points": 10, "Prerequisites": ""},  # used as prereq for MIS608's pair (see doc)
        {"Subject Code": "MGT502", "Subject Name": "Business Communication", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "MGT600", "Subject Name": "Business Environments", "Credit Points": 10, "Prerequisites": ""},
        # add the rest as needed...
    ]
    return pd.DataFrame(bank)