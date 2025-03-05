### GLOBETROTTER_HEADOUT

## GLOBETROTTER CHALLENGE README


# Project Overview

The GLOBETROTTER Challenge is an interactive web application designed to test users (wanderlust) knowledge of world geography through clues, trivia, and stunning images sourced from the Unsplash API. The backend is built using Django, and the dataset is expanded using OpenAI's API. The application is containerized with Docker and deployed on Railway for a scalable production-ready solution.


# Tech Stack Used

Backend: Python, Django
Frontend: HTML, CSS, JavaScript
Database: PostgreSQL
APIs: OpenAI for expanding dataset of destination info, Unsplash for fetching images of destinations
Containerization: Docker
Hosting: Railway
CI/CD Support: Git for version control


# Architecture Choice

The choice of Django allows for a clean MVC structure, and PostgreSQL serves as a robust and scalable database solution, while Docker simplifies deployments across different environments.


# Prerequisites

Before you start, ensure you have the following software installed:

Python (>= 3.10) from [python.org](https://www.python.org/downloads/)
PostgreSQL from [postgresql.org ](https://www.postgresql.org/download/)
Docker from [docker.com](https://www.docker.com/products/docker-desktop/)


# Project Structure

The project is structured as follows:

C:\GLOBETROTTER\
├── .env                     <-- Environment variables file  
├── .gitignore
├── docker-compose.yml       <-- Docker Compose configuration  
├── Dockerfile               <-- Dockerfile for container creation  
├── README.md                <-- Project documentation  
├── requirements.txt         <-- List of Python & deployment dependencies  
├── backend\
│   ├── venv\               <-- Virtual environment (ignored by Git)  
│   └── globetrotter_project\
│       ├── manage.py       <-- Django management file  
│       ├── settings.py     <-- Django settings  
│       ├── urls.py         <-- Project URL router  
│       ├── wsgi.py         <-- WSGI entry point  
│       └── game\           <-- Django app folder  
│           ├── __init__.py  
│           ├── admin.py    <-- Django admin registration  
│           ├── apps.py  
│           ├── models.py   <-- Models definitions (e.g., Destination, Score)  
│           ├── tests\      <-- Unit tests  
│           │   ├── test_models.py  
│           │   └── test_views.py  
│           ├── urls.py     <-- App-specific URLs  
│           ├── views.py    <-- View functions/classes  
│           ├── templates\  
│           │   └── game\  
│           │         └── index.html  <-- Main game template  
│           └── static\    <-- Static files  
│                 ├── css\  
│                 │     └── style.css  
│                 └── js\  
│                       └── app.js  
└── scripts\                <-- Auxiliary scripts  
    ├── data.json          <-- Starter dataset  
    ├── expanded_dataset.json  <-- Expanded dataset (after script execution)  
    └── final_code.py      <-- Script to generate additional trivia data  


# Step-by-Step Guide to Setup

1) Clone this repository via command line:

mkdir GLOBETROTTER  
cd GLOBETROTTER  


2) Create a virtual environment: (C:\GLOBETROTTER\backend\)

python -m venv venv  

Activate the virtual environment:

.\venv\Scripts\activate   


3) Install the following Python packages as listed in requirements.txt: (Make sure the directory should be in venv mode inside your DJANGO APP (in my case, its backend\ ) and then install via command line: "pip install -r requirements.txt")

asgiref==3.8.1  
certifi==2025.1.31  
charset-normalizer==2.1.1  
dj-database-url==2.3.0  
Django==4.2  
django-cors-headers==3.14.0  
gunicorn==23.0.0  
idna==3.10  
packaging==24.2  
psycopg2-binary==2.9.6  
python-dotenv==1.0.0  
requests==2.28.1  
sqlparse==0.5.3  
typing_extensions==4.12.2  
tzdata==2025.1  
urllib3==1.26.20  
whitenoise==6.9.0  
dj-static==0.0.6


4) Building the Django Project: All Django-related code is in ("C:\GLOBETROTTER\backend\globetrotter_project\").

4.1) settings.py (C:\GLOBETROTTER\backend\globetrotter_project\globetrotter_project)

4.1.1) Project Documentation and Imports:

"""
Django settings for globetrotter_project project.
"""
from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

This opening section includes a docstring describing the file’s purpose and imports necessary modules.
The Path class helps manage file system paths.
The os module is used for interacting with environment variables.
The dj_database_url package simplifies database configuration via URLs.
The load_dotenv function from the dotenv package loads environment variables from a .env file.

4.1.2) Loading Environment Variables and Defining BASE_DIR:

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
This part loads environment variables from the .env file into the runtime.
BASE_DIR defines the root directory of the project by resolving the path two levels up from the current file.

4.1.3) Secret Key and Debug Settings:

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

SECRET_KEY retrieves the secret key from an environment variable, enhancing security by keeping it out of source code.
DEBUG is set based on an environment variable; it defaults to False for production.
ALLOWED_HOSTS specifies which hosts/domains can serve the project. It is retrieved from an environment variable and split into a list.

4.1.4) Installed Applications:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'whitenoise.runserver_nostatic',
    'game',
]

This list defines all Django and third-party apps installed in the project.
Core Django apps provide administration, authentication, session management, etc.
corsheaders is included to handle Cross-Origin Resource Sharing.
whitenoise.runserver_nostatic integrates Whitenoise for serving static files even during development.
The custom game app is added for project-specific functionality.

4.1.5) Middleware Configuration:

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

Middleware is a chain of components that process requests and responses.
SecurityMiddleware provides security enhancements.
WhiteNoiseMiddleware serves static files efficiently in production and is positioned right after SecurityMiddleware.
CorsMiddleware handles CORS.
Other middleware manage sessions, common HTTP functions, CSRF protection, authentication, messages, and clickjacking protection.

4.1.6) CORS Configuration:

CORS_ALLOW_ALL_ORIGINS = True
This setting allows all origins during development, making it easier to work with front-end applications. In production, this should be configured more restrictively.

4.1.7) Root URL Configuration and Templates:

ROOT_URLCONF = 'globetrotter_project.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'game' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF specifies the module that contains URL patterns for the project.
The TEMPLATES configuration tells Django where to look for template files and defines context processors that automatically include certain variables in all templates.

4.1.8) WSGI Application:

WSGI_APPLICATION = 'globetrotter_project.wsgi.application'
This setting points to the WSGI application used by Django's server and in production, enabling communication between the web server and Django application.

4.1.9) Database Configuration: 5

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'globetrotter_db'),
            'USER': os.getenv('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', '#Anonymous05'),
            'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
            'PORT': os.getenv('POSTGRES_PORT', '5432'),
        }
    }

First, it tries to obtain a database URL from the environment.
If available, dj_database_url.config converts the URL into Django's database settings.
If not, it falls back to individual PostgreSQL settings with defaults for database name, user, password, host, and port.

4.1.10) Static Files Configuration:

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'game' / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_URL defines the URL prefix for static files.

STATICFILES_DIRS lists directories where Django will search for additional static files (like CSS, JavaScript, images).
STATIC_ROOT specifies the directory where static files will be collected for production.
STATICFILES_STORAGE uses Whitenoise's storage backend to compress and serve static files efficiently.

4.1.11) Default Primary Key Field Type:

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

This setting defines the default type of primary key field that Django uses for models that do not specify one, ensuring scalability for larger datasets.


4.2) Project url configuration (urls.py) (C:\GLOBETROTTER\backend\globetrotter_project\globetrotter_project)

4.2.1) Defining the URL Patterns:

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game.urls')),  # Direct root URL to the game app
]

The urlpatterns list is where URL routes are defined:
The first entry routes any URL that begins with admin/ to Django's built-in admin site. This allows administrators to access the admin interface.
The second entry uses an empty string ('') as the URL pattern. It includes the URL configuration from the game application. This means that the root URL of the project is handled by the URLs defined in the game app. The use of include helps keep the project modular and organized.

4.2.2) Serving Static Files in Development:

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

This conditional block checks if the DEBUG setting is enabled. When DEBUG is True (typically during development):

The static function appends an additional URL pattern to serve static files directly from the directory specified by STATIC_ROOT. This is useful because the Django development server does not serve static files by default. In a production environment, serving static files is usually handled by a dedicated web server or a service like Whitenoise.


5) Building the Django App: “game”

All code in this section is located under
("C:\GLOBETROTTER\backend\globetrotter_project\game\")

5.1) models.py (C:\GLOBETROTTER\backend\globetrotter_project\game)

5.1.1) Importing the Required Module:

from django.db import models

This line imports the models module from Django's database framework, which provides the base classes and fields needed to define the data structure (models) for the application.

5.1.2) Defining the Destination Model:

class Destination(models.Model):
This line defines a new model class called Destination that inherits from Django's Model class. This inheritance allows the class to gain all the functionality for interacting with a database.

5.1.3) Field Definitions

    city = models.CharField(max_length=100, unique=True)

The city field is a character field with a maximum length of 100 characters. The unique=True attribute ensures that each city name is unique in the database.

    country = models.CharField(max_length=100, blank=True)

The country field is also a character field with a maximum length of 100 characters. The blank=True attribute allows the field to be empty, meaning that the country information is optional.

    clues = models.JSONField(default=list)

The clues field is a JSONField that stores data in JSON format. The default=list ensures that if no data is provided, it will default to an empty list. This field can hold an array of clues for the destination.

    fun_fact = models.TextField(blank=True)

The fun_fact field is a TextField, which allows for longer text entries compared to CharField. With blank=True, it is optional, letting users or administrators leave this field empty if no fun fact is available.

    trivia = models.JSONField(default=list)

The trivia field, like the clues field, is a JSONField designed to store additional trivia in JSON format. The default value is set to an empty list.

    image_url = models.URLField(blank=True, max_length=500)

The image_url field is a URLField, which is meant to store a valid URL pointing to an image. It has a maximum length of 500 characters and is optional (blank=True), allowing the field to be empty if no URL is provided.

5.1.4) String Representation of the Model:

    def __str__(self):
        return self.city

This method defines the string representation of a Destination instance. When an object of the Destination model is printed or viewed in the Django admin interface, it will display the city name. This provides a human-readable identifier for each record.

5.2) views.py (C:\GLOBETROTTER\backend\globetrotter_project\game)

5.2.1) import json
from django.shortcuts import render
from .models import Destination

This section imports the necessary modules and the Destination model. The json module is used to convert Python objects into JSON format. The render function from Django shortcuts is used to generate an HTTP response by combining a template with a context. The Destination model, imported from the local models module, represents the database structure containing information about various destinations.

5.2.2) def index(request):
    # Query the Destination model (fields: city, country, clues, fun_fact, trivia, image_url)
    dests = list(Destination.objects.all().values(
        'city', 'country', 'clues', 'fun_fact', 'trivia', 'image_url'
    ))
    context = {
        'destinations_json': json.dumps(dests)
    }
    return render(request, 'game/index.html', context)

This function handles HTTP requests to the index page. It performs the following actions:
Queries the Destination model to retrieve all records and extracts specific fields such as city, country, clues, fun_fact, trivia, and image_url. The query returns a queryset that is then converted into a list of dictionaries using the values() method.
Converts the list of destination dictionaries into a JSON-formatted string using json.dumps. This JSON string is stored in a context dictionary under the key 'destinations_json'. The JSON data can then be used in the template for dynamic content generation.
Uses the render function to create and return an HTTP response. The response is generated by rendering the 'game/index.html' template with the context containing the destinations data.


5.3) index.html (C:\GLOBETROTTER\backend\globetrotter_project\game\templates\game)

5.3.1) Template Loading and Document Structure:

{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Globetrotter Challenge</title>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{% static 'css/style.css' %}">
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
</head>
<body class="light-mode">

This section starts with a Django template tag to load static files. The document is defined with the standard HTML5 doctype and language attribute. The head includes metadata (charset, viewport) and sets the title. It imports the Roboto font from Google Fonts, links the external CSS using a Django static tag, and includes a script for canvas-confetti to enable animations. The body starts with a class set to "light-mode" to apply light theme styles.

5.3.2) Fixed Static Panel Section:

<div id="static-panel">
  <div id="static-left">
    <div id="score-display">
      Score: <span id="scoreValue">0</span> 💰
      <div id="score-details">Correct: <span id="correctCount">0</span> | Wrong: <span id="wrongCount">0</span></div>
    </div>
  </div>
  <div id="static-center">
    <header>
      <h1>GLOBETROTTER CHALLENGE</h1>
      <p id="tagline">Guess the destination based on cryptic clues!</p>
    </header>
  </div>
  <div id="static-right">
    <button id="modeSwitch" title="Switch Mode">MODE</button>
    <button id="challengeBtn" title="Challenge a Friend">Challenge a Friend</button>
    <input type="text" id="username" placeholder="Enter Username">
  </div>
</div>

This block defines a fixed header panel that remains visible on the page. The panel is divided into three sections:
The left section displays the score using elements with IDs for score value and details.
The center section holds a header with the title and tagline.
The right section includes interactive elements like a mode switch button, a challenge button, and a text input for the username.

5.3.3) Main Game Area:

<main id="game">
  <div id="question-card">
    <div id="clue-image-container">
      <div id="clues"></div>
      <div id="image-container"></div>
    </div>
    <div id="options-container">
      <div class="options-column" id="left-options"></div>
      <div class="options-column" id="right-options"></div>
    </div>
    <div id="feedback"></div>
    <button id="nextBtn" onclick="nextQuestion()" disabled>Next</button>
  </div>
</main>

The main section of the document is dedicated to the game content. It includes:
A question card that contains a clue and image container. The clue and image containers are separate areas for showing hints and related images.
An options container split into two columns for answer choices.
A feedback area to display messages based on user interactions.
A "Next" button that triggers a JavaScript function (nextQuestion()) and is initially disabled.

5.3.4) Full-Screen Overlay for Animation:

<div id="cross-overlay"></div>
This single div element is reserved for displaying a full-screen overlay, used specifically to show a cross animation when a wrong answer is given. It is hidden by default and will be activated through CSS and JavaScript when needed.

5.3.5) Embedding Data and JavaScript Inclusion:

<script id="destinations-data" type="application/json">{{ destinations_json|safe }}</script>
<script src="{% static 'js/app.js' %}" defer></script>

The first script element embeds JSON data directly into the HTML. The data (destinations_json) is rendered safely from the server, allowing JavaScript to access it for dynamic content generation. The second script tag links to an external JavaScript file (app.js) using Django's static files tag and defers its execution until after the document has been parsed.

5.3.6) Closing HTML Tags:

</body>
</html>
These tags properly close the body and HTML elements, ensuring that the document is well-formed.


5.4) style.css (C:\GLOBETROTTER\backend\globetrotter_project\game\static\css)

5.4.1) CSS Variables for Light and Dark Modes:

:root {
  --bg-color-light: #ffffe0;
  --header-bg-light: #ffcccb;
  --underline-light: #d4af37;
  --text-color-light: #333;
  --option-initial: #d3d3d3;
  
  --bg-color-dark: #000;
  --header-bg-dark: #001f3f;
  --underline-dark: #d4af37;
  --text-color-dark: #ddd;
  
  --font-family: 'Roboto', sans-serif;
  --button-font-size: 1.8em;
  --button-padding: 15px 25px;
}

This block defines a set of CSS custom properties (variables) for both light and dark modes. The variables hold values for background colors, header colors, underline colors, text colors, and common settings like font family and button dimensions. By using these variables, you can easily manage color schemes and styling across the stylesheet.

5.4.2) Global Styles & Borders:

body {
  font-family: var(--font-family);
  margin: 0;
  padding: 0;
}
body.light-mode {
  background-color: var(--bg-color-light);
  color: var(--text-color-light);
  border: 4px solid #000;
}
body.dark-mode {
  background-color: var(--bg-color-dark);
  color: var(--text-color-dark);
  border: 4px solid #444;
}

This part applies global styles. The body element is given the font specified by the variable and has its margin and padding reset. Separate styles for light and dark modes set different background colors, text colors, and borders. The .light-mode class applies a bold black border, while the .dark-mode class uses a dark grey border.

5.4.3) Fixed Static Panel:

#static-panel {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 20vh;
  background-color: var(--option-initial);
  border-bottom: 2px solid var(--underline-light);
  z-index: 1100;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}
body.dark-mode #static-panel {
  background-color: var(--header-bg-dark);
  border-bottom: 2px solid var(--underline-dark);
}

This code creates a fixed header panel that stays at the top of the viewport and occupies 20% of the viewport height. It uses flexbox to align its child elements (left, center, and right sections). In light mode, it uses the light color variables, while in dark mode the background and underline change to dark-specific colors.

5.4.4) Static Panel Sections:

#static-left, #static-center, #static-right {
  flex: 1;
}
#static-left {
  text-align: left;
}
#static-center {
  text-align: center;
}
#static-right {
  text-align: right;
  display: flex;
  flex-direction: column;
  gap: 5px;
  align-items: flex-end;
}

The fixed panel is divided into three parts. Each section takes equal space due to flex: 1. The left, center, and right sections have their text aligned accordingly. The right section is styled as a column with a gap between its items and aligns them to the right.

5.4.5) Score Display:

#score-display {
  font-size: 1.8em;
  font-weight: bold;
}
#score-details {
  font-size: 0.8em;
  margin-top: 5px;
}

This snippet styles elements for score presentation. The main score is made prominent with a larger font size and bold weight, while the additional score details have a smaller font and a small margin on top.

5.4.6) Header Styling:

header {
  margin-top: 20px;
  padding: 0;
}
header h1 {
  font-size: 3.5em;
  margin: 0;
  font-weight: bold;
  text-transform: uppercase;
  white-space: nowrap;
}
header p#tagline {
  font-size: 1.8em;
  margin-top: 5px;
  white-space: nowrap;
}

The header inside the static panel is given extra margin at the top for spacing. The main heading (h1) uses a very large font size, bold weight, uppercase transformation, and ensures that it stays on one line with white-space: nowrap. The tagline paragraph is similarly styled with a moderate font size and top margin.

5.4.7) Main Game Area:

main#game {
  margin-top: 22vh;
  padding: 20px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

This block styles the main content area of the game. It adds a top margin to avoid the fixed static panel, centers the content horizontally, applies padding, and restricts the maximum width to 1200px.

5.4.8) Clue & Image Container:

#clue-image-container {
  text-align: center;
  margin-bottom: 20px;
}
#clues {
  font-size: 2em;
  margin-bottom: 20px;
  font-weight: bold;
}
#image-container {
  margin: 20px auto;
}
#image-container img {
  max-width: 700px;
  max-height: 400px;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

This section centers the content in the clue and image container. The clues text is made large and bold. The image container centers the image with automatic side margins. The image itself is limited to a maximum width and height, given rounded corners, and a shadow effect to add depth.

5.4.9) Options Container and Buttons:

#options-container {
  display: flex;
  justify-content: space-between;
  padding: 0 50px;
  margin-bottom: 20px;
}
.options-column {
  width: 40%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

The options container uses flexbox to space two columns (left and right) apart with padding. Each column is set to 40% width and stacks its buttons vertically with gaps between them.

.option-btn {
  width: 100%;
  background-color: var(--option-initial);
  color: #000;
  font-size: var(--button-font-size);
  font-weight: bold;
  border: 1px solid #000;
  padding: var(--button-padding);
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s;
  box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
}
.option-btn:hover {
  transform: scale(1.05);
  box-shadow: 4px 4px 8px rgba(0,0,0,0.4);
}
.option-btn.correct {
  background-color: #28a745 !important;
}
.option-btn.wrong {
  background-color: #8b0000 !important;
}
body.light-mode .option-btn.wrong {
  color: #ffffe0;
}
body.dark-mode .option-btn.correct {
  color: #000;
}

The .option-btn style makes each button take full column width, uses the initial option background, and sets text styling. It also includes a subtle shadow and transitions for a hover effect that scales the button and increases the shadow. Additional classes (.correct and .wrong) change the background color to indicate if an option is correct or wrong. Mode-specific tweaks adjust text color for the wrong and correct states in light and dark modes respectively.

5.4.10)  Feedback Styling:

#feedback {
  font-size: 1.8em;
  margin-bottom: 20px;
  min-height: 60px;
  font-weight: bold;
}

This rule styles a feedback area with a larger, bold font and ensures a minimum height so that space is reserved even if no feedback is present. A bottom margin separates it from other elements.

5.4.11) Next Button Styling:

#nextBtn {
  width: 100%;
  padding: 15px 0;
  font-size: 1.8em;
  font-weight: bold;
  background-color: #f1c40f;
  color: #000;
  border: 1px solid #000;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}
#nextBtn:hover:enabled {
  background-color: #d4ac0d;
  transform: scale(1.05);
}
#nextBtn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

This section styles the "Next" button to be full-width with ample padding. It uses a bright yellow background with black text and border. A hover effect enlarges the button slightly and changes its background color. When the button is disabled, it shows a grey background and a "not allowed" cursor.

5.4.12) Full-screen Overlay for Wrong Answer Animation:

#cross-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1200;
  display: none;
  align-items: center;
  justify-content: center;
}
.cross-animation {
  font-size: 12em;
  color: #8b0000;
  opacity: 0.8;
  animation: fadeOut 2s ease-out forwards, shake 0.5s ease-in-out;
}
@keyframes fadeOut {
  0% { opacity: 0.8; }
  100% { opacity: 0; }
}
@keyframes shake {
  0% { transform: translate(0, 0); }
  25% { transform: translate(15px, 0); }
  50% { transform: translate(0, 0); }
  75% { transform: translate(-15px, 0); }
  100% { transform: translate(0, 0); }
}

This code creates a full-screen overlay that is hidden by default. When activated (for instance, after a wrong answer), it shows a large cross (styled by .cross-animation) in the center. Two animations run concurrently: one fades the cross out over 2 seconds and the other shakes it briefly for visual impact.

5.4.13) Allow Vertical Scrolling:

html, body {
  min-height: 100vh;
  overflow-y: auto;
}

The final snippet ensures that both the HTML and body elements have a minimum height equal to the viewport height and that vertical scrolling is allowed. This helps maintain a good layout, especially when content exceeds the viewport.


5.5) app.js (C:\GLOBETROTTER\backend\globetrotter_project\game\static\js)

5.5.1) Parsing Embedded Destinations Data:

const destinations = JSON.parse(document.getElementById('destinations-data').textContent);

Explanation: This line retrieves a JSON string embedded in the HTML element with the ID destinations-data and parses it into a JavaScript object (in this case, an array of destination objects). This array is then stored in the constant destinations for use throughout the game.

5.5.2) Declaring Game State Variables:

let currentQuestionIndex = 0;
let score = 0;
let correctCount = 0;
let wrongCount = 0;
let questions = [];

Explanation- These variables maintain the game state:
currentQuestionIndex: Keeps track of which question is currently being displayed.
score: Tracks the total number of correct answers.
correctCount and wrongCount: Count the number of correct and incorrect responses, respectively.
questions: An array that will later store a shuffled copy of the destinations data.

5.5.3) Initializing the Game:

function initGame() {
  questions = destinations.slice();
  shuffleArray(questions);
  currentQuestionIndex = 0;
  score = 0;
  correctCount = 0;
  wrongCount = 0;
  updateScore();
  loadQuestion();
}

Explanation: The initGame function sets up the game by:
Creating a copy of the destinations array into questions.
Shuffling the questions array (using the shuffleArray function described below).
Resetting the game state counters.
Updating the score display.
Loading the first question by calling loadQuestion().

5.5.4) Shuffling an Array Using Fisher-Yates:

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

Explanation: This function randomizes the order of the elements in the provided array. It uses the Fisher-Yates (Knuth) shuffle algorithm:
It iterates backward through the array.
For each index i, a random index j (between 0 and i) is chosen.
The elements at indices i and j are then swapped. This shuffling is used to randomize both the order of questions and the order of answer options.

5.5.5) Loading a Question:

function loadQuestion() {
  document.getElementById('feedback').innerText = '';
  document.getElementById('nextBtn').disabled = true;
  
  const cluesDiv = document.getElementById('clues');
  const imageContainer = document.getElementById('image-container');
  const leftOptionsDiv = document.getElementById('left-options');
  const rightOptionsDiv = document.getElementById('right-options');
  
  cluesDiv.innerHTML = '';
  imageContainer.innerHTML = '';
  leftOptionsDiv.innerHTML = '';
  rightOptionsDiv.innerHTML = '';
  
  document.body.style.backgroundImage = 'none';
  
  if (currentQuestionIndex >= questions.length) {
    cluesDiv.innerHTML = `<p>Game over! Your final score is ${score} (Correct: ${correctCount} | Wrong: ${wrongCount}).</p>`;
    document.getElementById('nextBtn').innerText = 'Play Again';
    document.getElementById('nextBtn').disabled = false;
    return;
  }
  
  const question = questions[currentQuestionIndex];
  
  const cluesToShow = question.clues.slice(0, 2);
  cluesToShow.forEach(clue => {
    const p = document.createElement('p');
    p.innerText = clue;
    cluesDiv.appendChild(p);
  });
  
  if (question.image_url) {
    const img = document.createElement('img');
    img.src = question.image_url;
    img.alt = `Image of ${question.city}`;
    imageContainer.appendChild(img);
  }
  
  let options = [question.city];
  const otherCities = questions.filter(q => q.city !== question.city).map(q => q.city);
  shuffleArray(otherCities);
  options = options.concat(otherCities.slice(0, 3));
  shuffleArray(options);
  
  const leftOptions = options.slice(0, 2);
  const rightOptions = options.slice(2);
  
  leftOptions.forEach(option => {
    const btn = document.createElement('button');
    btn.className = 'option-btn';
    btn.innerText = option;
    btn.onclick = () => checkAnswer(btn, option, question.city, question.fun_fact);
    leftOptionsDiv.appendChild(btn);
  });
  
  rightOptions.forEach(option => {
    const btn = document.createElement('button');
    btn.className = 'option-btn';
    btn.innerText = option;
    btn.onclick = () => checkAnswer(btn, option, question.city, question.fun_fact);
    rightOptionsDiv.appendChild(btn);
  });
}

Explanation: The loadQuestion function handles rendering the current question:

It clears any previous feedback and resets the "Next" button.
It clears out the contents of the clues, image, and options containers.
It resets the body background to the default state.
If there are no more questions (i.e., currentQuestionIndex exceeds the number of questions), it displays a game-over message along with the final score, changes the "Next" button to “Play Again,” and enables it.
Otherwise, it extracts the current question, displays up to two clues, and creates an image element if an image URL exists.
It then generates answer options by ensuring the correct answer is included along with three randomly selected incorrect answers. These options are shuffled and divided into two columns (left and right) for display.
For each option, it creates a button that, when clicked, calls the checkAnswer function with the corresponding parameters.

5.5.6)  Checking the User's Answer:

function checkAnswer(button, selected, correct, funFact) {
  const optionButtons = document.querySelectorAll('.option-btn');
  optionButtons.forEach(btn => btn.disabled = true);
  
  const feedbackDiv = document.getElementById('feedback');
  if (selected === correct) {
    button.classList.add('correct');
    feedbackDiv.innerHTML = `🎉 Correct! Fun Fact: ${funFact}`;
    score++;
    correctCount++;
    updateScore();
    confetti({ particleCount: 200, spread: 100, origin: { y: 0.6 } });
  } else {
    button.classList.add('wrong');
    feedbackDiv.innerHTML = `😢 Incorrect! Fun Fact: ${funFact}`;
    wrongCount++;
    updateScore();
    triggerCrossAnimation();
    optionButtons.forEach(btn => {
      if (btn.innerText === correct) {
        btn.classList.add('correct');
      } else if (!btn.classList.contains('wrong')) {
        btn.classList.add('wrong');
      }
    });
  }
  document.getElementById('nextBtn').disabled = false;
}

Explanation: The checkAnswer function validates the user's answer when an option button is clicked:

It disables all answer buttons to prevent multiple selections.
It compares the selected answer with the correct answer.
If the answer is correct:
It visually marks the button as correct.
It updates the feedback area with a positive message and fun fact.
It increments the score and the correct answer counter.
It updates the displayed score.
It triggers a confetti animation (using an external library).
If the answer is incorrect:
It marks the selected button as wrong.
It displays a negative message along with the fun fact.
It increments the wrong answer counter and updates the score.
It triggers a full-screen cross animation to indicate an error.
It also highlights the correct answer among all buttons.
Finally, it enables the "Next" button so that the user can proceed.

5.5.7) Triggering the Cross Animation for Incorrect Answers:

function triggerCrossAnimation() {
  const crossOverlay = document.getElementById('cross-overlay');
  crossOverlay.innerHTML = '<div class="cross-animation">❌</div>';
  crossOverlay.style.display = 'flex';
  setTimeout(() => {
    crossOverlay.style.display = 'none';
    crossOverlay.innerHTML = '';
  }, 2000);
}

Explanation: When an incorrect answer is chosen, this function displays a full-screen overlay with a red cross (using an emoji). The overlay appears for 2 seconds before being hidden again, providing a clear visual indication of the wrong answer.

5.5.8) Moving to the Next Question

function nextQuestion() {
  if (currentQuestionIndex >= questions.length - 1) {
    initGame();
    document.getElementById('nextBtn').innerText = 'Next';
    return;
  }
  currentQuestionIndex++;
  loadQuestion();
}

Explanation: The nextQuestion function determines how to proceed after a question is answered:

If the current question is the last one, the game is restarted by calling initGame(), and the "Next" button is reset.
Otherwise, it increments the currentQuestionIndex and calls loadQuestion() to display the next question.

5.5.9) Updating the Score Display

function updateScore() {
  document.getElementById('scoreValue').innerText = score;
  document.getElementById('score-details').innerText = `Correct: ${correctCount} | Wrong: ${wrongCount}`;
}

Explanation: This function updates the score shown on the page. It retrieves the elements that display the overall score and the breakdown of correct and wrong counts, then updates their text to match the current game state.

5.5.10) Challenge a Friend Feature (WhatsApp Sharing):

document.getElementById('challengeBtn').addEventListener('click', () => {
  const username = document.getElementById('username').value.trim();
  if (!username) {
    alert('Please enter a unique username to challenge a friend.');
    return;
  }
  const shareMessage = encodeURIComponent(
    `Hey, I'm ${username} with a score of ${score} in Globetrotter Challenge! Can you beat me? Play now: ${window.location.href}`
  );
  const whatsappUrl = `https://api.whatsapp.com/send?text=${shareMessage}`;
  window.open(whatsappUrl, '_blank');
});

Explanation: This snippet implements the "Challenge a Friend" feature:

An event listener is attached to a button with the ID challengeBtn.
When clicked, it checks if a username is provided.
If a username exists, it creates a message including the username, current score, and game URL.
The message is encoded for URL compatibility, and then WhatsApp's sharing URL is built.
Finally, it opens the WhatsApp URL in a new window, allowing the user to send the invite.

5.5.11) Mode Switching Between Dark and Light Modes:

const modeSwitch = document.getElementById('modeSwitch');
modeSwitch.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
  document.body.classList.toggle('light-mode');
});

Explanation: This block adds functionality to toggle between dark and light themes:
It attaches an event listener to an element with the ID modeSwitch.
When clicked, it toggles CSS classes on the body element to switch between dark and light modes.

5.5.12) Starting the Game on Page Load:

window.onload = initGame;

Explanation: This final line ensures that as soon as the web page has fully loaded, the initGame function is called to start the game immediately.


6) Data Generation/ Dataset Expansion Script  (C:\GLOBETROTTER\scripts)

Create final_code.py in the scripts folder to generate and enrich the dataset:

6.1) Imports and Environment Setup

This section imports necessary modules for JSON handling, HTTP requests, delays, regular expressions, environment variable management, and concurrent execution. It then loads environment variables from a .env file and sets up the API key for OpenAI.

import json                     #For parsing and generating JSON data
import requests                 #For making HTTP API calls
import time                     #For adding delays (sleep)
import os                       #For interacting with the operating system (e.g., environment variables)
import re                       #For using regular expressions to process strings
from dotenv import load_dotenv  #For loading environment variables from a .env file
from concurrent.futures import ThreadPoolExecutor, as_completed  # For running tasks concurrently

#Load environment variables from .env file so that API keys and other secrets are available.
load_dotenv()

#Retrieve the OpenAI API key from environment variables.
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
#Set up headers for OpenAI API calls using the API key.
openai_headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

6.2) Configurable Parameters

Several configurable parameters are defined here. They set the target number of destinations, the delays between generation and processing calls, and the maximum number of attempts for generating unique city names.

# Configurable parameters:
target_total = 120               # The total number of unique destinations (including originals) required.
generation_delay = 5             # Delay (in seconds) after each generation call to avoid rapid-fire requests.
processing_delay = 5             # Delay (in seconds) after processing all destinations.
max_generation_attempts = 50     # Maximum number of attempts to generate additional unique cities.

6.3) Helper Functions for JSON and String Sanitization

Two functions are provided here. The first, sanitize_json_string, extracts all double-quoted substrings and rebuilds a valid JSON array. The second, fallback_extract_strings, serves as a backup to extract strings if standard sanitization fails.

def sanitize_json_string(s):
    """
    Sanitize the raw JSON string by extracting all complete double-quoted strings 
    and rebuilding a valid JSON array.
    """
    items = re.findall(r'"([^"]+)"', s)  # Find all substrings between double quotes.
    return json.dumps(items)             # Return as a JSON-formatted string (an array).

def fallback_extract_strings(s):
    """Fallback method: extract all double-quoted strings from s."""
    return re.findall(r'"([^"]+)"', s)

6.4) Generating Destination Names

The generate_destination_names function builds a prompt for GPT-3.5-turbo to generate a JSON array of famous international city names, while excluding any names already provided. It then calls the OpenAI API, sanitizes the response, and returns the list of city names. If issues arise, it retries a few times and may fall back to a simpler extraction method.

def generate_destination_names(count, exclude_list, retries=3):
    """
    Generate a JSON array containing 'count' famous international destination city names
    using the GPT-3.5-turbo model.
    """
    exclude_str = ", ".join(exclude_list)  # Create a comma-separated string of cities to exclude.
    prompt = (
        f"Provide a JSON array containing {count} famous international destination city names "
        f"that are well-known around the globe. Exclude these if possible: [{exclude_str}]. "
        'Return only the city names as strings. For example: '
        '["Sydney", "Rio de Janeiro", "Cape Town", "New York City", "London", "Dubai", "Tokyo"]'
    )
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
        "temperature": 0.7,
    }
    for attempt in range(retries):
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=openai_headers, json=data)
        if response.status_code == 200:
            raw_text = response.json()['choices'][0]['message']['content'].strip()  # Extract response text.
            sanitized_text = sanitize_json_string(raw_text)  # Sanitize to ensure valid JSON.
            try:
                destination_names = json.loads(sanitized_text)  # Attempt to parse JSON.
                if isinstance(destination_names, list) and all(isinstance(n, str) for n in destination_names):
                    return destination_names  # Return the valid list of strings.
                else:
                    print("Error: Generated output is not a valid list of strings.")
            except json.JSONDecodeError:
                print("Error: Unable to decode JSON after sanitization.")
                print("Sanitized text:", sanitized_text)
                fallback = fallback_extract_strings(sanitized_text)
                if fallback:
                    print("Using fallback extraction method.")
                    return fallback
        else:
            print(f"Error: API returned status code {response.status_code}")
            print("Response:", response.text)
        time.sleep(2)  # Wait for 2 seconds before retrying.
    return []  # Return an empty list if unable to generate valid names.

6.5) Fixing Malformed JSON for Trivia

The function fix_inner_quotes attempts to fix unescaped inner quotes within the trivia array in the JSON text by locating the array and escaping any problematic characters.

def fix_inner_quotes(text):
    """
    Attempt to fix unescaped inner quotes in the trivia array of the JSON text.
    """
    match = re.search(r'"trivia":\s*\[(.*?)\]', text, flags=re.DOTALL)
    if not match:
        return text
    array_content = match.group(1)
    elements = re.findall(r'"(.*?)"', array_content)
    fixed_elements = []
    for elem in elements:
        fixed_elem = elem.replace('"', '\\"')
        fixed_elements.append(f'"{fixed_elem}"')
    fixed_array = ", ".join(fixed_elements)
    fixed_text = re.sub(r'("trivia":\s*\[).*?(\])', r'\1' + fixed_array + r'\2', text, flags=re.DOTALL)
    return fixed_text

6.6) Generating Detailed Destination Information

The generate_details function sends a prompt to GPT-3.5-turbo asking for detailed destination information (including country, clues, fun fact, and trivia) in a specified JSON format. It tries to decode the response; if decoding fails due to formatting issues, it attempts to fix the JSON using fix_inner_quotes before retrying.

def generate_details(destination_name, retries=3):
    """
    Generate detailed information for a given destination including clues, fun fact, trivia, and country info.
    """
    prompt = (
        f"Provide details for the destination {destination_name} in the following JSON format:\n"
        'Ensure that the output is valid JSON with all inner double quotes properly escaped:\n'
        '{"city": "<city name>", "country": "<country>", "clues": ["<clue1>", "<clue2>"], '
        '"fun_fact": "<fun fact>", "trivia": ["<trivia1>", "<trivia2>"]}'
    )
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 0.7,
    }
    for attempt in range(retries):
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=openai_headers, json=data)
        if response.status_code == 200:
            result_text = response.json()['choices'][0]['message']['content'].strip()  # Get response text.
            try:
                details = json.loads(result_text)  # Attempt to load JSON.
                return details
            except json.JSONDecodeError:
                print(f"Error decoding JSON for {destination_name} (attempt {attempt+1}).")
                print("Raw response:", result_text)
                fixed_text = fix_inner_quotes(result_text)
                try:
                    details = json.loads(fixed_text)
                    return details
                except json.JSONDecodeError:
                    print(f"Failed to fix JSON for {destination_name} on attempt {attempt+1}.")
        else:
            print(f"Error: API returned status code {response.status_code} for {destination_name}.")
        time.sleep(2)
    return {
        "city": destination_name,
        "country": "",
        "clues": ["No clue available."],
        "fun_fact": "No fun fact available.",
        "trivia": ["No trivia available."]
    }

6.7) Fetching an Image URL

This function uses the Unsplash API to search for an image based on the destination name. It retrieves and returns the URL of the first image found or returns an empty string if no image is found.

def fetch_image_url(destination_name):
    """
    Fetch an image URL for the destination using the Unsplash API.
    """
    UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
    url = f"https://api.unsplash.com/search/photos?query={destination_name}&per_page=1"
    unsplash_headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    response = requests.get(url, headers=unsplash_headers)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            return results[0]['urls']['regular']
    return ""

6.8) Processing a Single Destination

The process_destination function combines previous functions. It generates detailed information for a given destination and fetches its image URL. The result is a dictionary enriched with all necessary details.

def process_destination(name):
    """
    Process a single destination: generate details and fetch its image URL.
    """
    details = generate_details(name)
    details['city'] = name
    details.setdefault('country', "")
    details['image_url'] = fetch_image_url(name)
    return details

6.9)  Main Execution Block

This part of the script orchestrates the overall process:

It loads an existing dataset from data.json.
It builds a dictionary of unique cities and enriches any missing data.
It generates additional unique city names until the target is reached, using both API calls and a fallback list.
It then processes all destinations concurrently.
Finally, it saves the enriched dataset to expanded_dataset.json.

"""
if __name__ == '__main__':
    # Load the original dataset from 'data.json'
    with open('data.json', 'r') as f:
        original_data = json.load(f)
    
    # Build a dictionary of unique cities (using lowercase keys for uniqueness)
    unique_cities = {}
    expanded = []
    for entry in original_data:
        name = (entry.get('city') or entry.get('name') or "").strip()
        if name:
            unique_cities[name.lower()] = name
        if not (entry.get('clues') and entry.get('fun_fact') and entry.get('trivia') and entry.get('country')):
            details = generate_details(name)
            entry.update(details)
        if not entry.get('image_url'):
            entry['image_url'] = fetch_image_url(name)
        expanded.append(entry)
    
    print(f"Original dataset provides {len(unique_cities)} unique cities.")
    
    # Generate additional unique city names until reaching target_total or maximum attempts.
    attempts = 0
    while len(unique_cities) < target_total and attempts < max_generation_attempts:
        attempts += 1
        needed = target_total - len(unique_cities)
        print(f"\nAttempt {attempts}: Generating {needed} additional unique city names...")
        new_names = generate_destination_names(needed, list(unique_cities.keys()))
        if new_names:
            for name in new_names:
                cleaned = name.strip()
                lc = cleaned.lower()
                if cleaned and lc not in unique_cities:
                    unique_cities[lc] = cleaned
                    print(f"Accepted new city: {cleaned}")
        else:
            print("No names returned in this generation call.")
        print(f"Waiting {generation_delay} seconds after generation attempt {attempts}...")
        time.sleep(generation_delay)
    
    # Use fallback cities if the target_total is still not reached.
    if len(unique_cities) < target_total:
        fallback_cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
            "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte",
            "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington"
        ]
        for city in fallback_cities:
            if len(unique_cities) >= target_total:
                break
            if city.lower() not in unique_cities:
                unique_cities[city.lower()] = city
                print(f"Added fallback city: {city}")
    
    final_city_list = list(unique_cities.values())[:target_total]
    print(f"\nFinal list of unique city names collected ({len(final_city_list)}):")
    print(final_city_list)
    
    # Process details for all unique cities concurrently using a ThreadPoolExecutor.
    processed_destinations = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_destination, name): name for name in final_city_list}
        for future in as_completed(futures):
            try:
                result = future.result()
                processed_destinations.append(result)
                print(f"Processed: {result['city']}")
            except Exception as e:
                print(f"Error processing {futures[future]}: {e}")
    print(f"Waiting {processing_delay} seconds after processing...")
    time.sleep(processing_delay)
    
    final_count = len(processed_destinations)
    print(f"\nFinal dataset has {final_count} destinations (expected: {target_total}).")
    
    # Save the final enriched dataset to 'expanded_dataset.json'.
    with open('expanded_dataset.json', 'w') as f:
        json.dump(processed_destinations, f, indent=2)
    
    print("Dataset expansion complete. Check 'expanded_dataset.json' for the unique destinations.") 
    """


7) Custom Django Management Command (import_data.py) (C:\GLOBETROTTER\backend\globetrotter_project\game\management\commands)

7.1) Imports and Setup for Django Management Command

This file imports modules for JSON handling, constructing file paths, Django's management command framework, and the Destination model from the Django application.

import json                         # For parsing JSON data.
from pathlib import Path            # For constructing filesystem paths in an OS-independent way.
from django.core.management.base import BaseCommand  # Base class for Django management commands.
from game.models import Destination  # Import the Destination model from the Django app.

7.2) Defining the Command Class

The command class inherits from Django's BaseCommand and provides a help message describing its purpose. This sets up the custom management command for importing destination data.

class Command(BaseCommand):
    help = 'Import destinations from expanded_dataset.json'

7.3) Handling File Location and Import Logic

Inside the handle method, the code calculates the project's root directory, constructs the path to the expanded_dataset.json file (located in a scripts folder), and attempts to open it. For each destination entry in the JSON file, the command uses Django's get_or_create method to insert or skip duplicate records in the Destination model. It outputs the results of each operation.

    def handle(self, *args, **kwargs):
        # Determine the project root by going up 5 directory levels.
        root_dir = Path(__file__).resolve().parents[5]
        # Construct the full path to the JSON file.
        json_path = root_dir / 'scripts' / 'expanded_dataset.json'
        
        self.stdout.write(f"Looking for JSON file at: {json_path}")
        
        try:
            # Open and load the JSON data.
            with open(json_path, 'r') as f:
                data = json.load(f)
                # Process each destination entry.
                for entry in data:
                    destination, created = Destination.objects.get_or_create(
                        city=entry.get('city'),
                        defaults={
                            'country': entry.get('country', ''),
                            'clues': entry.get('clues', []),
                            'fun_fact': entry.get('fun_fact', ''),
                            'trivia': entry.get('trivia', []),
                            'image_url': entry.get('image_url', ''),
                        }
                    )
                    # Output whether a destination was imported or skipped.
                    if created:
                        self.stdout.write(f"Imported: {destination.city}")
                    else:
                        self.stdout.write(f"Skipped (exists): {destination.city}")
        except FileNotFoundError:
            # Output an error if the JSON file is not found.
            self.stdout.write(self.style.ERROR(f"File not found: {json_path}"))


8) Environment Variables

Create a .env file in the root directory (C:\GLOBETROTTER\) with the following content:

SECRET_KEY="your_django_secret_key"          #Extract it from settings.py 
POSTGRES_DB=railway  
POSTGRES_USER=postgres  
POSTGRES_PASSWORD="your_database_password"   #It is set by the user while installing POSTGRESQL
POSTGRES_HOST=postgres.railway.internal                          
POSTGRES_PORT=5432  
DEBUG=False                                     # Set to false while deploying to any web host
UNSPLASH_ACCESS_KEY="your_unsplash_access_key"  # Get it by creating account on UNSPLASHED
OPENAI_API_KEY="your_openai_api_key"   # Get it from here "https://platform.openai.com/api-keys"
ALLOWED_HOSTS="*"                               # All allowed hosts are set
DATABASE_URL="your_postgres_connection_url"  


9) Docker Configuration

Create the following files in your project root (C:\GLOBETROTTER\):

9.1) Dockerfile:

FROM python:3.10-slim  
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1  
WORKDIR /app  
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*  
COPY requirements.txt /app/  
RUN pip install --upgrade pip && pip install -r requirements.txt  
COPY . /app/  
EXPOSE 8000  
CMD ["gunicorn", "--chdir", "backend/globetrotter_project", "--bind", "0.0.0.0:8000", "globetrotter_project.wsgi:application"]  
docker-compose.yml:

9.2) docker-compose.yml

version: '3.9'  
services:  
  web:  
    build: ./backend  
    command: python manage.py runserver 0.0.0.0:8000  
    volumes:  
      - ./backend:/app  
    ports:  
      - "8000:8000"  
    env_file:  
      - .env  
    depends_on:  
      - db  
  db:  
    image: postgres:15  
    environment:  
      POSTGRES_DB: railway  
      POSTGRES_USER: postgres  
      POSTGRES_PASSWORD: "your_database_password"     #Get it while installing postgresql
    volumes:  
      - postgres_data:/var/lib/postgresql/data/  
    ports:  
      - "5432:5432"  
volumes:  
  postgres_data:  

9.3) Build the Docker Image (Directory: C:\GLOBETROTTER\) in normal mode via command line:

docker-compose build


10) Running Unit Tests

Globetrotter project includes unit tests for views and models to ensure that the application behaves as expected. Follow the steps below to run the tests and generate a test coverage report.

10.1) Activate the Virtual Environment 

cd C:\GLOBETROTTER\backend
venv\Scripts\activate

10.2) Navigate to the Django Project Directory

cd globetrotter_project

10.3) Run Django's built-in test runner

python manage.py test


11) Pushing the project to GitHub via fresh Command Prompt interface

11.1) Go to project root directory:

cd C:\GLOBETROTTER

11.2) Initialize Git:

git init  

11.3) Add Files:

git add .  

11.4) commit Changes:

git commit -m "Initial commit of GLOBETROTTER project"  

11.5) Push to GitHub:

After creating a new repository on GitHub:

git remote add origin https://github.com/yourusername/GLOBETROTTER.git  
git branch -M main  
git push -u origin main  


12) For Deployment on Railway

12.1) Create a Railway Project:

12.2) Import Your GitHub Repository:

12.3) Link your GitHub repository with the Railway project. Railway will detect your Dockerfile automatically.

12.4) Add PostgreSQL Plugin:

Under your Railway project, go to the "Plugins" section and add PostgreSQL.

12.5) Set Environment Variables:

Add all variables from your .env file in the environment settings of Railway.

12.6) Configure Build Commands:

Under "Build":
python backend/globetrotter_project/manage.py collectstatic --noinput 

12.7) Configure Pre-Deployment Commands:

Under "Deploy":
python backend/globetrotter_project/manage.py migrate && python backend/globetrotter_project/manage.py import_data  

12.8) Deploy your Application:

Click on the deploy button to push your application live.

12.9) Set Public Networking:

Once the deployment is complete, enable public access and set the application port to 8000.

12.10) Railway will provide a public URL for your application. Open the URL in your browser to verify that the application is running correctly.

12.11) Use Railway’s logging interface to monitor application logs.


13) Core Requirements Fulfilled

1️⃣ Dataset & AI Integration:

The application expands from a starter dataset using OpenAI to generate clues, fun facts, and trivia for 100+ destinations.

2️⃣ Functional Web App:

Presents 1-2 clues for each destination.
Lets users select answers from multiple options.
Provides immediate feedback with animated response effects.
Tracks users' scores and allows for replay.

3️⃣ Challenge a Friend Feature:

Users can generate a personalized invite link to challenge friends via WhatsApp, displaying their score.


14) Future Enhancements

Consider adding timed games or limit on the number of incorrect answers.

Integrate multiplayer functionality for more interactive gameplay.


15) Conclusion

This README provides a detailed overview of setting up, building, and deploying the GLOBETROTTER Challenge application! 🌍
