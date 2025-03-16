"""
The main Python script defines a Flask web application that allows users to input paper details,
extracts specific fields using the Gemini API, compiles the data, and provides functionality to
download or clear the accumulated data.

:param link: Thank you for providing the details. Please go ahead and provide the link for the paper
:param text: The `text` parameter in the `call_gemini_api` function represents the content of the
paper details that will be used to extract specific fields. This text should contain information
related to the paper, such as the title, author, year, journal name, impact factor, purpose of the
paper,
:return: The main Python script defines a Flask web application that provides functionality to
display a form for inputting paper details (links and text). The script includes functions to
interact with the Google GenAI API to extract specific fields from the provided paper details. The
extracted fields are then processed and displayed in a tabular format on the web application.
"""
from flask import Flask, render_template, request, send_file, session, redirect, url_for
import openpyxl
from io import BytesIO
from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
# Access the API key
API_KEY = os.getenv("API_KEY")
app = Flask(__name__)
app.secret_key = API_KEY

# Define headers for Excel and HTML table.
headers = [
    "LINKS OF THE PAPER",
    "TITLE OF THE PAPER",
    "AUTHOR",
    "YEAR OF PAPER",
    "JOURNAL NAME",
    "IMPACT FACTOR",
    "PURPOSE OF THE PAPER",
    "TECHNIQUES USED AND PROPOSED IN THE PAPER",
    "DATASET USED",
    "ACCURACY OF THE TECHNIQUES",
    "ADVANTAGES OVER OTHER TECHNIQUES",
    "DRAWBACK OF PROPOSED TECHNIQUES",
    "CONCLUSION OF PAPER",
    "FUTURE WORK"
]

# Initialize the Google GenAI client.
client = genai.Client(api_key=API_KEY)

def call_gemini_api(link, text):
    """
    The function `call_gemini_api` extracts specific fields from paper details and returns them as plain
    text with 14 fields separated by '|||'.
    
    :param link: Thank you for providing the details. Please go ahead and provide the link for the paper
    :param text: The `text` parameter in the `call_gemini_api` function is the content of the paper
    details that will be used to extract specific fields. This text will be processed by Gemini to
    extract information such as the title of the paper, author, year of the paper, journal name, impact
    factor
    :return: The function `call_gemini_api` is designed to extract specific fields from provided paper
    details and return the answer as plain text with exactly 14 fields separated by '|||'. It sends a
    request to the Gemini API with the provided link and text, expecting a response with the extracted
    fields. The response is then processed to ensure it contains 14 fields before returning the result
    vector, which is a
    """
    # Instruct Gemini to return plain text with exactly 14 fields separated by "|||".
    # If a field is unavailable, it should return "NA".
    prompt = (
        "Extract the following fields from the provided paper details and return the answer as plain text with exactly 14 fields separated by '|||'. "
        "The fields, in order, are:\n"
        "1. LINKS OF THE PAPER\n"
        "2. TITLE OF THE PAPER\n"
        "3. AUTHOR\n"
        "4. YEAR OF PAPER\n"
        "5. JOURNAL NAME\n"
        "6. IMPACT FACTOR\n"
        "7. PURPOSE OF THE PAPER\n"
        "8. TECHNIQUES USED AND PROPOSED IN THE PAPER\n"
        "9. DATASET USED\n"
        "10. ACCURACY OF THE TECHNIQUES\n"
        "11. ADVANTAGES OVER OTHER TECHNIQUES\n"
        "12. DRAWBACK OF PROPOSED TECHNIQUES\n"
        "13. CONCLUSION OF PAPER\n"
        "14. FUTURE WORK\n\n"
        f"Link: {link}\n\n"
        f"Text: {text}\n\n"
        "For any field that is not available or mentioned, return 'NA'. "
        "Return only the plain text result with fields separated by '|||'."
    )

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
    )
    raw = response.text.strip()
    print("Raw Gemini response:", raw)
    # Split the plain text response by the delimiter.
    result_vector = [field.strip() for field in raw.split("|||")]
    if len(result_vector) != 14:
        # The `print` statement you provided is used to output a warning message in case the number of
        # fields extracted from the Gemini API response is not equal to 14.
        print(f"Warning: Expected 14 fields but got {len(result_vector)} fields. Result: {result_vector}")
    return result_vector

# Home page with the form.
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Endpoint to compile data and display the accumulated results.
@app.route('/compile', methods=['POST'])
def compile_data():
    links = request.form.getlist('link')
    texts = request.form.getlist('text')
    new_rows = []
    for link, text in zip(links, texts):
        # Skip completely empty rows.
        if not link.strip() and not text.strip():
            continue
        result_vector = call_gemini_api(link, text)
        if len(result_vector) == 14:
            row = result_vector
        else:
            row = [link] + [""] * (len(headers) - 1)
        new_rows.append(row)
        print("Compiled row:", row)

    # Append new rows to the existing session data if it exists.
    if 'compiled_data' in session:
        compiled_data = session['compiled_data']
    else:
        compiled_data = []
    compiled_data.extend(new_rows)
    session['compiled_data'] = compiled_data

    return render_template('compiled.html', headers=headers, rows=compiled_data)

# Endpoint to download the accumulated compiled data as an Excel file.
@app.route('/process', methods=['POST'])
def process():
    # Use the accumulated compiled data from the session.
    compiled_data = session.get('compiled_data', [])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(headers)
    for row in compiled_data:
        ws.append(row)
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return send_file(output, download_name="research_data.xlsx", as_attachment=True)

# Endpoint to clear all accumulated compiled data.
@app.route('/delete_data', methods=['POST'])
def delete_data():
    session['compiled_data'] = []
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)