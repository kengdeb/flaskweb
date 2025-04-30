from flask import Flask, request, render_template, send_file, redirect, url_for
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


def process_excel_file(filepath, filename):
    df = pd.read_excel(filepath)
    if 'Technician' in df.columns:
        df.drop('Technician', axis=1, inplace=True)

    processed_filepath = os.path.join(PROCESSED_FOLDER, filename)
    df.to_excel(processed_filepath, index=False)

    table_html = df.to_html(classes='table table-striped', index=False)
    download_link = f'/download/{filename}'
    return table_html, download_link


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        table_html, download_link = process_excel_file(filepath, filename)

        return render_template('index.html', table_html=table_html, download_link=download_link)

    return redirect(url_for('index'))


@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
# if __name__ == '__main__':
#     app.run(debug=True)
