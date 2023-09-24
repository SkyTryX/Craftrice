from uuid import uuid4; from flask import Flask, render_template, request, redirect; from json import dump, load, decoder

app = Flask(__name__)
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/waiting", methods=['POST'])
def waiting():
    uuid = uuid4()
    with open("requests.json", 'r') as file:
        try:
            data = load(file)
        except decoder.JSONDecodeError:
            data = []

    data.append({"identification":{
        "uuid": f'{uuid}',
        "queue_pos": len(data)
    },
    "request":{
        "v1": int(request.form["v1"]),
        "op": request.form["op"],
        "v2": int(request.form["v2"])
    }})

    with open("requests.json", 'w') as json_file:
        dump(data, json_file, indent=4, sort_keys=True)
    return render_template("waiting.html", pos= len(data), uuid = f'{uuid}')

@app.route("/results")
def results():
    return render_template('results.html', res= 0)
 
app.run(host = '127.0.0.1', port='8080', debug=True)