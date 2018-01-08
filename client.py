import socket
import sys
import os
from cmd import Cmd

import click


class ClientPrompt(Cmd):
    intro = '''
    Welcome to the Client-FTP shell.\n
    \tType help or ? to list commands.\n
    '''
    prompt = '(C-FTP) >> '

    def __init__(self, user):
        super(ClientPrompt, self).__init__()

        self.user = user

    def do_quit(self, arg):
        """Quits the console"""
        click.echo("Quitting the User session...")

        if self.user.is_auth:
            cmd_str = '({0}, {1}, {2}, {3})'.format(self.user.username, "quit", 0, 0)
            self.user.client_socket.send(cmd_str.encode("utf8"))
            self.user.disconnect()
        return True

    def do_EOF(self, line):
        """END OF FILE, quits Client Shell by Ctrl-Z """
        return True

    def do_connect(self, port):
        """connect port\n
        Creates a socket and connects to a given port."""
        int_port = int(port)
        self.user.connect(int_port)

    def do_auth(self, arg):
        """auth username password\n
        Logs user."""
        username, password = arg.split()

        self.user.login(username, password)

        click.echo("Welcome {0}!".format(self.user.username))

        self.prompt = "({0}) >> ".format(self.user.username)

        cmd_str = '({0}, {1}, {2}, {3})'.format(self.user.username, "auth", 0, 0)
        self.user.client_socket.send(cmd_str.encode("utf8"))

        server_response = self.user.client_socket.recv(1024).decode()

        click.echo(server_response)

    def do_send(self, arg):
        """
        ===================================
         Sends a command to the FTP server
         \tsend [cmd]
        ===================================
         Valid commands:
        -----------------------------------
        \tmv [address1] [address2]
        \tmkdir [dir_name]
        \tget [filename]
        \tput [filename]
        \tls
        \tpwd
        """
        if self.user.is_auth:
            new_prompt = self.prompt + "[Send] "
            next_cli = SendConsole(self.user)
            next_cli.prompt = new_prompt
            next_cli.cmdloop()
        else:
            click.echo("Please authenticate yourself\nType help or ? to list commands.\n")


class SendConsole(ClientPrompt):
    intro = '''===================================\n'''

    valid_cmds = frozenset({"ls", "get", "mv", "touch", "mkdir", "put", "pwd"})

    def do_mv(self, args):
        """mv source target
        Move (rename) files
        """
        src, target = args.split()
        cmd_str = '({0}, {1}, {2}, {3})'.format(self.user.username, "mv", src, target)
        self.user.client_socket.send(cmd_str.encode("utf8"))

        server_response = self.user.client_socket.recv(1024).decode()

        click.echo(server_response)

    def do_mkdir(self, arg):
        """mkdir directory_name
        Make directories"""
        cmd_str = '({0}, {1}, {2}, {3})'.format(self.user.username, "mkdir", arg.strip(), 0)
        self.user.client_socket.send(cmd_str.encode("utf8"))

        server_response = self.user.client_socket.recv(1024).decode()

        click.echo(server_response)

    # def do_cd(self, arg):
    #     """cd DIR
    #     Change the shell working directory."""
    #     cmd_str = '({0}, {1}, {2}, {3})'.format(self.user.username, "cd", arg.strip(), 0)
    #     self.user.client_socket.send(cmd_str.encode("utf8"))
    #     server_response = self.user.client_socket.recv(1024).decode()
    #     click.echo(server_response)

    def do_touch(self, arg):
        """touch filename
        Creates an empty file with filename.
        """
        cmd_str = '({0}, {1}, {2}, {3})'.format(self.user.username, "touch", arg.strip(), 0)
        self.user.client_socket.send(cmd_str.encode("utf8"))

        server_response = self.user.client_socket.recv(1024).decode()

        click.echo(server_response)

    def do_get(self, arg):
        filename = arg.strip()
        cmd_str = '({0}, {1}, {2}, {3})'.format(self.user.username, "get", filename, 0)
        self.user.client_socket.send(cmd_str.encode("utf8"))

        abs_path = os.getcwd()

        local_path = os.path.join(abs_path,"test", "local",self.user.username,filename)

        click.echo("Sending data....")

        with open(local_path, 'w') as f:
            data = self.user.client_socket.recv(1024).decode()
            print(data)
            f.write(data)
            while True:
                data = self.user.client_socket.recv(1024).decode()
                print(data)
                if "--END--" in data:
                    break
                f.write(data)

        click.echo("File {0} downloaded on {1}".format(filename, local_path))

    def do_put(self, arg):
        filename = arg.strip()
        abs_path = os.getcwd()
        local_path = os.path.join(abs_path,"test", "local",self.user.username,filename)

        cmd_str = '({0}, {1}, {2}, {3})'.format(self.user.username, "put", filename, 0)
        self.user.client_socket.send(cmd_str.encode("utf8"))

        click.echo("Sending data....")

        with open(local_path, 'r') as f:
            partial_f = f.read(1024)
            #print(partial_f)
            self.user.client_socket.send(partial_f.encode("utf8"))
            while partial_f:
                partial_f = f.read(1024)
                #print(partial_f)
                self.user.client_socket.send(partial_f.encode("utf8"))
        self.user.client_socket.send("--END--".encode("utf8"))

        click.echo("100%!!")

    def do_ls(self, arg):
        """ls
        List directory contents"""
        cmd_str = '({0}, {1}, {2}, {3})'.format(self.user.username, "ls", 0, 0)

        self.user.client_socket.send(cmd_str.encode("utf8"))

        server_response = self.user.client_socket.recv(1024).decode()

        click.echo(server_response)


    def do_pwd(self, arg):
        """pwd
        Prints name of current/working <remote> directory"""
        cmd_str = '({0}, {1}, {2}, {3})'.format(self.user.username, "pwd", 0, 0)

        self.user.client_socket.send(cmd_str.encode("utf8"))

        server_response = self.user.client_socket.recv(1024).decode()

        click.echo(server_response)

    def do_exit(self, arg):
        """exit
        Leaves Send console."""
        click.echo("Leaving Send Console...")
        return True


class User():
    def __init__(self):
        self.is_auth = False

    def login(self, username, password):
        self.username = username
        self.password = password
        self.is_auth = True

    def connect(self, port=5000):
        self.client_socket = socket.socket()
        self.host = socket.gethostname()
        self.port = port

        try:
            self.client_socket.connect((self.host, self.port))
        except socket.error:
            click.echo("Error on client_socket.bind method")
            sys.exit()

        self.client_socket.send("(?, hello, 0, 0)".encode("utf8"))
        click.echo("Connected on FTP-Server at {0}:{1}".format(self.host, self.port))

    def disconnect(self):
        self.client_socket.close()

if __name__ == '__main__':
    user = User()
    cmd_prompt = ClientPrompt(user)
    cmd_prompt.cmdloop()
