# Tutorial

-----

## Connecting with server

Connects with the server using the port 5000

```
connect 5000
```


## Autentication

To autenticate to server so a user can type more specific commands use the command:

```
auth <username> <password>
```

> This application does not realy autenticate, since the FTP protocol is insecure

## Send

To run the application's nested terminal type:

```
send
```

List of valid commands inside a send nested terminal

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

> The cd command has problemas when using it with more than one thread