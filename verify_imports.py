try:
    import flask
    import werkzeug
    import jinja2
    from markupsafe import soft_unicode
    print("All imports successful!")
    print(f"Flask version: {flask.__version__}")
    print(f"Werkzeug version: {werkzeug.__version__}")
    print(f"Jinja2 version: {jinja2.__version__}")
    print(f"MarkupSafe version: {markupsafe.__version__}")
except ImportError as e:
    print(f"Import error: {e}")
