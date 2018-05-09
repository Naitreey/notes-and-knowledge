overview
========
- cryptography package 分为 recipes layer (high level) and hazardous layer
  (lower level).

higher layer
============

symmetric cryptosystem
----------------------

Fernet
^^^^^^

methods
""""""""
- generate_key(). generate symmetric secret key.

- encrypt(data). input is bytes-like object. output is URL-safe base64-encoded
  encrypted bytes.

- decrypt(token, ttl=None). the reverse of the previous procedure.

MultiFernet
^^^^^^^^^^^
