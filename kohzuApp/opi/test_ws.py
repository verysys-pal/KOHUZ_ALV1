import asyncio, websockets, json, sys

async def test():
    try:
        async with websockets.connect("ws://localhost:8888/ws") as ws:
            req = {
                "type": "subscribe",
                "pvs": [f"KOHZU:m{i}.{pv}" for i in range(1, 7) for pv in ["RBV", "VAL", "DMOV", "HLS", "LLS", "MRES", "VELO", "HLM", "LLM", "STOP"]]
            }
            await ws.send(json.dumps(req))
            print("Sent request.")
            for _ in range(30):
                msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                print("Received:", msg[:100])
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

asyncio.run(test())
