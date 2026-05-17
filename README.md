# Smart Toll Agent 🚗💳

An AI-powered Smart City Toll Enforcement System built using FastAPI, Streamlit, Gemini AI, ChromaDB, and LlamaIndex.

## Features

- AI-powered toll inspection
- Vehicle telemetry analysis
- Overspeed detection
- Traffic law lookup using RAG
- Fine calculation system
- Toll deduction simulation
- Streamlit dashboard UI
- FastAPI backend APIs
- ChromaDB vector storage

---

## Tech Stack

- Python
- FastAPI
- Streamlit
- Gemini AI
- LlamaIndex
- ChromaDB
- Pandas

---

## Project Structure

```bash
smart_toll_agent/
│
├── backend/
│   ├── app.py
│   ├── tools.py
│   └── data/
│
├── frontend/
│   └── dashboard.py
│
├── requirements.txt
├── README.md
└── venv/
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/smart-toll-agent.git
cd smart-toll-agent
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
.\venv\Scripts\Activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Backend

```bash
uvicorn backend.app:app --reload
```

Backend URL:

```bash
http://127.0.0.1:8000/docs
```

---

## Run Frontend

```bash
streamlit run frontend/dashboard.py
```

Frontend URL:

```bash
http://localhost:8501
```

---

## Future Improvements

- Real-time CCTV integration
- License plate OCR
- Payment gateway integration
- Cloud deployment
- Real-time traffic analytics

---

## Author

Dhananjay Karad
