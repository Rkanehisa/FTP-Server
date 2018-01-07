import socket
import sys
from cmd import Cmd

import click


class ClientPrompt(Cmd):
    intro = '''Welcome to the Client-FTP shell.\n
    \tType help or ? to list commands.\n'''
    prompt = '(C-FTP) >> '

    valid_cmds = frozenset({"ls", "get", "mv", "mkdir", "put"})

    def do_welcome(self, username):
        """welcome [name]
        Welcome screen for a User"""
        click.echo("Welcome {}!".format(username))

    def do_quit(self, arg):
        """Quits the console"""
        click.echo("Quitting the User session...")
        return True

    def do_EOF(self, line):
        """END OF FILE, quits Client Shell by Ctrl-Z """
        return True

    def do_connect(self, port=5000):
        """connect [port=5000]\n
        Creates a socket and connects to a given port."""
        self.client_socket = socket.socket()
        self.host = socket.gethostname()
        self.cport = int(port)

        try:
            self.client_socket.connect((self.host, self.cport))
        except socket.error:
            click.echo("Error on client_socket.bind method")
            sys.exit()

        self.client_socket.send("Hello!".encode("utf8"))
        click.echo("Connected on FTP-Server at {0}:{1}".format(
            self.host, self.cport))

    def do_send(self, cmd):
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
        """
        if cmd is not None:
            input_cmd, args = cmd.strip().split(' ', 1)

            if input_cmd in self.valid_cmds:
               self.client_socket.send(b"AAAA")
            else:
                click.echo(
                    "Invalid command.\n\tType help or ? to list commands.\n")


if __name__ == '__main__':
    ClientPrompt().cmdloop()
