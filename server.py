import socket
import sys
from threading import Thread

import click


@click.command()
@click.option('--port', default=5000, help='Defines a port for the server')
def main(port):
    host = socket.gethostname()
    server_port = port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((host, server_port))
    except socket.error:
        click.echo("Error on server_socket.bind")
        sys.exit()

    server_socket.listen(5)

    click.echo("server_socket now listening...")

    while True:
        conn, addr = server_socket.accept()
        ip, port_ = str(addr[0]), str(addr[1])

        click.echo("Connected with IP {0} : PORT {1}".format(ip, port_))

        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            click.echo("Error while creating Thread!")

    server_socket.close()


def client_thread(conn, ip, port, buffer_size=512):
    is_active = True

    click.echo("Creating Client Thread")
    while is_active:
        client_input = rcv_cmd(conn, buffer_size)


def rcv_cmd(conn, buffer_size):
    client_input = conn.recv(buffer_size)
    # client_input_size = sys.getsizeof(client_input)

    dec_input = client_input.decode("utf8").rstrip()
    click.echo(dec_input)

    return dec_input


if __name__ == '__main__':
    main()
