import sys
import socket
import threading

opened_ports = []
socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mutex = threading.Lock()


def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:
        return False

    return True


def check_port(target, port):
    mutex.acquire()
    try:
        if socket_instance.connect_ex((target, port)) == 0:
            opened_ports.append(port)
    finally:
        mutex.release()


def main():

    target = '' # provide a domain or an ipv4 address

    if is_valid_ipv4_address(target) == False:
        try:
            target = socket.gethostbyname(target)
            socket_instance.settimeout(2)
        except socket.error as err:
            print("socket creation failed with error %s" % (err))
            sys.exit()

    for port in range(1, 1000):
        try:
            threading.Thread(target=check_port, args=(target, port)).start()
        except:
            print("Error: unable to start thread")

    print(opened_ports)

    socket_instance.close()


if __name__ == '__main__':
    main()
