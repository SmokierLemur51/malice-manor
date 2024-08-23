from . import factory

def run() -> None:
    app = factory.create_app()
    app.run(debug=True)


def init_db() -> None:
    factory.init_db()