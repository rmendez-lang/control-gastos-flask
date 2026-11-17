from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
import sqlite3, os, csv, io
from datetime import date
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'gastos.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cambia-esta-clave-en-produccion')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )''')
        user = db.execute('SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()
        if not user:
            db.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                       ('admin', generate_password_hash('123')))


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped


@app.route('/', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        with get_db() as db:
            user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        flash('Usuario o contraseña incorrectos.', 'error')
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    today = date.today().isoformat()
    month = date.today().strftime('%Y-%m')
    with get_db() as db:
        expenses = db.execute('SELECT * FROM expenses ORDER BY expense_date DESC, id DESC LIMIT 8').fetchall()
        total = db.execute('SELECT COALESCE(SUM(amount),0) FROM expenses').fetchone()[0]
        today_total = db.execute('SELECT COALESCE(SUM(amount),0) FROM expenses WHERE expense_date = ?', (today,)).fetchone()[0]
        month_total = db.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE substr(expense_date,1,7) = ?", (month,)).fetchone()[0]
        count = db.execute('SELECT COUNT(*) FROM expenses').fetchone()[0]
    return render_template('dashboard.html', expenses=expenses, total=total, today_total=today_total,
                           month_total=month_total, count=count, today=today)


@app.route('/gastos/nuevo', methods=['POST'])
@login_required
def add_expense():
    expense_date = request.form.get('expense_date', '')
    description = request.form.get('description', '').strip()
    amount_raw = request.form.get('amount', '').strip()
    try:
        amount = float(amount_raw)
        if amount <= 0: raise ValueError
        date.fromisoformat(expense_date)
        if not description: raise ValueError
    except (ValueError, TypeError):
        flash('Verifica la fecha, descripción y monto. El monto debe ser mayor que cero.', 'error')
        return redirect(url_for('dashboard'))
    with get_db() as db:
        db.execute('INSERT INTO expenses (expense_date, description, amount) VALUES (?, ?, ?)',
                   (expense_date, description, amount))
    flash('Gasto registrado correctamente.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/gastos/eliminar/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    with get_db() as db:
        db.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    flash('Registro eliminado.', 'success')
    return redirect(request.referrer or url_for('dashboard'))


@app.route('/reporte')
@login_required
def report():
    start = request.args.get('desde', '').strip()
    end = request.args.get('hasta', '').strip()
    query = 'SELECT * FROM expenses WHERE 1=1'
    params = []
    if start:
        query += ' AND expense_date >= ?'; params.append(start)
    if end:
        query += ' AND expense_date <= ?'; params.append(end)
    query += ' ORDER BY expense_date DESC, id DESC'
    with get_db() as db:
        expenses = db.execute(query, params).fetchall()
    total = sum(row['amount'] for row in expenses)
    return render_template('report.html', expenses=expenses, total=total, start=start, end=end)


@app.route('/reporte/csv')
@login_required
def report_csv():
    start = request.args.get('desde', '').strip(); end = request.args.get('hasta', '').strip()
    query = 'SELECT expense_date, description, amount FROM expenses WHERE 1=1'; params = []
    if start: query += ' AND expense_date >= ?'; params.append(start)
    if end: query += ' AND expense_date <= ?'; params.append(end)
    query += ' ORDER BY expense_date DESC'
    with get_db() as db: rows = db.execute(query, params).fetchall()
    output = io.StringIO(); writer = csv.writer(output)
    writer.writerow(['Fecha', 'Descripción', 'Monto (S/)'])
    for row in rows: writer.writerow([row['expense_date'], row['description'], f"{row['amount']:.2f}"])
    return Response('\ufeff' + output.getvalue(), mimetype='text/csv; charset=utf-8',
                    headers={'Content-Disposition': 'attachment; filename=reporte_gastos.csv'})


@app.route('/salir')
def logout():
    session.clear()
    return redirect(url_for('login'))


init_db()
if __name__ == '__main__':
    app.run(debug=True)
