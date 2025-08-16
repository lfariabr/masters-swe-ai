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
    model = QStandardItemModel(df.shape[0], df.shape[1])
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
    if is_transcript:
        # keep transcript behavior unchanged (XLSX sample)
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "sample_transcript.xlsx")
        return load_excel_as_model(file_path)
    
    # Hardcoded curriculum data
    from data.courses.msit_ad import load_curriculum_df, load_elective_bank_df, load_curriculum_and_bank_same_df
    from data.courses.adit21 import load_curriculum_adit_df, load_elective_bank_adit_df, load_curriculum_and_bank_adit_same_df

    # Choose the appropriate function based on the course type #TODO
    # if 'msit' in __file__:
    #     df = load_curriculum_and_bank_same_df()
    # elif 'adit21' in __file__:
    #     df = load_curriculum_and_bank_adit_same_df()
    # else:
    #     # Return error or empty model if no match
    #     raise ValueError("Unsupported course type for hardcoded curriculum.")
    
    # df = load_curriculum_df()
    
    # testing to see if makes sente to bring both curriculum + bank together
    df = load_curriculum_and_bank_same_df()

    desired_cols = ["Subject Code", "Subject Name", "Type", "Credit Points", "Prerequisites"]
    cols = [c for c in desired_cols if c in df.columns] or list(df.columns)
    return _df_to_qmodel(df[cols])

def is_dark_mode():
    palette = QApplication.instance().palette()
    bg = palette.color(QPalette.Window)
    return bg.lightness() < 128