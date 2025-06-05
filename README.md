# Google2FA Login Example

This repository contains a minimal Flask application demonstrating how to implement login with Google Authenticator two-factor authentication (2FA).

## Setup

1. Ensure you have Python 3 installed.
2. Install the required packages:
   ```bash
   pip install -r app/requirements.txt
   ```
3. Run the application:
   ```bash
   python app/app.py
   ```
4. Open your browser at `http://localhost:5000`.

## Usage

- Login using the default credentials:
  - **Username:** `user1`
  - **Password:** `password`
- After submitting the credentials, a QR code will be displayed. Scan it with Google Authenticator and enter the generated code to complete the login.

This example uses an in-memory user store for simplicity.
