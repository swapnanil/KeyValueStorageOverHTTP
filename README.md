Key-value pair storage over HTTP
================================

This is a multithreaded, client-server architechture based key-value storate and retrival system written in Python. It can be used to add, update, delete and retrieve key-value pairs over a network through HTTP.

Usage examples:
-----

1. Adding a new key-pair value  
```
POST /addPair HTTP/1.1
Host: localhost:8462
Cache-Control: no-cache
Content-Type: application/x-www-form-urlencoded

key=key-name&value=key-value
```
2. Retrieve a key value  
```
GET /retrieve/key-name HTTP/1.1
Host: localhost:8462
Cache-Control: no-cache
```

Starting the server:
-------------------
```python main.py [port]```

Possible modifications:
-----------------------
1. Using a better storage system than Python's dictionary
