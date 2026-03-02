import sys
import subprocess
import importlib
import requests


def check_python_version():
    # Check Python version >= 3.10
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        return True, f"{version.major}.{version.minor}.{version.micro}"
    return False, f"{version.major}.{version.minor}.{version.micro}"


def check_virtual_environment():
    # Check if running inside a virtual environment
    return sys.prefix != sys.base_prefix


def check_package_installed(package_name):
    # Check if a package is installed
    try:
        module = importlib.import_module(package_name)
        version = getattr(module, "__version__", "Unknown")
        return True, version
    except ImportError:
        return False, None


def check_internet():
    #Check internet connectivity
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.RequestException:
        return False



# Run all onboarding checks
print("=== Developer Onboarding Check ===")

total_checks = 0
passed_checks = 0

version_ok, version = check_python_version()
total_checks += 1
if version_ok:
    print(f"[PASS] Python version: {version}")
    passed_checks += 1
else:
    print(f"[FAIL] Python version: {version}")

total_checks += 1
if check_virtual_environment():
    print("[PASS] Virtual environment: Active")
    passed_checks += 1
else:
    print("[FAIL] Virtual environment: Not Active")

for package in ["pylint", "black", "numpy"]:
    total_checks += 1
    installed, version = check_package_installed(package)
    if installed:
        print(f"[PASS] {package} installed: version {version}")
        passed_checks += 1
    else:
        print(f"[FAIL] {package} not installed")

total_checks += 1
if check_internet():
    print("[PASS] Internet connectivity: OK")
    passed_checks += 1
else:
    print("[FAIL] Internet connectivity: Failed")

print("---")
print(f"Result: {passed_checks}/{total_checks} checks passed")

with open("setup_report.txt", "w", encoding="utf-8") as file:
    file.write(f"{passed_checks}/{total_checks} checks passed\n")
