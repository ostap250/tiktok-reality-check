# 🦉 TikTok Reality Check

**Discover your scrolling persona and see what you could have accomplished instead.**

A privacy-focused Streamlit web application that analyzes your TikTok data export to reveal your viewing patterns, calculate wasted time, and provide absurd comparisons that put your scrolling habits into perspective.

---

## 📖 About

TikTok Reality Check is a local web application that processes your TikTok data export (JSON) to provide insights into your scrolling behavior. The app runs entirely on your machine—your data never leaves your browser or localhost, ensuring complete privacy.

Whether you're a night owl scrolling until 3 AM or a morning scroller checking TikTok before coffee, this app reveals your digital habits with a modern, glassmorphic interface and thought-provoking comparisons.

---

## ✨ Features

### 📊 Deep Analysis
Calculate exactly how much time you've spent scrolling: total videos watched, hours wasted, and days lost to the infinite scroll.

### 🎭 Persona Detection
Discover your scrolling persona based on your peak viewing hours:
- 🦉 **The Night Owl** - Late-night scrolling enthusiast
- ☀️ **The Early Bird** - Morning scroll sessions
- ☕ **The Lunchtime Scroller** - Midday TikTok breaks
- 🌇 **The Evening Binger** - Post-work scrolling marathon

Enable "Guilt Trip Mode" for harsher, more direct persona descriptions.

### 🤯 The Absurd Reality
A horizontal, draggable slider that compares your scroll time to real-life achievements:
- "You could have become President of Argentina X times"
- "Cook X packs of instant noodles"
- "Walk to the Moon and back"
- "Learn X languages to fluency"
- And many more absurd comparisons!

### 🎨 Modern UI
Experience a premium "Passive Dark Glassmorphism" design with:
- Deep charcoal background (#0f1116)
- Subtle glass-effect cards with backdrop blur
- Smooth animations and hover effects
- Interactive metric cards
- Clean, minimalist aesthetic

### 🔒 Privacy First
Your data stays local. The app processes your JSON file entirely in your browser/localhost—no data is sent to external servers or stored anywhere.

---

## 📸 Screenshots

![Dashboard Screenshot](screenshots/dashboard.png)
*Main dashboard showing stats, persona, and absurd comparisons*

![Upload Screen Screenshot](screenshots/upload.png)
*Clean upload interface*

![Persona Card Screenshot](screenshots/persona.png)
*Persona detection with glassmorphic card design*

---

## 🚀 Installation & Run

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/tiktok-reality-check.git
cd tiktok-reality-check
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install streamlit pandas
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`.

---

## 📥 How to Get Your TikTok Data

1. **Open TikTok App** on your mobile device
2. **Go to Settings** → **Privacy** → **Download Your Data**
3. **Request Data Export** (may take 24-48 hours)
4. **Download the ZIP file** when TikTok sends you the email
5. **Extract the ZIP** and locate the JSON file
6. **Navigate to:** `Activity` → `Video Browsing History` → `VideoList.json`
7. **Upload** this JSON file in the app

**Note:** The app expects the JSON structure: `['Activity']['Video Browsing History']['VideoList']`

---

## 🏗️ Project Structure

This project follows a **modular architecture** based on the **Separation of Concerns** principle:

```
tiktok-reality-check/
│
├── app.py              # Main controller - orchestrates the application
├── logic.py            # Pure data processing (JSON parsing, calculations)
├── ui.py               # HTML generation functions
├── utils.py            # Helper utilities (CSS loading, JavaScript)
├── styles.css          # Design system - Passive Dark Glassmorphism theme
│
├── .gitignore          # Git ignore rules (protects user JSON files)
└── README.md           # This file
```

### Architecture Overview

- **`app.py`**: Main entry point that handles session state, view routing, and coordinates between modules
- **`logic.py`**: Business logic layer - processes JSON, calculates stats, determines persona, generates absurd comparisons
- **`ui.py`**: Presentation layer - generates HTML strings for all UI components
- **`utils.py`**: Utility functions for CSS injection and JavaScript code
- **`styles.css`**: Complete design system with glassmorphic styling

This modular approach ensures:
- ✅ Easy maintenance and testing
- ✅ Clear separation of concerns
- ✅ Reusable components
- ✅ Scalable architecture

---

## 🛠️ Technologies Used

- **Streamlit** - Web application framework
- **Pandas** - Data processing and analysis
- **Python** - Core programming language
- **CSS3** - Modern glassmorphic styling with backdrop filters

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## ⚠️ Disclaimer

This application is for educational and self-reflection purposes only. It processes your data locally and does not store or transmit any information. Use responsibly and remember: awareness is the first step toward change.

---

**Made with ❤️ for digital wellness awareness**

