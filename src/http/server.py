try:
    import usocket as socket
except:
    import socket


# this is a simple HTTP server
class HttpServer:

    # initializes an HTTP server with IP address, port, and a handler
    # which handles incoming HTTP requests
    def __init__(self, ip, port, handler):
        self.ip = ip
        self.port = port
        self.handler = handler

    # starts the server on the specified IP address and port
    def start(self):
        s = socket.socket()

        ai = socket.getaddrinfo(self.ip, self.port)
        addr = ai[0][-1]

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(5)
        print('server started on %s:%s' % addr)

        # main server loop
        while True:
            print('waiting for connection ...')
            res = s.accept()
            client_s = res[0]
            print('accepted')

            try:
                # read the status line
                status_line = client_s.readline().decode('utf-8').strip()

                # content length
                length = 0

                # read all headers, and look for Content-Length header
                # in order to read data from the request
                headers = {}
                while True:
                    h = client_s.readline()
                    if h == b"" or h == b"\r\n":
                        break
                    parts = h.decode('utf-8').strip().lower().split(':')
                    name = parts[0].strip()
                    value = parts[1].strip()
                    headers[name] = value
                    if name == 'content-length':
                        length = int(value)

                # read data from the request
                data = client_s.read(length).decode('utf-8')

                # let the handler to process the request
                self.handler.handle(client_s, status_line, headers, data)

                client_s.close()
            except Exception as e:
                import sys
                sys.print_exception(e)
                print('continue ...')

