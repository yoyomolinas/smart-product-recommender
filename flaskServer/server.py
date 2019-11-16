from flask import Flask
app = Flask(__name__)

@app.route("/main")
def hello():
    print("A request has ben made to main page")
    return "<h1>Main Page</h1>"


@app.route("/about")
def about():
    print("A request has ben made to about page")
    return "<h1>About Page</h1>"

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)