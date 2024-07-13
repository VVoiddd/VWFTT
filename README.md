# VWFTT (VoidWare-File-Transfer-Tool)

## Overview
VWFTT is a peer-to-peer file transfer tool that allows users to upload MP4 files securely to a server. The tool provides a web interface for users to sign up, log in, and upload files. The uploads are stored in a directory, and the tool lists recently transferred files with details like the filename, upload time, and the uploader's username.

## Features
- User registration and login with secure password hashing.
- Dark, user-friendly interface.
- File upload functionality with secure server credentials.
- List of recently transferred files with upload details.
- Secure storage of user information in an unreadable format.

## Installation

### Prerequisites
- Python 3.x
- Flask
- Bootstrap

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/VVoiddd/VWPTPFTT.git
    ```

2. Navigate to the project directory:
    ```bash
    cd VWPTPFTT
    ```

3. Install the required Python packages:
    ```bash
    pip install flask
    ```

4. Run the `install.bat` script:
    ```bash
    .\install.bat
    ```

5. Start the application by running the `start.bat` script:
    ```bash
    .\start.bat
    ```

## Usage
- Open your web browser and navigate to `http://YourIP:5000/`.
- Sign up for a new account or log in with an existing account.
- Upload MP4 files using the provided form.
- View the list of recently transferred files on the upload page.

## Notes
- Make sure the server IP and port are correctly set in the `upload.html` template.
- Ensure the `uploads` directory exists or is created by the application.
- Update the `PASSWORD` variable in `app.py` with your own secure password.
