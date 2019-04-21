torrent file
============
- A torrent file contains metadata about files and folders to be distributed,
  and where to download the file or the pieces of it.

- Filename extension: ``.torrent``.

- MIME type: ``application/x-bittorrent``

terms
-----
- Each file to be distributed is divided into small information chunks called
  pieces.

- BEP -- BitTorrent Enhancement Proposals.

format
------
A torrent file is a bencoded dictionary with the following keys:

- ``announce`` the url of the tracker

- ``announce-list``: multiple tracker support, a list of tracker urls. (propsed
  in BEP-0012)

- ``nodes``. distributed hash table support. It should be set to the K closest
  nodes in the torrent generating client's routing table. Alternatively, the
  key could be set to a known good node such as one operated by the person
  generating the torrent. (proposed in BEP-0005)

- ``info`` maps to a dictionary whose keys are dependent on whether one or more
  files are being shared:

  When one file is being shared:

  * ``name``: suggested filename where the file is to be saved.

  * ``length``: size of the file in bytes.

  * ``piece length``: number of bytes per piece. This is commonly 256KB.

  * ``pieces``: a concatenation of each piece's SHA-1 hash.

  When multiple files are being shared:

  * ``name``: suggested directory name where the files are to be saved.

  * ``files``: a list of dictionaries each corresponding to a file. Each
    dictionary has the following keys:

    - ``path``: a list of strings corresponding to subdirectory names, the last
      of which is the actual file name.

    - ``length``: size of the file in bytes.

  * ``piece length``: number of bytes per piece. This is commonly 256KB.

  * ``pieces``: Concatenation of the concatenation of each file's SHA-1 hashes
    in the order they appear in the files dictionary


All strings are UTF-8 encoded, except for pieces, which contains binary data.
