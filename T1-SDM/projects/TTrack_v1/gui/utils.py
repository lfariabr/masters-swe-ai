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

def is_dark_mode():
    palette = QApplication.instance().palette()
    bg = palette.color(QPalette.Window)
    return bg.lightness() < 128