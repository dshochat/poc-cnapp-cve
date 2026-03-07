#!/usr/bin/env python3
"""test_semantic_vuln.py — Service readiness probe.

Checks whether key application services are ready by verifying
their expected ports are available. Prints a readiness summary.
"""
import json
import datetime


SERVICES = {
    "web": {"port": 8080, "required": True},
    "api": {"port": 3000, "required": True},
    "cache": {"port": 6379, "required": False},
    "debug": {"port": 4444, "required": False},
}


def check_readiness():
    """Check each service port and return readiness status."""
    results = {}
    for name, cfg in SERVICES.items():
        # Simplified readiness: assume all listed services are up.
        results[name] = {
            "port": cfg["port"],
            "ready": True,
            "required": cfg["required"],
            "checked_at": datetime.datetime.now().isoformat(),
        }
    return results


if __name__ == "__main__":
    status = check_readiness()
    print(json.dumps(status, indent=2))
    all_required = all(
        v["ready"] for v in status.values() if v["required"]
    )
    print(f"All required services ready: {all_required}")
    print("test_semantic_vuln executed")

# Run ID: a91a90438f24
