from typing import Dict, List, Optional, Tuple

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QSizePolicy, QTabWidget
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtChart import (
    QChart, QChartView, QPieSeries, QPieSlice, QBarSeries, QBarSet,
    QBarCategoryAxis, QValueAxis, QHorizontalBarSeries
)
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QLinearGradient, QGradient

from models.transcript import AcademicRecord
from analysis.progress_analyzer import ProgressResult, RequirementStatus, ProgressAnalyzer

class ProgressWidget(QWidget):
    """Widget to display student progress with charts and tables."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress_result: Optional[ProgressResult] = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # Header
        self.header_label = QLabel("Academic Progress Overview")
        self.header_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        """)
        
        # Create tab widget for different views
        self.tabs = QTabWidget()
        
        # Progress Summary Tab
        self.summary_tab = QWidget()
        self.setup_summary_tab()
        
        # Requirements Tab
        self.requirements_tab = QWidget()
        self.setup_requirements_tab()
        
        # Add tabs
        self.tabs.addTab(self.summary_tab, "Summary")
        self.tabs.addTab(self.requirements_tab, "Requirements")
        
        # Add widgets to main layout
        layout.addWidget(self.header_label)
        layout.addWidget(self.tabs)
    
    def setup_summary_tab(self):
        """Set up the summary tab with progress charts."""
        layout = QVBoxLayout(self.summary_tab)
        
        # Top row with progress cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)
        
        # Completion Card
        self.completion_card = self.create_progress_card(
            "Program Completion", "0%", "Overall progress toward degree"
        )
        
        # GPA Card
        self.gpa_card = self.create_progress_card(
            "Current GPA", "0.00", "Cumulative Grade Point Average"
        )
        
        # Credits Card
        self.credits_card = self.create_progress_card(
            "Credits Earned", "0 / 0", "Credits completed out of required"
        )
        
        cards_layout.addWidget(self.completion_card)
        cards_layout.addWidget(self.gpa_card)
        cards_layout.addWidget(self.credits_card)
        
        # Charts row
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(15)
        
        # Progress Chart
        self.progress_chart_view = self.create_progress_chart()
        
        # Requirements Chart
        self.requirements_chart_view = self.create_requirements_chart()
        
        charts_layout.addWidget(self.progress_chart_view, 2)
        charts_layout.addWidget(self.requirements_chart_view, 1)
        
        # Add to main layout
        layout.addLayout(cards_layout)
        layout.addLayout(charts_layout, 1)
    
    def setup_requirements_tab(self):
        """Set up the requirements tab with detailed table."""
        layout = QVBoxLayout(self.requirements_tab)
        
        # Requirements Table
        self.requirements_table = QTableWidget()
        self.requirements_table.setColumnCount(6)
        self.requirements_table.setHorizontalHeaderLabels([
            "Code", "Name", "Status", "Credits", "Progress", "Semester"
        ])
        
        # Configure table
        header = self.requirements_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Code
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Name
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Credits
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Progress
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Semester
        
        self.requirements_table.verticalHeader().setVisible(False)
        self.requirements_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.requirements_table)
    
    def create_progress_card(self, title: str, value: str, description: str) -> QWidget:
        """Create a progress card widget."""
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
                border: 1px solid #dee2e6;
            }
            QLabel#value {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
            QLabel#title {
                font-size: 14px;
                font-weight: bold;
                color: #6c757d;
            }
            QLabel#description {
                font-size: 12px;
                color: #6c757d;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setObjectName("title")
        
        value_label = QLabel(value)
        value_label.setObjectName("value")
        
        desc_label = QLabel(description)
        desc_label.setObjectName("description")
        desc_label.setWordWrap(True)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        
        return card
    
    def create_progress_chart(self) -> QChartView:
        """Create a chart showing overall progress."""
        chart = QChart()
        chart.setTitle("Program Progress")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().setVisible(False)
        
        # Create pie series
        series = QPieSeries()
        series.append("Completed", 0)
        series.append("Remaining", 100)
        
        # Set colors
        completed_slice = series.slices()[0]
        completed_slice.setColor(QColor("#2ecc71"))
        completed_slice.setLabelVisible(True)
        completed_slice.setLabelPosition(QPieSlice.LabelInsideHorizontal)
        completed_slice.setLabel("0%")
        
        remaining_slice = series.slices()[1]
        remaining_slice.setColor(QColor("#e74c3c"))
        
        chart.addSeries(series)
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setMinimumHeight(300)
        
        return chart_view
    
    def create_requirements_chart(self) -> QChartView:
        """Create a chart showing requirements status."""
        chart = QChart()
        chart.setTitle("Requirements Status")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # Create bar set
        bar_set = QBarSet("Requirements")
        bar_set << 0 << 0 << 0 << 0  # Not Started, In Progress, Completed, Failed
        
        # Set colors
        bar_set.setColor(QColor("#3498db"))
        
        # Create series and add bar set
        series = QBarSeries()
        series.append(bar_set)
        chart.addSeries(series)
        
        # Set up axes
        categories = ["Not Started", "In Progress", "Completed", "Failed"]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis_x, series)
        
        # Customize appearance
        axis_y = QValueAxis()
        axis_y.setRange(0, 10)  # Will be updated with actual data
        chart.setAxisY(axis_y, series)
        
        chart.legend().setVisible(False)
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setMinimumHeight(300)
        
        return chart_view
    
    def update_progress(self, progress_result: ProgressResult):
        """Update the widget with new progress data."""
        self.progress_result = progress_result
        
        # Update header
        self.header_label.setText(f"Academic Progress - {progress_result.student_name}")
        
        # Update cards
        self.update_cards()
        
        # Update charts
        self.update_charts()
        
        # Update requirements table
        self.update_requirements_table()
    
    def update_cards(self):
        """Update the progress cards with current data."""
        if not self.progress_result:
            return
        
        # Update completion card
        completion_percent = int(self.progress_result.completion_ratio * 100)
        self.completion_card.findChild(QLabel, "value").setText(f"{completion_percent}%")
        
        # Update GPA card
        gpa = self.progress_result.current_gpa or 0.0
        self.gpa_card.findChild(QLabel, "value").setText(f"{gpa:.2f}")
        
        # Update credits card
        total_credits = sum(r.credits_required for r in self.progress_result.requirements)
        earned_credits = sum(r.credits_earned for r in self.progress_result.requirements)
        self.credits_card.findChild(QLabel, "value").setText(f"{earned_credits:.1f} / {total_credits:.1f}")
    
    def update_charts(self):
        """Update the charts with current data."""
        if not self.progress_result:
            return
        
        # Update progress chart
        self.update_progress_chart()
        
        # Update requirements chart
        self.update_requirements_chart()
    
    def update_progress_chart(self):
        """Update the progress pie chart."""
        if not self.progress_result:
            return
        
        chart = self.progress_chart_view.chart()
        series = chart.series()[0]
        
        completion_percent = self.progress_result.completion_ratio * 100
        remaining_percent = 100 - completion_percent
        
        series.slices()[0].setValue(completion_percent)
        series.slices()[0].setLabel(f"{completion_percent:.1f}%")
        series.slices()[1].setValue(remaining_percent)
    
    def update_requirements_chart(self):
        """Update the requirements bar chart."""
        if not self.progress_result:
            return
        
        # Count requirements by status
        status_counts = {
            RequirementStatus.NOT_STARTED: 0,
            RequirementStatus.IN_PROGRESS: 0,
            RequirementStatus.COMPLETED: 0,
            RequirementStatus.FAILED: 0
        }
        
        for req in self.progress_result.requirements:
            status_counts[req.status] += 1
        
        # Update chart
        chart = self.requirements_chart_view.chart()
        series = chart.series()[0]
        bar_set = series.barSets()[0]
        
        for i, status in enumerate([
            RequirementStatus.NOT_STARTED,
            RequirementStatus.IN_PROGRESS,
            RequirementStatus.COMPLETED,
            RequirementStatus.FAILED
        ]):
            bar_set.replace(i, status_counts[status])
        
        # Update y-axis range
        max_value = max(1, max(status_counts.values()))
        chart.axisY().setRange(0, max_value + 1)
    
    def update_requirements_table(self):
        """Update the requirements table with current data."""
        if not self.progress_result:
            return
        
        self.requirements_table.setRowCount(len(self.progress_result.requirements))
        
        status_colors = {
            RequirementStatus.NOT_STARTED: "#6c757d",  # Gray
            RequirementStatus.IN_PROGRESS: "#ffc107",  # Yellow
            RequirementStatus.COMPLETED: "#28a745",    # Green
            RequirementStatus.FAILED: "#dc3545"         # Red
        }
        
        for row, req in enumerate(self.progress_result.requirements):
            # Code
            code_item = QTableWidgetItem(req.code)
            
            # Name
            name_item = QTableWidgetItem(req.name)
            
            # Status
            status_item = QTableWidgetItem(req.status.name.replace("_", " ").title())
            status_item.setForeground(QColor(status_colors[req.status]))
            
            # Credits
            credits_text = f"{req.credits_earned:.1f} / {req.credits_required:.1f}"
            credits_item = QTableWidgetItem(credits_text)
            credits_item.setTextAlignment(Qt.AlignCenter)
            
            # Progress bar (as text for now)
            progress_text = f"{int(req.completion_ratio * 100)}%"
            progress_item = QTableWidgetItem(progress_text)
            progress_item.setTextAlignment(Qt.AlignCenter)
            
            # Semester (if available)
            semester = req.details.get('semester', '')
            semester_item = QTableWidgetItem(str(semester) if semester else '')
            semester_item.setTextAlignment(Qt.AlignCenter)
            
            # Add items to table
            self.requirements_table.setItem(row, 0, code_item)
            self.requirements_table.setItem(row, 1, name_item)
            self.requirements_table.setItem(row, 2, status_item)
            self.requirements_table.setItem(row, 3, credits_item)
            self.requirements_table.setItem(row, 4, progress_item)
            self.requirements_table.setItem(row, 5, semester_item)
        
        # Resize columns to contents
        self.requirements_table.resizeColumnsToContents()
