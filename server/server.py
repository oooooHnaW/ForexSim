import websocket
from dotenv import load_dotenv, find_dotenv
import os
from datetime import datetime
import json

# .env for API keys and IP/Cloudflare/HTTP(S) info
load_dotenv(find_dotenv(".env.server"))

serverAPI = os.getenv("FINNHUB_API")

# Active subscriptions (Limited to 50 for free tiers)
subscriptions = set()

# Class of symbol subscriptions
class SymbolSubscription:
    def __init__(self, sym):
        self.sym = sym

    def subscribe(self):
        return json.dumps({"type":"subscribe","symbol":self.sym})

    def unsubscribe(self):
        return json.dumps({"type":"unsubscribe","symbol":self.sym})

    
# What happens when I receive a message
def on_message(ws, message):
    payload = json.loads(message)

    if "data" in payload:
        trade_list = payload["data"]
        
        for trade in trade_list:
            symbol = trade["s"] # Stock Ticker Symbol
            price = trade["p"] # Last Price
            timestamp_ms = trade["t"] # Timestamp in milliseconds
            
            readable_time = datetime.fromtimestamp(timestamp_ms/1000).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"[{readable_time}] {symbol:10} | Price: {price}")

# Socket errors
def on_error(ws, error):
    print(error)

# Explains what happens when socket closes (Don't need to touch)
def on_close(ws, close_status_code, close_msg):
    print(f"Socket Disconnected!\nCode {close_status_code} | Message {close_msg}")

# What happens when starting a websocket
def on_open(ws):
    # Adding subscriptions
    eurusd = SymbolSubscription(sym="OANDA:EUR_USD")
    ws.send(eurusd.subscribe())
    subscriptions.add(eurusd)
    # print(subscriptions)



if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={serverAPI}",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
