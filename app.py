from flask import Flask, request, jsonify, render_template_string
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="your_db_user",
    password="your_db_password",
    database="membership_db"
)
cursor = db.cursor()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = generate_password_hash(data['password'], method='sha256')
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Register - Mongol Bartha</title>
            <link rel="stylesheet" href="styles.css">
        </head>
        <body>
            <h1>Register for Free</h1>
            <form method="post">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Register</button>
            </form>
        </body>
        </html>
    ''')

@app.route('/premium-register', methods=['GET', 'POST'])
def premium_register():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = generate_password_hash(data['password'], method='sha256')
        cursor.execute("INSERT INTO users (username, password, membership) VALUES (%s, %s, 'premium')", (username, password))
        db.commit()
        return jsonify({'message': 'Premium user registered successfully'}), 201
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Premium Register - Mongol Bartha</title>
            <link rel="stylesheet" href="styles.css">
        </head>
        <body>
            <h1>Subscribe to Premium (500 Taka/month)</h1>
            <form method="post">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Subscribe</button>
            </form>
        </body>
        </html>
    ''')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user and check_password_hash(user[0], password):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/upgrade', methods=['POST'])
def upgrade():
    data = request.get_json()
    username = data['username']
    password = data['password']

    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user and check_password_hash(user[0], password):
        cursor.execute("UPDATE users SET membership = 'premium' WHERE username = %s", (username,))
        db.commit()
        return jsonify({'message': 'Upgraded to premium'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/admin/users', methods=['GET'])
def admin_users():
    cursor.execute("SELECT id, username, membership FROM users")
    users = cursor.fetchall()
    user_list = [{"id": user[0], "username": user[1], "membership": user[2]} for user in users]
    return jsonify(user_list), 200

if __name__ == '__main__':
    app.run(debug=True)
