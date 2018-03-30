# XnbRead

A python3 library for reading XNB files, a Microsoft container format used for
storing game content.

## Custom readers

Some games will have XNB files with custom data types. It is possible to add
your own readers dynamically (providing you can figure out the binary format,
of course). See `stardew.py` for a trivial example.

## Bugs

I have tested the library on Stardew Valley's XNB files. Any types and readers
not used in those may be poorly tested. Fixes and issue reports are welcome!

## License

XnbRead is licensed under the MIT License -- see `LICENSE.txt`.
