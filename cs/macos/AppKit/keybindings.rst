overview
========
- Key bindings are specified in an dictionary file that must have an extension
  of ``.dict``.

config files
============
- standard key bindings::

    /System/Library/Frameworks/AppKit.framework/Resources/StandardKeyBinding.dict

- user's custom key bindings::

    ~/Library/KeyBindings/DefaultKeyBinding.dict

format
======
- the dictionary file must be XML property list format, with backward
  compatibility with NeXTSTEP property list format.

- Key bindings are key-value pairs with the key being a string that specifies a
  physical key and the value identifying an action method to be invoked when
  the key is pressed.

- The text system supports the specification of multiple keystroke bindings
  through nested binding dictionaries. For instance, Escape could be bound to
  ``cancel:`` or it could be bound to a whole dictionary which would then
  contain bindings for the next keystroke after Escape.

key codes
=========
- The alphanumeric character that appears on a US keyboard.

- 一些在 ASCII 字符集中包含的 special keys, 可使用其 ASCII code value 的
  octal/hex number character entity 形式 ``&#xNNNN;`` 来表示 (对于 NeXTSTEP 格
  式, 使用 escape sequence ``\UNNNN``). e.g., tab, enter, return, escape,
  delete.

- key modifiers::

    ^ control
    ~ option
    $ shift
    @ command
    # modifier for keys on the numpad

- Function-key, 使用 unicode value 的 character entity (or escape sequence) 来
  表示. See [AppKitFuncKeys]_ for enum constant values.

methods
=======
- For a list of usable methods organized by their categories, see
  [KeyBindingSelectors]_.

concepts and conventions
------------------------
- Direction: Some methods refer to spatial directions; left, right, up, down.
  These are meant to be taken literally, especially in text. To accommodate
  writing systems with directionality different from Latin script, the terms
  forward, beginning, backward, and end are used.

- Selection: Methods that refer to moving, deleting, or inserting imply that
  some elements in the responder are selected, or that there’s a zero-length
  selection at some location (the insertion point). 

- Marks: A number of action methods for editing text imitate the Emacs concepts
  of point (the insertion point), and mark (an anchor for larger operations
  normally handled by selections in graphical interfaces).

- Kill buffer: Like Emacs, deletion methods affecting lines, paragraphs, and
  the mark implicitly place the deleted text into a buffer, separate from the
  pasteboard, from which you can later retrieve it.

references
==========
.. [GHKeyBindings] `ttscoff/KeyBindings <https://github.com/ttscoff/KeyBindings>`_
.. [AppKitTextDefault] `Text System Defaults and Key Bindings <https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/EventOverview/TextDefaultsBindings/TextDefaultsBindings.html>`_
.. [AppKitFuncKeys] `Function-Key Unicodes <https://developer.apple.com/documentation/appkit/1535851-function-key_unicodes?language=objc>`_
.. [KeyBindingSelectors] `Usable Selectors for Cocoa Key Bindings <http://www.hcs.harvard.edu/~jrus/site/selectors.html>`_
.. [DefaultKeyBindings] `DefaultKeyBinding.dict <https://web.archive.org/web/20161104151247/http://osxnotes.net/keybindings.html>`_
.. [EmuateEmacs] http://www.hcs.harvard.edu/~jrus/site/KeyBindings/Emacs%20Opt%20Bindings.dict
