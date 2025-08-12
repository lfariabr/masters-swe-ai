#!/usr/bin/env python3
"""
Simple .env encryption script for TTrack v3.9.0
Run this before building the executable to encrypt credentials.
"""

from cryptography.fernet import Fernet
import os

# Hardcoded encryption key - generated once for this project
# To generate a new key: print(Fernet.generate_key())
ENCRYPTION_KEY = b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='

def encrypt_env():
    """Encrypt .env file to .env.enc for secure bundling"""
    
    if not os.path.exists('.env'):
        print("❌ Error: .env file not found!")
        print("   Make sure you have a .env file in the project root.")
        return False
    
    try:
        cipher = Fernet(ENCRYPTION_KEY)
        
        # Read .env file
        with open('.env', 'rb') as f:
            env_data = f.read()
        
        # Encrypt the data
        encrypted_data = cipher.encrypt(env_data)
        
        # Write encrypted data to .env.enc
        with open('.env.enc', 'wb') as f:
            f.write(encrypted_data)
        
        print("✅ Successfully encrypted .env to .env.enc")
        print(f"   Original size: {len(env_data)} bytes")
        print(f"   Encrypted size: {len(encrypted_data)} bytes")
        return True
        
    except Exception as e:
        print(f"❌ Error encrypting .env: {e}")
        return False

def verify_encryption():
    """Verify that encryption/decryption works correctly"""
    
    if not os.path.exists('.env.enc'):
        print("❌ No .env.enc file found to verify")
        return False
    
    try:
        cipher = Fernet(ENCRYPTION_KEY)
        
        # Read encrypted file
        with open('.env.enc', 'rb') as f:
            encrypted_data = f.read()
        
        # Decrypt and verify
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # Read original for comparison
        with open('.env', 'rb') as f:
            original_data = f.read()
        
        if decrypted_data == original_data:
            print("✅ Encryption verification successful")
            return True
        else:
            print("❌ Encryption verification failed - data mismatch")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying encryption: {e}")
        return False

if __name__ == "__main__":
    print("🔐 TTrack Environment Encryption Tool")
    print("=" * 40)
    
    # Encrypt the .env file
    if encrypt_env():
        # Verify the encryption worked
        verify_encryption()
        print("\n📦 Ready for build! Use .env.enc in your PyInstaller spec.")
    else:
        print("\n❌ Encryption failed. Check your .env file and try again.")
