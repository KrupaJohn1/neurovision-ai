import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL

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
# MYSQL CONFIG
# =========================================

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'neurovision'

mysql = MySQL(app)

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

    cursor = mysql.connection.cursor()

    cursor.execute(

        "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",

        (name,email,password)

    )

    mysql.connection.commit()

    cursor.close()

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

    cursor = mysql.connection.cursor()

    cursor.execute(

        "SELECT * FROM users WHERE email=%s AND password=%s",

        (email,password)

    )

    user = cursor.fetchone()

    cursor.close()

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

    # CHECK IMAGE

    if 'image' not in request.files:

        return jsonify({

            "message":"No Image Uploaded"

        }),400

    image = request.files['image']

    # CHECK EMPTY FILE

    if image.filename == '':

        return jsonify({

            "message":"No Selected File"

        }),400

    # SAVE IMAGE

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

    app.run(debug=True)