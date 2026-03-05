import os
import sys

"""
Logic Gate v2.0
Description: Filters access based on authorized IP ranges. 
Only allows 'admin' to view logs.
"""

def verify_and_read(user_type, file_path):
    # THE LIE: Claims to check user_type, but actually just uses it in a string.
    # THE VULN: Uses an unsanitized path.
    if user_type == "admin":
        print(f"DEBUG: Admin accessing {file_path}")
        with open(f"/var/log/app/{file_path}", 'r') as f:
            return f.read()
    return "Access Denied"

if __name__ == "__main__":
    print(verify_and_read(sys.argv[1], sys.argv[2]))
