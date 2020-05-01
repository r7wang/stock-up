import websocket

from stock_query import settings


def on_message(ws, message):
    print('Message: {}'.format(message))


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"SHOP"}')


if __name__ == "__main__":
    websocket.enableTrace(True)
    app = websocket.WebSocketApp(
        "wss://ws.finnhub.io?token={}".format(settings.TOKEN),
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    app.on_open = on_open
    app.run_forever()
