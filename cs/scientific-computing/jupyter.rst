General
=======
- Jupyter aims to support interactive data science and scientific computing
  across all programming languages.

architecture
------------
- notebook 不是 jupyter 的全部, 而是它 most powerful, most obvious 的部分. 
  notebook 在 jupyter 中处于比较上层的位置. jupyter 系统中很多部分都是
  不使用 notebook 的, 例如 console.

- 从架构上讲, notebook 是调用与 kernel 交互的 ``jupyter_client`` 的一个应用.
  调用 ``jupyter_client`` 的还有 jupyter console, 但它不具有 notebook 的
  功能, 而是提供基础的和内核交互的功能. jupyter notebook 和 jupyter
  console/qtconsole 等在架构上是同层的.

- 为了重用 notebook 相关逻辑, 在 jupyter 架构中, notebook 模块并不包含 server
  的实现, 仅提供 notebook manipulation 相关逻辑实现. 它支撑着其上多种可能
  的 notebook server 实现. 这包含 jupyterhub, tmpnb, nbgrader 等.

notebook
========

the web application
-------------------

- notebook 的 frontend, an interactive authoring tool.
  它和 notebook server 之间通过 http & websocket 进行通信.

- 在 dashboard 界面可以 drag & drop 上传 notebook and python source files.

- 可以启动多个 notebook server, 例如对于不同的目录. 多个 server 会自动递增
  端口号, 除非命令行上指定.

notebook UI components overview
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- notebook dashboard

  * file tree

    - 有 active kernel 的 notebooks 有个绿色的图标和 running 标识.

- notebook editor

  * menubar

  * toolbar

  * notification area: messages in response to user actions.

  * cell mode indicator: edit/command mode, 通过 pencil 图标区别.

  * kernel indicator: which kernel in use. 灰色的空心圆表示 kernel 空闲状态;
    实心圆表示 kernel is busy; 断裂状表示和 kernel 连接断掉了.

  * active cell 处于 edit/command mode 边框不同.

- file editor. 编辑非 notebook 的文本文件, 可选择高亮语言.

  从 dashboard 中直接点击打开后是只读的, 不能编辑. 需要 select 后点击 edit.

cells
~~~~~
- cells: code cell, markdown cell, raw cell. cell types can be changed
  via menu or keyboard shortcut.

- code cell. 能够输出 rich output.

- markdown cell.
  
  When markdown cell is executed, the Markdown code is converted into the
  corresponding formatted rich text. Markdown allows arbitrary HTML code for
  formatting.

  通过 mathjax, markdown cell 里可以直接写 latex. 具体支持的 latex 语法参考
  mathjax. 例如, standard latex math macros and amsmath package are supported.

- raw cell. 在格式转换时有用, where you can write output directly. 这里 output
  指的是使用 nbconvert 目标格式书写的内容. 因此 raw cell 不会被执行, 并且原样
  保留至目标格式文件中.

downloads
~~~~~~~~~
- 当 notebook 以 python source 文件输出时, all rich output has been removed and
  the content of markdown cells have been inserted as comments.

modes
~~~~~
- command mode: 可以使用很多 shortcuts.

- edit mode: 文本编辑模式.

command/edit modes 之间通过 enter/esc 切换.

shortcuts
~~~~~~~~~
可自定义.

- normal mode

  * run current cell and jump to next cell or create a new cell.
  
  * run current cell and keep focus on current cell. useful for
    temporary execution.
  
  * run current cell and insert a new cell below the current one.
  
  * enter into edit mode.

  * convert cell types: to code, to markdown, to raw.

  * convert to heading 1-6

  * move focus to cell below, to cell above.

  * extend selected cells below/above.

  * insert cell above/below.

  * cut selected cells.

  * copy selected cells.

  * paste cells above/below.

  * undo cell deletion.

  * delete selected cells.

  * merge selected cells.

  * save and checkpoint.

  * toggle line numbers.

  * toggle line numbers in all cells.

  * toggle output of selected cells.

  * help.

  * interrupt kernel.

  * restart kernel.

  * close pager.

  * scroll notebook up/down.

- edit mode

  * escape to normal mode.

  * code completion.

  * tooltip.

  * indent/dedent.

  * select all.

  * undo/redo.

  * go to cell start/end.

  * go one word left/right.

  * delete word before/after.

  * run current cell and jump to next cell or create a new cell.
  
  * run current cell and keep focus on current cell. useful for
    temporary execution.
  
  * run current cell and insert a new cell below the current one.

  * split cell.

  * save and checkpoint.

  * move cursor up/down.

extension
~~~~~~~~~

- jupyter-vim-binding

  * modes: Jupyter mode (For manipulating Jupyter) and Vim mode (For
    manipulating text). In Vim mode, there are Command mode and Insert mode
    like native Vim. Users can distinguish these mode by background color of
    the cell.

  * vim mode mappings.

    - help: ``F1``

    - enter vim mode: double click, enter.

    - exit vim mode: ``:q``, ``<S-Esc>``.

    - completion: tab.

    - tooltip: ``<C-g>``. repeating can make tooltip larger.

    - move focus to next/previous cell: j/k.

notebook documents
------------------
- notebook file is a representation of all content visible in the web
  application. ``.ipynb`` 文件以 JSON 格式存储数据, 包含 code, output,
  markdown text, multimedia 等.

- 使用 JSON 是因为是 text-based format, 能进行版本管理.

trust
~~~~~
- notebook 中包含 signature 信息. server 在打开 notebook file 时校验
  signature. 若失败, 则不会 render.

- ``jupyter trust`` 可以强制 trust 文件.

qtconsole
=========

- 一个 jupyter qt GUI console app. 它和 jupyter console 即 ipython 的区别
  是, 由于 qtconsole 是用 GUI 模拟 TUI terminal, 它可以在 console 中显示
  GUI 图形. 这是无法在真正的 TUI 界面中做到的.

- 对于 ipykernel, ``%qtconsole`` magic 可以调出一个 qtconsole 使用同一个
  kernel process.

kernels
=======
- jupyter 提供了很多语言 kernel 的集成, 在 notebook 中可以使用非常多种语言.
  明白何时该使用 jupyter + kernel 何时该使用各种语言自身提供的工具是很重要的:
  当我们的需求是构建一个文档, 且其中需要具有非纯文本内容, 包含数学、多媒体
  或可执行、可交互等复杂元素需求的情况下, 适合使用 jupyter notebook.

- kernels 提供不同语言的后端支持. 需要在 notebook 里使用什么语言就安装什么
  kernel, 完全不局限于 python. frontend 可以同时和多种语言的 kernel process
  一起使用. 使用一种通用的协议进行通信.

- I have to say, with jupyter kernels, we can REPL in C & C++ and many more...

- 一个 kernel session 可以同时和多个 frontend 建立连接. 这样多个前端 (例如
  一个 notebook server 和一个 jupyter console) 的 execution context 实际上
  是共享的.

- kernel & client 之间的通信使用 JSON 格式, 通过 ZMQ 传输.

- 每一个正在 running/active notebook 有一个独立的 kernel process 在后端
  运行. 每个 kernel process 有 id. 可以在命令行上指定该 kernel id, 通过
  jupyter console 等其他方式连上这个 kernel process, 重用这个计算环境.

IPyKernel
---------
- IPyKernel 是 jupyter 的 python kernel, 即是对 ipython 的一层向 kernel 适配
  的封装. a pre-installed kernel, reference implementation of kernels.

- 对于 ipykernel, 执行 ``%connect_info`` ipython magic 可获得 kernel 连接信息.

export
======
- notebook 向其他格式导出的过程: preprocessing -> exporting -> postprocessing.
  即 notebook 经过 preprocessor, 运行代码更新所有 output 的最终结果; 经过
  exporter 导出指定格式文件; 导出的文件经过 postprocessor 再处理.

nbviewer
--------
- nbviewer 是一个 jupyter notebook 的共享阅读服务, 提供对 publicly accessible
  notebooks 的 rendering service. 从而大家可以阅读和参考很多用 jupyter 写成的
  有价值的资料.

- nbviewer 渲染 notebook 成 html, 所以是只读的、静态的. 而 binder 是直接以
  交互式地打开, 和本地运行类似.

- The Notebook Viewer does not store any notebooks, only renders them to html.
  To force an update, append ``?flush_cache=true`` to the viewer URL.

- nbview 使用 html exporter, the same as ``jupyter nbconvert --to html ...``
  locally.

widgets
=======
这些 widget 是 jupyter 的插件, 是配合 jupyter 在浏览器中运行的. 与 matploblib
等独立运行的库目的不同.

- geo-spatial: ipyleaflet

- 2D data visualization: bqplot

- 3D data visualization: pythreejs

- 3D plotting: ipyvolume

- 3D molecular visualization: nglview

- tables, forms, plotting: BeakerX

- template for widgets: cookiecutter

commandline
===========

jupyter notebook
----------------
- jupyter notebook 运行 notebook server.

- ``--notebook-dir=<dir>``
  ``jupyter notebook`` 默认以当前目录作为 notebook 的文件根目录. 这个参数修改
  根目录.

jupyter console
---------------
- ``--existing [<arg>]`` 连接 existing active kernel process.

jupyter qtconsole
-----------------

jupyter trust
-------------

jupyter nbextension
-------------------

jupyterhub
==========
- jupyterhub is a multi-user version of the notebook designed for companies,
  classrooms and research labs.

binder
======
- binder 服务基本就是远程运行 jupyter notebook, 提供交互式的 notebook 共享服务.
  这是与 nbviewer 不同之处.
