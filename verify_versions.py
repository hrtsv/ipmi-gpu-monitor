import sys
import flask
import werkzeug
import jinja2
import markupsafe
import sqlalchemy
import flask_sqlalchemy
import flask_jwt_extended
import gunicorn

print(f"Python version: {sys.version}")
print(f"Flask version: {flask.__version__}")
print(f"Werkzeug version: {werkzeug.__version__}")
print(f"Jinja2 version: {jinja2.__version__}")
print(f"MarkupSafe version: {markupsafe.__version__}")
print(f"SQLAlchemy version: {sqlalchemy.__version__}")
print(f"Flask-SQLAlchemy version: {flask_sqlalchemy.__version__}")
print(f"Flask-JWT-Extended version: {flask_jwt_extended.__version__}")
print(f"Gunicorn version: {gunicorn.__version__}")

# Verify Jinja2 functionality
template = jinja2.Template("Hello, {{ name }}!")
result = template.render(name="World")
print(f"Jinja2 template test: {result}")

# Verify MarkupSafe functionality
escaped = markupsafe.escape("<script>alert('XSS')</script>")
print(f"MarkupSafe escape test: {escaped}")