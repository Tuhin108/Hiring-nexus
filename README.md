**Hiring Nexus - Neural Interface** 🤖
_A cyberpunk-themed hiring platform that utilizes AI to streamline the recruitment process_
===========================
📖 Description
---------------
Hiring Nexus is a powerful web application designed to optimize the recruitment process. It provides a structured and data-driven approach for recruiters and hiring managers to efficiently filter, score, and rank job applicants. By leveraging the Gemini API, it offers deeper, AI-powered insights into each candidate's profile, moving beyond traditional keyword matching.

✨ Features
-----------
1. Intelligent Candidate Filtering: Instantly narrow down your applicant pool for specific job positions by intelligently matching keywords from their experience and skills.
2. Customizable Scoring System: A finely-tuned, weighted algorithm scores each candidate to ensure the most relevant skills and experience are prioritized:
3. Experience: Weighted at 60% to highlight the most relevant professional history.
4. Skills: Weighted at 30% to confirm technical and professional qualifications.
5. Education: Weighted at 10% with a bonus for advanced degrees and top institutions.
6. AI-Powered Insights: Go beyond basic scores. The application uses the Gemini API to generate detailed summaries of a candidate's strengths and weaknesses, giving you a holistic view of their potential.
7. Intuitive User Interface: A clean and easy-to-use web interface makes managing and analyzing candidate data seamless, allowing you to focus on making the best hiring decisions.

🧰 Tech Stack Table
-------------------

| Category | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | Python | The core language for the backend logic and data processing. |
| | Flask | A lightweight Python web framework for handling API endpoints and serving the web interface. |
| | Requests | A Python library used for making API calls to the external Gemini service. |
| **Frontend** | HTML | Provides the structure and content of the user interface. |
| | CSS | Styles the application, giving it a modern cyberpunk theme with visual effects. |
| | JavaScript | Manages client-side interactions, form submissions, and dynamic content updates. |
| **Integrations** | Gemini API | An external service for generating AI-powered insights and rankings for candidates. |
| **Data Format** | JSON | The standard format for storing candidate data and for communication between the frontend and backend. |

📁 Project Structure
---------------------
The project is structured into the following folders and files:
* `app`: The core Flask application logic.
* `applications.json`: A JSON file for loading your candidate data.
* `templates/index.html`: The main HTML file for the web interface.
* `static/js/app.js`: Contains JavaScript for the front-end functionality.
* `static/css/style.css`: The CSS file for styling the application.

### ⚙️ How to Run
To get the Hiring Helper application up and running, follow these steps:
#### 1\. Prerequisites
Make sure you have the following installed on your system:
  * **Python 3.8 or higher**
  * **A Gemini API key**
#### 2\. Installation
First, clone the repository and navigate into the project directory:
```bash
git clone https://github.com/your-username/hiring-helper.git
cd hiring-helper
```
Next, install the necessary Python dependencies using pip:
```bash
pip install -r requirements.txt
```
#### 3\. Configuration
Set your Gemini API key as an environment variable before you run the application. This key is crucial for the AI-powered ranking feature.
```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```
#### 4\. Running the Application
Start the Flask server by executing the main Python script:
```bash
python app.py
```
Once the server is running, open your web browser and go to `http://127.0.0.1:5000` to access the application.

📸 Screenshots
---------------
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0d885fb0-d1aa-49ef-ac96-ca631cdbcc28" />


👤 Author
---------
The Hiring Nexus application was developed by [Tuhin Kumar Singha Roy](https://github.com/Tuhin108).


**Made with ❤️ by Tuhin for HR and Companies**
