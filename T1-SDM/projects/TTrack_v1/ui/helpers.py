import csv
import pandas as pd
from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
                        QTableWidgetItem, 
                        QFileDialog, 
                        QPushButton, 
                        QWidget, 
                        QHBoxLayout,
                        QMessageBox
                        )

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

def export_table_to_csv(table, title="Export Table", default_file_name="results_export.csv"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suggested_name = f"{default_file_name.replace('.csv', '')}_{timestamp}.csv"
    
    path, _ = QFileDialog.getSaveFileName(
        None, title, suggested_name, "CSV files (*.csv)"
    )
    
    if not path:
        return
    
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write headers
        headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]
        writer.writerow(headers)

        # Write rows
        for row in range(table.rowCount()):
            row_data = [table.item(row, col).text() if table.item(row, col) else "" for col in range(table.columnCount())]
            writer.writerow(row_data)

def set_download_button_style(button, color, is_dark):
    button.setStyleSheet(f"""
        QPushButton {{
            background-color: {color};
            color: white;
            border: none;
            padding: 4px 10px;
            font-size: 12px;
            border-radius: 6px;
            max-width: 150px;
        }}
        QPushButton:hover {{
            background-color: {'#1e6fa1' if is_dark else '#1665a2'};
        }}
    """)

def download_button(table, parent, filename="export.csv"):
    """Create a properly styled download button"""
    button = QPushButton("⬇️ Export CSV")
    button.clicked.connect(lambda: export_table_to_csv(table, "Export Results", filename))
    
    # Apply proper theme-aware styling (remove unsupported transform properties)
    is_dark = parent.theme_manager.is_dark_mode
    
    button.setStyleSheet(f"""
        QPushButton {{
            background-color: #2980b9;
            color: white;
            border: none;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: 500;
            border-radius: 6px;
            min-width: 120px;
            max-width: 150px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        QPushButton:hover {{
            background-color: #3498db;
        }}
        QPushButton:pressed {{
            background-color: #1f5f8b;
        }}
        QPushButton:focus {{
            border: 2px solid #74b9ff;
        }}
    """)
    
    # Create a right-aligned container
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 5, 0, 5)
    layout.setSpacing(0)
    layout.addStretch()  # Push button to the right
    layout.addWidget(button)
    
    container.setMaximumHeight(45)
    return container

def download_processed_data(parent):
    """
    Download all processed data (results, summary, electives) as CSV files
    """
    from PyQt5.QtWidgets import QFileDialog
    
    # Check if data is available
    if not hasattr(parent.data_processor, 'results_df') or parent.data_processor.results_df is None:
        QMessageBox.warning(parent, "No Data", "No processed data to download. Please process data first.")
        return
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Get the data
        results_df = parent.data_processor.results_df
        transcript_df = parent.data_processor.transcript_df
        
        # Generate summary and electives data (use v2 engine + canonical bank)
        from core.engine import (
            generate_progress_summary_v2,
            suggest_electives_v2,
        )

        # Determine which course bank to use (ADIT/MSIT)
        course_key = getattr(parent, 'selected_course', 'ADIT')
        course_key = (course_key or 'ADIT').strip().upper()
        if course_key == 'MSIT':
            from data.courses.msit_ad import load_elective_bank_df as _load_bank
        else:
            from data.courses.adit21 import load_elective_bank_adit_df as _load_bank

        elective_bank_df = _load_bank()

        summary_df = generate_progress_summary_v2(results_df)
        electives_df = suggest_electives_v2(
            results_df,
            elective_bank_df,
            transcript_df,
            max_electives=20
        )
        
        # Choose directory for saving
        directory = QFileDialog.getExistingDirectory(
            parent, 
            "Select Directory to Save Processed Data", 
            ""
        )
        
        if not directory:
            return
        
        # Save all files
        results_file = f"{directory}/results_{timestamp}.csv"
        summary_file = f"{directory}/summary_{timestamp}.csv"
        electives_file = f"{directory}/suggested_electives_{timestamp}.csv"
        
        results_df.to_csv(results_file, index=False)
        summary_df.to_csv(summary_file, index=False)
        electives_df.to_csv(electives_file, index=False)
        
        # Show success message
        QMessageBox.information(
            parent,
            "✅ Download Complete",
            f"Processed data saved successfully!\n\n"
            f"📄 Results: results_{timestamp}.csv\n"
            f"📊 Summary: summary_{timestamp}.csv\n"
            f"🧠 Suggested Electives: suggested_electives_{timestamp}.csv\n\n"
            f"📁 Location: {directory}"
        )
        
    except Exception as e:
        QMessageBox.critical(
            parent,
            "❌ Download Failed",
            f"Failed to download processed data:\n\n{str(e)}"
        )

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
