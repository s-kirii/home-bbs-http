from api.server import HTTPServersHandle
import sys

if __name__=="__main__":
    ipv6 = False
    try:
        if sys.argv[1] == "ipv6":
            ipv6 = True
    except IndexError:
        pass
    
    sv_handle = HTTPServersHandle(ipv6=ipv6)
    sv_handle.start_server()