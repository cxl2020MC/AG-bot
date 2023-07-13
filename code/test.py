from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def main():
    print(request.get_json())
    print(request.cookies)
    print(request.headers)
    return "OK"

app.run()