from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS
import bcrypt

app = Flask(__name__)
CORS(app)

def create_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='sistema',
    )

@app.route('/saveuser', methods=['POST'])
def add_new_user():
    try:
        connection = create_connection()
        cursor = connection.cursor()

        user = request.get_json()
        user_password = user['user_password']

        # Encrypt the password using bcrypt
        hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())

        # Replace the original password with the encrypted password
        user['user_password'] = hashed_password.decode('utf-8')

        query = "INSERT INTO `sys_users` (`user_id`, `user_name`, `user_cpf`, `user_email`, `user_password`) VALUES (NULL, %s, %s, %s, %s)"
        values = (user['user_name'], user['user_cpf'], user['user_email'], user['user_password'])

        cursor.execute(query, values)
        connection.commit()
        cursor.close()

        return jsonify(user)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        connection.close()

@app.route('/login', methods=['POST'])
def login_user():
    try:
        connection = create_connection()
        cursor = connection.cursor()

        user = request.get_json()
        email = user['user_email']
        encrypted_password_frontend = user['user_password']

        # Retrieve the salted hash from the database for the user with the provided email
        query = "SELECT user_password FROM sys_users WHERE user_email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result is not None:
            # Retrieve the stored salted hash from the database
            salted_hash_db = result[0]

            # Check if the encrypted password from the frontend matches the salted hash from the database
            if bcrypt.checkpw(encrypted_password_frontend.encode('utf-8'), salted_hash_db.encode('utf-8')):
                return jsonify({'message': 'Login successful'}), 200
            else:
                return jsonify({'message': 'Incorrect password'}), 401
        else:
            return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:    
        connection.close()


if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
