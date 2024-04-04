# ##
# ## EPITECH PROJECT, 2024
# ## JAM_1
# ## File description:
# ## file
# ##

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

# Configuration de l'application Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_clé_secrète'  # Clé secrète pour les sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cms.db'  # Chemin de la base de données SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données SQLAlchemy
db = SQLAlchemy(app)

# Configuration de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Définition de la classe User pour représenter les utilisateurs dans la base de données
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Fonction de chargement de l'utilisateur pour Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Définition de la classe Article pour représenter les articles dans la base de données
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Page d'accueil du CMS
@app.route('/')
def index():
    articles = Article.query.all()
    return render_template('index.html', articles=articles)

# Page de création d'un nouvel article
@app.route('/create_article', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        article = Article(title=title, content=content)
        db.session.add(article)
        db.session.commit()
        flash('Article ajouté avec succès!', 'success')
        return redirect(url_for('index'))
    return render_template('create_article.html')

# Page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Connexion réussie!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'danger')
    return render_template('login.html')

# Déconnexion de l'utilisateur
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Créer les tables dans la base de données si elles n'existent pas déjà
    app.run(debug=True)
