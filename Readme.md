# Research Paper Data Extractor

A simple web application built with Flask that extracts metadata from research paper details using the Google Gemini API. The app compiles research paper data (such as title, author, year, etc.) into an accumulative vector and allows users to either view the compiled data or download it as an Excel file.

## Features

- **Extract Research Data:**  
  Uses the Google Gemini API to extract 14 specific fields from the provided paper details.  
  If a field is unavailable, the API returns "NA" for that field.

- **Accumulate Compiled Data:**  
  Compiled results are stored in a session as a vector of vectors. This allows you to compile multiple entries over time until you decide to clear the data.

- **Download Excel File:**  
  Download the accumulated compiled data as an Excel file (.xlsx) using the `openpyxl` library.

- **User-Friendly Frontend:**  
  A modern, responsive UI with a beautiful design using custom CSS.  
  Includes buttons to add new entries, clear form entries, compile data, download Excel files, and clear all compiled data.

## Prerequisites

- Python 3.x
- [Flask](https://palletsprojects.com/p/flask/)
- [openpyxl](https://openpyxl.readthedocs.io/)
- [Google GenAI Python client](https://developers.google.com/genai) (or similar, ensure it is installed and configured)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/meakc/research-paper-data-extractor.git
   cd research-paper-data-extractor
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**

   Create a `.env` file in the root directory and add your Google API key:

   ```env
   API_KEY = "your_google_api_key"
   ```

## Usage

1. **Run the Application:**

   ```bash
   python app.py
   ```

2. **Open Your Browser:**

   Navigate to `http://127.0.0.1:5000` to access the web application.

3. **Input Paper Details:**

   Enter the link and text of the research paper details you want to extract.

4. **Compile Data:**

   Click the "Compile" button to extract and compile the data.

5. **Download Excel File:**

   Click the "Download Excel" button to download the compiled data as an Excel file.

6. **Clear Compiled Data:**

   Click the "Clear Compiled Data" button to clear all accumulated data.


## Acknowledgements

- [Flask](https://palletsprojects.com/p/flask/)
- [openpyxl](https://openpyxl.readthedocs.io/)
- [Google GenAI Python client](https://developers.google.com/genai)

---

created by meakc