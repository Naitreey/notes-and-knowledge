overview
========
- a python library for read/write Excel 2010 xlsx/xlsm/xltx/xltm files.

installation
============
- openpyxl

- optional: lxml

- optional: pillow

module-level functions
======================
- ``load_workbook(filename, read_only=False, keep_vba=False, data_only=False, keep_links=True)``.
  load an existing workbook.

  * ``data_only``. whether cells with formulae have either the formula
    (default) or the value stored the last time Excel read the sheet.

  * ``keep_vba``. controls whether any Visual Basic elements are preserved or
    not (default). If they are preserved they are still not editable.

Workbook
========
- An in-memory representation of a spreadsheet document.

- A workbook is always created with at least one worksheet.

instance attributes
-------------------
- ``active``. the currently active Worksheet.

- ``sheetnames``. the names of all worksheets of this workbook.

- ``template``. boolean. Set to True to make the workbook a template (xltx).

instance methods
----------------
- ``create_sheet(title=None, index=None)``.

- ``copy_worksheet(from_worksheet)``. create a copy worksheet of
  ``from_worksheet``. Only cells (including values, styles, hyperlinks and
  comments) and certain worksheet attribues (including dimensions, format and
  properties) are copied. You also cannot copy worksheets between workbooks.
  You cannot copy a worksheet if the workbook is open in read-only or
  write-only mode.

- ``__getitem__(key)``. key 是 worksheet 的名字, 返回指定的 worksheet.

- ``__iter__()``. iterate through all worksheets of this workbook.

- ``save(filename)``. save current workbook under filename. This will overwrite
  existing files without warning.

Worksheet
=========
- Sheets are given a name automatically when they are created. They are
  numbered in sequence (Sheet0, Sheet1, Sheet2, etc.)

instance attributes
-------------------
- ``title``. a worksheet's title. Set it to change title.

- ``sheet_properties``.

- ``rows``. Returns a generator that iterate through all rows of a worksheet.
  Each generated row is a tuple of cells in the row.

- ``columns``. Returns a generator taht iterate through all columns of a
  worksheet. Each generated column is a tuple of cells in the column.

- ``values``. iterates over all the rows in a worksheet but returns just the
  cell values.

instance methods
----------------
- ``__getitem__(key)``.
  
  * Given a ``<x><y>`` coordinate, e.g., A1, B2, etc, returns a cell.  Create a
    new cell if it does not exist yet.

  * Given a ``<x><y>:<x><y>`` slice, e.g., ``A1:C3``, returns a rectangular
    range of cells, as a 2-D cell array. Create them if any of them does not
    exist.

  * Given a ``<x>`` axis value, e.g., A, B, etc., returns a list of cells
    belonging to that column.

  * Given a ``<x>:<x>`` axis slice, e.g., ``A:C``, returns a 2-D array of 
    cells, where each row of the array contains the list of cells of a column
    in the worksheet.

  * Given a ``<y>`` axis value -- a number, e.g., 1, 2, returns a list of cells
    belongging to that row.

  * Given a ``<y>:<y>`` axis slice, e.g., ``1:3``, returns a 2-D array of
    cells, where each row of the array contains the list of cells of a row in
    the worksheet.

- ``__setitem__(key, value)``. set a value to a cell.

- ``cell(row, column, value=None)``. get a cell at the specified row and
  column, optionally set it to value. Create the cell if not exist yet.

- ``iter_rows(min_row=None, max_row=None, min_col=None, max_col=None, values_only=False)``.
  Produces cells from the worksheet, by row. Specify the iteration range using
  indices of rows and columns. If no cells are in the worksheet an empty tuple
  will be returned.

- ``iter_cols(min_col=None, max_col=None, min_row=None, max_row=None, values_only=False)``.
  Produces cells from the worksheet, by column. Specify the iteration range
  using indices of rows and columns. If no cells are in the worksheet an empty
  tuple will be returned.

- ``append(iterable)``. append an iterable of values at the bottom of the
  current sheet to form a row. If iterable is a list, tuple, range, generator,
  append each element into consecutive columns. If iterable is a dict, keys
  are column indexes (column number or letter), and values are assigned to
  their columns.

- ``merge_cells(range_string=None, start_row=None, start_column=None, end_row=None, end_column=None)``.
  When merging cells all cells but the top-left one are removed from the
  worksheet. specify ``range_string`` or ``start_row``, ``start_column``,
  ``end_row`` and ``end_column``. ``range_string`` is ``<x><y>:<x><y>``.

- ``unmerge_cells(range_string=None, start_row=None, start_column=None, end_row=None, end_column=None)``.

- ``add_image(img, anchor=None)``. Add an image to the sheet.  Optionally
  provide a cell for the top-left anchor.

Cell
====
instance attributes
-------------------
- ``value``. cell's value. Set it to change cell's value.
