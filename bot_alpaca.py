import config_alpaca, websocket, json, requests
BASE_URL="https://paper-api.alpaca.markets"
ORDERS_URL="{}/v2/orders".format(BASE_URL)
HEADERS={'APCA-API-KEY-ID':config_alpaca.API_KEY, 'APCA-API-SECRET-KEY':config_alpaca.SECRET_KEY}
 
#websocket endpoint, ie l'url qu'on va requêter :
socket="wss://stream.data.alpaca.markets/v1beta1/crypto" 

#les on_open, on_close etc sont des callback functions, qui sont nécessaires à renseigner dans le cas d'évenements donnés.
#par exemple pour on_open ie quand on ouvre la connexion on veut s'authentifier, d'ou la fonction suivante :
def on_open(ws):
    print("opened")
    auth_data={
        "action": "auth",
        "key": config_alpaca.API_KEY,
        "secret": config_alpaca.SECRET_KEY
    }
    ws.send(json.dumps(auth_data))
    #ici ce qu'on a fait c'est qu'on a créé les données d'identification et on les a transmis au websocket

    stream_picked={
        "action":"subscribe",
        "trades":["ETHUSD"],
        "quotes":[],
        "bars":["ETHUSD"]
    }
    ws.send(json.dumps(stream_picked))

def create_order(symbol, qty, side, type, time_in_force):
#permet de placer une commande. voir Undertand orders à cette url : https://alpaca.markets/docs/trading-on-alpaca/orders/
    data={
        "symbol":symbol,
        "qty":qty,
        "side":side,
        "type":type,
        "time_in_force":time_in_force
    }
    r=requests.post(ORDERS_URL,headers=HEADERS,json=data)
    return json.loads(r.content )

seq=[]

def on_message(ws,message):
    data=json.loads(message)
    p=data[0]["p"]
    print(p)
    print("salut")
    seq.append(p)

    #une fois l'authentification réussie (ou pas d'ailleurs), il faut pouvoir transmettre le message renvoyé par le websocket, c'est donc ce que fait cette fonction
    #on va essayer de réagir au message reçu, en effectuant un achat d'action si les conditions nous semblent intéressantes.

    if (len(seq)>99): #on a toute la séquence qu'on voulait récupérer pour input au modèle.
        decision=model(seq)
        seq=[]
        if decision=="buy":
            create_order("ETHUSD",1,"buy", "market","gtc")
        else : 
            create_order("ETHUSD",1,"sell", "market","gtc")


ws=websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
ws.run_forever()