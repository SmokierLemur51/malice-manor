from . import factory

def run() -> None:
    app = factory.create_app()
    app.run(debug=True)


