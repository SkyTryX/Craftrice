import asyncio, websockets, json; from time import sleep; from methods import *

with open("requests.json", "r") as file:
    dict:list = json.load(file)
if(len(dict) != 0):
    v1:int = int(dict[0]["request"]["v1"])
    op:str = dict[0]["request"]["op"]
    v2:int = int(dict[0]["request"]["v2"])
    uuid:str = dict[0]["identification"]["uuid"]
    dict.pop(0)
    for d in dict:
        d["identification"]["queue_pos"] -= 1
    with open("requests.json", 'w') as json_file:
            json.dump(dict, json_file, indent=4, sort_keys=True)
else:
    quit("[WEBSOCKET] Aucun appel de calcul")

async def mineproxy(websocket):
    print(f'[WEBSOCKET] - Calcul en cours (v1={v1}, op={op}, v2={v2}) par {uuid}')
    coords_input:list[int] = ["-31.5 -59 70", "-31.5 -59 72", "-31.5 -59 74", "-31.5 -59 78", "-31.5 -59 80", "-31.5 -59 82"]
    try: 
        #Determine quelle valeur est négative
        if v1 < 0: v1_neg:bool = True 
        else: v1_neg:bool = False
        if v2 < 0: v2_neg:bool = True 
        else: v2_neg:bool = False

        #Traduction de décimal à binaire
        v1_bin:list[int] = dec2bin(v1, v1_neg)
        v2_bin:list[int] = dec2bin(v2, v2_neg)

        #On fait disparaitre les villageois des anciens calculs
        print("[MINECRAFT] - Elimination des anciens villageois")
        await websocket.send(json.dumps(format_json("kill @e[type=villager]")))

        #Pour chaque valeur en binaire, on importe l'input sur Minecraft grâce à des spawns de villageois
        print("[MINECRAFT] - Apparition des villageois en fonction de la traduction binaire des nombres")
        value_check:int = 0
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
        print("[MINECRAFT] - Calcul en cours...")
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
        print("[WEBSOCKET] - Traduction des resultats renvoyés par Minecraft")
        output_dec:int = 0
        pos:int = 0
        output_bin:list[int] = []
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

                if msg["body"]["position"]["x"] == -8 and op == "+" or msg["body"]["position"]["x"] == -7 and op == "x" and msg['body']["matches"] == False:
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
                    for bit in output_bin:
                        if bit == 1:
                            output_dec -= 2**pos
                        pos-= 1
            print(f"[WEBSOCKET] - Resultat pour {uuid}: {output_dec} (bin={output_bin})")
            with open("res.json", 'w') as json_file:
                json_file = {
                    "uuid": uuid,
                    "res": output_dec
                }
                json.dump(dict, json_file, indent=4, sort_keys=True)

    except websockets.exceptions.ConnectionClosedError:
        print("[WEBSOCKET] - La connection avec Minecraft a été rompu par l'hote distant")

async def main():
    async with websockets.serve(mineproxy, host='localhost', port=3000):
        print("[WEBSOCKET] - Connection Possible (port=3000)")
        await asyncio.Future()
asyncio.run(main())