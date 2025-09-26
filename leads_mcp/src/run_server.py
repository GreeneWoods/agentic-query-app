from app_definition import create_app
import uvicorn


if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app, host='localhost', port=8002)
