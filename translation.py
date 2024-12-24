import sys
import os
import re
import time
import json
from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# Set console to UTF-8 mode
sys.stdout.reconfigure(encoding='utf-8')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def confirm_action(prompt):
    while True:
        choice = input(prompt + " (yes/no): ").strip().lower()
        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n']:
            return False
        else:
            print("\nInvalid choice. Please try again.")

class KeyManager:
    def __init__(self, storage_file='key_storage.enc'):
        self.storage_file = storage_file
        self.master_key = self._get_or_create_master_key()
        self.fernet = Fernet(self.master_key)
    
    def _get_or_create_master_key(self):
        # Create a master key for encrypting stored keys
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'static_salt',  # In production, use a random salt
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(b"master_password"))  # In production, use a secure master password
        return key
    
    def save_key(self, key):
        encrypted_data = self.fernet.encrypt(json.dumps({"key": key}).encode())
        with open(self.storage_file, 'wb') as f:
            f.write(encrypted_data)
    
    def load_key(self):
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = self.fernet.decrypt(encrypted_data)
                return json.loads(decrypted_data)["key"]
        except Exception:
            return None
        return None

class AlienTranslator:
    def __init__(self, key="default_key"):
        self.key = key
        self.key_sum = sum(ord(c) for c in key)  # Use key to create a shift value
        self.ascii_to_alien = {
            chr(i): chr((i + 8000 + self.key_sum) % 65535) for i in range(32, 127)
        }
        self.alien_to_ascii = {v: k for k, v in self.ascii_to_alien.items()}
    
    def to_alien(self, text):
        """Convert Text to alien language"""
        return ''.join(self.ascii_to_alien.get(c, c) for c in text)
    
    def from_alien(self, alien_text):
        """Convert alien language back to Text"""
        return ''.join(self.alien_to_ascii.get(c, c) for c in alien_text)

def main():
    clear_screen()
    print("\n=== Welcome to Encrypted Alien Language Translator ===")
    print("Each message is uniquely encrypted using your secret key!")
    
    # Initialize key manager
    key_manager = KeyManager()
    last_key = key_manager.load_key()
    
    # Secure key input
    try:
        if last_key:
            use_last_key = confirm_action("Would you like to use your last encryption key?")
            if use_last_key:
                key = last_key
            else:
                key = getpass("\nEnter your encryption key (or press Enter for default): ")
        else:
            key = getpass("\nEnter your encryption key (or press Enter for default): ")
        
        if key != "default_key":  # Only confirm if not using default key
            confirm_key = getpass("Confirm your encryption key: ")
            if key != confirm_key:
                raise ValueError("Keys do not match!")
        
        translator = AlienTranslator(key)
        key_manager.save_key(key)  # Save the key securely
        
    except ValueError as e:
        print(f"\nError setting up key: {e}")
        input("\nPress Enter to try again...")
        return
    
    while True:
        clear_screen()
        print("\n=== Alien Language Translator ===")
        print(f"Current key: {'*' * len(translator.key)}")
        print("\n1. Convert to Encrypted Alien Language")
        print("2. Convert from Encrypted Alien Language")
        print("3. Change Encryption Key")
        print("4. Clear Screen")
        print("5. Exit")
        
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                clear_screen()
                text = input("\nEnter text to convert to alien language: ").strip()
                if text:
                    alien_text = translator.to_alien(text)
                    print("\nEncrypted alien text:", alien_text)
                    input("\nPress Enter to continue...")
                else:
                    print("\nError: Please enter some text to encrypt!")
                    input("\nPress Enter to continue...")
            
            elif choice == '2':
                clear_screen()
                alien_text = input("\nEnter encrypted alien text to convert back: ").strip()
                if alien_text:
                    try:
                        decoded_text = translator.from_alien(alien_text)
                        print("\nDecoded text:", decoded_text)
                        input("\nPress Enter to continue...")
                    except KeyError:
                        print("\nError: Invalid alien text or wrong encryption key!")
                        input("\nPress Enter to continue...")
                else:
                    print("\nError: Please enter some alien text to decrypt!")
                    input("\nPress Enter to continue...")
            
            elif choice == '3':
                clear_screen()
                if confirm_action("Are you sure you want to change the encryption key?"):
                    try:
                        new_key = getpass("\nEnter new encryption key: ")
                        confirm_key = getpass("Confirm new encryption key: ")
                        
                        if new_key != confirm_key:
                            raise ValueError("Keys do not match!")
                            
                        translator = AlienTranslator(new_key)
                        key_manager.save_key(new_key)  # Save the new key securely
                        print("\nEncryption key updated and saved successfully!")
                    except ValueError as e:
                        print(f"\nError: {e}")
                input("\nPress Enter to continue...")
            
            elif choice == '4':
                clear_screen()
            
            elif choice == '5':
                clear_screen()
                print("\nGoodbye!")
                break
            
            else:
                print("\nInvalid choice. Please try again.")
                input("\nPress Enter to continue...")
        
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
