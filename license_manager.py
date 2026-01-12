import json
import hashlib
import base64
from datetime import datetime, timedelta
import os

class LicenseManager:
    def __init__(self, license_file="license.key"):
        self.license_file = license_file
        self.license_data = self.load_license()
    
    def generate_hash(self, data):
        """Generate SHA-256 hash"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def generate_trial_license(self):
        """Generate a 7-day trial license"""
        if os.path.exists(self.license_file):
            return False
        
        expiry_date = datetime.now() + timedelta(days=7)
        license_data = {
            "type": "trial",
            "expiry": expiry_date.isoformat(),
            "activated": datetime.now().isoformat(),
            "usage_count": 0,
            "max_accounts": 50
        }
        
        license_key = self.generate_hash(
            f"TRIAL-{expiry_date.isoformat()}-{os.urandom(8).hex()}"
        )
        
        license_data["key"] = license_key
        
        with open(self.license_file, 'w') as f:
            json.dump(license_data, f, indent=4)
        
        self.license_data = license_data
        return True
    
    def activate_license(self, license_key):
        """Activate a paid license"""
        # This is a simplified version
        # In real implementation, you would validate against a server
        
        if not license_key or len(license_key) != 64:
            return False
        
        # Simulate license validation
        if license_key.startswith("PAID-"):
            expiry_date = datetime.now() + timedelta(days=365)
            license_data = {
                "type": "paid",
                "key": license_key,
                "expiry": expiry_date.isoformat(),
                "activated": datetime.now().isoformat(),
                "usage_count": 0,
                "max_accounts": 1000
            }
            
            with open(self.license_file, 'w') as f:
                json.dump(license_data, f, indent=4)
            
            self.license_data = license_data
            return True
        
        return False
    
    def load_license(self):
        """Load license from file"""
        try:
            with open(self.license_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Generate trial if no license exists
            self.generate_trial_license()
            with open(self.license_file, 'r') as f:
                return json.load(f)
    
    def validate_license(self):
        """Check if license is valid"""
        if not self.license_data:
            return False
        
        expiry_date = datetime.fromisoformat(self.license_data['expiry'])
        if datetime.now() > expiry_date:
            return False
        
        return True
    
    def get_license_status(self):
        """Get license status as string"""
        if not self.license_data:
            return "No License"
        
        if not self.validate_license():
            return "Expired"
        
        return f"{self.license_data['type'].title()} (Active)"
    
    def get_expiry_date(self):
        """Get license expiry date"""
        if not self.license_data:
            return "N/A"
        
        expiry_date = datetime.fromisoformat(self.license_data['expiry'])
        return expiry_date.strftime("%Y-%m-%d")
    
    def get_usage_count(self):
        """Get number of accounts reported"""
        if not self.license_data:
            return 0
        
        return self.license_data.get('usage_count', 0)
    
    def increment_usage(self):
        """Increment usage counter"""
        if not self.license_data:
            return
        
        self.license_data['usage_count'] = self.get_usage_count() + 1
        
        with open(self.license_file, 'w') as f:
            json.dump(self.license_data, f, indent=4)
    
    def reset_usage(self):
        """Reset usage counter"""
        if not self.license_data:
            return
        
        self.license_data['usage_count'] = 0
        
        with open(self.license_file, 'w') as f:
            json.dump(self.license_data, f, indent=4)