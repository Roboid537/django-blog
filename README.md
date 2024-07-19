```markdown
# Django Rest API for Blog
```

## Description

This repo contains a basic implemenation of blog application with features.

1. **User Management**
    - Register user
    - Login/Logout
    - Fetch User
    - Manage Profile
    - Get/Refresh JWT Authentication Token
2. **Posts**
    - Create, Retrieve, Update and Delete Post
    - Create and Retrive Comment
    - Only Authenticate and Authorized user perform CRUD on Post, Comment
    - Like and Dislike post
3. **Additional Feature**
    - Pagination

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. By default it uses sqlite database but you are free
to use any database. Make sure to set respective confiuration in
settings.

### Prerequisites

- **Python:** [https://www.python.org/downloads/](https://www.python.org/downloads/)
- **pip:** (Usually included with Python)
- **Virtual Environment (recommended):** `python -m venv venv` (or use your preferred method)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Roboid537/django-blog.git
   cd django-blog
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate
   # On Windows, use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create Database Migrations:**
   ```bash
   python manage.py makemigrations users posts
   ```

5. **Apply Migrations to the Database:**
   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Your API will typically be accessible at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).


## Testing with Postman

We have provided a Postman collection to help you test the API endpoints.

1. **Import the Collection:**
   - Import the `[Django-Blog.postman_collection.json]` file (located in the root of the repository) into your Postman workspace.

2. **Run the Requests:**
   - Execute the requests within the collection to test the different API endpoints.


## API Documentation


- **Base URL:** e.g., `http://127.0.0.1:8000/`
- **Endpoints:**
    - register/
    - login/
    - token/refresh/
    - logout/
    - "" # for users endpoint
    - profile/
    - post/
