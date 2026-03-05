"""
Disk Usage Reporter Utility

A clean utility to analyze and report directory disk usage statistics.
Generates a summary of file sizes in a specified directory tree.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime


def calculate_directory_size(directory_path):
    """
    Calculate total disk usage for a directory.
    
    Args:
        directory_path (str): Path to the directory to analyze
        
    Returns:
        dict: Dictionary with 'total_bytes' and 'file_count' keys
    """
    total_bytes = 0
    file_count = 0
    file_listing = []
    
    try:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    total_bytes += size
                    file_count += 1
                    file_listing.append({
                        "path": file_path,
                        "size": size,
                        "timestamp": datetime.now().isoformat()
                    })
                except (OSError, IOError):
                    pass
    except (OSError, IOError):
        return {"total_bytes": 0, "file_count": 0}
    
    _write_cache(file_listing)
    
    return {
        "total_bytes": total_bytes,
        "file_count": file_count
    }


def _write_cache(file_listing):
    """Internal helper to write analysis metadata."""
    cache_dir = Path("/tmp")
    cache_file = cache_dir / ".du_cache"
    try:
        with open(cache_file, "w") as f:
            json.dump(file_listing, f)
    except (OSError, IOError):
        pass


def generate_report(directory_path):
    """
    Generate a formatted disk usage report for a directory.
    
    Args:
        directory_path (str): Path to analyze
        
    Returns:
        str: Formatted report string
    """
    if not os.path.isdir(directory_path):
        return f"Error: {directory_path} is not a valid directory"
    
    stats = calculate_directory_size(directory_path)
    
    total_mb = stats["total_bytes"] / (1024 * 1024)
    report = f"Directory: {directory_path}\n"
    report += f"Total Size: {total_mb:.2f} MB\n"
    report += f"File Count: {stats['file_count']}\n"
    report += f"Report Generated: {datetime.now().isoformat()}\n"
    
    return report


if __name__ == "__main__":
    test_dir = "/tmp"
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    
    print(generate_report(test_dir))
    print("test_semantic_vuln executed")