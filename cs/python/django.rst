overview
========

concepts
--------
- 作为一个 web server or web framework, django 的各种主要功能和模块,
  都是在从 receive request 开始, 至 send out response 结束, 这个流程中
  做文章的.

  一个 django 应用, 或任何一个 web app, 一旦运行起来, 就只做一件事:
  接收请求 -- 处理请求 -- 返回响应.

- django 的架构 MVC/MTV.

  * Template 属于展示层, 它是一个功能实现的最外层. View 属于控制层 (controller).
    Model 属于 model 层, 它在最里面.

from request to response, full workflow
---------------------------------------

django release
--------------

- new feature release (A.B, A.B+1) every 8 months.
  new LTS release (X.2) every 2 years, LTS is supported with security updates
  for 3 years.
  each version following an LTS will bump to the A+1 major version number.
  patch release (A.B.C, A.B.C+1) will be issued as needed.

- 1.11 LTS is the last version supporting python2.

- Django 2.0 和 1.11 相比, 不是特别大的区别, 不充满 breaking changes,
  而是连续的演进. 只是版本号规范的重新定义.


project and application
=======================

project
-------
- 在 django 语境下, 一个 project 就是一个 web project, 一个项目. 一个项目可以是
  一个组相互关联的事物、事情和功能的集合, 它们构成一个抽象整体, well a web app.

project structure
^^^^^^^^^^^^^^^^^
- 所有第一方的 django apps.

- docs.

- env files and/or directories.

- other files.

distribution
^^^^^^^^^^^^
* 由于 django 设计的 project 代码 import 逻辑 -- 即 project 目录需要在 ``sys.path``
  中, 导致 django project 不适合整个打包为 python package 然后用 pip 安装至
  site-packages 目录. 因为这样的效果是在 ``sys.path`` 中包含 site-packages 的子目录.
  结果就是 import 时可能存在覆盖问题.

- 整个 django project 适合打包成 rpm/deb, 放在 ``/usr/lib`` 下. 或者对于只需单次
  部署, 非 package 发布形式的话, 完全可以放在任意一个目录下, 例如 ``$HOME``.

- 一个 django project 中的每个 reusable app, 都应该可以打包成 python package 用
  pip 安装.

initialization
^^^^^^^^^^^^^^
- Django 初始化项目的流程由 ``django.setup()`` 控制.

  * load settings.
  
  * setup logging.
  
  * Populate default app registry with ``INSTALLED_APPS``.

- ``setup()`` is called automatically when

  * running HTTP server via dev server or wsgi handler.
  
  * executing management command.

- Django app's root package ``__init__`` and the modules that define
  application configuration classes shouldn’t import any models at
  module-level, even indirectly.

Use a django project in standalone script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- define ``DJANGO_SETTINGS_MODULE`` environ to settings module.

- call ``django.setup()`` to complete project setup.

app
---

- 一个 app 就是这个 project 中的一件事情, 一个功能, 一个模块等. 它可以单独存在,
  具有自洽的逻辑和组成. 也可以是更大整体 (即 project) 的组成部分.

  In essence, a Django application is just a Python package that is specifically
  intended for use in a Django project.

- django 提供了很多方便的功能使得 project 在 app 尺度的模块化十分容易, 例如模块
  化的 URLconf, ``include()``. 每个 app 可以独立存在, 又可以在整个项目中
  plug-and-play (PnP). 与 app 模块化配合的是 RESTful url 的模块化, 并要求 url
  层级清晰. 每个 app 的 URLconf 自成体系, 有 index, 有 object, 有 method.

distribution
^^^^^^^^^^^^
- 理想情况下, app 应该可以独立发布成 python package. 然后在任何 django 项目
  中按照标准 django 方式 (import 等) 即可使用, 成为新项目的一个 app.

- It’s often useful to prepend ``django-`` to your module name when creating
  a package to distribute. This helps others looking for Django apps identify
  your app as Django specific.

app structure
^^^^^^^^^^^^^
A django application should not be a namespaced package. All modules should be
in one filesystem path.

- views.

- forms.

- models. 可以是 subpackage, 若此, 需要在 ``__init__`` 中 import 所有 models.

- urls.

- migrations

- templates.

- static.

- ``template_tags``

- apps

- ``fields.py``. 放置所有自定义的 model fields.

- ``mixins.py``. 所有在本 app 中定义的 mixin classes. 这些 mixins 可能不仅仅
  是 views 会用到, forms, models 等也可能使用. 所以单独拿出来.

- ``tasks.py``. 需要使用 task queue 时, 放置所有任务.

- ``validators.py``. 放置所有自定义的 forms/models validators.

- ``signals.py``

- fts, its, uts.

- validators.

- admin

project app
^^^^^^^^^^^
- project 子目录是一个 project global app. 全局的模板, 全局的静态文件, 全局的
  url, 全局的管理命令等, 都应该放在这个 app 中.

- There’s no restriction that a project app can’t also be considered an
  application and have models, etc. 但若是如此, 则需要添加进入
  ``INSTALLED_APPS``.

- structure.

AppConfig
---------
- Each application has an AppConfig, which contains the application's
  configuration during app loading and also works for retrospection.

- 由于包含配置和 models 等信息, 从 ``INSTALLED_APPS`` 中加载的实际上就是这个类
  的路径.

- AppConfig vs settings.py

  * AppConfig 用于保存一个 django app 的 metadata 性质的 configuration.
    It's not meant to be changed easily and frequently.

  * settings.py 用于保存功能配置. It's designed be changed easily and
    frequently.

- AppConfig 一般放在 ``apps.py`` 中. 无论 AppConfig 放在哪里, 它所在的 module
  一定不能存在 module-level 对 models 的 import/reference. 这是因为, 在创建
  model class 时, 依赖于 app configs 已经 populated. 所以 model-level early
  import will break this precondition.

class attributes
^^^^^^^^^^^^^^^^
- ``name``. python import path to the app this AppConfig is configuring. 需要这
  个 name 是因为 AppConfig 理论上可以放在任何地方, 所以需要指定它所配置的 app
  的所在位置. Required, must be unique across a django project.

- ``label``. 这是各处使用的 ``app_label`` 的来源. 默认为 ``name``'s last part.
  This attribute allows relabeling an application when two applications have
  conflicting labels. Must be unique across a django project.

- ``verbose_name``. app's human-readable name. 例如 admin site 会使用. default
  ``label.title()``

- ``path``. app's filesystem path. default use app module's path.

instance attributes
^^^^^^^^^^^^^^^^^^^
- ``module``. application module object.

- ``apps``. ref to belonging to app registry.

- ``models_module``. app's ``models`` module object.

- ``models``. app's all models. an OrderedDict of model name to model object.

class methods
^^^^^^^^^^^^^
- ``create(entry)``. 创建 AppConfig for entry.

  * entry should be import path to app's AppConfig class.
 
  * Backward compatibility. If entry is the dotted path to an application
    module, Django checks for a ``default_app_config`` variable in that module,
    which should be an import path to an AppConfig class. If
    ``default_app_config`` is not available, base AppConfig is used.

methods
^^^^^^^
- ``get_models(include_auto_created=False, include_swapped=False)``.
  Return an iterator of app's models.

- ``get_model(model_name, require_ready=True)``.
  Return model class by name (case-insensitive).

- ``ready()``. hook to run when app loading is ready during django setup.
  如果需要, 可以在这里访问 models, 因为此时 models 都已经加载完毕.

  ``ready()`` method implementation must be idempotent. 在某些情况下可能
  被调用多次.

Apps
----
- ``django.apps.registry.Apps``

- application registry

default registry
^^^^^^^^^^^^^^^^
- 若需要在代码中获取当前安装的 django apps, 应该使用 ``django.apps.apps``
  application registry, 而不是直接访问 ``settings.INSTALLED_APPS``.

- 在项目初始化阶段, django 会调用 ``django.apps.apps.populate()`` 加载所有
  apps.

instance attributes
^^^^^^^^^^^^^^^^^^^
- ``ready``

methods
^^^^^^^

- ``populate(installed_apps=None)``. load application configuration and models.
  For each entry of ``installed_apps``, 加载逻辑为:

  * If it's AppConfig instance, 直接使用, 否则调用 ``AppConfig.create()`` 进行
    加载.
   
    Set ``apps_ready`` flag. 到此为止 app 相关的 metadata configs 都已经确定.
    这样在创建 model class 时, app label 等才能有所归属.

  * import 每个 app 的 ``models`` module.

    Set ``models_ready`` flag. 到此为止 models 都已加载完毕.

  * call each ``AppConfig.ready()`` hook.

    set ``ready`` flag. 到此为止所有 apps 加载完毕.

- ``get_app_configs()``. Return an iterable of ``AppConfig``.

- ``get_app_config(app_label)``. get one app config.

- ``is_installed(app_name)``. Whether or not an app is installed. app name is
  ``AppConfig.name``.

- ``get_model(app_label, model_name, require_ready=True)``. Return model class.

settings
--------
- ``INSTALLED_APPS``. a list of import strings to activated django apps in this
  project.

  * 该配置的意义是告诉 django 哪些 module 是属于该项目的, 即是需要加载的, 在各
    个组件的机制中需要考虑的 (例如 templates, static files, management
    commands, etc.). 这样, 允许我们在项目源代码中包含一些 "ignored" modules. 可
    能用于一些 django 之外的其他目的, 或暂时不想让 django 加载. 从而避免了
    django 去误加载.
  
  * 一定要写 path to AppConfig class, 即 ``<app>.apps.<app>Config``. 这是应用自
    定义 app config 的最佳方式.

    若 INSTALLED_APPS 中只有 app module path, 则 django checks for
    ``<module>.default_app_config`` for app config class. 这仅用作向后兼容.
    
    若没找到自定义的 app config, fallback 至 ``django.apps.AppConfig``.  但这样
    就无法使用 custom app config.

  * 列表中每个值成为创建的 ``AppConfig.name`` attribute, 因此必须保证唯一.  每
    个值的最后一部分成为 ``AppConfig.label`` attribute, 除非 class 中另有定义.
    因此也应要保证唯一性.

  * 要注意考虑 apps 在列表中放置的顺序. 这会影响:

    - Apps registry 的 population order. 从而影响 ``AppConfig.ready()`` 的执行
      顺序.  这会影响: signal handlers 的注册以及执行顺序.

    - When several applications provide different versions of the same resource
      (template, static file, management command, translation), the application
      listed first in INSTALLED_APPS has precedence.

design patterns
---------------

- 注意适当地按模块化思路将 project 拆成 apps. Your apps don't have to be
  reusable, they can depend on each other, but they should do one thing.

  Try to answer question: "What does my application do?". If you cannot answer
  in a single sentence, then maybe you can split it into several apps with
  cleaner logic.

  对于仅有一个功能模块的项目, 可以简单地将 project 直接应用为 app.

management commands
-------------------

startproject
^^^^^^^^^^^^
::

  django-admin startproject <name> [directory]

- 在 ``directory`` 中创建 django project directory structure. 若未指定, 创建
  ``$PWD/<name>`` 然后在里面初始化. 若指定, directory 必须事先存在.

startapp
^^^^^^^^
::

  ./manage.py startapp name [directory]

- create a django app directory structure in ``directory``, default to
  ``$PWD/<name>``. 若指定了 directory, 必须必须事先存在.

- 特定的 template files 可以通过 django template system 渲染后再输出. 它们
  支持以下 template variables:

  * startapp command cli options.

  * ``app_name``

  * ``app_directory``

  * ``camel_case_app_name``

  * ``docs_version`` django docs version

  * ``django_version``

- ``--template TEMPLATE``. 支持指定 alternative template directory structure
  path. default is ``django/conf/app_template``. could be:
  
  * a dir path,
    
  * a file path to compressed file containing dir directory
   
  * a url to the compressed file

- ``--extension EXTENSIONS``. a list of extensions of files to render with
  django template system.

- ``--name FILES``. a list of additional files to be rendered by template
  engine.

URLconf
=======

- URLconf 是 url pattern 和 view callable 之间的映射.

- 一组全局的 URLconf 加载逻辑.
  
  * 最顶层的 URLconf 由 ``settings.ROOT_URLCONF`` 定义. root urlconf
    中包含全局的 url, 并引入各个 app 中的 URLconf.

  * 不同层的 URLconf 可以位于不同的 namespace. 由 ``include()`` 或者
    ``app_name`` 定义.

  * URLconf 内容可以动态生成.

- 对一个请求, 如何选择相应的 url 并进行处理:

  * 选择 URLconf: ``Request.urlconf`` 或全局的 ``settings.ROOT_URLCONF``.

  * 按顺序遍历 url patterns, stops at the first one that matches the requested
    URL. 请求与 url pattern 在匹配时, 忽略 domain name 和 query string 部分,
    并不考虑请求方法. 按照不同请求方法进行不同处理的逻辑在 view callable 中实现.

  * call view callable, 传入 ``HttpRequest`` object, 传入 url pattern
    中匹配的 groups and named groups, 分别以 positional & kwargs 传入.

URLconf definition
------------------
- ``<app>/urls.py``.

- ``urlpatterns`` 全局量. A list of url patterns.

  * 使用 ``include()`` 加载别的 urlpatterns list 至特定 url prefix 下面.
    可以指定一个 URLconf 的 import path, 或者一个 ``url()`` list.

    Whenever Django encounters ``include()``, it chops off whatever part of the
    URL matched up to that point and sends the remaining string to the included
    URLconf for further processing.

- ``app_name``. optional. 指定该 URLconf 所属的 namespace.
  
related functions
^^^^^^^^^^^^^^^^^

- ``include()``.

url namespace
-------------

一个 url namespace 由两部分组成: application namespace 和 instance namespace.

namespace can be nested. 在一个本身有 namespace 的 urlpatterns 中 ``include``
另一个有 namespace 的 urlpatterns, 就得到了 nested namespace.

application namespace
^^^^^^^^^^^^^^^^^^^^^
- 对应一个 django app.

- 一个 django app 的多个 instance 具有相同的 application namespace.

- application namespace 可以通过两种方式指定:
  
  * 如果是 include 另一个 URLconf, 在 included URLconf 中指定 ``app_name``
    这可以避免不同 app 的 url name 相互覆盖.
   
  * 如果是 include 一段单独的 urlpatterns, 在 ``include()`` 中指定
    ``(urlpatterns, <app_namespace>)`` 形式参数.

instance namespace
^^^^^^^^^^^^^^^^^^
一个 app 可以在一个项目中部署多个 instance.

.. XXX 不理解 instance namespace. Looks like pretty useless.

application namespace 和 instance namespace 看上去很乱的样子, 什么意思啊??
只有当一个项目中部署了同一个 app 的多个实例时, 才需要考虑到 instance namespace.

URL pattern
-----------

* 由于所有 url 的路径部分都以 ``/`` 起始, 所以 django 的 url pattern 把它的
  匹配省去了, 写成 ``^path/to/resource/`` 而不是 ``^/path/to/resouce/``.

* view callable 会收到在各级 url pattern 中匹配的变量值.

* Each regular expression in a urlpatterns is compiled the first time it’s
  accessed. This makes the system blazingly fast.

url pattern definitions
^^^^^^^^^^^^^^^^^^^^^^^

- ``path(route, view, kwargs=None, name=None)``.

  * arguments.

    - kwargs. pass additional arguments to the view function or method 若
      ``view`` 的部分是 ``include()`` expression, kwargs 会传入包含的每个 url
      pattern.

    - name. url pattern's name.

  * capture format::

      <[type:]name>

    - ``name`` name of matched path.

    - ``type`` path converter. used to convert captured string to the specified
      value. 默认为 ``str`` converter.

  * 一个 capture group 是否会匹配并赋值, 取决于 path converter 的 regex pattern
    是否匹配. 相应地, capture group 是否可以跨越 ``/`` 完全取决于 path
    converter 的正则是否匹配.

  * 传入 view callable 的参数总是 kwargs 的形式.

- ``re_path(route, view, kwargs=None, name=None)``.

  * regex pattern 中应使用 named capturing group, 增加灵活性. 避免使用
    unnamed capturing group.

  * only capture the values the view needs to work with and use non-capturing
    arguments when the regular expression needs an argument but the view
    ignores it.
  
- ``path()`` vs ``re_path()``.
 
  * ``path()`` is used for simple or more confined pattern matching.

  * ``re_path()`` 更灵活, 因为可以直接指定正则. 但相对于 ``path()``,
    缺乏类型转换功能. 输出的总是字符串.

path converter
""""""""""""""
- builtin path converters:
  
  * str. match any non-empty string, excluding /.

  * int. match a sequence of non-negative digits.

  * slug. ASCII letters, numbers, hyphen, underscore.

  * uuid. match uuid format, return UUID instance.

  * path. match any non-empty string, including /.

- path converter class definition.

  * ``regex`` attribute. regex pattern to match url segment.

  * ``to_python(value)``. convert matched string to value to be passed
    to view callable.

  * ``to_url(value)``. reverse process of ``to_python()``. used for
    url reversing.

- 注册 path converter: ``register_converter()``.

- path converter 和注册操作应该放在 ROOT_URLCONF 中. 因为注册的 converter
  全局可见.

url resolution
--------------

- Resolver404 is a subclass of Http404. 一般不会在 view 中 raise Resolver404
  因为绝大部分情况下不会需要在 view 中 resolve url.

Reverse url resolution
----------------------

- design principle: Avoid hard-coded URLs.

- 为了能够 reverse resolution, 需要对 url pattern 命名. 这样的 URLconf 包含从
  url 映射至功能以及从功能反向映射至 url 的双向信息.

- You can deliberately choose the same URL name as another application if you
  want to override a view.

- 对于不同场景下的 url reversing 需求, django 提供了不同的操作:
  ``url`` tag, ``reverse()`` function, ``Model.get_absolute_url()`` method.

related functions
^^^^^^^^^^^^^^^^^
- ``django.urls.base.reverse()``.

  reverse 函数在反向查找时, 根据命名、参数数目、以及 kwargs 的名字来匹配.
  如果根据这些规则去匹配后有冲突, ``reverse()`` 选择 urlpatterns 中最后一个
  符合的 pattern. 这可以用于 override 其他 app 提供的同名 view.

  reverse 输出的 url 已经是 url-encoded.

- ``django.shortcuts.resolve_url(to, *args, **kwargs)``.
  Reverse resolution of ``to`` into a url. 这是一个比较 high-level 的抽象操作.

  Accepts:

  * model instance, call ``Model.get_absolute_url()``

  * reverse url resolution by calling ``reverse()``

  * a url.

timezone
========

- 日期时间使用 django.utils.timezone 里的函数, 它们会自动根据 settings.py 里的时间
  相关设置来返回恰当的结果. 直接使用 datetime module 还需要去手动读取配置.

view
====

* view 这个概念没有什么很好的意义. 应该说, 从一定程度上, HTTP 的请求可以看作是
  对整个 app 的不同视角 (view), 但这种说法有些牵强. 总之, views 就是对 url
  请求的 server 端实现.

* 每个 view 都必须返回 ``HttpResponse`` instance 或者 raise some exception. 任何其他
  结果 django 都认为是有问题的.

* 常用的非 200 响应有单独定义的 ``HttpResponse`` 子类.
  ``Http404`` 是一个单独定义的 exception, 为方便使用. django catch 这个异常,
  返回 ``templates/404.html`` 页面.

- When to use javascript/ajax with django? 当我们需要做纯前端交互逻辑和页面渲染时,
  才需要用 javascript, 当我们只是需要从服务端取数据以完成这些交互逻辑和渲染操作时,
  才需要使用 ajax, 否则都应该使用 django 的模板去构建.

* trick: 给 view callable 设置默认参数可以做到让多个 url 指向一个 view callable.

  .. code:: python

    urlpatterns = [
        url(r'^blog/$', views.page),
        url(r'^blog/page(?P<num>[0-9]+)/$', views.page),
    ]
    # View
    def page(request, num="1"):
        pass

* view decorators for http method restriction

  - ``require_http_methods(...)``

  - ``require_GET``

  - ``require_POST``

  - ``require_safe`` GET or HEAD

* view decorators for compression

  - ``gzip_page`` 将 ``GZipMiddleware`` 的功能选择性地应用在所需的 view 上面.

* view decorators for caching

  - ``cache_control(...)``

  - ``never_cache``

* HEAD handling. downstream webserver should strip body of HEAD response
  automatically, so that HEAD handling should be exactly like handling GET.

* error handling view. 对于一个请求, 当 urlpatterns 中没有匹配到时, 或者在处理过程中
  抛异常时, django 会返回一个 error-handling view. 在 URLconf 中可以自定义各个常用
  error code 对应的 response view. 例如 ``handler400``, ``handler403``,
  ``handler404``, ``handler500``.

view, template, form/formset 的设计思考
---------------------------------------

* 使用同一个 view 和同一个 url 去获取 form 和处理 form data.
  基本逻辑: GET 和 POST with invalid data 时返回 form 本身, 并且由于已经有数据,
  可以在 render 时对错误进行相应提示; POST with valid data 时处理数据返回结果.

* 前端构建的传至后端的 form data 必须要能再次回到前端填充成原始的 form
  输入内容. 也就是说, Form, BaseFormSet 等的实例必须包含能重新构建前端
  form 填充形式的所有数据. 不要在前端 form 和 django form/formset 之间
  进行数据格式转换, 这是多此一举的, 而且非常麻烦.

* form/formset 没必要和 model 一致 (也就是说没必要用 modelform), 而是完全
  由前端业务逻辑决定的. 但是, form 中的各项最好和页面模板中的 html form
  项是一致的. 这样从 POST 数据构建 form, ``form_valid``, ``form_invalid``
  等的处理和数据重填都很方便.

* 如果想要传递某些 form 项但不希望用户输入, 则使用 hidden input type (配合
  js 进行输入), 而不是直接从 form 中去掉这项. 注意 view 中逻辑需要对 hidden
  input 的数据合法性进行验证.

* form clean & validation. 不要在 view 本身的逻辑中写 form 本身数据 clean &
  validation 逻辑, 要归入 form class 的定义中, 对于 model form 的情况,
  还可考虑是否应当再归入 model class 中, 即从 model 层对数据的合法性进行进一步
  限制.

  但对于 form data 是否 suspicious 之类的检查, 需要在 view 中进行.

view shortcut utilities
-----------------------

response
^^^^^^^^
- ``django.shortcuts.render()``

- ``django.shortcuts.redirect()``

  * return ``HttpResponseRedirect``.

  * 输入 model instance, redirect to ``Model.get_absolute_url()``.

  * 输入 view name (with args, kwargs), redirect to ``reverse()`` url.

  * 输入 absolute/relative url, redirect to that url.

  * ``permanent=True``, return 301 (Moved Permanently) rather than 302 (Found).

model retrieval
^^^^^^^^^^^^^^^
- ``django.shortcuts.get_object_or_404()``

  ``QuerySet.get()`` a single object from a Model/Manager/QuerySet, 满足 args
  和 kwargs 设置的过滤条件. 语法与 ``Q`` objects + field lookup syntax 相同.

  由于是直接 raise ``Http404``, 所以这只适合在 view 中使用.

- ``django.shortcuts.get_list_or_404()``

  ``QuerySet.filter()`` a list of objects, 其他同上.

reverse url resolution
^^^^^^^^^^^^^^^^^^^^^^

- ``django.shortcuts.resolve_url()``. See `Reverse url resolution`_.

Class-based views
-----------------

- class-based views 相对于 function-based views 的一些好处.

  * Class-based (OOP-based) code reuse and abstraction is much more powerful
    and convenient than function-based (procedure-based) code reuse. 这是 CBV
    的最本质价值.

  * Object oriented techniques such as mixins (multiple inheritance) can be used
    to factor code into reusable components.

  * Organization of code related to specific HTTP methods (GET, POST, etc.) can
    be addressed by separate methods instead of conditional branching.

- 处理每个 request, View class 都会实例化一个新的 instance. 所以在
  写 view class 时不要担心状态存留问题.

- ``View``, base view class. 所有 class-based views 都是它的子类.

- attributes.

  * 所有传入 constructor 的 kwargs 都会成为 instance attributes.

  * 除此之外, ``request``, url pattern 匹配的 ``args`` & ``kwargs``
    三个参数会成为 view instance attributes.

- methods.

  * ``__init__``. 每个 class-based view 的 constructor 的参数形式都应该
    是 ``**kwargs``, 它们成为 view 实例属性.

  * ``as_view()`` class method, returns a function that can be called
    when a request arrives for a URL matching the associated pattern.
    The function creates an instance of the class and calls its
    ``dispatch()`` method.

    它的参数用于在 urlpatterns 中对 view 的参数进行自定义.
    任何传入 as_view() 的 kwargs 都会成为 view instance 的 attribute.

  * ``dispatch()`` looks at the request to determine whether it is a
    GET, POST, etc, and relays the request to a matching method if
    one is defined, or raises ``HttpResponseNotAllowed`` if not.

  * 实现与各个 request method 同名的方法来进行相应处理.
    若 HEAD 没有实现, 则用 GET 的处理代替.

- generic view classes.

  这些类提供了一些常用操作的通用实现, 以及一些自定义和扩展方式.
  但注意这些类仅适用于它所设计的情况, 若与需求不匹配, 请直接去
  subclass ``View``, 手动实现所需操作.

  例如, ListView 等直接与某个数据模型中的一系列 objects 相对应时才方便
  使用. 意思是, 如果 view 就是要展示 a list of model object.
  CreateView, UpdateView, DetailView, DeleteView 等直接与某个数据模型中的
  特定一个 object 的操作相对应时才方便使用. 意思是, 如果 view 就是要
  创建、更新、查看、删除特定的 object.
  凡是实际 view 的目的与 generic view 预设的操作目的不一致时, 都不该
  生搬硬套这些 generic view. 而是退而求其次, 例如 FormView, TemplateView,
  View 等对操作的假设很少的一般化 view.

  CRUD & class-based views.
  C -- CreateView, R -- DetailView, U -- UpdateView, D -- DeleteView.

  * ``RedirectView``

    - subclass ``View``

    - ``url`` 或 ``pattern_name`` 必须设置至少其一, 以指定 redirect url.
      对于 ``pattern_name``, 通过 ``reverse()`` 生成 url.
      若两个参数都不能正确获得 url, 将返回 HttpResponseGone (410 -- Gone).

    - 适用场景: 只适用于 GET 某个资源时进行简单的 302 Found redirect 至该
      资源的新 url. 不适合任何需要复杂后端业务逻辑处理后返回 redirect 至
      结果页面等情况. RedirectView 没有什么扩展性.

  * ``TemplateView``

    - subclass ``TemplateResponseMixin``, ``ContextMixin``, ``View``

  * ``ListView``

    - parent classes

      * ``MultipleObjectTemplateResponseMixin``

        - ``TemplateResponseMixin``

      * ``BaseListView``

        - ``MultipleObjectMixin``

          * ``ContextMixin``

        - ``View``

    - 默认使用 ``<app>/<model>_list.html`` 作为模板, ``template_name`` 参数
      自定义.

    - template context variable: ``object_list``, 以及 ``<model>_list`` 或者
      自定义的 ``context_object_name``. 两者的内容相同.

  * ``DetailView``

    - parent classes

      * ``SingleObjectTemplateResponseMixin``

        - ``TemplateResponseMixin``

      * ``BaseDetailView``

        - ``SingleObjectMixin``

          * ``ContextMixin``

        - ``View``

  * ``FormView``

    - parent classes

      * ``TemplateResponseMixin``

      * ``BaseFormView``

        - ``FormMixin``

          * ``ContextMixin``

        - ``ProcessFormView``

          * ``View``

    - ``ProcessFormView`` 定义了 POST 之后对于 valid/invalid
      form data 分别调用 ``form_valid()`` ``form_invalid()``
      两个 method, 后两者负责返回 HttpResponse instance.

  * ``CreateView``

    - parent classes

      * ``SingleObjectTemplateResponseMixin``

        - ``TemplateResponseMixin``

      * ``BaseCreateView``

        - ``ModelFormMixin``

          * ``FormMixin``

          * ``SingleObjectMixin``

        - ``ProcessFormView``

          * ``View``

    - 默认 ``template_name_suffix`` ``_form``

  * ``UpdateView``

    - parent classes: 类似 CreateView.

    - 默认 ``template_name_suffix`` ``_form``

    - 若要展示一个对象的详情, 并在同一个页面对它进行一定程度的修改,
      实际上可以使用 UpdateView 很方便地实现, 不使用 DetailView.

  * ``DeleteView``

    - parent classes

      * ``SingleObjectTemplateResponseMixin``

        - ``TemplateResponseMixin``

      * ``BaseDeleteView``

        - ``DeletionMixin``

        - ``BaseDetailView``

    - ``DeletionMixin`` 定义 POST 和 DELETE 都会删除这个对象.

- 避免过于复杂的 mixins, main class 的多继承. 如果继承太复杂, 需要太多
  override 和自定义, 不如自己从基本的 generic view 开始继承, 自己实现
  所需功能.

  另一种办法是, 将一个复杂 view 所需的功能拆成多个简单的 view 的功能,
  然后写一个 view 进行 routing.

- 对于比较简单的自定义, 可以不用去 subclass django 提供的 view classes.
  只需要在 URLconf 中使用 view class 时, 在 ``.as_view()`` 中传入所需
  的自定义参数. 这些参数等价于在实例化 view class 时传入 constructor
  的参数.

- view decorators & class-based views

  view decorators normally decorate view functions, 预期一定的参数
  形式 (例如 request 作为第一参数). 因此和 class-based view 一起使用时,
  要么直接 wrap ``.as_view()`` 返回的 view function; 要么通过
  ``django.utils.decorators.method_decorator`` 转换一下 (使 self
  参数成为第一参数), 再应用在 view class 上或者 ``dispatch()``
  之类的 view method 上.

- AJAX 处理.

  * 简单的分情况处理: 若要处理 ajax 请求, 只需 override 所需使用的
    class-based view 中最后返回 HttpResponse 的处理部分, 让它最终返回
    JsonResponse 即可.  若要能根据请求是否是 AJAX 来区分返回页面还是纯数据,
    可以判断 ``request.is_ajax()``, 即通过 ``X-Request-With: XMLHttpRequest``
    header 来辨别, 然后选择返回 ``TemplateResponse`` or ``JsonResponse``.

  * 类比 ``TemplateResponseMixin`` 实现 ``JsonResponseMixin``, 方便与其他
    generic view 结合.

    .. code:: python

      class JSONResponseMixin:
          def render_to_json_response(self, context, **response_kwargs):
              return JsonResponse(
                  self.get_serializable_data(context),
                  **response_kwargs,
              )

          def get_serializable_data(self, context):
              # serialize context data to json object, list, etc.
              return data

    应用时, 按需 override ``render_to_response()`` 调用
    ``render_to_json_response()``.

* 当选择将 mixin 与 class 的功能结合使用时, 可以有多个 mixin class, 但只能有一个
  main class. 并且 mixin 先于 main class 出现在 MRO 中才行.

view mixins
^^^^^^^^^^^

TemplateResponseMixin
"""""""""""""""""""""
Every built in view which returns a TemplateResponse will call the
render_to_response() method that TemplateResponseMixin provides.

render_to_response() itself calls get_template_names(), which by
default will just look up template_name on the class-based view; two
other mixins (SingleObjectTemplateResponseMixin and
MultipleObjectTemplateResponseMixin) override this to provide more
flexible defaults when dealing with actual objects.

- ``template_name`` 自定义模板名.

- ``render_to_response()`` 实现最终的 ``HttpResponse`` 实例化和返回.

- ``get_template_names()`` 生成模板名字 list.

MultipleObjectMixin
""""""""""""""""""""
提供方法获取 iterable of objects ``get_queryset()`` 并进行 pagination
``paginate_queryset()``.

attributes.

- ``model`` 定义这个 view 是操作在什么 model 上的.
  Specifying ``model = SomeModel`` is really just shorthand for saying
  ``queryset = SomeModel.objects.all()``.

- ``queryset`` 自定义数据集.

- ``paginate_by`` the number of entries for a page.

- ``page_kwarg`` kwarg for requested page number. 对应的参数可以作为 kwarg
  传入 view function, 或者作为 query string 的一个参数. 若未提供, 默认使用
  第一页. page number is 1-based integer, or special string ``last`` for last
  page.

- ``allow_empty``. 是否允许第一个页面为空, 即完全没有东西可以显示. If False,
  raise 404 instead of displaying an empty page.

- ``paginate_orphans``. An integer. 如果指定, 表示如果最后一页只剩下小于等于
  这个数目的条目, 就塞到倒数第二页显示.

- ``paginator_class``. paginator class.

- ``ordering``. ordering of list.

- ``context_object_name``

methods.

- ``get_queryset()`` method 动态自定义获取的数据集.
  It uses the queryset or model attribute on the view class to get
  queryset. Returns an iterable or more preferably a QuerySet, not
  paginated yet.

- ``paginate_queryset(queryset, page_size)``.
  Returns a 4-tuple containing (paginator, page, object_list, is_paginated).

template context.

- ``object_list``. original queryset, NOT paginated.

- ``<context_object_name>``. ditto.

- ``is_paginated``

- ``paginator``. 

- ``page_obj``. A Page object instance, containing current page's entries.

MultipleObjectTemplateResponseMixin
""""""""""""""""""""""""""""""""""""
A TemplateResponseMixin adjusted for a list of entries.

- Requires main class provides ``object_list`` attribute.

attributes.

- ``template_name_suffix``. default ``_list``.

methods.

- ``get_template_names()``. fallback to use
  ``<app_label>/<model_name><template_name_suffix>.html``

ContextMixin
""""""""""""
Every built in view which needs context data, such as for rendering a
template (including TemplateResponseMixin above), should call
get_context_data() passing any data they want to ensure is in there as
keyword arguments. get_context_data() returns a dictionary; in
ContextMixin it simply returns its keyword arguments, but it is common
to override this to add more members to the dictionary.

- ``get_context_data()`` 自定义 context.

  .. TODO 了解各个子类是如何 override 这个方法的.

SingleObjectMixin
""""""""""""""""""
provides a get_object() method that figures out the object based on the
URL of the request (it looks for pk and slug keyword arguments as
declared in the URLConf, and looks the object up either from the model
attribute on the view, or the queryset attribute if that’s provided).

- ``model``

- ``queryset``

- ``context_object_name``

- ``pk_url_kwarg``, url pattern 中使用的 object 正则 group 名字.
  默认是 ``pk``.

- ``get_object()`` 获取单个数据. 使用 ``pk_url_kwarg`` 的值从 queryset
  中选择要获取的 object.

SingleObjectTemplateResponseMixin
""""""""""""""""""""""""""""""""""

FormMixin
""""""""""

- ``form_class``

- ``success_url``

- ``get_form_kwargs()``. 获取 form 实例化时的 constructor arguments.

- ``form_valid()`` POST valid data 时调用.

- ``form_invalid()`` POST invalid data 时调用.

ModelFormMixin
""""""""""""""
- ``fields`` 选择生成的 ModelForm 要包含的 fields.
  该参数或者 ``form_class`` 必选一.

- ``model``, ``get_object().__class__`` ``queryset.model``
  三者之一决定这个 view 所使用的 ``ModelForm`` 是什么.

- 若未提供 ``success_url``, 使用 ``Model.get_absolute_url()``.

- ``form_valid()`` 调用 ``form.save()`` 保存 model instance.

- ModelFormMixin 和一些 form 类型的 view 结合, 成为具体的
  CreateView, UpdateView.

File handling
=============

- 文件不一定是用户上传的, 只要是存储在数据库之外的文件体都可以用这个模块处理.

- 用户文件的下载在生产时应通过前端服务器来处理, 在研发时通过 django 来处理. 用
  户文件的上传则始终通过 django 来处理.

file classes
------------

File
^^^^
- ``django.core.files.File``.

- wrapper around file-like object.

class attributes
""""""""""""""""
- DEFAULT_CHUNK_SIZE. 64KB.

constructor
""""""""""
- ``file``. underlying file-like object.

- ``name``. filename. If not defined, use ``file.name``.

attributes
""""""""""
- ``file``. file-like object.

- ``name``

- ``size``. file size.

- ``mode``. file mode.

- underlying file-like object's attributes.

methods
"""""""

- ``__str__()``. return ``File.name`` or empty string if name is None.

- ``__len__()`` check ``File.size``.

- ``__bool__()`` check ``bool(File.name)``

- ``__enter__()``, ``__exit__``. context manager. close underlying file when
  exiting.

- ``open(mode=None)``. open or re-open ``File.name`` with optionally new mode.
  return self.

- ``close()``. close file.

- ``chunks(chunk_size=None)``. returns a generator yielding file content by
  ``chunk_size`` or ``File.DEFAULT_CHUNK_SIZE``.

- ``multiple_chunks(chunk_size=None)`` whether requiring multiple chunks to
  exhaust the file.

- ``__iter__()``. iterate file content by line. like file object. 这里识别 CR,
  CRLF, LF 三种 line endings. 这是为了便于处理来自不同 client OS 的文件.

- exposed underlying file-like object's methods.

ContentFile
^^^^^^^^^^^
- File subclass.

- operates on in-memory string or byte sequences, without a backing file.

constructor
""""""""""
- ``content``. initial string or bytes.

- ``name``.

ImageFile
^^^^^^^^^
- File subclass.

- need pillow to get image dimensions.

attributes
""""""""""
- width.

- height.

FieldFile
^^^^^^^^^
- File subclass.

- FileField 使用的文件体对象. FieldFile 是 File 的子类. 具有 file-like object
  API.  区别在于 FieldFile is a wrapper around the result of the
  ``Storage.open()`` method.

attributes
""""""""""

* url.

methods
"""""""

* file-like object methods.

* ``save(name, content, save=True)``. save file to storage backend. 更新
  ``FieldFile.name`` 为保存文件后 storage backend 返回的名称, 这就是文件的最终
  名称或路径. 如果原来文件已经保存, 这里不会删除或替换, 而是简单地创建一个新文
  件. 并更新 model instance 上的列属性为新保存的文件路径.

  这个方法单独来使用时, 可以用于更新文件名. 这时应该使用 ``save=True``, 则在
  storage backend 中以及数据库中的列值都会一起更新.

  - ``name`` 一般为 ``FieldFile.name``

  - ``content`` 一般为 ``FieldFile.file``. 必须为 File instance, 而不是文件内容
    本身.

  - ``save``. 是否调用 ``Model.save`` 保存关联的 model instance.
  
  在保存 model instance 时自动调用该方法以保存文件至 storage backend (在
  ``Field.pre_save`` hook 中调用).

* ``delete(save=True)``. delete file from storage backend, set model instance
  上列属性为 None, 下次获取该列时, 根据 FileDescriptor 逻辑更新为一个空的
  FieldFile. 若 ``save=True``, 调用 ``Model.save`` 更新 model instance.

ImageFieldFile
^^^^^^^^^^^^^^

file storage
------------

utilities
^^^^^^^^^

- ``get_storage_class(import_path=None)``. get ``DEFAULT_FILE_STORAGE`` class
  or storge of import path string.

- ``default_storage`` stores an instance of ``DefaultStorage`` lazy object,
  which resolves to ``DEFAULT_FILE_STORAGE``.

- ``DefaultStorage`` class.

Storage
^^^^^^^
- base storage class.

- Storage subclasses must be deconstructible. 因为要作为 ``FileField`` 参数.

constructor
""""""""""""
- For subclasses, all constructor parameters must be optional. If required,
  must be taken from settings.

methods
"""""""
- ``get_valid_name(name)``. get a file name based on ``name`` that is suitable
  for this storage backend. ``name`` 是一个 potentially invalid name for this
  storage backend. 基本上就是在做 normalization. default implementation retains
  only ``[[:alnum:]._]``.

- ``generate_filename(filename)``. like ``get_valid_name()`` but for file path.
  The filename argument may include a path as returned by
  ``FileField.upload_to``.

- ``get_available_name(name, max_length=None)``. get an available name based on
  ``name``, without exceeding ``max_length``. . The name argument passed to
  this method will have already cleaned to a filename valid for the storage
  system, according to the ``get_valid_name()`` method. If ``name`` is already
  taken, an underscore plus a random 7 character alphanumeric string is
  appended to the filename before the extension.

  If a free unique filename cannot be found, a SuspiciousFileOperation
  exception is raised.

- ``open(name, mode="rb")``. open file from storage by name and mode.
  Returns an instance of File or its subclass.

- ``_open(name, mode="rb")``. Required for subclasses. Called by ``open()``.
  Actual mechanism the storage class use to open the file. Must return a File
  instance.

- ``path(name)``. Required for subclasses that provide local file storage.
  This returns local filesystem path where the file can be opened using Python
  standard ``open()``.

- ``save(name, content, max_length=None)``. save a new file to storage.
  
  * ``name`` is used as file name if not already taken or illegal. Otherwise
    it's modified accordingly to generate an unique name. In any way, the real
    file name is returned as a result of successful file storing operation.

  * ``content`` is an instance of File or a file-like object that is wrappable
    thereof.

  * ``max_length`` is the same as ``get_available_name()``

- ``_save(name, content)``. Required. Called by ``save()``. ``name`` is supposed
  to be already valid, 但是根据存储机制的不同, 仍然可能造成冲突. ``content`` is
  a File instance. Return the actual saved name.

- ``delete(name)``. delete the file referenced by name. If deletion is
  unsupported, just don't implement this.

- ``exists(name)``. check name exists in storage.

- ``size(name)``. file size in bytes.

- ``url(name)``. get file's absolute url.

- ``get_created_time(name)``. get creation time or last changed time of name
  (depending on OS), as datetime.

- ``get_modified_time(name)``. get last modified time of name, as datetime.

- ``get_accessed_time(name)``. get last access time of name, as datetime.

- ``listdir(path)``. list path. return a 2-tuple of lists, the first is
  directories under ``path``, the second is other files. This is non-recursive.

FileSystemStorage
^^^^^^^^^^^^^^^^^

constructor
""""""""""""
- ``location``. absolute path to the directory of this storage. default
  ``MEDIA_ROOT``.

- ``base_url``. absolute base url of files in this storage. default
  ``MEDIA_URL``.

- ``file_permissions_mode``. file's permissions when saving. default
  ``FILE_UPLOAD_PERMISSIONS``.

- ``directory_permissions_mode``. permissions of the necessary intermediate
  directories when it's created. default ``FILE_UPLOAD_DIRECTORY_PERMISSIONS``.

attributes
""""""""""
- ``base_location``. original value of location.

- ``location``. absolutified value of location.

- ``base_url``.

- ``file_permissions_mode``

- ``directory_permissions_mode``

file uploading
--------------
- uploaded files are instances of ``UploadedFile`` and its subclasses, as
  stored in ``HttpRequest.FILES``.

file classes
^^^^^^^^^^^^

UploadedFile
""""""""""""

- subclass of File.

constructor.

- ``file=None``. underlying file-like object.
 
- ``name=None``.
 
- ``content_type=None``.
 
- ``size=None``.
 
- ``charset=None``
 
- ``content_type_extra=None``

attributes

- ``content_type``. The content-type header uploaded with the file.

- ``content_type_extra``. A dictionary containing extra parameters passed to
  the content-type header. This is front-faced-server-specific.

- ``charset``. For ``text/*`` content-type.

- ``size`` overrides ``File.size``. 上传的文件的大小由 FileUploadHandler 在
  完成上传后设置. FileUploadHandler 知道自己接收了多少 bytes.

- ``name``. overrides ``File.name``. a property. 只保留 constructor 输入的
  ``name`` 参数的 basename 部分, 并 truncate 至 255 字符长度.

TemporaryUploadedFile
""""""""""""""""""""""
- subclass of UploadedFile.

- represents file uploaded to a temporary file on disk.

methods
""""""""
- ``temporary_file_path()``. return full path to the temporary file.

InMemoryUploadedFile
""""""""""""""""""""
- subclass of UploadedFile.

- represents file uploaded to memory directly.

SimpleUploadedFile
""""""""""""""""""
- A InMemoryUploadedFile subclass.

- 输入 file content in bytes, file name, file size, content type.

- Mainly useful for testing.

upload handlers
^^^^^^^^^^^^^^^

- Django's default file upload policy is to read small files into memory and
  large files onto disk. based on ``FILE_UPLOAD_MAX_MEMORY_SIZE``.

FileUploadHandler
"""""""""""""""""

attributes

- ``chunk_size``. controls the size of chunks fed into
  ``FileUploadHandler.receive_data_chunk``. default 64KB.

  When there are multiple chunk sizes provided by multiple handlers, Django
  will use the smallest chunk size defined by any handler.

  chunk size should be divisible by 4 and should not exceed 2GB.

methods

- ``handle_raw_input(input_data, META, content_length, boundary, encoding)``.
  Allows an upload handler to completely override the parsing of the raw HTTP
  input, and do it all alone. 这个方法是在对整个 post data 的处理之前进行的.
 
  Return None if upload handling should continue normally, or a tuple of
  ``(POST, FILES)`` if the handler should return the new data structures
  suitable for the request directly.

  * ``input_data`` a file-like object containing post stream.

  * ``META`` is request.META.

  * ``content_length`` length of ``input_data``.

  * ``boundary``. MIME boundary for post data in content-type header.

  * ``encoding``. post data's encoding.

- ``new_file(field_name, file_name, content_type, content_length, charset, content_type_extra)``.
  optional. hook to be called when one file upload is starting. 注意一个 post
  data 中可以包含多个文件上传. called before any data has been fed to any
  handlers.

  * ``field_name`` input field name of the file.

  * ``file_name`` filename provided by browser.
  
  * ``content_type`` content-type provided by browser.

  * ``content_length`` file length provided by browser. None if not provided.

  * ``charset``. None if not provided.

  * ``content_type_extra``. extra info from content-type header.

  raise StopFutureHandlers to prevent subsequent handlers from handling this
  file.

- ``receive_data_chunk(raw_data, start)``. Required. receive a chunk of data
  ``raw_data`` from one upload, for this handler. ``start`` is the position
  in the file where this chunk begins.

  * Returns data to be fed into the subsequent handler's ``receive_data_chunk``
    method. 这可以当作 data filter 使用.
    
  * Return None to short-circuit remaining upload handlers from getting this
    chunk. 例如 MemoryFileUploadHandler 和 TemporaryFileUploadHandler 都有利用
    return None 来避免后面的 handler 重复保存上传的数据.

  * Raise StopUpload or SkipFile when appropriate.

- ``file_complete(file_size)``. Required. hook method called after one file has
  finished uploading. ``file_size`` corresponds to the actual size accumulated
  by all the chunks.

  Returns an UploadedFile that will be stored in request.FILES. Return None to
  indicate UploadedFile instance should come from subsequent handlers.

- ``upload_complete()``. hook to be called when all file uploads are completed.

MemoryFileUploadHandler
"""""""""""""""""""""""
- upload file in memory.

TemporaryFileUploadHandler
""""""""""""""""""""""""""
- upload file to temp file on disk.

exceptions
^^^^^^^^^^
upload handlers can raise the following exceptions.

- StopUpload. raise when upload handler wants to abort entire file uploading
  and post data parsing.

- SkipFile. raise when upload handler wants to skip the current file upload.

- StopFutureHandlers. raise when upload handler do not want future handlers to
  handle a file upload.

model fields
------------
- 注意在删除 model instance 时, file-related field 对应的文件实体不会自动删除.
  需要单独处理.

FileField
^^^^^^^^^

- 文件列. 这是文件体的抽象. 而不仅仅是文件路径, 后者是 FilePathField 的事.
 
- FileField 在数据库中保存文件路径为字符串. 虽然它对应的数据库列是 file path
  string, 但它对应的 model instance attribute 是 ``FieldFile`` 文件体 object.

  * 对于 mysql, 使用 varchar 来存储.

- 数据库中保存的是文件的相对路径, 由 ``upload_to`` + filename 组成, 或者根据
  ``upload_to`` callable 生成. 这是 FieldFile.name

- 在 model instance 上, 通过一个特殊的 FileDescriptor 实现了:

  * set ``File.name`` string 或者 None 或者 File/FieldFile instance 都可以.

  * get 该列属性得到 FieldFile instance. 由于 getter 的逻辑, 即使文件列属性
    设置为 None, 获取时也会转换成一个 (empty) FieldFile instance.

- 在 model instance 保存至数据库时, 该列包含的 FieldFile 会通过 storage backend
  存储.

- 如果需要一次性地修改文件保存的路径, 可以 set ``FieldFile.name``, 然后再
  save model instance. 如果需要系统性地修改, 则使用 ``upload_to`` callable
  form.

- 删除 model instance 时, FileField 对应的文件不会自动删除. 需要手动处理.

options
"""""""

* ``upload_to``. 两种形式.
 
  - 若是 string, a directory string relative to ``MEDIA_ROOT`` (if using
    ``FileSystemStorage``), with ``datetime.datetime.strftime()`` format
    specifiers. 文件体会保存在该目录下.

  - 若是 callable, 应该直接可传入 storage backend 的 ``Storage.save()`` 的文件
    名或路径. 接受以下参数:

    * ``instance``, current model instance.

    * ``filename``, original value of ``FieldFile.name``.

* ``storage``. file storage instance for handling actual storage-related
  operations.

* ``max_length`` is default to 100.

* ``null``. null 选项对 FileField 没有实际意义. 最好设置 False. 因为:

  - FileDescriptor 在值为 None 时生成 empty FieldFile.

  - FileField.get_prep_value 对于 FieldFile 通过 ``str()`` 转换为文件路径.

  - File instance 在 name is None 时给出 string form 为空字符串.

  可以看出, FileField 的数据库值不可能为 NULL, 一定为字符串, 并以 empty string
  代表无文件.

checkings
"""""""""

* 检查不能设置 primary_key 参数.

* 检查 upload_to 必须是相对路径, 不是绝对路径.

methods
""""""""
- ``pre_save(model_instance, add)``. 在这里进行保存文件至 storage backend.
  参考 ``FieldFile.save()`` 进行的一系列操作. 并返回 FieldFile instance 的
  最终形态 (这个 FieldFile 后面在 ``get_prep_value`` 中给出文件路径).

- ``get_prep_value(value)``. If None, return None. 一般不会遇到这个逻辑. 否则
  给出 ``str(value)``. 一般情况下 ``value`` 是 FileField instance, 所以这里
  给出的就是 file name. 由此可知 file field 在数据库交互时转换为文件路径.

ImageField
^^^^^^^^^^

- subclass of FileField, 包含 FileField 的一切功能和相关处理逻辑. 它对应的
  model instance 属性为 ``ImageFieldFile``.

- 它对应的 forms.ImageField 会校验 binary data is valid image. 但 ImageField 本
  身不会校验. 文件处理逻辑和 FileField 相同.

- 使用该列的 model 可以设置相关联的保存图像宽度和高度的列. 这便于获取合适的分辨
  率图像.  例如 preview 和 full image 的区别. height/width fields 的值会根据
  ImageFieldFile 属性自动设置.

options
"""""""

* ``height_field``, ``width_field``. name of field on model where to store
  image height and width.

checkings
"""""""""

* 检查 pillow library 已经安装.

context processors
------------------
- ``django.template.context_processors.media``. 提供 ``MEDIA_URL``.

template tags
-------------
- in ``django.templatetags.static``

get_media_prefix
^^^^^^^^^^^^^^^^
- return ``MEDIA_URL``

settings
--------

- ``MEDIA_ROOT``. 保存用户文件的目录, absolute path. Default ``""``
  (current working directory). Must differ from ``STATIC_ROOT``.

- ``MEDIA_URL``. serve user files. must end in a slash if set to a non-empty
  value. default ``""``.

- ``DEFAULT_FILE_STORAGE``. Default file storage class to be used for any
  file-related operations that don’t specify a particular storage system

- ``FILE_UPLOAD_PERMISSIONS``. a number representing file permissions when
  saving to storage. normally something like ``0oNNN``. default None. thus
  file permission depends on OS behavior, e.g. umask.

  These permissions are not applied to files in ``FILE_UPLOAD_TEMP_DIR``.

  These are also default file permissions of ``collectstatic``.

- ``FILE_UPLOAD_DIRECTORY_PERMISSIONS``. permissions of the directories
  in storage. default None. thus file permission depends on OS behavior, e.g.
  umask.

  These are also default directory permissions of ``collectstatic``.

- ``FILE_UPLOAD_MAX_MEMORY_SIZE``. 会保存在内存中的上传文件的体积上限. 超出
  时, 该文件上传保存在文件系统中. default 2.5MB.

- ``FILE_UPLOAD_TEMP_DIR``. 当文件上传需要临时保存在文件系统中时, 使用的目录.
  默认 None, based on OS. For linux this is ``/tmp``.

  由于 ``/tmp`` 可能还是在内存中, 这样 TemporaryFileUploadHandler 就没什么意义
  了. 可以修改目录为 ``/var/tmp``.

serve files during development
------------------------------

- use ``django.conf.urls.static.static`` to generate urlpatterns suitable for
  serving user files under ``MEDIA_ROOT`` during development. 这个 helper 
  function 只在 DEBUG mode 下管用. 所以在生产中没事.

template
========

general
-------

template backend
^^^^^^^^^^^^^^^^
* django 支持同时配置多个模板 backend engine. 包含 django 自己的模板语言和 jinja2.

* ``settings.TEMPLATES``, 对每种 template engine, 支持以下参数:

  - ``BACKEND``, engine import path,

  - ``DIRS``, 全局模板路径.

  - ``APP_DIRS``, 是否包含考虑各个 app 目录下的模板目录.

  - ``OPTIONS``, 模板引擎参数.

  - ``NAME``, 引擎的名字, 默认是 ``django.template.backends`` 中各 module name.

* ``django.template.loader`` module. 通用的加载模板 api, 对所有 backend 遍历.

  - ``get_template()``, 根据模板路径, 返回 Template instance.

  - ``select_template()``, 在一系列可能路径中选择一个模板.

  - ``render_to_string()``, shortcut function.

* ``django.template.base.Template`` 是各 engine 实现的模板类的父类.

  - ``origin``, Origin object, 包含模板的 debug 信息, ``name`` (模板的路径) 和
    ``template_name`` (加载模板所用的路径即模板名) 以及可能包含 loader.

  - ``render()``, render template with context and request.

* ``django.template.engines`` 包含当前所有 template engines.

* ``django.template.backends.base.BaseEngine`` 所有 backend template engine
  的父类.

  - ``get_template()``

  - ``from_string()``

* ``django.template.backends.django.DjangoTemplates`` backend

  - OPTIONS:

    * ``APP_DIRS``, 访问各 app 下的 ``templates`` 目录寻找模板.

    * ``autoescape``, 对于非 html 模板应设置为 False.

    * ``context_processors``

    * ``string_if_invalid``, 对于 invalid variables 输出的默认值.

    * ``builtins``, 添加 template tag modules 至 builtin tags.

    * ``loaders``

  - 由于历史原因, ``django.template.backends.django.DjangoTemplates``
    engine 是 ``django.template.Engine`` 的 wrapper.
    ``django.template.backends.django.Template`` 是 ``django.template.Template``
    的 wrapper. 传入的 context dict 最终生成 ``django.template.context.Context``
    和 ``django.template.context.RequestContext``.

* ``django.template.backends.jinja2.Jinja2`` backend

  - OPTIONS:

    * ``APP_DIRS``, 访问各 app 下的 ``jinja2`` 目录寻找模板.

    * ``autoescape``

  - jinja2 template 支持在模板内进行复杂的操作, 因此一般情况下不需要指定
    context processor.

* components:

  - engine (``Engine``)

  - template (``Template``)

  - template language

  -  context (``Context``)

  - context processor

  - loader

  体会 django 是如何将用变量填充模板这件事模块化成一个个环节和组件对象的.

context processors
^^^^^^^^^^^^^^^^^^

- callable object, 输入 HttpRequest, 输出需要添加进 template context 的
  dict 值. 它的目的是将通用的 context variables 的 添加过程通用化,
  避免在每个 view 里面都写一遍.  这发生在 ``Template.render()`` method 中,
  真正 render 操作之前. 注意这意味着 context processor 添加的量会覆盖从
  view 传入的量.

- context processor 对于不同 engine 基本上是通用的.

- 初始化 engine 时输入的 processor list 按顺序应用, 这意味着越靠后的输出
  结果优先级越高.

- ``django.contrib.auth.context_processors.auth``:
  ``user``, ``perms``

- ``django.template.context_processors.debug``:
  ``debug``, ``sql_queries``

- ``django.template.context_processors.i18n``:
  ``LANGUAGES``, ``LANGUAGE_CODE``

- ``django.template.context_processors.media``:
  ``MEDIA_URL``

- ``django.template.context_processors.static``:
  ``STATIC_URL``

- ``django.template.context_processors.csrf``:
  ``csrf_token``. django template engine 一定会启用这个, 即使没设置.

- ``django.template.context_processors.request``:
  ``request``

- ``django.template.context_processors.tz``:
  ``tz``

- ``django.contrib.messages.context_processors.messages``:
  ``messages``, ``DEFAULT_MESSAGE_LEVELS``

template context
^^^^^^^^^^^^^^^^

- Context object 在通用 API 中是纯粹的 dict.

template loaders
^^^^^^^^^^^^^^^^

- responsible for locating, loading, and returning Template objects.

- ``django.template.loaders.base.Loader`` 是所有 loader 的基类.

  提供以下 API.

  * ``get_template()``
    调用 ``get_template_sources()`` 和 ``get_contents()``,
    给出对应于输入的模板名的 Template object.

  子类须实现以下方法:

  * ``get_template_sources()``, 对于某个模板路径输入, 获取可能的
    template Origin 列表.

  * ``get_contents()``, 根据可能的 template Origin 获取 template 内容.

- engine 的 ``loaders`` 参数自定义 loaders.
  loaders 中每项可以是 loader import paths, 或者是 a tuple/list of
  loader 路径 + loader 初始化参数.

- ``django.template.loaders.filesystem.Loader``
  使用 ``DIRS`` option

- ``django.template.loaders.app_directories.Loader``
  使用各 app 的 ``templates`` dir.

- ``django.template.loaders.eggs.Loader``
  从 eggs 加载.

- ``django.template.loaders.locmem.Loader``

- ``django.template.loaders.cached.Loader``
  cache 已经加载过的和没找到的 templates. 当 ``DEBUG=False`` 且 ``loaders``
  没有设置时, 这个 loader 是自动加载的.

django template system & language
---------------------------------

* template namespace. 每个 app 下可以有 ``templates/`` 目录, 不同 app 的 templates
  目录在一个 namespace 中, 因此会相互覆盖. 所以需要再创建 ``templates/<app>`` 子目录.

* literals.

  * 支持 scalar literals. 例如 string, integer, float, etc.

  * string literal. 模板的 tag 中出现的 string literal 将原样出现在 html 中, 注
    意这些 string literal 是 verbatim 出现在 html 中, python string 的各种
    ``\`` 转义是不支持的. 或者说, 这些字符串相当于 python raw string.

  * 不支持 list, tuple, dict 等 compound literal values.

* 为了结构清晰, 应该把不同 app 的模板放在各自目录下的 ``templates/<app>/`` 下面.

* template 中 object 的 ``.`` operator 的查找顺序:

  - dict key
   
  - object attribute
   
  - list index.

  若 attribute 是一个 callable, it'll be called with no argument. django
  不允许 callable 输入变量. 数据应该在 view 中计算完成再传入 template 进行渲染,
  而不是在 template 中才计算.

  注意凡是包含 ``__call__`` 属性的变量都会 called, 所以小心, 如果需要直接使用传入
  的量, 但它包含 ``__call__`` 属性. 会得到非预期结果. 例如:
  
  - 不能在模板中直接使用 enum.Enum 类型.

  - **不能在模板中直接使用 model class, 因为会被实例化.**

  This lookup order can cause some unexpected behavior with objects that override
  dictionary lookup. 例如重定义了 ``__getitem__`` (defaultdict), 导致没有 key
  时没有 raise KeyError, 从而轮不到 attribute lookup.

  若最终没有找到, fallback 至 template backend 的 ``string_if_invalid`` option 值,
  默认是空字符串.

* 对于 callable variable, 执行中 raise exception, the exception will be propagated,
  unless the exception has an attribute ``silent_variable_failure`` whose value
  is True, 此时 ``string_if_invalid`` 会被使用. ``ObjectDoesNotExist`` 就是
  这样, 因此获取 model instance 时若不存在会替换.

  The template system won’t call a variable if it has alters_data=True set,
  and will instead replace the variable with string_if_invalid,
  unconditionally. 这是为了防止 render template 时误操作修改服务端状态.
  ``Model.delete()`` ``Model.save()`` 之类的都有设置.

* 在 template 中使用 symbolic url, 即使用 url 的名字, 而不写死 url 路径在模板中.
  这样可以降低 template 和 URLconf 之间的耦合. 在重构 url 结构时, 不需要修改模板
  文件.

* 模板的搜索顺序:

  - ``DIRS`` in ``settings.py``.

  - 若 ``APP_DIRS == True``, 每个 app 目录下的 ``templates/`` 目录.

* 每个 template context 至少包含 "True", "False", "None".

* Django’s template language has no way to escape the characters used for its
  own syntax. 只能使用 ``templatetag`` tag, ``verbatim`` tag, 或把这些字符放在
  context variable 中, 或自定义 tag/filter.

* ``django.shortcuts.render()`` 调用 ``django.template.loader.render_to_string()``
  渲染模板成 string 然后加载至 HttpResponse.

* 模板有四类语法元素, 变量替换 ``{{ var }}``, tag 执行 ``{% tag var1 var2 %}``,
  filter ``{{ var|filter:"sef" }}``, 注释 ``{# comment #}`` (只能单行,
  不允许 newline).

* 模板中 single quote 和 double quote 没有区别, 跟 python 一样.

writing template tags
^^^^^^^^^^^^^^^^^^^^^
- 若设置 tag function 接收 keyword-only argument, 必须设置 ``**kwargs`` 参数.

filters
^^^^^^^

- ``add``

- ``first``

- ``last``

- ``default``

- ``default_if_none``

- ``length``, 返回长度数值, 所以可以进行数值类型的逻辑判断.

- ``length_is``

- ``wordcount``

- ``filesizeformat``

- ``floatformat``

- ``stringformat``

- ``safe``

- ``safeseq``

- ``escape``, when auto-escaping is on, there’s no danger of the escape
  filter double-escaping data – the escape filter does not affect
  auto-escaped variables.

- ``force_escape``, applied immediately and returns a new, escaped string.
  不管有没有已经 escaped.

- ``escapejs``, 不懂.

- ``capfirst``

- ``title``

- ``upper``

- ``lower``

- ``cut(value, arg)``. 删除 ``arg`` 部分. 本质是 ``value.replace(arg, "")``.

- ``addslashes``

- ``striptags``

- ``truncatechars``

- ``truncatechars_html``

- ``truncatewords``

- ``truncatewords_html``

- ``wordwrap``

- ``date``

- ``time``

- ``timesince``

- ``timeuntil``

- ``dictsort``, 支持 ``.`` operator 选择深层 sort key, 例如 ``obj.key|attr``.
  dictsort can also order a list of lists (or any other object implementing
  ``__getitem__()``) by elements at specified index.

- ``dictsortreversed``

- ``divisibleby``

- ``get_digit``

- ``iriencode``

- ``urlencode``

- ``join``

- ``linebreaks`` 根据情景把 ``\n`` 转变成 ``<br/>`` 或 ``</p>``, 最终是包在
  ``<p></p>`` 中的.

- ``linebreaksbr`` 单纯地把 ``\n`` 转变成 ``<br/>``.

- ``unordered_list``

- ``urlize``

- ``urlizetrunc``

- ``make_list``

- ``pluralize``

- ``random``

- ``slice``

- ``slugify``

- ``yesno``

- ``center``

- ``ljust``

- ``rjust``

- ``phone2numeric``

- ``pprint``

tags
^^^^

- ``extends``, 必须是模板中的第一个 tag. extends 的值可以是 string
  从而是模板路径, 或者是 Template object 从而 extends 这个模板.

  路径是基于 template loader 的 root directory 的, 即与 ``get_template()``
  中使用的路径相同. 或者路径还可以是 ``./`` ``../`` 等明确的相对路径起始的,
  此时是相对于本模板的路径的.

- ``include``, 使用当前 context 来 render 所指向的模板, 然后将结果嵌入当前位置.
  与 extends 类似, 支持 Template object. 支持 ``with key=val key2=val2``
  语法向模板中传入额外 context. 支持 ``only`` option, 屏蔽当前 context,
  只传入指定的值或完全没有值.

  注意被 include 的模板和当前模板的渲染是完全独立的, 除了 context 之外, 没有
  任何相关性, 没有共享的状态. 这不是将模板嵌入, 而是将模板的渲染结果嵌入.

- ``load``, 当加载 custom tag/filter library 时, 被加载的项只在当前模板中有效,
  若要在父或子模板中使用, 需要重新加载. 支持 ``from``, 从 module 中加载指定
  的 tag/filter. ``load fil1 tag1 from module``.

- ``block``.

  * 对于扩展而非覆盖整个 block, 可以用 ``block.super`` variable 引用父模板中的
    同名 block 内容.

  * 在一个模板文件中, block definition can be nested. 在 child template 中, 只
    需 overrides/extends parent template 声明的 block 即可. 对于 child template
    中没有重定义的 block, fallback 至使用 parent template 中同名 block 的内容.

  * child template 中对一个 block 的重定义, 可以定义新的 sub block. 从而 grand
    child template 可以选择性重定义 sub block or top-level block.

  * child template 中声明的 top-level block, 若在 parent template 中没有定义,
    则没有作用. 即在预处理时直接被忽略.

  * 使用 ``{% endblock <name> %}`` 增加可读性.

  * template blocks 表达的是模板结构的继承关系, 它本质上是 template language 的
    一个 preprocessing directive. 所有的 block 在 compile time resolve 成为模板
    代码. 此后再也没有 block tag.  在 runtime, 模板代码去 render context, 生成
    页面. 因此, 不能通过某种 runtime 条件判断让 block 出现、消失或重定义.

  * 接上, 若要根据 runtime 条件判断是否重新定义一个 block, 可以用以下方法:

    .. code:: htmldjango

      {% block name %}
        {% if condition %}
          {# redefinition/extension of parent block... #}
        {% else %}
          {{ block.super }}
        {% endif %}
      {% endblock %}

- ``autoescape``, 对于已经标记为 safe 的量, autoescape 不会去操作. 例如
  经过 ``safe``, ``escape`` filter 的量已经被标记为 safe.

- ``comment``, block comment. opening tag 中可以包含 optional note. 这可用于
  例如说明这段代码注释掉的原因.

- ``cycle``, 在循环过程中使用, 循环输出参数. 支持 ``as``, 将循环的当前值赋
  给变量, 在后面使用. 支持 ``silent``, 可以单纯声明 cycle, 而不立即输出值.
  ``{% cycle 1 2 as nums silent %}``

- ``debug``, 输出 debug 信息. including the current context and imported
  modules. 注意由于字符串中包含 ``<...>`` 结构, 但是字符串没有被
  ``conditional_escape()``, 导致直接显示在页面上时浏览器会把有用的信息全都
  当成不认识的 html tag 忽略掉!!! 所以必须配合以下 snippet 来使用::

    <pre>{% filter force_escape %}{% debug %}{% endfilter %}</pre>

  ``<pre>`` 让字符串中的 newline and whitespaces 得以保留. ``force_escape``
  filter 强制 escape 已经被 ``NodeList`` mark as safe (但根本不 safe) 的 debug
  字符串.[SODjTemplateDebug]_

- ``filter``, 将整段内容经过一个或多个 filter.

- ``firstof``, first True value of args. 支持 ``as``, 给变量赋值.

- ``for``, 支持 ``reversed`` option, 反向循环.
  支持 ``empty`` tag, 作为 fallback, 类似 for...else...
  在 for loop tag 中, 可访问以下量:

  * ``forloop.counter``

  * ``forloop.counter0``

  * ``forloop.revcounter``

  * ``forloop.revcounter0``

  * ``forloop.first``, whether is first time

  * ``forloop.last``, whether is last time

  * ``forloop.parentloop``, access parent loop in nested loops.

- ``if``, ``elif``, ``else``, truthy value 即可, 与 python 相同.
  支持 python 相同的 logical operators and comparison operators.
  注意使用 () 是 invalid.

- ``ifchanged``, 它里面的内容或它后面的变量改变时, 才输出. 支持 ``else`` tag,
  即不改变时输出别的.

- ``lorem``, sample data.

- ``now``, now, 可以设置 format. format 可以是 settings 中的预定义量的字符串
  形式. 支持 ``as`` 进行赋值.

- ``regroup``, ``{% regroup <list-of-objs> by <key> as <var> %}``
  生成 a list of namedtuples. 每个 namedtuple 包含 ``grouper`` 和 ``list``
  属性. 注意原来的 list 必须要根据 ``key`` 来排序, 例如可用 ``dictsort``
  filter 来做. ``key`` 可以是 obj 的任何 key, attr, index 等. 相当于 ``obj.key``.

- ``resetcycle``

- ``spaceless``, 删除里面 tag 之间的 spaces.

- ``url``, 模板里的 ``reverse()``, 参数可以是 positional 或 kwargs.
  支持 ``as`` 进行赋值, 此时 ``url`` tag 不输出东西, 只赋值.

- ``templatetag``, 单个 template 语法元素不能通过写在字符串里的方式 escape,
  必须使用这个 tag 加适当参数写出, 或把整块内容放在 ``verbatim`` 里.

- ``verbatim``, verbatim 输出内容.

- ``widthratio``, 不懂.

- ``with``, 用于设置临时值, 或 cache 运算结果. 可以用 kwarg 形式设置多个.

- compile-time & runtime tags

  * compile-time: ``extends``, ``block``

template inheritance
^^^^^^^^^^^^^^^^^^^^

Template inheritance allows you to build a base “skeleton” template that
contains all the common elements of your site and defines ``block``'s that
child templates can override.

Content within a ``{% block %}`` tag in a parent template is always used as
a fallback.

- common design.

  * ``base.html`` 包含网站基本框架结构、样式风格等.

  * ``base_<section>.html`` 包含各自功能部分的各异的基本框架结构、样式风格.

  * 每个功能部分的具体页面去实现所需功能.

escaping
^^^^^^^^
django template 默认 escape output of every variable tag.
template 中的 string literal 没有被 html escape, 而是原样包含在 html 中.

disable auto escaping:

- 在变量级别上, 使用 ``safe`` filter.
  
- 在 block 级别上, 使用 ``autoescape`` tag 来开启或关闭 auto escaping.
  ``autoescape`` tag 的影响包含在 child template 中的同名 block.

- 在代码中, 使用 ``mark_safe()``

安全性问题. 默认对模板变量的 auto-escaping 有助于避免 XSS attack. 若要
disable auto-escaping, 需小心谨慎.

context objects
^^^^^^^^^^^^^^^

- ``Context`` 是一个 stack, 包含多层 context dicts (dict or ``ContextDict``
  instance).

  * ``Context`` wrap context dict. 具有大量 dict-like interface.

  * ``push()`` stack 和 ``pop()`` stack, 以及 ``update()``.

  * ``flatten()`` 返回各层的综合结果为一个 dict. 这也用于 Context object
    之间比较.

- ``RequestContext`` 是 ``Context`` 的子类, 它输入多一个 HttpRequest,
  在 render 时通过 context processor 生成额外的 context variables.

  * 注意 RequestContext 才会调用 context processor, Context 不会.

request and response
====================

* ``HttpRequest``

  - attributes.

    * ``scheme``. http or https. 这里 https 指的不是说 django server 直接接受
      到的请求是 TLS 加密过的 http 流量, 而是说它通过上游服务器 (例如 nginx)
      设置的特定 header 的值判断出这个请求走的 https 协议. 这个加密的请求在
      上游服务器解密后以 plain http 的形式传递给 django server.

    * ``body``. raw request body as bytes string, 这会把 request body 全部
      读入内存. 如果已知 request body 可能非常大, 例如文件上传情况, 则应该避免
      直接访问 raw request body. 反正该处理的 django 的 file uploader 都处理完
      了.

      如果 request body 长度大于 ``DATA_UPLOAD_MAX_MEMORY_SIZE`` 会 raise
      ``RequestDataTooBig`` exception (subclass of SuspiciousOperation).

      ``body`` property 主要用于 raw body handling. 对同一个 HttpRequest,
      只能在以下两种方式中选择一种 body 处理方式:
      
      - 访问 raw ``body``, 进行 manual parsing.
        
      - 使用 ``POST``/``FILES`` 等 property. django 会自动去做 body parsing.
        这包含处理 form data, file upload saving, etc.

    * ``path``. url full path.

    * ``method``. 如果不用 class-based view, 而是用一般的 view function, 则需要
      在函数中区别 method 来进行不同的逻辑:

      .. code:: python

        if request.method == "GET":
            pass
        elif request.method == "POST":
            pass

    * ``encoding``. request body 的 encoding, 即 ``Content-Type`` header 的
      ``charset`` 参数.

    * ``content_type``, ``content_params``.

    * ``GET``. 以 QueryDict 形式保存所有 query string 参数. 不是只有 GET 请求才有.

    * ``POST``. 以 QueryDict 形式保存的 form data, 即通过设置 Content-Type 为
      ``application/x-www-form-urlencoded`` 和 ``multipart/form-data`` 时 POST
      的 body, 但并不包含文件上传部分.

      注意, 前端 form 中留空的部分, 仍然在 form data 中, 其值为 empty string "".
      并不存在 input field 值为 None 的情况. 当这些 empty values 传入 form 后,
      如何转换取决于 form field 的转换规则 (``to_python()``).

    * 在 view 中 ``GET`` ``POST`` 是 immutable 的, 需要先 ``QueryDict.copy()``
      后再修改.

    * ``COOKIES``.

    * ``FILES``. MultiValueDict of ``UploadedFile`` instances.

    * ``META``. 包含所有 request headers 以及基本上当前 server 的全部环境变量.
      header fields 的名字遵从 WSGI environ 格式要求.

    * ``resolver_match``. 回溯这个请求匹配到的 url, view function, 参数, app 等信息.

    * ``session``. 当前 session. set by ``SessionMiddleware``.

    * ``user``. 当前用户. set by ``AuthenticationMiddleware``.

  - methods.

    * ``.get_host()``, 获取请求的服务端 FQDN/IP, 根据 ``X-Forwarded-Host`` 或者
      ``HOST`` request header. 这隐含了对 ``ALLOWED_HOSTS`` 的检查和限制.

    * ``.get_port()``.

    * ``.get_full_path()`` 路径包含 query string.

    * ``.build_absolute_uri(...)`` 包含 scheme, FQDN 等部分的完整 URI.

    * ``.is_secure()``, True if https scheme.

    * ``.is_ajax()``, True if ``X-Requested-With: XMLHttpRequest`` present.
      用于在一些情况下检查跨域 ajax request.

    * file object methods.

  - HttpRequest object is file-like object, 但是只读的, 支持 file object 相关的
    读操作.

* ``QueryDict`` 是 django 对 query string 以及 form data 中存在一个 key 对应
  多个值的情况的 dict 的封装.

  它是 dict 的子类. 具有所有 dict methods. 常见的 dict 操作只获取某个
  key 对应的最后一个值. 若要获取整个 list, 使用 list 类方法.

  methods.

  - ``__getitem__()`` 会 raise MultiValueDictKeyError (subclass of KeyError).

  QueryDict 能处理一个 key 多个值时放在一个 list 中; 但不能重组以明确的
  list index 形式序列化的数组或多维数组参数. 例如 ``array[0]=0&array[1]=1``
  ``array[0][0]=0&array[1][1]=1``. 可使用
  https://github.com/bernii/querystring-parser.git 提供的操作解决.

* ``HttpResponse``

  - constructor 可传入 byte string, 或者 iterator, 作为初始相应 body.
    无论哪种, 以及之后的 write 操作来 append, 所有相应都全部载入内存
    再提交至底层. 若要避免这种方式, 例如处理大文件, 使用 ``StreamingHttpResponse``
    或子类.

  - HttpResponse is file-like object, 注意是 write-only stream, not readable,
    not seekable.

  - 支持 mapping protocol (dict-like interface), 对 headers 进行操作.
    header keys are case-insensitive.

  - attributes.

    * ``content``. bytestring of response body.

    * ``charset``. charset of response ``Content-Type``.

    * ``status_code``.

    * ``reason_phrase``. 根据 status_code 给出的 reason, 除非明确设置.

    * ``streaming``, False.

    * ``closed``.

  - methods.

    * ``.set_cookie()``

    * ``.delete_cookie()``, 本质是设置一个 max_age=0, expires 在过去时间的
      cookie, 传给浏览器从而删除 cookie.

    * ``.getvalue()``

    * mapping protocol methods.

    * file object methods.

* HttpResponse subclasses.

  - HttpResponseRedirect (302 -- Found)

  - HttpResponsePermanentRedirect (301 -- Moved Permanently)

  - HttpResponseNotModified (304 -- Not Modified)

  - HttpResponseBadRequest (400 -- Bad Request)

  - HttpResponseNotFound (404 -- Not Found)

  - HttpResponseForbidden (403 -- Forbidden)

  - HttpResponseNotAllowed (405 -- Method Not Allowed)

  - HttpResponseGone (410 -- Gone)

  - HttpResponseServerError (500 -- Internal Server Error)

* ``JsonResponse`` 可以方便地生成 json response. 它使用 ``DjangoJSONEncoder``.
  若要返回 json array, 必须设置 ``safe=False``.

* ``StreamingHttpResponse``

  - 用于传输很大的 response body.

  - 需要用 iterator 来初始化, 这个 iterator 最好不加载所有内容至内存.

  - attributes.

    * ``streaming_content``

    * ``streaming``, True.

* ``FileResponse``
  FileResponse expects a file open in binary mode.

* 无论是 ``HttpResponse`` 或 ``StreamingHttpResponse`` 都是 ``HttpResponseBase``
  的子类. 在 HttpResponseBase 中实现了一部分 file-like object interface,
  这是为了让 WSGI server 去使用, 即把 response 当作 file-like object 使用.

  这里有一点是非常重要的. WSGI-compliant server 必须在结束本次 request/response
  cycle 时, 调用 response 的 ``.close()`` method. 相应地, ``HttpResponseBase``
  的 ``.close()`` 会将传入自身的所有 closable objects 都关闭掉.

  这不但对进程重用 fd 避免 reach max opened files limit 很重要.
  更关键的是, 对于为了 response 而生成的临时文件, 这是最简单的删除方式.
  搭配 unnamed temporary file, 我们可以在 file closed 的同时, 内核自动
  释放硬盘资源.

static files
============
- package ``django.contrib.staticfiles``.

- django 的静态文件功能属于 contrib package, 而不是 core functionality, 这是因
  为只有研发时才需要通过 django 去 serve static files, 生产时通过前端服务器
  serve static files.

app configs
-----------

``django.contrib.staticfiles.apps.StaticFilesConfig`` 包含了以下设置

- ``ignore_patterns``. 默认的 ignore patterns.

settings
--------

- ``STATIC_URL``. the base url for identifying static file requests. This can
  be used in both development and production, but in different ways.
  default None.

- ``STATICFILES_FINDERS``. a list of finders used by staticfiles. Default is
  ``'django.contrib.staticfiles.finders.FileSystemFinder'`` and
  ``django.contrib.staticfiles.finders.AppDirectoriesFinder``. 前者负责
  ``STATICFILES_DIRS``, 后者负责每个 app 中的 ``static`` directory.

- ``STATICFILES_DIRS``. The directories the ``FileSystemFinder`` will use to
  find static files. 这些目录用于放置 non-app-specific static files.

  This is a list of directory strings or a list of ``(namespace, directory)``
  tuples. 第二种语法用于定义 namespace. 否则的话, ``STATICFILES_DIRS`` 中的每个
  路径同属于一个 namespace 下.
  
  default is empty list.

- ``STATICFILES_STORAGE``. file storage engine to use for ``collectstatic``
  management command. default ``django.contrib.staticfiles.storage.StaticFilesStorage``.

- ``STATIC_ROOT``. This is the root directory where ``StaticFilesStorage`` and
  subclasses will use to store collected static files.  Ready to be served by
  django or other web server. 这个需要配合 ``STATICFILES_STORAGE`` 使用.
  
  注意这个目录不是源代码目录里保存静态文件的.

  default None.

placement of static files
-------------------------
如果使用默认的 ``STATICFILES_FINDERS``, 则执行以下静态文件放置策略:

- app-specific 的静态文件要放在 ``<app>/static/<app>/<filename>``.
  这样一个 app 的静态文件和它的代码在一起, 模块化更好.

- 全局的静态文件可以选择两种放置方法:

  * 放在全局的 ``STATICFILES_DIRS`` 中, 例如 ``$BASE_DIR/static``.

  * 放在项目 app 中, ``<project-name>/static/<filename>``.

serve static files
------------------
- 在研发时, 如果没有使用 ``django.contrib.staticfiles``, 则只能 serve 固定目录
  下的静态文件, 例如 ``STATIC_ROOT`` 下的静态文件.

  需要手动添加必要的 urlpatterns 来 serve static files:

  .. code:: python

    from django.conf.urls.static import static

    urlpatterns += [
        *static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    ]

- 在研发时, 如果有在使用 ``django.contrib.staticfiles``, 则有两种 serve static
  files 的方式:

  1) 使用 staticfiles 提供的 ``runserver`` command 来运行研发服务器的话, 无需
  手动配置静态文件相关的 urlpatterns. runserver command 会自动截取 ``STATIC_URL``
  prefix 的请求.

  2) 若没有使用它提供的 ``runserver`` 来运行研发服务器, 且还需 django serve static
  files, 可类似上述配置 urlpatterns, 手动添加 ``STATIC_URL`` 至 urlconf:

  .. code:: python

    from django.conf.urls.static import static
    from django.contrib.staticfiles.views import serve

    urlpatterns += [
        *static(prefix=settings.STATIC_URL, view=serve)
    ]
    # or

    from django.contrib.staticfiles.urls import urlpatterns as staticfiles_urls

    urlpatterns += staticfiles_urls

  无论哪种, staticfiles 会调用 ``STATICFILES_FINDERS`` 来获取静态文件. 这种方式在
  寻找静态文件时具有比较好的灵活性, 适合源代码仓库使用.

- 在生产时, 使用 ``collectstatic`` 将静态文件聚集在一起放在 ``STATIC_ROOT``,
  使用 nginx 来高效地 serve 静态文件.
  
  还可以使用其他非 filesystem-based static file storage backend, 例如 CDN.

finders
-------
- ``django.contrib.staticfiles.finders.searched_locations`` saves a list of
  searched paths for static files.

storage backends
----------------
- all static storage backends are based on ``django.core.files.storage.Storage``

StaticFilesStorage
^^^^^^^^^^^^^^^^^^
- subclass of ``django.core.files.storage.FileSystemStorage``

- ``STATIC_ROOT`` as ``FileSystemStorage.location``

- ``STATIC_URL`` as ``FileSystemStorage.base_url``

- 对原有的 FileSystemStorage 改动比较小, 效果是
  
  * 在 ``STATIC_ROOT`` 中保存的文件即 ``collectstatic`` 收集到的文件
    
  * 目录权限使用 ``FILE_UPLOAD_PERMISSIONS`` 和 ``FILE_UPLOAD_DIRECTORY_PERMISSIONS``.

ManifestStaticFilesStorage
^^^^^^^^^^^^^^^^^^^^^^^^^^
- subclass of StaticFilesStorage, with ManifestFilesMixin.

- 对它保存的每一个文件, 保存一份文件名包含 MD5 hash 的 copy, 并且替换部分文件内
  容, 保证静态文件中引用的其他本地静态文件路径也是包含 hash 的版本.

- During ``post_process()`` of ``collectstatic``, the storage backend
  automatically replaces the paths found in the saved files matching other
  saved files with the path of the cached copy.

- The purpose of this storage is to keep serving the old files in case some
  pages still refer to those files, e.g. because they are cached by you or a
  3rd party proxy server. Additionally, it’s very helpful if you want to apply
  far future Expires headers to the deployed files to speed up the load time
  for subsequent page visits.

- ``post_process()`` 最后会保存原始文件名路径至 hashed 文件路径的映射至
  ``STATIC_ROOT/staticfiles.json``. 这样在 runtime 渲染模板时才能生成正确的
  静态文件路径.

class attributes
""""""""""""""""
- ``patterns``. 包含需要替换的文件 glob pattern 以及需要替换的内容 re patterns.
  默认是替换 css 文件中的 ``@import`` and ``url()`` rules.

- ``max_post_process_passes``. 如果每次遍历都对某些文件进行了修改, 对所有文件最
  多遍历这么多次.

- ``manifest_strict``. default True. 此时, 若在 runtime 要求获取的文件不在
  ``staticfiles.json`` 中, raise ValueError. 否则, 给出原始文件路径.

attributes
""""""""""
- ``hashed_files``. 保存源文件路径至 hashed 文件路径的映射. storage 初始化时,
  从 ``staticfiles.json`` 中读取已知的映射关系至内存.

methods
""""""""

- ``url(name, force=False)``. overrides ``FileSystemStorage.url()``. 在 DEBUG
  mode 下, 且 ``force=False`` (即一般外部调用方式), 给出 unhashed path url. 否
  则给出对应于 hashed path 的 url.

- ``file_hash(name, content=None)``. create the hash of ``name`` containing
  ``content``. subclass can override this to use a custom hash.

CachedStaticFilesStorage
^^^^^^^^^^^^^^^^^^^^^^^^

- subclass of StaticFilesStorage, with CachedFilesMixin.

- 类似于 ManifestStaticFilesStorage, 但是使用 cache framework 来存储等价于
  ``staticfiles.json`` 的一个映射关系.

- 这个 storage backend 比 ManifestStaticFilesStorage 要慢, 因为它每次读写都需要
  访问 cache, 就要走网络.

- 若在 ``settings.CACHES`` 可设置 ``staticfiles`` 即单独给静态文件使用的 cache,
  否则 fallback to ``default``.

attributes
""""""""""
- ``hashed_files``. 这是一个 proxy object to cache. 读写都会去访问 cache.

template tags
-------------

- 使用 ``static`` template tag 来自动根据 ``STATIC_URL`` 生成 static file
  的 url, 不要把静态文件的 url 写死在 html 里. 这样, 真正的 url 会根据
  ``STATICFILES_STORAGE`` 的机制去生成, 这样只需要设置
  ``StaticFilesStorage`` 或 某个 CDN 的 storage 实现, 就可以轻易切换所有
  url 的指向, 真正做到了单一变量没有重复.

  ``static`` tag 支持 ``as``, 只赋值不输出.

- ``get_static_prefix``, 获取 STATIC_URL, 自定义 url 补全, 支持 ``as``.

- ``get_media_prefix``

context processors
------------------

- ``django.template.context_processors.static``. 提供 ``STATIC_URL``.

template tags
-------------
- ``django.templatetags.static``

- 需要 ``{% load static %}``

static
^^^^^^
* return url corresponding the specified static file.

* 若没有使用 staticfiles package, 直接 prefix path with ``STATIC_URL``.

* 若有使用 staticfiles package, delegate to ``{STATICFILES_STORAGE}.url()``.

get_static_prefix
^^^^^^^^^^^^^^^^^
- return ``STATIC_URL``

views
-----
- ``django.contrib.staticfiles.views.serve(request, path, insecure=False, **kwargs)``

  * view static files that are findable by ``STATICFILES_FINDERS``.

  * intended as a local development helper, only works in DEBUG mode or
    ``insecure=True``.

  * calls ``django.views.static.serve()`` view internally.

- ``django.views.static.serve(request, path, document_root=None, show_indexes=False)``

  * use ``mimetypes`` to guess mimetype.

testing
-------
- ``django.contrib.staticfiles.testing``

StaticLiveServerTestCase
^^^^^^^^^^^^^^^^^^^^^^^^
- subclass of ``django.test.LiveServerTestCase``.

class attributes
""""""""""""""""
- ``static_handler``. override parent's setting. 使用与 ``runserver``
  相同的 ``StaticFilesHandler``, 后者使用 ``serve`` view. 从而可以 serve
  finders 能找到的静态文件.

management commands
-------------------

collectstatic
^^^^^^^^^^^^^
::

  ./manage.py collectstatic

- collect static files based on ``STATICFILES_FINDERS``, and put them in
  ``STATICFILES_STORAGE``.

- If there are duplicated files in the same namespace, the first found is used.

- By default, If ``STATIC_ROOT`` is not empty, files are copied only if they
  have a modified timestamp greater than the timestamp of the corresponding
  file in ``STATIC_ROOT``. Use ``--clear`` to remove existing files.

- files are collected according to ``STATICFILES_FINDERS``.

- The collectstatic management command calls the ``post_process()`` method of
  the ``STATICFILES_STORAGE`` after each run and passes a list of paths that
  have been found by the management command.

- options.

  * ``--ignore PATTERN``, ``-i PATTERN``. ignore matched files/directories
    during collectstatic. can be specified multiple times.

  * ``--dry-run``, ``-n``.

  * ``--clear``, ``-c``. clear existing files before collecting new files.

  * ``--link``, ``-l``. symlink instead of copying. only useful for local
    storage.

  * ``--no-post-process``. do not call ``post_process()`` of storage backend.

  * ``--no-default-ignore``. 不要忽略一些默认的常见 glob pattern, 例如备份
    文件.

findstatic
^^^^^^^^^^
::

  ./manage.py findstatic staticfile [staticfile ...]

- all matching locations are found.

- options.

  * ``--first``. get first only.

runserver
^^^^^^^^^
- override django.core.management 提供的 ``runserver`` command, 提供
  自动 serve 以 ``MEDIA_URL`` 为 prefix 的静态文件请求.

- options.

  * ``--nostatic``. disable serving static files.

  * ``--insecure``. serve static files even if DEBUG is false.

admin site
==========

* If the builtin admin site doesn't suit your need, just rewrite it yourself.

* admin site app 是 ``django.contrib.admin``, 它依赖于 ``django.contrib.auth``,
  ``django.contrib.contenttypes``, ``django.contrib.messages``,
  ``django.contrib.sessions``.

* When you put 'django.contrib.admin' in your INSTALLED_APPS setting, Django
  automatically looks for an admin module in each application and imports it.

* 整个 project 使用同一个 ``AdminSite`` instance, 它或者是默认的
  ``django.contrib.admin.sites.site`` instance, 或者是在项目中某全局处实例化的.
  将这个 instance 的 urls 加入 project's URLconf.

* 对一个 app 的 admin site 的自定义在 ``admin.py`` 中进行.

* 用 ``AdminSite.register()`` method 将需要在 admin site 中进行编辑的 models
  包含在 admin site 中. 可以创建 ``ModelAdmin`` 子类来自定义展示方式. 此时,
  还可以使用 ``admin.register`` decorator 进行注册.

* model 里各个 field 的名字和类型直接影响它们在 admin.site 的显示和交互方式.

* 在新增用户页面, 必须先创建用户 (通过指定 username/password) 之后才能修改用户
  的其他信息.

* 用户必须有对 User model 的 add 和 change 权限, 才能真正有创建用户权限. 这是
  一个安全机制, 为了防止 permission elevation.
  If you give a non-superuser the ability to edit users, this is ultimately
  the same as giving them superuser status because they will be able to
  elevate permissions of users including themselves!

* 用户密码只显示 hash 值 (数据库只知道 hash 值). 并提供修改密码的连接.

* ModelAdmin.

  - ``actions``.

    * ``ModelAdmin.actions`` list 控制批量编辑操作. list 元素可以是
      操作函数/方法的名字字符串或 callable 本身.
      ``.short_description`` attribute 定义它在 action list 中显示的操作名.
      设置 ``actions = None`` 可禁用所有批量操作.

    * ``ModelAdmin.get_actions()`` 可以在 per-request 级别上控制允许的
      action list.

    * ``AdminSite.add_action()`` 给 admin site 的所有对象的 action list
      添加操作.

    * ``AdminSite.disable_action()`` 禁用全局操作.

  - ``date_hierarchy`` 添加一个按照日期进行条目筛选的组件.

  - ``fields``, ``fieldsets``, ``exclude`` 定义哪些列显示, 哪些不显示.

    对于 ``fields``, 若要多列显示在一行, 将这些列放在一个 tuple 中:
    ``(('a', 'b'), 'c')``.

    对于 ``fieldsets``, 格式为 a sequence of ``(name, field_options)``.
    field options 中, ``fields`` key 的值与 ``ModelAdmin.fields`` 一致;
    ``classes`` key 的值是一系列 css classes; ``description`` 是对 fieldset
    的描述.

    If neither ``fields`` nor ``fieldsets`` options are present, Django will default
    to displaying each field that isn’t an ``AutoField`` and has ``editable=True``,
    in a single fieldset, in the same order as the fields are defined in the model.

  - ManyToManyField 在 admin 界面上默认显示为 ``<select multiple>``, 当选项太多
    时多选很不方便, ``filter_horizontal`` ``filter_vertical`` 提供了方便的多选
    交互方式.

  - ``form`` 属性自定义要使用的 ``ModelForm`` 子类. ``get_form()`` method 是最终
    获取 form class 的 entry point. 所以我们可以直接使用另一个 form 类, 或者在
    获取 form 时再根据情况进行自定义.

  - ``inline`` 定义一系列 inline 编辑的 models. 它们是 ``InlineModelAdmin`` 的子类.

  - ``list_display`` 定义要在批量编辑列表中显示的列. 它的值可以是 model 的列, 也可以
    是给出动态值的 callable (可以给 callable 列设置 header). 不设置这个属性时,
    编辑列表显示一列, 其值为 ``str(instance)``.

    Usually, elements of ``list_display`` that aren’t actual database fields can’t
    be used in sorting (because Django does all the sorting at the database level).

    The field names in list_display will also appear as CSS classes in the
    HTML output, in the form of ``column-<field_name>`` on each <th> element.
    This can be used to set column widths in a CSS file for example.

    注意 list_display 不能是 related object 的列, 但能通过 callable 来解决这个问题.
    此时注意给 callable 附上恰当的 ``short_description`` 和 ``admin_order_field``.

  - ``list_display_links`` 设置哪些列可以进入详情.

  - ``list_editable`` 设置在批量编辑页面中可以直接 inline 编辑的列.

  - ``list_filter`` 控制右侧边栏 filter widget, 这里提供了很多修改方式.

  - ``ordering`` 控制 change list 的排序. 默认使用 model 本身的默认排序方式.

  - 存在多个选项的列, 例如 ``choices``, ``ForeignKey`` 可以通过 ``radio_fields``
    设置为 radio button.

  - ``raw_id_fields`` 是另一种进行 select 的界面.

  - ``readonly_fields`` 只读列. ``get_readonly_fields()`` 动态自定义最终返回
    的 readonly fields.

    * 设置某属性在新建时是需要输入的, 在修改时是只读的:

      .. code:: python

        def get_readonly_fields(self, request, obj=None):
            if obj is None:
                return self.readonly_fields
            else:
                return self.readonly_fields + ("some_field",)

  - ``search_fields`` 设置一些可以搜索的列 (包含 related field lookup), 此时
    change list 上面有搜索框.

  - 很多配置项可以设置 AdminSite 级别的全局值, ModelAdmin 级别的 model 局部值,
    值, callable 列级别的独立值.

  - 各种操作的页面模板可以通过相应属性设置为自定义的模板.

* InlineModelAdmin

  - TabularInline
    一个 inline object 的各 field 是作为 column 出现的, 从而每个 inline object
    在页面上只占一行.


  - StackedInline
    一个 inline object 的各 field 是作为 row 出现的, 从而每个 inline object
    在页面上占多行, 各 object 之间再添加额外一行 object 描述进行分隔.

settings
========

* NEVER deploy a site into production with ``DEBUG`` turned on.

* In debug mode, ``ALLOWED_HOSTS == []`` 时, 只允许一些本地 ``HTTP_HOST`` header,
  localhost, 127.0.0.1, ::1.

  当作为 nginx 的上游服务器时, django 部分本应局限在本地, 并不依赖于服务器 IP.
  此时 ``ALLOWED_HOSTS`` 可以只设置为本地 IP, 将 Host header 的访问安全性限制在
  nginx 层解决, 然后 nginx 去重写 HTTP_Host 为本地.

  若 HTTP_HOST 不在 ALLOWED_HOSTS 中, raise SuspiciousOperation, return 400.

* ``UST_TZ`` determines whether datetime objects are naive.

signals
-------

setting_changed
^^^^^^^^^^^^^^^
django 在以下位置设置了相关的 event handler:


design pattern
--------------
- the section describes how to design django settings in a flexible way that
  works across different environment.

- Why need this? once you start setting up your Django app on multiple
  environments; like production, testing, and staging — and on machines for
  developers, you are likely to run into a pain point; managing the
  configuration across the different environments.

settings subpackage
^^^^^^^^^^^^^^^^^^^

- ``settings`` 拆分成 ``settings`` subpackage. 内含 ``base.py``,
  ``production.py`` 和 ``local.py`` 三个 modules.

  * ``base`` settings 包含在不同环境下都需要的公共的、基础的配置项部分.

  * ``production`` 和 ``local`` settings 分别是生产环境和研发环境需要的配置部分
    .

- 无论是哪个 settings 配置文件, 意义在于两点:

  * 确定各个环境下所需的配置项是哪些.

  * 对于无需根据不同环境进行修改的配置项, 设置固定配置值. 对于可能需要根据具体
    情况设置的配置项, 设置默认值, 并可从环境变量 (以及 env file) 中获取实际配置
    值.

- 实际使用哪个 settings 文件, 根据环境变量 ``DJANGO_SETTINGS_MODULE`` 来自动决
  定.

- 如果某个环境需要修改配置项或者默认配置值, 修改相应的 settings 文件. 如果某个
  环境需要修改配置项的实际配置值, 不修改 settings 文件, 修改环境变量. 这样,
  settings files 实际是一部分固定的配置 + 一部分模板化的配置.

settings in env file
^^^^^^^^^^^^^^^^^^^^

- use ``django-environ`` to facilitate configuration.

- ``.env.example`` 包含全部可配置项, 以及示例值. 此文件用于表示 env file 的格式
  以及支持的配置项. 提示用户该文件只用于格式说明.

- 在使用时, 用户添加一个 ``.env`` 文件在项目根目录, 填入需要配置的配置项, 使用
  ``.env.example`` 中的示例格式. ``.env`` 文件不加入版本管理.

- ``.env`` 文件在研发、测试、生产等不同环境下设置, 用于设置该具体实例下使用的
  配置值.

- 当我们使用 docker 时, 根据不同的服务启动方式, 有以下方式加载 env file 至
  app process environment 中.

  * one-off app container: ``docker run --env-file``

  * single swarm service: ``docker service create --env-file``

  * services defined in composefile (swarm stack 以及 docker-compose):
    ``env_file`` key.

settings in environment
^^^^^^^^^^^^^^^^^^^^^^^

- ``.env.example`` (从而 ``.env``) 文件中的配置项还可以通过设置环境变量来临时修
  改.  例如, 在生产环境, 临时设置 ``DEBUG=True``.

- 在使用 docker 时, 根据不同的服务运行方式, 选择合适的临时环境变量传入方式.

migration
=========

overview
--------
- Database migrations is a version control system for your database schema.

  ``makemigrations`` is responsible for packaging up your model changes into
  individual migration files - analogous to commits - and ``migrate`` is
  responsible for applying those to your database.

- Django will make migrations for any change to your models or fields - even
  options that don’t affect the database. the only way it can reconstruct a
  field correctly is to have all the changes in the history.

- django 生成的 migrations 需要仔细检查, 对于复杂的数据库修改, 不能保证与预期完
  全相符, 必要时需要人工修改甚至人工创建 migrations. 对于自动生成的 migrations,
  尤其是 ``squashmigrations`` 生成的 migration file, 一定要测试可用.

compatibility
^^^^^^^^^^^^^
- Migration system is backward-compatible according to the same policy as
  django. 即同一个 major version 下的能保证向后兼容. 旧版本生成的 migration
  file 能在新版本中使用, 但反之没有保证.

migration workflow
------------------

* Make changes to your models.

* run ``makemigrations``. Models will be scanned and compared to the versions
  currently contained in migration files, and then a new set of migrations
  will be written out.

* 检查生成的 migration file 中操作是否符合预期.

* After the model and migration are tested and run as expected, commit the
  migration and the models change to your version control system *as a single
  commit*. (理想情况如此, 实际上必须配合单元测试和/或集成测试才能做到, 因为
  data model 是否合适, 是需要在业务逻辑中使用中才能切实体会出来的.)

* 在极端情况下, 例如对 app models 的修改积累的 migration files 已经非常多,
  例如几千个以上, 可以用 ``squashmigrations`` 将历史整合.

migration files
---------------
- Migration files are used to declare migration operations.

- Migration file 名字中的序号部分对 django 并无意义, 只对人类有用. Django order
  migration files by dependencies specified in each file.

- migration files 中的 string literal 要统一使用 unicode string 或 bytestring.
  这不仅是一般的 py2py3 统一性要求. 在 django 中, 若要 app 同时兼容 py2py3.
  必须这样做. 因为, py2 默认 bytestring, 这样应用在数据库中的是 bytes,
  同样的代码在 py3 下运行时, 由于 django 看见都是 unicode string, 而数据库中是
  bytes, 这样要再生成一个 migration 去修改现有数据库结构至支持 unicode string.

* 若要在 migration 中删除/重命名某个 model 或者删除它的数据, 必须设置
  dependency 保证依赖于原 model 和数据的 migration 执行在先.

* Migration 大致分为 schema migrations & data migrations.

  - schema migrations 大部分情况下可以依赖 makemigrations 自动生成.

  - data migrations 必须手写, 涉及例如 ``RunPython``, ``RunSQL`` 等操作.

  schema migrations & data migrations 最好分成不同的 migration file 来写. 这样
  的好处是:
  
  1) 清晰 (显然);
  
  2) 对每个 Migration, MigrationExecutor 会将它包裹在 SchemaEditor 的 context
  下. 这个 context 对于 transactional DDL backend 生成一个 transaction. 对于
  postgresql, 若一个 transaction 中同时有 schema change 和数据修改, 会报错. 而
  对于 nontransactional DDL backend, 虽不会生成 transaction, 但在 context exit
  时仍需要执行一些 defered sql, 若在 data migration 中出错 raised exception, 就
  可能导致 schema change 不完整.

* Initial migration. The “initial migrations” for an app are the migrations
  that create the first version of that app’s tables.

migration definition
--------------------
- A ``Migration`` class in migration file, which is a subclass of
  ``django.db.migrations.Migration``.

- Each migration operation is an instance of  ``Operation`` class.

- 在 migration 中无法访问 model 中定义的 methods. 解决办法是在 migration 中
  再定义一遍. 由于 migration 只代表在确定历史状态下的操作, 所以这种重复不造成
  问题.

Migration
^^^^^^^^^

class attributes
""""""""""""""""

- ``initial``. Whether the migration is an initial migration. There can be
  more than one initial migration for an app, in case of complex model 
  dependencies, etc.

  default is None. migration will be considered “initial” if it is the first
  migration in the app.

  makemigrations 生成的 initial migration 具有 ``initial=True``.

- ``dependencies``. a list of 2-tuple of ``(app_name, migration_name)`` that
  it depends on.

- ``operations``. a list of ``Operation`` performed by this Migration.

- ``run_before``. a list of 2-tuple of ``(app_name, migration_name)`` that
  depends on this Migration. 这是用于, 当不能修改 child migration 的依赖关系
  的时候. 例如 child migration 实际上是 third party library 提供的.

- ``replaces``. a list of 2-tuple of ``(app_name, migration_name)`` that this
  Migration replaces. 如果这是一个 squashed migration.

- ``atomic``. whether to wrap the whole migration in a transaction. default
  True. 但是, 注意如果 backend (e.g., mysql) 不支持 transactional DDL, 则
  SchemaEditor 还是不会使用 transaction.

migration operations
--------------------
- Operation 实例有三个主要功能:

  * 负责将自身所包含的操作映射为对 model state 的修改. 从而完成 model state 历
    史的正向和反向演进. 这个 model state 的保持对自动生成新的 migration 和
    squash migration 等操作都是关键的. 这主要通过调用 ProjectState methods 完成.

  * 负责将自身所包含的操作映射为对数据库状态的修改. 从而完成真正的正向和反向数
    据库操作. 这主要通过调用 SchemaEditor 完成.

  * 负责在 squashmigrations 时生成 squashed operation.

- 了解 Operation 的意义在于两方面:

  * 会写 data migration 和其他更复杂的情况处理.

  * 会读自动生成的 schema migration, 能够判断是否正确. 若否, 能够纠错.

Operation
^^^^^^^^^
- base class of all Migration Operations.

attributes
""""""""""
- ``reversible``. whether the operation can be run in reverse. 若不能, 应设置
  False.

- ``reduces_to_sql``. whether the operation can be represented as a SQL
  statement. RunPython can not, because it may involves arbitrarily complex
  logic.

- ``atomic``. Whether it should be forced to wrap the operation in an atomic
  transaction. 例如, mysql 不支持 transactional DDL, 所以默认情况下每个 Migration
  并没有创建单独的 transaction. 而对于 data migraiton, 我们最好使用 transaction.
  这时需要设置这个为 True.

- ``elidable``. 在 squash migration 时, 这个 operation 与其他进行优化时, 能否直
  接忽略这个 Operation.

methods
""""""""
- ``deconstruct()``. Operation must be deconstructible. 因为在 squashmigrations 时
  需要重新写入.

- ``state_forwards(app_label, state)``. Mutate ProjectState forwards. After
  mutation, ProjectState matches what this migration would perform.

  * ``app_label`` is the app belonged.

  * ``state`` is a ProjectState.

- ``database_forwards(app_label, schema_editor, from_state, to_state)``. mutate
  database state forwards.

  * ``app_label``. the app belonged to.

  * ``schema_editor``.

  * ``from_state``. ProjectState before this operation.

  * ``to_state``. expected ProjectState after this operation.

- ``database_backwards(app_label, schema_editor, from_state, to_state)``. ditto
  backwards.

- ``describe()``. a description of what this operation does. output during
  makemigrations.

- ``references_model(name, app_label=None)``. for squashmigrations.

- ``references_field(model_name, name, app_label=None)``. for squashmigrations.

- ``allow_migrate_model(connection_alias, model)``.

- ``reduce(operation, in_between, app_label=None)``. Return a list of
  Operations this operation and the passed in operation should be squashed
  into. Or True/False indicates 是否可以跳过这个 ``operation`` 继续尝试后面的
  operations 继续优化.

model operations
^^^^^^^^^^^^^^^^

CreateModel
"""""""""""
- During migration, create a model in ProjectState, and a corresponding table
  in database.

- constructor.

  * ``name``. model class name.

  * ``fields``. a list of 2-tuples of ``(fieldname, field_instance)``.

  * ``options=None``. a dict of model's Meta options.

  * ``bases=None``. a list of base concrete models. can be actual model class
    or those in string format (to use historical version). If None, use django
    Model.

    This is normally None if no explicit base other than Model is defined.

  * ``managers=None``. a list of 2-tuples of ``(manager_name, manager_instance)``
    to use during migration (``use_in_migrations``). The first one is default
    manager during migration. If None, a default is created normally during
    migration as normal.

    This is normally None if no explicit manager is defined.

DeleteModel
"""""""""""
- Delete a model from ProjectState and table from db.

- constructor.

  ``name``. model name.

RenameModel
"""""""""""
- Rename model and its table.

- constructor.

  * ``old_name``

  * ``new_name``

- 如果 MigrationAutodetector 将 rename 操作识别成了 DeleteModel + CreateModel,
  则需要手动改成这个.

AlterModelTable
""""""""""""""""
- Change only ``db_table`` of Meta option.

- constructor.

  * ``name``.

  * ``table``.

.. TODO can not fully comprehend its meanings

special operations
^^^^^^^^^^^^^^^^^^

RunPython
""""""""""

constructor.

- ``code``. a callable accepting two positionals:

  * a ``django.apps.registry.Apps`` instance that has the historical versions
    of all your models loaded into it to match where in your history the
    migration sits;

  * a ``SchemaEditor`` that can be used to manually effect database schema
    changes.

    当在 RunPython 中使用 SchemaEditor 时, 只该做以下两类操作:
   
    - django 本身的 schema migration 系统功能之外的 schema 或其他数据库结构改动.
      例如创建存储过程.

    - 当需要进行特殊的 schema change 与 ProjectState mutation, 这些修改无法用
      builtin django migration operations 来表达. 而且更可能是一次性的 (否则何
      不封装一个 custom Operation subclass).

    避免在 RunPython 中做手动的在 django 管理范围内的 schema changes. 这样的修
    改不是由 DDL Operation 声明的, migration framework 在生成 historical model
    state 时不会考虑, 这会导致数据库状态与 migration subpackage 记录不一致,
    MigrationAutodetector will fail to work.

  需要访问 model 时, 应该使用从当前 ProjectState 生成的 Apps registry. 这样才符
  合相应历史点的状态. 但这样获取的 model 具有一定限制. See `project state`_.

- ``reverse_code=None``. ditto for backwards migration.

- ``atomic=None``. 注意不是 False. 默认是 None.

- ``hints``. a dict of hints passed to ``allow_migrate()`` of db router.

- ``elidable``. whether elidable.

attributes.

- ``reversible`` is True if ``reverse_code`` is not None.

static methods.

- ``noop(apps, schema)``. provides a convenient noop operation to make this
  operation reversible.

methods.

- ``states_forwards()``. does nothing. no state change for
  RunPython.

- ``database_forwards()``. execute ``code``

- ``database_backwards()``. execute ``reverse_code`` if there is one.

About transaction.

- If SchemaEditor is not atomic (either because backend does not support DDL
  transaction or ``migration.atomic=False``), but the operation is deemed
  atomic (``operation.atomic or (migration.atomic and operation.atomic is not False)``),
  a transaction is opened for RunPython exclusively.

- Otherwise no additional transaction is opened.
  
因此在 postgres 中, 默认不会单独创建 RunPython 自己的 transaction. 使用 Migration
level 的 transaction.

RunSQL
""""""
.. XXX 对于 schema change, 什么时候使用 RunSQL, 什么时候使用 RunPython 的
   schema editor?

- 对于 Schema change, 如果能够提供相应的 state operations, 则应该提供.

project state
-------------

ProjectState 重建的 model 不同于当前源代码中声明的 model.

* 生成的 model 具有相应历史点的 fields, relationships, managers (包括
  ``use_in_migrations``) 以及 Meta options.

* Functions in field options, custom model managers (``use_in_migrations``),
  custom model fields, 以及 model class 的 concrete base model 是以 reference
  形式引用的. So the functions and classes will need to be kept around for as
  long as there is a migration referencing them.
  
  若后续需要修改相应的源代码, 原始版本要保存下来, 例如直接扔到要使用它的
  migration file 里面; 如果后续完全不再需要相应的 function or class, 可以
  squashmigrations, 消除 migration 中对它们的引用, 然后从源代码中删除掉.

* Custom class attributes and methods are not restored and thus not
  accessible. 这是因为不能 serialize arbitrary python code.

* signal handlers are not called properly. 因为注册的 ``sender`` model
  与重建的实际上并不是一个.

database backend notes
----------------------

MySQL
^^^^^
- schema migration (DDL) 与 data migration (DML) 应该放在不同的 migration 中执
  行. 避免在一个 migration 中同时包含 DDL & DML 操作.

  因为 DDL statements will implicitly commit transactions, 这导致如果一个
  migration 先 DML, 再 DDL, 但是 DDL 部分 failed, 则需要手动 rollback
  DML 做的修改.

deconstruction and serialization
--------------------------------
- 生成 migration file, 需要将内存中的 model changes (注意对比的是从 python
  source code 解析至内存中的 python 对象和数据结构) 反向 serialize 成 python 源
  代码. 由于并不存在对 python object 序列化的通用标准 (注意序列化的要求是等价性
  , 无信息损失), django 只对有限的、容易序列化的对象定义了 serialization 逻辑.

- 这些可序列化的值具有的特点大致分为以下几类:

  * 具有 literal form 的, 这主要是 builtin types.

  * 可直接 import 的定义. 例如 class, function.

  * 可获取对象包含的数据值, 并可通过 constructor 直接重建的.

  * 包含 deconstruct API 的对象.

- 可 serialize 的值:

  * values of builtin python types.

  * datetime instances.

  * decimal.Decimal instances.

  * enum.Enum instances.

  * uuid.UUID instances.

  * functools.partial, functools.partialmethod instances with serializable
    function and args/kwargs.

  * django LazyObject wrapping serializable value.

  * django model field instances.

  * Any function or (unbound or bound) method reference. 注意 instance is
    lost. 只剩下 class. Must be accessible from module top-level scope.

  * Any class. Must be accessible from module top-level scope.

  * Anything with a ``deconstruct()`` method.

- 不可 serialize 的值:

  * inner class. (找不到)

  * arbitrary class instance. (无法保证序列化后信息无损, 除非作者通过
    ``deconstruct()`` 来告诉 django 怎样的信息是足够重建原实例.)

  * bound method, including classmethod, instance method.
    .. XXX why not even classmethod?

  * lambda. (找不到定义)

deconstructible protocol
^^^^^^^^^^^^^^^^^^^^^^^^

- ``deconstruct()``. 具有这个 method 的任意 object, django 会去 deconstruct.
  在 class 中定义这个方法就是告诉 django 这个类的实例都是 deconstructible 的.

  Returns a 3-tuple ``(path, args, kwargs)``. ``path`` is import path to class;
  ``args`` is a list of positionals and ``kwargs`` is a dict of kwargs to pass
  to class constructor. Each subvalue must be serializable.

  这是用于 deconstruct 任意 class instance 的, 而 ``Field.deconstruct()`` 
  returns 4-tuple.

- ``__eq__(other)``. called by Django’s migration framework to detect changes
  between states. A new migration is generated if the instances are not equal.
  注意并不是在任何 migration 相关的地方使用 deconstructible instance 时, 都会
  通过 ``__eq__`` 来判断相等.

decorator
^^^^^^^^^

- ``@deconstructible(klass=None, path=None)``. class decorator. overrides
  original class's ``__new__`` to capture args and kwargs; provides a
  ``deconstruct()`` method.

  只要 original class 的 constructor params 全部 deconstrucible, 就可以使用
  这个 decorator. 省去一些麻烦.


migration checkings
-------------------
- Checking history consistency. 如果数据库中保存的 applied migrations history
  与根据 migration files 生成的 migration directed graph 对比后, 发现有些已经
  应用的 migration 的依赖项反而没有应用, 则认为存在 consistency problem.

migration signals
-----------------
post_migrate
^^^^^^^^^^^^
- At the end of ``migrate`` and ``flush`` management commands, 对于每个
  registered 并且有 models.py 模块的 app, 发送一次 ``post_migrate`` signal.

- 该 signal 表示参数对应的 app 已经 migrate 完成, 可以进行 post migration 处理
  了.

- 在发送 ``post_migrate`` signal 时, 所有 apps 早已初始化完成, app registry
  (Apps) 早已初始化完成, 且已经完成 database migrations. 

- 发送 ``post_migrate`` signal 是在 ``emit_post_migrate_signal()`` 中进行的.

- Handlers of this signal must not perform database schema alterations. 若需
  数据库操作, 只该是 data manipulation.

- arguments:

  * sender. 完成 migration 的 app's AppConfig.

  * app_config. ditto.

  * verbosity. same as ``manage.py migrate``'s the very same flag.

  * interactive. same as ``manage.py migrate --noinput`` flag.

  * using. db alias used.

  * plan. migration plan used by ``migrate`` command.

  * apps. An app registry containing the state of the project after the
    migration run. Use this instead of global app registry.

settings
--------
- ``MIGRATION_MODULES``. a dict of app name to migration subpackage path.  When
  specifying app name in ``makemigrations``, the corresponding subpackage will
  be created if not exist.

  If subpackage path is None, Django will skip the app's migration altogether
  even if it has one.

management commands
-------------------

showmigrations
^^^^^^^^^^^^^^
::

  ./manage.py showmigrations [app_label]...

- show all migrations in a project.

- options.

  * ``--list`` list migrations organized by app. This is default.

  * ``--plan`` show migrations in the order they'll be applied, with verbosity
    of 2 and above, all dependencies of a migration will also be shown. This
    looks very useful.

makemigrations
^^^^^^^^^^^^^^
::

  ./manage.py makemigrations [<app_label>]...

- 执行原理.
  
  * 首先检查数据库中的 migration history 是否与 migration subpackage 的一致.

    检查的数据库包含所有配置的数据库 (如果具有 db router 配置) 或 default.
    检查的内容包括: 数据库中已经应用的 migration 部分是完整的, 与 migration
    subpackage 中保存的应用顺序 (即依赖关系) 是相符的. (并不要求数据库中已经
    应用了全部 migration.)

  * 根据 migration subpackage 中的全部修改历史, 重新构建出一套已经记录的最新
    models 情况在内存中. 与 ``models.py`` 中的当前 models 状态进行比较, 生成
    合适的 migration 操作以能够达到当前 models 状态, 保存在 migration files 中.

- Providing one or more app names as arguments will limit the migrations
  created to the app(s) specified *and any dependencies needed*.

  ``makemigrations`` 和 ``migrate`` 操作一般不要限制 ``app_label``, 要对所有
  apps 同时进行. 因为 model 之间经常是相互依赖的. 如果只对某个 model 更新数据库
  状态可能 break dependency.

- ``--dry-run`` 可用来检查当前记录的数据库结构 (通过 migration files 来体现)
  是否和 models 里的模型代码保持一致.

- ``--empty`` create an empty migration file, for manual editting. 这经常用于
  data migration.

- ``--name``. specify name of the generated migration file. 可用于指定该
  migration 的目的、内容等, 常用于 data migration.

- ``--merge``. Fix migration conflict.

migrate
^^^^^^^
::

  ./manage.py migrate [<app_label>] [<migration_name>]

- apply migration, forward or backward.

- 在正向 migration 时, 一般应避免指定 app name. 这有可能导致非直接依赖的数据库
  结构没有得到应用. 造成数据库状态不完整.

- 若指定了 ``migration_name``, 是将数据库状态确定在某个 migration 相应的状态上.
  若当前状态已经新于指定的状态, 则 unapply necessary migrations.

- 操作原理 (大致).

  * 首先检查数据库中的 migration history 是否与 migration subpackage 的一致.

  * 根据命令行生成 migration plan. forward or backward, 是否指定了应用范围 (
    app name 和 migration name). migration plan 根据从 migration subpackage 构
    建的 migration directed graph 数据结构得出.

  * 按照顺序应用每个 ``Migration``. 对于每个 Migration, 依次执行定义的
    ``operations``. 对每个 ``Operation``, 定义了一系列执行逻辑.

- ``--database``. 在多数据库情况下, 指定使用的数据库.

- ``--fake-initial``. 如果 apps' initial migrations 对应的表名已经存在,
  则不真正应用 initial migration, 假装已经应用了. Make sure that the current
  database schema matches your initial migration before using this flag.

squashmigrations
^^^^^^^^^^^^^^^^
::

  ./manage.py squashmigrations <app_label> [start_migration] <end_migration>

- Squash the migrations of app name, starting from the initial migration or
  the ``start_migration`` until ``end_migration`` (included).

- ``squashmigrations`` 主要用来将过多的 migration 历史合并成一个等价的
  "squashed" 版本. Squashing is the act of reducing an existing set of many
  migrations down to one (or sometimes a few) migrations which still represent
  the same changes.

- The recommended workflow for squashing migration:

  * squash, keeping the old files, commit and release
   
  * wait until all systems are upgraded with the new release.
   
  * Deleting all the migration files it replaces.
  
  * Updating all migrations that depend on the deleted migrations to depend
    on the squashed migration instead.
  
  * Removing the ``replaces`` attribute in the Migration class of the squashed
    migration.

  * Once you’ve squashed a migration, you should not then re-squash that
    squashed migration until you have fully transitioned it to a normal
    migration.

- squash 逻辑. 根据起止 Migration (即 directed graph 上的两个 vertex), 从
  directed graph 中得出需要 squash 的 migration list. 提取所有 Operation.  传入
  optimizer, 进行优化. 优化时, 对每个 operation, 尝试与它后面的所有 operation
  依次优化合并. 对于每个 operation, 调用 ``Operation.reduce()``. 反复执行直到优
  化结果不再变化. 将优化结果写入新的 migration file, 成为 squashed migration.
  在写 migration 的过程中, 涉及对 Operation 的 deconstruction & serialization.

- migration 逻辑.  The squashed migration's ``replaces`` attribute says what
  migrations it replaces.  They can coexist with the squashed migration files.
  Django will intelligently switch between the original migrations and the
  squashed migration depending 根据当前项目实例的 migration 执行进度来决定. If
  the instance is still part-way through the set of migrations that were
  squashed, it will keep using them until it hits the end and then switch to
  the squashed history, while new installs will just use the new squashed
  migration and skip all the old ones.

- 当数据库结构之间的关系比较复杂时, 慎用 squash migration. 最好检查 squash 的结
  果是否符合当前 models 结构.

- options.

  * ``--no-optimize``. disable optimization. useful if django's optimization is
    incorrect.

  * ``--squashed-name``. specify the name of the squashed migration. default use
    ``<start_migration>_squashed_<end_migration>``.

sqlmigrate
^^^^^^^^^^
::

  ./manage.py sqlmigrate app_label migration_name

- Prints the SQL for the named migration.

- options.

  * ``--backwards``. Print SQL for unapply the migration.

  * ``--database DATABASE``. specify database to generate SQL.

recipes
-------

- How to move model between apps, without losing any data?
  possibly with foreign key constraints?
  possibly with many-to-many field constraints?
  possibly with one-to-one field constraints?

  目前 django 没有提供直接可用的方式去做 model 跨 app 的迁移. 基本解决思路是
  两种:

  1. 不动数据, 想办法通过修改表结构、重命名等方式将 django 的状态和数据库的结构
     修改至预期的状态.
     根据要迁移的 model 的复杂程度, 这种方式实现时的复杂程度各有不同. 若没有
     foreign key, 则还比较简单. 若有 foreign key 则复杂一些, 若有 many-to-many
     field, 会非常复杂 (目前我尚未梳理清晰解决办法).

     参考:
     基本方案: https://stackoverflow.com/a/26472482/1602266
     要移动的 model 有 foreign key field: https://stackoverflow.com/a/29622570/1602266
     有 foreign key 指向要移动的 model: https://stackoverflow.com/a/30613732/1602266
     要移动的 model 有 many-to-many field: 没有现成答案, 我觉得需要首先将
     many-to-many field 转换成 through model, 然后迁移 through model.

  2. 创建新数据库结构, 迁移数据, 删除旧数据库结构.
     这种方式相比上述方式简单很多. 非常适合数据量不大的情况 (也许 10K~100K).
     只需手写 data migration 逻辑, 用 ``RunPython`` 执行即可, 注意要设置正确
     的 migration 依赖顺序. 按照先创建新的, 迁移, 再删除旧的, 这个顺序创建
     migration. 第一个和最后一个 migration 都可以通过修改 models 来自动生成.

- Change nullable field to non-nullable. 根据不同需求有两种办法

  * specify a default on model field or a one-time default.

  * create manual migration. 根据业务逻辑先将不合适的列值替换掉, 再
    makemigrations ALTER TABLE.

- add a non-nullable field without default to existing model. 步骤:

  * 先创建 nullable field 或使用某个默认值的 field.

  * create manual migration, 根据业务逻辑修改数据.

  * ALTER TABLE to non-nullable, 添加其他所需条件, 例如 UNIQUE.

- Making non-atomic data migrations. 如果要修改的数据非常多, 可能希望
  不使用整体性的 atomic migration (``Migration.atomic == False``), 而是
  使用 batch modification. 对于每个 batch, 放入一个 transaction.

session
=======

* Session data is stored on the server side. 在客户端, session 通过 session ID
  cookie 进行标识. client-server 通信只传递带 session id 的 cookie, 避免敏感信息
  泄露.

* session app: ``django.contrib.sessions``
  middleware: ``django.contrib.sessions.middleware.SessionMiddleware``

* 默认配置下, session 是写入数据库的 ``django_session`` 表.
  ``SESSION_ENGINE`` 控制使用的 session backend.
  session 有多种 backend 选择: cache, cached_db, db, file, signed_cookies.

  若使用 cache 存 session, 根据 django 文档, 此时应该用 memcached 作为
  cache backend. It'll be faster to use file or database sessions directly
  instead of sending everything through the file or database cache backends.
  The local-memory cache backend is NOT multi-process safe.

* SessionMiddleware 生成 ``request.session`` attribute, 它是一个 dict-like object
  (mapping protocol), instance of ``backends.base.SessionBase``.

* ``SessionBase``

  - SessionBase 是各个 session backend (``SESSION_ENGINE``) 中 ``SessionStore``
    的父类. 每一个 SessionStore instance 就是一个 session data.

  - 各个 session engine 统一使用了 SessionBase 提供的 session data 编码解码方式,
    即各个 session engine 存储的 session data 格式是统一的.

  - attributes

    * ``session_key``, session data 唯一标识, readonly.

      对于 db-based session, 这是存储在 session cookie 中的值,
      即唯一传递至客户端的 session 信息.

    * ``modified``, session data 是否被修改过. 修改 ``request.session``
      时, 该属性自动设置 True. 从 view function 返回之后, SessionMiddle
      会根据该属性值来 ``.save()`` session 以更新或新建 session entry;
      并在 response 中加入 ``Set-Cookie`` header, 更新/设置 session cookie.

  - methods

    * ``__init__()``, 传入现有 session key, 从 backend 创建 session 实例.

    * mapping protocol methods

    * ``flush()``, delete session data. SessionMiddleware 随后会设置 response
      去删除客户端的 session id cookie (设置 Set-Cookie header 的过期时间在过去).

    * ``create()``, 在 session engine 中创建保存了当前 session data 的新 session
      entry. 生成唯一的 session_key.

    * ``save()``, 用当前数据更新现有 session entry 或者生成新 session entry.

    * ``set_expiry()``, 若没有调用该操作, 将使用全局的 expiry policy,
      涉及 settings.SESSION_COOKIE_AGE.

    * ``get_expiry_age()``

    * ``get_expiry_date()``

    * ``get_expire_at_browser_close()``

    * ``clear_expired()``

    * ``cycle_key()``, 对同一个 session data 赋值新的 session key.
      login() 调用这个操作, 以解决 session fixation attack.

    * ``set_test_cookie()``, ``test_cookie_worked()``, ``delete_test_cookie()``
      测试客户端浏览器是否接受 cookie. (测试流程可以封装成 middleware?)

  - 各个 backend 的 SessionStore 要实现以下方法, ``exists()``, ``create()``,
    ``save()``, ``delete()``, ``load()``, ``clear_expired()``.

* session dict 中, ``_xx`` 形式的 key 是 django 内部使用的.

* ``db`` backend

  - ``Session`` model, 代表数据库中的 session entry.
    Session model 仅对 db backend 有意义.

* Note that the session cookie is only sent when a session has been created
  or modified.

* settings.

  - ``SESSION_COOKIE_AGE`` 设置全局的 session cookie ``max_age`` 参数值.
    该值默认为 2 weeks.

  - ``SESSION_ENGINE``, 设置 session backend.

  - ``SESSION_SAVE_EVERY_REQUEST``, 是否每个 request 都更新 session.

  - ``SESSION_EXPIRE_AT_BROWSER_CLOSE``, 设置 session id cookie 是否是
    (browser-) session cookie, 即只持续当前浏览器 session.

  - ``SESSION_COOKIE_SECURE``. session cookie 使用 secure cookie.

* 只有用户明确 logout 时, 才会主动从 session store 中删除这条 session entry
  (通过 ``logout()``). 对于 persistent session store, session 从不自动删除,
  即使过期. 因此需要定期执行 ``clearsessions`` 命令删除过期 session.
  对于 cache-based session store, 显然不存在这个问题.

cache framework
===============
- django 包含两种 cache 机制:

  * server 端 cache. 由 django web service 自己控制的 cache server. 就像数据库一样,
    可以在代码逻辑中任意方式使用.
  
  * downstream in-path cache. 通过 cache control 类的 HTTP headers 指示 downstream 
    n-path cache system (例如 CDN) 或者浏览器本地缓存该如何进行缓存. 这样的交互主要
    则局限很多, 主要应用在页面或静态文件的加速读取上面.

  两种 cache 机制各自有不同的适用性, 并不能相互替代.

- 对于 server 端 cache, django 提供多种精度的缓存控制.

  * per-site cache.

  * per-view cache.

  * template cache.

  * low-level cache APIs.

- django builtin 提供了几种 server-side cache backend 的封装.

  * memcached.

  * database cache.

  * filesystem cache (file-based).

  * local memory cache.

  * dummy cache (fake cache).

- django-redis package 提供了 redis 作为 cache backend 的封装. See
  `django-redis`_.

settings
--------

- ``settings.CACHES``. a dict of caches, mapping cache alias to its config
  dict. 若不设置, 默认只设置 ``default`` cache, 使用 ``LocMemCache`` backend.

  如设置该参数, 必须设置一个 ``default`` cache.

  对于每个 cache, config dict 内容:

  * BACKEND.

  * LOCATION. 指定 cache 的路径. depending on backend, this may use different
    format.

  * KEY_FUNCTION. function that derives the final cache key from input prefix,
    version and key name.

  * KEY_PREFIX. cache key's prefix string.

  * TIMEOUT. cache content expire time.

  * OPTIONS. backend-specific option dict.

  * VERSION. default version number of keys.

cache backends
--------------
- ``django.core.cache.caches`` 保存着根据 settings.CACHES 生成的一组 cache
  backend instances. It's an instance of ``CacheHandler``.

- ``django.core.cache.cache`` is a proxy to ``default`` cache. It's an instance
  of ``DefaultCacheProxy``.

memcached
^^^^^^^^^
- Two memcached backend implementations, based respectively on,
  python-memcached and pylibmc.

BaseMemcachedCache
""""""""""""""""""

MemcachedCache
""""""""""""""

PyLibMCCache
""""""""""""

form
====

- form & form fields 与 model & model fields 是对应的, 并且是紧密联系的.

Form
----

* ``django.forms.Form`` 是 form handling 的核心. A ``Form`` class describes
  a form and determines how it works and appears.

- form methods.

  * ``is_valid()`` method 验证 form data 是否合法并清理数据设置 ``cleaned_data``.
    在背后, 它调用所有 fields 的验证和数据清理逻辑.

* 很多对象 render 为 html 形式后会添加标识 id 和样式 class. 方便进行前端自定义.

* When we instantiate a form, we can opt to leave it empty or pre-populate it.

constructor options
^^^^^^^^^^^^^^^^^^^

- ``initial``. 设置 form fields 的初始值. 这些初始值会 override field definition
  中的初始值. (instance-time options override class definition-time options.)

class attributes
^^^^^^^^^^^^^^^^
- ``declared_fields``. declaratively defined fields. An OrderedDict.

- ``base_fields``. all fields. For normal Form, this is the same as
  ``declared_fields``. For ModelForm, 包含 declared fields and auto-generated
  fields. Also An OrderedDict.

attributes
^^^^^^^^^^
- ``errors``. 获取 Form 的错误信息. 若未验证, 自动调用 ``Form.full_clean()``
  验证 form.

methods
^^^^^^^

cleaning & validation
""""""""""""""""""""""
- ``is_valid()``. Check whether or not the form is valid. If the form is
  not validated yet, 访问 ``errors`` property 的操作会自动进行验证.

- ``full_clean()``.

- ``clean_<fieldname>()``. form-level clean & validation on a specific
  field. 对于一个列, 如果它的某部分 clean & validation 逻辑不是仅仅对列值
  自身进行验证, 而是需要一些 form-level 的考量, 或者某些相关的外部信息,
  则可以放在这里. 注意这里仍然是关于这个列单独去考虑时具有的 clean &
  validation 逻辑. 若涉及多个列的关系, 应该放在 ``Form.clean()`` 中.

  在调用该方法时, ``<fieldname>.clean()`` method is called already, 因此
  ``Form.cleaned_data`` 中相应位置已经转换成了相对于列定义而言是合法的
  数据格式.

  该方法 return cleaned field value, or raise ValidationError.

- ``clean()``. Custom Form 若要进行 form-level 的 clean & validation (而不是
  form field-level), 可自定义这个方法. 

  这里的验证应该满足以下原则: 当所需的各个 fields 已经通过 field-level
  clean & validation 时, 也即在 ``cleaned_data`` 中存在时, 才进行验证.
  否则直接返回原数据即可.

  If valid, return a new ``cleaned_data`` or None (``cleaned_data`` is modified
  in-place). If invalid, raise ValidationError, 它会加入 NON_FIELD_ERRORS.

- ``non_field_errors()``.

- ``add_error()``.

field visibility
""""""""""""""""
- ``hidden_fields()``

- ``visible_fields()``

form rendering
^^^^^^^^^^^^^^

* 永远不要在 django form 中添加 css styling 信息. 记住, django form 是业务逻辑
  的数据部分的后端抽象, 它必须与前端展示逻辑解耦合. CSS styling 要放在模板中.

  考虑到要和各种前端框架的 element 结构层级、样式定义结合, 直接把整个 form
  或者 field 按照默认的 html 代码输出很多时候是不实际的. 
  
  解决方法:
  
  - 如果使用 vanilla django, 只能仔细在 html 代码中定义好结构和样式,
    只用模板变量填入必要的信息.

  - 使用 django-widget-tweaks 来更方便地调整 widget 样式. 或者参考使用
    django-material 等风格 plugin.

* ``str(form)`` 即获得 form instance 对应的 html 代码. 注意 rendered Form
  instance 不包含 ``<form>`` element wrapper 和 submit button.

* ``form.non_field_errors`` 是全局错误. When rendered as html, 成为 ul
  element ``<ul class="errorlist nonfield">``. ``nonfield`` class 与
  ``BoundField.errors`` 进行区分.

* 也可以 ``form.as_table`` ``form.as_p`` ``form.as_ul``.

* render 后, 每个 input field 的 ``id`` attribute 是 ``id_<field-name>``.

* ``form[<field-name>]`` 是各个 field 对应的 ``BoundField``.

bound and unbound form
^^^^^^^^^^^^^^^^^^^^^^
``is_bound`` 属性判断是否 bound.

- unbound form: no data. when rendered, being empty or containing only default
  values.

- bound form: has data. can tell if data is valid, 若数据非法, 会生成
  相应的错误信息, 可填入模板, 返回给用户.

Form clean & validation
^^^^^^^^^^^^^^^^^^^^^^^
- Form cleaning and validation 可通过几个点触发:

  * call ``is_valid()``
  
  * access ``errors`` property
  
  * call ``full_clean()``

- Form 的 clean & validation 整体逻辑由 ``full_clean()`` 控制. 遵从以下步骤:

  * clean & validation of form fields ``_clean_fields()``. 对每个 field,

    - 调用 ``Field.clean()`` 进行 form field 定义的 clean & validation logic.

    - 调用 form-level 定义的 ``clean_<fieldname>()`` method, 若有定义.

    若以上任一方法 raise ValidationError, 记录错误至 ``Form.errors``.
    停止该 field validation, 进行下一个 field validation.

  * clean & validation of form in general ``_clean_form()``.

    - 调用 ``Form.clean()`` 进行 form-level 整体 clean & validation.

    这里的 ValidationError 会加入 NON_FIELD_ERRORS, ``clean()`` 返回的
    data 会设置为新的 ``Form.cleaned_data``.

  * post clean & validation hook ``_post_clean()``.
    See `model form clean & validation`_.

  以上三步中, 任何一步 raise ValidationError 只会记录下来, 不影响其他步骤的执行.

- 在 clean & validation 之后, 最终的有效 form data 只能从 ``Form.cleaned_data``
  获取. ``Form.cleaned_data`` 中只包含成功 cleaned 的 field data 部分. 因此
  在各个地方使用时, 要考虑到所需 field 可能不存在.

form inheritance
^^^^^^^^^^^^^^^^

- ``Form`` 类继承时, 父类的列在先, 子类的列在后. 对于多继承, 列的先后顺序
  根据各父类的远近关系按由远至近的顺序. 这里的远近关系值的是在 MRO 中的顺序
  的逆序, 在 MRO 中越靠后越远.

- 若要删除从父类继承的某个列, 设置它为 None.

ModelForm
---------

- ``ModelForm`` 是 ``Form`` 的一种, 它根据现成的 model 去生成 form.

* 当一个 form 与某个 model 对应时, 使用 ``ModelForm``, 否则使用 ``Form`` 即可.

- 指定所使用的 ``Model``, 它会 build a form, along with the appropriate fields
  and their attributes, from a Model class. 省去手动写 field 的麻烦.

- The generated Form class will have a form field for every model field
  specified, in the order specified in the fields attribute.

Meta options
^^^^^^^^^^^^

specifying fields
"""""""""""""""""
- ``fields``. 设置 model form 中包含的列. ``'__all__'`` 自动包含所有列.

  It is strongly recommended that you explicitly set all fields that should
  be edited in the form using the ``fields`` attribute. Failure to do so can
  easily lead to security problems when a form unexpectedly allows a user to
  set certain fields, especially when new fields are added to a model.

- ``exclude``. 排除一些列. ``fields`` 和 ``exclude`` 必须设置至少一个.

field customization
"""""""""""""""""""
- ``widgets``. A dict mapping from field name to widget class or instance.
  Customize widgets.

- ``labels``.

- ``help_texts``.

- ``error_messages``.

- ``field_classes``. Customize field class.

localization
""""""""""""
- ``localized_fields``.

constructor options
^^^^^^^^^^^^^^^^^^^

- ``instance``. 将 form 与一个现存的 model instance 关联, 为了更新它的 一些列.
  这样, 在 clean & validation 时, 可能会修改传入的 model instance. 若验证失败,
  传入的 model instance 可能处于 inconsistent state, 不适合再次使用.

  instance 上的各列值与 ``initial`` 参数的初始值, 合并在一起, 作为 BaseForm
  的 ``initial`` 参数, 即作为 Form 的初始值. ``initial`` 的值 overrides
  ``instance`` 上的值.

  注意, instance 上原来的列值不会作为 form field 的默认值. form 上 required
  以及有默认值的列等等仍然必须按照 form 本身的要求进行填充. instance 上原来
  的列值是用于维持不在 model form 中进行修改的属性的值.

class attributes
^^^^^^^^^^^^^^^^

attributes
^^^^^^^^^^

- ``instance``. 对于 bound model form, form clean & validation 之后, 生成的
  model instance 会保存在这里.

  Any fields not included in a form will not be set by model form. 这些列的值
  可通过在 ModelForm, Model 等的 hooks 中设置, ModelForm 的 ``initial`` 参数
  设置, 或者在 model field 层的 ``default``.

methods
^^^^^^^

- ``.save(commit=True)``

  保存 model form 关联的 instance to database (通过 ``Model.save()``).
  If the form hasn’t been validated, calling ``save()`` will do so by checking
  ``form.errors``.

  ``commit=False`` 时并不将数据存入数据库, 而是只返回 model instance.
  若 model 存在 ManyToManyField 需要修改或创建, ``commit=False`` 显然
  不会创建在 form 中选定的那些关联. 这样, 若手动执行 ``Model.save()``
  来保存实例的话, 之后需要使用 ``ModelForm.save_m2m()`` 单独保存选定
  的关联关系至数据库.

  若 model 中定义了 ``FileField`` 且 form 中传入了相应文件, ``.save()``
  会自动将文件保存至 ``upload_to`` 位置.

Auto-generated fields
^^^^^^^^^^^^^^^^^^^^^

- The generated Form class will have form fields corresponding to model field
  specified, in the order specified in the fields attribute.

- ModelForm 自动生成的 form field 与 model field 的映射关系, 以及默认选项设置由
  ``models.Field.formfield()`` 方法决定.
  
  几个比较值得关注的映射, 从 model field 至 form field:

  * ``AutoField``, ``BigAutoField`` 不映射.

  * ``TextField`` -> ``CharField``, widget 为 ``forms.Textarea``.

  * ``ForeignKey`` -> ``ModelChoiceField``. 参数默认值:

    - ``queryset``: remote model default manager's all.

    - ``to_field_name``: ``ForeignKey.to_field``.

  * ``ManyToManyField`` -> ``ModelMultipleChoiceField``.

  比较值得关注的一般性的 form field options 与 model field option 的决定关系.

  * ``required``. ``blank=True`` 则 ``required=False``. 由于默认 Field option
    ``blank=False``, 因此默认 ``required=True``.

  * ``label``. ``verbose_name`` capitalized.

  * ``choices``. 若 model field 有 choices, form field ``widget`` 默认是
    ``Select``. 选项的设置逻辑:

    - 如果 ``blank=True``, 即允许不选择. 因此包含 empty choice 项.
      此时, 如果没有 ``default``, 默认选择 empty choice; 如果有 ``default``,
      默认选择 default.

    - 如果 ``blank=False``, 即不允许不选择. 此时, 如果有 ``default``, 不包含
      empty choice, 默认选择 default; 如果没有 ``default``, 仍包含 empty
      choice 并默认选择, 这是为了强制用户进行选择, 否则后端 form 校验时会
      报错.

  * ``initial``. 如果有 ``default``, 使用该值或者 callable.

  * ``empty_value``. If ``null=True``, ``empty_value=None``.

Custom fields
^^^^^^^^^^^^^
- Additional fields can be declared in ModelForm class namespace
  declaratively as a normal Form.

- 若一个定义的列的名字与 model field 相同, model field will be overrided.
  ModelForm will only generate fields that are missing from the form, or in
  other words, fields that weren’t defined declaratively.

model form clean & validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- ModelForm 在普通的 Form clean & validation 逻辑之后, 实现了
  ``Form._post_clean()`` hook. 执行逻辑:

  * 使用 ``Form.cleaned_data`` 填充 ``ModelForm.instance``.
 
  * 调用 ``Model.full_clean()`` 进行 model instance clean & validation.

  * 调用 ``Model.validate_unique()``.

  以上每个步骤中 raise ValidationError, 不影响剩下的执行.

model form inheritance
^^^^^^^^^^^^^^^^^^^^^^

- 遵循与 Form inheritance 相同的规则.

- Meta class 是自动继承的 (作为 class attribute), 若要自定义可明确继承.

- 在 parent form 中 declaratively defined additional fields 可以设置
  None 来移除. 但 ModelForm 自动生成的列并不能这样移除. 仍需要设置
  Meta.exclude option.

ModelForm factory
^^^^^^^^^^^^^^^^^

- ``modelform_factory()``.

- 对于从 Model 至 ModelForm 自动映射生成的 Form class, 如果没有很多自定义
  需求, 可以使用 ``modelform_factory()`` function, 省得写 class definition.

- 还可用于基于现有的 ModelForm, 做一些小的修改, 生成新的 ModelForm.

parameters
""""""""""

form and model cleaning and validation in general
-------------------------------------------------
- model 的归 model, form 的归 form.
  
  即, 对于需要在 model-level 保证的数据条件限制 (而不论在哪里使用 model), 就在
  model 层保证; 对于某个 form-specific 的条件限制则在 form 层保证.

normal form cleaning and validation procedure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See `Form clean & validation`_ for detail.

- For each form field
 
  * 调用 field-level cleaning and validations.

  * 调用 field-specific cleaning and validation method defined on form class
    ``clean_<fieldname>()``.

- For form level, call ``clean()``.

- Call post clean hook. noop by default.

form field cleaning and validation procedure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
See `form field clean & validation`_ for detail.

- ``to_python()``

- ``validate()``

- ``run_validators()``

model form cleaning and validation procedure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See `model form clean & validation`_ for detail.

- 前两步同上.

- post clean hook 中进行 model-level clean and validation.

model instance cleaning and validation procedure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See `model instance clean & validation`_.

- For each model field, 调用 field-level cleaning and validation.

- For model-level, call ``clean()``.

model field cleaning and validation procedure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``to_python()``

- field-level validation ``validate()``

- run all validators.

Validation errors and messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- 在 clean & validation methods 中, 若验证失败, 应 raise ValidationError with
  appropriate arguments. 这包含 form-level, form field-level, model-level,
  model field-level 各种 clean & validation 相关方法.

ValidationError
"""""""""""""""
- constructor options.

  * message.
    
    A message Can be
    
    - a single error
     
    - a list of errors. 这可用于当一个 validation 操作发现多个错误.
     
    - a dict mapping from field names to a list of errors.

    An error can be:

    - A string.

    - A ValidationError instance with ``message`` attribute.

    A list or dict can be:

    - an actual list or dict

    - A ValidationError with ``error_list`` or ``error_dict`` attribute.

  * code. error code.

  * params. a dict of string interpolation parameters corresponding to
    ``message``.

error messages
""""""""""""""
* Error messages defined at the form field level or at the form Meta level
  always take precedence over the error messages defined at the model field
  level.

* Error messages defined on model fields are only used when the
  ValidationError is raised during the model clean & validation step and no
  corresponding error messages are defined at the form level.

* You can override the error messages from NON_FIELD_ERRORS raised by model
  clean & validation by adding the NON_FIELD_ERRORS key to the error_messages
  dictionary of the ModelForm’s inner Meta class.

model formsets
--------------

form field
----------
- model field maps to 数据库列; form field maps to HTML input 元素.

* A form’s fields are themselves classes; they manage form data, perform
  validation and clean form data when a form is submitted.

* A form field is represented to a user in the browser as an HTML “widget” -
  a piece of user interface machinery. Each field type has an appropriate
  default ``Widget`` class.

field options
^^^^^^^^^^^^^

* ``label`` 定义 ``<label>`` tag 内容.

* ``max_length`` 定义 ``<input>`` 最大长度, 并具有验证功能.

* ``help_text`` 在 render 时放在 field 旁边.

* ``error_messages`` overrides default field validation errors.

methods
^^^^^^^

clean & validation
""""""""""""""""""

- ``clean(value)``. handle `form field clean & validation`_, return cleaned
  value.

- ``to_python(value)``. 将 form field data 转换成该列预期的数据类型.

- ``validate(value)``. field-specific validation that is not suitable for a
  validator. 也就是不仅仅是对 value 的验证, 而可能需要考虑 field-level
  的一些特性. This method does not return anything and shouldn’t alter the
  value.

- ``run_validators(value)``. Run ``Field.validators``, aggregates all the
  errors into a single ValidationError.

field types
^^^^^^^^^^^

FilePathField
""""""""""""""

CharField
""""""""""
- constructor parameters.

  * ``empty_value``. default is ``""``. 意味着默认情况下所有的
    ``Field.empty_values`` 在 ``to_python()`` 时都会转换成空字符串.

  * ``strip``. 默认 leading and trailing whitespace chars are stripped.
    对于比如密码等输入, 则不该 strip.

- 关于区分 empty string & NULL. Django 强制认为 empty string & None 是
  一样的. 因此, 对于 CharField 而言, form data 是 "" 或 None 都会
  转换成 ``CharField.empty_value``, 无论这个值是什么.

  若要一个 CharField, 只有 NULL 时才认为是空值, 而对 "" 有别的含义. 可以
  定义类似 `snippets/nullcharfield.py`.

FileField
""""""""""
bound 之后的值 ``.value()`` 是 ``UploadedFile`` instance.

URLField
""""""""
html input type is ``url``.

EmailField
""""""""""
html input type is ``email``.

integer fields
""""""""""""""
* All integer fields. html input type is ``number``.

ModelChoiceField
""""""""""""""""
- a subclass of ChoiceField.

- 用于选择一个 model object, 例如作为 foreign key relation.

- 当需要在前端进行复杂筛选时, ModelChoiceField 根本不适合直接 render 至
  html 形式. 因为复杂筛选一般需要 js 插件实现, ajax 加载所需数据. 这时,
  这个列的作用主要是后端抽象, 进行验证等.

- constructor options.

  * ``queryset``. 待选的 QuerySet, also used for validate user selection.
    This is required. 

  * ``empty_label``. empty option's text. empty option can be disabled by
    setting this to ``None``. default is ``---------``.

  * ``to_field_name``. Select widget 的 option list 使用 model 的哪个列值
    作为 option value. The field must ensure uniqueness in the queryset.
    default is None, causing the primary key is used.

- methods.

  * ``label_from_instance(obj)``. 给出对应于 model instance 的 option text.
    默认给出 string representation.

- cleaning & validation:

  * ``to_python()`` 将 form data 匹配 ``to_field_name`` 列, 从 queryset
    中解析成一个 model instance.

- error message codes:

  * ``required``. (inherited from Field.)

  * ``invalid_choice``.

- 如果 queryset 需要根据一些外部参数动态生成, 可在 form 实例化时设置
  ModelChoiceField 的 queryset 参数::

    # in form class 
    def __init__(self, *args, **kwargs):
        self.fields['<name>'].queryset = ...

ModelMultipleChoiceField
""""""""""""""""""""""""
参数是待选的 QuerySet.

form field clean & validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

form field clean & validation 由 ``Field.clean(value)`` method 实现. 步骤为:

- 调用 ``to_python(value)``.

- 调用 ``validate(value)``.

- 调用 ``run_validators(value)``.

以上任一 raise ValidationError 则立即停止.

validators
""""""""""
Validators are run after the field’s to_python and validate methods have been
called.

widget
------

BoundField
----------

attributes
^^^^^^^^^^
- ``id_for_label``. html id of the field.
  
- ``label``. html label of the field.
  
- ``html_name``. ``<input>`` element's ``name`` attribute, 包含
  ``Form.prefix``.
  
- ``help_text``. field's help text.
  
- ``is_hidden``. whether the field is hidden.
  
- ``errors``. 的 string 形式是一个 ``<ul class="errorlist">`` element,
  但在 loop over 它的时候, 每个 error 只生成纯字符串.

- ``field``. The original ``django.forms.Field`` instance of this
  BoundField.

methods
^^^^^^^

- ``__str__()`` 给出它的 input HTML element.

- ``label_tag()``. field's label wrapped in ``<label>`` tag, including
  ``Form.label_suffix``.
  
- ``value()``. 根据该 bound field 所属的 form 是否 ``is_bound``, 给出该列
  的初始值 (``Form.initial`` 或者 ``Field.initial``) 或数据值. 注意这个
  值只是赋予这个 form field 的值, 它可能是合法的也可能不是. form clean
  & validation 并不修改这个值.

Export
======

CSV
---

由于 HttpResponse 是 writable file-like object, 可以直接转递给 ``csv.writer``
``csv.DictWriter`` 作为 write target.
若要传输很大的 csv 文件, 需要使用 StreamingHttpResponse. 这需要一些技巧.
详见 django 文档.

model
=====

* model 是一个数据对象类型, 它是数据库表的抽象. 或者从另一个角度来看, 由于 model
  的存在, 要求数据库表应该按照 object-oriented 的方式进行设计. 而一个 entry 就是
  一个 instance. 这是一种比较好的设计思路.

* model 定义时 field 以 class attribute 方式去定义, 而实例化后, 每个实例会
  生成同名的 attribute 在自己的 ``__dict__`` 中, 覆盖 class attribute.

* 当 model class 创建时, 定义在 class namespace 中的各个 ``Field`` 实际上
  存储在 ``Model._meta.fields`` 中.

* 对于 class namespace 中的各个属性, 只有 ``django.db.models.Field`` 的实例
  才会认为是 model field. 其他属性实际上可以随意设置.

* 表之间的关系抽象为在一个模型中包含另一个模型的实例作为属性. 这种抽象在逻辑上十分自然.
  并且在实例中进行 attribute lookup 以及在 QuerySet 中进行 field lookup 筛选时, 自然地
  支持了多级深入的操作.

* 通过 ``Meta`` inner class 定义来定义 model 的 metadata.

  - ``ordering`` 决定 QuerySet 的默认排序. 语法与 ``QuerySet.order_by`` 相同.
    若不设置, 且 queryset 没有 ``order_by``, 则生成的 SQL 没有 ORDER BY clause,
    即没有固定顺序.

* Model object managers (like ``.objects``) are only accessible via model classes,
  not the model instances.

* 定义 ``__str__`` method 给模型的实例一个有意义的 string 形式.

* 注意 ``Meta.verbose_name`` 和 ``__str__`` 的区别. 前者是模型本身的 verbose name,
  后者是 model instance 的字符串表现形式.
  在 admin site 中, 分类管理的 section 名字用 verbose name, 每个部分中, 对实例
  进行批量编辑的列表中, 显示实例用的 string 形式.

* 如果一个 app 中的 model 太多, 可以进一步模块化. 将 models 扩展成一个 subpackage.
  注意在 models package 的 init 文件中引入所有子模块中定义的 model.

* ``django.core.exceptions.ObjectDoesNotExist`` 是所有 ``Model.DoesNotExist``
  exception 的父类.

model class
-----------
class methods
^^^^^^^^^^^^^
- ``check(**kwargs)``. Entry point for all model related system checks. This
  method is called by ``django.core.checks.model_checks.check_all_models``
  which is a registered system check.

  The checks performed here:

  * Every field instance's ``check()`` method.

  * Every model manager's ``check()`` method.

  * ...

  If model subclas wanna extend checks, it's recommended that you delegate each
  check to separate non-public methods.

inheritance
-----------

三种 model 继承方式.

- abstract base model

  * ABC model 用于将多个 model 中的相同部分抽象出来, 避免重复. 它并不创建
    实际的数据库表. 仅用于从 python class 的视角上去做逻辑一般化. 每个
    继承了它的 concrete model 仍然包含并在数据库表中实例化所有列.

  * 使用 ``Meta.abstract = True`` 定义 ABC model.

  * subclass model 自动继承父类的 Meta class. 若要扩展, 则继承 Meta class 即可.
    ABC model 的子类的自己的 ``Meta`` attribue 自动设置 ``abstract = False``.
    若子类 model 仍需是 ABC, 需要再设置.

  * 对于 ABC model 的继承, 可以覆盖列名. 因为 ABC model 并没有实际的表去关联.
    还可以通过设置列名为任意非 ``Field`` 属性, 来删除一个数据库列, 用一个属性
    去替换.

  * 若 ABC model 中包含 FK 等关系列, 则 related_name/related_query_name  应该
    使用默认的值或者设置对于不同的 subclass model 自动取不同的值, 例如包含
    ``%(class)s`` ``%(app_label)s``, 否则会造成反向关系冲突.

  * multiple inheritance. 一个 model 可以继承多个 abstract model. 这常用于
    将一些公共的列提取出来构成 abstract mixin model class. 然后在不同的 model
    继承使用. 此外, 注意根据 MRO, 只有第一个 parent Meta 有效.

- concrete model inheritance

  * subclass model 继承 concrete model 时, 在数据库层, 子类的表只建立多出来的
    那些列, 属于父类的信息则保存在父类的表中. 两者通过隐性建立的 OneToOneField
    关联:

    .. code:: python

      <parent>_ptr = models.OneToOneField(
        <parent-model>,
        on_delete=models.CASCADE,
        parent_link=True,
      )

    注意 ``parent_link`` 让父类的 fields 在子类实例中可以直接获取. 这才符合
    继承概念. 此外, 注意这个 OTO field 默认命名为 ``<parent-model>_ptr``.
    也可以在子类 model 中明确定义这个 OTO field, 例如修改名字之类的.

    在子类实例中, 可以访问 OTO 获取父类实例. 注意父类实例由于具有 OTO field
    的反向关系, 也还可以再获取子类实例本身. 甚至由于子类实例本身就是父类实例,
    子类实例中也访问父类中的反向关系, 再得到自己的另一个 instance.

  * 仔细想想, 非 ABC model 在继承时, 子类 model 表中只保存那些扩展的信息, 继承的
    信息都保留在父类表中. 这个设计实际上才是合理的. 因为子类的实例也是父类的实例,
    我们可以从子类实例中抽出纯父类实例那部分 (例如通过 ``super``). 我们把这种继承
    和实例化的思路应用在 ORM 上, 就得到了父类 model 的数据集显然是应该包含子类
    model 的数据集的 (抽出公有部分). 所以子类表只存扩展字段即可, 通过 one-to-one
    field 与存在父类表中的基础数据对应, 两部分数据构成一个完整的子类实例.

  * 若 model 继承时不是继承的 ABC model, 而是实体 model, 则子类的 field 不能
    和父类的 field 重名, 即 field attribute can not be overrided. 这与一般的
    python 类不同. 这是因为 model instance 实际上是数据库表 entry 的抽象,
    如果重名, 在获取属性即列值时就存在歧义和令人困惑之处.

  * 在继承实体 model 时, 不继承 Meta, 因为这是不合理. 因为这时 parent Meta
    的值仅应对父类生效, 例如 verbose_name. 子类也使用显然不合理. 但有一个
    例外, 即 ordering 会从父类继承.

  * 继承实体模型时, 若父模型中有 FK 等关系列, 子模型直接使用保存在父模型表
    中的关系. 这体现在, 从子模型实例中可以得到父模型指向的 related model
    instances, 但在 related model instance 中, 只有向父模型的反向关系. 无法
    区分 related manager 得到的实例哪些是父, 哪些是子 (除非在父模型中保存
    有对不同子模型区分的列值).

  * 在数据库层, subclass table 的 PK 直接使用了 OTO 关系列的值, 即 parent
    table 的 PK id, 因此, 这保证了在 django 中, subclass model 实例的 id
    与它对应的 parent model 实例部分的 id 实际是一个项, 且 pk 值即外键值
    也能正确地与 parent model id 一致. 所以不存在区分子模型实例 id 与父
    模型实例部分 id 的问题.

  * multiple inheritance. 继承多个 concrete model 可能造成一些麻烦.
    首先, 数据会分散在各个继承的模型表中. 其次, 不同的模型列可能冲突.
    尤其是, 默认的 id field 会冲突, 因此 parent models 需要使用 AutoField
    指定明确的 id field 或者指定完全自定义的 primary key field. 若继承
    的几个 parent models 具有相同的 parent concrete model, 则这些 model
    中的指向 parent model 的 OneToOneField 必须显性定义, 因为默认的列名
    是 ``<parent>_ptr``. 所以再次继承时会发生冲突.

- proxy model

  * proxy model 不修改 model, 而是修改对 model 数据的操作, 即 only change
    the python behavior of a model.  因此 proxy model 和它的原始 model
    共享所有数据集. The whole point of proxy objects is that code relying
    on the original Person will use those and your own code can use the
    extensions you included (that no other code is relying on anyway).

  * proxy model 可以用来添加 method, 修改 Meta options 例如 ordering.

  * QuerySets still return the original model.

unmanaged model
---------------

- If you are mirroring an existing model or database table and don’t want all
  the original database table columns, use ``Meta.managed=False``. That option
  is normally useful for modeling database views and tables not under the
  control of Django.

model meta options
------------------

* ``apps``. specify the app registry to use. default use ``django.apps.apps``.

* ``abstract``, whether is abstract model.

* ``app_label``, 定义 model 所属的 app.

  对于在其他 app 中已经定义的 model, 可在 import
  过程中修改 ``model._meta.app_label`` 的值修改它所属 app.

  注意无论是在 Meta 中修改还是其他修改方式, 这直接改变了 django 看待这个 model
  所属于的 app. 因此这导致相应的 migration 必须被创建和应用. 因此, 不能通过
  这个方式修改 django contrib app 的 models. 因为这会修改这些应用的 migrations.

* ``db_table``

* ``db_tablespace``. 该 table 所在的 tablespace. 默认为 settings.DEFAULT_TABLESPACE.

* ``default_related_name``, 对于 relation field, ``related_name`` 的默认值.
  默认是 ``<model>_set``.

* ``get_latest_by``. ``QuerySet.latest()`` ``QuerySet.earliest()`` 默认
  使用的 fields: The name of a field or a list of field names.

* ``managed``, This is useful if the model represents an existing table or a
  database view that has been created by some other means.

* ``order_with_respect_to``, This can be used to make related objects
  orderable with respect to a parent object. ``order_with_respect_to`` and
  ``ordering`` cannot be used together, and the ordering added by
  order_with_respect_to will apply whenever you obtain a list of objects of
  this model.

* ``ordering``. default ordering when obtaining a list of objects.
  和 ``QuerySet.order_by()`` 语法相同.

* ``permissions``, extra permissions relating to this model (content type).

* ``default_permissions``, 对该 model 默认创建的一系列权限. 默认 add/change/delete.

* ``proxy``, proxy model.

* ``indexes``, A list of indexes that you want to define on the model.

* ``unique_together``, 一组或多组 associative unique constraint. 使用
  a tuple of tuples 来定义.

* ``verbose_name``, ``verbose_name_plural``, human-readable name for the model.

* ``label``, ``label_lower``, readonly. ``<app_label>.<model_name>``.

* ``default_manager_name``. 指定 ``Model._default_manager`` 使用哪个名字的
  manager. default is None.

* ``base_manager_name``. 指定 ``Model._base_manager`` 的名字. default is None.

model field
-----------

- ``django.db.models.Field``. field base class. Field 是
  ``RegisterLookupMixin`` 的子类.

design
^^^^^^
- model instance 的属性只是 field value, 而不是 Field instance. Field instance
  是一个模型, 它表达列应具有的行为, 并在需要的时候进行相关列的操作. 但它本身
  并不保存状态. 也就是说, model field instance is basically immutable, 它不包含
  数据状态, 只包含定义和声明.

- Field 无状态的一个意义是让它可以 deconstruct & serialize into migration.

constructor
^^^^^^^^^^^

- Many of Django’s model fields accept options that they don’t do anything
  with.  This behavior simplifies the field classes, because they don’t need to
  check for options that aren’t necessary. They just pass all the options to
  the parent class and then don’t use them later on.

- 这些 options 作为 constructor kwargs, 实例化后成为 field instance attributes.

- 对于任何需要使用 callable 作为 field option value 时, 必须保证 callable 满足
  migration framework 的 serialization 要求.

  * 若需要根据参数动态生成 callable, 不能使用 wrapper function return another
    function 的方式. 这样不可 serialize. 必须创建一个 deconstructible callable
    class.

    .. code:: python

      @deconstructible
      class Factory:

        def __call__(self, ...):
          return ...

- ``primary_key=True``.
  设置某个 field 为 primary key, 否则 django 自动给 model 添加 id field
  作为 primary key.

  .. code:: python

    id = models.AutoField(primary_key=True)

  The primary key field is read-only. If you change the value of the primary key
  on an existing object and then save it, a new object will be created alongside
  the old one.

  primary key field 自动设置 null=False 和 unique=True, 若明确设置了 null=True 
  检查时会报错.

- ``unique``.
  unique constraint 显然自动生成 index, 所以不用设置 ``db_index``.
  OneToOneField 一定是 unqiue 的, 设不设都行.
  ManyToManyField 由于本身不是一个列, 不支持 unique option.

  unique constraint is checked during model instance clean & validation, and
  enforced in db.

- ``unique_for_date``, ``unqiue_for_month``, ``unique_for_year``.
  this field is unqiue with respect to the specified period of time.
  该选项的值为所参考的时间列.

  在 model instance clean & validation 时检查. 

- ``default``.
  a value or callable. lambda 不能做 default, 因为不能 serialized in migration.
  对于 relational fields, default 设置为 remote_field 值, 而不是 model instance.

  仅在 SQL 中创建 entry 时该列的值未指定时生效, 而不是
  ``field=None`` 时. 后者情况是指定了该列, 但值是 null. 在未指定时, default value
  根据 ``Field.get_default`` 逻辑给出: 若 nullable, 给出 None, 否则给出 "".

  对于 model field 设置的默认值, django 并不应用到数据库表定义中. 而是维持在
  django 层. 这是为了保证 default value 的灵活性 (e.g., callable 而不是固定值).
  所以在写数据时, 对于默认值列还是会与其他列数据一同发给数据库.

  .. TODO read with form

- ``blank`` 若为 True, form 中允许该项为空.

  .. TODO read with form

- ``null`` 默认是 False, 此时 create table 时有 ``NOT NULL``, 且不允许
  field 值为 None; 若 True, create table 时有 ``NULL``, 且允许 field 值
  为 None.

  ``blank`` 是规定 form validation 时是否允许空值. 两者的意义是不同的.
  ``null`` 和 ``blank`` 的默认值都是 ``False``.

  .. TODO read with form

- ``choices``.
  设置 field 的可选值, 其值是 a iterable of ``(value, description)``
  pairs 或者设置 optgroups ``(label, ((value, description), ...), ...)``.
  choices 只需是 iterable 即可, 从而允许动态生成.
  
  选项值的 symbolic enum 以及 choices list 本身, 应设置在 model class 中.
  这是为了方便后续在查询等操作中使用.
  
  注意如果只在 model class 中设置 enum, choices 等常量的话, 这些常量是不能在
  migration 中使用的. 因为 migration 重建的 model class 不包含这些 class
  attributes. 所以为了可用性, 需要在 module-level 设置相应的常量.
  
  设置该选项后, 默认的 form field 使用 TypedChoiceField, form widget 是
  (multiple) select box.
  
  Given a model instance, the display value for a choices field can be accessed
  using the ``get_FOO_display()`` method.

  .. TODO read with form

- ``editable``.
  若 False, 不在 model form 中出现, 并且 skipped during model validation.

  .. TODO read with form

- ``help_text``.
  设置该列值的详细的帮助信息, 以协助用户输入. ModelForm 会使用它. 其字符串值在
  模板中直接显示, 不会被 escape. 可以直接嵌入 html 语法.

- ``error_messages``.
  A dict that overrides ``default_error_messages`` class attribute.
  Valid keys are defined in ``default_error_messages`` of each field types
  and their parent classes.

- ``verbose_name``.
  对于非关系型 field, 该参数是第一个 kwarg, 因此经常以
  positional 形式写出; 对于关系型 field 必须以 kwarg 形式写出.
  默认根据 field name 生成.

- ``db_column``. 指定 db column name. 默认为 field name.

- ``db_index``, 是否创建 single field index.

- ``db_tablespace``, 若建立索引, 索引所在的 tablespace. 默认为
  ``settings.DEFAULT_INDEX_TABLESPACE`` 或 ``Meta.db_tablespace``.
  这个有效性取决于 db backend.

  * 对于 mysql, innodb 默认使用 file-per-table tablespace. 这参数就没啥意义.

- ``validators``. 指定 validators. 这些 validators 会在 form validation 或
  model instance validation 的时候生效.

- ``max_length``. 对于一些 field types, 可以设置最大长度. 这包含: CharField,
  TextField, SlugField, BinaryField,

attributes
^^^^^^^^^^

- ``description``. description of the field. 这与 help_text 的区别是,
  这个使用来描述列的 implementation 的, 即适合于用在代码文档中. 而
  help text 是描述列该填什么内容的, 即适合于界面输入提示.

  description 的值可以包含 ``__dict__`` interpolation placeholder. 但
  注意它本身不去 interpolate.

- ``empty_strings_allowed``.
  Designates whether empty strings fundamentally are allowed at the
  database level for this field. 影响 (但不决定) 该列的默认值.

- ``default_error_messages``.
  该列的设置的默认 error message template. 只需设置 override parent class
  的部分即可. 所有 ``default_error_messages`` 和 ``error_messages`` option
  构成该列的 error messages.

field property introspection.

- ``name``. field name as specified in model class definition.

- ``attname``. 在 model instance 上, 列的值使用的属性名字. 注意对于 FK 类型的列,
  attname 为 ``<name>_id``, 而 ``name`` 用于封装 get/set related model instance
  logic.

- ``column``. 该列在数据库中的列名字. 由 attname 或者 db_column option 决定.
  对于 m2m field, 列不在 model table 中, 列名不由这个决定.

- ``auto_created``.
  该 field 是否自动创建. 自动创建的 field 例如 AutoField, 用于继承的 parent
  link OneToOneField.

- ``concrete``.
  Whether the field has a database column associated with it. 注意对于 m2m
  field 这个 concrete column 在 through table 中, 这仍然是有数据库列的, 所以
  是 concrete 的.
  non-concrete fields 例如 GenericForeignKey, 反向的关系列 ForeignObjectRel.

- ``hidden``.
  Whether a field is used to back another non-hidden field’s functionality.
  这用于区分 public fields and private fields.

- ``is_relation``.
  Whether the field is a relation, i.e. a reference to other model instances.
  对于 Field subclass, 有 remote_field 就认为是关系列.

- ``model``.
  the model on which the field is defined.

property introspection for relational fields. 以下属性在所有 field 中都有.
但是只有当 ``is_relation == True`` 时, 它们才不是 None. 自定义的 relation
fields 需要设置这些属性.

- ``many_to_many``.
  many-to-many relation flag. e.g., ManyToManyField.

- ``many_to_one``.
  many-to-one relation flag. e.g., ForeignKey.

- ``one_to_many``.
  one-to-many relation flag. e.g., GenericRelation.

- ``one_to_one``.
  one-to-one relation flag. e.g., OneToOneField.

- ``related_model``.
  the model the field relates to.

- ``remote_field``.
  该列在 ``related_model`` 上的对应列 (实际存在或虚拟的列).

以下参数用于处理 custom field 的 deprecation and removal process. 当一个 field
已经完全不再支持时, 唯一的价值在于支持 historical migrations.

- ``system_check_deprecated_details``. a dict of ``msg``, ``hint``, ``id``.

- ``system_check_removed_details``. ditto.

methods
^^^^^^^

db data type related APIs
""""""""""""""""""""""""""

- ``get_internal_type()``.
  给出这个 Field class 对应的 django builtin field type name.

  对于每种 db connection backend, 定义了一组从 internal type name 至
  db-specific 的参数或类型映射. 它们的 key 即 internal type names.

  定义这个方法, 意思是告知 Field API 这个列在数据库层与哪个 builtin field
  是相同的.

  对于 builtin fields, 直接返回自身名字. 因为它们就是定义在映射中的 key.

- ``db_type(connection)``.
  给出数据库中实际使用的 field type.
  
  对于 builtin fields, 根据 ``BaseDatabaseWrapper.datatypes`` 和 field options
  生成 field type.

  若这个方法返回 None, 则生成的 SQL 会直接跳过这个 Field.

- ``rel_db_type(connection)``.
  当这个 Field 成为 ForeignKey, OneToOneField 等 many-to-one field 所指向
  的列时, 给出相应的 many-to-one field 所应使用的 ``db_type()``.

db field value related APIs
""""""""""""""""""""""""""""

- ``get_prep_value(value)``.
  将 field value 转换成这个列的数据库形式, 但不应考虑与具体数据库相关的不同
  情况. 这是 ``get_db_prep_value()`` 的预处理部分.

  * value: 在 model instance 上的列值的 python 形式.

- ``get_db_prep_value(value, connection, prepared=False)``
  将 field value 转换成 db-specific 的列值. 默认该方法给出 ``get_prep_value()``
  的值. 即默认没有 db-specific 转换, 直接使用通用值. 但一些 model field 通过
  ``<backend>.operations`` 进行了进一步转换.

  * value: 在 model instance 上的列值的 python 形式或者已经处理过的列值.

  * connection: database connection.

  * 是否已经预处理过了, 默认逻辑是如果 prepared, 直接返回 value.

- ``get_db_prep_save(value, connection)``.
  将 field value 转换成 db-specific 的列值, 但是只有在需要对该列数据进行写入
  时使用 (例如 INSERT, UPDATE). 除此之外, 与 ``get_db_prep_value()`` 相同.

  * value: 在 model instance 上的列值的 python 形式. (已经经过 ``pre_save()``
    操作).

  * connection: database connection.

- ``from_db_value(value, expression, connection)``.
  将从 database backend 传回来的 value 进一步转换成所需 python 形式. builtin
  fields 没有实现这个方法. 因 backend 传回的已经是所需形式. 在应用时,
  ``from_db_value()`` 是作为 ``sql.SQLCompiler.get_converters()`` 的一部分.

  * value: 已经经过多次转换的列值.

  * expression: ``Col`` expression of this field.

  * connection: database connection.

- ``pre_save(model_instance, add)``. 在 INSERT, UPDATE 等写操作之前进行的一些
  操作. 主要用于更新 model instance 上的列值等. 最终确定下 model instance 上的
  各个列值. 这个方法发生在 ``get_db_prep_save()`` 之前.

Deserialization
""""""""""""""""

- ``to_python(value)``.
  called by deserialization and during the clean() method used from forms.
  Return valid field value as python object.

  The method should deal gracefully with any of the following arguments:

  * An instance of the correct type.

  * A string.

  * None.

Serialization
""""""""""""""

- ``value_to_string(obj)``.
  convert field value, which is attribute of ``obj``, to string form.
  使用 ``value_from_object(obj)`` 获取列的值, 然后再 serialize.

form field
""""""""""

- ``formfield(form_class=None, choices_form_class=None, **kwargs)``.
  Returns the default django.forms.Field of this field for ModelForm.
  ``kwargs`` are passed to form class constructor.

field checkings
""""""""""""""""

- ``check(**kwargs)``. 检查列定义是否合法.
  检查项.

  * field ``name`` does not end with underscore, does not contain field
    lookup separator ``__``, and is not ``pk``.

  * 检查 choices 格式和内容合法.

  * 检查 db_index 参数值合法.

  * 检查 primary_key field 没有设置 null=True.

  * 检查 validators 都是 callable.

  * backend-specific field checks.

  * 检查 field class 是否 pending deprecation 或者已经 removed. 若此, 输出相应
    的警告或错误信息.

  子类若需扩展 system checks, 应将每个测试点放在一个单独的 non-public method 中.

model clean & validation
""""""""""""""""""""""""

- ``clean(value, model_instance)``.
  1. 调用 to_python() 转换 value 为合法列值(或报错).

  2. 调用 validate() 做基本校验.

  3. 调用 validators.

- ``validate(value, model_instance)``

  * 若不可编辑, 不校验.
    
  * 若有选项, 校验值是否属于选项.
    
  * 校验是否允许 NULL.

  * 校验是否允许空值.

default value
""""""""""""""
- ``has_default()``. 是否有明确设置的默认值.

- ``get_default()``. 给出该列合适的默认值. 这个方法总能编出一个
  值来. 即使 ``has_default() is False``.

  * 如果 Field 有明确设置的默认值, 使用该值

  * 否则, 如果 nullable, 返回 None.

  * 否则, 返回 "" empty string.

  注意到, 如果一个列没有设置明确默认值, 且 NOT NULL, 会给出 "" 默认值.

deconstruction
""""""""""""""
 
- ``deconstruct()``.
  Returns a 4-tuple with enough information to recreate the field.

  * The name of the field on the model.

  * The import path of the field.

  * A list of positional arguments.

  * A dict of keyword arguments.

  这在 migration 中使用.

field types
^^^^^^^^^^^
所有 field types 都是 ``Field`` 子类.

- AutoField.
  当 model 没有指定 primary key field 时, 自动添加的 id field. 一般不手动指定.
  自动设置 blank=True.  model form 不会生成相应 field.

  checkings.

  * must have ``primary_key=True``.

- BigAutoField.  64-bit AutoField subclass.

- IP address 用 ``GenericIPAddressField``.
  支持 IPv4, v6. 以 string form 存储.

  max_length 固定在 39.

  options.

  * protocol. ``ipv4``, ``ipv6``, or ``both``.

  * unpack_ipv4. unpack ipv4-embedded ipv6 into corresponding ipv4 address.

  validations.

  * 校验值是合法的 ip address of the specified protocol.

- 实数一般用 ``FloatField``.
  
- 若 float 不能满足需要, 需要 mathematically correct 时考虑 ``DecimalField``.

  ``max_digits`` and ``decimal_places`` are required.

  checkings.

  * 检查 ``max_digits`` 和 ``decimal_places`` 是否定义, 是否合法.
    max_digits 须大于 decimal_places.

  validations.

  * 检查值是否满足 decimal 定义要求.

- ``IntegerField``, ``PositiveIntegerField``, ``BigIntegerField``,
  ``SmallIntegerField``, ``PositiveSmallIntegerField``.
  各种整数.

  checkings.

  * 不能设置 ``max_length`` option.

  validations.
  
  * 数值是否在 backend 允许的范围内.

- ``DateField``, ``TimeField``, ``DateTimeField``.

  * 在 python 中以 datetime.date, datetime.datetime 分别表示.

  * ``auto_now_add`` 适合做 create time; ``auto_now`` 适合做 modified time.
    这些参数在调用 ``Model.save()`` 来保存时才有效, 通过其他途径修改数据
    时不会生效. (**不要使用这两个参数**)

    若只是想设置默认值, 那就用 ``default=``, 别用这两个选项.

    ``auto_now``, ``auto_now_add`` 和 ``default`` 是互斥的.

    设置这两个参数, 意味着该列不能手动修改. 即使手动设置了特别的值, 在
    ``Model.save()`` 时也会修改为当前时间. 并会自动设置 ``editable=False`` 和
    ``blank=True``.

    **在单元测试时, ``auto_now`` 和 ``auto_now_add`` 会阻碍手动构建任意时间. 此
    时, 一个解决方案是在创建 model instance 之后再单独更新一次时间. 使用 UPDATE
    类的语句, 避开 ``Model.save``. 而对于 factory boy, 完全他妈没有解决办法, 因
    为 ``_after_postgeneration`` 会再保存一次我日. 我以后再也不他妈用这两个傻逼
    参数了. 我操你妈 django.**

  * 所在的 model class 会添加 ``get_previous_by_<name>`` 和 ``get_next_by_<name>``
    两个 method.

  * mysql note: 只有 5.6.4+ 版本支持毫秒精度的时间, 使用 DATETIME(6).
    对于 legacy 数据库, 需要手动更新 column data type.

  checkings.

  * 检查 ``auto_now``, ``auto_now_add``, ``default`` 是否设置了多个.

  * 检查 user 是否错将 ``datetime.date``, ``timezone.now`` 等 动态
    默认时间值写成了固定时间 ``datetime.date()``, ``timezone.now()`` 之类的.
    这不涉及一般的静态默认时间值. 仅仅是检查是否写错了.

- ``DurationField``. 保存时间区间数据. 赋值 ``datetime.timedelta``

  除了 postgresql 和 oracle 之外, 该数据以 microseconds 单位保存 (``10**6 μs = 1s``).

- ``BooleanField``, ``NullBooleanField``. 后者允许存 NULL.

  BooleanField 总是 null=False. 在未设 default 值时, form validate 不接受 None.
  若直接保存而不经 form 校验, None 会被数据库拒绝.

  checkings.

  * 不能设置 null=True.

  NullBooleanField 总是 null=True, blank=True. 会区别对待不同值.

- ``CharField``.
  若设置 null=True, 则 char field 存在两种空值, ``""`` 和 ``NULL``. 根据具体
  场景考虑这是否合适.

  checkings.

  * max_length must be defined.

  validations.

  * value length match max_length constraint.

  mysql note: VARCHAR column 若设置 unique constraint, 要求 max_length <= 255.

  django 没有提供 CharField 对应的 binary 形式. 即没有 VARBINARY type 的 django model.
  只有 TextField (LONGTEXT) 对应的 BinaryField (LONGBLOB).

- ``TextField``.

  max_length attribute will be reflected in the Textarea widget of the
  auto-generated form field. However it is not enforced at the model or
  database level. 

  MySQL 作为后端时, TextField 不能在 model 中直接定义索引. 因为 mysql 要求
  TEXT/BLOB 上的索引必须指定长度. 而 django 不提供指定索引长度. 解决办法是
  使用 RunSQL 创建索引和执行相关 state operation.

- ``EmailField``

  validations.

  * string is valid email.

- ``SlugField`` 只应该在创建 instance 时保存该列值.

  配合 ``slugify()`` 函数使用. 

  max_length by default is 50.

  默认会给 SlugField 创建 index.

  options.

  * allow_unicode. allow unicode chars in slug.

  validations.

  * 检查值是否是合法的 slug.

- ``FilePathField``.
  这个列相当于 CharField with choices option. 其中, choices 为根据 constructor
  参数搜索到的一组现有的文件和/或目录. 这个列不是用于保存任意路径的. 而是用于
  路径选择.

  注意该列本身不检查和限制保存的路径, 所有相关逻辑在对应的 forms.FilePathField
  中实现.

  checkings.

  * ``allow_files`` ``allow_foleders`` 不能都是 False.

- ``FileField``. see `model fields`_ in `File handling`_.

- ``ImageField``. see `model fields`_ in `File handling`_.

- ``JSONField``. postgresql 可以使用 native JSONField, 对于 mysql 5.7+ 可以使用
  django-mysql module 提供的 JSONField.

- ``BinaryField``. 其值必须是 bytes instance. 限制它不能出现在 model form 中.

  注意 binary field 不是用来保存静态文件的, 静态文件还是要在文件系统中保存.
  这只是用于保存小量的只读只写的特殊用途的 binary data.

  default value. 若 ``super().get_default()`` 给出 "", 转换成 b"" empty bytes
  string.

  validations.

  * 若设置了 ``max_length``, 检查数据长度.

  数据库类型对应:

  * mysql: LONGBLOB. 2**32 - 1 bytes = 4GiB.

- ``URLField``.
  A CharField subclass for urls.

  validations.

  * 校验值是 valid url.

- ``UUIDField``.
  a field for ``uuid.UUID`` class instances.
  一般用法是设置 ``default=uuid.uuid4`` callable.

relation fields
""""""""""""""""

relational fields 的说明.

- recursive relationship. 若 relation field 需要与自身表建立关联, 使用
  ``"self"`` 作为 ``to`` 参数值.

- lazy relationship. 若 relation field 需与可能尚未建立的 model 建立关联,
  使用 ``"[<app_label>.]<model>"``.

concrete forward relations.

- ``RelatedField``. Base class of relational fields.

  attributes.

  * opts. containing model's Meta options.

  checkings.

  * 检查 ``related_name`` 是合法的 python identifier (或 ends with "+").

  * 检查 ``related_query_name`` 不包含 lookup separator ``__`` 且 not
    ends with ``_``.

  * 检查 ``to`` 设置的关联 model 是否存在. 例如不在 ``INSTALLED_APPS`` 中,
    或者不存在的字符串形式.

  * 检查 swapped model.
    .. TODO understand swappable.

  * 检查该列的 reverse accessor 和 reverse query name 是否在 related model
    中引起冲突.

- ``ForeignObject``. subclass of RelatedField, abstraction of ForeignKey
  to provide multi-column foreign relations. 使用 ForeignObject 可以实现从多个列
  至多个列的外键关系封装.

  attributes.

  * ``forward_related_accessor_class``. ForwardManyToOneDescriptor.
    在 model instance 上 FK 列属性实际上是这个 descriptor. 在 get 时,
    从数据库获取 related model instance 并返回; set 时, 直接赋值
    related model instance 或 None, 并更新关系列值.

  checkings.

  * 检查指定的 ``to_fields`` 都存在.

  * 检查 ``to_fields`` 中是否存在 unique constraint. 注意由于 ForeignObject
    仍然是 many-to-one relation, 因此要求能够 uniquely identify.

- ``ForeignKey``. many-to-one relation.

  foreign key field 的名字应该是所指向的 model 的名字的全小写版本.

  ForeignKey field 默认设置 ``db_index=True``, 即默认建立该列的索引.

  ``ForeignKey`` field 在数据库中命名为 ``<field>_id``, 除非用 ``db_column``
  自定义.

  若 ``ForeignKey`` field 设置 ``null=True``, 则对这个属性赋值 None 即可
  不设置关联.

  options.

  * ``on_delete``.
    required parameter. django 目前 constraints 完全是在 django 层实现的.
    没有使用数据库原生的 constraint.

    - 若该条数据必须随指向的数据共存亡, ``django.db.models.CASCADE``.

    - 若只要 FK 关系仍存在就禁止删除原数据, ``django.db.models.PROTECT``.

    - 若需设置为 NULL 以表示不指向任何东西, ``django.db.models.SET_NULL``.

    - 若需设置为默认指向的东西, ``django.db.models.SET_DEFAULT``.

    - 若需自定义设置逻辑, ``django.db.models.SET(value|callable)``.

    - 啥也不干, 由数据库决定该怎么办, ``django.db.models.DO_NOTHING``.

  * ``limit_choices_to``, 限制生成的 ModelForm 中该列的关联范围. Either a
    dictionary, a Q object, or a callable returning a dictionary or Q object
    can be used.

  * ``related_name``, 自定义从 related object 反向获取时, related manager
    的名字. 默认是 ``Meta.default_related_name``, 后者的默认值是
    ``<model>_set``. 若不让 django 创建反向关系, set related_name to '+' or
    end it with '+'.

  * ``related_query_name``, 在 field lookup syntax 中, 从 related model
    向这个 model 反向查询时, 使用的名字. 若有设置 related_name 或
    Meta.default_related_name, 默认使用它们中的一个, 否则默认为 model name.
    最好明确定义一个 singular name 作为 related query name 的值, 因为
    ``related_name`` 若明确设置了的话一般是复数形式. 这样在反向查询时比较
    别扭.

  * ``to_field``, 关联的 model 的 field, 默认是 primary key. 关联的 field
    必须有 unique constraint.

  * ``db_constraint``. 默认 True 即可. 是否在数据库层建立 FK 关系.

  * ``swappable``, 默认 True 即可. 与 swappable AUTH_USER_MODEL 相关, 为了
    支持 custom user model.
    .. TODO understand swappable.

- ``OneToOneField``: one-to-one relation.

  - 一对一关系一般用于一个模型作为另一个模型的延伸、扩展、附加属性等.
    ``OneToOneField`` 在 model 继承时用于定义父表和子表通过哪一列来关联.

  - OneToOneField 本质上是 ForeignKey 的一种特例. 前者是后者的子类.

  - one-to-one field 在 mysql 中实现时, 实际上是一个普通的 field (类型与指向
    的 model 的 primary key 一致), 配合 unique key constraint 以及 foreign key
    reference constraint.

  - OTO field 的 ``parent_link`` 结合 conrete model inheritance 时有特殊作用,
    它让父类的 field 可在子类即 OTO field 所在 model 中直接访问.

  - ``related_name``. 由于反向关系直接给出一个 model instance, by default
    ``related_name`` is lower-case name of the current model.

- ``ManyToManyField``: many-to-many relation.

  - 由于一个列无法体现多对多的关系, ``ManyToManyField`` 在实现时, 不是构成了一个列,
    而是一个单独的 table. table 的命名根据 ``<app>_<model>_<m2mfield>`` 全小写命名.
    table 中包含 many-to-many 关系的两种模型数据的行 id.

    该表中的两个 FK 列都有 index.

  - It doesn’t matter which model has the ``ManyToManyField``, but you should only
    put it in one of the models – not both. ``ManyToManyField`` 应该放在那个编辑
    起来更自然的 model 中, 也就是说, 从哪个方向建立多对多映射关系更自然, 就把它
    放在哪个 model 中.

  - many-to-many field 的名字应该是一个复数类型的名字, 以表示多个的概念.
    同样的, ``related_name`` ``related_query_name`` 也应该是表示反向关系的
    复数.

  - ``ManyToManyField`` 不是一个列, 而是抽象了一个包含映射关系的表, 只有设置
    映射和没有映射, ``null=`` 参数对它没有意义. 指定该参数会导致 django
    system check 警告.

  - ManyToManyField 不存在 on_delete 参数, 一方面是因为它本身不是一个列, 这个语义
    就不太对; 另一个也是因为它背后的两个 FK field 都必须是 CASCADE 的, 所以没必要
    指定.

  - constructor options.

    * related_name, related_query_name, limit_choices_to.

    * ``symmetrical``, M2M relationship pointing to self 时, 可能希望
      ``related_name`` 与 field name 相同, 此时, 希望 ``a.relations.add(b)`` 之
      后, ``b.relations`` 自动也包含 ``a``. 对称的 M2M 关系是通过在 through
      table 中自动添加反向的关联关系来实现的. 例如, 添加 a->b 时, 同时添加 b->a
      关系至 through table 中.

    * ``through``. through model. 多对多关系实际上是通过一个关系表来实现的. 这
      个关系表的 model 可通过 ``ManyToManyField.through`` attribute 获得. 并可
      以通过 ``through`` option 来指定单独创建的 through model, 这可用于在
      through model 中加入额外的状态信息等列.

      ``.through`` 属性在 field instance 是 through model class.

      through model 的定义遵从常规 model 的全部规则. 例如, 在 through model 中
      创建的用于 M2M 关联的 FK fields, 也会在反向创建 related manager
      attribute.

      别忘了一般情况下 through table 应保证两个 FK 列是 unique together 的.

      定义 through model 后, add, create, set, remove 这些 related manager
      methods 都不能用了. 这导致必须手动模拟这些方法的操作, 例如需要手动触发
      ``m2m_changed`` signal. 这可以通过设置 custom related manager 来实现.

reverse virtual relation fields.

model index
-----------

index 通过 ``Model.Meta.indexes`` option 指定, a list of Index objects.

``Index`` object.

* ``fields``, 指定单一索引或复合索引的列, 以及方向. 语法和 QuerySet.order_by
  相同.

* ``name``, index name.

* ``db_tablespace``. 指定该 index 所在的 tablespace. 对于 single field index,
  fallback 至 field's db_tablespace; 若未指定或是复合索引, fallback 至
  model ``Meta.db_tablespace``.

单列的索引在 ``Field.db_index`` 定义还是在 ``Model.Meta`` 中定义?

* 如果继承了 abstract parent model, 而存在给继承了的 field 添加索引的需求,
  则为了统一应该将索引创建在 ``Model.Meta`` 中.

* 如果存在复合索引, 则为了统一应该将索引创建在 ``Model.Meta`` 中.

* 其他随意.

model instance clean & validation
---------------------------------

* model instance 的 clean & validation 不会在直接创建或保存 model instance
  时自动执行. 这些逻辑依赖两方面进行保证:
  
  - 向下, 在 model-level 设置的数据库 constraints 会在数据库层进行保障 (当有
    相应的数据库结构时), 在 model 层不做校验, 依靠在写入时数据库报错来
    invalidate;
    
  - 向上, 在 model-level 设置的数据有效性 constraints 和数据合法性校验与数据
    类型转换会在 ModelForm 层校验时执行. 所以, 任何外源性的非可信数据, 最好
    先填入 ModelForm, 整体校验后保存. 只有内源性的数据在修改数据库时, 才可以
    直接读写 model instance.

* 在定义 model class 时, 要考虑应该在 model 层就限制的数据合法性要求.
  这包括:

  - 对于 model field, ``validators``.
    对于自定义 model fields, 还可以自定义 field 的 clean methods 等.

  - 对于 model 内各数据之间的制约关系, 自定义 model 的 clean methods 等.

* ``.save()`` 时不会自动调用 ``.full_clean()`` (因 form 验证时会执行它),
  若 model instance 不是来源于上层 form, 这验证操作必须手动执行. 或者
  等着数据库下层报错.

- ``Model.clean()``.

  注意由于即使 field-level validation 失败, ``Model.clean()``
  也会执行. 因此不能假设各列属性的值是合法的甚至是存在的. 需要
  进行判断. 这个方法中, 应该是先判断所需的列值存在并合法, 若
  是这样, 再进行 inter-field 或 model 整体的 clean & validation.
  若不满足前提条件, 不该报错. 而是默默返回.

validators
----------

a callable that takes a value and raise ValidationError if it failed.
由于是 callable 即可, 所以还可以是 object with ``__call__`` method.

注意 class-based validator 若要用在 model field 中, 应该保证 serializable.

validators can be added to model fields and form fields.

builtin validators ``django.core.validators``.

* various string validators.

  - RegexValidator, 通用正则 validator.

  - URLValidator, a RegexValidator subclass for url.

  - EmailValidator.

  - validate_email, a EmailValidator instance.

  - validate_slug, a RegexValidator instance for slug, i.e., letters, numbers,
    underscores and hyphens.

  - validate_unicode_slug, a RegexValidator instance for unicode slug.

  - validate_comma_separated_integer_list, a RegexValidator instance.

  - int_list_validator, a RegexValidator instance.

  - MaxLengthValidator.

  - MinLengthValidator.

  - ProhibitNullCharactersValidator

* ip address.

  - validate_ipv4_address, for ipv4.

  - validate_ipv6_address, for ipv6.

  - validate_ipv46_address, for both ipv4 and v6.

* numerical:

  - MaxValueValidator.

  - MinValueValidator.

  - DecimalValidator.

* file:

  - FileExtensionValidator.

  - validate_image_file_extension

model instance
--------------
* instantiation.

  model instance 的列值来自

  * args and kwargs. 一般只使用 kwargs 形式即可. 若 args and kwargs 都有,
    对于一个 field 优先使用 args 的值.

    - 对于 FK field, 有两种指定方式:
      ``<FK-field>=<FK-model-object>``, ``<FK>_id=<FK-model-object>.{id|pk}``.
      这不同于 field lookup, 不支持 id 和 object 交叉混合的方式.

  * field 的默认值 ``Field.get_default()``.

  可以看出在实例化时, 所有的列都一定会有个值.

- 对于 model class 在实例化时, Django doesn’t hit the database until you
  explicitly call ``save()``.

- ``INSERT`` 和 ``UPDATE`` 都是用 ``.save()`` 实现.

- 对实例中 ``ForeignKey`` ``OneToOneField`` 等指向单一 model 实例的 field 赋值
  时使用相应 model 的 instance 即可. 给 FK field 赋的 model instance 可以是尚未
  保存的 (即还没有 pk 值). 在 ``Model.save()`` 时, 会检查 FK 指向的 instance 
  是否有 pk, 若否会报错. 因此必须首先保存.

- 实例中的 ``ManyToManyField`` 实际上是一个 Manager object, 需要用 ``.add()`` 给
  这个集合中增加关联关系. ``.add()`` 接受一次传入多个对象, 建立多个映射.

QuerySet
--------

evaluation and cache
^^^^^^^^^^^^^^^^^^^^

evaluation
""""""""""
- QuerySets are lazy. 在必须访问数据库之前, 所有的过滤筛选等操作都只在内存
  中构建类似于 AST 的结构, 并不编译至 SQL 语句和访问数据库执行语句. 这种
  不同阶段的分工类似于解释器 lex 阶段构建语法树, 编译阶段生成可执行 bytecode.

- 以下操作导致 queryset being evaluated:

  * iteration. Any operation that calls ``__iter__``.

  * Slicing operation that involves ``step`` argument.

  * Pickle queryset.

  * representation ``__repr__``

  * length ``__len__``

  * testing queryset in a boolean context ``__bool__``.

- 注意并不是所有 queryset evaluation 都会填充 cache.

cache
""""""
- QuerySet cache. The first time a QuerySet is evaluated – and, hence, a
  database query happens – Django saves the query results in the QuerySet’s
  cache and returns the results that have been explicitly requested. Subsequent
  evaluations of the QuerySet reuse the cached results.

- QuerySet slicing 时的 cache 处理.

  当取一个 QuerySet 的部分数据时 (通过 extended indexing syntax, 即转换成
  ``OFFSET`` ``LIMIT``), 若本身有 cache, 则直接返回结果, 否则只访问数据库
  (如果需要访问的话) 进行所需部分数据的查询和返回, 并不 cache. 这里的抽象
  逻辑是, slicing 和 indexing 这些操作是在一个完整的 QuerySet 上进行的部分
  截取. 而 cache 是属于 QuerySet 的, 若有则应该包含它代表的所有数据.

- ``bool(queryset)`` 会计算整个 ``queryset``, 从而填入 cache.

- ``print()`` ``repr()`` 只计算整个 QuerySet 的一个 slice, 因此不会填入
  cache.

- QuerySet 的外键列的 cache 处理.

  若模型包含 ``ForeignKey`` ``OneToOneField`` field 时, QuerySet 在取实例时
  相当于只将 FK_id 取回来, 而不会自动 JOIN 表查询取到关联的对象数据. 这是
  为了避免不必要的 overhead. 当用户明确要访问 FK object 这个属性时, 才再次
  访问数据库将数据填入 cache, 返回真实的关联对象. 之后再访问该属性时不再
  访问数据库.

pickling
^^^^^^^^
- Pickle a queryset force all results to be loaded and cached. 这是因为 pickle
  的目的往往是为了能从 pickled 数据快速重建原对象. 如果不保存 queryset 中的实例,
  仍需从数据库中获取 (较慢, 并依赖于外部数据库), 就失去了 pickle 的意义.

- 注意 when you unpickle a QuerySet, it contains the results at the moment it
  was pickled, rather than the results that are currently in the database.

- 若希望 unpickle 时从数据库重新加载内容. 可只 pickle ``QuerySet.query`` attribute.

constructor options
^^^^^^^^^^^^^^^^^^^
- model. 与这个 QuerySet 关联的 model.

- query. 设置与这个 QuerySet 关联的底层 SQL Query object. 默认 None, 创建一个新的
  Query object.

- using. 限制操作在哪个数据库上. 默认 None, 不指定.

attributes
^^^^^^^^^^
- model.

- query. 与这个 QuerySet 关联的底层 SQL Query object. 这个 Query object
  保持着 QuerySet 的所有 internal sql query state.

- ordered. whether or not the queryset is ordered.
  A queryset is ordered if one the following is true:

  * it has a ``order_by()`` clause

  * its model has a default ordering ``Meta.ordering``.

  检查一个 QuerySet 的最终 ORDER BY 效果::

    QuerySet.query.get_compiler(DEFAULT_DB_ALIAS).get_order_by()

- db. the db to be used for this queryset.

methods
^^^^^^^
- QuerySet 封装了 database entries 以及对数据的 CRUD 和聚合等操作.

- 获取对象的各个方法在 ``Manager`` 和 ``QuerySet`` 中都有 (在 QuerySet 中定义,
  expose to Manager 中), 且可以串联在一起. ``.delete()`` 是唯一的 QuerySet 有
  但 Manager 没有的方法 (为了避免误删全部).

representation
""""""""""""""
- ``__repr__``.

boolean operation
""""""""""""""""""
- ``__bool__``.

pickling
""""""""
- ``__getstate__``

- ``__setstate__``

limiting queryset
"""""""""""""""""
- slicing operation (extended index syntax), ``__getitem__``.

  * Slicing an unevaluated QuerySet without ``step`` argument, returns another
    unevaluated QuerySet. Slicing with ``step`` argument will evaluate the
    queryset.

  * Slicing an evaluated queryset returns a list of object. Thus, slicing with
    step parameter will return a list (queryset is evaluated implicitly).

  * A sliced queryset can not be modified further, since it doesn't translate
    well to SQL.

counting
""""""""
- ``count()``

- ``__len__()``. 这需要 fetch all objects, 只有当 cache 已经填充, 或者后续需要
  使用 cache 时才这么用. 若只需要 count, 使用 ``count()``.

filtering
""""""""""

- ``filter(*args, **kwargs)``.  positionals 是 Q objects, kwargs 为 field
  lookup syntax. 匹配所有条件同时满足的.

- ``exclude(*args, **kwargs)``. ditto. 但是排除所有条件同时满足的. 实现上
  相当于 ``filter(~Q(*args, **kwargs))``. SQL::
 
    NOT (condition1 AND condition2)

  若要排除 matching condition1 OR matching condition2 的::

    exclude(<condition1>).exclude(<condition2>)

  SQL::

    NOT condition1 AND NOT condition2

sorting
""""""""

aggregation
""""""""""""
- ``annotate(*args, **kwargs)``
  Annotates each object in the QuerySet with the provided list of query
  expressions.
  
  这不仅仅可用于 ``GROUP BY`` 聚合, 还可用于对每行返回所需
  的运算结果, 即 annotate 的一般含义. 使用这个一般意义, 还可以进行 sql
  ``SELECT name AS name2`` 操作: ``queryset.annotate(name2=F("name"))``.

  * 到底是聚合, 还是单纯地 annotation, 取决于使用的 query expression
    的属性和操作.

  * annotate 语法与 aggregate 相同, 但是每个聚合值是 attach 到各个
    元素上的, 成为元素的 attribute.
    
  * attribute name.
    
    对于 kwargs, keys 成为新增的 attribute names.
    
    对于 positionals, attribute name is generated for them based upon the name
    of the aggregate function and the model field that is being aggregated::

      <field_name>__<expression_name>

    Only aggregate expressions that reference a single field can be positional.

  * 由于结果成为了 attributes, 返回的仍是一个 QuerySet, 因此可以继续
    operation chain.

  * annotate 增加的 attributes 可以在后续的 operation chain 中使用, 例如
    用于进一步 ``filter()``.

  * 使用 annotate 进行多项聚合时必须要谨慎, 很可能结果不对, 并且必要时检查
    生成的 raw sql statements. 多项聚合结果可能错误的原因是 django 简单
    地将多项聚合条件涉及的所有表 join 在一起, 然后再算聚合值.

  * GROUP BY 使用的列.
    
    - 默认情况下, GROUP BY 使用 model PK.

    - 若 queryset operation chain 中, ``.annotate()`` 前面有 ``.values()``
      或 ``.values_list()`` 且它们指定了列参数 (不是无参的), 则 annotate 时
      的 GROUP BY 会使用这些列来分组, 不再使用原 model 的 pk. 此时, annotate
      的结果不再与各个 model instance 对应. 这样, 生成的组不再局限于 model
      instance.

      注意, 此时 ``.values()`` ``.values_list()`` 选择的列, 以及 ``.annotate()``
      中新增的列, 是在 GROUP BY 之后进行的. SQL 对应为::

        SELECT <values/values_list columns and annotate columns>
            FROM <some_table>
            GROUP BY <values/values_list columns>;

      需要明确, 当 annotate 出现在 ``.values()`` ``.values_list()`` 后面时,
      并不是说只剩下了它们选择出来的列, 而是最终从表中中取出这些列. 所以,
      annotate 仍然可以访问所有在原来表中存在的列, 它不限于 values, values_list.

- ``aggregate(*args, **kwargs)``

  给整个 QuerySet 生成各种聚合值.

  * 需要执行的聚合操作通过 positional args 或 keyword args 来指定.
    返回聚合结果 dict. key 是聚合项, value 是聚合值. key 自动根据
    field name 和聚合操作名生成; 或者通过 keyword 参数指定.

  * 由于返回一个 dict, 所以 ``.aggregate`` 要作为 QuerySet chain 的最后操作.

get, create, update, delete
""""""""""""""""""""""""""""
For retrieval operation, QuerySet itself serves as ``SELECT`` SQL equivalent,
whereas ``get()`` API is just a convenience method to get out a single model
instance.

- ``create(**kwargs)``. Create a model instance and save it. Return the created
  instance.

- ``update(**kwargs)``. Update the matched rows with ``kwargs``, then return
  the number of rows matched.

  更新操作是批量进行、立即生效的. 它使用 ``UPDATE`` statement, 无需从数据库取
  数据, 因此不创建和填充 model instance. 因此各种 model 层的封装特性, 例如
  custom ``save()``, auto_now, pre_save/post_save signal 等都不会生效.

CRUD
""""
* attributes & methods.

  - ``.all()``

  - ``.get()``, 生成的 sql 与 ``.filter()`` 的相同, 也就是说取回的
    queryset 可能是多行的, 没有在数据库层做 LIMIT 1 之类的限制.
    而是在 python 中检查返回的是否为一行, 若不是则 raise DoesNotExist
    或者 MultipleObjectsReturned.

  - ``.get_or_create()``. lookup params 应注意保证筛选条件的唯一性. 这不但是 get
    部分的要求, 也是保证 create 部分创建实例时唯一性的要求. 例如, 在多个线程中同时
    使用该方法时, 若一开始 get 失败, 同时进入 create 阶段, 但由于条件的唯一性,
    只有一个 create 可以成功. 若条件不唯一, 将导致生成多个实例.

  - ``.distinct()``, 相当于 ``SELECT DISTINCT`` statement.

  - ``.order_by()``, ``-<field>`` 表示逆序, ``?`` 表示随机, 可使用 field
    lookup 指定 related model fields. 若指定的 field 是 relation field,
    使用相关 model 的默认排序, 如果没有默认排序, 使用 pk. 若希望生成的
    SQL 完全避免排序 (甚至避免 model 默认排序), 使用无参 ``.order_by()``.
    若要排序的是 reverse FK, many-to-many 类关系, 注意涉及到 JOIN, 原来的
    一行可能排序后变成多行.

    ``?`` 随机排序跟不排序完全是两码事. 前者是对每行加入一个随机值然后再
    根据这个值去排序各行, 对应的 sql 是 ``ORDER BY RAND() ASC``; 后者的
    话就完全不排序, return in unspecified order.

    chained ``.order_by`` 只有最后一个有用.

  - ``.values()`` 给出的 QuerySet 每个元素为 field-value mapping dict, 方便
    遍历.

    可通过 positional args 指定要返回的 fields/field lookup.

    通过 kwargs 传递聚合参数给 ``.annotate``. 这可用于对返回的 dict 中增加计算项.

    注意 ``.values()`` 返回的仍是 QuerySet, 可以继续 chain 下去.

    对于 FK field, 返回的 dict 中 key 是 ``<field>_id``.

    对于 many-to-many field 若没有明确在参数中指定, 则不返回, 这是因为需要 JOIN,
    导致 QuerySet 中的结果重复. 同理, 若明确指定 reverse FK, 也导致结果集重复.

  - ``.values_list()`` 给出的 QuerySet 每个元素为 fields tuple.

    positional args 指定的 fields 可以包含 query expression, 这样在返回的
    fields tuple 中包含计算项.

    多值关系中可能造成结果重复:

    values() and values_list() are both intended as optimizations for a
    specific use case: retrieving a subset of data without the overhead
    of creating a model instance. This metaphor falls apart when dealing
    with many-to-many and other multivalued relations (such as the
    one-to-many relation of a reverse foreign key) because the “one row,
    one object” assumption doesn’t hold.

  - ``exists()``, 判断 queryset 是否是空的.
    
    这还可用于实现高效的 ``elem in queryset`` 式的判断. 即
    ``queryset.filter(<elem-filter>).exists()`` 比 ``in`` operator 高效.
    因为由于 queryset 的实现, membership 检查要 调用 ``__iter__`` 做遍历.

- 使用 extended indexing and slicing syntax 来进行 ``LIMIT`` ``OFFSET`` 之类的
  操作. 注意 negative index 是不允许的. 如果是单个的 index, 就返回 QuerySet
  中的单个结果, 如果是 slice, 就返回一个 QuerySet. 一般情况下返回的 QuerySet
  仍然是 lazy 的, 但若 slice syntax 中有步长参数, 则会计算 QuerySet, 访问数据库.

- 在过滤方法串联中, 每次返回的 ``QuerySet`` 都是相互独立的, 各自可以单独使用,
  不会相互影响.

- 同一个 model 的实例之间进行比较时, 比较的是 primary key. 不同 model 的实例
  之间总是不相等的. 但是大小关系没有确定结果. (why not TypeError?)

- delete.

  * 删除时会返回删除的总对象数目和每个类型删除的对象数目. 这么做的一个
    重要原因是模型或表之间有设置了级联删除的.所以很可能一个删除操作一下子级联
    删除了很多不同表中的条目.

  * model instance 和 QuerySet 都有 delete method.

- ``select_related()``.
  如果用户在查询某模型时, 已知会访问到关联的 FK 对象, 可使用 ``select_related()``
  来强制进行 JOIN 操作, 一次把所有 FK 对象数据取回来, 这样更高效. 避免获取各个
  FK object 时再单独访问数据库. To avoid the much larger result set that would
  result from joining across a ‘many’ relationship, ``select_related`` is limited
  to single-valued relationships - foreign key and one-to-one.

  支持 field lookup syntax, 从而可以 select 多层 FK 关系::

    .select_related("a__b__c")

  同时 select 关联的 a 条目, 与 a 关联的 b 条目, 与 b 关联的 c 条目.

- 对于十分复杂的一长串的 ORM 操作 QuerySet (涉及可能多个过滤、聚合等), 如果对它
  到底会怎么执行不确定, 需要检查 raw SQL 长什么样子, 通过 ``QuerySet.query``.
  对于直接执行不返回 queryset 的情况, 直接看 ``django.db.connection.queries``.

- 由于排序导致的反直觉现象.

  若 model 有设置 ``Meta.ordering``, 或者 queryset 有含参的 ``.order_by()``,
  则生成的 SQL 里一定会排序. 且 django 会在 select 部分添加排序相关的列.
  进一步, 若 GROUP BY 不是按照默认的 id 来分组, 则会在现有的分组 fields 列表
  中添加排序相关列. 即使这些排序列不在最终的 queryset 中作为 attribute 出现,
  它们也会在 SQL 中被包含.

  这可能导致 DISTINCT, GROUP BY, aggregation 等结果与预期不符. 需要小心对待.

raw SQL
^^^^^^^
``QuerySet.raw()`` 和 ``Manager.raw()``.
输入 SQL statements, 输出 ``RawQuerySet``.

Should be used sparingly and carefully.

Field lookups
^^^^^^^^^^^^^
各种过滤和获取的方法的参数语法, 对应到 SQL ``WHERE`` clause.
Syntax: ``<field>[__<field>...][__<lookuptype>]=value``.
若省略 lookuptype, 默认是 ``exact``.
常用 lookuptypes: ``exact``, ``iexact``, ``contains``, ``icontains``,
``startswith``, ``endswith``, ``istartswith``, ``iendswith``.

* 对 foreign key field 指定条件, 可以用以下方式进行判断: 1. FK 列 与 FK object
  实例进行比较; 2. FK 列 与 FK 值进行比较; 3. 使用 ``<FK>_id`` 虚拟的列
  和 FK 值进行比较.

* 对 many-to-many 关系进行 lookup 时, 由于实质上是在 through table 中对 FK 指向
  的 entry 进行匹配. 即进行单行的匹配: 对这个对象关联的所有对象进行单行的匹配,
  只要有一行匹配上了, 就认为 main object 符合条件. e.g.,

  注意, 由于 table JOIN 操作, 这样的匹配很容易在结果集中出现重复的 object,
  所以需要对结果去重.

* 对于 FK/M2M 等关系列, 如果需要指定该关系是否存在 (即是否有关联的 related
  object) 时, 可使用 ``related_field=None``. 这对应于 SQL 里 JOIN 之后筛选
  IS NULL 之类的操作.

* 对于表达关系的列, 可以从多至一的方向深入被指向的模型进行筛选, 这抽象了各种
  SQL ``JOIN``.

* 这种过滤可以反向进行, 即从一至多的方向进行筛选. 注意这与属性访问时得到
  RelatedManager 虽然语法相通, 但意义不同. 这里是通过对 related model 的行
  指定筛选条件, 来筛选 main object.

  reverse lookup 的起点是那个 model 中设置的 relation field 的
  related_query_name 值. 在此之后再指定 related model 中的 field 和条件.

* 对于每个查询方法, 传入的所有 positional and keyword arguments (Q objects +
  field lookup syntax) 代表的条件都会 ``AND`` 在一起. 注意对于 ``.exclude()``,
  取了一个反.

* django 提供了一个特殊的 ``pk`` field 名称, 用来代指当前 model 的 pk field,
  它可以像实际的 pk field 一样去写任何 field lookup 语法.

* 对于字符串比较的各种 lookuptype, 基本上都转换成了 ``LIKE`` 类语句. 在这些
  语句语法中, 由 SQL metachar ``%`` 和 ``_`` 概念. 在 django 层, 若输入这两个
  字符, 将自动在 SQL 层进行转义, 保证 django 的抽象与底层 SQL 实现无关.

* 注意到 lookup type 只有 positive 的, 没有 negative 的, 这些只能使用
  ``QuerySet.exclude()`` 或 Q expression 配合 positive lookup types 构建.

query expressions
^^^^^^^^^^^^^^^^^

* ``F()`` expression 在 CRUD 操作中代表一个列的值 (F for Field) 的 symbolic
  form. django 不会去访问数据库将值取出来, 与 F expression 进行的各种操作的
  结果是 ``CombinedExpression``, 仍然是保持 symbolic form. 当 ``.save()``
  ``.filter()`` 等访问数据的操作时, 这些 symoblic expression 转化为 SQL
  statement, 让数据库去执行所需操作. 全程不在 python 层进行数据的读写. 全部
  由数据库进行.

  这样的好处: 1. 效率更高, 因为没有读入内存和写回数据库的过程, 而是全部由数据库
  自身去操作. 只是生成 SQL instruction 让数据库去执行. 2. 由于操作在数据库进程
  中而不是业务代码的 python 进程中执行, 可以避免 race condition.

  Django supports the use of ``+ - * / % **`` with F() objects, both with
  constants and with other F() objects. 也就是说 ``F`` 定义了对这些算符的
  overriding special methods.

  F objects 还支持一些 bit operations: ``.bitand()``, ``.bitor()``,
  ``.bitrightshift()``, ``.bitleftshift()``.

  注意在保存包含 F object 的 model instance 之后, 需要 ``.refresh_from_db()``,
  不然的话 instance 的属性仍然是 ``CombinedExpression``, 而不是真实的值.
  如果对这些实例再次 save, 将再次执行 combinedExpression 对应的数据库过程,
  从而进行了重复修改.

* ``Q()`` expression 用于将查询条件模块化成一个个可任意组合的抽象单元.
  Q object 可以进行与、或、非操作 (``&`` ``|`` ``~``), 构成表达复杂逻辑
  的 Q object. 它最终在底层转化成恰当的 SQL 查询语句.

  ``.filter()`` ``.get()`` 等查询方法除了可以接受作为 kwargs 的 field lookup
  语法, 还支持传入多个作为 positional args 的 Q objects, 这些 Q object
  代表的条件会 ``AND`` 在一起. 这真是把 python 函数语法运用到极致了啊!!
  抽象得真好!!!

* conditional expressions. ``Case()`` ``When()`` 封装了 ``CASE WHEN`` SQL
  语句.

  - ``When``. 条件通过 positional Q objects 或者 keyword field lookup syntax
    指定. 结果通过 ``then=`` 指定, 结果可以是一个 query expression.
    
    注意, 如果 ``then=`` 的值是一个 string, 会被认为是 field name, 从而转换成
    ``F()`` expression. 若需要 literal value, 使用 ``Value()`` expression.

  - ``Case``. 接受 positional ``When`` objects 作为 cases, 这些 When objects
    依次执行, 直到有一个为 True 为止, 返回的结果是相应的 When 的 then.
    若没有一个 When 为真, 则返回 ``default=`` 值或 None.

* aggregation expressions.

  - 各聚合函数的参数是列, 并可使用 field lookup syntax 去指定任意 related table
    field.

  - QuerySet 为空时, 除了 Count 之外所有 aggregate function 都返回 None,
    Count 返回 0.

  - 所有 aggregate function 接受一个 positional arg 作为要聚合的对象, 这可以是
    field lookup syntax 也可以是 query expression.

  - 所有 aggregate function 接受一个 ``output_field`` kwarg, 指定输出列的类型.

  - ``Count()`` 有 ``distinct`` 参数, 对应于 ``COUNT(DISTINCT <colname>)``.

  - ``Avg``

  - ``MAX``

  - ``MIN``

  - ``StdDev``

  - ``Variance``

  - ``Sum``

RawQuerySet
-----------
An iterable. Iterating its resultant iterator yields model instances.

SQL query 中的列名需要和 model field name 对应或者使用 ``translations=``
参数指定映射关系, 才能正确生成 model instance.

SQL query 的参数使用 ``params=`` 传入. 为了避免 SQL injection attack,
不要使用 str.formatting, 不要 quote parameter placeholder.

若 SQL 中 SELECT 的列不是 model 的全部列, 而只是一部分, 则返回的 model
instance 是 defered model instance. 注意 primary key field 不能省去,
否则后续获取 defered fields 时无法定位 entry 了.

SQL 中除了 model field 之外的列, 会在结果中以 annotated field 形式出现.

methods.

- 显然 QuerySet 的很多方法 RawQuerySet 都不具备. RawQuerySet 没有实现
  ``__bool__`` & ``__len__``, all RawQuerySet's are True.

- ``__getitem__``. 支持 sequence indexing protocol. 但实际上是在内存中
  进行 indexing. 即全取回来成 list, 再 index. 对于大数据量要避免, 而
  应该使用 OFFSET, LIMIT.

Manager
-------

BaseManager
^^^^^^^^^^^

class attributes
""""""""""""""""
- ``use_in_migrations``. Serialize the manager and use it during migration.

attributes
""""""""""

* ``auto_created``. 该 manager 是否是自动创建, 而不是在 model class 中明确定义的.

* ``model``. The attached model class.

* ``db``. 使用的数据库.

methods
"""""""

* ``db_manager(using=None, hints=None)``. 生成一个使用指定数据库的 manager
  instance.

* ``check(**kwargs)``. perform checks regarding this model manager. 这里什么也
  没检查. 子类扩展 system checks 时, 应将每个测试点放在一个单独的 non-public
  method 中.

Manager
^^^^^^^

每个 model 都有至少一个 ``Manager`` instance, 用于进行 table-level operations.
``Manager`` instance is accessible only via model class, rather than from
model instances, to enforce a separation between “table-level” operations and
“record-level” operations.

Manager object 是对某个 model 进行表级别的数据库的起点. 它将所有合适的 QuerySet
methods 都 attach 到这个 manager class 上. 它的本质是从 manager object 上访问
任何 queryset method 的时候, 都立即创建一个 QuerySet object, 然后就是正常的
queryset methods 操作.

methods
"""""""

- 从 QuerySet 复制过来的各种 methods. 复制标准:

  * Public methods are copied by default.

  * Private methods are not copied by default.

  * ``queryset_only=True`` methods are not copied.

  * ``queryset_only=False`` methods (even if private) are copied.

specify manager in model
^^^^^^^^^^^^^^^^^^^^^^^^
- 当定义 model 时, 若不明确指定 manager (无论是修改 manager name 还是 custom
  manager class), 则会自动生成 ``objects = Manager()`` manager. 若明确设置,
  可以设置任意个 managers. This is an easy way to define common “filters” for
  your models.

- default manager.

  * 定义. 由 ``Model.Meta.default_manager_name`` 指定一个已定义的 manager 作为
    default manager. 若其值为 None, 自动选择 model class 中第一个定义的 manager
    object 当作 ``_default_manager``.

  * 作用. default manager 允许进行一些默认的过滤等操作, 这是作为访问该 model
    数据时进行的默认过滤. 当程序逻辑需要访问一个非确定的 generic model 的
    manager 时, 应使用 default manager, 而不该假设 ``objects`` manager 存在.

- base manager.
  
  * 定义. ``Model.Meta.base_manager_name`` 指定使用预定义的某个 manager 作为
    base manager. 若值为 None, 自动生成一个标准 ``django.db.models.Manager``
    作为 base manager. 该 manager 不包含在 ``Model._meta.managers`` 中.

  * 作用. 相比于 default manager, base manager 一般不进行任何过滤. 可以默认
    认为它提供该 model 最全的数据集. 例如, 当通过一个 model instance 访问
    FK/O2O 类型的 related object 时, 会使用 related model 的 ``_base_manager``
    获取 queryset (再筛选出关联的 entries), 而不是使用 ``_default_manager``. 这
    是因为 default manager 可能进行了一些过滤和限制.

    注意对于 M2M 类型的 related manager 仍然是 default manager 的 subclass.

custom manager
^^^^^^^^^^^^^^
subclass ``django.db.models.Manager`` 以进行自定义.

- 添加 custom manager method. 用处:
  
  * 当需要对 models 添加 table-level 的功能和操作时 (而不是对 row-level 即具体
    model instance 的方法.)

  * table-level 的 ORM 操作, 可以封装成 custom manager helper methods. 在
    form/view 等上层代码中不直接写 ORM method chain, 而是将所有 ORM code 塞到
    model-level 代码中. 这样做有至少两点好处: 1) 提高可读性 2) 将应用与业务逻
    辑与 django-specific ORM 解耦合.

  * 是否应该将 ORM 操作封装成 manager 的 helper method 仍然要根据具体情况去
    具体分析. (Does it worth the effort?)

- 一些常见的 custom manager method.

  * ``get_by_natural_key(...)``. 该方法的输入是能够 uniquely identify
    ``Manager.model`` 的一条数据的信息, 输出是 model instance.

- customize initial queryset. override ``get_queryset()`` method.
  ``Manager.all()`` method 的返回值与之一致.

自定义的 manager class 必须能够 shallow copied by ``copy.copy()``.

related manager
^^^^^^^^^^^^^^^
- related manager. 一对多、多对多关系中, 正向的 manager object (如果有) 是属性名,
  逆向的 manager object 默认是 ``<lower_model>_set``, 可通过 ``related_name``
  自定义. 在一对一的关系中, 正反向都是对称直接访问的.

- ``RelatedManager`` 的一些方法: ``add()``, ``create()``, ``remove()``,
  ``clear()``, ``set()``. 这些操作都是立即在数据库生效的.

- 在访问 related objects, 如需使用 custom related manager, 可以
  通过 ``RelatedManager.__call__`` 来指定想要使用的 custom manager.


in model inheritance
^^^^^^^^^^^^^^^^^^^^
- model 继承 parent model 定义的 managers. 标准的 python inheritance 机制.

- 若 model 和 parents 都没定义 managers, 自动创建 ``objects`` manager.

- default manager 若没指定, 使用该 model 中定义的第一个 manager 或 parent
  model 的 default manager.


signals
-------
- ``m2m_changed``

  * ``pk_set``. 不能保证这只包含确实需要添加或删除的 pks, 只能保证是
    ``.add()``, ``.remove()`` 等方法传入的一个子集. 所以如果必须, 应该
    在 signal handler 中进行检查.

design pattern
--------------
- 假如对于一个复杂查询, 难以映射映射成基于现有模型的 ORM 操作, 需要使用 raw
  SQL, 如果这个查询的每行结果实际上可以看作是某种 model 的实例, 则可以考虑将这
  个逻辑写成 database view, 在 django 应用中设计相应的 unmanaged model. 从而转
  化为 ORM 操作.

  这样做至少有以下好处:

  * 无需手动处理数据库读操作. 只有初始的 view 创建写死了 SQL. 其他操作都可基于
    ORM. 挽救了一定的灵活性.
   
  * 无需手动进行数据库和 python 数据类型的转换.

  * 该模型可作为基础, 提供更多的操作可能性.

database
========

settings
--------
- ``settings.DATABASES`` 定义项目需要使用的数据库. 项目可以使用多个数据库.  注
  意多个数据库可以使用相同或不同的 database engine.

- 一般使用 ``default`` database 即可. Django uses the database with the alias
  of default when no other database has been selected.

subsettings
^^^^^^^^^^^

- ``TIME_ZONE``. 其值与 ``settings.TIME_ZONE`` 形式相同. 用于指定该数据库内的
  datetime values 所使用的时区 (当 datetime field 不支持时区时).

  对于 django 维护的数据库, 不该设置这个参数. 使用默认值 None 即可. 这是因为
  默认 django 转换时间至 UTC 来保存 (对于不支持时区的 db backend), 保证了
  timezone-agnostic. 可在 django 层方便地转换成所需时区.

  * 若 ``USE_TZ``, 且 db backend 不支持 aware datetime, datetime is converted
    to this timezone if set or UTC if not set.

  * 若 ``USE_TZ`` 且 db backend 支持 aware datetime, 设置该参数会报错.

  * 若根本不 ``USE_TZ``, 设置该参数会报错, 因全部 datetime 使用原始时间.

backend-specific notes
^^^^^^^^^^^^^^^^^^^^^^
mysql
"""""

* 对于 mysql, 配置值加载顺序. (优先级低至高.)

  1. MySQL option files. 因为 mysqlclient 调用 libmysqlclient C API
     ``mysql_options()``, 加载各种 mysql 配置文件. 这里关注的是配置文件中
     client group 的配置.

  2. NAME, USER, PASSWORD, HOST, PORT. 转换成连接参数.

  3. OPTIONS. 里面直接写 ``mysqlclient.connect`` 允许的各种连接参数. 应
     包含::

      'OPTIONS': {
          # "read commited" is default for django2.0+
          'isolation_level': "read committed",
          'charset': "utf8mb4",
      }

* 保证服务端 ``sql_mode`` 开启了 STRICT_TRANS_TABLES. 对于 mysql 5.7+ 这是
  默认值, 因此不用配置.

* 设置 isolation level.

  django is designed for ``read committed`` isolation level, it won't work
  *correctly* under another isolation level. This is default for django 2.0+.
  不用配置.
  
  例如, 当使用 atomic request 时, 若多个线程中同时 get 一个 entry,
  即使其中一个 create 已经 commit, 在别的中也不可见, 仍然会 create,
  等到 request 处理结束 commit 时才报错, 返回 500 internal error.
  也就是说, atomic request 与 repeatable read isolation level 一起,
  更容易做无用功, 并返回 500.

  所以不能用 mysql default ``repeatable read``. 在 django 2.0+, 连接时默认会
  设置 mysql isolation level 为 read committed.

* 使用 ``charset`` OPTIONS key 保证 mysqlclient 和服务端之间通过 utf8mb4
  charset 通信. 由于不能保证 django server 运行的环境中有 mysql 配置文件, 因此
  需要在这里配置.

* 对于测试数据库, 需要保证创建数据库时使用的 charset 为 utf8mb4, 以及合适的
  collation. 如果 mysqld system variable 已经设置 ``character_set_server`` 为
  utf8mb4, 并设置了合适的 ``collation_server``, 则不需要单独设置.  否则的话, 需
  要单独设置一个 ``TEST`` dict::

    'TEST': {
        'CHARSET': "utf8mb4",
        'COLLATION': "utf8mb4_unicode_520_ci", # 或其他更优化的 collation.
    }

sqlite3
""""""""

- 由于 sqlite 数据库就是单个的文件, 默认配置下无需手动创建数据库. django 会自动
  创建数据库文件.

database connection
-------------------
- default connection: ``django.db.connection``.
  这是与 ``settings.DATABASES['default']`` 配置的数据库相对应的连接.

- all connections: ``django.db.connections``.
  包含该 django project 配置的全部 databases 连接, 每一项与 ``settings.DATABASES``
  对应.

- Connection & cursor implement Python DB-API (PEP-249).
  SQL statement 使用 ``%s`` placeholder.

- 由于 db backend 实际使用的 driver 创建的 Connection object (according to DB
  API) 可能只具有 threadsafety = 1, 即 Connection object 不能在线程间共享, 所以
  ConnectionHandler 保存了一个 thread-local 的 ``self._connections`` 存储, 用于
  保存线程独立的 db backend 实例 (backend 实例中 wrap 底层的 Connection
  object).

persistent connection
^^^^^^^^^^^^^^^^^^^^^
- ``settings.DATABASES.CONN_MAX_AGE`` 设置数据库连接的最大持续时间. 即
  persistent connection.

  默认值为 0. 效果是, 对每个请求开启一次连接, 即 nonpersistent connection.  具
  体而言, 当处理请求中需要访问数据库时, 开启一个数据库连接; 然后在请求处理结束
  时把连接关掉.

  设置为 None 则永不关闭连接.

  注意 persistent connection 的时长必须与数据库方面的相关 timeout 设置相匹配
  才可以. 对于 mysql, 相关设置为 ``wait_timeout``.

- 对每个数据库, 每个线程 (或进程, 取决于 server 的机制) 最多开一个连接即可.  因
  线程已经是最小的并行处理单元, 每个线程中同时只能处理一个请求 (即使是使用
  coroutine 进行异步处理). django 服务端最多同时保持的数据库连接数目取决于服务
  器线程数 (或进程数).

- persistent connection 的好处是, 在高并发 (大量客户端请求) 情况下, 避免每个请
  求重连数据库带来的效率损耗.

- persistent connection 的坏处是, 提高了数据库服务器的负担. 若数据库服务器需要
  同时去 serve 多个 web 应用. 某个应用建立了很多 persistent connection 就意味着
  别的应用可用的资源少了. 所以如果: 1)该应用的流量并不太大, 2)或者由于 cache 等
  原因, 实际数据库访问并不很频繁, 3)数据库需要 serve 多个应用, 则可以缩短
  persistent connection 的时长, 或使用 nonpersistent connection.

- 注意, 对于流量非常小的情况, persistent connection 可能长时间处于 wait 状态,
  db server 端会等待超时断开, 并记录错误日志 (for mysql)::
  
    Aborted connection ... Got timeout reading communication packets
   
  而 django db 连接层会因连接异常断开而报错 (for mysql)::

    2013, 'Lost connection to MySQL server during query
 
  反映到 HTTP 层为 500 Internal Server Error. 这种情况下不该设置 persistent
  connection. 对于大流量网站, 则没有这个问题.

  .. TODO 但是我不理解为什么 close_if_unusable_or_obsolete 没有检测到该关闭
  这个连接了????

connection management
^^^^^^^^^^^^^^^^^^^^^
- 在处理请求中, 需要访问数据库时, 开启连接.

- 在请求处理结束时, ``request_finished`` signal handler 检查连接是否达
  max age 以及是否可用, 若达到或已经不可用则关闭.

- 在下一次请求开始时, ``request_started`` signal handler 进行相同的检查.

cursor
------

CursorWrapper
^^^^^^^^^^^^^
封装 database library 给出的 cursor object. 封装了或者传递了各种 cursor methods.

BaseDatabaseWrapper
^^^^^^^^^^^^^^^^^^^

methods.

- ``cursor()``. create a cursor.

database transactions
---------------------

* django 对 transaction 的处理逻辑:
  对于 django db API 提供的一些需要通过多个 sql 才能实现的复杂操作 (例如,
  QuerySet.delete(), QuerySet.update()), django 自动构造 transaction
  & savepoints. 对于单个的 sql statement, 默认开启 autocommit mode.

* autocommit.

  django by default runs in autocommit mode (即默认会开启数据库后端的 autocommit
  mode). 意思是, 若当前 SQL statement 并非已经处于一个 active transaction 中,
  则自动将该 SQL wrap 在一个自己的 transaction 中. 根据该语句是否成功, 自动
  commit/rollback.

  autocommit 可以由 ``settings.DATABASES.AUTOCOMMIT`` option 控制.

* ``django.db.transaction.atomic`` decorator/context manager 手动创建
  transaction. For nested ``atomic`` operations, the inner ``atomic``
  create savepoints.

  避免在 transaction 内部 catch ``django.db.DatabaseError``, 因为
  ``atomic`` 是靠这个 exception 判断是否 rollback. 如果需要 catch 这类
  异常, 正确做法是在 atomic block 外部.

  Attempting to commit, roll back, or change the autocommit state of the
  database connection within an atomic block will raise an exception.

  Nested atomic blocks workflow:

  - opens a transaction when entering the outermost atomic block;

  - creates a savepoint when entering an inner atomic block;

  - releases or rolls back to the savepoint when exiting an inner block;

  - commits or rolls back the transaction when exiting the outermost block.

* atomic requests.

  处理 http request 时, 可以直接将整个 view 的操作放在一个 transaction 中.
  从而保证一个 view 进行的所有 db state change 是一起生效或不生效. django
  提供了 ``settings.DATABASES.ATOMIC_REQUESTS`` 自动将所有 view wrap 在
  该数据库的 ``transaction.atomic`` 中. (注意只有 view function 被 wrap,
  middleware 等过程并没有.)

  此时在 view 中, 再使用 ``django.db.transaction.atomic`` 则是在 transaction
  中创建 savepoints.

  若 view 里没有 raise exception, 则 commit; 否则 rollback. 注意, 我们不能在
  view 里随便 raise exception, 不恰当的异常 django 会转换成 500 error. 这是
  不合适的. 因此, 在 atomic views 的前提下, 我们必须规范 view 中 raise 的
  exception, 避免非必要的 500 error:

  - ``Http404`` -> HttpResponseNotFound

  - ``PermissionDenied`` -> HttpResponseForbidden

  - ``MultiPartParserError`` -> HttpResponseBadRequest

  - ``SuspiciousOperation`` -> HttpResponseBadRequest

  - other exceptions -> HttpResponseServerError

  局部禁用 atomic requests: ``django.db.transaction.non_atomic_requests``
  decorator.

  何时使用和不使用 atomic requests: 如果在大部分的 view 的处理中, 需要考虑
  使用 ``non_atomic_requests`` decorator, 则不该设置 ``ATOMIC_REQUESTS``.

* transaction hook: ``django.db.transaction.on_commit()``. 若当前 transaction
  commit 成功, 则执行注册的操作. 可以在 transaction 内部注册多个 hooks,
  在最外层 commit 时按顺序执行.

  如果 on_commit 注册不在 atomic block 中, hook 会立即执行. 这使得即使外层
  transaction 被去掉后, hook 仍能得到执行. 尽管执行时机不一定合理.

  ``on_commit`` hook 还是挺有用的. 例如无法在 transaction 外部直接添加后续执行
  逻辑时, 就可以通过这个 hook 加入代码. 具体而言, 例如在 view 中注册一个
  on commit hook, 在 commit 成功后才发送 celery task, 保证执行顺序, 避免
  任务执行时可能相关数据还没有 commit, 这样就造成了 race condition.

* low-level APIs.

multiple databases
------------------
(什么场景下需要使用多个数据库呢??)

即使使用多个数据库, 并且不想定义 default 数据库, 仍然要定义 ``default: {}``.
此时需要配合定义 ``settings.DATABASE_ROUTERS``, 保证 model 与它所在的数据库
的关联性.

routing scheme
^^^^^^^^^^^^^^
The default routing scheme ensures that if a database isn’t specified, all
queries fall back to the default database.

自定义 routing scheme 通过定义 Router objects, 然后填入 ``settings.DATABASE_ROUTERS``.

Implementation.

``django.db.utils.ConnectionRouter``, 即 ``django.db.router``.

它封装了各种操作对应的 routing method, 例如 db_for_write, db_for_read 等.
加载了 settings.DATABASE_ROUTERS 定义的 Router objects 对各操作进行 routing,
或者 fallback 使用 default routing scheme.

各种数据库操作, 都在恰当的阶段 (如选择数据库时) 会调用 router object 给出
相应的判断和选择.

manually using multiple databases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- queryset chaining 过程中可以在任意位置加上 ``.using()``. 整个就对于该数据库操作.

- model instance methods 有 ``using=`` kwarg.

- manager instance 有 ``.db_manager(using=)`` method.

problems
^^^^^^^^
- unnecessary messy complexity when CRUD with multiple dbs.

- no builtin admin integration

- referential integrity forbids cross-database relations.
  meaning related models must reside in the same database.

- bulitin app relational mess.

tablespaces
-----------
tablespace 需要手动创建, django 不负责创建 tablespace, 只负责使用.

settings
^^^^^^^^
- settings.DEFAULT_TABLESPACE. table 的 tablespace 默认值. 即 ``Meta.db_tablespace``
  默认值. 默认为空. 此时依赖 backend 自己选择 tablespace 处理方式.

- settings.DEFAULT_INDEX_TABLESPACE. index 的 tablespace 默认值.

schema
------
- database schema changes is executed by SchemaEditor (``DatabaseSchemaEditor``).

- Each database backend in Django supplies its own version of SchemaEditor.

usage
^^^^^
::

  with connection.schema_editor() as editor:
      # operations

- A schema editor corresponding to a database connection can be created by
  ``.schema_editor()`` method of a database connection wrapper.

- DatabaseSchemaEditor must be used as a context manager, as this allows it to
  manage things like transactions and deferred SQL (e.g., constraints that
  requires multiple tables to be present, like FK).

- It exposes all possible operations as methods, that should be called in the
  order you wish changes to be applied.

BaseDatabaseSchemaEditor
^^^^^^^^^^^^^^^^^^^^^^^^
- A base DatabaseSchemaEditor for relatively standard SQL-based relational
  databases. It implements all standard schema operations.

class attributes
""""""""""""""""
- A lot of DDL SQL statement templates.

instance attributes
"""""""""""""""""""
- ``connection``. db connection.

- ``collect_sql``. 是否只是记录要执行的 sql statements, used by ``sqlmigrate``.

- ``atomic_migration``. schema changes (DDL statement) 是否在一个 transaction
  中执行. (由 context manager 创建.)

methods
"""""""

utilities

- ``execute(sql, params=())``. execute sql using cursor, or just collect
  them into a list (useful for ``sqlmigrate`` management command).

operations

- ``create_model(model)``. Create model table, all columns, constraints,
  indexes, local M2M intermediate tables, etc. 注意列的默认值不会包含在
  数据库表的定义中.

- ``delete_model(model)``. Delete model table, including local M2M intermediate
  tables.

- ``add_index(model, index)``.

- ``remove_index(model, index)``.

- ``alter_unique_together(model, old_unique_together, new_unique_together)``.
  两个 unique together 分别是原来的和预期的 ``Meta.unique_together``. 这里
  删除多余的, 添加缺少的. 最终达到 new 的效果.

- ``alter_index_together(model, old_index_together, new_index_together)``.
  ditto for ``Meta.index_together``.

- ``alter_db_table(model, old_db_table, new_db_table)``. rename old table name
  to new name.

- ``alter_db_tablespace(model, old_db_tablespace, new_db_tablespace)``. move
  model's table between tablespaces.

- ``add_field(model, field)``. add field instance to model. 对于 M2M field 创建
  intermediate table; 生成 ALTER TABLE statement, 如果定义了非 None 的默认值,
  这里首先会包含在列定义中应用到数据库, 这样是为了给 existing rows 填充默认值,
  然后再 drop default (因为 django 一般使用 django 层的默认值, 不使用数据库层
  default); 添加 table-level index, FK etc.

- ``remove_field(model, field)``. remove field from model. 删除 M2M intermediate
  table, and all related constraints.

- ``alter_field(model, old_field, new_field, strict=False)``. alter various
  aspects of old field matching new field. If strict is True, raise error if
  the old db column definition does not match old field.

test database creation
----------------------
- ``django.db.connection.creation`` exposes test database creation/destruction
  operations related to current connection.

- ``django.db.backends.<backend>.creation`` Encapsulate backend-specific
  operations pertaining to creation and destruction of the test database.

BaseDatabaseCreation
^^^^^^^^^^^^^^^^^^^^

methods
"""""""
- ``create_test_db(verbosity=1, autoclobber=False, serialize=True, keepdb=False)``.

- ``destroy_test_db(old_database_name=None, verbosity=1, keepdb=False, suffix=None)``

authentication and authorization
================================
- django auth module: ``django.contrib.auth``.

- authentication: 管理用户身份. authorization: 管理用户权限.

user model
----------
一个恰当的 user model 是认证和授权的基础.

``./manage.py createsuperuser`` 或 ``AUTH_USER_MODEL.objects.create_superuser()``
创建超级管理员.

managers
^^^^^^^^
If your user model defines ``username``, ``email``, ``is_staff``,
``is_active``, ``is_superuser``, ``last_login``, and ``date_joined`` fields the
same as Django’s default user, you can just install Django’s UserManager;
however, if your user model defines different fields, you’ll need to define a
custom manager that extends BaseUserManager provding two API methods:

- ``create_user()``

- ``create_superuser()``

managers.

- ``BaseUserManager``

  * ``normalize_email(...)``

  * ``get_by_natural_key(...)``, Retrieves a user instance using the contents
    of the field nominated by USERNAME_FIELD.

  * ``make_random_password(...)``

- ``UserManager``

  * ``create_user(...)``.
  若 password=None, set unusable password. 任何不认识的 kwarg 会传入新建的
  user instance.

  * ``create_superuser(...)``

AbstractBaseUser
^^^^^^^^^^^^^^^^
提供了最核心最必须的那些 user model 列和功能, 剩下的所有内容, 包括用户识别列
(username, email 等) 都没有实现, 需要子类去实现. 它提供了 password 管理方法.

在认证方面, 提供 ``is_authenticated`` ``is_anonymous`` 属性用于认证检查.
注意 AbstractBaseUser 以及它的子类在认证方面表示已认证用户, 故该两个属性
分别是只读的 True/False.

子类必须提供 username, email 等信息的列, 并设置必要的配置参数.

- 配置.

  * ``USERNAME_FIELD``, the name of field used as identifier, must be unique.

  * ``EMAIL_FIELD``, used by get_email_field_name().

  * ``REQUIRED_FIELDS``, all required fields on your user model, except for
    USERNAME_FIELD and password. Will be prompted for when creating superuser.

- fields.

  * password. 密码以 hash 形式存放, 符合密码存储的一般准则. 因此不该手动修改
    该属性值. 而使用 ``set_password()``.

  * last_login

- attributes.

  * is_anonymous. always False.

  * is_authenticated. always True.

- methods.

  用户信息获取.

  * ``get_username()``, 这个方法的意义在于它获取 USERNAME_FIELD 的值, 因此
    对 swapped user model 是通用的.

  * ``get_email_field_name()``, ditto for EMAIL_FIELD.

  * ``get_full_name()``

  * ``get_short_name()``

  校验.

  * ``clean()``

  * ``normalize_username()``

  密码管理.

  * ``set_password()`` 参数是 None 时设置 unusable password. 与
    ``set_unusable_password()`` 一样.

  * ``set_password(...)``

  * ``check_password(...)``, 校验密码. 若发现需要更新密码, 则会自动更新.
    例如因为 hash algorithm 有变化或者它默认的 iteration 有变化.

  * ``set_unusable_password()``.
    当使用外部认证机制时, 禁用普通密码. 此时 ``check_password()`` will always
    be False.

  * ``has_usable_password()``

  session.

  * ``get_session_auth_hash()``, Used for Session invalidation on password
    change.

PermissionMixin
^^^^^^^^^^^^^^^
PermissionsMixin 为 user model 提供 Group & Permission 即权限相关数据列
和功能. 便于 custom user model 使用, giving you all the methods and database
fields necessary to support Django’s permission model.

它规定 superuser 有一切权限而无需明确赋予.

- fields.

  * is_superuser. Superuser has all permissions without needing to be
    assigned explicitly.

- relations.

  * M2M with Group, 即用户所属的权限组.

  * M2M with Permission, 即用户本身具有的权限.

- methods. 实现权限相关方法. django 默认的权限控制是 Model level 的, 没有
  实现 instance level 的权限控制. 但它仍然在 API 上预留了 instance level
  权限控制的参数 ``obj``. 这为扩展提供了可能.

  获取权限.

  * ``get_all_permissions()``. 全部权限, 包括自身的权限和组提供的权限.

  * ``get_group_permissions()``. 组提供的权限.

  检查权限.

  * ``has_perm()``. 检查是否有单个权限.

  * ``has_perms()``. 检查是否有多个权限.

  * ``has_module_perms()``. 检查是否有对某个 app 的权限.

AbstractUser
^^^^^^^^^^^^
AbstractUser 实际上完整地实现了 django 所使用的默认的 user model. 它之所以
是抽象的, 是为了 project 在自定义 user model 时能直接利用现有的模型.

基于 AbstractUser 的 user model 有三种用户: 普通用户, 管理员 (is_staff),
超级管理员 (is_superuser). 两种状态: 正常用户和禁用用户 (is_active).

若一个用户不再使用, 应使用 ``is_active`` flag 来禁用用户, 而不是删除. 这样,
与用户相关的各种 FK, M2M 等关系不会失效, 或者被级联删除, 这在历史记录类型的
表方面尤其如此.

auth backend 应当检查用户是否被禁用. 对于 ModelBackend & RemoteUserBackend
都是有检查的.

- fields.

  * username.

  * first_name.

  * last_name.

  * email.

  * is_staff. 对于 admin site 有意义.

  * is_active.

  * date_joined.

- methods.

  * ``email_user()``. A convenient method to send an email to this user.

User
^^^^
User 只是将抽象的 AbstractUser 具体化成实际模型所建立的 placeholder class.
它本身并不定义任何额外的内容, 除了 Meta.swappable. 这样便于 project 自己
去自定义 User model. 即直接 subclass AbstractUser 即可.

- fields, attributes

  * ``groups``.

  * ``user_permissions``.

- methods.

  * ``has_module_perms(<app>)``, 判断用户是否在某个 app 中有至少一个权限.

AnonymousUser
^^^^^^^^^^^^^
AnonymousUser implements basic interface of AbstractUser.

``AnonymousUser`` 虽然不具备很多 ``User`` 的属性和方法, 但是可以进行
认证检查和权限检查. 因为很多时候网站是允许匿名用户的.

在权限方面, AnonymousUser 没有任何组权限, 但注意对于它个人的权限并不一定
是什么都没有, 而是取决于 auth backend.

在认证方面, AnonymousUser 的 ``is_authenticated`` ``is_anonymous`` 分别是
只读的 False/True.

扩展和自定义 user model
^^^^^^^^^^^^^^^^^^^^^^^

- proxy model to auth.User:
  
  purely behavioral extension, use proxy model.

- one-to-one relation to user model:

  store additional information (profile-like infos) related to a user,
  but not auth-related, create new model with ``OneToOneField`` to user model.

  为了在用户创建、删除等操作时两表同步, 需要使用 signal.
  在 admin site 中使用 InlineModelAdmin 同时编辑 user model 和 profile model
  信息.

- custom user model 配合各个 app 中的 app-specific profile models:

  default User model just does not fit your need, create custom user
  model as ``AUTH_USER_MODEL`` to override the default. AUTH_USER_MODEL
  的形式和 relationship field 中引用 field 的形式相同: ``[app_label.]model``.

  即使 User model 已经足够, 也应该使用自定义的 user model, 这样方便之后
  进行扩展.
  If you’re starting a new project, it’s **highly recommended** to set up a
  custom user model, even if the default User model is sufficient for you.
  This model behaves identically to the default user model, but you’ll be
  able to customize it in the future if the need arises.

- 用户相关的信息的存储位置和存储方式.

  * 若这些信息是 app-specific 的, 而不是用户本身的属性、通用的信息或认证和权限
    相关的信息, 则应该存在 app models 中, 添加对 user model 的 one-to-one
    relation, 这样是解耦合的.

    理由: 1. 当多个 app 需要添加相似的 user model 关系, 若直接与 user model 建立
    关系, 则可能出现冲突, 因此降低了 app 的重用价值. 若与 app 自己的 user profile
    model 建立关系, 在由它统一与 user model建立关系, 则大大降低了冲突的可能.
    2. 假如需要途中替换 user model, 若统一通过 profile model 间接建立关联, 则
    每个 app 只需更新 profile model 与 user model 的关联; 若各 model 直接与 user
    model 关联, 则需要更新所有关联.

    注意 user profile model 不能用 concrete model inheritance 实现. user profile
    model 需要在 app 中与 user 进行关联. 在创建用户时, 同时创建各个 app 中的
    profile 部分. 两者是解耦合的. 在 concrete model inheritance 中, 子类就是包含
    父类内容的一个完整类, 而不单纯是 profile 部分. 创建子类实例会相应在父类表中
    创建相应部分. 这种抽象逻辑与 profile model 是不相符的. 并且子类实例与其父类
    的那个部分是强耦合的.

  * 若是属于用户本身, 甚至是用户认证相关的属性, 才应该放在 user model 中.

  然而这涉及到在创建 user model instance 时需要创建 one-to-one relation
  model instance. 尤其是调用 auth app 提供的各种 create_user, create_superuser
  之类的方法时需要自动创建关联表中的实例, 这样才能保持解耦合效果 (若不能自动
  创建, 而需要 override 用户创建方法加上 one-to-one field 的话, 则又耦合回来
  了). 做到自动创建, 需要使用 signal framework.

- Reusable apps shouldn’t implement a custom user model.
  If you need to store per user information in your app, use a ForeignKey
  or OneToOneField to ``settings.AUTH_USER_MODEL``.

- 由于 ``AUTH_USER_MODEL`` 不一定是 ``django.contrib.auth.models.User``,
  因此在某个 app 中使用 user model 时, 不能直接 import User 类, 而是要
  在 runtime 使用 ``get_user_model()`` 或者 import-time 使用
  ``settings.AUTH_USER_MODEL``. 例如,

  * 需要动态获取 user model 时, 一般使用 ``get_user_model()``.

  * model 定义中建立 user model 关系时, 使用 lazy binding, 即 AUTH_USER_MODEL.

  * 在 connect handler to signal 时, 若需要 filter user model, 使用 AUTH_USER_MODEL.

  ``get_user_model()`` 也可以在 import-time 使用.

  .. code:: python

    class ProfileUser(get_user_model()):
        pass

- django custom user model requirements

  * 对于 django builtin auth backends, user model 必须有某种 unique field
    可唯一识别用户. 对于 custom backends, 当然随意.

  * Your model must provide a way to address the user in a “short” and
    “long” form.

- ``AbstractBaseUser``, ``AbstractUser``:
  AbstractBaseUser provides the core implementation of a user model,
  including hashed passwords and tokenized password resets.
  If you want to rethink some of Django's assumptions about
  authentication, then AbstractBaseUser gives you the power to do so.
  If you're just adding things to the existing user (i.e. profile data
  with extra fields), then use AbstractUser because it's simpler and
  easier.

- 注意自定义的 user model 可能还需要搭配自定义的 user manager.

- 自定义的 user model 还需考虑 builtin auth form, 以及在 admin site 对
  user model 的额外要求.

- Change to custom user model mid-project. **HORRIBLE**.
  迁移步骤参考 https://code.djangoproject.com/ticket/25313#comment:2

  开发时,

    1. Create a custom user model identical to auth.User, call it User (so
       many-to-many tables keep the same name) and set
       `db_table='auth_user'` (so it uses the same table).

    2. ``settings.AUTH_USER_MODEL`` 设置为上述 model.

    3. 设置 user app 里所有 model 的 `db_table` 与数据库里表名字相同.
       重命名 user app 为 `accounts`. 修改所有相关 import 等引用.

    4. 删除所有 migrations.

    5. `./manage.py makemigrations app1 app2 app3 ...`

    6. 构建安装包.

  测试时 (测试库),

    1. 备份数据库.

    2. Truncate `django_migrations` table.

    3. 安装.

    4. `./manage.py migrate --fake`

  部署 (线上库),

    1. 备份数据库.

    2. Truncate `django_migrations` table.

    3. 安装.

    4. `./manage.py migrate --fake`

  最后一步,

    1. Unset `db_table`, make and apply this migration.

    2. 将所有对 `auth.User` 的直接引用转换为 `get_user_model()` 或
       `settings.AUTH_USER_MODEL`.

Permission and Authorization
----------------------------

- 每个 app 的每个 model 都默认存在 view, add, change, delete 四个权限. 这些权限
  是在 Model.Meta.default_permissions 定义的.

- 权限检查 ``User.has_perm(<app_label>."view|add|change|delete"_<model>)``

- 一个用户或一个组可以有任意个权限 (many-to-many). 组具有的权限用户自动具有.

Permission
^^^^^^^^^^
- auth package 提供的 Permission 对象一定是和某个 model 关联的 (通过
  ContentType). 这其实符合一般的权限限制要求.

- 创建 Permission object 需要配合合适的 ``ContentType``.

- 可以通过 ``Model.Meta.permissions`` 来创建与 model 直接相关的自定义权限.
  这些权限在 migration 的时候, 通过 django.contrib.auth 的 post_migrate
  signal hook 来创建.

- caching. ``ModelBackend`` 会在取到一个用户的权限信息后进行 cache. 若在
  一个 request-response cycle 中, 需要修改权限并立即进行验证, 最好从数据库
  重载这个用户. 若不是在一个请求中, 一般没事, 因每次 request object 都会
  初始化 User object (lazily).

- object-level permission.
  django 自身提供了 per-model permission 机制. 对于 per-object 权限, 在
  auth module 提供的 api 中已经提供 placeholder parameter ``obj``, 但默认的
  ModelBackend 没有使用. 若要 per-object permission 机制, 需要自己实现, 或者
  使用比如 django-guardian.

- 自定义权限. 通过 ``Model.Meta.permissions`` 设置.

- ``Permission`` model.

  fields.

  * name.

  * content_type.

  * codename.

Group
^^^^^

User 和 Group 是 many-to-many 的关系.

builtin Group model 并不能在一切需要组的情况下使用, 这个组概念仅适用于权限分配
相关用途 (那是因为 Group class 中定义了 permissions relation),
即用户归于组、组具有权限. 而不适用于资源分配, 即用户归于组、
组具有资源.

那样的组还是要单独写 (即 Group class 定义 resources relation) 或者使用
django-guardian.

- ``Group`` model.

  * name.

  * permissions.

Authentication
--------------
- 一个正经的 web app 不会存储用户的原始密码, 只会存储密码的 hash.
  因此, User instance 需要使用 ``set_password()``.

- 修改密码: 通过 ``./manage.py changepassword`` 和 ``User.set_password()``
  来修改密码.

- 在 project 中嵌入 django auth 功能的几种方式:

  * 直接全部使用默认配置, 在 project 的 root urlconf 中直接 include
    django.contrib.auth.urls. 只实现所需的 templates 即可.

  * 使用 auth 提供的各种 views, 或者 subclass 进行自定义. 绑定任意的
    urls.

  * 使用自定义的 view 和 urls 等, 在其中使用 auth 提供的 forms.

  * 以上 auth 提供的方便玩意儿都不使用, 只手动使用 ``authenticate()`` 和
    ``login()`` ``logout()`` 等.

authenticate & login/logout
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- authentication.

  ``authenticate()`` 提供认证检验. 若认证成功返回 User object, 否则 None.
  注意它只做检验 (返回相符的 User instance), 不改变状态. 它将 credentials
  传递给 auth backends, 真正的认证过程依靠各个 auth backends 实现.

  在认证时, 它依次尝试所有的 backend, 直到:

  * 第一个认证成功为止;

  * 或某个 raised ``PermissionDenied``;

  * 或遍历结束整个 list.

- login.

  * ``login()`` 在 ``authenticate()`` 的基础上, 改变认证状态, 并将认证相关信息
    保存在 session 中.

    未 login 时, ``request.user`` 是 ``AnonymousUser``, login 后成为 user
    instance. 两者的 ``is_authenticated`` attribute 的值分别是 False/True,
    可用于判断是否登录了.

    在登录时, 若本来有非匿名用户 session 信息, 会校验登录前后用户是否相同.
    若不相同, 则原有 session 会被 flush 掉. 若相同或原来是匿名用户, session
    会保留下来, 但 session key 即 session cookie 值会重新生成.

    最后, session 对应的用户 id, 认证使用的 backend 会保存在 session 中.

    由于对于一定的 session, 校验时使用的 auth backend 是存储在 session 中的.
    如果要更改 backends setting 以使用不同的 backend 来认证, 需要清空 session.

  * ``AuthenticationMiddleware`` 会根据 request 中的 session id 信息,
    匹配相应用户, 设置 ``request.user``. 从而避免每次请求都跳转至 login
    页面再次登录.

- logout.

  ``logout()`` 清空 session 信息, 重设 request.user 为 AnonymousUser.

- settings.

  ``settings.LOGIN_URL``, The URL where requests are redirected for login.
  default ``/accounts/login/``. 该值可以设置为 url pattern name.

  ``settings.LOGIN_REDIRECT_URL``, 登录后的默认跳转路径.

  ``settings.LOGOUT_REDIRECT_URL``, 登出后的默认跳转路径.

authentication views
^^^^^^^^^^^^^^^^^^^^
auth views 不提供默认的 templates, 需要自己写模板.

若不想直接使用默认的 auth.urls 设置, 可单独使用 views 以对参数进行自定义,
以及 bind to custom urls.

- ``LoginView``, for login.

  配置项.

  * template_name. default: ``registration/login.html``.

  * redirect_field_name. default: ``next``.

  * authentication_form. default: ``AuthenticationForm``.

  * extra_context.

  * redirect_authenticated_user. 对于已经登录的用户, 访问 login view 时
    是否自动 redirect 至 next url.

  * success_url_allowed_hosts.

  context variables.

  * form.

  * next.

  * site.

  * site_name.

- logout: ``LogoutView``.

  配置项.

  * next_page. 用于登出后的 redirect. default ``settings.LOGOUT_REDIRECT_URL``.

  * template_name. 登出后显示的页面内容. default ``registration/logged_out.html``.

  * redirect_field_name. default next.

  * extra_context.

  * success_url_allowed_hosts.

  这些参数的逻辑是, 若希望登出后 redirect 至某个 url, 则设置 next_page.
  当 logout 请求的 url query string 存在 redirect_field_name 时, 会
  redirect 至它指向的 url, override next_page 的配置.
  若希望登出后显示一个某种已登出之类状态页面, 不设置 next_page, 设置
  template_name.

  context variables.

  * title.

  * site.

  * site_name.

- logout then redirect to login: ``logout_then_login()``.
  只是一个 shortcut to LogoutView.

- password change: ``PasswordChangeView``.
  这些 view 会在更新密码后再更新 session 中的 auth hash, 所以它们不会因为
  修改密码而登出用户.

  配置.

  * template_name. default ``registration/password_change_form.html``.

  * success_url. default ``password_change_done``.

  * form_class. default ``PasswordChangeForm``.

  * extra_context.

  密码修改成功后默认 redirect 至 password_change_done.

- password change done: ``PasswordChangeDoneView``.

  配置.

  * template_name. default ``registration/password_change_done.html``.

- password reset: ``PasswordResetView``.

  配置:

  * template_name. default ``registration/password_reset_form.html``

  * form_class. Form that input email. default ``PasswordResetForm``

  * email_template_name. reset email template.
    default ``registration/password_reset_email.html``

  * subject_template_name. template for email subject.
    default ``registration/password_reset_subject.txt``

  * token_generator. default:
    ``django.contrib.auth.tokens.PasswordResetTokenGenerator``.

  * success_url. default: password_reset_done.

  * from_email. default: settings.DEFAULT_FROM_EMAIL.

  * html_email_template_name. html 邮件模板. 默认不使用.

  * extra_context.

  * extra_email_context.

  email template context.

  * email.

  * user.

  * site_name.

  * domain.

  * protocol. https or http.

  * uid. user's pk in base64.

  * token.

  密码重置流程:

  * 发起重置: 用户输入注册邮箱, 确认重置密码, 生成一次性密码重置链接,
    发送至用户邮箱 (若邮箱不存在, 不会报错, 但也不会发送邮件, 这样避免泄露
    注册情况).

    Users flagged with an unusable password aren’t allowed to request a
    password reset to prevent misuse when using an external authentication
    source like LDAP.

  * 发起重置完成: 邮件发送后显示邮件发送成功页面.

  * 确认重置: 用户从自己的邮箱中点击重置链接, 后端验证后 redirect 至填入新密码
    的 form url, 进行重置.

  * 重置完成: 提示重置完成.

- password reset done: ``PasswordResetDoneView``.
  密码重置请求已经发出后显示的页面.

  配置.

  * template_name. default: ``registration/password_reset_done.html``.

  * extra_context.

- password reset confirm: ``PasswordResetConfirmView``.
  点击邮件中的密码重置链接后显示的密码重置页面.

  Store the token in the session and redirect to the
  password reset form at a URL without the token. That
  avoids the possibility of leaking the token in the
  HTTP Referer header.

  url kwargs:

  * uidb64.

  * token.

  配置.

  * template_name. default: ``registration/password_reset_confirm.html``

  * token_generator.

  * post_reset_login. 重置后是否自动登录.

  * post_reset_login_backend.

  * form_class. default: SetPasswordForm.

  * success_url. default: password_reset_complete.

  * extra_context.

  template context.

  * form.

  * validlink.

- password reset complete: ``PasswordResetCompleteView``.
  重置密码后提示成功的页面.

  配置.

  * template_name. default: ``registration/password_reset_complete.html``.

  * extra_context.

- view helper: ``redirect_to_login()``.

authentication forms
^^^^^^^^^^^^^^^^^^^^

若不想使用 auth views, 可单独使用 auth forms.

* ``AuthenticationForm``.
  注意它会拒绝 inactive user.

* ``PasswordChangeForm``

* ``PasswordResetForm``
  ``.save()`` method 并不修改任何状态, 而是调用 ``.send_mail()`` 发送重置邮件.

* ``SetPasswordForm``
  form to set new password without entering old password.

* ``UserChangeForm``
  used in admin site.

* ``UserCreationForm``

* ``AdminPasswordChangeForm``
  used in admin site.

urls
^^^^

- ``auth.urls`` 提供了完整的 auth urls 和 view 实现. 这些 url 是没有
  namespace 的. 在使用时可以直接放在 url root path 上, 或者 ``include()``
  中设置 namespace.

authentication signals
^^^^^^^^^^^^^^^^^^^^^^

- ``user_logged_in``

  args.

  * sender.

  kwargs.

  * request.

  * user.

- ``user_logged_out``, params ditto.

- ``user_login_failed``.

  args.

  * sender.

  kwargs.

  * credentials.

  * request.

authorization and authentication backends
-----------------------------------------
``auth`` app 中的各种上层认证和授权操作实际上要转发给底层 backend 去操作.
不同类型的 backend 的实现不同, 但符合相同的 api, 供上层调用.

- ``AUTHENTICATION_BACKENDS`` 配置 backend list. 很多 auth 相关操作遍历该 list.
  若在使用外部认证机制认证的同时, 还要使用 django 默认的认证和权限系统,
  则在这个列表中包含某个外部认证 backend + ModelBackend 作为 fallback.

- 结合使用外部的 auth backend 时, 仍然需要根据 ``AUTH_USER_MODEL`` 对每个
  用户创建系统账户. 因为从逻辑上讲, 这些 user objects 才是这个系统 (django)
  自己的用户. 外部 auth backend 只是提供了一系列用户实体集合. user model
  才是这个系统所需的 user 所具有的属性和功能的表征. 从实现上讲, 没有 user
  model 什么也没法弄, 没有用户概念的实体寄托.

- ``ModelBackend`` 和 ``RemoteUserBackend`` 不允许 inactive user 认证.
  ``AllowAllUsersModelBackend`` 和 ``AllowAllUsersRemoteUserBackend``
  允许 inactive user 认证.

- General interface of auth backend.

  Required:

  * ``get_user(user_id)``. takes a user_id – which could be a username, database ID or
    whatever, but has to be the primary key of your user object – and returns a
    user object. If the specified user can not be retrieved according to backend's
    knowledge or its policy (e.g. user's inactive), returns None.

  * ``authenticate(request, ...)``. takes a request argument and credentials as
    keyword arguments, return a user object that matches those credentials if
    the credentials are valid. If they’re not valid, it should return None.

  Optional: 权限类方法. 在 AbstractUser 上调用这些方法时, 会 delegate 至各个
  定义了这些方法的 backend 去执行. 即遍历 AUTHENTICATION_BACKENDS 检查是否定义了
  所需的方法.

  各个 backend 给出的权限的并集是用户的相应部分权限.

  * ``get_group_permissions()``

  * ``get_all_permissions()``
    
  * ``has_perm()``

  * ``has_module_perms()``

ModelBackend
^^^^^^^^^^^^
默认的 auth backend. 通过 USERNAME_FIELD/password 进行认证.

ModelBackend 会将取到的用户权限 cache 在 user instance 上. 对于组权限和用户权限
分别是 ``_group_perm_cache`` & ``_user_perm_cache``.

Inactive users are rejected.

API.

* 获取用户实体.

  - ``.get_user(<pk>)``
    该操作由 ``auth.get_user()`` 调用. 后者根据 session 中存储的 user id 以及
    auth backend 调用正确的 ``.get_user()`` method. 获取用户实体.

* 认证.

  - ``.authenticate(...)`` return user object or None.

  - ``.user_can_authenticate()``

* 权限.

  - ``.get_user_permissions()``

  - ``.get_group_permissions()``

  - ``.get_all_permissions()``

  - ``.has_perm(...)``

  - ``.has_module_perms()``

  没有实现 object-level permission, 即当传入 ``obj`` instance 时, 总是返回
  空权限集 ``set()`` 或者 False.

AllowAllUsersModelBackend
^^^^^^^^^^^^^^^^^^^^^^^^^
允许 inactive user 认证. 但仍然没有任何权限.

这是 ModelBackend 的子类.

RemoteUserBackend
^^^^^^^^^^^^^^^^^
通过外部认证机制进行自动的用户认证和创建. 这用于与 LDAP 等统一认证机制结合使用.
需要认证的用户名通过 ``REMOTE_USER`` header 传递至 django.

这是 ModelBackend 的子类. 因此包含上述的 API.

inactive users are rejected.

attributes.

- ``create_unknown_user``. 是否自动创建 django 数据库中不存在的用户.

methods.

- ``authenticate()``. 实际上无需认证, 因为是外部认证. 所以这里对传入的用户直接
  就认为是 authenticated. 若用户不存在则创建, 否则直接获取并返回.

- ``clean_username()``. 在认证前, 将 REMOTE_USER clean 成所需的格式.

- ``configure_user()``. 对于新创建的用户, 进行配置.

AllowAllUsersRemoteUserBackend
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
允许 inactive user 认证. 但仍然没有任何权限.

这是 RemoteUserBackend 的子类.

middlewares
-----------

AuthenticationMiddleware
^^^^^^^^^^^^^^^^^^^^^^^^

根据 request 中 cookie 保存的 session 信息进行自动的用户识别和认证, 避免每次访问
都要登录.

调用 ``auth.get_user()`` 操作, 后者从 session 中获取到 user id 之后, 还会校验
存储的 session auth hash 与从 user instance 中计算得到的是否一致. 若不一致,
则 flush session, 设置 AnonymousUser. 对于 AbstractBaseUser, 效果是在修改密码
后会自动登出用户, 要求 重新登录.

若认证成功返回 user instance, 否则返回 AnonymousUser.
无论认证的结果是什么用户, 都保存在 ``request.user`` 上.

RemoteUserMiddleware
^^^^^^^^^^^^^^^^^^^^
在 AuthenticationMiddleware 的基础上, 进行检查和认证.
所以是在 ``settings.MIDDLEWARE`` 中, AuthenticationMiddleware 后面添加
这个 middleware.

经过 AuthenticationMiddleware 之后, 若用户本来是认证的, session 中保存的
用户已经赋值给了 ``request.user``, 则这里检查用户名与 REMOTE_USER 是否
相同. 若用户本来是未认证的, 则使用 RemoteUserBackend 认证和登录用户.

注意这个 middleware 默认要求 REMOTE_USER 在每个请求中都有. 这只适用于
HTTP Basic Auth 之类的简单认证. 若只希望在 login 等页面进行远程认证, 之后
就通过 session, 则使用 PersistentRemoteUserMiddleware.

attributes.

- header. 包含 remote username 的 header.

- force_logout_if_no_header. 没有 header 时, 是否 logout user.

PersistentRemoteUserMiddleware
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

没有 header 时也不 logout user. 它是 RemoteUserMiddleware 的子类.

Useful for setups when the external authentication via ``REMOTE_USER`` is only
expected to happen on some "logon" URL and the rest of the application wants to
use Django's authentication mechanism.

view mixins & decorators
------------------------
以下 decorators and mixins 提供在各个 app 的 view 中提供用户认证和权限管理.

decorators
^^^^^^^^^^

- ``login_required``.

  * ``redirect_field_name`` 默认是 next, 为了让登录后再次跳转至 next 的 url,
    相应的 login view 中需要使用 next 值再次跳转.

  * ``login_url``.

- ``permission_required``, 检查用户是否有权限.

  * ``perm``. 单个的或 a list of permissions.

  * ``login_url``.

  * ``raise_exception`` 是否直接 raise PermissionDenied, 不然就跳转登录.

- ``user_passes_test``, 通用的用户认证和权限类条件判断. 注意它的应用场景仍然是
  认证和权限范围. 这是它的设计目的: 条件检查失败后跳转至 login url 或 raise 403.
  所以不能说所有条件判断时都可以使用.

mixins
^^^^^^
``AccessMixin`` 共同父类. AccessMixin 不会 override ``.dispatch()`` method.
由于它提供了一系列参数和 ``handle_no_permission`` 方法, 除了可以作为以下的
共同父类之外, 还可以作为比较一般化的 mixin class, 在 view 中按需求使用它提供
的方法.

class attribute.

* login_url.

* permission_denied_message.

* raise_exception.

* redirect_field_name.

以下 mixin class 都会 override ``View.dispatch()`` method, 因此需要保证在
MRO 的最左边. 此外, 由于它们直接 override ``dispatch()``, 因此无论 request
method 是什么都会生效. 不如相应的 decorator 灵活.

- ``LoginRequiredMixin``

- ``PermissionRequiredMixin``

  class attribute.

  * permission_required.

- ``UserPassesTestMixin``

  methods.

  * ``test_func()``. 要进行的检查.

若要求对未登录用户和已登录却权限不足的用户分别做不同的处理, 则不能同时使用
LoginRequiredMixin 和 PermissionRequiredMixin, 因为它们使用同一个
``AccessMixin.handle_no_permission()``. 此时, 需要使用一个 decorator 形式配合一
个 Mixin 形式, 或者两个 decorator 形式, 才能设置不同的处理方式.

context processors
------------------

django.contrib.auth.context_processors.auth
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

为 template context 自动添加一系列用户、权限相关量.

- ``user``, 当前用户.

- ``perms``, 当前用户的权限.

  * ``perms.<app_label>`` 相当于 ``User.has_module_perms(<app_label>)``.

  * ``perms.<app_label>.<perm>`` 相当于 ``User.has_perm(<app_label>.<perm>)``

  * ``perms`` 支持使用 ``in`` operator 检查权限, ``<app_label> in perms`` 或
    ``<app_label>.<perm> in perms`` 都可以.

helpers
-------

- ``update_session_auth_hash()``.

token generator
---------------

django.contrib.auth.tokens.PasswordResetTokenGenerator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
必要特性.

- 安全性. 合法的 token 依赖于用户当前密码的 hash 和服务器配置的 secret key,
  所以具有安全性.

- 唯一性. 生成的 token 依赖于当前密码 hash, 用户上次登录时间和当前服务器时间.
  所以每次重置成功 token 后新生成的 token 都会变化.

- 时效性. token 包含生成时间. 若 token 已经过期, 则验证失败.

配置.

- settings.SECRET_KEY.

- settings.PASSWORD_RESET_TIMEOUT_DAYS.

password management
-------------------

加密后的密码存储格式: ``<algorithm>$<iterations>$<salt>$<hash>``

默认的算法: PBKDF2 with SHA256 hash.
Recommended by NIST, sufficient for most uses.

password hashing
^^^^^^^^^^^^^^^^

- ``PASSWORD_HASHERS``. a list of supported hashing algorithms.
  第一项用于加密密码. 其他所有项 (包含第一项) 都可用于检验密码.

- PBKDF2, Argon2, Bcrypt, SHA1, MD5, Crypt.

- iterations. subclass hasher class and override ``iterations`` attribute.

A set of functions to create and validate hashed password. Can be used
independently from the User model.

- ``check_password()``

- ``make_password()``

- ``is_password_usable()``

password upgrading
^^^^^^^^^^^^^^^^^^
使用 django 默认的认证机制 ModelBackend 时, 在用户在登录认证时, 若存储的密码的
hash 算法、iterations 等参数与 PASSWORD_HASHERS 配置的不同时,
``user.check_password()`` 会根据当前配置自动更新密码.

This means that old installs of Django will get automatically more secure as
users log in, and it also means that you can switch to new (and better) storage
algorithms as they get invented.

Django can only upgrade passwords that use algorithms mentioned in
PASSWORD_HASHERS, so as you upgrade to new systems you should make sure never
to remove entries from this list.

password strength validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By default, validators are used in the forms to reset or change passwords and
in the ``createsuperuser`` and ``changepassword`` management commands. Validators
aren’t applied at the model level.

配置.

- ``AUTH_PASSWORD_VALIDATORS``. a list of validator config dicts.
  Each of which contains a ``NAME`` and optionally ``OPTIONS`` dict.
  ``NAME`` is import path of validator class; ``OPTIONS`` is kwargs
  to initialize validator instance.

builtin strength validators.

- ``UserAttributeSimilarityValidator``

- ``MinimumLengthValidator``

- ``CommonPasswordValidator``

- ``NumericPasswordValidator``

A set of functions to validate password.

- ``validate_password()``

- ``password_changed()``. Informs all validators that the password has been
  changed. This can be used by validators such as one that prevents password
  reuse. This should be called once the password has been successfully changed.

- ``password_validators_help_texts()``. 用于提供全部密码要求.

- ``password_validators_help_text_html()``. ditto in html.

- ``get_password_validators()``

Password validator API.

- ``validate()``

- ``get_help_text()``

- ``password_changed()``. optional.

about testing
-------------
- 在使用 factory boy 创建 fake user 时, 需要处理 raw password 至
  hashed password 的转换. 如果密码是 random password, 还需要保存
  生成的随机密码至 user instance 上. See `snippets/user_factories.py`


middleware
==========

overview
--------
- middleware 是在 request/response cycle 中, server 和 views 之间的一系列
  中间操作 (hooks). middleware 的作用是 pre-process request 以及 post-process
  response.

- 整个 middleware 体系可类比为一层套一层的同心环, 第一个 middleware 在最外层,
  views 在圆心. 当外部 call 一个 middleware 并传入 request 时, 这个 middleware
  负责调用它内层的 middleware/view, 后者再重复进行这个调用链, 完成 request
  从外部一层层经过所有 middleware 以及 view 的过程. 反向地, response 也进行类似
  的过程.

define middleware
-----------------
- middleware 通过 middleware factory 定义. 调用它时返回一个 middleware
  callable. 这个 callable 接受 request 参数, 返回相应的 response.

- middleware factory 可以是一个 function, 也可以是 middleware class.
  它的参数是 ``get_response()`` callable, 即它内层的 middleware.
  它给出的 middleware 可以是一个 function, 也可以是一个 callable instance of
  middleware class.

- class-based middleware 专有的 other hooks

  * ``process_view()``, 在 request pass-through 完成, 即经过所有 middleware 到达
    view 时, 在 call view function 之前, 会依次调用所有 middleware 的
    ``process_view()`` hook. 这个 hook 返回 None or HttpResponse. 若是 None,
    则执行下一个 ``process_view()`` 直至 view function; 若是 HttpResponse,
    则直接进入 response pass-through 流程, 即经过各 middleware 反向向外走.

  * ``process_exception()``, Django calls process_exception() when a view
    raises an exception. process_exception() should return either None or an
    HttpResponse object. If it returns an HttpResponse object, the template
    response and response middleware will be applied. Otherwise, default
    exception handling kicks in.

  * ``process_template_response()``, called just after the view has finished
    executing, if the response instance has a render() method. It must return
    a response object that implements a render method. It could alter the
    given response by changing response.template_name and response.context_data,
    or it could create and return a brand-new TemplateResponse or equivalent.

  * Django automatically converts exceptions raised by the view or by
    middleware into an appropriate HTTP response with an error status code.
    This conversion takes place before and after each middleware.

use middleware
--------------
- ``settings.MIDDLEWARE`` 定义启用的 middlewares. The order in settings.MIDDLEWARE
  matters because a middleware can depend on other middleware.

- 在进程的生命周期中, 各个 middleware 只生成一次, 对每个 request 重用.

- 在 request/response cycle 中, middleware/view 的执行流程.

  1. request pass-through 阶段, request 正向经过各个 middleware, 若在任何一个
     middleware 中 return HttpResponse, 则开始反向向外走.

  2. 经过所有 middleware 之后, 进入 view 处理阶段.

     2a. 正向应用所有 middleware 的 ``process_view()``, 它们返回 None 或 HttpResponse.
         若其中任一个给出 HttpResponse, 直接开始 response pass-through.

     2b. 执行 view function. 若执行过程中 raised exception, 反向执行各个 middleware
         的 ``process_exception()``. 若 view function 返回的不是 HttpResponse, raise
         exception.

     2c. 若 HttpResponse 有 ``.render()`` method, 反向执行各个 middleware 的
         ``process_template_response()``. 它必须返回带有 ``.render()`` 的
         HttpResponse. 都执行完成后 render response, 若 render 时 raised exception,
         再次反向执行各个 middleware 的 ``process_exception()``.

  3. response pass-through 阶段, response 反向经过各个 middleware.

  NB: 在任何一个 middleware/view 中 raised exception 会被转换成 HttpResponse
      再传递回上层 middleware.
      在 process_exception 处理时, 若任一返回 HttpResponse 则继续下面的步骤;
      若全部都返回 None, 则 re-raise exception.

messages framework
==================

* 提供 cookie- and session-based 临时信息. 这些信息 (或信息的标识) 经常是在
  本次 view 处理中设置, 在下次 (可能不同的) view 处理中使用. (通过 302
  redirect response 传至 client, 再次请求时传回 server.) 这些信息也可能是在
  本次 view 中使用.

* ``django.contrib.messages`` 默认就有运行. 它提供 ``MessageMiddleware``, 并
  依赖于 SessionMiddleware (messages 部分功能依赖 session 生效), 以及
  ``messages`` context processor.

storage backend
---------------
``settings.MESSAGE_STORAGE`` 默认使用 FallbackStorage.

base: ``django.contrib.messages.storage.base.BaseStorage``.
所有子类实现 ``_get()``, ``_store()`` methods.

每种存储信息的方式对应一个 backend.

- ``django.contrib.messages.storage.session.SessionStorage``
  在 session backend 中存储, 位于 session cookie key 所指向的条目内.

- ``django.contrib.messages.storage.cookie.CookieStorage``
  在 cookie 中存储 (从而在 client/server 间传递). 同时还包含一个
  message 的 signed hash, 使用 server 的一个 secret key 签署.
  避免篡改.

  cookie 相对于 session 的好处是性能. 因为不涉及存入 backend.

- ``django.contrib.messages.storage.fallback.FallbackStorage``
  首先使用 cookie, 对于 cookie 放不下的, 存在 session 里.

message
-------
- ``django.contrib.messages.storage.base.Message``

message level
-------------
- message levels: DEBUG, INFO, SUCCESS, WARNING, ERROR.
  ``settings.MESSAGE_LEVEL`` 设置最低接受添加的 message 的 level.

- 每个 message level 有对应的 lowercased version message tag.

APIs
----

- ``add_message()``. shortcuts: ``debug|info|success|warning|error()``.

- ``get_messages()``, 在代码中直接使用或模板 context variable ``messages``
  间接使用.

- ``set_level()``, 直接修改 message storage 的最低保存 level, 从而可以
  设置 per request level.

- ``get_level()``

逻辑
----

每次请求, middleware 实例化 message storage, 赋值给 ``request._messages``.
在 view 中, 使用 ``add_message()`` 添加 message, 标记为 queued messages.
在代码或模板中遍历 message storage 时, 会标记该 storage 已经被使用过,
清空 queued messages. middleware 处理响应时, 会将往次设置但没有使用过的
以及新添加的 messages 保存起来, 附在响应中.

手动设置 ``BaseStorage.used=False`` 可避免遍历过的 message storage 被
清空. 下次仍可使用.

view mixin
----------
提供了一个 view class mixin 用于添加 success message. 其实这也是 message
的最常见用处.

``django.contrib.messages.views.SuccessMessageMixin``
这需要配合 ``FormMixin`` 使用. ``success_message`` attr 设置信息 format
string.

signal
======

builtin signals
---------------

* before/after ``Model.save()`` is called:

  - ``django.db.models.signals.pre_save``

  - ``django.db.models.signals.post_save``

* before/after ``Model.delete()`` or ``QuerySet.delete()`` is called:

  - ``django.db.models.signals.pre_delete``

  - ``django.db.models.signals.post_delete``

* starts/finishes http request.

  - ``django.core.signals.request_started``

  - ``django.core.signals.request_finished``

定义 receiver function
----------------------

- args: ``sender``.

- kwargs: receiver function 必须接受任意数目的 kwargs, 即必须 ``**kwargs``.

注册 receiver function
----------------------

两种方式.

- ``Signal.connect()``.

  * ``weak=True``. Signals handlers are stored by default as weak references.

    这是考虑到使用一个 local object 的 method 作为 signal handler 时, 希望当
    object 的 scope 结束后, object 能够被正常 gc (handler 也自动消失).

    see also: [SODjSignalWeakRef]_.

- ``django.dispatch.receiver()`` decorator.

``INSTALLED_APPS`` 的顺序会影响 signal handlers 的加载顺序, 从而影响触发
事件时, signal handler 的执行顺序. 当 signal handler 之间存在依赖关系时,
需要注意这一点.

signal 相关代码应该放在哪
-------------------------

- signal receiver 定义放在 ``<app>/signals.py``.

- 注册操作放在 app 的 configuration class (``<app>/apps.py:AppConfig``)
  ``.ready()`` method 中. 若定义时使用了 receiver decorator, 在这里
  只需 import 即可.

  注意 ``AppConfig.ready()`` 可能在测试时被执行多次, 为避免 signal
  duplication, 要通过 ``dispatch_uid`` 保证注册过则不再注册.

定义 custom signal
------------------

实例化 Signal 或它的子类 (例如 ModelSignal).

``Signal`` object.

- ``.connect()``, register a consumer function for this signal.
  指定 ``sender=`` 来过滤 signal 的来源, ``dispatch_uid=`` 指定
  receiver 的唯一标识, 避免某些情况下的重复注册.

  指定 ``dispatch_uid`` 后, receiver 的注册标识将不再依赖于 receiver
  function 的 id 即内存地址.

- ``.send()``, 发送信号, 调用所有注册的 receiver functions.
  调用过程是在本线程中依次执行的. 若某个 receiver function 在执行过程
  raise exception, send 不会 catch, 这导致 send 过程被中断, 不能保证
  所有 receiver 都收到该信号 (即被调用).

- ``.send_robust()``, catch exception raised by receiver function.
  从而保证所有 receiver 都调用一遍.

- ``.disconnect()`` unregister receiver function.

the contenttypes framework
==========================

``django.contrib.contenttypes.models.ContentType`` 保存了一个 django project
中的所有 models 的唯一识别 (app_label + model), 并提供了一系列 contenttypes
和 model class 相互转换, generic relation 等功能.

当在项目数据库中创建新的 model 时, 相应的 contenttypes 也自动创建. 这是通过在
``AppConfig.ready()`` 中注册 pre_migrate/post_migrate signals 来实现的.

ContentType 的用途.

- 在需要对不确定的多个 model 数据进行相似逻辑的 CRUD 操作时, 使用 contenttypes
  进行通用化. (``apps.get_model`` 也可以.)

- 如果需要设置某个 model field 它的值是其他的 model, 即这个列的数据是 model class
  时, 需要设置 foreign key 至 ContentType. 因后者保存着 model class 数据.
  ``django.contrib.auth.models.Permission`` 就是这样做的.

GenericForeignKey, GenericRelation 的用途.

- 当一个 table 需要关联的外键是来自不同的 table 的, 抽象地将, 一个 model 的实例
  可能需要关联不同 model class 的实例时. 可以使用 GenericForeignKey 做到.
  本质上是在这个 model 每个 entry 中保存了该 entry 关联的 contenttype (即 model)
  以及关联该 model 中的 entry 的 primary key.

  例如, 不同类型的对象比如 blog entry, picture, 等需要关联相同类型的 comment.

- 注意 GenericForeignKey 由于只是与之关联的 content_type, object_id 两个列的抽象,
  在 migration 过程中, ``apps.get_model()`` 构建的 model 不包含 GenericForeignKey,
  只能直接设置两个实际列的值.

CSRF protection
===============

原理与操作逻辑
--------------
1. CSRF token 是随机生成的. Possibly based on urandom.
   csrf token 由 salt + secret 构成.

   (token 本身已经很安全, 第三方站点不能访问. 加上 salt 是为了提高对
   side-channel attack 的防范.)

2. 后端设置 csrf token cookie (或者它在 DOM 中的等价形式), 它随响应到达
   user agent.

   * 在 cookie 中的 csrf token 维持一个 anonymous 或 login session 不变. 
     在每次 login 时由 ``auth.login()`` 执行 ``rotate_token()``, 此时
     salt 和 secret 都改变. (csrf token cookie 本身的 max age 由配置控制.)
   
   * 在 DOM 中由 ``csrf_token`` context variable 生成的 csrf token 每次
     调用都变化. 但是 salt 变化, secret 不改变.

   * 后端在何时首次设置 csrf token cookie: 当用户登录时; 当访问的页面中存在 form
     等需要设置 csrf token DOM element 时; 当某个 view 要求设置 csrf token cookie 
     时, 例如通过 ``ensure_csrf_cookie`` decorator, 或者手动调用 ``get_token()``.

     所以对于 anonymous user, 当他需要进行任何 post 操作时的复杂性, 其实
     从另一个角度说明了应该避免 anonymous user 做状态修改. 而是要先登录.
     这也是避免了恶意操作.

3. 前端在提交 POST (form or ajax) 时将 csrf token 设置在 request header
   中 (或者包含在 form data 中, 这都是第三方无法复制的方式). 这样在
   请求中, 存在两份 token, 一份在 cookie 中, 一份在 header 中 (或 form 中).

4. CsrfViewMiddleware 校验 secret 部分是否相等, 不管 salt 部分.
   若校验失败, 则返回 403 Forbidden.

5. 额外: 在 https 下还会检查 referer header, 只允许同一个 domain 或只允许指定的
   subdomain 向该 domain 发起 POST. 这是避免 subdomain owned by untrusted user.

use CSRF token during POST
--------------------------
任何种类的 POST 修改服务器状态时, 都要实现 CSRF protection.

form post
^^^^^^^^^
添加 ``csrf_token`` form input. 作为 form data 的一部分 POST 至服务端.

ajax post
^^^^^^^^^
添加 ``X-CSRFToken`` header. 随 body 一起 POST 至服务端.

- 若 csrf token 存储在 cookie 中: 访问 ``CSRF_COOKIE_NAME`` cookie
  获取 token value.

- 若 csrf token 存储在 session 中: 需要在模板中 render token 或者手动
  加入 cookie, 不然前端看不见 token. 我认为 csrf token 存在 session 中
  这种方式是无意义的, 因为最终都必须要靠某种方式传递到前端来. 不如只放在
  cookie 中就可以了. 安全性方面 cookie 也没什么问题.

middlewares
-----------
- ``django.middleware.csrf.CsrfViewMiddleware``.
  Should come before any view middleware that assume that CSRF attacks have
  been dealt with.

  该 middleware 的主要逻辑在 ``process_view()`` 中执行. 这样可以与各种 csrf
  decorators 配合使用. 因为 ``process_view()`` 的输入之一就是 view callable,
  所以可以根据 ``csrf_exempt`` 等的作用进行不同操作.

decorators
----------
- ``csrf_protect``. 强制保护特定的 view. 除了一般的用法之外, 对于 reusable app,
  这可用于强制一些 view 进行 csrf 校验, 而无论所在的 project 是否开启 csrf.

- ``csrf_exempt``. 强制不检查 csrf.

- ``ensure_csrf_cookie``. 强制 view 设置 csrf token cookie.

- ``requires_csrf_token``.

context processors
------------------
- ``django.template.context_processors.csrf``.
  提供 ``csrf_token`` context variable, 这个 context processor 是默认就有的,
  并且是强制添加的. 无需在 template backend settings 中设置.

template rendering
------------------
* ``csrf_token`` context variable.

* ``{% csrf_token %}`` tag. 根据 ``csrf_token`` context variable 生成
  hidden input element, ``name=csrfmiddlewaretoken``.

settings
--------
- ``CSRF_USE_SESSIONS``

- ``CSRF_COOKIE_NAME``

- ``CSRF_COOKIE_AGE``

- ``CSRF_COOKIE_HTTPONLY``
  Designating the CSRF cookie as HttpOnly doesn’t offer any practical
  protection because CSRF is only to protect against cross-domain attacks. If
  an attacker can read the cookie via JavaScript, they’re already on the same
  domain as far as the browser knows, so they can do anything they like anyway.
  (XSS is a much bigger hole than CSRF.)

- ``CSRF_COOKIE_DOMAIN``

- ``CSRF_COOKIE_PATH``

- ``CSRF_COOKIE_SECURE``. 使用 secure cookies.

- ``CSRF_HEADER_NAME``

- ``CSRF_FAILURE_VIEW``

- ``CSRF_TRUSTED_ORIGINS``

Clickjacking Protection
=======================

middleware
----------
- ``django.middleware.clickjacking.XFrameOptionsMiddleware``
  当 ``X-Frame-Options`` header 没有已经设置的时候, 给所有 response 添加
  这个 header. 取 ``settings.X_FRAME_OPTIONS`` 的值.

decorators
----------
- xframe_options_deny. 设置 DENY. set the header on per-view-basis.

- xframe_options_sameorigin. 设置 SAMEORIGIN. set the header on per-view-basis.

- xframe_options_exempt. 避免 middleware 设置这个 header.

settings
--------

- ``settings.X_FRAME_OPTIONS``. 默认是 SAMEORIGIN.

Pagination
==========

- 若 pagination 是由前端 js library 去实现 (例如 datatables), 只传递给后端所需
  页的第一个记录的 id 以及记录数目, 则没必要在 view 中使用纯后端的 paginator.
  只需返回前端任何它需要的数据即可.

Serialization
=============


JSON
----

- 注意 Serializer/Deserializer API 与 JSON encoder/decoder 是不同层的结构. 前者
  是对于各种数据格式通用的 django-specific 的封装. 后者只是对 JSON 的 encoder
  decoder API 的扩展. 对于 JSON format, 两者的关系是 django serialization API
  通过 DjangoJSONEncoder 来实现.

- DjangoJSONEncoder 在 ``json.JSONEncoder`` 基础上, 额外支持:

  * datetime.datetime. 在 serialization 时,
    
    - 采用 iso format.
      
    - 若包含 microseconds, 只保留前 3 位.

    - 若包含时区 offset 部分, 保留. 若 offset 为 ``+00:00``, 转换成 ``Z``.

  * datetime.date,
    
  * datetime.time,
    
  * datetime.timedelta,
  
  * decimal.Decimal,
    
  * django.utils.functional.Promise,
    
  * uuid.UUID.

management commands
-------------------

dumpdata
^^^^^^^^
::

  ./manage.py dumpdata [<app_label>[.ModelName]]...

- Dump data of the specified apps/models, or of all installed apps.

- ``--all``. By default, dumpdata uses the default manager on each model to
  select records to dump. Use this option to use base manager, which presumably
  does not do default filtering.

- ``--format``. Serialization format. Default JSON format.

- ``--indent``. Serialization format's indent option.

- ``--exclude``. exclude app or model. can be specified multiple times.

loaddata
^^^^^^^^

Security, SSL & HTTPS
=====================
- 很多 SSL 相关的检查和操作最好在前端服务器而不是在上游 django 处理.

- csrf, session cookies 等使用 secure cookies.

- 在前端服务器上使用 HSTS.

- Make sure that your Python code is outside of the Web server’s root.

middleware
----------
- ``django.middleware.security.SecurityMiddleware``. 默认有使用.

settings
--------
- SECURE_PROXY_SSL_HEADER. 当 django 应用作为上游服务器时, 前端服务器与 django
  通信时一般采用 http. https 止于前端服务器部分. 所以 scheme 永远是 http.
  默认配置情况下, 此时 ``request.is_secure()`` 是 False. 为了检验客户端与
  服务端通信是否 https, 可以前端服务器需要在转发时设置额外的 header 以示说明.
  django 会根据这个配置去给出 ``is_secure()`` 的结果.

- SECURE_SSL_REDIRECT, SECURE_REDIRECT_EXEMPT, SECURE_SSL_HOST. 不要使用.
  要在前端服务器配置. 这样所有资源都有统一的 https 处理. 事实上, 在作为
  上游服务器时, 若 ALLOWED_HOSTS 限制只允许本地访问, 在 django 中配置的
  redirect 根本不会成功.

- SECURE_HSTS_SECONDS, SECURE_HSTS_INCLUDE_SUBDOMAINS, SECURE_HSTS_PRELOAD.
  HSTS 配置. 不要使用. 要在前端服务器配置.

- SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE. secure cookies.

- SECURE_BROWSER_XSS_FILTER. 不要使用, 在前端服务器设置 ``X-XSS-Protection``.

- SECURE_CONTENT_TYPE_NOSNIFF. 不要使用, 在前端服务器设置 ``X-Content-Type-Options``.

- ALLOWED_HOSTS. 限制 Host header 值.

Logging
=======
- django uses ``logging`` module.
  logging configs 使用 dict config 方式加载.

settings
--------
- ``settings.LOGGING``. a dict of ``logging.config.dictConfig()`` format
  config. The settings are merged with django's default logging settings.

  * Note: 一般情况下不需要重新配置 django 自己的 loggers, 使用默认配置即可.
    因此, ``disable_existing_loggers=True`` is probably not what you want.
    因为, 如果设置禁用, 则需要在 LOGGING 中重新配置 ``django`` hierarchy
    下面的 loggers. 否则相关日志就没了.

- ``settings.LOGGING_CONFIG``. a callable that is passed ``LOGGING``
  as argument to configure logging. default ``logging.config.dictConfig``.
  ``None`` 时 django 不进行日志配置.

- logging is configured during ``setup()``.

- 如需自定义配置 logging, 可以设置 ``LOGGING_CONFIG=None`` 再手动配置.
  或者自定义两个参数的内容. 反正是相互调用的关系.

django default logging config
-----------------------------
- 对 ``django`` 和 ``django.server`` 两个 logger 有明确配置.

- ``django.server`` logger.

  * level: INFO

  * handlers:
    
    - StreamHandler to stderr. level: INFO. formatter: server time + message,
      colored based on status code.

- ``django`` logger.

  * level: INFO

  * handlers:

    - ``DEBUG=True`` 时, INFO+ 级别日志输出到 stderr. 没有特殊 formatting,
      只输出 message.

    - ``DEBUG=False`` 时, ERROR+ 级别日志给 ADMINS 发邮件.
  
  注意这个默认配置导致 ``DEBUG=false`` 时发生 exception 不会输出
  traceback 至 console.

django builtin logger hierarchy
-------------------------------

- ``django``. catch-all logger for messages in the django hierarchy.

- ``django.request``. 与处理请求相关的日志. 对于由 uncaught exception
  导致的 5XX 错误会输出 exception traceback.

  extra: ``status_code``, ``request`` object.

  日志等级:
  
  * ERROR. 5XX status code.
    
  * WARNING. 4XX status code.

- ``django.template``. template rendering infos.

- ``django.db.backends``. 数据库交互日志. 其中 ``django.db.backends.schema``
  包含 migration 过程中的 schema changes.

  extra: ``duration``, ``sql``, ``params``

  日志等级:

  * DEBUG: 执行的 sql 语句和时间. 需要配合 ``settings.DEBUG``.

- ``django.security.*`` security-related errors.

  extra: 不一定.

  日志等级: 主要是 WARNING, ERROR.

- ``django.server`` logger 仅用于 ``runserver`` development server
  输出请求和相应信息.

  extra: ``status_code``, ``request`` object.

  日志等级:
  
  * ERROR. 5XX status code.
    
  * WARNING. 4XX status code.

  * INFO. 其他.

django logging handlers
-----------------------

AdminEmailHandler
^^^^^^^^^^^^^^^^^
- constructor.

  * ``include_html=False``. control whether the traceback email includes an
    HTML attachment containing the full content of the debug Web page that
    would have been produced if DEBUG were True.

  * ``email_backend=None``. specify an alternative email backend. by default
    use ``settings.EMAIL_BACKEND``.

- behaviors.
  
  * sends an email to the site ADMINS for each log message it receives.

  * If the log record contains a ``request`` attribute, the full details of the
    request will be included in the email. The email subject will include the
    phrase “internal IP” if the client’s IP address is in the
    ``settings.INTERNAL_IPS``; if not, it will include “EXTERNAL IP”.
  
  * If the log record contains stack trace information, that stack trace will
    be included in the email.

django logging filters
----------------------
CallbackFilter
^^^^^^^^^^^^^^
简化创建新的 filter, 直接传一个 filter function 即可.

RequireDebugFalse
^^^^^^^^^^^^^^^^^
only pass on records when ``settings.DEBUG`` is False.

RequireDebugTrue
^^^^^^^^^^^^^^^^

Email
=====
- module: django.core.mail

- 如果只需要简单地发送邮件, 使用 utility functions 已经足够. 但若需要更高级、
  更细致的需求, 则应该使用 EmailMessage 等 OOP interfaces.

  utility functions 的 API 已经不再更新, 这是因为它们的存在纯粹为了向后兼容.
  由于 the list of parameters they accepted was slowly growing over time, it
  made sense to move to a more object-oriented design for email messages.

utilities
---------
- ``send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)``.
  从任意发件人给任意收件人发邮件.

  * ``subject`` and ``message`` are just strings.

  * ``from_email``. email address of sender. This is required.
    ``DEFAULT_FROM_EMAIL`` is not used here. It's used in EmailMessage.

  * ``recipient_list``. a list of receiver email addresses.

  * ``fail_silently=False``. Fail silently if any error occurs.

  * ``auth_user=None``. used by SMTP backend, by default use ``EMAIL_HOST_USER``.

  * ``auth_password=None``. used by SMTP backend, by default use
    ``EMAIL_HOST_PASSWORD``.

  * ``connection=None``. a connection is an instance of a mail backend. 这可用
    于重用邮件服务器连接或使用非默认 mail backend. 默认情况下, 每次调用
    ``send_mail()`` 都会创建一个 ``EMAIL_BACKEND`` 实例, 不会去重用. 这对于
    smtp 之类的后端意味着每发一封邮件都创建一遍连接. 可能具有效率问题 (但仍需要
    根据具体情况具体分析).

  * ``html_message=None``. string of html version of the mail message. If this
    is provided, the resulting email will be a multipart/alternative email with
    message as the text/plain content type and ``html_message`` as the
    text/html content type.

  Return 0 if sending failed, 1 if successful. 实际是发送成功的邮件数目. 由于
  这里只发送一封 (注意即使有多个收件人也是 *发送了* 一封邮件).

- ``send_mass_mail(datatuple, fail_silently=False, auth_user=None, auth_password=None, connection=None)``.
  邮件群发. 给多个收件人发送多封 (可能不同的) 邮件.

  * ``datatuple``, an iterable in which each element is a sequence in the
    following format::

      (subject, message, from_email, recipient_list)

    Each separate element of datatuple results in a separate email message.

  If ``connection`` is not specified, only one mail backend is instantiated
  and used to send all messages (via ``.send_messages()`` method).

- ``mail_admins(subject, message, fail_silently=False, connection=None, html_message=None)``.
  A shortcut for sending email to ADMINS. 这用于系统管理方面的邮件, 例如告警.
  发件人自动设为 ``SERVER_EMAIL``. Subject is prefixed with
  ``EMAIL_SUBJECT_PREFIX`` automatically.

- ``mail_managers(subject, message, fail_silently=False, connection=None, html_message=None)``.
  like ``mail_admins()``, for sending to MANAGERS.

safe MIME types
---------------
- include SafeMIMEMessage, SafeMIMEText, SafeMIMEMultipart.

- 这些 mime types 对 header injection attack 进行了防范. They forbidding
  newlines in header values. If any ``subject``, ``from_email`` or
  ``recipient_list`` contains a newline (in either Unix, Windows or Mac style),
  the email function (e.g. ``send_mail()``) will raise
  ``django.core.mail.BadHeaderError`` (a subclass of ValueError) and, hence,
  will not send the email.

EmailMessage classes
--------------------
- EmailMessage is responsible for creating the email message itself.

EmailMessage
^^^^^^^^^^^^
constructor
"""""""""""
- ``subject=""``. email subject line.

- ``body=""``. email body text.

- ``from_email=None``. default is ``settings.DEFAULT_FROM_EMAIL``.

- ``to=None``. an iterable of recipient addresses.

- ``bcc=None``. an iterable of Bcc addresses.

- ``connection=None``. the email backend instance to use for send this
  EmailMessage during ``.send()``.

- ``attachments=None``. a list of attachments. Each attachment can be either
  MIMEBase instance, or ``(filename, content, mimetype)`` tuple. If mimetype
  is not provided, guess it from filename or use a default
  ``application/octet-stream``. content can be a string or bytes form of file.

- ``headers=None``. A dict of extra headers to put on the message.

- ``cc=None``. an iterable of Cc addresses.

- ``reply_to=None``. an iterable of Reply-To addresses.

instance attributes
""""""""""""""""""""
- ``subject``

- ``body``

- ``from_email``

- ``to``

- ``bcc``

- ``connection``

- ``attachments``

- ``extra_headers``

- ``cc``

- ``reply_to``

instance methods
""""""""""""""""
- ``send(fail_silently=False)``. Send the message via ``self.connection`` or by
  instantiating a default mail backend. If ``fail_silently`` is True,
  exceptions raised while sending the message will be quashed.

- ``message()``. Construct a django.core.mail.SafeMIMEText object (a subclass
  of Python’s MIMEText class) or a django.core.mail.SafeMIMEMultipart object
  (a subclass of MiMEMultipart) holding the message to be sent.

- ``attach(filename=None, content=None, mimetype=None)``. add attachment to
  ``self.attachments``. Argument format:
 
  * one argument that is a MIMEBase instance
   
  * 3 arguments ``(filename, content, mimetype)``. filename is the name of the
    file attachment as it will appear in the email, content is the data that
    will be contained inside the attachment and mimetype is the optional MIME
    type for the attachment. If you omit mimetype, the MIME content type will
    be guessed from the filename of the attachment.

  If you specify a mimetype of message/rfc822, it will also accept
  django.core.mail.EmailMessage and email.message.Message.

  For a mimetype starting with text/, content is expected to be a string.
  Binary data will be decoded using UTF-8, and if that fails, the MIME type
  will be changed to application/octet-stream and the data will be attached
  unchanged.

- ``attach_file(path, mimetype=None)``. a shortcut method to attach a file from
  filesystem. If the MIME type is omitted, it will be guessed from the
  filename.

EmailMultiAlternatives
^^^^^^^^^^^^^^^^^^^^^^
- subclass of EmailMessage.

- Useful to include multiple versions of the content in an email.

constructor
"""""""""""
- inherit all parameters from EmailMessage.

- ``alternatives=None``. an iterable of alternatives. Each alternative is a
  tuple of ``(content, mimetype)``.

instance methods
""""""""""""""""
- inherit all methods from EmailMessage.

- ``attach_alternative(content, mimetype)``. include extra versions of the
  message body in the email.

email backends
--------------
- The email backend is responsible for sending the email.

- support context manager protocol.

- email backend protocol:
  
  * Custom email backends should subclass BaseEmailBackend that is located in
    the django.core.mail.backends.base module.
    
  * A custom email backend must implement the ``send_messages(email_messages)``
    method. This method receives a list of EmailMessage instances and returns
    the number of successfully delivered messages.
    
  * If your backend has any concept of a persistent session or connection, you
    should also implement the ``open()`` and ``close()`` methods.

utilities
^^^^^^^^^
- ``get_connection(backend=None, fail_silently=False, **kwargs)``. get an
  instance of the specified or default email backend. ``backend`` is its
  import path, ``fail_silently`` and ``kwargs`` are passed to constructor.

base.BaseEmailBackend
^^^^^^^^^^^^^^^^^^^^^
- defines the interface of email backends.

instance methods
""""""""""""""""
- ``open()``. open a connection to mail server.

- ``close()``. close the opened connection.

- ``send_messages(email_messages)``. send a list of EmailMessages, return the
  number of emails sent. If the connection is not open, this call will
  implicitly open the connection, and close the connection afterwards. If the
  connection is already open, it will be left open after mail has been sent.

- ``__enter__()``. open on entering context. return self.

- ``__exit__(exc_type, exc_value, traceback)``. close on exiting from context.

smtp.EmailBackend
^^^^^^^^^^^^^^^^^
- subclass of BaseEmailBackend.

- send email via SMTP protocol.

constructor
""""""""""""
以下参数若省略某个, 则 fallback 至相应的各个 settings 配置项.

- ``host=None``

- ``port=None``

- ``username=None``

- ``password=None``

- ``use_tls=None``

- ``use_ssl=None``

- ``timeout=None``

- ``ssl_keyfile=None``

- ``ssl_certfile=None``

- ``fail_silently=False``

console.EmailBackend
^^^^^^^^^^^^^^^^^^^^
- subclass of BaseEmailBackend.

- writes the emails that would be sent to the specified stream or stdout.

- It utilizes the ``.as_bytes()`` method of mime subtype messages.

constructor
""""""""""""
- all from BaseEmailBackend.

- ``stream=sys.stdout``. the stream where to write email.

filebased.EmailBackend
^^^^^^^^^^^^^^^^^^^^^^
- subclass of console.EmailBackend. 主要重用了 ``.send_messages()``.

- write emails to a file.

- A new file is created for each new session that is opened on this backend
  instance.  注意这指的是, 一组从 ``.open()`` 到 ``.close()`` 的组合是一个
  session. The directory to which the files are written is either taken from
  the ``file_path`` constructor parameter, or fallback to
  ``settings.EMAIL_FILE_PATH``.

constructor
""""""""""""
- ``file_path=None``. directory where to put email files. fallback to
  ``settings.EMAIL_FILE_PATH``.

locmem.EmailBackend
^^^^^^^^^^^^^^^^^^^
- subclass of BaseEmailBackend.

- An email backend for use during test sessions. The test connection stores
  email messages in a dummy outbox (django.core.mail.outbox), rather than
  sending them out on the wire.

- ``outbox`` is a list of EmailMessage instances for each message that would
  be sent.

dummy.EmailBackend
^^^^^^^^^^^^^^^^^^
- subclass of BaseEmailBackend.
- the dummy backend does nothing with your messages.

settings
--------
- ``EMAIL_BACKEND``. backend used for sending email. default
  django.core.mail.backends.smtp.EmailBackend.

- ``EMAIL_HOST``. server hostname for sending email. default localhost.

- ``EMAIL_PORT``. server port for sending email. default 25.

- ``EMAIL_HOST_USER``. username for SMTP email server authentication. if empty
  authentication is not performed. default "".

- ``EMAIL_HOST_PASSWORD``. password for SMTP email server authentication. if
  empty authentication if not performed. default "".

- ``EMAIL_USE_TLS``. whether to use explicit TLS when talking to SMTP server.
  default False.

- ``EMAIL_USE_SSL``. whether to use implicit TLS when talking to SMTP server.
  default False. Note that EMAIL_USE_TLS/EMAIL_USE_SSL are mutually exclusive,
  so only set one of those settings to True.

- ``EMAIL_SSL_CERTFILE``. the path to a PEM-formatted certificate chain file to
  use for the SSL/TLS connection. default None.

- ``EMAIL_SSL_KEYFILE``. the path to a PEM-formatted private key file to use
  for the SSL/TLS connection. default None.

- ``DEFAULT_FROM_EMAIL``. Default email address to use for various automated
  correspondence from the site manager(s). This doesn’t include error messages
  sent to ADMINS and MANAGERS. default webmaster@localhost.

- ``SERVER_EMAIL``. The email address that error messages come from. default
  root@localhost.

- ``EMAIL_FILE_PATH``. The directory used by the ``file`` email backend to
  store output files.

- ``EMAIL_SUBJECT_PREFIX``. Subject-line prefix for email messages sent with
  django.core.mail.mail_admins or django.core.mail.mail_managers. default
  ``[Django] ``.

- ``EMAIL_TIMEOUT``. a timeout in seconds for blocking email operations like
  the connection attempt. default None.

- ``EMAIL_USE_LOCALTIME``. Whether to send the SMTP Date header of email
  messages in the local time zone or in UTC. default False.

i18n
====

testing
=======

writing test cases
------------------

SimpleTestCase
^^^^^^^^^^^^^^
- 默认情况下禁止访问数据库. 如果测试用例不需要使用数据库, 则可以使用这个
  test case class 来强制禁止.

- 这里也显然不会去处理 db 状态在测试之间的一致性.

class attributes
""""""""""""""""
- ``allow_database_queries=False``. disable db queries by default. Because
  transaction isn't enforced between tests.

- ``client_class=Client``.

attributes
""""""""""
- ``client``. test client instance. 由于每个 test case instance 只有一个 test
  method to run. 所以 client 实际上为单个 method 服务. 不存在 test method 之间
  client state 的问题.

assertions
""""""""""
- ``assertFieldOutput(fieldclass, valid, invalid, field_args=None, field_kwargs=None, empty_value="")``
  test form field behavior. 用于简化 custom form field validation 方面的测试?

- ``assertFormError(response, form, field, errors, msg_prefix="")``.
  并没有什么用. 集成测试级别的输入, 单元测试级别的检测, 乱七八糟.

- ``assertFormsetError(response, formset, form_index, field, errors, msg_prefix='')``.
  ditto.

- ``assertRaisesMessage(expected_exception, expected_message)`` or
  ``assertRaisesMessage(expected_exception, expected_message, callable, *args, **kwargs)``.
  A simpler form of ``TestCase.assertRaisesRegex``. 这里简单检测 exception 的
  string form 中是否包含 message.

- ``assertWarnsMessage(expected_warning, expected_message)`` or
- ``assertWarnsMessage(expected_warning, expected_message, callable, *args, **kwargs)``.
  ditto for ``TestCase.assertWarnsRegex()``

- ``assertHTMLEqual(html1, html2, msg=None)``. compare equality based on html
  semantics. see docs for what is considered equal.

- ``assertHTMLNotEqual(html1, html2, msg=None)``.

- ``assertInHTML(needle, haystack, count=None, msg_prefix="")``
  "in" checking based on html semantics.

- ``assertXMLEqual(xml1, xml2, msg=None)``

- ``assertXMLNotEqual(xml1, xml2, msg=None)``

- ``assertJSONEqual(json, expected_data, msg=None)``. json is in dumpped string
  form.

- ``assertJSONNotEqual(json, expected_data, msg=None)``

- ``assertTemplateUsed(response, template_name, msg_prefix='', count=None)`` or
  ``assertTemplateUsed(template_name)``.

  * 作为 context manager 使用时, 无需生成 response, 因此可以进行任何单元级别的
    template rendering 相关检测.

  * ``template_name`` 是 ``Template.name``, 一般是从 root namespace 定位
    template 时使用的相对路径.

  * ``count``, the number of time the template should be rendered, as occurred
    in ``response.template_names``.

  * 注意如果要验证的模板在所有模板搜索路径中存在重复, 即刻意的
    overriding/extending, 只通过 ``template_name`` 校验不能完全保证正确加载, 还
    需校验 ``Template.origin.name``. 这可通过::

      self.assertTrue(any("..." in t.source.name for t in response.templates))

- ``assertTemplateNotUsed(response, template_name, msg_prefix="")`` or
- ``assertTemplateNotUsed(template_name)``.

- ``assertContains(response, text, count=None, status_code=200, msg_prefix="", html=False)``
  check response's status code, text occurs in its content (for exact count
  times if provided), ``html`` see ``assertHTMLEqual()``

- ``assertNotContains(response, text, status_code=200, msg_prefix="", html=False)``
  注意要求 status code 匹配、text 不匹配.

- ``assertRedirects(response, expected_url, status_code=302, target_status_code=200, msg_prefix="", fetch_redirect_response=True)``

  * If response is not a followed response, check response has ``status_code``,
    and redirects to ``expected_url``. If ``fetch_redirect_response``, then the
    response is followed in this method, the ``target_status_code`` is checked.

  * If response is a followed response, check the final point of redirect chain
    matches ``expected_url`` and ``target_status_code``.

override settings
"""""""""""""""""
- ``settings(**options)``. like ``django.test.utils.override_settings``. Normally used as context manager.

- ``modify_settings(**option_configs)``. like ``django.test.utils.modify_settings``.
  But normally as context manager.

hooks
"""""
- ``_pre_setup()``. 这里做了以下事情:

  * 每个 test case 执行之前新建一个 ``client`` instance.

  * 每个 test case 执行之前清空 ``mail.outbox``.

TransactionTestCase
^^^^^^^^^^^^^^^^^^^
- subclass of ``SimpleTestCase``.

- TransactionTestCase 不是说把每个 test wraps 到一个 transaction 中. 而是说,
  它适合测试 transaction 相关的功能点. 它本身并没有自动使用 transaction.

  例如, 当一个功能点的行为根据是否在 transaction 中具有不同表现, 则无法使用
  ``django.test.TestCase`` 进行测试, 因它总是在 transaction 中执行 test case.

- json fixture loading. TransactionTestCase 保证每个 test case 数据库状态的方式
  是,
  
  * 在每个 test case 执行之前, load test fixture into database
  (``./manage.py loaddata``);
  
  * test case 执行之后, flush database (``./manage.py flush``), 恢复到 migration
    执行后的状态.

  这是在 ``unittest.TestCase.__call__`` 的外面来执行的. 因此在 method level
  的 ``setUp()`` 之前与 ``tearDown()`` 之后.

- 对初始数据的注意事项.

  * TransactionTestCase 本身没有自动应用 transaction, 为恢复数据库状态, 采用的方法
    是 test case 后 flush database. 然而这也会丢失在 migration phase 应用的 data
    migration 数据.

  * 这就是为什么说当直接使用 TransactionTestCase 时, 只应该用于测试 transaction.
    而 SimpleTestCase/TestCase 在单元或集成测试中一般都是更好的选择.

  * 对于需要 TransactionTestCase 保留初始数据的情况, 应设置 ``serialized_rollback``.
    LiveServerTestCase, StaticLiveServerTestCase 等就是这样.

class attributes
""""""""""""""""
- ``multi_db=False``. 默认只使用对应于 default db 的测试数据库. True 则使用
  所有数据库. 这造成的影响包括:
  
  * json fixture 会 load into all dbs.

  * flush data 时会 flush 所有数据库.

- ``serialized_rollback=False``. Reload initial data applied during migration
  phase (data migration), on a per-testcase basis. 这是为了避免, TransactionTestCase
  在 test case 执行完后 flush database 导致的初始数据丢失.

  这个选项要配合 ``SERIALIZE=True``.

- ``reset_sequences=False``. reset all sequences before before running each
  test cases.

assertions
""""""""""
- ``assertQuerysetEqual(qs, values, transform=repr, ordered=True, msg=None)``.
  qs is transformed by ``transform``, then compared with values.

  * If unordered, item counts are compared.

  * If ordered, they must be a list of the same items. 在考虑顺序的比较时, if
    qs is not ordered, ValueError is raised.

- ``assertNumQueries(num, func, *args, using=DEFAULT_DB_ALIAS, **kwargs)`` or
- ``assertNumQueries(num, using=DEFAULT_DB_ALIAS)``
  assert the number of db queries are made in ``func(*args, **kwargs)`` or in
  the context.

TestCase
^^^^^^^^

- subclass of ``TransactionTestCase``.

- Suitable for tests that rely on database access. It runs each test inside a
  transaction to provide isolation.

- All test methods are wrapped in an overall transaction (由 ``setUpClass`` 设
  置); each test method is wrapped in an individual savepoint (由
  ``_fixture_setup`` 设置).

- json fixture loading. 与 TransactionTestCase 不同, TestCase 只在 ``setUpClass``
  中加载一次 json fixture. 在 ``setUpTestData()`` 之前.

class methods
"""""""""""""
- ``setUpTestData()``. Setup test data common to the entire test class.  这些数
  据在 ``tearDownClass()`` 中随其他数据一起被 rollback. 这用于 class-level test
  data setup. 这个方法在 json fixture loading 之后执行.

LiveServerTestCase
^^^^^^^^^^^^^^^^^^
- Subclass of ``TransactionTestCase``. 因此注意它保证数据库状态一致性的方式
  并没有使用 transaction.

  * 注意必须设置 ``serialized_rollback=True``, 以保证 data migration 不被
    flush 掉. 并且考虑到 FT 对效率不太敏感.

- 它的逻辑是, 单开线程运行 threaded dev server. 从主线程中发请求 (而不是直接
  访问 django 内部) 至 server socket, 由 OS 转发至 server thread. 后者按照
  标准的服务端处理流程进行响应.

  除此之外, LiveServerTestCase 与 TransactionTestCase 的功能一致.

- 它不是 subclass of ``TestCase``. 原因: TestCase 需要共享 class-level atomic
  blocks (``TestCase.cls_atomics``). 由于 TestCase class 是全局的, 将导致各个线
  程共享 transaction. 而这里, 我们需要 server thread 自己做线程和 transaction
  管理 (就像一个标准 web server 那样). 所以不能使用 TestCase.

- 配合外部测试工具使用. 当外部测试工具需要进行 functional tests, 进行真实的
  服务端访问时, 必须要有一个 web server 在运行, 不能使用 ``django.test.Client``
  这种内部模块单元测试工具来模拟.

  然而, 我们不能开一个普通的 dev server (``runserver``), 因为我们需要让功能性
  测试运行在 test database 上. 而研发服务器使用的是标准数据库配置
  ``settings.DATABASES`` 而不是 ``TEST`` 部分配置. ``LiveServerTestCase``
  就是解决了这个问题, 它在当前进程即 ``./manage.py test`` 命令进程中开一个 dev
  server thread, 这样自动使用了已经使用 ``TEST`` 部分配置好的数据库连接, 只会
  访问测试数据库.

- 注意 django core 的 runserver command 不提供 serve static files 的功能.
  相应地 ``LiveServerTestCase`` 只是为了方便, 提供了 serve ``STATIC_ROOT``
  下静态文件的功能. 若要方便测试时 serve 源代码目录下的静态文件, 使用
  `StaticLiveServerTestCase`_.

- Server thread is launched during test class setup, shut down during test
  class teardown.

- 测试服务器以线程方式与功能测试运行在一个进程中, 还有一个必要性:

  * 研发阶段的功能测试可能需要 mock 不方便的外部依赖. 这样, test method 必须
    与 dev server 在一个进程中, 共享全局对象. 这样 test method 中对全局量的
    修改, 在 dev server 线程中才能可见.

  * 注意到, 这也给出了一个功能测试时进行 mock 的限制: 只能 mock 多线程都可见
    的全局量.

class attribute
"""""""""""""""
- ``host='localhost'``.

- ``port=0``. default 0. ephemeral port.

- ``server_thread_class=LiveServerThread``

- ``static_handler``. handler for serving static files.

- ``live_server_url``. 默认设置 server thread bind to localhost and some
  ephemeral port (0). 所以需要访问这个属性获取实际的 url.

StaticLiveServerTestCase
^^^^^^^^^^^^^^^^^^^^^^^^
- See `StaticLiveServerTestCase`_.

json test fixtures
^^^^^^^^^^^^^^^^^^
- 避免使用 json test fixtures.
  
  * json test fixtures are loaded and purged between each test methods.
    所以会非常慢.

  * It makes test less readable (because json fixture's content is opaque in
    test code)

  * It makes test less maintainable (如果多个 test case 需要使用类似的却不完全相同的
    json fixtures, 则需要复制整个 json file. 再做修改.)

  * schema changes needs to modify json fixtures accordingly.

- 准备 test data 的更好方式.
  
  * test method 中配置 fixture data.
    
  * test method level common fixture data, ``setUp()``, ``tearDown()``.

  * test class level common fixture data ``setUpTestData()``, ``setUpClass()``.
    
  配合 factory boy, faker 等使用.

override settings
^^^^^^^^^^^^^^^^^
- ``override_settings(**options)``. temporarily overrides a list of settings
  passed in as kwargs. 相关的 setting 的值被直接替换掉.
  
  Can be used as context manager, function/class decorator etc.

- ``modify_settings(**option_configs)``. 当要修改的 setting 的值是多项时, 直接
  替换不方便. 使用这个来做部分修改. value of each key is a dict with three
  optional keys:

  * ``append``

  * ``prepend``

  * ``remove``

  whose value can be a string or a list of values. 注意, keys 的顺序影响操作结果.
  所以要考虑清楚.

  Can be used as context manager, function/class decorator etc.

- 临时删除配置项.

  * 使用 ``override_settings()`` without args. ``override_settings`` 本身会创建
    一个 new settings 临时替换 original settings.

  * 在 test 过程中, 访问 settings, 删除所需属性.

- 以上修改 settings 的 procedure, 会在正向和反向修改结束后都 trigger
  ``setting_changed`` signal.

email handing
^^^^^^^^^^^^^
- test runner transparently replaces the normal email backend with an in-memory
  noop backend ``locmem.EmailBackend``. See `locmem`_ for details.

- ``mail.outbox``.

  * a list of ``EmailMessage`` accumulated during test method running.

  * 该属性只在测试时存在.
  
  * 对于 SimpleTestCase, 每个 test method 执行之前会清空 outbox. 通过设置
    ``mail.outbox = []`` 来手动清空.

request and response
--------------------

RequestFactory
^^^^^^^^^^^^^^
- 用于生产 mock HttpRequest objects. 这主要用于对 view 进行单元测试时, 传递进入
  view.

- 说它是 mock request, 是因为这样生成的 HttpRequest, 可以具有 view 交互所需的
  api & attributes, 但并不与真实的 HttpRequest 完全相同. 这符合 mock 的实质. 
  RequestFactory 的意义是封装了对这种很复杂的 mock object 的构建流程. 否则每次
  手工去构建的话, 根本不可能.

constructor
"""""""""""
- ``json_encoder=DjangoJSONEncoder``. json encoder used when posting json data.

- ``**defaults``. default wsgi request environs. can be overriden by calls of
  each request methods.

request methods
"""""""""""""""
- ``get()``, ``post()``, ``put()``, ``delete()``, ``head()``, ``options()``,
  ``trace()``.
  
- see `Client`_ for signatures. They have the same signature except for
  ``follow``.

- 它的各个 request methods 只是生成相应的 fake HttpResponse object 即返回, 并不
  进行真正的 request processing 流程. 这由它的子类 Client 来实现.

Client
^^^^^^
- ``django.test.Client``. subclass of RequestFactory.

- test client is an integration testing tool. 因为它跨越了太多的功能层和模块,
  包含 middleware, url resolution, view wrappers, etc., 然后才到 view callable.

  Test client is neither suitable for unit testing nor functional testing.  它
  不适合 FT 是因为: 1) 它直接访问了 django 的内部结构来进行请求, 不具有外部视角;
  2) 它不具备浏览器的功能, 不能渲染页面, 从而不能测试最终效果, 只生成 response
  object 结束.

constructor
"""""""""""
- ``enforce_csrf_checks=False``. By default Client disables csrf checks.
  这是通过 CsrfViewMiddleware 提供的一个 hack 来实现的.

- ``json_encoder=DjangoJSONEncoder``. see RequestFactory.

- ``**defaults``. See RequestFactory.

attributes
""""""""""
- ``cookies``. 保存客户端 cookies. 对于每个, ``HttpResponse.cookies`` 全部同步
  到 Client 上. Client 在每次请求时, 都将保存的 cookies 加入 ``HTTP_COOKIE``
  header.

- ``session``. 直接访问 session backend 获取对应于当前客户端的 SessionStore.

request methods
""""""""""""""""
- ``get(path, data=None, follow=False, secure=False, **extra)``.

  * ``path`` is absolute url target.

  * ``data`` is a dict of query string payload. query string can be added
    in ``path`` directly. If both ``path`` and ``data`` is present, ``data``
    takes precedence.

  * ``follow``. whether or not follow redirection. If so, a ``redirect_chain``
    is added to response object, which is a list of 2-tuple of intermediate
    ``(url, status)``.

  * ``secure``. emulate https request.

  * ``extra``. extra WSGI environ items. E.g., extra http headers, cgi variables.

- ``post(path, data=None, content_type=MULTIPART_CONTENT, follow=False, secure=False, **extra)``

  * ``path``, ``follow``, ``secure``, ``extra``. ditto.
    post 时, query string 只能加在 ``path`` 上面.

  * ``data`` is a dict of post data.
    
  * ``content_type``.

    - If ``multipart/form-data; boundary=...``, data is treated as form data.
      此时, value in data can be string (coerced to bytes), file-like object
      (``.read()`` is called once), an iterable (当一个 key 有多个值时).

    - If ``application/json``, data is serialized as json data, by ``json_encoder``.

    - 对于其他 content-type, data is converted to bytes and used as is.

- ``head(path, data=None, follow=False, secure=False, **extra)``. like get, 
  except response body is empty.

- ``options(path, data='', content_type='application/octet-stream', follow=False, secure=False, **extra)``.
  if data is provided, it's used as-is, no parsing.

- ``put(path, data='', content_type='application/octet-stream', follow=False, secure=False, **extra)``
  data is encoded according to ``content_type``.

- ``patch(path, data='', content_type='application/octet-stream', follow=False, secure=False, **extra)``
  data is encoded according to ``content_type``.

- ``delete(path, data='', content_type='application/octet-stream', follow=False, secure=False, **extra)``
  data is encoded according to ``content_type``.

- ``trace(path, follow=False, secure=False, **extra)``

authentication
""""""""""""""

- ``login(**credentials)``. simulate user login, manually, without making an
  actual login post request. 由于不走 request-response cycle, 这里需要单独调用
  相关的 session, cookie 等设置逻辑. 调用该方法后, Client instance 的 ``cookies``
  中包含 session cookie. 后端的 session 也设置完毕.

  Return True/False for login success/failure.

- ``force_login(user, backend=None)``. log user in, skipping authentication.
  除了跳过认证阶段之外, 其他与 ``Client.login()`` 一致.

  The user will have its ``backend`` attribute set to the value of the backend
  argument (which should be a dotted Python path string), or to
  ``settings.AUTHENTICATION_BACKENDS[0]`` if a value isn’t provided.

- ``logout()``. logout current user. clear Client's cookie.

utilities
"""""""""
- ``request()`` process a request, returns a HttpResponse object. 它直接调用
  request wsgi handler 去处理请求, 所以 ``path`` 只需要是 absolute url 即可, 不
  需要 domain 部分.

FakePayload
^^^^^^^^^^^
A wrapper around BytesIO that restricts what can be read since data from the
network can't be seeked and cannot be read outside of its content length. This
makes sure that views can't do anything under the test client that wouldn't
work in real life.

testing-purpose HttpResponse attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- ``client``.

- ``request``. All parameters of the initiating request.

- ``wsgi_request``. The WSGIRequest object that django http processing code
  actually sees.

- ``template``. A list of Template instances used to render the final content,
  in the order they were rendered.

- ``context``. A template context object or a ``ContextList`` of template
  context objects, in the order in which they were rendered. Regardless,
  the template variable can be accessed via key.

- ``json(**kwargs)``. parse content as json. works only if Content-Type is
  ``application/json``, otherwise ValueError is raised. ``kwargs`` are passed
  to ``json.loads()``.

- ``status_code``.

- ``resolver_match``. An instance of ResolverMatch for the requested url.

- ``redirect_chain``. available when redirection is followed.

test tags
---------
- ``@tag(*tags)``. 应用于 test class/method 上. Subclasses inherit tags from
  superclasses, and methods inherit tags from their class.

  object's tags is kept in its ``obj.tags`` attribute, as a set.

- 对不同类型的测试用例应添加相应的 tag, 例如 ``ut`` for unit test, ``it`` for
  integration test, ``ft`` for functional test. 这样有助于在命令行上迅速选择需
  要执行的测试集::
 
    ./manage.py test [--tag <tag1>]... [--exclude-tag <tag>]...

  无需写冗长的目录层级以及遍历所有 apps.

- 注意必须要避免测试代码中出现 module level error. 这会影响给测试用例打 tag.
  
  当测试代码存在 module level error 时 (例如在文件顶部发生 import error), 会导
  致 tag 无法生效 (因为根本没有执行). 这样, 在 ``./manage.py test --tag`` 对执
  行 tag 执行测试时, 就会直接过滤掉这些加载失败的测试代码. 这导致看上去新增的测
  试用例没有执行. 然而, 如果执行全部测试用例时 (不过滤), 则发现这些测试代码发生
  了 module level error.

skipping tests
--------------
- ``@skipIfDBFeature(*features)``. decorator to class or method. skip if
  db supports at least one of the named features. A feature is an attribute
  name of ``connection.features``, as in ``DatabaseFeatures`` of each db
  backend.

- ``@skipUnlessDBFeature(*features)``. Skip a test unless a database has all
  the named features.

- ``@skipUnlessAnyDBFeature(*features)``. Skip a test unless a database has any
  of the named features.

test databases
--------------

workflow
^^^^^^^^
- 测试时对数据库的配置操作由 test runner 定义. 以下描述适用于 DiscoverRunner.

- 对于每个 ``settings.DATABASES`` 中配置的数据库, 测试时单独创建一个相应的测试
  数据库.

  * 测试数据库在测试开始时创建, 测试结束后自动删除. 除非使用了 ``--keepdb`` option.

  * 创建测试库的顺序由 ``TEST.DEPENDENCIES`` key 决定.

- 创建数据库后, 自动应用 migrations.

test database definitions
^^^^^^^^^^^^^^^^^^^^^^^^^
- 每个数据库依据各自的 ``TEST`` dictionary 进行创建. 注意 TEST dict 只进行测试库
  定义, 而连接参数仍然使用 parent db settings dict.

- 测试时使用的数据库用户必须有创建、删除数据库的权限.

keys
""""
- ``NAME``. test db name. default ``test_${NAME}``.

  * for sqlite, by default use a in-memory db.

- ``CHARSET``. 创建测试库使用的 charset. 注意到 ``DATABASES`` connection dict
  中没有这一项, 这是因为生产库不是由 django 创建的. 在那里, 只需要配置连接参数.
  而这里是建库参数. 默认使用 db-specific default.

  * 对于 mysql, fallback to ``character_set_server``

- ``COLLATION``. ditto.

  * 只对 mysql 有效, fallback to ``collation_server``

- ``SERIALIZE``. serialize database state into in-memory JSON, attached to db
  connection, used to restore database state between tests in TransactionTestCase
  with ``serialized_rollback=True``.  default True.

- ``DEPENDENCIES``. test db creation dependency. default ``['default']``.

- ``MIRROR``. 配置该测试数据库为某个 alias 的 mirror. 这是在当 parent dict 实际
  上是作为某个 primary 数据库的 replica 时来使用. 设置 mirror 后, 该测试库并不
  单独创建, the connection to replica will be redirected to point the database
  it mirrors. 这样就模拟了 replication.

mysql
"""""
- 关于 charset & collation 的设置, 见 mysql sections of `backend-specific notes`_
  of `database`_.

test runners
------------
- test runner 实际上封装了 django test 的完整流程. ``test`` management
  command 的全部行为由 test runner 定义.

- test runner 的 API 要求:
  
  * ``run_tests(test_labels)``. Accept an iterable of test labels passed on cli
    as positionals. return the number of failed tests.

  * ``add_arguments(cls, parser)``. class method. optional. add CLI definitions
    to ``test`` command.

DiscoverRunner
^^^^^^^^^^^^^^
DiscoverRunner 的工作流程, see `DiscoverRunner run_tests`_.

run tests
""""""""""
.. _DiscoverRunner run_tests:

- ``run_tests(test_labels, extra_tests=None, **kwargs)``.

  * ``extra_tests`` a list of extra ``unittest.TestCase`` instances to be 
    added to the discovered test suite.

  workflow.

  * setup test environment. see `setup/teardown`_.
  
  * build test suite by test discovery. see `test discovery`_.
  
  * setup test databases. see `setup/teardown`_.
  
  * running system checks.
  
  * running test suite.
  
  * tear down test databases. see `setup/teardown`_.
  
  * tear down test environment. see `setup/teardown`_.
  
  * return the number of test failure and errors.

setup/teardown
""""""""""""""
- ``setup_test_environment(**kwargs)``. call ``django.test.utils.setup_test_environment``.

  * 为保证测试与生产情况符合, 默认 runner 会在 setup 过程中设置 ``DEBUG=False``.

- ``teardown_test_environment(**kwargs)``. call ``django.test.utils.teardown_test_environment``.

- ``setup_databases(**kwargs)``. call ``django.test.utils.setup_databases``.

- ``teardown_databases(old_config, **kwargs)``. call ``django.test.utils.teardown_databases``.

cli handling
""""""""""""
- ``add_arguments(parser)``. add command line arguments to ``parser``.
  DiscoverRunner 定义了以下选项:

  * ``--pattern <pattern>``. same option to unittest discovery cli. It defaults
    to ``test*.py``.

  * ``--top-level-directory``. same option to unittest discovery cli.

  * ``--keepdb``. Preserve test database between ``./manage.py test`` runs.
    测试数据库和相关 migrations 若已经存在则不会重新创建, 测试运行完后也不会
    销毁测试数据库. 每次执行时检查是否有 unapplied migrations, 若有则应用.
    这可以极大地提高单元测试执行速度.

  * ``--reverse``. sort test cases in reverse order. 可用于调试 test isolation
    问题.

  * ``--debug-mode``. 一般测试时 ``DEBUG=False``. 这里强制设置为 True, 可
    用于调试测试中遇到的问题.

  * ``--debug-sql``. 使用 CursorDebugWrapper, 将 sql logging 同 unittest 对每个
    test case 的信息一同输出. 在与 django 默认日志配置相兼容的 ``LOGGING_CONFIG``
    配置下, 这里会默认只对 failing test 输出 sql log; 当 ``--verbosity`` >= 2
    时, 对所有 test 都输出.

  * ``--parallel [N]``. run tests in parallel. If N is omitted, use host's
    number of logical cores.

    Each process gets its own database. You must ensure that different test
    cases don’t access the same external resources.

    To display traceback, require tblib. 即使这样也可能出问题. 因此只能说
    如果希望很快执行一遍, 可以尝试这个. 但不保证可靠.

  * ``--tag <tag>``. run specified tag. may be specified multiple times.

  * ``--exclude-tag <tag>``. this takes precedence over ``--tag``. may be
    specified multiple times.

- 对 CLI 上 ``test_label`` 的解释:

  * 可以是 unittest 接受的单个 module, class, method, etc. 但不能是 file path.

  * 可以是 unittest discover 接受的目录, 或 import path, for discovery.

  * 若不指定, 相当于从当前目录开始 test discovery.

test discovery
""""""""""""""
- 基于 unittest discovery 来构建 test suites. 因此, test files 可以根据任何项目
  合理的方式去组织.

- discovered test suite is filtered by tags.

- discovered test suite is reordered into the following running order.

  1. ``django.test.TestCase`` instances.

  2. ``django.test.SimpleTestCase`` instances (including TransactionTestCase).

  3. ``unittest.TestCase`` instances.

  这是按照对测试数据库状态的可能影响的持续程度来排序的.

  .. TODO 不知道这样会不会 break module-level setup/teardown?

test utilities
--------------
- assist in the creation of your own test runner. used by DiscoverRunner.

settings
--------
- ``TEST_RUNNER``. 定义 ``test`` management command 使用的 runner.

- ``DATABASES[alias].TEST``. see `test database definitions`_.

management commands
-------------------

test
^^^^
::
  ./manage.py test [<test_label>]...

- 对 ``test_label`` 的解析取决于 test runner. See `test runners`_.

- Abort testing. similar to unittest's behavior.

  * press Ctrl-C once. the test runner will wait for the currently running test
  to complete and then exit gracefully. During a graceful exit the test
  runner will output details of any test failures, report on how many tests
  were run and how many errors and failures were encountered, and destroy any
  test databases as usual. 

  * press Ctrl-C twice. the test run will halt immediately, but not gracefully.
  No details of the tests run before the interruption will be reported, and
  any test databases created by the run will not be destroyed.

- options.

  * ``--failfast``. same option of unittest

  * ``--testrunner``. specify a test runner class to use, instead of
    ``settings.TEST_RUNNER``.

- also accepts other options defined by test runner class.
  See `test runners`_.

integration with testing frameworks
-----------------------------------
- django 默认基于 unittest module 实现自动化测试的诸多功能. 但提供与多种单元测
  试框架集成的方式.

design patterns
---------------
- test directory organization:
  
  * FT/IT/UT 分别放在 ``<app_name>/fts``, ``<app_name>/its``, ``<app_name>/uts``.

  * 由于使用 unittest discovery 机制, 目录名称不需要固定.

- Every layers of code must be unit-tested in isolation. view, form, model etc.
  Use mocks to ensure test isolation.

  * 严格来说, 对于 model layer 的 UT, 数据库是一个外部依赖, 应该 mock 掉. 但
    实际上需要看情况处理.
   
  * 如果相关数据库操作容易 mock (只涉及固定的一两个数据库操作), 则可以 mock 掉.
    这样可以极大地提高该 UT 执行效率 (可以做到测试用例执行时间在 0.002s 以下).
    
  * 如果不容易 mock, 则可以保持一点 integration 的意味. 这样避免了需要对 db 层
    进行复杂的 mock, 可以检测到 model layer 真实应用到数据库中可能产生的意料之
    外的问题.

- model layer test 除非必要, 尽量不碰数据库. 数据库会极大降低 UT 的执行速度.

  * use in-memory model instance whenever possible.

- 选择使用合适的 test case class:

  * ``unittest.TestCase``. 对于单元测试, 为保证测试的独立性, 可以选择不使用
    django test case classes. 这样避免了访问 django 提供的集成测试工具.
  
  * ``SimpleTestCase``. 适合测试不需要使用数据库时, 这样可以完全禁止访问数据库.
    适合单元测试, 不适合集成和功能测试.

  * ``TransactionTestCase``. 适合测试需要手动构建 db transaction 的情况, 无论
    是单元还是集成. 但除此之外, 一般不该直接使用这个 class.

  * ``TestCase``. 适合需要访问数据库时, 保证数据库状态一致性, 单元测试和集成测
    试.

  * ``LiveServerTestCase``, ``StaticLiveServerTestCase``. 因开启 server, 适合功
    能测试.

- 区分清晰哪部分属于 SUT, 哪部分属于外部依赖, 这样才能确定什么东西是需要 mock
  掉的. 例如, 在一个功能中, 不仅仅 form 层是 view 层的依赖; 在 view 层代码中,
  django generic view class 同样也是 业务逻辑 view class 的依赖.

- Don't test django code, test only your logic.
  
  * 例如, 设置了 ``template_name`` 之后, 加载 template 的整个逻辑是 django
    framework 提供的, 与你无关. 因此无需写测试去测试是否加载了正确的模板文件.

- Don't test constants. 例如, 没必要测试一个 ModelForm 中设置的 model class
  是否正确.

- mock only the relevant APIs, not any more. 例如, 在 form 只会调用 Model.save,
  就不要 mock 整个 Model, 而是 Model.save.

- integration test 时才使用 django 的那些跨越多个模块层的工具, 写单元测试时
  不要使用.

- 单元测试时, 可以设置 ``LANGUAGE_CODE`` 为默认的 ``en-us``. 这样便于测试
  一些字符串相关的输出情况.

- 如何提高 django 单元测试的执行速度.

  * 数据库方面.
    
    1) 如果没有使用 database-specific features, 例如 django 的
    ``django.contrib.postgres`` package, django-mysql, 则可以在测试时替换
    为使用 sqlite. 这有很大的速度提升. 这是因为首先 sqlite overhead is low,
    其次 django 在内存中创建 sqlite 测试库. 但如果使用了与数据库相关的功能,
    这个方法就不太可行了.

    2) 如果必须使用 mysql, postgres 等 full-feature 数据库, 且可能需要访问
    数据库, 使用 ``--keepdb`` option 仍然可以极大地提高单元测试效率. 事实上,
    与 ``--keepdb`` 相比, 完全 skip database setup 并不能提高多少速度.

  * 单元测试书写方面.

    1) 在保证隔离的单元测试中, 若不需要访问数据库, 可以完全 skip database
    setup.  例如通过自定义 test runner, override ``setup_databases``,
    ``teardown_databases``. See `snippets/browser_test_runner.py`.

    2) 在保证隔离的单元测试中, 若不需要访问数据库, 可以使用 SimpleTestCase, 或
    者 unittest.TestCase. 由于避免了 fixture setup, db transaction management
    等 overheads, 这样可以提高数倍的单元测试执行效率.

  * run tests in parallel. 但这不一定可靠. See `management commands`_ for
    detail.

- 关于对模板和页面的测试.
  
  * 对 template 的测试, 很难做到去将依赖项剥离, 去独立测试 template rendering.
    这是因为所有依赖项都需要在模板中去使用. 而模板渲染结果本身又完全是前端内容,
    所以模板渲染的测试不需要进行单独的单元测试或集成测试, 而是在功能测试中进行.

  * 对页面的 FT 不要测试 style, 而要测试功能. 只需保证基本的页面元素和样式是否
    加载即可. Avoid brittle tests.

  * 对于 template tags/filters 等的测试则可以做到 UT, 例如通过构建 minimal
    template example.

- 如何单元测试 ``ModelForm``?

  * 只测试你自己的 customization.

  * 无需 mock model. 在 TDD 时, 只需要写一个 placeholder model 在那里放着
    让 ModelForm 使用即可.

  * 但别忘了在集成测试时要覆盖到对 modelform 整体逻辑的测试.

  * see also: [SODjModelFormTDD]_

- about testing schema migrations and data migrations.

  * 一般情况下不需要单独测试. 在执行 ``test`` management command 时就自动测试了.

  * migration 基于数据库和数据的一定历史状态, 也难以保证在软件的生命周期中始终
    能够测试通过.

  * 也许对一些复杂的 data migration 的 (不依赖于某个历史状态的) 局部逻辑可能
    需要单元测试.

- 对 management commands 进行功能测试.

  * 使用 ``call_command()``

  * 将输出转入 in-memory file-like object, e.g., StringIO.

- 在 web app 的功能性测试中, 一般需要浏览器. 常见的处理方法是在每个 test class
  的 setup/teardown 中打开和关闭浏览器. 这带来的问题是太慢了. 我这里写了一个
  test runner 在 setup/teardown test environment 时打开和关闭浏览器.
  `code <snippets/browser_test_runner.py>`_

- 如果在 FT 中需要 mock 掉外部依赖, 必须使用 LiveServerTestCase (and
  subclasses).

- 关于 QuerySet. 当模块中使用到 queryset 以及其他 django db 层的方法时, 这些全
  部是你的模块与 django 逻辑的集成点, 也是代码逻辑与数据库的集成点. 因此, 在模
  块设计中, 需要构造一些方法, 将这些集成点封装起来. 将集成的面缩小至最小, 隐藏
  细节. 这样不但是更好的设计, 更可读的代码, 也更容易进行单元测试. 只需在 UT 中
  mock 这些封装的集成点即可.

System check
============
overview
--------
- A set of static checks for validating Django projects.

- It detects problems and provides hints for how to fix them.

- When the system checks are run:

  * explicitly by checking command ``./manage.py check``.

  * implicitly when the management command's ``require_system_checks=True``,
    which is the default.

  这些是在 ``BaseCommand.check()`` 中实现的.

writing system checks
---------------------
- A check is a callable with the following formal parameters:

  * ``app_configs``. A list of applications that should be inspected. If None,
    the check must be run on all installed apps in the project.

  * ``**kwargs``. not used.

  It returns a list of CheckMessage instances, each representing an found
  issue, if no issue is found, returns [].

- Register the callable to the global CheckRegistry.::

    @register(label1, ...)
    def check(app_configs, **kwargs):
        return issues

  ``register`` decorator is ``CheckRegistry.register()`` method.

- Put system checking codes in ``<app_label>/checks.py``, running system check
  registration in ``AppConfig.ready()`` method (when app is loaded).

check registry
--------------
- ``django.core.checks.registry.CheckRegistry``

methods
"""""""
- ``register(check=None, *tags, deploy=False)``. register a check.  ``check``
  can be the check callable, or just another tag in which case the method is
  used as a decorator. ``deploy`` define whether this is a deployment check.

check messages
--------------
- all check messages are instances of CheckMessage class.

- Messages are tagged with a level indicating the severity of the message.

- builtin message levels: DEBUG, INFO, WARNING, ERROR, CRITICAL. Defined in
  django.core.checks.messages.

- builtin CheckMessage subclasses: Debug, Info, Warning, Error, Critical.

CheckMessage
^^^^^^^^^^^^
constructor
"""""""""""
- level. message level. a int level number, probably one of the predefined
  values.

- msg. describing the problem, in less than 80 chars. Should not contain
  newlines.

- ``hint=None``. a hint for fixing the problem. no newline. If no hint can be
  provided, or the hint is self-evident from the error message, the hint can be
  omitted.

- ``obj=None``. An object providing context for the message (for example, the
  model where the problem was discovered). Anything that defines a string
  representation.

- ``id=None``. A unique identifier for the issue. Identifiers should follow the
  pattern ``<app_label>.XNNN``, where X is one of the letters CEWID, indicating
  the message severity. The number should be unique within the application.

methods
"""""""
- ``__eq__(other)``. Message instances are comparable. They are equal when
  their level, msg, hint, obj, id are all equal. This makes testing easier.

check tags
----------
- tags allow only a category of checks to be run.

- The bulitin tags are defined as enum: ``django.core.checks.registry.Tags``.
  See https://docs.djangoproject.com/en/stable/ref/checks/#builtin-tags for
  explanations.

  * database. Database checks are not run by default because they do more than
    static code analysis as regular checks do. They are only run by the
    ``migrate`` command or if you specify the ``database`` tag when calling the
    check command.

deployment checks
-----------------
- deployment checks are only run when ``check --deploy`` is used.

- deployment checks is meant to check only issues regarding deployment
  environment/settings, etc, which is not universally applicable to any stage
  of development, just specific to production.

- 它们与普通的 checks 是分开成两组的.

builtin checks
--------------
- See https://docs.djangoproject.com/en/stable/ref/checks/ for a list of
  builtin checks.

model checks
^^^^^^^^^^^^
- Call ``Model.check()`` classmethod, performing all range of checks regarding
  models/fields/managers, etc.

management commands
-------------------
check
^^^^^
::

  ./manage.py check [app_label]...

- If app labels are specified, only those apps are checked. By default all apps
  are checked.

- ``--tag TAG``. only checks belonging to TAG are checked. can specify multiple
  times.

- ``--list-tags``. list all tags.

- ``--deploy``. activate additional deployment-only checks.

- ``--fail-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}``. consider issues of the
  specified level or higher to be serious, and causing check to fail. default
  is ERROR.

django-admin
============
CLI usage
---------
::

  {django-admin | ./manage.py} subcommand [options] [args]

- common options.

- 对于 ``django-admin``, 若要加载 project-specific commands,
  需要设置::

    --settings=<import-path> --pythonpath=$PWD

  否则 django 无法初始化 project.

writing management commands
---------------------------
对于某个 app, 创建 management commands 的方式:

- 创建 ``<app>/management/commands`` 目录, 创建必要的 ``__init__.py``
  各层成为 package.

- 对每个 management command, 创建以命令名作为 module name 的 submodule.
  ``commands/`` 目录下的 private module (starts with ``_``) 不会认为是
  command module.

- 每个 module 内包含一个 ``Command`` class, 它是 ``BaseCommand`` 的
  subclass.
  
- 实现 ``handle()`` method 进行所需操作. 错误信息通过 ``CommandError`` raise
  出来.

- 实现 ``add_arguments()`` method 添加命令行参数.

execution logic
----------------
执行 management 命令时的基本步骤:

- ``django-admin`` 和 ``manage.py`` 执行 ``execute_from_command_line()``,
  实例化 ``ManagementUnity``.

- ``ManagementUnity`` 配置项目, 加载所有 commands. 加载并实例化指定的
  management ``BaseCommand`` subclass. 将命令行参数传递给它.

- ``BaseCommand`` 构建 ArgumentParser 以及命令行. 解释传入的命令行参数.
  最终调用 ``handle()`` 执行所需操作.

commands
--------

command loading prcedence.

``INSTALLED_APPS`` + ``django.core.management``, 越靠前的优先级越高.

django.core.management
^^^^^^^^^^^^^^^^^^^^^^

* ``shell`` 启动 shell 并加载项目相关 django 配置; 这相当于
  执行了:

  .. code:: python

    os.environ['DJANGO_SETTINGS_MODULE'] = "<project>.settings"
    import django; django.setup()

* ``makemigrations``. Make new migration files. See `migration`_.

* ``dbshell``

  似乎不会使用平时 django 运行时传入的 OPTIONS 参数.

* ``migrate``. Update database schema with migration files. See `migration`_.

* ``inspectdb``. 根据数据库 schema 反向推导生成与之匹配的 model code.
  通过分析 mysql's builtin ``information_schema`` database.

* ``test``. Run unit tests. See `unit testing`_.

* ``dumpdata``. Dump database data of django apps in serialized format.
  See `Serialization`_.

django.contrib.sessions
^^^^^^^^^^^^^^^^^^^^^^^

* ``clearsessions`` 清除过期的 session data. django 不提供自动清理
  session 的机制. 可以定期执行这个命令手动清除过期的 session.

django.contrib.staticfiles
^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``runserver``.

  对于 runserver 输出的请求相应日志, 每一行是在该请求结束后才输出, 因此
  才记录有 method, url, http version, status code 等信息.

output colorscheme
------------------

palette
^^^^^^^
- pre-defined: dark, light, nocolor.

- ``DJANGO_COLORS`` environ 设置 color palette. default is dark. format::

    [<palette>][;role=<fg>[/<bg>][,<option>[,<option>,...]][;role=...]]

  * if palette is omitted, use nocolor.

  * every role spec after palette is a customization based on palette.

- roles: see https://docs.djangoproject.com/en/2.0/ref/django-admin/#extra-niceties

- fg, bg colors: black , red , green , yellow , blue , magenta , cyan , white 

- options: bold , underscore , blink , reverse , conceal


API
---

Core functionality resides in ``django.core.management``.

module-level functions
^^^^^^^^^^^^^^^^^^^^^^
- ``call_command(name, *args, **options)``. call management command
  programmatically.
  
  * ``name``. a command name string or a command object.
    
  * ``*args``. commadline argument list. 

  * ``**options``. Command line option and ``stealth_options`` in kwarg form.
    这部分相当于不通过 parser 解析, 直接传入 ``BaseCommand.execute()``, 应该符
    合 ``parse_args()`` 输出格式. 这里可以传入任何 ``execute()`` method 支持的
    额外参数, 例如 stdout, stderr 等.

command class
^^^^^^^^^^^^^
BaseCommand
""""""""""""
``django.core.management.BaseCommand``: base class of all management commands.

options
~~~~~~~
- ``help``. command description. default empty string.

- ``missing_args_message``. 对于 subcommand 定义了 required positionals 时,
  若未提供, 输出该信息, 而不是 argparse 默认的一般化信息.

- ``output_transaction``. 若 ``handle()`` 返回一组 sql, 设置作为 transaction
  自动添加 BEGIN/END. default False.

- ``require_migrations_checks``. 检查 migration files 是否与数据库中的历史一致.
  default False.

- ``require_system_checks``. django system checking. default True.

- ``leave_locale_alone``.

- ``base_stealth_options``. a tuple of common stealth options. including:
  ``skip_checks``, ``stdout``, ``stderr``.

- ``stealth_options``. 一组不在 management command line 定义的 options. 它们用
  于在 ``call_command()`` 时传递一些额外的参数. 例如 stdout/stderr redirection.

attributes
~~~~~~~~~~
- ``style``. output colorscheme ``Style`` definitions instance. attribute
  names are uppercased palette role name. attribute values are corresponding
  ``colorize()`` function.

- ``stdout``, ``stderr``. command's stdout, stderr. 使用这个进行输出, 以保证
  符合 Command instance's redirection 配置, 并便于测试.

  stdout/stderr is instance of ``OutputWrapper``. ``write()`` method 会自动
  添加 line ending, 如果输入没有提供的话.

methods
~~~~~~~
- ``add_arguments(parser)``. 添加自定义的命令行参数. parse 是 ArgumentParser.

- ``get_version()``. default return django version. can be overrided to provide
  command version.

- ``execute(*args, **options)``. execute command with parsed arguments. 
  ``args`` is mostly useless.

  * ``stdout``, ``stderr`` options 可进行 redirection.

  * ``skip_checks`` 便于在 programmatically 执行 management command 使用, 此时
    无需再进行执行 system checks.

- ``handle(*args, **options)``. main execution logic. return value is printed
  to stdout. returned output 应该用于输出某种执行结果数据. 对于过程中的 generic
  output 直接写入 ``self.stdout``, ``self.stderr`` streams 即可.

- ``check(app_configs=None, tags=None, display_num_errors=False,
  include_deployment_checks=False, fail_level=checks.ERROR)``.
  Run system checks. If any CheckMessage has a level equal or higher than
  ``fail_level`` and not silenced, the SystemCheckError is raised, therefore
  the command exits with a non-zero status.

- ``check_migrations()``. migration check.

- ``run_from_argv()``. cmdline execution entrypoint. create parser, parse args
  and call ``execute()``. Raised ``CommandError`` will be printed to stderr
  then exiting with status code 1.

- ``create_parser()``.

exceptions
^^^^^^^^^^
CommandError
""""""""""""
If this exception is raised during the execution of a management command from a
command line console, it will be caught and turned into a nicely-printed error
message to the appropriate output stream (i.e., stderr); as a result, raising
this exception (with a sensible description of the error) is the preferred way
to indicate that something has gone wrong in the execution of a command.

bash completion
---------------
django source repo 里提供了 bash completion script.

plugins
=======
reusable django packages 可以从 django packages 网站查询. 这个网站的好处是,
对于一个 package, 它上面有详细信息, 包含版本支持情况, 最近更新时间, 有多少
人在使用, 以及同类 packages 之间的比较 grid.

django-nested-admin
-------------------

django-mysql
------------

system checks
^^^^^^^^^^^^^
Strict Mode
"""""""""""

- mysql strict mode check: django_mysql.W001

InnoDB Strict Mode
""""""""""""""""""

- InnoDB strict mode check: django_mysql.W002

utf8mb4
"""""""

- system check id: ``django_mysql.W003``

- utf8mb4 charset check.

queryset extensions
^^^^^^^^^^^^^^^^^^^

- QuerySet extension 可以从不同角度使用.

  * 若原来使用的 ``django.db.models.Model`` 作为父类, 可以替换使用
    ``django_mysql.models.Model``.  该类设置了 ``objects`` manager 使用
    ``django_mysql.models.QuerySet.as_manager()``.

  * 若使用了自定义的 parent model class, 可以不修改 model 原来的父类,
    直接设置 ``objects`` 或其他 default manager 为
    ``django_mysql.models.QuerySet.as_manager()``.

  * 若使用了 custom QuerySet class, 可继承 ``django_mysql.models.QuerySetMixin``,
    添加所需功能.

  * 使用 ``add_QuerySetMixin()`` 对某个 QuerySet instance 单独 override
    ``__class__`` attribute, 返回一个添加了 ``QuerySetMixin`` 方法的新的
    queryset (不修改传入的 queryset). 这种动态修改 class 的方式, 完全不推荐,
    需小心使用.

more model fields
^^^^^^^^^^^^^^^^^

JSONField
"""""""""
- 使用 mysql JSON data type.

- MySQL 5.7+ 可用.

- 其值可以是任何 valid json value 的 python equivalent. 只要能够 ``json.dumps()``.

- additional constructor options.

  * default. 注意默认的 default 值是 ``dict`` function. 如需要其他值比如 NULL
    需明确设置.
    
    Incorrectly using a mutable object, creates a single object that is shared
    between all instances of the field. 此时应该使用 callable that returns the
    mutable objects.

- additional checkings.

  * check ``default`` is not mutable container object. 因为会共享.

  * check mysql version.

- field lookups.

  * Most of the standard lookups don’t make sense for JSONField and so have
    been made to fail with NotImplementedError.

  * In cases where names collide with existing lookups, or not achievable
    via field lookup syntax, use the ``JSONExtract`` database function.

  * exact match, in standard form (``field=b``, ``field__exact=b``)

  * ordering, in standard form (gt, gte, lt, lte lookups), conforming to
    mysql's JSON ordering definition.

  * path lookup:
    
    - key: ``field__key__subkey``

    - array index: ``field__<N>``

    可以多层叠加.

  * key presence lookups:

    - has key: ``field__has_key``

    - has all keys: ``field__has_keys=[...]``

    - has any keys (has at least one of key list): ``field_has_any_keys=[...]``

  * length lookups (``JSON_LENGTH`` function):
    
    - ``field__length``

    - ``field__length__<ordering>``

  * containment lookups (``JSON_CONTAINS`` function):

    - ``field__contains``

    - ``field__contained_by``

EnumField
""""""""""
- 使用 mysql ENUM data type.

- 这是 CharField 子类.

- options.

  * choices. required. 除了 django model field 标准的 ``choices`` 参数
    格式之外, 支持 a list of strings. 此时, 选项值与显示形式相同.

  * 虽是 CharField 子类, 但不允许 ``max_length``. 将 max length 的检查
    交给 mysql. mysql 会检查 enum 的元素个数以及每个元素的长度是否超过
    上限.

- 允许 append new choices. 允许 modify human readable form of existing
  choices. 但 MySQL 不允许 modifying value of existing choices.

Bit1BooleanField
""""""""""""""""
- BooleanField subclass.

- use mysql BIT(1) data type for boolean data.

NullBit1BooleanField
""""""""""""""""""""

- NullBooleanField subclass.

extra field lookups
^^^^^^^^^^^^^^^^^^^

JSON field lookups
""""""""""""""""""

django-auth-ldap
----------------

添加一个 LDAPBackend 即可. 不需要单独的 middleware. 所以在 LDAP 认证之后,
登录状态与平时一样, 通过 session + AuthenticationMiddleware 维持.

authentication
^^^^^^^^^^^^^^
authentication methods.

1. Search/bind.
   Connecting to the LDAP server either anonymously or with a fixed account and
   searching for the distinguished name of the authenticating user. Then we can
   attempt to bind again with the user’s password.

2. Direct bind.
   Derive the user’s DN from his username and attempt to bind as the user
   directly.

user
^^^^
``LDAPBackend.authenticate()`` 在认证成功后会建立对应的 django 用户. 然后,

- 根据配置的 DN entry attributes 更新 user model fields.

- 执行 ``populate_user`` signal handlers, 进行任意的自定义修改.

- 根据 ldap 里组的情况, 设置用户和组的 M2M 关系.

对应的 django user 会设置 unusable password.

settings
^^^^^^^^
- config prefix. 默认为 ``AUTH_LDAP_``. LDAPBackend subclass can override this.
  When several LDAP backend co-exist and operate independently, each of them
  may need a different prefix.

- ``AUTH_LDAP_SERVER_URI``

- ``AUTH_LDAP_START_TLS``. LDAP 使用 StartTLS extension 做加密连接. 

- ``AUTH_LDAP_BIND_DN``, ``AUTH_LDAP_BIND_PASSWORD``.
  访问 ldap 使用的 Distinguished Name & password.
  
  默认为空, 为 anonymous bind.

  无论使用 search/bind 或 direct bind 进行用户认证, 这两个选项都是需要的. 因为
  访问 ldap 可进行的操作不仅仅是认证, 这里设置的 DN 是用于任何 ldap 操作的 DN.

- 用户认证方式.

  * ``AUTH_LDAP_USER_SEARCH``.
    对于 search/bind, 需要设置对认证用户的搜索范围和 pattern 等信息.
    
  * ``AUTH_LDAP_USER_DN_TEMPLATE``.
    对于 direct bind, 需要设置要认证的用户 DN 的模板.

- ``AUTH_LDAP_PERMIT_EMPTY_PASSWORD``.
  是否允许待认证用户有空密码.

- ``AUTH_LDAP_BIND_AS_AUTHENTICATING_USER``.
  是否 bind as authenticating user, 这样避免在 connecting user & authenticating
  user 之间来回切换, 即反复 bind 不同用户.
  
  the LDAP connection would be bound as the authenticating user during login
  requests and as the default credentials during other requests, so you might
  see inconsistent LDAP attributes depending on the nature of the Django view.

- ``AUTH_LDAP_USER_ATTR_MAP``.
  LDAP attribute 至 user model fields 的映射.

django-environ
--------------
overview
^^^^^^^^
- usage: parse environ and env file to fill configuration files.

- 为什么需要这么做:
  
  * 这是为了将配置文件模板化, 当我们需要部署多个实例, 而每个实例的配置值可能不
    尽相同时, 每个实例只需修改抽象出来的配置值, 而不需要维护一个自定义的配置文
    件.

  * 由于 settings 是 python source, 其中的配置具有复杂的结构, 如果不用 env file
    and environ, 只用 local settings file, 当需要修改复杂配置项例如 ``DATABASES``
    中的某个具体子项的值时, 需要复杂的操作. 模板化则修改起来很简单.

- features.

  * read env file.

  * read environ.

  * value casting with predefined types and formats.

- inspired by 12factor app.

env file format
^^^^^^^^^^^^^^^
- basic shell variable format, 支持 single/double quotes for value.

- support ``$var`` for referencing another variable.

environ.Env
^^^^^^^^^^^
- encapsulate getting environment variables.

- 所有 Env 实例共享一份环境变量, 即 ``os.environ``.

- basic usage.

  * configuration scheme 可以在 ``Env`` 初始化时一次性指定, 或者获取配置值时
    分别指定.

  * read env file: ``Env.read_env()``

- ``cast`` 参数值和对应的环境变量形式:

  * str. specify string.

  * bytes, convert to string then encode to bytes.

  * bool, True in string form: true, on, ok, y, yes, 1. otherwise False.

  * int. any string that is legal for ``int()``.

  * float. any string that is legal for ``float()``.

  * json. any string taht is legal for ``json.loads()``

  * list. value format: ``a,b,c``

  * tuple. value format: ``(a,b,c)``

  * dict. value format: ``key=val,key=val``

  * 另一种更细致的 dict 转换形式: cast 参数值为::
    
      {"key": <cast>, "value": <cast>, "cast": {"key": <cast>, ...}}
     
    value format::

      key=val;key=val

    外层的 ``key`` 值表达的是将各个字段的 key 进行统一使用指定的 ``<cast>`` 形
    式; 外层的 ``value`` 值表达的是各个字段转换的 fallback 类型.  外层的
    ``cast`` key 的值是一个 dict, 里面的 keys 是原始形式中的各个 key 字段名, 其
    值是要对相应 value 进行转换的类型, 若没有指定, 则 fallback 至外层指定的
    value 类型.

  * url. parsed by urlparse.

  * path. 转换成 ``environ.Path``. value format is string.

  * ``db_url``.

  * ``cache_url``

  * ``search_url``

  * ``email_url``

- If the key is not available in environ, raise ImproperlyConfigured.

constructor
"""""""""""
- ``**scheme``. 设置配置项的 scheme. a scheme is a tuple of
  ``(cast, default)``.

methods
"""""""
- ``__call__(var, cast=None, default=NOTSET, parse_default=False)``.
  获取环境变量值. ``parse_default`` 则 default 也会被 cast.

- ``__contains__(var)``. key in environ.

- ``read_env(env_file=None, **overrides)``. if ``env_file`` is None,
  try to read ``.env`` at project root. ``overrides`` overrides value
  in env file.

- ``str()``

- ``bytes()``

- ``bool()``

- ``int()``

- ``float()``

- ``json()``

- ``list()``

- ``tuple()``

- ``dict()``

- ``url()``

- ``db_url()``

- ``cache_url()``

- ``email_url()``

- ``search_url()``

- ``path()``

Path
^^^^

- convenient file paths handling in settings.

- If path is required but not physically exists, raise ImproperlyConfigured.

constructor
""""""""""""
- ``start=""``. default current directory. The starting part of Path.

- ``is_file=False``. whether ``start`` is a file or directory, if it is a file, 
  resolve to its parent directory.

- ``required=False``. whether the path is required to exist physically.

methods
""""""""
- ``__call__(*paths, **kwargs)``. get path in string, with ``paths`` appended.

- ``path(*paths, **kwargs)``. new path from current path.

- ``file(name, *args, **kwargs)``. open file, ``name`` is relative to
  current path. args, kwargs are passed to ``open``.

- ``__add__(other)`` append path.

- ``__sub__(other)``. If string, subtract trailing path from current path;
  if int, go up that many levels.

- ``__invert__()``. go up one level (``~Path``).

- ``__contains__(item)``. whether item is current path's subpath.

- ``__fspath__()``. os.PathLike object interface.

django-stubs
------------
- provide pep484 type annotation stub files for django framework.

References
==========
.. [SODjTemplateDebug] `Django debug display all variables of a page <https://stackoverflow.com/a/21205925/1602266>`_
.. [SODjSettings] `How to manage local vs production settings in Django? <https://stackoverflow.com/questions/1626326/how-to-manage-local-vs-production-settings-in-django>`_
.. [SODjModelFormTDD] `TDD in Django, how to unit test my modelform? <https://stackoverflow.com/questions/51763138/tdd-in-django-how-to-unit-test-my-modelform/51781735#51781735>`_
.. [SODjSignalWeakRef] `Why does Django's signal handling use weak references for callbacks by default? <https://stackoverflow.com/questions/1110668/why-does-djangos-signal-handling-use-weak-references-for-callbacks-by-default>`_
