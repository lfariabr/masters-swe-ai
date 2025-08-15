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
    Build and return a QStandardItemModel from existing hardcoded data loaders.
    - If transcript: load from your existing hardcoded transcript DataFrame.
    - If curriculum: load from load_curriculum_df().
    """
    pass #TODO

def is_dark_mode():
    palette = QApplication.instance().palette()
    bg = palette.color(QPalette.Window)
    return bg.lightness() < 128