from flask import Flask, request, render_template, Blueprint, send_file, redirect, url_for, flash
from cryptography.fernet import Fernet, InvalidToken
import os
from io import BytesIO
import zipfile

main = Blueprint('main', __name__)

def is_binary_file(data):
    return b'\x00' in data or any(c < 32 or c > 126 for c in data)

def encrypt_file(file_data, filename):
    key = Fernet.generate_key()
    f = Fernet(key)

    encrypted_data = f.encrypt(file_data)

    encrypted_file = BytesIO()

    encrypted_file.write(f"{filename}\n".encode())  
    encrypted_file.write(encrypted_data)

    encrypted_file.seek(0)

    return encrypted_file, key

def decrypt_file(encrypted_data, key):
    f = Fernet(key)
    try:
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data
    except InvalidToken:
        return None

@main.route('/')
def index():
    return render_template('upload.html')

@main.route('/upload_encrypt', methods=['POST'])
def upload_encrypt():
    if 'file' not in request.files:
        flash("No file uploaded", "error")
        return redirect(url_for('main.index'))

    file = request.files['file']
    if not file:
        flash("Uploaded file could not be read.", "error")
        return redirect(url_for('main.index'))

    file_data = file.read()
    encrypted_file, key = encrypt_file(file_data, file.filename)

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr(f"{os.path.splitext(file.filename)[0]}.enc", encrypted_file.getvalue())
        zip_file.writestr('key.key', key)

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name=f'{os.path.splitext(file.filename)[0]}_encrypted.zip',
        mimetype='application/zip'
    )

@main.route('/upload_decrypt', methods=['POST'])
def upload_decrypt():
    if 'file' not in request.files:
        flash("Decryption file not uploaded", "error")
        return redirect(url_for('main.index'))

    if 'key' not in request.files:
        flash("Decryption key not uploaded", "error")
        return redirect(url_for('main.index'))

    encrypted_file = request.files['file']
    key_file = request.files['key']

    if not encrypted_file or encrypted_file.filename == '':
        flash("Decryption file is missing or not properly uploaded.", "error")
        return redirect(url_for('main.index'))

    if not key_file or key_file.filename == '':
        flash("Decryption key is missing or not properly uploaded.", "error")
        return redirect(url_for('main.index'))

    try:
        encrypted_file_lines = encrypted_file.read().split(b'\n', 1)
        if len(encrypted_file_lines) < 2:
            flash("Invalid encrypted file format.", "error")
            return redirect(url_for('main.index'))

        original_file_name = encrypted_file_lines[0].decode().strip()
        encrypted_file_data = encrypted_file_lines[1] 

    except Exception as e:
        flash(f"Error processing encrypted file: {str(e)}", "error")
        return redirect(url_for('main.index'))

    key_data = key_file.read()

    decrypted_data = decrypt_file(encrypted_file_data, key_data)
    if decrypted_data is None:
        flash("Decryption failed: Invalid key or corrupted data.", "error")
        return redirect(url_for('main.index'))

    decrypted_file = BytesIO()
    decrypted_file.write(decrypted_data)
    decrypted_file.seek(0)

    return send_file(
        decrypted_file,
        as_attachment=True,
        download_name=original_file_name
    )