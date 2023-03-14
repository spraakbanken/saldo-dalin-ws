# -*- coding: utf-8 -*-

import utf8
import saldo_util
import socket
import cjson
from mod_python import apache
from mod_python import util

host = "localhost"
port = 8090
size = 2048


def function(format, segment):
    result = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send("0 " + segment)
        buff = ""
        while True:
            buff = s.recv(size)
            if len(buff) == 0:
                break
            result += buff
        s.close()
        result_code = apache.OK
        if format == "xml":
            result = xmlize(result)
        elif format == "html":
            result = htmlize(segment, result)
    except:
        result_code = apache.HTTP_SERVICE_UNAVAILABLE
    return (result, result_code)
