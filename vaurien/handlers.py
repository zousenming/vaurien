import gevent


def normal(source, dest, to_backend, name, settings, proxy):
    request = proxy.get_data(source)
    dest.sendall(request)


def delay(source, dest, to_backend, name, settings, proxy):
    if to_backend:
        # a bit of delay before calling the backend
        gevent.sleep(settings.get('sleep', 1))

    normal(source, dest, to_backend, name, settings, proxy)


def errors(source, dest, to_backend, name, settings, proxy):
    """Throw errors on the socket"""
    if to_backend:
        proxy.get_data(source)
        # XXX find how to handle errors (which errors should we send)
        #
        # depends on the protocol
        dest.sendall("YEAH")


def hang(source, dest, to_backend, name, settings, proxy):
    """Reads the packets that have been sent."""
    # consume the socket and hang
    proxy.get_data(source)
    while True:
        gevent.sleep(1.)


def blackout(source, dest, to_backend, name, settings, proxy):
    """Don't do anything -- the sockets get closed"""
    return


handlers = (normal, delay, errors, hang, blackout)