from flask import Flask, render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from database import filter_email, insert_tables2, insert_product, get_product
import os
import boto3

from database import insert_user, get_product, find_user_email
from uploadAWS import aws_upload_file

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('loginPage.html')

    else: 
        email = request.form.get('inputEmail')
        password = request.form.get('inputPassword')

        user_result = find_user_email(email)

        if not user_result:
            flash('Email or Password incorrect!')
            return redirect(url_for('login'))

        elif check_password_hash(user_result[0][2], password):
            session['user'] = email
            return redirect(url_for('home'))

        else:
            flash('StudentID or Password incorrect!')
            return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('registerPage.html')

    else: 
        email = request.form.get('inputEmail')
        password = request.form.get('inputPassword')
        retype = request.form.get('inputRetype')
        name = request.form.get('inputName')
        job = request.form.get('jobtitle')
        phash = None

        if password == retype:
            phash = generate_password_hash(password)

            # Check student used or not
            user_result = find_user_email(email)

            if user_result:
                flash("Student ID have been register! Please SignIn")
                return redirect(url_for('register'))

            else: 
                insert_user(email, phash, name)
                session['user'] = email
                return redirect(url_for('home'))

        else:
            flash("Password not same! Please try again.")
            return redirect(url_for('register'))

@app.route("/market", methods=['GET', 'POST'])
def market():
    product_lists = get_product()

    return render_template('marketApp.html', product_lists = product_lists)
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            UPLOAD_FOLDER = 'path/upload'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            save_file =  os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            aws_upload_file(save_file, object_name=file_path)
            # return redirect(url_for('download_file', name=filename))
            return f"{filename}"
    return render_template('fileUpload.html')

@app.route('/create', methods=['GET' ,'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        discription = request.form.get('discription')
        price = request.form.get('price')
        category = request.form.get('category')

        user = session['user']
        user_product = get_product()

        try:
            product_id = user_product[-1][0] + 1
        except:
            product_id = 1

        if 'file' not in request.files:
            flash('No file part')
            # return redirect(request.url)
            insert_product(user, category, title, discription, price, 'None')
            return 'No file part'

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            # return redirect(request.url)
            insert_product(user, category, title, discription, price, 'None')
            return 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            os.mkdir(f'path/image/{user}-{str(product_id)}')

            UPLOAD_FOLDER = f'path/image/{user}-{str(product_id)}'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            save_file =  os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            insert_product(user, category, title, discription, price, filename)
            aws_upload_file(save_file, object_name=file_path)
            return redirect(url_for('market'))

    return render_template('createProduct.html')

@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html", methods = ["POST", "GET"])


@app.route("/Howitworks")
def Howitworks () :
    return render_template("howitworks.html", method = 'GET')


@app.route("/OurStory")
def ourstory () : 
    return render_template("ourstory.html", method = "GET")

@app.route("/contactus", methods = ["GET", "POST"])
def contactus() : 
    if request.method == "GET":
        return render_template("ContactUs.html")

    else :
        email = request.form.get("email")
        LastName = request.form.get("LastName")
        FirstName = request.form.get("FirstName")
        if not filter_email(email):
            insert_tables2(FirstName, LastName, email)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug = True)  
