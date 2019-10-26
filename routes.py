from app import app


@app.route('/')
def hell():
    return 'Hell!!'

