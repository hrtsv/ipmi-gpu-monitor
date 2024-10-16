import sys
print(f"Python version: {sys.version}")

try:
    import flask
    print(f"Flask version: {flask.__version__}")
except ImportError as e:
    print(f"Flask import error: {e}")

try:
    import jinja2
    print(f"Jinja2 version: {jinja2.__version__}")
except ImportError as e:
    print(f"Jinja2 import error: {e}")

try:
    import markupsafe
    print(f"MarkupSafe version: {markupsafe.__version__}")
    print("MarkupSafe contents:", dir(markupsafe))
except ImportError as e:
    print(f"MarkupSafe import error: {e}")

try:
    from markupsafe import soft_unicode
    print("soft_unicode import successful")
except ImportError as e:
    print(f"soft_unicode import error: {e}")