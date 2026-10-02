import websocket
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(".env.server"))

serverAPI = os.getenv("FINNHUB_API")
print(serverAPI)

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"unsubscribe","symbol":"AAPL"}')
    ws.send('{"type":"unsubscribe","symbol":"AMZN"}')
    ws.send('{"type":"unsubscribe","symbol":"BINANCE:BTCUSDT"}')
    ws.send('{"type":"unsubscribe","symbol":"IC MARKETS:1"}')


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={serverAPI}",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
