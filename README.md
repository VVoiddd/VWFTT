# VWPTPFTT - VoidWare-Peer-To-Peer-File-Transfer-Tool

VWPTPFTT is a simple tool for securely transferring MP4 files over the network. It allows users to upload MP4 files to a designated server IP and port with authentication.

## Features

- Secure MP4 file upload with server IP, port, and password authentication.
- Automatically creates an `uploads` folder if it doesn't exist.
- Lists recently transferred files with timestamps.
- User signup functionality with email and password storage (hashed for security).

## Installation

1. Clone this repository.
2. Ensure Python 3.x is installed.
3. Install dependencies: `pip install flask`.
4. Run the application: `python app.py`.
5. Access the application via `http://192.168.68.101:5000`.

## Usage

- Open the provided link in your web browser.
- Enter the server IP, port, password, and select an MP4 file to upload.
- Click "Upload" to transfer the file securely.
- Check the list of recently transferred files for upload timestamps.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
