# Streamlit Climate Dashboard (Starter)

Minimal, testable scaffold with:
- Secure login (hashed passwords via passlib)
- Per-user settings in SQLite
- Per-user CSV upload (private to each user)
- Tiny dashboard (summary + quick chart)
- Chatbot placeholder page

## Local Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Create `.streamlit/secrets.toml` based on `.streamlit/secrets.example.toml` (do **not** commit real secrets).

## Deploy on Streamlit Community Cloud
1. Push this repo to GitHub.
2. Create a new Streamlit app from the repo, set **Main file** to `app.py`.
3. In the app's **Settings → Secrets**, add:
   ```toml
   ADMIN_USERNAME = "admin"
   ADMIN_PASSWORD = "a-strong-password"
   ```
4. Deploy. The app creates the `data/` folder at runtime (ephemeral in the cloud). For production, move uploads to cloud storage.

## Repo layout

```
streamlit-climate-dashboard/
├─ app.py
├─ requirements.txt
├─ .gitignore
├─ .streamlit/
│  ├─ config.toml
│  └─ secrets.example.toml
├─ lib/
│  ├─ __init__.py
│  ├─ db.py
│  └─ auth.py
├─ pages/
│  ├─ 1_Upload.py
│  ├─ 2_Settings.py
│  ├─ 3_Dashboard.py
│  └─ 4_Chatbot.py
└─ data/ (created at runtime; ignored by git)
```
