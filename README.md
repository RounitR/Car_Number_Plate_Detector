<h1> Automatic Car Number Plate Detection </h1>

<h2>Overview</h2>
<p>This project is a Flask-based web application that allows users to upload videos, processes them using OpenCV and EasyOCR, and detects car number plates. The system highlights detected plates in the video, checks if they follow a specific regex pattern, and outputs the most common valid number plate detected.</p>

<h2>Features</h2>
<ul>
<li> <b>Upload Video:</b> Users can upload video files for processing.</li>
<li> <b>Automatic Plate Detection:</b> The application detects number plates using contour detection and Optical Character Recognition (OCR).</li>
- **Validation**: Plates are validated using a regex pattern ensuring they are 7 uppercase characters.
- **Video Output**: The processed video, with highlighted plates, is available for preview and download.
</ul>
## Tech Stack
- **Frontend**: HTML5, CSS3
- **Backend**: Flask (Python)
- **Processing Libraries**: OpenCV, EasyOCR
- **Video Processing**: Contour detection, Canny edge detection
- **File Handling**: Secure upload and processing of video files

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/username/repo-name.git
    ```
2. Navigate to the project directory:
    ```bash
    cd repo-name
    ```
3. Set up a virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```
4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
   
## How to Run
1. Activate the virtual environment:
    ```bash
    source env/bin/activate
    ```
2. Run the Flask server:
    ```bash
    python app.py
    ```
3. Open your browser and navigate to `http://127.0.0.1:5000/`.

## Project Structure
- **app.py**: The main Flask application file that handles routing and video processing.
- **/static/**: Contains processed video outputs and styles.
- **/uploads/**: Stores uploaded video files.
- **/templates/**: HTML files for rendering the web pages.
- **requirements.txt**: Contains the list of dependencies for the project.

## Usage
1. Upload a video file from the homepage.
2. The system processes the video and detects any valid number plates.
3. The processed video with the detected plate is displayed and available for download.

## License
This project is licensed under the MIT License.

---

You can adjust this content to suit your project's specifics.