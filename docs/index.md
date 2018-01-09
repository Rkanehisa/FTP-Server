# Tutorial

-----

## Connecting with server

Connects with the server using `port <port_number>` command.

```
connect 5000
```


## Autentication

The server can handle more than one user, so it's useful to authenticate yourself.

```
auth <username> <password>
```

> This application does not realy autenticate, since the FTP protocol is insecure

## Send

The most useful commands are run inside a nested terminal, acessible by typing:

```
send
```

List of valid commands inside the <Send> terminal.

```
===================================
 Sends a command to the FTP server
 	send [cmd]
===================================
 Valid commands:
-----------------------------------
	mv [address1] [address2]
	mkdir [dir_name]
	get [filename]
	put [filename]
	cd
	ls
	pwd
	touch [filename]
```

> The cd command has problems when using it with more than one thread

### Example

Running the server application.
```
$ python server.py
server_socket now listening...
```

----

Running the client application.

```
$ python client.py
```

```
    Welcome to the Client-FTP shell.

        Type help or ? to list commands.

    
(C-FTP) >> connect 5000
Connected on FTP-Server at server:5000
(C-FTP) >> auth user pass
Welcome user!
Server: Hello user@addr
(user) >> send
===================================

(user) >> [Send] ?

Documented commands (type help <topic>):
========================================
EOF  auth  cd  connect  exit  help  ls  mkdir  mv  pwd  quit  send  touch

Undocumented commands:
======================
get  put

(user) >> [Send] ls
example_quote.txt
(user) >> [Send] mkdir src
Path src created!
(user) >> [Send] mkdir typo
Path typo created!
(user) >> [Send] mv typo correct
<FTP-Server/test/remote/user/typo> file renamed to </FTP-Server/test/remote/user/correct>
(user) >> [Send] pwd
/FTP-Server
(user) >> [Send] touch __init__.py
File __init__.py created!
(user) >> [Send] ls
correct
__init__.py
example_quote.txt
src
(user) >> [Send] get example_quote.txt
Sending data....
File example_quote.txt downloaded on /FTP-Server/test/local/user/example_quote.txt
(user) >> [Send] exit
Leaving Send Console...
(user) >> quit
Quitting the User session...
```

-----

> Team Rodrigo Kanehisa (rkanehisa), Marcos Vinicius (mschonfinkel)