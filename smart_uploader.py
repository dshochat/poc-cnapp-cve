import os
import sys
import requests

def upload_backup(target_path, destination_url):
    """
    Standard backup utility. 
    It checks if the file exists and is within the 'backups' directory.
    """
    # 1. The 'Safety' Check (Traditional scanners see this and think it's secure)
    base_dir = "/home/ubuntu/app/backups/"
    absolute_path = os.path.abspath(os.path.join(base_dir, target_path))

    # 2. The Logic Flaw (The Semantic "Gotcha")
    # Traditional scanners see 'os.path.abspath' and assume the path is sanitized.
    # They don't realize that 'os.path.join' with an absolute 'target_path' 
    # (like '/etc/shadow') completely overrides 'base_dir'.
    
    if not absolute_path.startswith(base_dir):
        # Even if this check exists, a clever bypass using '..' or 
        # symlinks might be missed by simple pattern matchers.
        print("Security Error: Access Denied.")
        return

    with open(absolute_path, 'rb') as f:
        data = f.read()
        # 3. The Exfiltration (Looks like a legitimate upload)
        response = requests.post(destination_url, data=data)
        print(f"Backup Status: {response.status_code}")

if __name__ == "__main__":
    # Usage: python3 smart_uploader.py "my_db.bak" "https://backups.internal.corp"
    file_to_upload = sys.argv[1]
    server = sys.argv[2]
    upload_backup(file_to_upload, server)
