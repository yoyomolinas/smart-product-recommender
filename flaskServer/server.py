from flask import Flask
app = Flask(__name__)

@app.route("/main")
def hello():
    return "<h1>Main Page</h1>"


@app.route("/about")
def about():
    return "<h1>About Page</h1>"

if __name__ == '__main__':
    app.run(debug=True)