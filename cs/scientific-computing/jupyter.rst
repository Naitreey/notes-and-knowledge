General
=======
- Jupyter aims to support interactive data science and scientific computing
  across all programming languages.
- jupyter notebook frontend 可以和多种语言的 kernel process 一起使用.
  使用一种通用的协议进行通信.

- jupyterhub is a multi-user version of the notebook designed for companies,
  classrooms and research labs.

- jupyter 提供了很多语言 kernel 的集成, 在 notebook 中可以使用非常多种语言.
  明白何时该使用 jupyter 何时该使用各种语言自身提供的工具是很重要的:
  当我们的需求是构建一个文档, 且其中需要具有非纯文本内容, 包含数学、多媒体
  或可执行、可交互等复杂元素需求的情况下, 适合使用 jupyter notebook.

notebook
--------

kernels
-------
- kernels 提供不同语言的后端支持. 需要在 notebook 里使用什么语言就安装什么
  kernel, 完全不局限于 python.

- IPyKernel 是 jupyter 的 python kernel, 即是对 ipython 的一层向 kernel 适配
  的封装. a pre-installed kernel, reference implementation of kernels.

- I have to say, with jupyter (jupyter-c-kernel), we can REPL in C & C++...

nbviewer
--------
- nbviewer 是一个 jupyter notebook 的共享阅读服务, 提供对 publicly accessible
  notebooks 的 rendering service. 从而大家可以阅读和参考很多用 jupyter 写成的
  有价值的资料.

- nbviewer 渲染 notebook 成 html, 所以是只读的、静态的. 而 binder 是直接以
  交互式地打开, 和本地运行类似.

- The Notebook Viewer does not store any notebooks, only renders them to html.
  To force an update, append ``?flush_cache=true`` to the viewer URL.

- the same as ``jupyter nbconvert --to html ...`` locally.

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
notebook
~~~~~~~~
- ``--notebook-dir=<dir>``
  ``jupyter notebook`` 默认以当前目录作为 notebook 的文件根目录. 这个参数修改
  根目录.

binder
------
- binder 服务基本就是远程运行 jupyter notebook, 提供交互式的 notebook 共享服务.
  这是与 nbviewer 不同之处.
