import pandas as pd
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette

def load_excel_as_model(file_path):
    df = pd.read_excel(file_path)
    model = QStandardItemModel()
    model.setColumnCount(len(df.columns))
    model.setHorizontalHeaderLabels(df.columns.tolist())

    for row in df.itertuples(index=False):
        items = [QStandardItem(str(cell)) for cell in row]
        model.appendRow(items)

    return model

def _df_to_qmodel(df: pd.DataFrame) -> QStandardItemModel:
    """Convert a DataFrame into a read-only QStandardItemModel."""
    # Note: starting with 0 rows, then append. If we pre-allocate rows and also append,
    # we'll end up with an initial block of empty rows (visible as blank rows in the UI).
    model = QStandardItemModel(0, df.shape[1])
    model.setHorizontalHeaderLabels(df.columns.tolist())
    for r in range(df.shape[0]):
        row_items = []
        for c in range(df.shape[1]):
            it = QStandardItem(str(df.iat[r, c]))
            it.setEditable(False)
            row_items.append(it)
        model.appendRow(row_items)
    return model

def load_as_model_hardcoded(is_transcript: bool = True) -> QStandardItemModel:
    """
    Build and return a QStandardItemModel.
    - Transcript (True): fall back to the existing XLSX loader (unchanged behavior).
        student's progress in courses (load_excel_as_model).
    - Curriculum (False): build from hardcoded course data (load_curriculum_df).
        academic course requirements (load_curriculum_df).
    """

    # Use the same sample XLSX used by the regular sample loader
    if is_transcript:
        import os
        gui_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(gui_dir)
        file_path = os.path.join(project_root, "services", "data", "sample_academic_transcript_v2.xlsx")
        return load_excel_as_model(file_path)
    
    # Hardcoded Course Curriculum data - Can be replaced in the future with a dropdown menu
    from data.courses.msit_ad import (
        load_curriculum_df, load_elective_bank_df, load_curriculum_and_bank_same_df)
    from data.courses.adit21 import (
        load_curriculum_adit_df, load_elective_bank_adit_df, load_curriculum_and_bank_adit_same_df)

    # Default to ADIT combined (curriculum + elective bank) for hardcoded curriculum path
    df = load_curriculum_and_bank_adit_same_df()

    desired_cols = ["Subject Code", "Subject Name", "Type", "Credit Points", "Prerequisites"]
    cols = [c for c in desired_cols if c in df.columns] or list(df.columns)
    return _df_to_qmodel(df[cols])

def is_dark_mode():
    palette = QApplication.instance().palette()
    bg = palette.color(QPalette.Window)
    return bg.lightness() < 128