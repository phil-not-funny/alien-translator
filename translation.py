import sys
import os

# Set console to UTF-8 mode
sys.stdout.reconfigure(encoding='utf-8')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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
    print("\nWelcome to Encrypted Alien Language Translator")
    key = input("Enter your encryption key (or press Enter for default): ")
    translator = AlienTranslator(key if key else "default_key")
    
    while True:
        clear_screen()
        print("\nAlien Language Translator")
        print("1. Convert to Encrypted Alien Language")
        print("2. Convert from Encrypted Alien Language")
        print("3. Change Encryption Key")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
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
            new_key = input("\nEnter new encryption key: ").strip()
            translator = AlienTranslator(new_key)
            print("\nEncryption key updated successfully!")
            input("\nPress Enter to continue...")
        
        elif choice == '4':
            clear_screen()
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()