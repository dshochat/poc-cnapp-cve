# sync_tool.py (The "Poisoned" Script)
import os
import sys

def sync_logs(target_file):
    # LOGIC FLAW: User-controlled input directly used in file path
    # No CVE exists for this custom code.
    source_dir = "/var/log/app/"
    full_path = os.path.join(source_dir, target_file)
    
    print(f"Syncing file: {full_path}")
    with open(full_path, 'rb') as f:
        data = f.read()
        # Simulate exfiltration to an unapproved IP
        print("Sending data to 1.1.1.1...") 

if __name__ == "__main__":
    sync_logs(sys.argv[1])
