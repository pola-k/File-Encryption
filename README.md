# SecureDoc

SecureDoc is a web application that allows users to securely encrypt and decrypt various types of files, including text-based documents (.doc, .docx, .pdf, .txt) and images, using Advanced Encryption Standard (AES) encryption. The application ensures that only those with the correct decryption key can access the original content, providing a secure method for protecting sensitive information before sharing or storing it.

## Features

- Upload and encrypt text-based documents and images.
- Download the encrypted file along with the decryption key.
- Decrypt previously encrypted files using the correct key.
- Error handling for incorrect decryption keys.

## Installation

To run the SecureDoc web application, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/pola-k/SecureDoc.git
   ```

2. Navigate to the project directory:
   ```bash
   cd SecureDoc
   ```

3. Run the application:
   ```bash
   python run.py
   ```

4. Open your web browser and go to `http://localhost:5000` to access the application.

## Usage

- **Encrypting Files**: 
  - Select a file to encrypt and click the "Encrypt" button. 
  - The application will generate an encrypted file and a decryption key for download.

- **Decrypting Files**: 
  - Select the encrypted file and the corresponding decryption key file, then click the "Decrypt" button. 
  - If the key is correct, the original file will be decrypted.

## Error Handling

- If an incorrect decryption key is provided, the application will raise an error, notifying the user that the key is invalid.

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to report issues, please open an issue or submit a pull request.
