- the BDD tool has forced us to structure our test code. In the inline-style
  FT, we’re free to use as many lines as we want to implement a step, as
  described by its comment line. It’s very hard to resist the urge to just
  copy-and-paste code from elsewhere, or just from earlier on in the test.

- BDD really encourages you to write test code that seems to match well with
  the business domain, and to use a layer of abstraction between the story of
  your FT and its implementation in code. The TDD alternative to this
  abstraction layer is Page pattern.

- theoretically, if you wanted to change programming languages, you could keep
  all your features in Gherkin syntax exactly as they are, and throw away the
  Python steps and replace them with steps implemented in another language.

- The Gherkin syntax, for all its attempt to be human-readable, is ultimately a
  constraint on human language, and so it may not capture nuance and intention
  as well as inline comments do.
