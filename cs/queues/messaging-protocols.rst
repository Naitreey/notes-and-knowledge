AMQP
====
- Advanced Message Queuing Protocol.

- design principle: interoperability between different vendors.

- features:
  
  * reliability
   
  * interoperability

  * feature rich

  * a binary wire protocol

- It assumes an underlying reliable transport layer protocol such as TCP.

- AMQP was originally designed by JP Morgan.

- implementations:

  * Apache Qpid

  * Apache ActiveMQ

  * RabbitMQ

- major versions:

  * 1.0

  * 0-9-1

MQTT
====
- Message Queue Telemetry Transport

- design principle: suitable for resource-constrained devices and low
  bandwidth, high latency networks.

- features:

  * suitable for IoT, embedded devices

  * simplicity

  * a compact binary packet payload

- publish-and-subscribe messaging, no queues

STOMP
=====
- Simple/Streaming Text Oriented Messaging Protocol

- design principle: simple, and widely-interoperable.

- features:

  * text-based

  * simplicity

  * interoperability

- no queues and topics, it uses a SEND semantic with a “destination” string.
