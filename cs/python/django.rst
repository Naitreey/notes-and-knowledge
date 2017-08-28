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

  * primary key:

    可以用 ``primary_key=True`` 设置某个 field 为 primary key, 否则 django 自动
    给 model 添加 id field 作为 primary key

    .. code:: python
      id = models.AutoField(primary_key=True)

   The primary key field is read-only. If you change the value of the primary key
   on an existing object and then save it, a new object will be created alongside
   the old one.

  * model 定义时 field 以 class attribute 方式去定义, 而实例化后, 每个实例会
    生成同名的 attribute 在自己的 ``__dict__`` 中, 覆盖 class attribute.

  * 对于 class namespace 中的各个属性, 只有 ``django.db.models.Field`` 的实例
    才会认为是 model field. 其他属性实际上可以随意设置.

  * field options.

    - ``null`` 默认是 False, 所以 create table 时有 ``NOT NULL``.

    - ``null`` 是规定数据库中 empty value 是否存储为 NULL 值;
      ``blank`` 是规定 form validation 时是否允许空值.
      两者的意义是不同的.

    - Given a model instance, the display value for a choices field can be accessed
      using the ``get_FOO_display()`` method.

    - 如果一个 model 包含多个与同一个其他 model 建立的 ``ManyToManyField``, 需要设置
      ``related_name`` 以保证反向的查询没有歧义.

  * many-to-one field.

    - 多对一的映射关系用 ``django.db.models.ForeignKey`` 实现.

    - foreign key field 的名字应该是所指向的 model 的名字的全小写版本.

  * many-to-many field.

    - 由于一个列无法体现多对多的关系, ``ManyToManyField`` 在实现时, 不是构成了一个列,
      而是一个单独的 table. table 中包含 many-to-many 关系的两种模型数据的行 id.

    - It doesn’t matter which model has the ``ManyToManyField``, but you should only
      put it in one of the models – not both. ``ManyToManyField`` 应该放在那个编辑
      起来更自然的 model 中, 也就是说, 从哪个方向建立多对多映射关系更自然, 就把它
      放在哪个 model 中.

    - many-to-many field 的名字应该是一个复数类型的名字, 以表示多个的概念.
      同样的, ``related_name`` ``related_query_name`` 也应该是表示反向关系的
      复数.

    - intermediate model. 若多对多的关系不仅仅是一个简单双向的关系, 而需要包含
      一些其他状态信息, 则需要使用一个中间模型去承载这个多对多关系.

  * one-to-one field.

    - 一对一关系一般用于一个模型作为另一个模型的延伸、扩展、附加属性等.
      ``OneToOneField`` 在 model 继承时用于定义父表和子表通过哪一列来关联.

  * 通过 ``Meta`` inner class 定义来定义 model 的 metadata.

  * Model object managers (like ``.objects``) are only accessible via model classes,
    not the model instances.

  * 定义 ``__str__`` method 给模型的实例一个有意义的表现形式.

  * 注意 ``Meta.verbose_name`` 和 ``__str__`` 的区别. 前者是模型本身的 verbose name,
    后者是 model instance 的字符串表现形式.

  * inheritance.

    - 使用 ``Meta.abstract = True`` 定义 ABC model.

    - ABC model 的子类的自己的 ``Meta`` attribue 自动设置 ``abstract = False``.
      若子类 model 仍需是 ABC, 需要再设置.

    - 仔细想想, 非 ABC model 在继承时, 子类 model 表中只保存那些扩展的信息, 继承的
      信息都保留在父类表中. 这个设计实际上才是合理的. 因为子类的实例也是父类的实例,
      我们可以从子类实例中抽出纯父类实例那部分 (例如通过 ``super``). 我们把这种继承
      和实例化的思路应用在 ORM 上, 就得到了父类 model 的数据集显然是应该包含子类
      model 的数据集的 (抽出公有部分). 所以子类表只存扩展字段即可, 通过 one-to-one
      field 与存在父类表中的基础数据对应, 两部分数据构成一个完整的子类实例.

    - proxy model 不修改 model, 而是修改对 model 数据的操作. 因此 model 和它的
      proxy model 共享所有数据集. The whole point of proxy objects is that code
      relying on the original Person will use those and your own code can use
      the extensions you included (that no other code is relying on anyway).

    - multiple inheritance. The main use-case where this is useful is for “mix-in”
      classes: adding a particular extra field or method to every class that inherits
      the mix-in.

    - 若 model 继承时不是继承的 ABC model, 而是实体 model, 则子类的 field 不能
      和父类的 field 重名, 即 field attribute can not be overrided. 这与一般的
      python 类不同. 这是因为 model instance 实际上是数据库表 entry 的抽象,
      如果重名, 在获取属性即列值时就存在歧义和令人困惑之处.
      对于 ABC model 的继承, 可以覆盖列名. 因为 ABC model 并没有实际的表去关联,
      没有歧义.

  * unmanaged model.

    - If you are mirroring an existing model or database table and don’t want all
      the original database table columns, use ``Meta.managed=False``. That option
      is normally useful for modeling database views and tables not under the
      control of Django.

  * 如果一个 app 中的 model 太多, 可以进一步模块化. 将 models 扩展成一个 subpackage.
    注意在 models package 的 init 文件中引入所有子模块中定义的 model.

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

  * view 在 render template 时, 提供的 context 可通过 ``get_context_data()`` method
    自定义.

  * ``model`` attribute 定义这个 view 是操作在什么 model 上的.
    Specifying ``model = SomeModel`` is really just shorthand for saying
    ``queryset = SomeModel.objects.all()``. ``queryset`` 可以更准确地提取
    数据集. ``get_queryset()`` method 可以动态获取数据集.

  * ``DetailView`` 可以通过 override ``get_object()`` method 来自定义对象获取过程.

  * Form. The default implementation for ``form_valid()`` simply redirects to
    the ``success_url``.

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

  * template context. 模板在被 render 时, 处在一定的 context 中.
    默认包含 ``object_list``, 即从数据库取到的对象列表. ``object_list``
    还有一个更有意义的名字, 由 model class name 转换而成 (``CamelCase -> camel_case``).

- static file

  * static file namespace 与 template namespace 机制类似.

  * 使用 ``static`` template tag 来自动根据 ``STATIC_URL`` 生成 static file 的 url,
    不要把静态文件的 url 写死在 html 里. 这样, 真正的 url 会根据
    ``STATICFILES_STORAGE`` 的机制去生成, 这样只需要设置 ``StaticFilesStorage`` 或
    某个 CDN 的 storage 实现, 就可以轻易切换所有 url 的指向, 真正做到了单一变量没有重复.

  * 静态文件的放置:

    - app-specific 的静态文件要放在 ``<app>/static/<app>/<filename>``.
      这样一个 app 的静态文件和它的代码在一起, 模块化更好.

    - 全局的静态文件可以选择两种放置方法:

      * 放在全局的 ``STATICFILES_DIRS`` 中, 例如 ``$BASE_DIR/static``.

      * 放在项目 app 中.

  * serve static files.

    - 在开发时, 使用 builtin server 即可 serve 各个 app 下的静态文件.

    - 在项目部署时, 执行 ``collectstatic`` 将静态文件集合在一起放在 ``STATIC_ROOT``,
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

- session


- form

  * csrf token
