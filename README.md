# Algonova Backend

Welcome to the Algonova Backend repository. This project is the server-side application for the Algonova platform, a robust system designed for educational purposes. It handles student management, lessons, groups, and feedback, built with Django and Django REST Framework.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Running the Application](#running-the-application)
  - [Running the Django Server](#running-the-django-server)
  - [Running Celery for Asynchronous Tasks](#running-celery-for-asynchronous-tasks)
- [API Endpoints](#api-endpoints)
- [Important Notice: Development vs. Production](#important-notice-development-vs-production)

## Features

This backend provides a comprehensive set of features to power an educational application:

*   **Student Management**: Full CRUD (Create, Read, Update, Delete) operations for student profiles.
*   **Lesson Management**: Functionality to create and manage educational lessons.
*   **Group Management**: Ability to organize students into groups or classes.
*   **Feedback System**: Collect and manage feedback, likely for lessons or student performance.
*   **Secure Authentication**: Uses JSON Web Tokens (JWT) for securing API endpoints.
*   **Asynchronous PDF Generation**: Generates PDF documents (e.g., reports, certificates) asynchronously to avoid blocking API requests. This is handled by Celery and WeasyPrint.

## Technology Stack

*   **Backend Framework**: [Django](https://www.djangoproject.com/)
*   **API Framework**: [Django REST Framework](https://www.django-rest-framework.org/)
*   **Asynchronous Tasks**: [Celery](https://docs.celeryq.dev/en/stable/)
*   **Message Broker**: [Redis](https://redis.io/) (used for Celery queue)
*   **Authentication**: [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
*   **PDF Generation**: [WeasyPrint](https://weasyprint.org/)
*   **Database**: Configured for SQLite (development), easily switchable to PostgreSQL or others for production.

## Project Structure

The project is organized into several Django apps, each responsible for a specific domain:

```
Algonova_Backend/
├── Algonova_Backend/   # Core project configuration
├── students/           # Handles student-related logic and API endpoints
├── lessons/            # Manages lessons and content
├── groups/             # Manages student groups
├── feedbacks/          # Handles feedback submission and retrieval
├── utils/              # Shared utility functions and helpers
├── templates/          # HTML templates, e.g., for PDF generation
└── requirements.txt    # Project dependencies
```

## Getting Started

Follow these instructions to get a local copy of the project up and running for development and testing.

### Prerequisites

Make sure you have the following installed on your system:

*   [Python 3.8+](https://www.python.org/downloads/)
*   [Git](https://git-scm.com/)
*   [Redis](https://redis.io/docs/getting-started/installation/)
*   **WeasyPrint Dependencies**: WeasyPrint requires the installation of Pango, Cairo, and GDK-PixBuf. Please follow the specific instructions for your operating system:
    *   **Windows**: [WeasyPrint on Windows](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows)
    *   **macOS**: `brew install pango cairo libffi`
    *   **Linux (Debian/Ubuntu)**: `sudo apt-get install python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info`

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/Algonova_Backend.git
    cd Algonova_Backend
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install project dependencies:**
    All required Python packages are listed in the `requirements.txt` file.
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the project root directory. You can copy the example file:
    ```sh
    cp .env.example .env
    ```
    Now, open the `.env` file and fill in the required values, especially `SECRET_KEY`.

5.  **Apply database migrations:**
    ```sh
    python manage.py migrate
    ```

## Running the Application

For the application to run fully, you need to start the Redis server, the Django development server, and the Celery worker.

### Running the Django Server

Start the development server on `http://127.0.0.1:8000/`:
```sh
python manage.py runserver
```

### Running Celery for Asynchronous Tasks

First, ensure your Redis server is running. If you installed it locally, you can typically start it with `redis-server`.

If you don't have redis server, just make sure you have Docker or Docker Desktop and pull redis docker images with `docker run -d -p 6379:6379 redis:7-alpine`.

Then, open a **new terminal window**, activate the virtual environment, and start the Celery worker:
```sh
celery -A Algonova_Backend worker -l info -P eventlet
```
This worker will listen for tasks, such as PDF generation, and execute them in the background.

## API Endpoints

The API endpoints are managed by Django REST Framework. Once the server is running, you can explore the available endpoints through the browsable API, typically starting at `http://127.0.0.1:8000/api/`.

## Important Notice: Development vs. Production

This project is configured for a **development environment**. The use of Celery with Redis for asynchronous PDF generation is a powerful feature, but it may not be supported by all hosting providers, especially those that do not offer shell access or support for running background services like Celery workers.

If you plan to deploy this application to a hosting provider that does not support Python backends or background workers, you will need to significantly refactor the application. This might involve:
1.  Switching to a synchronous approach for PDF generation, which could lead to longer API response times.
2.  Deploying the backend to a different, more capable hosting service (like Heroku, AWS, DigitalOcean) that provides the necessary infrastructure.

This `README.md` should give any developer a clear understanding of your project's purpose, architecture, and how to get it running. Let me know if you'd like any adjustments!

