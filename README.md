# AI Study Buddy (Flashcard Generator)

Turn raw study notes into interactive flashcards powered by a Hugging Face **text-generation** model.  
Built with **Flask + MySQL + Vanilla JS**. Designed for fast prototyping and easy monetization.

## ✨ Features
- Paste notes → get **5 question–answer flashcards**
- Flip-card UI (front: question, back: answer)
- Save cards to **MySQL**
- Simple, beginner-friendly codebase

## 🧱 Tech Stack
- Frontend: HTML5, CSS3, JavaScript
- Backend: Python (Flask)
- Database: MySQL
- AI: Hugging Face Inference API (text-generation model, default: `google/flan-t5-base`)
- Deployment-ready: Gunicorn (optional)

## 🚀 Quickstart (Local)
1. **Clone** this repo, then create a virtual environment and install deps:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set environment variables** (copy and edit `.env.example` → `.env`):
   ```bash
   cp .env.example .env
   # Fill in: HF_API_KEY, MYSQL_* and optional HF_MODEL
   ```

3. **Create MySQL DB and table**:
   ```sql
   -- Run this in your MySQL client:
   SOURCE schema.sql;
   ```

4. **Run the app**:
   ```bash
   flask --app app run --debug
   # Visit http://127.0.0.1:5000
   ```

## 🔐 Environment Variables
See `.env.example` for full list:
- `HF_API_KEY` – your Hugging Face Inference API token
- `HF_MODEL` – (optional) text-generation model (default `google/flan-t5-base`)
- `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`, `MYSQL_PORT`

## 🧠 How AI Generation Works
We call a **text-generation** model on Hugging Face with a structured prompt:
> “Generate exactly 5 question–answer pairs as a JSON array ... based on these notes ...”

We then **parse the JSON** in the response and persist the pairs.

## 🧪 Testing (manual quick check)
- Paste a short passage (3–6 sentences).  
- Click **Generate Flashcards**.  
- Flip cards to view answers.  
- Confirm rows appear in `flashcards` table.

## 🛠️ Notes
- If the model returns extra text around JSON, the backend extracts the JSON block.
- For production, add authentication, users, and rate limits.

## 📄 License
MIT