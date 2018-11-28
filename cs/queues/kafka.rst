- high volume publish-subscribe messages and streams

- dumb broker and smart consumer.

- Kafka does not attempt to track which messages were read by each consumer and
  only retain unread messages.

- Kafka require external services to run.

- When your application needs access to stream history, delivered in
  partitioned order at least once. Kafka is a durable message store and clients
  can get a “replay” of the event stream on demand, as opposed to more
  traditional message brokers where once a message has been delivered, it is
  removed from the queue.

- Use Kafka if you need to supporting batch consumers that could be offline, or
  consumers that want messages at low latency. 

- RabbitMQ will keep all states about consumed/acknowledged/unacknowledged
  messages while Kafka doesn't, it assumes the consumer keep tracks of what's
  been consumed and not. 
