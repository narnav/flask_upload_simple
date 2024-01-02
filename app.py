from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
db = SQLAlchemy(app)

class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))

@app.route('/')
def index():
    images = ImageData.query.all()
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file:
        filename = file.filename
        file_extension = os.path.splitext(filename)[1]
        # Generate a unique filename using timestamp
        unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}{file_extension}"
        file_path = os.path.join('static/uploads', unique_filename)
        file.save(file_path)

        # Process the image (e.g., resize, convert format)
        img = Image.open(file_path)
        img.thumbnail((300, 300))  # Resize image if needed
        img.save(file_path)

        new_image = ImageData(filename=unique_filename)
        db.session.add(new_image)
        db.session.commit()

    return redirect(url_for('index'))
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
