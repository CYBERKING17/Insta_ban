"""
Linux-specific functionality
"""

import os
import subprocess

class LinuxUtils:
    @staticmethod
    def is_root():
        """Check if running as root"""
        return os.geteuid() == 0
    
    @staticmethod
    def run_as_root():
        """Restart as root"""
        if not LinuxUtils.is_root():
            os.execvp('sudo', ['sudo', 'python3'] + sys.argv)
    
    @staticmethod
    def set_proxy(proxy_url):
        """Set system proxy (Linux)"""
        try:
            # Set for current session
            os.environ['http_proxy'] = proxy_url
            os.environ['https_proxy'] = proxy_url
            
            # Try to set system-wide (requires root)
            if LinuxUtils.is_root():
                # This would vary by distribution
                # Example for Ubuntu/Debian
                pass
                
            return True
        except:
            return False
    
    @staticmethod
    def get_distribution():
        """Get Linux distribution info"""
        try:
            with open('/etc/os-release', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith('PRETTY_NAME='):
                        return line.split('=')[1].strip().strip('"')
        except:
            pass
        return "Unknown Linux"