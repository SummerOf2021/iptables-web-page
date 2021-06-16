# Introduction 

We created this web application to manage the iptables, with this application you can add rules, delete rules, list rules, save an encrypted backup and restore the iptables.

Use `key-generation.py` to generate your own key and save this key because you're going to encrypt and decrypt using this key which is called `key.key`.

The server will be running on local host port 5000, and we implemented mutual TLS, if you want to remove this just edit the following code in `Server.py`

```python
HTTPS_ENABLED = True

VERIFY_USER = True
```

set VERIFY_USER to false to remove client authentication, and HTTPS_ENABLED  to false to remove Server authentication. 

The username and password is "admin" and you can change it from the following line

```python
    if request.form['password'] == 'admin' and request.form['username'] == 'admin':
```

# Requirements

you need to have the following libraries:

`datetime, os, flask, cryptography, flask_cors, werkzeug, ssl, sys`

make sure to install them before running the code.

Also you have to generate your own certificate authority and sign certificate for the server and the client, I have list how you can make that in the next section. 

Then you have to import the CA authority `rootCA.pem` and the client certificate `Client.pfx` into your browser

### Create CA 

`openssl genrsa -des3 -out rootCA.key 4096`

`openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.crt`

`cat rootCA.crt rootCA.key > rootCA.pem`

### Create certificate for server and client

**First the certificate for the server:**

`openssl genrsa -out Server.key 2048`

`openssl req -new -key Server.key -out Server.csr`

`openssl x509 -req -in Server.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out Server.crt -days 1024 -sha256`

if you want to verify and see the certificate's content run the following command 

`openssl x509 -in Server.crt -text -noout` 

**now the client certificate** 

`openssl genrsa -out Client.key 2048`

`openssl req -new -key Client.key -out Client.csr`

`openssl x509 -req -in Client.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out Client.crt -days 1024 -sha256`

`cat Client.crt Client.key > Client.pem`

` openssl pkcs12 -export -in Client.pem -inkey Client.pem -out Client.pfx`

# Run the application

First run the following command 

`python3 key-generation.py `

then 

`sudo python3 Server.py `

# Web pages:

### Login page 
![121815943-82120a80-cc81-11eb-9bba-281c107ed3d0](https://user-images.githubusercontent.com/77105379/122270487-0c0edd00-cee7-11eb-9580-b030cf47da05.png)


### Home page

![121815938-77f00c00-cc81-11eb-9bfd-ee47160a4009](https://user-images.githubusercontent.com/77105379/122270505-103afa80-cee7-11eb-8c12-82812a24a263.png)

