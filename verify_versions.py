import sys
import os

def check_import(module_name):
    try:
        module = __import__(module_name)
        print(f"{module_name} version: {getattr(module, '__version__', 'unknown')}")
        print(f"{module_name} location: {getattr(module, '__file__', 'unknown')}")
    except ImportError as e:
        print(f"Error importing {module_name}: {e}")

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

modules_to_check = ['flask', 'werkzeug', 'jinja2', 'markupsafe', 'sqlalchemy', 'flask_sqlalchemy', 'flask_jwt_extended', 'gunicorn']

for module in modules_to_check:
    check_import(module)

print("\nPython path:")
for path in sys.path:
    print(path)

print("\nEnvironment variables:")
for key, value in os.environ.items():
    print(f"{key}={value}")

# Verify Jinja2 functionality
import jinja2
template = jinja2.Template("Hello, {{ name }}!")
result = template.render(name="World")
print(f"\nJinja2 template test: {result}")

# Verify MarkupSafe functionality
import markupsafe
escaped = markupsafe.escape("<script>alert('XSS')</script>")
print(f"MarkupSafe escape test: {escaped}")