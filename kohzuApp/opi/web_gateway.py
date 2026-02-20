
import tornado.ioloop
import collections.abc
# Patch for Python 3.10+ compatibility with older Tornado versions
if not hasattr(collections, 'MutableMapping'):
    collections.MutableMapping = collections.abc.MutableMapping

import tornado.web
import tornado.websocket
import epics
import json
import threading

import os

# Global state
connected_clients = set()
active_pvs = {}
main_loop = None

def global_pv_callback(pvname=None, value=None, char_value=None, **kwargs):
    """
    Callback from PyEPICS thread.
    Schedules update on Tornado Main Loop.
    """
    if pvname is not None and value is not None:
        msg_data = {"type": "update", "pv": pvname, "value": value}
        if char_value:
            msg_data["char_value"] = char_value
             
        # Schedule broadcast on main thread safely
        if main_loop:
            main_loop.add_callback(broadcast_update, json.dumps(msg_data))

def broadcast_update(message):
    """
    Executed on main thread. Sends message to all connected clients.
    """
    for client in connected_clients:
        try:
            client.write_message(message)
        except Exception as e:
            # Handle closed connections gracefully if remove failed
            pass

class EPICSWebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("Client connected")
        connected_clients.add(self)

    def on_close(self):
        print("Client disconnected")
        if self in connected_clients:
            connected_clients.remove(self)

    def on_message(self, message):
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            
            if msg_type == "subscribe":
                pvs = data.get("pvs", [])
                for pv_name in pvs:
                    self.monitor_pv(pv_name)

            elif msg_type == "write":
                pv_name = data.get("pv")
                val = data.get("value")
                if pv_name and val is not None:
                    print(f"Writing {pv_name} = {val}")
                    epics.caput(pv_name, val)

        except Exception as e:
            print(f"Error handling message: {e}")

    def monitor_pv(self, pv_name):
        if pv_name not in active_pvs:
            print(f"Monitoring PV: {pv_name}")
            # Create PV with global callback
            p = epics.PV(pv_name, callback=global_pv_callback)
            active_pvs[pv_name] = p
        else:
            # Send current value immediately if available
            p = active_pvs[pv_name]
            if p.connected:
                 self.write_message(json.dumps({
                     "type": "update", 
                     "pv": pv_name, 
                     "value": p.value,
                     "char_value": p.char_value
                 }))

class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

def make_app():
    return tornado.web.Application([
        (r"/ws", EPICSWebSocket),
        (r"/(.*)", NoCacheStaticFileHandler, {
            "path": os.path.dirname(__file__), 
            "default_filename": "motorx_all.html"
        }),
    ])

if __name__ == "__main__":
    app = make_app()
    port = 8888
    try:
        # Listen on all interfaces (0.0.0.0)
        app.listen(port, address="0.0.0.0")
        print(f"EPICS Web Gateway listening on http://0.0.0.0:{port}/")
    except OSError:
        port = 9999
        app.listen(port)
        print(f"EPICS Web Gateway listening on ws://localhost:{port}/ws")
        
    main_loop = tornado.ioloop.IOLoop.current()
    try:
        main_loop.start()
    except KeyboardInterrupt:
        print("Stopping gateway...")
