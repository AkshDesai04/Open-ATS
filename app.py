from flask import Flask, request, redirect, url_for, render_template, send_file, jsonify
import os
import json
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
    # Debug: Print the form data
    print("Form Data:", request.form)
    
    # Safely access form data
    jd = request.form.get('JD')
    ExperienceValue = request.form.get('ExperienceValue')
    Experience = request.form.get('Experience')
    SkillsValue = request.form.get('SkillsValue')
    Skills = request.form.get('Skills')
    ToolsValue = request.form.get('ToolsValue')
    Tools = request.form.get('Tools')

    # Debug: Print individual form values
    print(f"JD: {jd}, ExperienceValue: {ExperienceValue}, Experience: {Experience}")
    print(f"SkillsValue: {SkillsValue}, Skills: {Skills}, ToolsValue: {ToolsValue}, Tools: {Tools}")

    if not all([jd, ExperienceValue, Experience, SkillsValue, Skills, ToolsValue, Tools]):
        return "Missing form data", 400  # Bad Request if any data is missing

    # Ensure the directory for job description file exists
    if not os.path.exists('job_description.txt'):
        open('job_description.txt', 'w').close()  # Create an empty file if it doesn't exist

    # Save job description details to a file
    with open('job_description.txt', 'w') as file:
        file.write(f"position: {jd}\n")
        file.write(f"expected experience: {Experience} years\n")
        file.write(f"skills: {Skills}\n")
        file.write(f"tools: {Tools}\n")
        file.write(f"value: experience={ExperienceValue}, skill={SkillsValue}, tool={ToolsValue}\n")

    # Assuming main() returns some value
    result = main()  # Call main function without arguments

    print("Result:", result)

    if 'files[]' not in request.files:
        return redirect(request.url)

    files = request.files.getlist('files[]')

    if files:
        filenames = []
        for file in files:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)

        # Redirect to result page
        return redirect(url_for('result'))

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'GET':
        # Render the result.html template for GET requests
        return render_template('result.html')
    
    # Handle POST request for saving to CSV (if needed)
    data = json.loads(request.form['result'])
    csv_path = save_to_csv(data)
    return send_file(csv_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
