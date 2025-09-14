# Resume Builder (Django)

A simple, template‑based resume builder built with **Django** on the backend and **HTML/CSS** (with a bit of vanilla JS) on the frontend. Use the app to enter your details (education, work experience, projects, skills, etc.) and render a clean résumé page you can print or save as PDF via your browser.

> Repository: `Sam-Titan/Resume-Builder-Built-Using-Django`

---

## ✨ Features

- Form-driven resume creation using Django views & templates
- Clean, printable HTML output (use browser “Print → Save as PDF” to export)
- Basic static assets for styling
- SQLite database out of the box (dev-friendly)
- Simple project/app split for easy extension
- Live Preview Available
- ATS Scoring Feature
- Gemini LLM Integration
Note: This project focuses on a minimal, easy-to-understand structure, allowing you to extend it with your own models, forms, and templates.

---

## 🏗️ Tech Stack

- **Python** (Django)
- **HTML / CSS**
- **JavaScript** (vanilla)

---

## 📁 Project Structure (top-level)

```
Resume-Builder-Built-Using-Django/
├─ base/            # Django app: views, models, forms (extend here)
├─ resumekart/      # Django project: settings, urls, wsgi/asgi
├─ templates/       # Jinja-like Django templates for pages/resume
├─ static/          # CSS/JS and other static assets
├─ manage.py        # Django management utility
├─ db.sqlite3       # SQLite DB for local dev (can be deleted)
└─ venv/            # (Committed virtual environment; optional to use)
```

> Tip: You don’t need the committed `venv/`. It’s best practice to create your own virtual environment locally.

---

## 🚀 Quickstart

### 1) Clone
```bash
git clone https://github.com/Sam-Titan/Resume-Builder-Built-Using-Django.git
cd Resume-Builder-Built-Using-Django
```

### 2) Create & activate a virtual environment
```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies
If the repository includes `requirements.txt`:
```bash
pip install -r requirements.txt
```

If there is no `requirements.txt`, install Django directly:
```bash
pip install django
```

> Optional (common packages if you plan to extend PDF generation or forms):
> ```bash
> pip install django-crispy-forms xhtml2pdf pillow
> ```

### 4) Database setup
You can **use the existing** `db.sqlite3` or start fresh:
```bash
# start fresh (recommended if you change models)
rm -f db.sqlite3  # use 'del db.sqlite3' on Windows
python manage.py makemigrations
python manage.py migrate
```

### 5) (Optional) Create an admin user
```bash
python manage.py createsuperuser
```

### 6) Run the development server
```bash
python manage.py runserver
```
Visit: http://127.0.0.1:8000/

---

## 🧩 How to Use

1. Open the site locally (or after deployment).
2. Fill out the resume form(s) (education, experience, projects, skills, etc.).
3. Submit to render a styled resume page.
4. **Export:** Use your browser’s **Print → Save as PDF** for a ready-to-share file.

---

## 🔧 Customization

- **Models/Forms:** Add fields in `base/models.py` and corresponding Django forms.
- **Templates:** Modify or create layouts in `templates/`. You can add more templates for different resume styles.
- **Styling:** Update assets in `static/` (CSS/JS). Consider a utility framework like Tailwind or Bootstrap if you prefer.

---

## 🧪 Testing (Optional)

Add tests in `base/tests.py` and run:
```bash
python manage.py test
```

---

## 📦 Deployment Notes

- Set `DEBUG = False` and configure `ALLOWED_HOSTS` in `resumekart/settings.py`.
- Configure static file serving (e.g., `collectstatic`) on your platform (Render, Railway, Heroku, etc.).
- Use a production database (e.g., Postgres) and environment variables for `SECRET_KEY` and DB credentials.

---

## 🗺️ Roadmap / Ideas

- User accounts & authentication
- Multiple resume templates and theme switcher
- PDF generation via a server-side library
- Section reordering & drag‑and‑drop
- Import/Export data (JSON)
- Basic unit tests and CI

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Commit changes: `git commit -m "feat: add my feature"`
4. Push: `git push origin feat/my-feature`
5. Open a Pull Request

---

## 📜 License

No explicit license file is currently included. Until a license is added, treat the code as **All Rights Reserved** by the repository owner. If you plan to reuse/distribute, please open an issue or contact the maintainer.

---

## 📫 Maintainer

- GitHub: [@Sam-Titan](https://github.com/Sam-Titan)

If you run into issues, please open a GitHub Issue with steps to reproduce and your environment details.
