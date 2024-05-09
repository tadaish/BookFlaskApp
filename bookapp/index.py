from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello World"


if __name__ == "__main__":
    from bookapp.admin import *

    app.run(debug=True)
