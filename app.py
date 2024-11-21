from flask import Flask, render_template, request, redirect, url_for
from scripts import Bg_qrcode
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Folder to save uploaded files
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Check if the uploaded file is allowed (i.e., is an image)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the main page
@app.route('/')
def index():
    return render_template('bg_qr_gen.html')

# # Route for App 1
# @app.route('/qr_app')
# def app1():
#     return render_template('mainMenu/qr_menu/menu.html')

# # Route for App 2
# @app.route('/bgqr')
# def app2():
#     return render_template('/bg_qr_gen.html')

@app.route('/generate_bg', methods=['GET', 'POST'])
def generate_bg():
    qr_code_image = None

    if request.method == 'POST':
        url = request.form.get('url')
        file = request.files['logo']
        use_background = 'use_background' in request.form
        qr_color_hex = request.form.get('qr_color', '#000000')  # Get color input, default to black

        # Convert hex color to RGB tuple
        qr_color = tuple(int(qr_color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

        if url and (file and allowed_file(file.filename) if use_background else True):
            logo_path = None
            if use_background and file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                logo_path = file_path

            # Generate the QR code, pass the color and logo_path if background is used
            qr_code_image = Bg_qrcode.generate_qr_code(url, logo_path, qr_color=qr_color)

            if logo_path:
                os.remove(file_path)

    return render_template('/bg_qr_gen.html', qr_code_image=qr_code_image)

if __name__ == '__main__':
    # Create the uploads folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host="10.253.0.95",port=5001, debug=True)