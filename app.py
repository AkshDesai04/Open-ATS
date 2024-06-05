from flask import Flask, request, redirect, url_for, render_template, send_file, jsonify
import os
from main import main  # Assuming this imports the main function from another module

app = Flask(__name__)

# Ensure the directory for uploaded files exists
UPLOAD_FOLDER = 'resumes'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_form():
    return render_template('upload.html')  # Likely renders a form for uploading resumes

@app.route('/upload', methods=['POST'])
def process_resumes():
    jd = request.form['JD']

    if 'files[]' not in request.files:
        return redirect(request.url)

    file = request.files['files[]']

    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Assuming main() returns some value
        result = main()  # Call main function without arguments

        # Return JSON data instead of rendering a template directly
        return jsonify(result=result, jd=jd)

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        # Handle the Save to CSV action
        data = request.json['result']  # Retrieve JSON data sent from /upload route
        csv_path = save_to_csv(data)
        return send_file(csv_path, as_attachment=True)

    return render_template('result.html')

if __name__ == "__main__":
    app.run(debug=True)
