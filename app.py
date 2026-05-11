
import os
import mysql.connector

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# =========================================
# UPLOAD FOLDER
# =========================================

UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# =========================================
# CORS
# =========================================

CORS(app)

# =========================================
# HOME
# =========================================

@app.route('/')
def home():

    return "NeuroVision Backend Running"

# =========================================
# REGISTER
# =========================================

@app.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    name = data['name']
    email = data['email']
    password = data['password']

    connection = mysql.connector.connect(

        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=os.getenv("MYSQLPORT")

    )

    cursor = connection.cursor()

    cursor.execute(

        "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",

        (name,email,password)

    )

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({

        "message":"Account Created Successfully"

    })

# =========================================
# LOGIN
# =========================================

@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    email = data['email']
    password = data['password']

    connection = mysql.connector.connect(

        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=os.getenv("MYSQLPORT")

    )

    cursor = connection.cursor()

    cursor.execute(

        "SELECT * FROM users WHERE email=%s AND password=%s",

        (email,password)

    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:

        return jsonify({

            "message":"Login Successful"

        })

    else:

        return jsonify({

            "message":"Invalid Email or Password"

        }),401

# =========================================
# MRI IMAGE UPLOAD
# =========================================

@app.route('/upload', methods=['POST'])
def upload_image():

    if 'image' not in request.files:

        return jsonify({

            "message":"No Image Uploaded"

        }),400

    image = request.files['image']

    if image.filename == '':

        return jsonify({

            "message":"No Selected File"

        }),400

    filepath = os.path.join(

        app.config['UPLOAD_FOLDER'],
        image.filename

    )

    image.save(filepath)

    return jsonify({

        "message":"MRI Uploaded Successfully",
        "filename":image.filename

    })

# =========================================
# RUN APP
# =========================================

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=10000)