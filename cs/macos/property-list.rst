overview
========
- property list is a file format to store serialized objects.

- They are usually used to store user's settings.

- extension: ``.plist``.

- property list format is initially designed by NeXTSTEP.

NeXTSTEP format
===============
- data format:

  * string::

      "string"

  * binary data::

      <hex codes>

  * array::

      (elem, elem, ...)

  * dictionary::

      {
        "key" = "value";
        ...
      }

XML format
==========
- data format:

  * NSString::
   
      <string>UTF-8 encoded string</string>

  * NSNumber::
   
      <real>real number</real>
      <integer>integer number</integer>

  * NSNumber (boolean)::
   
      <true/>
      <false/>

  * NSDate::
   
      <date>ISO 8601 formatted string</date>

  * NSData::
    
      <data>base64 encoded data</data>

  * NSArray::
   
      <array>any elements</array>

  * NSDictionary::
    
      <dict>
        <key>key string</key>
        any value element
        <key>key string</key>
        any value element
        ...
      </dict>

binary property list format
===========================
- 由于 XML plist 存储效率低, Mac OS X 10.2 introduced a new binary property
  list format. Starting with Mac OS X 10.4, this is the default format for
  preference files.

- binary property list 的优势:

  * space efficient.

  * fast serialization/deserialization.

- The binary file can store information that cannot be captured in the XML or
  JSON file formats. The array, set and dictionary binary types are made up of
  pointers - the objref and keyref entries - that index into an object table in
  the file. This means that binary plists can capture the fact that - for
  example - a separate array and dictionary serialized into a file both have
  the same data element stored in them. This cannot be captured in an XML file.
  Converting such a binary file will result in a copy of the data element being
  placed into the XML file.

- data format: See [PListWIKI]_.

JSON format
===========
- In Mac OS X 10.7, support for reading and writing files in JSON format was
  introduced.
  
- JSON and property lists are not fully compatible with each other, though.

plutil utility
==============
- usages:

  * check the syntax of property lists.

  * convert property list between formats.

references
==========
.. [PListWIKI] `Property list <https://en.wikipedia.org/wiki/Property_list>`_
