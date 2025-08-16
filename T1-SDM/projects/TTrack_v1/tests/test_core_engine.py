import pandas as pd
import pytest

from core.engine import (
    parse_prereqs,
    normalize_subject_codes,
    suggest_electives_v2,
)


def test_parse_prereqs_variants():
    # empty and None cases
    assert parse_prereqs("") == []
    assert parse_prereqs(None) == []

    # mixed separators supported by current implementation: comma, plus, slash
    # note: spaces and the word 'and' are not split by current regex; hyphens are not allowed inside codes
    s = "itw601,REM502+ITA602/BIZ501"
    # Only tokens that look like codes: letters then 3 digits
    assert parse_prereqs(s) == ["ITW601", "REM502", "ITA602", "BIZ501"]


def test_normalize_subject_codes_removes_symbols():
    df = pd.DataFrame({"Subject Code": [" itw-601 ", "Rem 502", "ITA_602", "biz/501"]})
    out = normalize_subject_codes(df, col="Subject Code")
    assert out["Subject Code"].tolist() == ["ITW601", "REM502", "ITA602", "BIZ501"]


def test_suggest_electives_v2_respects_prereqs():
    # transcript has only ITW601 completed
    transcript_df = pd.DataFrame({
        "Subject Code": ["ITW601"],
        "Subject Name": ["Intro Work"],
    })

    # elective bank with two electives: one needs REM502 (not met), one needs ITW601 (met)
    elective_bank_df = pd.DataFrame({
        "Subject Code": ["ITA602", "BIZ501"],
        "Subject Name": ["Advanced ITA", "Business Basics"],
        "Credit Points": [10, 10],
        "Prerequisites": ["REM502", "ITW601"],
    })

    # curriculum not used directly by suggest_electives_v2, but called in v2 flow, keep minimal here
    result_df = pd.DataFrame({
        "Subject Code": ["CORE100"],
        "Subject Name": ["Some Core"],
        "Type": ["core"],
        "Status": ["❌ Missing"],
    })

    recs = suggest_electives_v2(result_df, elective_bank_df, transcript_df, max_electives=3)

    # Should only recommend the elective whose prereq (ITW601) is satisfied
    assert recs["Subject Code"].tolist() == ["BIZ501"]
    assert set(recs.columns) == {"Subject Code", "Subject Name", "Credit Points", "Prerequisites"}
