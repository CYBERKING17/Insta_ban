import os
import sys
import platform
import socket

def get_platform_info():
    """Get detailed platform information"""
    system = platform.system()
    
    info = {
        'os': system,
        'version': platform.version(),
        'architecture': platform.machine(),
        'python_version': platform.python_version(),
        'hostname': socket.gethostname()
    }
    
    # Get IP address
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        info['ip'] = s.getsockname()[0]
        s.close()
    except:
        info['ip'] = '127.0.0.1'
    
    # Detect specific Linux distributions
    if system == "Linux":
        try:
            with open('/etc/os-release', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith('PRETTY_NAME='):
                        info['os'] = line.split('=')[1].strip().strip('"')
                        break
        except:
            pass
        
        # Check if Kali
        if 'kali' in info['os'].lower():
            info['os'] = 'Kali Linux'
    
    return info

def clear_screen():
    """Clear terminal screen"""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux/Mac
        os.system('clear')

def display_banner():
    """Display application banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║    ██╗███╗   ██╗███████╗████████╗ █████╗  ██████╗        ║
    ║    ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝        ║
    ║    ██║██╔██╗ ██║███████╗   ██║   ███████║██║             ║
    ║    ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║             ║
    ║    ██║██║ ╚████║███████║   ██║   ██║  ██║╚██████╗        ║
    ║    ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝        ║
    ║                                                           ║
    ║          ACCOUNT REPORTER - CROSS PLATFORM TOOL          ║
    ║               For Educational Purposes Only              ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if all dependencies are installed"""
    required = ['requests', 'fake-useragent']
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    return missing

def setup_directories():
    """Create necessary directories"""
    directories = ['logs', 'exports', 'config']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)