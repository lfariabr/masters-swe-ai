from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableWidgetItem
import pandas as pd

def model_to_dataframe(model):
    """Convert QAbstractItemModel to pandas DataFrame"""
    if not model:
        return None
        
    rows = model.rowCount()
    cols = model.columnCount()
    
    # Get headers
    headers = []
    for i in range(cols):
        headers.append(model.headerData(i, Qt.Horizontal, Qt.DisplayRole) or f"Column {i}")
    
    # Get data
    data = []
    for row in range(rows):
        row_data = []
        for col in range(cols):
            index = model.index(row, col)
            row_data.append(model.data(index, Qt.DisplayRole))
        data.append(row_data)
        
    return pd.DataFrame(data, columns=headers)

def populate_table(table_widget, df):
    """Populate a QTableWidget with DataFrame data"""
    if df is None or (hasattr(df, 'empty') and df.empty):
        return
        
    # Reset the table
    table_widget.clear()
    
    # Handle case where df is a Series (like from value_counts)
    if hasattr(df, 'to_frame'):
        df = df.to_frame()
    
    # Convert index to column for DataFrames with a MultiIndex
    if hasattr(df, 'index') and hasattr(df.index, 'names') and any(df.index.names):
        df = df.reset_index()
    
    # Set row and column count
    rows = len(df)
    cols = len(df.columns) if hasattr(df, 'columns') else 1
    table_widget.setRowCount(rows)
    table_widget.setColumnCount(cols)
    
    # Set headers
    if hasattr(df, 'columns'):
        table_widget.setHorizontalHeaderLabels([str(c) for c in df.columns])
    if hasattr(df, 'index'):
        table_widget.setVerticalHeaderLabels([str(i) for i in df.index])
    
    # Populate data
    for i in range(rows):
        for j in range(cols):
            try:
                if hasattr(df, 'iloc'):
                    value = df.iloc[i, j] if cols > 1 else df.iloc[i]
                else:
                    value = df[i] if hasattr(df, '__getitem__') else str(df)
                item = QTableWidgetItem(str(value) if value is not None else "")
                table_widget.setItem(i, j, item)
            except Exception as e:
                print(f"Error populating cell ({i},{j}): {str(e)}")
                
    table_widget.resizeColumnsToContents()

def set_button_style(button, main_color, is_dark_mode, smaller=False):
    """Apply consistent styling to buttons
    
    Args:
        button: QPushButton to style
        main_color: Main color for the button
        is_dark_mode: Whether dark mode is enabled
        smaller: Whether to use a smaller button style (default: False)
    """
    text_color = "#ffffff" if not is_dark_mode else "#000000"
    hover_color = "#1a2533" if not is_dark_mode else "#e0e0e0"
    
    # Adjust padding and font size for smaller buttons
    padding = "8px 12px" if smaller else "10px 20px"
    font_size = "12px" if smaller else "14px"
    
    button.setStyleSheet(f"""
        QPushButton {{
            background-color: {main_color};
            color: {text_color};
            padding: {padding};
            font-size: {font_size};
            border-radius: 6px;
            border: 1px solid #cccccc;
        }}
        QPushButton:disabled {{
            background-color: #cccccc;
            color: #666666;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
            color: {'#ffffff' if not is_dark_mode else '#000000'};
        }}
    """)

def buttons():
    #TODO
    pass

def dialogs():
    #TODO
    pass

def tables():
    #TODO
    pass

def titles():
    #TODO
    pass

def subtitles():
    #TODO
    pass
