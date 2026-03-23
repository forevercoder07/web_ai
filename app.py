"""
Portfolio Web Application
Flask + SQLite + SQLAlchemy asosida qurilgan portfolio sayt
"""

import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from functools import wraps

# ── App sozlamalari ────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-super-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

db = SQLAlchemy(app)

# ── Database modellari ─────────────────────────────────────────────────────────

class Admin(db.Model):
    """Admin foydalanuvchi modeli"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Project(db.Model):
    """Loyihalar modeli"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(300), default='default_project.png')
    link = db.Column(db.String(500), nullable=True)
    github_link = db.Column(db.String(500), nullable=True)
    tech_stack = db.Column(db.String(500), nullable=True)  # "Python, Flask, SQLite"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_tech_list(self):
        if self.tech_stack:
            return [t.strip() for t in self.tech_stack.split(',')]
        return []


class Skill(db.Model):
    """Ko'nikmalar modeli"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False, default=50)  # 0-100 foizda
    category = db.Column(db.String(100), default='General')  # "Frontend", "Backend", "Tools"
    icon = db.Column(db.String(100), nullable=True)  # icon nomi


class About(db.Model):
    """Men haqimda modeli"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(200), default='Your Name')
    title = db.Column(db.String(200), default='Full Stack Developer')
    location = db.Column(db.String(200), default='Tashkent, Uzbekistan')
    email = db.Column(db.String(200), default='your@email.com')
    github = db.Column(db.String(300), nullable=True)
    linkedin = db.Column(db.String(300), nullable=True)
    telegram = db.Column(db.String(300), nullable=True)
    avatar = db.Column(db.String(300), default='default_avatar.png')


class Contact(db.Model):
    """Kontakt xabarlari modeli"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)


# ── Helper funksiyalar ─────────────────────────────────────────────────────────

def allowed_file(filename):
    """Fayl kengaytmasi ruxsat etilganmi?"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file):
    """Fayl saqlash va nomini qaytarish"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Noyob nom berish
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{int(datetime.utcnow().timestamp())}{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)
        return filename
    return None


def login_required(f):
    """Admin login tekshiruvi decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Iltimos avval tizimga kiring', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


def init_db():
    """Databaseni ishga tushirish va boshlang'ich ma'lumotlarni qo'shish"""
    with app.app_context():
        db.create_all()

        # Admin mavjudligini tekshirish
        if not Admin.query.first():
            admin = Admin(username='admin')
            admin.set_password('admin123')  # Ishga tushirgandan keyin o'zgartiring!
            db.session.add(admin)

        # About ma'lumoti mavjudligini tekshirish
        if not About.query.first():
            about = About(
                name='Your Name',
                title='Full Stack Developer',
                location='Tashkent, Uzbekistan',
                email='your@email.com',
                content='Men haqimda qisqacha ma\'lumot. Bu yerga o\'z biografiyangizni yozing.'
            )
            db.session.add(about)

        # Namuna ko'nikmalar
        if not Skill.query.first():
            skills_data = [
                ('Python', 90, 'Backend'), ('Flask', 85, 'Backend'),
                ('JavaScript', 80, 'Frontend'), ('HTML/CSS', 90, 'Frontend'),
                ('SQLite', 75, 'Database'), ('Git', 85, 'Tools'),
                ('React', 70, 'Frontend'), ('Docker', 60, 'DevOps'),
            ]
            for name, level, category in skills_data:
                db.session.add(Skill(name=name, level=level, category=category))

        # Namuna loyiha
        if not Project.query.first():
            project = Project(
                title='Portfolio Website',
                description='Flask asosida qurilgan shaxsiy portfolio sayt. Dark cyberpunk dizayn, admin panel va barcha zamonaviy funksiyalar bilan.',
                link='#',
                github_link='https://github.com/yourusername/portfolio',
                tech_stack='Python, Flask, SQLite, SQLAlchemy, JavaScript'
            )
            db.session.add(project)

        db.session.commit()
        print("✅ Database initialized successfully!")


# ── Asosiy sahifalar ───────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Bosh sahifa"""
    projects = Project.query.order_by(Project.created_at.desc()).limit(6).all()
    skills = Skill.query.all()
    about = About.query.first()

    # Ko'nikmalarni kategoriya bo'yicha guruhlash
    skill_categories = {}
    for skill in skills:
        if skill.category not in skill_categories:
            skill_categories[skill.category] = []
        skill_categories[skill.category].append(skill)

    return render_template('index.html',
                           projects=projects,
                           skill_categories=skill_categories,
                           about=about)


@app.route('/projects')
def projects():
    """Barcha loyihalar sahifasi"""
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('projects.html', projects=all_projects)


@app.route('/contact', methods=['POST'])
def contact():
    """Kontakt formasini qabul qilish"""
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()

    if not all([name, email, message]):
        return jsonify({'success': False, 'message': 'Barcha maydonlarni to\'ldiring'}), 400

    # Email validatsiyasi
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({'success': False, 'message': 'Email manzil noto\'g\'ri'}), 400

    new_contact = Contact(name=name, email=email, message=message)
    db.session.add(new_contact)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Xabaringiz muvaffaqiyatli yuborildi!'})


# ── Admin panel ────────────────────────────────────────────────────────────────

@app.route('/admin')
@login_required
def admin_dashboard():
    """Admin bosh sahifasi"""
    stats = {
        'projects': Project.query.count(),
        'skills': Skill.query.count(),
        'messages': Contact.query.count(),
        'unread': Contact.query.filter_by(is_read=False).count()
    }
    recent_messages = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats, recent_messages=recent_messages)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login sahifasi"""
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Tizimga muvaffaqiyatli kirdingiz!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Username yoki parol noto\'g\'ri!', 'error')

    return render_template('admin/login.html')

@app.route('/admin/change-password', methods=['GET', 'POST'])
@login_required
def admin_change_password():
    if request.method == 'POST':
        current = request.form.get('current_password', '')
        new_pass = request.form.get('new_password', '')
        confirm  = request.form.get('confirm_password', '')

        admin = Admin.query.filter_by(username=session['admin_username']).first()

        if not admin.check_password(current):
            flash('Joriy parol noto\'g\'ri!', 'error')
        elif new_pass != confirm:
            flash('Yangi parollar mos kelmadi!', 'error')
        elif len(new_pass) < 8:
            flash('Parol kamida 8 ta belgidan iborat bo\'lsin!', 'error')
        else:
            admin.set_password(new_pass)
            db.session.commit()
            flash('Parol muvaffaqiyatli o\'zgartirildi!', 'success')
            return redirect(url_for('admin_dashboard'))

    return render_template('admin/change_password.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin chiqish"""
    session.clear()
    flash('Tizimdan chiqdingiz', 'info')
    return redirect(url_for('admin_login'))


# ── Admin: Projects CRUD ───────────────────────────────────────────────────────

@app.route('/admin/projects')
@login_required
def admin_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=projects)


@app.route('/admin/projects/add', methods=['GET', 'POST'])
@login_required
def admin_add_project():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        link = request.form.get('link', '').strip()
        github_link = request.form.get('github_link', '').strip()
        tech_stack = request.form.get('tech_stack', '').strip()

        if not title or not description:
            flash('Sarlavha va tavsif majburiy!', 'error')
            return redirect(request.url)

        image_name = 'default_project.png'
        if 'image' in request.files:
            saved = save_file(request.files['image'])
            if saved:
                image_name = saved

        project = Project(title=title, description=description,
                          image=image_name, link=link,
                          github_link=github_link, tech_stack=tech_stack)
        db.session.add(project)
        db.session.commit()
        flash('Loyiha muvaffaqiyatli qo\'shildi!', 'success')
        return redirect(url_for('admin_projects'))

    return render_template('admin/project_form.html', project=None, action='Qo\'shish')


@app.route('/admin/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_project(id):
    project = Project.query.get_or_404(id)

    if request.method == 'POST':
        project.title = request.form.get('title', '').strip()
        project.description = request.form.get('description', '').strip()
        project.link = request.form.get('link', '').strip()
        project.github_link = request.form.get('github_link', '').strip()
        project.tech_stack = request.form.get('tech_stack', '').strip()

        if 'image' in request.files and request.files['image'].filename:
            saved = save_file(request.files['image'])
            if saved:
                project.image = saved

        db.session.commit()
        flash('Loyiha yangilandi!', 'success')
        return redirect(url_for('admin_projects'))

    return render_template('admin/project_form.html', project=project, action='Tahrirlash')


@app.route('/admin/projects/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Loyiha o\'chirildi!', 'success')
    return redirect(url_for('admin_projects'))


# ── Admin: Skills CRUD ─────────────────────────────────────────────────────────

@app.route('/admin/skills', methods=['GET', 'POST'])
@login_required
def admin_skills():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        level = int(request.form.get('level', 50))
        category = request.form.get('category', 'General').strip()

        if name:
            skill = Skill(name=name, level=level, category=category)
            db.session.add(skill)
            db.session.commit()
            flash('Ko\'nikma qo\'shildi!', 'success')

    skills = Skill.query.all()
    return render_template('admin/skills.html', skills=skills)


@app.route('/admin/skills/edit/<int:id>', methods=['POST'])
@login_required
def admin_edit_skill(id):
    skill = Skill.query.get_or_404(id)
    skill.name = request.form.get('name', skill.name).strip()
    skill.level = int(request.form.get('level', skill.level))
    skill.category = request.form.get('category', skill.category).strip()
    db.session.commit()
    return jsonify({'success': True})


@app.route('/admin/skills/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Ko\'nikma o\'chirildi!', 'success')
    return redirect(url_for('admin_skills'))


# ── Admin: About ───────────────────────────────────────────────────────────────

@app.route('/admin/about', methods=['GET', 'POST'])
@login_required
def admin_about():
    about = About.query.first()
    if not about:
        about = About(name='Your Name', title='Developer', content='...')
        db.session.add(about)
        db.session.commit()

    if request.method == 'POST':
        about.name = request.form.get('name', '').strip()
        about.title = request.form.get('title', '').strip()
        about.location = request.form.get('location', '').strip()
        about.email = request.form.get('email', '').strip()
        about.content = request.form.get('content', '').strip()
        about.github = request.form.get('github', '').strip()
        about.linkedin = request.form.get('linkedin', '').strip()
        about.telegram = request.form.get('telegram', '').strip()

        if 'avatar' in request.files and request.files['avatar'].filename:
            saved = save_file(request.files['avatar'])
            if saved:
                about.avatar = saved

        db.session.commit()
        flash('Ma\'lumotlar yangilandi!', 'success')
        return redirect(url_for('admin_about'))

    return render_template('admin/about.html', about=about)


# ── Admin: Messages ────────────────────────────────────────────────────────────

@app.route('/admin/messages')
@login_required
def admin_messages():
    messages = Contact.query.order_by(Contact.created_at.desc()).all()
    # Barcha xabarlarni o'qilgan deb belgilash
    Contact.query.filter_by(is_read=False).update({'is_read': True})
    db.session.commit()
    return render_template('admin/messages.html', messages=messages)


@app.route('/admin/messages/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_message(id):
    msg = Contact.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash('Xabar o\'chirildi!', 'success')
    return redirect(url_for('admin_messages'))


# ── Ishga tushirish ────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
