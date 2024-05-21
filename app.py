from flask import Flask, render_template, request, redirect, url_for, g, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connessione al database
DATABASE = 'database.db'
DATABASE_LIST = 'database_list.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def get_db_list():
    db = getattr(g, '_database_list', None)
    if db is None:
        db = g._database_list = sqlite3.connect(DATABASE_LIST)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

    db_list = getattr(g, '_database_list', None)
    if db_list is not None:
        db_list.close()

# Creazione delle tabelle nel database
def create_tables():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT
            )
        ''')
        db.commit()
        cursor.close()

        db_list = get_db_list()
        cursor_list = db_list.cursor()
        cursor_list.execute('''
            CREATE TABLE IF NOT EXISTS lista (
                id INTEGER PRIMARY KEY,
                item TEXT
            )
        ''')
        db_list.commit()
        cursor_list.close()

# Pagina di login
@app.route('/')
def login():
    return render_template('login.html')

# Pagina di registrazione
@app.route('/register')
def register():
    return render_template('register.html')

# Registrazione dell'utente nel database
@app.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    db.commit()
    cursor.close()
    return redirect(url_for('login'))

# Verifica dell'utente nel database e redirect alla dashboard
@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    cursor.close()
    if user:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return "Credenziali non valide. Riprova."

# Pagina dashboard
@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if username:
        if username == 'Joy':
            editable = True
        else:
            editable = False
        db_list = get_db_list()
        cursor_list = db_list.cursor()
        cursor_list.execute('SELECT * FROM lista')
        items = cursor_list.fetchall()
        cursor_list.close()
        return render_template('dashboard.html', items=items, editable=editable)
    else:
        return redirect(url_for('login'))

# Modifica della lista solo per l'utente "Joy"
@app.route('/update_list', methods=['POST'])
def update_list():
    username = session.get('username')
    if username == 'Joy':
        new_item = request.form['new_item']
        db_list = get_db_list()
        cursor_list = db_list.cursor()
        cursor_list.execute('INSERT INTO lista (item) VALUES (?)', (new_item,))
        db_list.commit()
        cursor_list.close()
    return redirect(url_for('dashboard'))

# Rimozione dalla lista solo per l'utente "Joy"
@app.route('/remove_item/<int:item_id>')
def remove_item(item_id):
    username = session.get('username')
    if username == 'Joy':
        db_list = get_db_list()
        cursor_list = db_list.cursor()
        cursor_list.execute('DELETE FROM lista WHERE id = ?', (item_id,))
        db_list.commit()
        cursor_list.close()
    return redirect(url_for('dashboard'))

# Pagina di conferma cancellazione dell'account
@app.route('/confirm_delete_account', methods=['GET'])
def confirm_delete_account():
    return render_template('confirm_delete_account.html')

# Funzione per eliminare l'account
@app.route('/confirm_delete_account', methods=['POST'])
def confirm_delete_account_post():
    if 'username' in session:
        username = session['username']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        db.commit()
        cursor.close()
        session.pop('username')
    return redirect(url_for('login'))

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
