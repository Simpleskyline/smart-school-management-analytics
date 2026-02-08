🎓 Smart School Management & Analytics System

Complete school management system with analytics dashboard.

## Features
- Student Management
- Teacher Management
- Class Management
- Attendance Tracking
- Fee Management
- Analytics Dashboard

## Tech Stack
- **Backend:** Python Flask
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MySQL
- **Analytics:** Pandas, Chart.js

## Setup

1. **Database:**
```bash
mysql -u root -p < database/school.sql
```

2. **Backend:**
```bash
cd backend
pip install -r requirements.txt
```

3. **Run:**
```bash
python run.py
```

4. **Access:**
- Frontend: Open `frontend/login.html`
- API: http://localhost:5000

## Default Login
- Username: `admin`
- Password: `admin123`

## License
MIT
