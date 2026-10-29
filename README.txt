AETHERIA — Environmental Data Analytics and Weather Intelligence

SETUP REQUIREMENTS
- Windows 10 or later
- Python 3.13
- Internet connection for weather data retrieval

HOW TO SET UP

1. Install Python 3.13 from https://www.python.org/downloads/.
   During installation, enable "Add Python to PATH" if that option appears.

2. Extract the Aetheria ZIP file to a folder.

3. Open Command Prompt or PowerShell.

4. Navigate to the extracted project folder. For example:

   cd "C:\path\to\Aetheria_Submission"

   Replace the example path with the actual folder location.

5. Create a virtual environment:

   py -3.13 -m venv .venv

   Run this command only once when setting up the project. If a working .venv environment already exists, do not create it again.

6. Activate the environment.

   Command Prompt:
   .venv\Scripts\activate.bat

   PowerShell:
   .\.venv\Scripts\Activate.ps1

7. Install the required packages:

   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt

HOW TO RUN

1. Make sure the virtual environment is activated.
2. Run:

   python -m streamlit run app.py

3. Open the local URL displayed in the terminal if the browser does not open automatically.

IMPORTANT NOTES
- Run commands from the project folder containing app.py and requirements.txt.
- Do not create the virtual environment repeatedly.
- Keep the supplied data and configuration files in their original locations.
- The Jupyter Notebook file Aetheria.ipynb can be opened separately in a compatible notebook environment.
- If Python or package installation fails, check the error message and the computer's Python and security settings.