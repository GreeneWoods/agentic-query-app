from fastapi import FastAPI


def create_app():
    app = FastAPI(title="Leads API", version="0.0.1")

    return app