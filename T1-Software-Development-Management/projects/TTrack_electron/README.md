# 📊 TTrack – Excel Electron Desktop App

A cross-platform desktop application built using **React**, **Node.js**, and **Electron**, designed for uploading and displaying two Excel files (Transcript & Curriculum) inside scrollable panels.

## 🚀 Features

- Upload and parse **two Excel files** (`.xls` or `.xlsx`)
- Backend converts Excel sheets to **JSON** using `xlsx`
- View parsed data in **separate scrollable boxes**
- Runs as a **native desktop app** using Electron
- Clean UI with headings and upload buttons
- Local Express.js server handles file parsing
- Ready for distribution: **Builds `.exe` installer**

## 🛠️ Tech Stack

- 🔵 **React** (frontend)
- 🟢 **Node.js + Express** (backend)
- 🧠 **Electron** (desktop wrapper)
- 📦 `xlsx`, `multer`, `cors` (file parsing & handling)
- 🧰 `concurrently`, `wait-on`, `electron-builder`, `cross-env`

## 🔧 Available NPM Scripts

| Script                        | Description                                           |
|------------------------------|-------------------------------------------------------|
| `npm start`                  | Start React dev server (browser disabled)             |
| `npm run server`             | Start Express backend                                 |
| `npm run dev`                | Start both backend and frontend in dev mode           |
| `npm run electron`           | Start Electron with local `build/` output             |
| `npm run electron-dev`       | Dev mode: backend + React + Electron window           |
| `npm run start-electron`     | Alias for `npm run electron-dev`                      |
| `npm run build`              | Builds React app                                      |
| `npm run dist`               | Build Electron `.exe` installer (Windows x64)         |
| `npm run full-build`         | Build React + Electron installer                      |
| `npm run clean`              | Remove `dist/` and `build/` folders                   |

## 🧪 How to Run in Development


## Install dependencies
```
npm install
```

## Run the app in Electron + Dev mode
```
npm run start-electron
```

## Running Build for dekstop app (Current not generating an exe installer file)
```
npm run full-build
```

This will:
Build the React frontend
Package everything with Electron
Output a .exe installer in the dist/ folder
