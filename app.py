from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import date, timedelta
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = "gizli_bir_anahtar"

def login_required(route_function):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return route_function(*args, **kwargs)
    wrapper.__name__ = route_function.__name__
    return wrapper

@app.route('/')
@login_required
def index():
    user_id = session['user_id']
    today = str(date.today())

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT steps, water_liters, sleep_hours FROM activity_log WHERE date = ? AND user_id = ?', (today, user_id))
    today_data = cursor.fetchone()

    cursor.execute('SELECT step_goal, water_goal, sleep_goal FROM goals WHERE user_id = ?', (user_id,))
    goal_data = cursor.fetchone()
    conn.close()

    progress = None
    if today_data and goal_data:
        step_percent = min(int(today_data[0] / goal_data[0] * 100), 100)
        water_percent = min(int(today_data[1] / goal_data[1] * 100), 100)
        sleep_percent = min(int(today_data[2] / goal_data[2] * 100), 100)
        progress = {
            'step_percent': step_percent,
            'water_percent': water_percent,
            'sleep_percent': sleep_percent
        }

    return render_template('index.html', progress=progress)

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    date_input = request.form['date']
    steps = request.form['steps']
    water = request.form['water']
    sleep = request.form['sleep']
    user_id = session['user_id']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO activity_log (date, steps, water_liters, sleep_hours, user_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (date_input, steps, water, sleep, user_id))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/history')
@login_required
def history():
    user_id = session['user_id']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM activity_log WHERE user_id = ? ORDER BY date DESC', (user_id,))
    data = cursor.fetchall()
    conn.close()
    return render_template('history.html', records=data)

@app.route('/delete/<int:record_id>')
@login_required
def delete(record_id):
    user_id = session['user_id']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM activity_log WHERE id = ? AND user_id = ?', (record_id, user_id))
    conn.commit()
    conn.close()
    return redirect(url_for('history'))

@app.route('/stats')
@login_required
def stats():
    user_id = session['user_id']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    today = date.today()
    week_ago = today - timedelta(days=6)

    cursor.execute('''
        SELECT date, steps, water_liters, sleep_hours
        FROM activity_log
        WHERE date BETWEEN ? AND ? AND user_id = ?
        ORDER BY date
    ''', (str(week_ago), str(today), user_id))
    data = cursor.fetchall()
    conn.close()

    if not data:
        return render_template('stats.html', step_plot="", water_plot="", sleep_plot="")

    dates = [row[0] for row in data]
    steps = [row[1] for row in data]
    water = [row[2] for row in data]
    sleep = [row[3] for row in data]

    def generate_plot(values, label, color):
        plt.figure(figsize=(6, 4))
        plt.plot(dates, values, marker='o', color=color)
        plt.title(f'Son 7 Günlük {label}')
        plt.xlabel('Tarih')
        plt.ylabel(label)
        plt.tight_layout()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        encoded = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return encoded

    return render_template('stats.html',
                           step_plot=generate_plot(steps, 'Adım', 'blue'),
                           water_plot=generate_plot(water, 'Su (Litre)', 'orange'),
                           sleep_plot=generate_plot(sleep, 'Uyku (Saat)', 'green'))

@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    user_id = session['user_id']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        step_goal = int(request.form['step_goal'])
        water_goal = float(request.form['water_goal'])
        sleep_goal = float(request.form['sleep_goal'])

        cursor.execute('SELECT * FROM goals WHERE user_id = ?', (user_id,))
        if cursor.fetchone():
            cursor.execute('''
                UPDATE goals
                SET step_goal = ?, water_goal = ?, sleep_goal = ?
                WHERE user_id = ?
            ''', (step_goal, water_goal, sleep_goal, user_id))
        else:
            cursor.execute('''
                INSERT INTO goals (user_id, step_goal, water_goal, sleep_goal)
                VALUES (?, ?, ?, ?)
            ''', (user_id, step_goal, water_goal, sleep_goal))
        conn.commit()
        conn.close()
        return redirect('/')

    cursor.execute('SELECT step_goal, water_goal, sleep_goal FROM goals WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()

    goals = {
        'step_goal': row[0] if row else 10000,
        'water_goal': row[1] if row else 2.0,
        'sleep_goal': row[2] if row else 8.0
    }

    return render_template('goals.html', goals=goals)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session['user_id']
    username = session['username']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        new_username = request.form.get('username', username)
        session['username'] = new_username
        cursor.execute('''
            UPDATE users
            SET username = ?, first_name = ?, last_name = ?, email = ?, birth_date = ?
            WHERE id = ?
        ''', (
            new_username,
            request.form.get('first_name', ''),
            request.form.get('last_name', ''),
            request.form.get('email', ''),
            request.form.get('birth_date', ''),
            user_id
        ))
        conn.commit()

    cursor.execute('SELECT first_name, last_name, email, birth_date FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    user = {
        'first_name': row[0] or '',
        'last_name': row[1] or '',
        'email': row[2] or '',
        'birth_date': row[3] or ''
    }

    try:
        age = date.today().year - int(user['birth_date'].split('-')[0])
    except:
        age = "?"

    conn.close()
    return render_template('profile.html', username=username, user=user, age=age)

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    user_id = session['user_id']
    error = success = None

    if request.method == 'POST':
        old = request.form['old_password']
        new = request.form['new_password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE id = ?', (user_id,))
        current = cursor.fetchone()[0]

        if old != current:
            error = "❌ Eski şifre yanlış!"
        else:
            cursor.execute('UPDATE users SET password = ? WHERE id = ?', (new, user_id))
            conn.commit()
            success = "✅ Şifre değiştirildi."
        conn.close()

    return render_template('change_password.html', error=error, success=success)

@app.route('/toggle-theme')
@login_required
def toggle_theme():
    user_id = session['user_id']
    current = session.get('theme', 'light')
    new = 'dark' if current == 'light' else 'light'
    session['theme'] = new

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET theme = ? WHERE id = ?', (new, user_id))
    conn.commit()
    conn.close()
    return redirect(request.referrer or '/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            conn.close()
            return "❌ Bu kullanıcı adı alınmış. <a href='/signup'>Geri dön</a>"
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            cursor.execute('SELECT theme FROM users WHERE id = ?', (user[0],))
            theme = cursor.fetchone()
            session['theme'] = theme[0] if theme and theme[0] else 'light'
            conn.close()
            return redirect('/')
        else:
            conn.close()
            return "❌ Geçersiz kullanıcı adı veya şifre. <a href='/login'>Tekrar dene</a>"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
