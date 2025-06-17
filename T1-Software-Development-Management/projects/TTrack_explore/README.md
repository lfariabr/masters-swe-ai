# 📘 TTrack – Torrens Degree Tracker

TTrack is a desktop application that helps **students and academic advisors** monitor academic progress by automatically checking a student's completed subjects against the requirements of their degree program. It simplifies the process of degree auditing and subject planning using a clean, intuitive interface built with **PyQt5**.

---

## ✨ Key Features

- ✅ Upload academic **transcripts** (.xlsx)
- 📚 Upload **program curriculum** (.xlsx) with core and elective subject definitions
- 🧠 Automatically **match** completed subjects to degree requirements
- 📊 Display **progress summary**: completed vs pending subjects
- 📌 Recommend eligible **elective subjects** based on unmet criteria
- 🔎 Parse and validate credit points, elective groupings, and prerequisites
- 💻 Fully offline desktop experience (no internet required)

---

## 📂 Project Structure

```
ttrack_pyqt5/
├── main.py                  # App entry point
├── gui/
│   ├── main_window.py       # Main application window
│   └── upload_widget.py     # File upload interface
├── utils/
│   └── parser.py            # Functions for parsing Excel files
├── data/                    # Sample curriculum and transcript files
├── db/                      # (Optional) SQLite or local data files
├── assets/                  # Icons and images
├── tests/                   # Unit tests (coming soon)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## ⚙️ Technologies Used

- **Frontend**: PyQt5 (custom widgets, modern layout)
- **Backend**: Python 3.10+
- **Data Parsing**: pandas, openpyxl
- **Visualization (planned)**: matplotlib or Plotly
- **Packaging (optional)**: PyInstaller or cx_Freeze

---

## 🚀 Getting Started

### 1. Clone the repo or extract the folder:

```bash
git clone https://github.com/yourname/ttrack-pyqt5.git
cd ttrack-pyqt5
```

### 2. Install dependencies

We recommend creating a virtual environment first:

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python main.py
```

---

## 🧪 Testing It Out

Use the included sample data:

- [`sample_transcript.xlsx`](data/sample_transcript.xlsx)
- [`sample_curriculum.xlsx`](data/sample_curriculum.xlsx)

---

## 🛠 Future Improvements

- Add support for prerequisite chains
- GPA calculation from grades
- Advanced rule builder UI
- Export progress report to PDF
- Dashboard analytics with filters

---

## 👨‍💻 Author

Developed by **Luis Faria** as part of the Master of Software Engineering (AI) at Torrens University.

---

## 📄 License

This project is open-source and free to use for academic or personal projects.
