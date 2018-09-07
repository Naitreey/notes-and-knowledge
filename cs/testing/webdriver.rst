overview
========
- WebDriver protocol is a W3C standard.

architecture
============
- WebDriver protocol is implemented by each browser's web driver components.
  These web driver components function as the server side that receives
  WebDriver protocol requests from client side.

- Each browser's web driver component has its implementation-specific way to
  communicate with browser itself, mapping WebDriver requests to browser
  actions.

- The client side is the client application that makes browser manipulation
  requests. They talks to web driver server in WebDriver protocol.

- Selenium WebDriver client library encapsulates client-side implementation
  of WebDriver protocol, exposing an intuitive API for application authors
  to use.
