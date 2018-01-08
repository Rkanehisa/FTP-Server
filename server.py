import socket
import sys
import os
from threading import Thread

import click

DEBUG = False


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


def client_thread(conn, ip, port, buffer_size=1024):
    is_active = True

    click.echo("Creating Client Thread")

    while is_active:
        client_input = rcv_cmd(conn, buffer_size)

        cmd = client_input['cmd']

        if cmd == 'auth':
            username = client_input['user']
            abs_path = os.getcwd()
            path = os.path.join(abs_path, "test", "remote", username)
            local_path = os.path.join(abs_path, "test", "local", username)
            if not os.path.exists(path):
                os.mkdir(path)
            if not os.path.exists(local_path):
                os.mkdir(local_path)
            # os.chdir(path)

            with open(os.path.join(path, 'example_quote.txt'), 'w') as f:
                f.write('''Midway upon the journey of our life, I found myself within a forest dark,\n
                    For the straight foreward pathway had been lost.''')

            conn.send("Server: Hello {0}@{1}".format(
                username, path).encode('utf8'))

        elif cmd == 'mv':
            src, target = client_input['args']
            src = os.path.join(path, src)
            target = os.path.join(path, target)
            try:
                os.rename(src, target)
            except OSError:
                click.echo("Error while renaming src -> target.")
                # conn.send("<*> src file does not exist!".encode("utf8"))

            server_msg = "<{0}> file renamed to <{1}>".format(src, target)
            conn.send(server_msg.encode("utf8"))

        elif cmd == 'cd':
            username = client_input['user']
            dirname = client_input['args'][0]
            pwd = os.getcwd()
            path = os.path.join(pwd,"test","remote",username, dirname)
            os.chdir(path)

        elif cmd == 'ls':
            ls_ = os.scandir(path)
            ls_out = ""
            ls_out += "\n".join(item.name for item in ls_)
            conn.send(ls_out.encode("utf8"))

        elif cmd == 'mkdir':
            path1_ = client_input['args'][0]
            path_ = os.path.join(path, path1_)
            os.mkdir(path_)
            server_msg = "Path {0} created!".format(path1_)
            conn.send(server_msg.encode("utf8"))

        elif cmd == 'touch':
            filename = client_input['args'][0]
            path_ = os.path.join(path, filename)

            f = open(path_, 'w')
            f.write("")
            f.close()

            server_msg = "File {0} created!".format(filename)
            conn.send(server_msg.encode("utf8"))

        elif cmd == 'pwd':
            pwd = os.getcwd()
            path_ = os.path.join(pwd, username)
            conn.send(pwd.encode("utf8"))

        elif cmd == 'get':
            filename = client_input['args'][0]
            path_ = os.path.join(path, filename)

            # conn.send("Sending {0}".format(path_).encode("utf8"))

            with open(path_, 'r') as f:
                partial_f = f.read(1024)
                conn.send(partial_f.encode("utf8"))
                while partial_f:
                    partial_f = f.read(1024)
                    conn.send(partial_f.encode("utf8"))
            conn.send("--END--".encode("utf8"))

            # server_msg = "File {0} sent!".format(filename)
            # conn.send(server_msg.encode("utf8"))

        elif cmd == 'put':
            filename = client_input['args'][0]
            path_ = os.path.join(path, filename)

            with open(path_, 'w') as f:
                while True:
                    data = conn.recv(1024).decode()
                    f.write(data)
                    if "--END--" in data:
                        break

            click.echo("Uploaded {0}".format(filename))

            # server_msg = "File {0} sent!".format(filename)
            # conn.send(server_msg.encode("utf8"))

        elif cmd == 'quit':
            click.echo("{0} is requesting to quit.".format(username))
            is_active = False
            conn.close()
            click.echo("{0} quited.".format(username))


def rcv_cmd(conn, buffer_size):
    client_input = conn.recv(buffer_size)
    # client_input_size = sys.getsizeof(client_input)

    dec_input = client_input.decode("utf8").strip()
    click.echo("\tReceived USER cmd: " + dec_input)

    parsed_input = parse_string(dec_input)

    return parsed_input


def parse_string(user_input):
    input_tuple = user_input[1:-1].replace(' ', '').split(',')

    if DEBUG:
        click.echo(str(input_tuple))

    input_dict = {'user': input_tuple[
        0], 'cmd': input_tuple[1], 'args': input_tuple[2:]}

    if DEBUG:
        click.echo(str(input_dict))

    return input_dict


if __name__ == '__main__':
    main()
