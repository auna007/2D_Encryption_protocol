import pyotp
import qrcode
import os

def generate_qrcode(secret_key, email):
    # Generate the TOTP URI
    totp = pyotp.TOTP(secret_key)
    uri = totp.provisioning_uri(name=email, issuer_name="2D Encryption/Decryption")

    # Generate QR code
    qr = qrcode.make(uri)

    # Create the directory if it doesn't exist
    if not os.path.exists('qrcode_images'):
        os.makedirs('qrcode_images')

    # Save the QR code image with the email as the filename
    file_path = os.path.join('qrcode_images', f'{email}.png')
    qr.save(file_path)
    print(f"QR code saved as {file_path}")

if __name__ == "__main__":
    secret_key = input("Enter your secret key: ")
    email = input("Enter your email: ")

    generate_qrcode(secret_key, email)
