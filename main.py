#!/usr/bin/env python3
"""
Instagram Account Reporter - Cross Platform Tool
Works on Windows, Ubuntu, and Kali Linux
"""

import os
import sys
import argparse
import hashlib
import json
from datetime import datetime
from license_manager import LicenseManager
from reporter import InstagramReporter
from utils import get_platform_info, clear_screen, display_banner

class InstagramAccountReporter:
    def __init__(self):
        self.platform = get_platform_info()
        self.license_manager = LicenseManager()
        self.reporter = InstagramReporter()
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Default configuration
            config = {
                "api_settings": {
                    "max_reports_per_day": 10,
                    "delay_between_reports": 5,
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
                "license_settings": {
                    "trial_days": 7,
                    "max_accounts": 50
                }
            }
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
            return config
    
    def display_menu(self):
        """Display main menu"""
        clear_screen()
        display_banner()
        
        print(f"\n{'='*60}")
        print(f"Platform: {self.platform['os']} {self.platform['version']}")
        print(f"License Status: {self.license_manager.get_license_status()}")
        print(f"{'='*60}\n")
        
        print("1. Report Instagram Account")
        print("2. Batch Report Multiple Accounts")
        print("3. Check Report Status")
        print("4. License Management")
        print("5. Platform Information")
        print("6. Settings")
        print("7. Exit")
        
        choice = input("\nSelect option (1-7): ").strip()
        return choice
    
    def report_account_menu(self):
        """Menu for reporting single account"""
        clear_screen()
        print("\n" + "="*60)
        print("REPORT INSTAGRAM ACCOUNT")
        print("="*60)
        
        username = input("\nEnter Instagram username to report: ").strip()
        if not username:
            print("Username cannot be empty!")
            input("\nPress Enter to continue...")
            return
        
        print("\nSelect report reason:")
        print("1. Spam")
        print("2. Fake Account")
        print("3. Harassment")
        print("4. Hate Speech")
        print("5. Nudity")
        print("6. Violence")
        print("7. Intellectual Property Violation")
        print("8. Self Harm")
        print("9. Scam")
        print("10. Other")
        
        reason_choice = input("\nSelect reason (1-10): ").strip()
        reasons = {
            '1': 'Spam', '2': 'Fake Account', '3': 'Harassment',
            '4': 'Hate Speech', '5': 'Nudity', '6': 'Violence',
            '7': 'Intellectual Property Violation', '8': 'Self Harm',
            '9': 'Scam', '10': 'Other'
        }
        
        reason = reasons.get(reason_choice, 'Other')
        additional_info = input("\nAdditional information (optional): ").strip()
        
        print(f"\nReporting @{username} for {reason}...")
        
        # Check license validity
        if not self.license_manager.validate_license():
            print("License expired or invalid!")
            input("\nPress Enter to continue...")
            return
        
        # Perform report
        success = self.reporter.report_account(
            username=username,
            reason=reason,
            platform=self.platform['os'],
            additional_info=additional_info
        )
        
        if success:
            print(f"✓ Successfully reported @{username}")
            self.license_manager.increment_usage()
        else:
            print(f"✗ Failed to report @{username}")
        
        input("\nPress Enter to continue...")
    
    def batch_report_menu(self):
        """Menu for batch reporting"""
        clear_screen()
        print("\n" + "="*60)
        print("BATCH REPORT MULTIPLE ACCOUNTS")
        print("="*60)
        
        print("\nEnter usernames (one per line). Type 'DONE' when finished:")
        usernames = []
        while True:
            username = input().strip()
            if username.upper() == 'DONE':
                break
            if username:
                usernames.append(username)
        
        if not usernames:
            print("No usernames provided!")
            input("\nPress Enter to continue...")
            return
        
        reason = input("\nEnter report reason for all accounts: ").strip()
        
        print(f"\nPreparing to report {len(usernames)} accounts...")
        
        # Check license
        if not self.license_manager.validate_license():
            print("License expired or invalid!")
            input("\nPress Enter to continue...")
            return
        
        # Check usage limits
        if self.license_manager.get_usage_count() + len(usernames) > self.config['license_settings']['max_accounts']:
            print(f"Exceeds maximum account limit ({self.config['license_settings']['max_accounts']})!")
            input("\nPress Enter to continue...")
            return
        
        success_count = 0
        for i, username in enumerate(usernames, 1):
            print(f"\n[{i}/{len(usernames)}] Reporting @{username}...")
            
            success = self.reporter.report_account(
                username=username,
                reason=reason,
                platform=self.platform['os']
            )
            
            if success:
                success_count += 1
                self.license_manager.increment_usage()
            
            # Delay between reports
            if i < len(usernames):
                import time
                time.sleep(self.config['api_settings']['delay_between_reports'])
        
        print(f"\n✓ Successfully reported {success_count}/{len(usernames)} accounts")
        input("\nPress Enter to continue...")
    
    def license_menu(self):
        """License management menu"""
        clear_screen()
        print("\n" + "="*60)
        print("LICENSE MANAGEMENT")
        print("="*60)
        
        print("\n1. Enter License Key")
        print("2. Generate Trial License")
        print("3. Check License Status")
        print("4. Back to Main Menu")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            license_key = input("\nEnter license key: ").strip()
            if self.license_manager.activate_license(license_key):
                print("✓ License activated successfully!")
            else:
                print("✗ Invalid license key!")
        
        elif choice == '2':
            if self.license_manager.generate_trial_license():
                print("✓ Trial license generated!")
                print(f"Expires: {self.license_manager.get_expiry_date()}")
            else:
                print("✗ Trial already used or error occurred!")
        
        elif choice == '3':
            status = self.license_manager.get_license_status()
            expiry = self.license_manager.get_expiry_date()
            usage = self.license_manager.get_usage_count()
            
            print(f"\nLicense Status: {status}")
            print(f"Expiry Date: {expiry}")
            print(f"Accounts Reported: {usage}/{self.config['license_settings']['max_accounts']}")
        
        input("\nPress Enter to continue...")
    
    def platform_info_menu(self):
        """Display platform information"""
        clear_screen()
        print("\n" + "="*60)
        print("PLATFORM INFORMATION")
        print("="*60)
        
        print(f"\nOperating System: {self.platform['os']}")
        print(f"Version: {self.platform['version']}")
        print(f"Architecture: {self.platform['architecture']}")
        print(f"Python Version: {self.platform['python_version']}")
        print(f"Hostname: {self.platform.get('hostname', 'N/A')}")
        print(f"IP Address: {self.platform.get('ip', 'N/A')}")
        
        input("\nPress Enter to continue...")
    
    def settings_menu(self):
        """Settings menu"""
        clear_screen()
        print("\n" + "="*60)
        print("SETTINGS")
        print("="*60)
        
        print(f"\nCurrent Settings:")
        print(f"Max Reports Per Day: {self.config['api_settings']['max_reports_per_day']}")
        print(f"Delay Between Reports: {self.config['api_settings']['delay_between_reports']} seconds")
        print(f"Max Accounts: {self.config['license_settings']['max_accounts']}")
        
        print("\n1. Change Delay Between Reports")
        print("2. Change Max Reports Per Day")
        print("3. Reset Usage Counter")
        print("4. Back to Main Menu")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            try:
                delay = int(input("Enter new delay (seconds): "))
                if 1 <= delay <= 60:
                    self.config['api_settings']['delay_between_reports'] = delay
                    with open('config.json', 'w') as f:
                        json.dump(self.config, f, indent=4)
                    print("✓ Delay updated!")
                else:
                    print("✗ Delay must be between 1 and 60 seconds")
            except ValueError:
                print("✗ Invalid input!")
        
        elif choice == '2':
            try:
                max_reports = int(input("Enter new max reports per day: "))
                if 1 <= max_reports <= 100:
                    self.config['api_settings']['max_reports_per_day'] = max_reports
                    with open('config.json', 'w') as f:
                        json.dump(self.config, f, indent=4)
                    print("✓ Max reports updated!")
                else:
                    print("✗ Must be between 1 and 100")
            except ValueError:
                print("✗ Invalid input!")
        
        elif choice == '3':
            confirm = input("Are you sure? (yes/no): ").strip().lower()
            if confirm == 'yes':
                self.license_manager.reset_usage()
                print("✓ Usage counter reset!")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop"""
        while True:
            choice = self.display_menu()
            
            if choice == '1':
                self.report_account_menu()
            elif choice == '2':
                self.batch_report_menu()
            elif choice == '3':
                print("\nFeature coming soon!")
                input("\nPress Enter to continue...")
            elif choice == '4':
                self.license_menu()
            elif choice == '5':
                self.platform_info_menu()
            elif choice == '6':
                self.settings_menu()
            elif choice == '7':
                print("\nThank you for using Instagram Account Reporter!")
                break
            else:
                print("\nInvalid option!")
                input("\nPress Enter to continue...")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Instagram Account Reporter')
    parser.add_argument('--username', help='Instagram username to report')
    parser.add_argument('--reason', help='Report reason')
    parser.add_argument('--batch', help='File containing usernames to report')
    parser.add_argument('--license', help='License key')
    
    args = parser.parse_args()
    
    app = InstagramAccountReporter()
    
    # Check or activate license via command line
    if args.license:
        if app.license_manager.activate_license(args.license):
            print("License activated successfully!")
        else:
            print("Invalid license key!")
            sys.exit(1)
    
    # Command line reporting
    if args.username:
        if not app.license_manager.validate_license():
            print("License required!")
            sys.exit(1)
        
        success = app.reporter.report_account(
            username=args.username,
            reason=args.reason or 'Spam',
            platform=get_platform_info()['os']
        )
        
        if success:
            print(f"Successfully reported @{args.username}")
            app.license_manager.increment_usage()
        else:
            print(f"Failed to report @{args.username}")
    
    # Batch reporting from file
    elif args.batch:
        if not app.license_manager.validate_license():
            print("License required!")
            sys.exit(1)
        
        try:
            with open(args.batch, 'r') as f:
                usernames = [line.strip() for line in f if line.strip()]
            
            reason = args.reason or 'Spam'
            success_count = 0
            
            for username in usernames:
                success = app.reporter.report_account(
                    username=username,
                    reason=reason,
                    platform=get_platform_info()['os']
                )
                
                if success:
                    success_count += 1
                    app.license_manager.increment_usage()
            
            print(f"Successfully reported {success_count}/{len(usernames)} accounts")
        
        except FileNotFoundError:
            print(f"File not found: {args.batch}")
            sys.exit(1)
    
    # Interactive mode
    else:
        app.run()

if __name__ == "__main__":
    main()