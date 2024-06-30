# Indic-Translator

Indic-Translator is a comprehensive translation tool designed to bridge linguistic divides in the digital age, with a focus on Indian languages.

## Features

- Text-to-text translation
- Speech-to-text translation
- PDF document translation
- Chrome extension for webpage translation
- Support for multiple Indic languages

## Project Structure

- `/extension`: Contains files for the Chrome extension
- `/preprocessing`: Contains files for data preprocessing and model training
- `/static`: Static assets for the web application
- `/templates`: HTML templates for the web interface
- `app.py`: Main application file
- `fairseq.ipynb` - fairseq implementation

## Installation and Usage

Follow these steps to set up and run the Indic-Translator project:

1. Clone the repository:
   ```
   git clone https://github.com/AbhishekNair050/Indic-Translator.git
   cd Indic-Translator
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Open a web browser and navigate to `http://localhost:5000` to access the Indic-Translator web interface.

### Chrome Extension

To use the Chrome extension:

1. Open Chrome and navigate to `chrome://extensions`
2. Enable "Developer mode" in the top right corner
3. Click "Load unpacked" and select the `/extension` directory from this project
4. To disable safe mode for extensions (if needed):
   - Go to `chrome://flags`
   - Search for "extensions" and disable "Extension Safety Check"
   - Restart Chrome

## Preprocessing

The `/preprocessing` directory contains our initial attempts and current preprocessing pipeline:

- `data_cleaning.py`: Cleans and prepares the training data
- `inference.py`: Handles model inference
- `main.py`: Main script for the preprocessing pipeline
- `model.py`: Defines the translation model architecture
- `preprocessing.py`: Implements text preprocessing functions
