# 🚀 Cyberpunk Portfolio — Ishga Tushirish Qo'llanmasi

## Loyiha Tuzilishi

```
portfolio/
├── app.py                    # Asosiy Flask ilovasi
├── requirements.txt          # Python kutubxonalari
├── README.md                 # Shu fayl
├── instance/
│   └── portfolio.db          # SQLite database (avtomatik yaratiladi)
├── static/
│   ├── css/
│   │   ├── style.css         # Asosiy portfolio CSS
│   │   └── admin.css         # Admin panel CSS
│   ├── js/
│   │   ├── main.js           # Asosiy JavaScript
│   │   └── admin.js          # Admin JavaScript
│   └── uploads/              # Yuklangan rasmlar (avtomatik)
└── templates/
    ├── index.html            # Asosiy portfolio sahifasi
    └── admin/
        ├── base.html         # Admin layout
        ├── login.html        # Login sahifasi
        ├── dashboard.html    # Bosh sahifa
        ├── projects.html     # Loyihalar ro'yxati
        ├── project_form.html # Loyiha qo'shish/tahrirlash
        ├── skills.html       # Ko'nikmalar
        ├── about.html        # Men haqimda
        └── messages.html     # Xabarlar
```

## ⚙️ O'rnatish va Ishga Tushirish

### 1. Python Virtual Environment yaratish
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. Ishga tushirish
```bash
python app.py
```

### 4. Brauzerda ochish
```
Portfolio:     http://localhost:5000
Admin panel:   http://localhost:5000/admin/login
```

## 🔐 Admin Login Ma'lumotlari

| Ma'lumot | Qiymat |
|----------|--------|
| Username | `admin` |
| Password | `admin123` |

> ⚠️ **MUHIM:** Production ga chiqishdan oldin `app.py` da `SECRET_KEY` va admin parolini o'zgartiring!

## 🎨 Sozlash

### Admin Parolini O'zgartirish
`app.py` faylida `init_db()` funksiyasida:
```python
admin.set_password('yangi_parolingiz')
```

### Secret Key
```python
app.config['SECRET_KEY'] = 'o'zingizning-maxfiy-kalitingiz'
```

## 📱 Funksiyalar

- ✅ Dark Cyberpunk dizayn
- ✅ Matrix rain animatsiya
- ✅ Typewriter effekt
- ✅ Scroll reveal animatsiyalar
- ✅ Neon glow effektlar
- ✅ Glassmorphism UI
- ✅ Responsive dizayn (telefon/planshet/kompyuter)
- ✅ Admin panel (login bilan himoyalangan)
- ✅ Loyihalar CRUD
- ✅ Ko'nikmalar CRUD (inline tahrirlash)
- ✅ About tahrirlash
- ✅ Rasm yuklash
- ✅ Kontakt forma (AJAX)
- ✅ Xabarlarni boshqarish
