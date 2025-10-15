import pandas as pd
import re

def extract_score(score_str):
    try:
        match = re.search(r'\d+', str(score_str))
        return int(match.group()) if match else None
    except:
        return None

def nps_type(score, max_score):
    if score is None or pd.isna(score):
        return "Unknown"

    if max_score <= 5:
        # Scale from 1–5
        if score >= 4:
            return "Promoter"
        elif score == 3:
            return "Passive"
        else:
            return "Detractor"
    else:
        # Scale from 1–10
        if score >= 9:
            return "Promoter"
        elif score >= 7:
            return "Passive"
        else:
            return "Detractor"

def classify_nps(df):
    df["Score"] = df["Score"].apply(extract_score)
    # Detect max score
    max_score = df["Score"].max()

    df["NPS Type"] = df["Score"].apply(lambda x: nps_type(x, max_score))
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

    # Clean and process date columns
    df["Year"] = df["Year"].astype(str).str.replace(",", "")
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, format="mixed", errors="coerce")
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    return df

def get_year_store_filters(df):
    years = df["Year"].unique().tolist()
    stores = df["Store"].unique().tolist()
    return years, stores
    