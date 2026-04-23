# 🛡️ Policy Consultant — Backend API

Production-ready FastAPI + PostgreSQL backend for an Insurance Consultant platform.

---

## 📁 Project Structure

```
Policy_Consultant_backend/
├── main.py                          # Render entry point
├── requirements.txt                 # Python dependencies
├── render.yaml                      # Render deploy config
├── .env                             # Secrets (gitignored)
├── .env.example                     # Template to commit
├── .gitignore
├── Policy_Consultant_API.postman_collection.json
├── Policy_Consultant.postman_environment.json
└── app/
    ├── __init__.py
    ├── main.py                      # FastAPI app + lifespan
    ├── config.py                    # Pydantic settings from .env
    ├── database.py                  # SQLAlchemy engine + get_db()
    ├── models.py                    # ORM: User, Contact
    ├── schemas.py                   # Pydantic schemas (request/response)
    ├── auth.py                      # JWT + bcrypt + dependencies
    └── routes/
        ├── __init__.py
        ├── auth_routes.py           # /register  /login  /admin/login
        ├── contact_routes.py        # /contact
        └── admin_routes.py          # /admin/users /admin/contacts + DELETE
```

---

## ⚙️ Local Setup

### 1. Configure Environment
```bash
# Open .env and set your real values:
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/policy_consultant
SECRET_KEY=your-long-random-secret-key
ADMIN_EMAIL=admin@policyconsultant.com
ADMIN_PASSWORD=Admin@12345
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 2. Create the Database
Open pgAdmin or psql and run:
```sql
CREATE DATABASE policy_consultant;
```

### 3. Activate Virtual Environment & Run
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Start the server
uvicorn main:app --host 0.0.0.0 --port 10000 --reload
```

### 4. Verify
- **API Root:** http://localhost:10000/
- **Swagger UI:** http://localhost:10000/docs
- **ReDoc:** http://localhost:10000/redoc

> Tables are created automatically on first startup via SQLAlchemy.

---

## 🔑 API Endpoints

### Auth (Public)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/register` | Register new user |
| `POST` | `/login` | User login → JWT |
| `POST` | `/admin/login` | Admin login → JWT |

### Contact (Public)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/contact` | Submit insurance inquiry |

### Admin (🔒 JWT Required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/admin/users` | List users (paginated + search) |
| `GET` | `/admin/user/{id}` | Get single user |
| `DELETE` | `/admin/user/{id}` | Delete user |
| `GET` | `/admin/contacts` | List contacts (paginated + filter) |
| `GET` | `/admin/contact/{id}` | Get single contact |
| `DELETE` | `/admin/contact/{id}` | Delete contact |

### Query Params
| Param | Endpoints | Description |
|-------|-----------|-------------|
| `page` | users, contacts | Page number (default: 1) |
| `page_size` | users, contacts | Items per page (default: 10, max: 100) |
| `search` | users, contacts | Filter by name or email |
| `insurance_type` | contacts | Filter: health, life, motor, travel, home, business, other |

---

## 🧪 Postman Testing

1. Open Postman
2. **Import Collection:** `Policy_Consultant_API.postman_collection.json`
3. **Import Environment:** `Policy_Consultant.postman_environment.json`
4. Select **"Policy Consultant - Local"** environment
5. Run **Admin Login** — token is auto-saved ✅
6. All admin routes will use the token automatically

---

## 🔐 Admin Credentials

Default hardcoded admin (set in `.env`):
```
Email:    admin@policyconsultant.com
Password: Admin@12345
```

---

## 🚀 Deploy to Render

1. Push to GitHub
2. Create new **Web Service** on [render.com](https://render.com)
3. Connect your repo
4. Render auto-detects `render.yaml`
5. Set environment variables in the Render dashboard:
   - `DATABASE_URL` → Your Render PostgreSQL URL
   - `SECRET_KEY` → A strong random string
   - `ADMIN_EMAIL` / `ADMIN_PASSWORD`
   - `ALLOWED_ORIGINS` → Your frontend URL

**Start Command:**
```
uvicorn main:app --host 0.0.0.0 --port 10000
```

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.111.0 | Web framework |
| Uvicorn | 0.29.0 | ASGI server |
| SQLAlchemy | 2.0.30 | ORM |
| psycopg2 | 2.9.9 | PostgreSQL driver |
| Pydantic v2 | 2.7.1 | Validation |
| python-jose | 3.3.0 | JWT |
| passlib[bcrypt] | 1.7.4 | Password hashing |
| python-dotenv | 1.0.1 | Env config |

---

## 🔒 Security Features

- ✅ Passwords hashed with **bcrypt**
- ✅ **JWT** tokens with configurable expiry
- ✅ Role-based access: `user` / `admin`
- ✅ Hardcoded admin via `.env` (no DB dependency)
- ✅ Input validation on all endpoints (Pydantic v2)
- ✅ CORS configured per environment
- ✅ Global exception handler (no stack traces exposed)
- ✅ `.env` secrets gitignored
