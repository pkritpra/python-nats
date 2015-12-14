# coding: utf-8
import tornado.ioloop
import tornado.gen
from datetime import timedelta
from nats.io.client import Client as NATS

@tornado.gen.coroutine
def main():
    nc = NATS()

    # Set pool servers in the cluster and give a name to the client
    # each with its own auth credentials.
    options = {
        "servers": [
            "nats://secret1:pass1@127.0.0.1:4222",
            "nats://secret2:pass2@127.0.0.1:4223",
            "nats://secret3:pass3@127.0.0.1:4224"
            ]
        }

    # Error callback takes the error type as param.
    def error_cb(e):
        print("Error! ", e)

    def close_cb():
        print("Connection was closed!")

    def disconnected_cb(e):
        print("Disconnected!")

    def reconnected_cb():
        print("Reconnected!")

    # Set callback to be dispatched whenever we get
    # protocol error message from the server.
    options["error_cb"] = error_cb

    # close_cb is called whenever tcp connection
    # to the server is closed.
    options["close_cb"] = close_cb

    # Called when we are not connected anymore to the NATS cluster.
    options["disconnected_cb"] = disconnected_cb

    # Called when we connect to a node in the NATS cluster.
    options["reconnected_cb"] = reconnected_cb

    yield nc.connect(**options)

    @tornado.gen.coroutine
    def subscriber(msg):
        yield nc.publish("pong", "pong:{0}".format(msg.data))

    yield nc.subscribe("ping", "", subscriber)

    for i in range(0, 10000000):
        yield nc.publish("ping", "ping:{0}".format(i))
        yield tornado.gen.sleep(0.1)

if __name__ == '__main__':
    tornado.ioloop.IOLoop.instance().run_sync(main)
