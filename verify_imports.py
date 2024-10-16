import sys
import os

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Sys.path: {sys.path}")

def check_import(module_name):
    try:
        module = __import__(module_name)
        print(f"{module_name} version: {module.__version__}")
        print(f"{module_name} location: {module.__file__}")
        if module_name == 'markupsafe':
            print(f"{module_name} contents: {dir(module)}")
    except ImportError as e:
        print(f"{module_name} import error: {e}")
    except AttributeError as e:
        print(f"{module_name} attribute error: {e}")

modules_to_check = ['flask', 'jinja2', 'markupsafe', 'werkzeug']

for module in modules_to_check:
    check_import(module)

try:
    from markupsafe import soft_unicode
    print("soft_unicode import successful")
except ImportError as e:
    print(f"soft_unicode import error: {e}")

print("\nEnvironment Variables:")
for key, value in os.environ.items():
    print(f"{key}={value}")