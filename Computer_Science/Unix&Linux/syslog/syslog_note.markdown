# overview
syslog is a standard.
A wide variety of devices, such as printers and routers, and message receivers across many platforms use the syslog standard. This permits the consolidation of logging data from different types of systems in a central repository.

The information provided by the originator of a Syslog message include the facility code and the severity level. The syslog software adds information to the information header before passing the entry to the syslog receiver. Such components include an originator process ID, a timestamp, and the hostname or IP address of the device.
# log components
## facility code
A facility code is used to specify the type of program that is logging the message.

for definition, see RFC 5424
## severity level
for definition, see RFC 5424
The meaning of severity levels other than emergency and debugging are relative to the application.
## message
The message component has these fields: TAG, which should be the name of the program or process that generated the message, and CONTENT which contains the details of the message.
# utitlity
- `logger` command
# syslog protocol
client-server application structure.
A server listens on a well-known port for protocol requests from clients. The most common Transport Layer protocol for network logging is the User Datagram Protocol (UDP), with the server listening on port number 514. UDP is unreliable, i.e. it does not guarantee the delivery of the messages. The use of UDP has been declared obsolete by RFC 5424 which states implementation must support Transport Layer Security (TLS) via the Transmission Control Protocol (TCP). Syslog over TLS uses port number 6514.
