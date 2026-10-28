import hashlib
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

class CryptoVehicleApp:
    def __init__(self):
        self.vehicle_registry = {}
        self.private_key = None
        self.public_key = None
        self.last_signature = None
        self.last_signed_message = None

    def generate_sha256(self, message: str) -> str:
        return hashlib.sha256(message.encode('utf-8')).hexdigest()

    def generate_key_pair(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        self.last_signature = None
        self.last_signed_message = None

    def sign_message(self, message: str) -> bytes:
        if not self.private_key:
            raise ValueError("Keys have not been generated yet!")
        
        self.last_signed_message = message
        self.last_signature = self.private_key.sign(
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return self.last_signature

    def verify_signature(self, message: str, signature: bytes) -> bool:
        if not self.public_key:
            raise ValueError("Keys have not been generated yet!")
        try:
            self.public_key.verify(
                signature,
                message.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False

    def register_vehicle(self, plate: str, owner: str, model: str) -> bool:
        clean_plate = plate.strip().upper()
        if clean_plate in self.vehicle_registry:
            return False
        self.vehicle_registry[clean_plate] = {
            "owner": owner.strip(),
            "model": model.strip()
        }
        return True

    def get_vehicle(self, plate: str):
        return self.vehicle_registry.get(plate.strip().upper())

def main():
    app = CryptoVehicleApp()
    
    while True:
        print("
" + "="*50)
        print("🗳️  CRYPTOGRAPHY & BLOCKCHAIN FUNDAMENTALS APP")
        print("="*50)
        print("1. Generate SHA-256 Hash")
        print("2. Generate Public-Private Key Pair")
        print("3. Sign a Message")
        print("4. Verify Last Signature")
        print("5. Register a Vehicle (Store)")
        print("6. Retrieve Vehicle Details (Get)")
        print("7. Exit")
        print("="*50)
        
        choice = input("Select an option (1-7): ").strip()
        
        if choice == '1':
            msg = input("Enter the text message to hash: ")
            hashed = app.generate_sha256(msg)
            print(f"
[Success] SHA-256 Hash:
{hashed}")
            
        elif choice == '2':
            print("
Generating 2048-bit RSA key pair...")
            app.generate_key_pair()
            print("[Success] Public and Private keys generated successfully!")
            
        elif choice == '3':
            if not app.private_key:
                print("
[Error] Please generate a key pair first (Option 2).")
                continue
            msg = input("Enter the message to digitally sign: ")
            sig = app.sign_message(msg)
            print(f"
[Success] Message signed successfully!")
            print(f"Signature (hex): {sig.hex()[:64]}...")
            
        elif choice == '4':
            if not app.public_key:
                print("
[Error] Keys do not exist. Generate key pair first.")
                continue
            if not app.last_signature:
                print("
[Error] No signature found. Sign a message first (Option 3).")
                continue
            
            print(f"
Verifying signature for the last signed message: '{app.last_signed_message}'")
            is_valid = app.verify_signature(app.last_signed_message, app.last_signature)
            
            if is_valid:
                print("✨ [VALID] The digital signature is authentic and verified!")
            else:
                print("❌ [INVALID] Signature validation failed.")
                
        elif choice == '5':
            plate = input("Enter Car Number Plate: ").strip()
            if not plate:
                print("[Error] Number plate cannot be empty.")
                continue
            owner = input("Enter Owner Name: ").strip()
            model = input("Enter Vehicle Model: ").strip()
            
            success = app.register_vehicle(plate, owner, model)
            if success:
                print(f"
[Success] Vehicle '{plate.upper()}' registered successfully.")
            else:
                print(f"
[Error] Duplicate plate! Vehicle with plate '{plate.upper()}' already exists.")
                
        elif choice == '6':
            plate = input("Enter Number Plate to look up: ").strip()
            details = app.get_vehicle(plate)
            if details:
                print(f"
🚘 Vehicle Details Found for [{plate.upper()}]:")
                print(f"   • Owner: {details['owner']}")
                print(f"   • Model: {details['model']}")
            else:
                print(f"
❌ [Error] Vehicle with number plate '{plate.upper()}' not found in registry.")
                
        elif choice == '7':
            print("
Exiting program. Thank you!")
            break
        else:
            print("
[Invalid Selection] Please choose a number between 1 and 7.")

if __name__ == '__main__':
    main()
