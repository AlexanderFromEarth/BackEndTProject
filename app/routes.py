from app import app

@app.route('/')
def smth():
    return app.name