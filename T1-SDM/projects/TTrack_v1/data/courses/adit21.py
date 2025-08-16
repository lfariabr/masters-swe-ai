"""
Course: ADIT21 - Associate Degree of Information Technology

The Associate Degree of Information Technology is two years in duration for a full time student, 
or four years duration for a part time student.
In this course, your core subjects will comprise of 14 subjects.
Each year consists of three Study Periods, also known as Trimesters.

- Core subjects - compulsory subjects that you must complete
- Elective subjects - subjects you can choose between from the Elective Bank below
Course comprises of 16 subjects that are required to complete: 14 core subjects and 2 elective subjects.

The course contains 3 subject levels - Level 100, 200 and 300, guiding students from foundational through to more complex subjects.
• Level 100: 7 core subjects and 1 elective subject
• Level 200: 6 core subjects and 1 elective subject
• Level 300: 1 mandatory core subject

Prerequisite subject: a subject you must complete before undertaking another subject
Corequisite subject: a subject you must complete with another subject at the same time
"""

import pandas as pd
from typing import List, Dict

def load_curriculum_adit_df() -> pd.DataFrame:
     # Core subjects (codes + names + credits; prereqs where known)
    data = [
        # Core no prereqs:
        {"Subject Code": "CAO107", "Subject Name": "Computer Architecture and Operating Systems", "Type": "Core", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "ITP122", "Subject Name": "Introduction to Programming", "Type": "Core", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "MIS100", "Subject Name": "Foundations of Information Systems", "Type": "Core", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "MIS102", "Subject Name": "Data and Networking", "Type": "Core", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "DIG103A", "Subject Name": "Interaction Design", "Type": "Core", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "IPP221", "Subject Name": "IT Professional Practice", "Type": "Core", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "IDS201", "Subject Name": "Introduction to Data Science", "Type": "Core", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "PBT205", "Subject Name": "Project Based Learning Studio Technology", "Type": "Core", "Credit Points": 10, "Prerequisites": ""},
                        
        # Core with prereqs:
        {"Subject Code": "ISE102", "Subject Name": "Introduction to Software Engineering", "Type": "Core", "Credit Points": 10, "Prerequisites": "ITP122"},
        {"Subject Code": "ICC104", "Subject Name": "Introduction to Cloud Computing", "Type": "Core", "Credit Points": 10, "Prerequisites": "ITP122"},
        {"Subject Code": "NDS203", "Subject Name": "Networking and Database Systems", "Type": "Core", "Credit Points": 10, "Prerequisites": "MIS102"},
        {"Subject Code": "HCD206", "Subject Name": "Human Centred Design for Software Engineering", "Type": "Core", "Credit Points": 10, "Prerequisites": "DIG103A"},
        {"Subject Code": "CEN207", "Subject Name": "Creative Enterprise", "Type": "Core", "Credit Points": 10, "Prerequisites": "HCD206"},
        {"Subject Code": "SBD303", "Subject Name": "Secure by Design", "Type": "Core", "Credit Points": 10, "Prerequisites": "NDS203"},

        # Elective slots (no code, just placeholders to be "filled"):
        {"Subject Code": "ELECTIVE_SLOT_1", "Subject Name": "Elective 1", "Type": "Elective", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "ELECTIVE_SLOT_2", "Subject Name": "Elective 2", "Type": "Elective", "Credit Points": 10, "Prerequisites": ""},
    ]
    return pd.DataFrame(data)

def load_elective_bank_adit_df() -> pd.DataFrame:
    # Elective Bank (subset shown; extend if you have the full list)
    # Credits default to 10 unless noted; add prereqs where listed in your doc
    bank = [
        # Level 100 Electives:
         {"Subject Code": "MKT102A", "Subject Name": "Understanding Advertising", "Credit Points": 10, "Prerequisites": ""},
         {"Subject Code": "MKT103A", "Subject Name": "Integrated Marketing Communications", "Credit Points": 10, "Prerequisites": ""},
         {"Subject Code": "PCD101", "Subject Name": "Place, Culture and Destination Management", "Credit Points": 10, "Prerequisites": ""},
         {"Subject Code": "IDO107", "Subject Name": "Introduction to DevOps", "Credit Points": 10, "Prerequisites": ""},
         {"Subject Code": "PST107", "Subject Name": "Probabilities and Statistics", "Credit Points": 10, "Prerequisites": ""},
         {"Subject Code": "CAI104", "Subject Name": "Concepts in Artificial Intelligence", "Credit Points": 10, "Prerequisites": ""},
         {"Subject Code": "JSF100", "Subject Name": "JavaScript Fundamentals", "Credit Points": 10, "Prerequisites": ""},
         {"Subject Code": "GPR103", "Subject Name": "2D Game Programming", "Credit Points": 10, "Prerequisites": ""},
         {"Subject Code": "CBS131", "Subject Name": "Cybersecurity Principles", "Credit Points": 10 , "Prerequisites": ""},

        # Level 200 Electives:
        {"Subject Code": "MKG201", "Subject Name": "Business-2-Business Marketing", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "PRL201", "Subject Name": "Content Creation for Social Media", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "COMR2002", "Subject Name": "Business Information Systems", "Credit Points": 10, "Prerequisites": ""},
        {"Subject Code": "CLR204", "Subject Name": "Classification and Regression", "Credit Points": 10, "Prerequisites": "PST107"},
        {"Subject Code": "AAI202", "Subject Name": "Applications of Artificial Intelligence", "Credit Points": 10, "Prerequisites": "CAI104"},
        {"Subject Code": "WAD200", "Subject Name": "Web App Development", "Credit Points": 10, "Prerequisites": "JSF100"},
        {"Subject Code": "AIP201", "Subject Name": "AI & Physics for Games", "Credit Points": 10, "Prerequisites": "GPR103"},
        {"Subject Code": "RGP204", "Subject Name": "Rapid Game Prototype", "Credit Points": 10, "Prerequisites": "GPR103"},
        {"Subject Code": "GDP204", "Subject Name": "Game Development PlayStation", "Credit Points": 10, "Prerequisites": "GPR103"},
        {"Subject Code": "EPT232", "Subject Name": "Ethical Hacking and Penetration Testing", "Credit Points": 10 , "Prerequisites": "CBS131"},
    ]
    return pd.DataFrame(bank)

def load_curriculum_and_bank_adit_same_df() -> pd.DataFrame:
    """
    Load curriculum and elective bank into a single DataFrame.
    This is useful for matching transcript with both curriculum and electives.
    """
    curriculum_df = load_curriculum_adit_df()
    bank_df = load_elective_bank_adit_df()

    # Add a column to distinguish between core/elective subjects
    curriculum_df['Source'] = 'Curriculum'
    bank_df['Source'] = 'Elective Bank'

    # Concatenate the two DataFrames
    combined_df = pd.concat([curriculum_df, bank_df], ignore_index=True)
    
    return combined_df