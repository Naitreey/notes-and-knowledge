- django term: project vs app.

  一个 project 就是一个 project, 一个项目. 一个项目可以是一个组相互关联的事物、
  事情和功能的集合, 它们构成一个抽象整体.

  一个 app 就是这个 project 中的一件事情, 一个功能, 一个模块等. 它可以单独存在,
  具有自洽的逻辑和组成. 也可以是更大整体 (即 project) 的组成部分.

  注意适当地按模块化思路将 project 拆成 apps. Your apps don't have to be reusable,
  they can depend on each other, but they should do one thing.

  Try to answer question: "What does my application do?". If you cannot answer
  in a single sentence, then maybe you can split it into several apps with cleaner
  logic.

  对于仅有一个功能模块的项目, 可以简单地将 project 直接应用为 app.

- app

  * In essence, a Django application is just a Python package that is specifically
    intended for use in a Django project.

  * django 提供了很多方便的功能使得 project 在 app 尺度的模块化十分容易, 例如
    模块化的 URLconf, ``include()``. 每个 app 可以独立存在, 又可以在整个项目中
    plug-and-play (PnP). 与 app 模块化配合的是 RESTful url 的模块化, 并要求
    url 层级清晰. 每个 app 的 URLconf 自成体系, 有 index, 有 object, 有 method.

  * 理想情况下, app 应该可以独立发布成 python package. 然后在任何 django 项目
    中按照标准 django 方式 (import 等) 即可使用, 成为新项目的一个 app.

  * It’s often useful to prepend ``django-`` to your module name when creating
    a package to distribute. This helps others looking for Django apps identify
    your app as Django specific.

  * 若需要在代码中获取当前安装的 django apps, 应该使用 ``django.apps.apps``
    application registry, 而不是直接访问 ``settings.INSTALLED_APPS``.

- project

  * 由于 django 设计的 project 代码 import 逻辑 -- 即 project 目录需要在 ``sys.path``
    中, 导致 django project 不适合整个打包为 python package 然后用 pip 安装至
    site-packages 目录. 因为这样的效果是在 ``sys.path`` 中包含 site-packages 的子目录.
    结果就是 import 时可能存在覆盖问题.

    整个 django project 适合打包成 rpm/deb, 放在 ``/usr/lib`` 下.

    然而, 一个 django project 中的每个 app, 都应该可以打包成 python package 用 pip
    安装.

  * project 目录可以作为一个全局 app 来使用. 全局的模板, 全局的静态文件, 全局的 url,
    全局的管理命令等, 都可以放在这个全局 app 中.

- URLconf

  * URLconf 中的 url pattern 在载入时就都编译好了, 所以是高效的.

  * 每个 app 的 URLconf 中应该包含 ``app_name``, 即它是 url name 的 namespace.
    可避免不同 app 的 url name 相互覆盖.

- 日期时间使用 django.utils.timezone 里的函数, 它们会自动根据 settings.py 里的时间
  相关设置来返回恰当的结果. 直接使用 datetime module 还需要去手动读取配置.

- model

  * model 是一个数据对象类型, 它是数据库表的抽象. 或者从另一个角度来看, 由于 model
    的存在, 要求数据库表应该按照 object-oriented 的方式进行设计. 而一个 entry 就是
    一个 instance. 这是一种比较好的设计思路.

  * model 定义时 field 以 class attribute 方式去定义, 而实例化后, 每个实例会
    生成同名的 attribute 在自己的 ``__dict__`` 中, 覆盖 class attribute.

- view

  * view 这个概念没有什么很好的意义. 应该说, 从一定程度上, HTTP 的请求可以看作是
    对整个 app 的不同视角 (view), 但这种说法有些牵强. 总之, views 就是对 url
    请求的 server 端实现.

  * 每个 view 都必须返回 HttpResponse instance 或者 raise some exception. 任何其他
    结果 django 都认为是有问题的.

  * class-based views 相对于 function-based views 的一些好处

    - Organization of code related to specific HTTP methods (GET, POST, etc.) can
      be addressed by separate methods instead of conditional branching.

    - Object oriented techniques such as mixins (multiple inheritance) can be used
      to factor code into reusable components.

  * Class-based views have an ``as_view()`` class method which returns a function that
    can be called when a request arrives for a URL matching the associated pattern.
    The function creates an instance of the class and calls its ``dispatch()`` method.
    ``dispatch`` looks at the request to determine whether it is a GET, POST, etc, and
    relays the request to a matching method if one is defined, or raises
    ``HttpResponseNotAllowed`` if not.

- template

  * template namespace. 每个 app 下可以有 ``templates/`` 目录, 不同 app 的 templates 目录
    在一个 namespace 中, 因此会相互覆盖. 所以需要再创建 ``templates/<app>`` 子目录.

  * template 中 object 的 ``.`` operator 的查找顺序:
    dict key, object attribute, list index.

  * 在 template 中使用 symbolic url, 即使用 url 的名字, 而不写死 url 路径在模板中.
    这样可以降低 template 和 URLconf 之间的耦合. 在重构 url 结构时, 不需要修改模板
    文件.

  * 模板的搜索顺序:

    - ``DIRS`` in ``settings.py``.

    - 若 ``APP_DIRS == True``, 每个 app 目录下的 ``templates/`` 目录.

- static file

  * static file namespace 与 template namespace 机制类似.

  * static file 的 url 是自动生成的, 以 static file namespace 为 url root.

  * 在源代码层面上, app 的静态文件和它的代码在一起, 模块化更好;
    在开发时, 使用 builtin server 即可 serve 各个 app 下的静态文件.

  * 在项目部署时, 执行 ``collectstatic`` 将静态文件集合在一起放在 ``STATIC_ROOT``,
    使用 nginx 来高效地 serve 静态文件.

- test

  * model 层的 test 的测试点是测试 model 的正确性、合理性;
    view 层的 test (配合 urlconf) 测试的是操作是否符合预期.
    因此前者手动操作数据库, 而后者模仿 useragent 用 client.

  * 每个 test method 执行结束后数据库状态都会被重置.

- 全局性质的 (属于整个 project 而不属于某个 app 的) templates 和 static files 应该放在
  ``$BASE_DIR/<project-name>/{templates,static}``.

- admin site

  * model 里各个 field 的名字和类型直接影响它们在 admin.site 的显示和交互方式.

  * 每个 model 在 admin site 中的显示方式可通过 ``admin.ModelAdmin`` 自定义.

  * admin site app 是 ``django.contrib.admin``, 它依赖于 ``django.contrib.auth``,
    ``django.contrib.contenttypes``, ``django.contrib.messages``,
    ``django.contrib.sessions``.

- settings

  * NEVER deploy a site into production with ``DEBUG`` turned on.

  * In debug mode, ``ALLOWED_HOSTS == []`` 时, 只允许一些本地 ``HOST`` header,
    localhost, 127.0.0.1, ::1.

  * ``UST_TZ`` determines whether datetime objects are naive.

- django-admin

  * ``./manage.py shell`` 会在启动解释器后设置一些项目相关项; 若想不用这个命令行
    但初始化同样的项目配置, 可以这样:

      .. code:: python

        os.environ['DJANGO_SETTINGS_MODULE'] = "<project>.settings"
        import django; django.setup()

- migration

  * You should think of migrations as a version control system for your
    database schema. ``makemigrations`` is responsible for packaging up
    your model changes into individual migration files - analogous to
    commits - and ``migrate`` is responsible for applying those to your
    database.

    Make changes to your models - say, add a field and remove a model -
    and then run ``makemigrations``. Your models will be scanned and
    compared to the versions currently contained in your migration files,
    and then a new set of migrations will be written out.

    Once the migration is applied correctly to test database, commit the
    migration and the models change to your version control system as a
    single commit.
