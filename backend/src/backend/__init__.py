from dotenv import load_dotenv
from . import factory

def run() -> None:
    load_dotenv()
    app = factory.create_app()
    app.run(debug=True)


