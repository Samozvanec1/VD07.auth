from app import app, db, bcrypt
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.forms import LoginForm, RegistrationForm, ChangePasswordForm, ChangeEmailForm, ChangeUsernameForm
# routes.py отвучает за все переходы на сайт и взаимодействие с базой данных
# использование html файлов для передачи пользователю(клиенту) при входе на сайт

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html') #передает html файл с данными.
    # render_template - функция Flask для отрисовки html файла

@app.route('/register', methods=['GET', 'POST']) #get - получение данных, post - отправка данных
def register():
    if current_user.is_authenticated: #если текущий пользователь уже залогинен
        return redirect(url_for('home')) #перенаправление на домашнюю страницу return завершает выполнение функции (программы)
    form = RegistrationForm() #создание экземпляра формы для регистрации
    if form.validate_on_submit(): #если данные валидны программа сохраняет изменения в базе данных
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #шифрование пароля при регистрации
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) #создание экземпляра пользователя
        db.session.add(user)     #добавление пользователя в базу данных
        db.session.commit() #commits - сохраняет изменения в базе данных
        flash('Ваш аккаунт был создан.', 'success') #сообщение об успешной регистрации
        # flash - показывает сообщение
        return redirect(url_for('login')) #перенаправление на страницу входа
    return render_template('registration.html', form=form) #передача формы в html файл
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('При входе произошла ошибка. Пожалуйста, попробуйте еще раз.', 'danger')
            #сообщение об ошибке при входе
    return render_template('login.html', form=form)

@app.route('/logout')
def logout(): #функция выхода из аккаунта
    logout_user()
    return redirect(url_for('home')) # перенаправление на домашнюю страницу

@app.route('/account')
@login_required #функция для защиты от неавторизованных пользователей
def account(): #функция аккаунта
    return render_template('account.html') #передача html файла
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit(): #проверка пароля
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit() #commits - сохраняет изменения в базе данных
            flash('Ваш пароль был изменен.', 'success')
            return redirect(url_for('account'))
        else:
            flash('Неправильный пароль. Пожалуйста, попробуйте еще раз.', 'danger')
    return render_template('change_password.html', form=form)
@app.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    form = ChangeEmailForm() # программа запрашивает пароль для изменения email
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if bcrypt.check_password_hash(hashed_password, form.password.data):
            current_user.email = form.email.data
            db.session.commit() #commits - сохраняет изменения в базе данных
            flash('Ваш email был изменен.', 'success')
            return redirect(url_for('account'))
        else:
            flash('Неправильный пароль. Пожалуйста, попробуйте еще раз.', 'danger')
    return render_template('change_email.html', form=form)

@app.route('/change_username', methods=['GET', 'POST'])
@login_required
def change_username():
    form = ChangeUsernameForm() # программа запрашивает пароль для изменения username
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.password.data):
            current_user.username = form.username.data
            db.session.commit() #commits - сохраняет изменения в базе данных
            flash('Ваш username был изменен.', 'success')
            return redirect(url_for('account'))
        else:
            flash('Неправильный пароль. Пожалуйста, попробуйте еще раз.', 'danger')
    return render_template('change_username.html', form=form)