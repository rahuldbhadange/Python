from flask import Flask, render_template  # From module flask import class Flask


app = Flask(__name__)  # Construct an instance of Flask class for our webapp
app.config["DEBUG"] = True  # Enable reloader and debugger


@app.route('/hello')
def main():
    """Render an HTML template and return"""
    return render_template('hello.html')  # HTML file to be placed under sub-directory templates


if __name__ == '__main__':  # Script executed directly?
    app.run()  # Launch built-in web server and run this Flask webapp
