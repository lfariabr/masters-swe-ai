import pandas as pd
import re

def extract_score(score_str):
    try:
        match = re.search(r'\d+', str(score_str))
        return int(match.group()) if match else None
    except:
        return None

def nps_type(score):
    if score is None or pd.isna(score):
        return "Unknown"
    elif score >= 9:
        return "Promoter"
    elif score >= 7:
        return "Passive"
    else:
        return "Detractor"

def classify_nps(df):
    df["ScoreValue"] = df["Score"].apply(extract_score)
    df["NPS Type"] = df["ScoreValue"].apply(nps_type)
    return df

def calculate_nps(df):
    valid_df = df[df["NPS Type"] != "Unknown"]
    total = len(valid_df)
    if total == 0:
        return 0.0
    promoters = len(valid_df[valid_df["NPS Type"] == "Promoter"])
    detractors = len(valid_df[valid_df["NPS Type"] == "Detractor"])
    return round(((promoters - detractors) / total) * 100, 2)

def load_and_process_csv(file):
    df = pd.read_csv(file)
    df = classify_nps(df)
    return df