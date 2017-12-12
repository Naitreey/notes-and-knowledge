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
--------
the web application
~~~~~~~~~~~~~~~~~~~
- notebook 的 frontend, an interactive authoring tool.
  它和 notebook server 之间通过 http & websocket 进行通信.

notebook documents
~~~~~~~~~~~~~~~~~~
- notebook file is a representation of all content visible in the web
  application. ``.ipynb`` 文件以 JSON 格式存储数据, 包含 code, output,
  markdown text, multimedia 等.

kernels
-------
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

IPyKernel
~~~~~~~~~
- IPyKernel 是 jupyter 的 python kernel, 即是对 ipython 的一层向 kernel 适配
  的封装. a pre-installed kernel, reference implementation of kernels.

export
------
- notebook 向其他格式导出的过程: preprocessing -> exporting -> postprocessing.
  即 notebook 经过 preprocessor, 运行代码更新所有 output 的最终结果; 经过
  exporter 导出指定格式文件; 导出的文件经过 postprocessor 再处理.

nbviewer
~~~~~~~~
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
-------
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
-----------
jupyter notebook
~~~~~~~~~~~~~~~~
- ``--notebook-dir=<dir>``
  ``jupyter notebook`` 默认以当前目录作为 notebook 的文件根目录. 这个参数修改
  根目录.

jupyter console
~~~~~~~~~~~~~~~

jupyterhub
----------
- jupyterhub is a multi-user version of the notebook designed for companies,
  classrooms and research labs.


binder
------
- binder 服务基本就是远程运行 jupyter notebook, 提供交互式的 notebook 共享服务.
  这是与 nbviewer 不同之处.
