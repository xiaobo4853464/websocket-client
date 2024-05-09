import base64
import hashlib
import hmac
import json
import sys
import time
from threading import Thread

import websocket

access_key = "MzRmMWVhZDExMDVhNTY0Zg"
secret_key = "YjcxNjVjOGFhMjY0NTE5ZmQ4NjBhZGQ5N2I4ZGI1OTI"
symbols = ["DOGE-USDT", "AVAX-USD", "AVAX-USDT", "XRP-USD", "AVAX-USDC", "BNB-USD", "BNB-USDT", "XRP-USDT", "DOGE-USDC",
           "BNB-USDC", "XRP-USDC", "DOGE-USD", "BTC-USDT", "ADA-USDC", "SOL-USDC", "SOL-USD", "USDT-USD", "USDC-USD",
           "ADA-USDT", "ETH-USDT", "ADA-USD", "BTC-USD", "BTC-USDC", "ETH-USDC", "SOL-USDT", "USDC-USDT", "ETH-USD"]


def on_message(ws, message):
    print("### on_message ###")
    print(message)


def on_error(ws, error):
    print("### on_error ###")
    print(error)


# def on_ping(ws, message):
#     print("### on_ping ###")
#     print(message)
#     ws.send('ping')
# def on_pong(ws, message):
#     print("### on_pong ###")
#     print(message)
#     ws.send('ping')


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        # for s in symbols:
        #     req = {"operation": "sub_rts", "request_id": str(int(time.time() * 1000)), "symbol": s,
        #            "side": "Buy",
        #            "base_size": "",
        #            "quote_size": "1000"}
        #     ws.send(json.dumps(req, ensure_ascii=False))
        #     time.sleep(5)
        req = {"operation": "sub_rts", "request_id": str(int(time.time() * 1000)), "symbol": 'ETH-USD',
               "side": "Buy",
               "base_size": "",
               "quote_size": "1000"}
        ws.send(json.dumps(req, ensure_ascii=False))

        # time.sleep(1)
        # ws.close()
        # print("Thread terminating...")

    def auth(*args):
        print('auth....')
        auth_req = {
            "operation": "auth",
            "request_id": "10001",
            "access_key": access_key,
            "timestamp": int(time.time() * 1000),
            "sign": ""
        }
        payload = f"{auth_req['timestamp']}GET/ws{auth_req['request_id']}"
        signature = hmac.new(secret_key.encode(), payload.encode(), hashlib.sha256).digest()
        encoded_signature = base64.b64encode(signature).decode()
        auth_req['sign'] = encoded_signature
        ws.send(json.dumps(auth_req))

    def heartbeat(*args):
        while True:
            time.sleep(6)
            ws.send("ping")

    Thread(target=auth).start()
    Thread(target=run).start()
    Thread(target=heartbeat).start()


if __name__ == "__main__":
    # websocket.enableTrace(True)
    url = "wss://qa-api.hts.sg/ws"

    ws = websocket.WebSocketApp(
        url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open,
        # on_ping=on_ping,
        # on_pong=on_pong
    )
    # ws.on_open = on_open
    ws.run_forever()
