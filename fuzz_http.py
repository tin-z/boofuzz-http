#!/usr/bin/env python
# Designed for use with boofuzz v0.0.9
from boofuzz import *
import argparse


def main(host, port, addr):
    session = Session(
        target=Target(
            connection=SocketConnection(host, port, proto='tcp')
        ),
        web_address=addr
    )

    s_initialize(name="Request")
    with s_block("Request-Line"):
        s_group("Method", ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE'])
        s_delim(" ", name='space-1')
        s_string("/index.html", name='Request-URI')
        s_delim(" ", name='space-2')
        s_string('HTTP/1.1', name='HTTP-Version')
        s_static("\r\n", name="Request-Line-CRLF")
    s_static("\r\n", "Request-CRLF")

    session.connect(s_get("Request"))

    session.fuzz()


if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-H", "--host", type=str, required=True, dest="host")
  parser.add_argument("-p", "--port", type=int, required=True, dest="port")
  parser.add_argument("-a", "--address", type=str, default="localhost", dest="addr" ,\
          help="By default boofuzz appends results on http://127.0.0.1:26000/, then we may want to expose the service on other addresses"
  )

  args = parser.parse_args()
  main(args.host, args.port, args.addr)


