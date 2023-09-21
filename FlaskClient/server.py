def format_json(cmd:str):
    return {"header": {
                        "version": 1,
                        "requestId": f'{uuid4()}',
                        "messagePurpose": "commandRequest",
                        "messageType": "commandRequest"
                    },
                    "body": {
                        "version": 1,
                        "commandLine": cmd,
                        "origin": {
                            "type": "player"
                        }
                    }}

from uuid import uuid4; from flask import Flask, render_template, request, redirect


app = Flask(__name__)
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/waiting", methods=['POST'])
def waiting():
    global v1, v2, op
    v1 = int(request.form["v1"])
    v2 = int(request.form["v2"])
    op = request.form["op"]
    return redirect("/results")

@app.route("/results")
def results():
    return render_template('results.html', res= 0)
 
app.run(host = '127.0.0.1', port='8080', debug=True)