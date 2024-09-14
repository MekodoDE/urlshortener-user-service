# User Service

## Description

The User Service is a component of the larger web application that provides user authentication, registration, and management functionalities. It is responsible for handling user-related operations such as user login, logout, registration, profile updates, and password changes.

## Features

- **User Authentication**:
  - Users can securely authenticate themselves using their credentials (username/email and password).
  - Sessions and tokens are used to manage user authentication state.

- **User Registration**:
  - New users can register for an account by providing necessary information such as username, email, and password.
  - Email verification process is implemented to ensure the validity of user accounts.

- **User Management**:
  - Authenticated users can manage their profiles, including updating profile information and changing passwords.
  - Administrators have additional privileges to manage user accounts, such as activating/deactivating accounts and assigning roles.

## Technologies Used

- **Backend**:
  - Flask (Python) for building the user service.
  - SQLAlchemy for database management.
  - Flask-Smorest for building RESTful APIs.
  - Marshmallow for object serialization/deserialization.
  - Flask-CORS for Cross-Origin Resource Sharing.

- **Database**:
  - SQLite for storing user data.

## Installation and Setup

1. **Clone the Repository**:
   - Clone the user service repository to your local machine.

2. **Install Dependencies**:
   - Navigate to the project directory and install dependencies using `pip install -r requirements.txt`.

3. **Configure Environment Variables**:
   - Set up environment variables for configuration, such as database connection details and secret keys.

4. **Run the User Service**:
   - Run the Flask application using `python app.py`.
   - The user service should now be running and accessible at the specified endpoints.
