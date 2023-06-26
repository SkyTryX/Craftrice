processed = False
def dec2bin(n: int, neg: bool) -> list[int]:
        if neg == True : n=n*-1
        decimal = n
        bin_inverse=[]
        while decimal != 0:
            bin_inverse.append(decimal % 2)
            decimal = decimal // 2
        while len(bin_inverse) < 3:
             bin_inverse.append(0)
        position=len(bin_inverse)
        binarie= []
        for i in bin_inverse:
            position-= 1
            binarie.append(bin_inverse[position])
        return binarie

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

import asyncio, websockets, json; from uuid import uuid4; from time import sleep; from flask import Flask, render_template, request, redirect
import threading
async def mineproxy(websocket):
    global resultat
    processed = True
    print('La connection avec Minecraft a été effectué!')
    coords_input = ["-31.5 -59 70", "-31.5 -59 72", "-31.5 -59 74", "-31.5 -59 78", "-31.5 -59 80", "-31.5 -59 82"]

    #Determine quelle valeur est négative
    if v1 < 0: v1_neg = True 
    else: v1_neg = False
    if v2 < 0: v2_neg = True 
    else: v2_neg = False

    #Traduction de décimal à binaire
    v1_bin = dec2bin(v1, v1_neg)
    v2_bin = dec2bin(v2, v2_neg)

    #On fait disparaitre les villageois des anciens calculs
    await websocket.send(json.dumps(format_json("kill @e[type=villager]")))

    #Pour chaque valeur en binaire, on importe l'input sur Minecraft grâce à des spawns de villageois
    value_check = 0
    for value in v1_bin:
        if value == 1:
            await websocket.send(json.dumps(format_json(f"summon villager {coords_input[value_check]}")))
        value_check+= 1
    value_check = 3
    for value in v2_bin:
        if value == 1:
            await websocket.send(json.dumps(format_json(f"summon villager {coords_input[value_check]}")))
        value_check+= 1

    #On fait spawn les signes des inputs grâce à des villageois (si positif, on spawn un villageois)
    if v1_neg == False:
        await websocket.send(json.dumps(format_json("summon villager -29 -52 9")))
    if v2_neg == False:
        await websocket.send(json.dumps(format_json("summon villager -23 -37 21")))

    #On regarde le calcul selectionné, pour regarder l'output que l'on veut
    if op == "x":
        sleep(20)
        for coords in ["-13 -59 81", "-12 -59 81", "-11 -59 81", "-10 -59 81", "-9 -59 81", "-8 -59 81"]:
            await websocket.send(json.dumps(format_json(f"testforblock {coords} lit_redstone_lamp")))
        #AJOUTER LE GETTER DE BIT DE POIDS FORT
    elif op == "+":
        sleep(10)
        for coords in ["-12 -59 50", "-11 -59 50", "-10 -59 50", "-9 -59 50"]:
            await websocket.send(json.dumps(format_json(f"testforblock {coords} lit_redstone_lamp")))
        await websocket.send(json.dumps(format_json(f"testforblock -8 -59 50 lit_redstone_lamp")))

    #On récupère les resultats en récupérant les websockets envoyés par Minecraft
    output_dec = 0
    pos = 0
    output_bin = []
    try:
        async for msg in websocket:
            msg = json.loads(msg)
            if msg['body'].get('matches', None) != None:
                if msg['body']["matches"] == True and msg["body"]["position"]["x"] != -8 and op == "+" or msg["body"]["position"]["x"] != -7 and op == "x" :
                    output_dec += 2**pos
                    output_bin.append(1)
                    pos+= 1
                elif msg['body']["matches"] == False and msg["body"]["position"]["x"] != -8 and op == "+" or msg["body"]["position"]["x"] != -7 and op == "x":
                    pos+= 1
                    output_bin.append(0)

                if msg['body']["matches"] == True and msg["body"]["position"]["x"] == -8 and op == "+" or msg["body"]["position"]["x"] == -7 and op == "x":
                    output_dec= 0
                    for i in range(len(output_bin)):
                        if output_bin[i]== 0: output_bin[i] = 1
                        else: output_bin[i] = 0

                    for i in range(-(len(output_bin)), 0):
                        if output_bin[len(output_bin)+i] == 0: 
                            output_bin[len(output_bin)+i] = 1
                            break
                        else:
                            output_bin[len(output_bin)+i] = 0

                    output_bin[len(output_bin)-1] = 0
                    pos= len(output_bin)-1
                    print(output_bin)
                    for bit in output_bin:
                        if bit == 1:
                            output_dec -= 2**pos
                        pos-= 1
            print(output_dec, output_bin)
            resultat = output_dec
    #Si Minecraft se ferme
    except websockets.exceptions.ConnectionClosedError:
        print("Exceptions.ConnectionClosedError || La connection avec Minecraft a été rompu par l'hote distant")

async def main():
    async with websockets.serve(mineproxy, host='localhost', port=3000):
        print("\nC'est prêt! -> /connect localhost:3000 || Ctrl+C pour arrêter le websocket")
        asyncio.sleep(10)

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
    while not processed:
        asyncio.run(main())
    return redirect("/results")

@app.route("/results")
def results():
    return render_template('results.html', res= resultat)
 
app.run(host = '127.0.0.1', port='8080', debug=True)