from flask import Flask, request, redirect, url_for, render_template, send_file
import os
import time
from main import main
from result import save_to_csv

app = Flask(__name__)

# Ensure the directory for uploaded files exists
UPLOAD_FOLDER = 'resumes'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return redirect(request.url)
    
    files = request.files.getlist('files[]')
    for file in files:
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    # Redirect to the result page
    return redirect(url_for('result'))

@app.route('/result', methods=['GET', 'POST'])
def result():
    # Simulate some data processing delay
    # time.sleep(5)  # Simulate a delay for data processing 
    
    # Fetch data from main.py's main() method
    data = main()  # This now returns the processed data

    if request.method == 'POST':
        # Handle the Save to CSV action
        csv_path = save_to_csv(data)
        return send_file(csv_path, as_attachment=True)
    
    return render_template('result.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
