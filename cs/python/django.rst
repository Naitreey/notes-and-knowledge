- When to use javascript/ajax with django? 当我们需要做纯前端交互逻辑和页面渲染时,
  才需要用 javascript, 当我们只是需要从服务端取数据以完成这些交互逻辑和渲染操作时,
  才需要使用 ajax, 否则都应该使用 django 的模板去构建.

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

  * 最顶层的 URLconf 由 ``settings.ROOT_URLCONF`` 定义.

  * django import 每个 URLconf 时, 加载 ``urlpatterns`` 变量里的 url 规则.

  * 匹配请求 url 时, 按照 ``urlpatterns`` 里的顺序进行, 执行第一个被匹配的
    url 的 view callable. urlpatterns are a list of ``url()`` instances.

  * URLconf 可以动态生成, 而不是写死在 ``urls.py`` 里.

  * URLconf 中的 url pattern 在它首次被访问时编译好.

  * 每个 app 的 URLconf 中应该包含 ``app_name``, 即它是 url name 的 namespace.
    可避免不同 app 的 url name 相互覆盖.

  * 由于所有 url 的路径部分都以 ``/`` 起始, 所以 django 的 url pattern 把它的
    匹配省去了, 写成 ``^path/to/resource/`` 而不是 ``^/path/to/resouce/``.

  * url regex pattern 中尽量使用 named capturing group, 增加灵活性.
    included url pattern 会收到在父级 url prefix 中匹配的变量值.

    only capture the values the view needs to work with and use non-capturing
    arguments when the regular expression needs an argument but the view
    ignores it.

  * 请求与 url pattern 在匹配时, 忽略 domain name 和 query string 部分, 并
    不论请求方法. 按照不同请求方法进行不同处理的逻辑在 view callable 中实现.

  * 使用 ``include()`` 加载别的 urlpatterns 至特定 url prefix 下面.
    可以指定一个 URLconf 的 import path, 或者一个 ``url()`` list.

    Whenever Django encounters ``include()``, it chops off whatever part of
    the URL matched up to that point and sends the remaining string to the
    included URLconf for further processing.

  * url reversing.

    Avoid hard-coding URLs.

    为了能够 reverse resolution, 需要对 url pattern 命名. 这样的 URLconf 包含从
    url 映射至功能以及从功能反向映射至 url 的双向信息.

    对于不同场景下的 url reversing 需求, django 提供了不同的操作:
    ``url`` tag, ``reverse()`` function, ``Model.get_absolute_url()`` method.

    - ``reverse()``.

      reverse 函数在反向查找时, 根据命名、参数数目、以及 kwargs 的名字来匹配.
      如果根据这些规则去匹配后有冲突, ``reverse()`` 选择 urlpatterns 中最后一个
      符合的 pattern. 这可以用于 override 其他 app 提供的同名 view.

      reverse 输出的 url 已经是 url-encoded.

  * url namespace. 两部分: application namespace 和 instance namespace.
    注意一个 app 可以在一个项目中部署多个 instance.

    namespace can be nested. 在一个本身有 namespace 的 urlpatterns 中 ``include``
    另一个有 namespace 的 urlpatterns, 就得到了 nested namespace.

    application namespace 可以通过两种方式指定: 如果是 include 另一个 app,
    在 ``urls.py`` 中指定 ``app_name``; 如果是 include 一段单独的 urlpatterns,
    在 ``include()`` 中指定 ``(urlpatterns, <app_namespace>)`` 参数.

    application namespace 和 instance namespace 看上去很乱的样子, 什么意思啊??
    只有当一个项目中部署了同一个 app 的多个实例时, 才需要考虑到 instance namespace.

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

  * field types.

    - IP address 用 ``GenericIPAddressField``.

    - 实数一般用 ``FloatField``, 精确要求时考虑 ``DecimalField``.

    - 整数有 ``IntegerField``, ``PositiveIntegerField``, ``BigIntegerField``,
      ``SmallIntegerField``, ``PositiveSmallIntegerField``.

    - ``DateField`` ``DateTimeField`` 可方便地实现创建时间、修改时间. 注意
      ``auto_now_add``, ``auto_now`` 和 ``default`` 参数是互斥的.

    - 若要允许在 ``BooleanField`` 中存 NULL, 使用 ``NullBooleanField``.

    - ``SlugField`` 要配合 ``slugify`` 函数使用, 只应该在创建 instance 时保存该列值.

    - ``FilePathField`` 要求值必须是满足路径匹配条件的文件路径.

  * field options.

    - ``null`` 默认是 False, 所以 create table 时有 ``NOT NULL``.

    - ``null`` 是规定数据库中 empty value 是否存储为 NULL 值;
      ``blank`` 是规定 form validation 时是否允许空值.
      两者的意义是不同的.
      ``null`` 和 ``blank`` 的默认值都是 ``False``.

    - ``choices`` 设置 field 的可选值. 每个选项的值的 symbolic enum 形式和整个选项
      列表应设置在 model class 中. 这是为了方便后续在查询等操作中使用. 设置该选项后,
      默认的 form 形式会变成 (multiple) select box. Given a model instance, the
      display value for a choices field can be accessed using the
      ``get_FOO_display()`` method.

    - 如果一个 model 包含多个与同一个其他 model 建立的 ``ManyToManyField``, 需要设置
      ``related_name`` 以保证反向的查询没有歧义.

    - ``help_text`` 设置该列值的更详细的帮助信息.

    - ``error_messages`` overrides default validation error messages.

  * validation.

    ``.save()`` 时不会自动调用 ``.full_clean()`` (因 form 验证时会执行它),
    若 model instance 不是来源于上层 form, 这验证操作必须手动执行. 或者
    等着数据库下层报错.

    ``Model.full_clean()`` 只能进行数据库层 data integrity 方面的检验, 复杂的检验
    要靠 ``ModelForm.full_clean()`` 去进行.
    field 中的很多限制条件, 例如 ``choices``, ``blank``, 以及一些 field type, 例如
    ``FilePathField`` 等, 本身不能限制存储的值, 因为这些条件不能在数据库中表达.
    这些条件只有配合 ``ModelForm`` 使用, 才能有用.

  * 表之间的关系抽象为在一个模型中包含另一个模型的实例作为属性. 这种抽象在逻辑上十分自然.
    并且在实例中进行 attribute lookup 以及在 QuerySet 中进行 field lookup 筛选时, 自然地
    支持了多级深入的操作.

  * many-to-one field.

    - 多对一的映射关系用 ``django.db.models.ForeignKey`` 实现.

    - foreign key field 的名字应该是所指向的 model 的名字的全小写版本.

    - django 自动给 foreign key field 添加索引.

    - ``ForeignKey`` field 在数据库中命名为 ``<field>_id``, 除非用 ``db_column``
      自定义.

    - ``on_delete`` 默认是 ``CASCADE``, 以后将变成 required parameter.
      如果对象之间的关系不是必须的, ``on_delete`` 应该设置成别的值, 例如 ``SET_NULL``.

    - 若 ``ForeignKey`` field 支持 ``null=True``, 则对这个属性赋值 None 即可去掉关联.

  * many-to-many field.

    - 由于一个列无法体现多对多的关系, ``ManyToManyField`` 在实现时, 不是构成了一个列,
      而是一个单独的 table. table 的命名根据 ``<app>_<model>_<m2mfield>`` 全小写命名.
      table 中包含 many-to-many 关系的两种模型数据的行 id.

    - It doesn’t matter which model has the ``ManyToManyField``, but you should only
      put it in one of the models – not both. ``ManyToManyField`` 应该放在那个编辑
      起来更自然的 model 中, 也就是说, 从哪个方向建立多对多映射关系更自然, 就把它
      放在哪个 model 中.

    - many-to-many field 的名字应该是一个复数类型的名字, 以表示多个的概念.
      同样的, ``related_name`` ``related_query_name`` 也应该是表示反向关系的
      复数.

    - intermediate model. 若多对多的关系不仅仅是一个简单双向的关系, 而需要包含
      一些其他状态信息, 则需要使用一个中间模型去承载这个多对多关系.

    - ``ManyToManyField`` 不是一个列, 而是抽象了一个包含映射关系的表, 只有设置
      映射和没有映射, ``null=`` 参数对它没有意义. 指定该参数会导致 django
      system check 警告.

    - through model. 多对多关系实际上是通过一个关系表来实现的. 这个关系表的 model
      可通过 ``ManyToManyField.through`` attribute 获得, 并可以通过 ``through``
      option 来指定单独创建的 through model.
      ``.through`` 属性在 model instance 上与普通的 ForeignKey field 相同, 是一个
      RelatedManager.

  * one-to-one field.

    - 一对一关系一般用于一个模型作为另一个模型的延伸、扩展、附加属性等.
      ``OneToOneField`` 在 model 继承时用于定义父表和子表通过哪一列来关联.

    - one-to-one field 在 mysql 中实现时, 实际上是一个普通的 field (类型与指向
      的 model 的 primary key 一致), 配合 unique key constraint 以及 foreign key
      reference constraint.

  * 通过 ``Meta`` inner class 定义来定义 model 的 metadata.

    - ``ordering`` 决定 QuerySet 的默认排序. 语法与 ``QuerySet.order_by`` 相同.
      若不设置, 则没有固定顺序 (SQL 没有 ORDER BY clause).

  * Model object managers (like ``.objects``) are only accessible via model classes,
    not the model instances.

  * 定义 ``__str__`` method 给模型的实例一个有意义的 string 形式.

  * 注意 ``Meta.verbose_name`` 和 ``__str__`` 的区别. 前者是模型本身的 verbose name,
    后者是 model instance 的字符串表现形式.
    在 admin site 中, 分类管理的 section 名字用 verbose name, 每个部分中, 对实例
    进行批量编辑的列表中, 显示实例用的 string 形式.

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

- CRUD

  * ``.save()``, ``.filter()``, slicing, 等等任何的抽象操作, 都是最终要映射为
    SQL statement 的.

  * 对于 model class 在实例化时, Django doesn’t hit the database until you
    explicitly call ``save()``.

  * ``INSERT`` 和 ``UPDATE`` 都是用 ``.save()`` 实现.

  * 对实例中 ``ForeignKey`` ``OneToOneField`` 等指向单一 model 实例的 field 赋值时
    使用相应 model 的 instance 即可.
    实例中的 ``ManyToManyField`` 实际上是一个 Manager object, 需要用 ``.add()`` 给
    这个集合中增加关联关系. ``.add()`` 接受一次传入多个对象, 建立多个映射.

  * Manager and QuerySet

    - 每个 model 都有一个 ``Manager`` instance, 用于进行 table-level operations.
      ``Manager`` instance is  accessible only via model class, rather than from
      model instances, to enforce a separation between “table-level” operations and
      “record-level” operations.

    - 获取对象的各个方法在 ``Manager`` 和 ``QuerySet`` 中都有 (在 QuerySet 中定义,
      expose to Manager 中), 且可以串联在一起. ``.delete()`` 是唯一的 QuerySet 有
      但 Manager 的没有的方法 (为了避免误删全部).

      * attributes & methods.

        - ``ordered``, QuerySet 是否有排序.

        - ``.all()``

        - ``.filter()``

        - ``.exclude()``

        - ``.get()``

        - ``.distinct()``, 相当于 ``SELECT DISTINCT`` statement.

        - ``.order_by()``, ``-<field>`` 表示逆序, ``?`` 表示随机, 可使用 field
          lookup 指定 related model fields. 若指定的 field 是 relation field,
          使用相关 model 的默认排序, 如果没有默认排序, 使用 pk. 若希望生成的
          SQL 完全避免排序 (甚至避免 model 默认排序), 使用无参 ``.order_by()``.
          若要排序的是 reverse FK, many-to-many 类关系, 注意涉及到 JOIN, 原来的
          一行可能排序后变成多行.

          chained ``.order_by`` 只有最后一个有用.

          在 django 生成的 SQL 中, order_by 指定的 field 会出现在后端执行的
          ``SELECT`` 语句中. (注意这是 django 的限制, 不是 SQL ``ORDER BY`` 的限制.)
          但仅用于排序, 不一定会返回在 QuerySet 中. 这导致 ``.distinct()``
          可能无法正常工作, 因为 fields 中包含额外的列.

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

        - 多值关系中可能造成结果重复:

          values() and values_list() are both intended as optimizations for a
          specific use case: retrieving a subset of data without the overhead
          of creating a model instance. This metaphor falls apart when dealing
          with many-to-many and other multivalued relations (such as the
          one-to-many relation of a reverse foreign key) because the “one row,
          one object” assumption doesn’t hold.

    - Field lookups. 各种过滤和获取的方法的参数语法, 对应到 SQL ``WHERE`` clause.
      Syntax: ``<field>[__<field>...][__<lookuptype>]=value``.
      若省略 lookuptype, 默认是 ``exact``.
      常用 lookuptypes: ``exact``, ``iexact``, ``contains``, ``icontains``,
      ``startswith``, ``endswith``, ``istartswith``, ``iendswith``.

      * 对 foreign key field 指定条件, 可以用以下方式进行判断: 1. FK 列 与 FK object
        实例进行比较; 2. FK 列 与 FK 值进行比较; 3. 使用 ``<FK>_id`` 虚拟的列
        和 FK 值进行比较.

      * 对于表达关系的列, 可以从多至一的方向深入被指向的模型进行筛选, 这抽象了各种
        SQL ``JOIN``.

      * 这种过滤可以反向进行, 即从一至多的方向进行筛选. 注意这与属性访问时得到
        RelatedManager 虽然语法相通, 但意义不同. 这里是通过对 related model 的行
        指定筛选条件, 来筛选 main object.
        若 ForeignKey field 没有设置 ``related_name``, 在反向 lookup 语法时, 指定
        related model 的全小写作为 reverse lookup 的起点; 若设置了 ``related_name``,
        则使用该名字作为 reverse lookup 起点. 在此之后再指定 related model 中的
        field 和条件.

      * 对于每个查询方法, 传入的所有 positional and keyword arguments (Q objects +
        field lookup syntax) 代表的条件都会 ``AND`` 在一起.
        但注意对于 ``.exclude()``, 这种与关系不太好理解.

      * ``.filter()`` 中同时指定多个条件时, 是在筛选所有这些条件都满足的实例, 这相当于
        ``WHERE condition1 AND condition2``.

        当 ``.filter()`` 是对所指向的关系 (即 JOIN 表) 进行查询时, 注意
        ``.filter(fk_obj__field1..., fk_obj__field2...)`` 以及
        ``.filter(fk_obj__field1...).filter(fk_obj__field2...)`` 两个的区别.
        前者是两个条件对 JOIN 表中一行同时满足; 后者是先 JOIN 一次筛出符合
        条件的, 再 JOIN 一次筛出符合另一个条件的, 相当于 subquery 嵌套.

      * ``.exclude()`` 中同时指定多个条件时, 是在排除满足其中任一个条件的实例, 即筛选
        所有这些条件都不满足的实例, 这相当于 ``WHERE NOT condition1 AND NOT condition2``.

      * django 提供了一个特殊的 ``pk`` field 名称, 用来代指当前 model 的 pk field,
        它可以像实际的 pk field 一样去写任何 field lookup 语法.

      * 对于字符串比较的各种 lookuptype, 基本上都转换成了 ``LIKE`` 类语句. 在这些
        语句语法中, 由 SQL metachar ``%`` 和 ``_`` 概念. 在 django 层, 若输入这两个
        字符, 将自动在 SQL 层进行转义, 保证 django 的抽象与底层 SQL 实现无关.

    - 使用 extended indexing and slicing syntax 来进行 ``LIMIT`` ``OFFSET`` 之类的
      操作. 注意 negative index 是不允许的. 如果是单个的 index, 就返回 QuerySet
      中的单个结果, 如果是 slice, 就返回一个 QuerySet. 一般情况下返回的 QuerySet
      仍然是 lazy 的, 但若 slice syntax 中有步长参数, 则会计算 QuerySet, 访问数据库.

    - 在过滤方法串联中, 每次返回的 ``QuerySet`` 都是相互独立的, 各自可以单独使用,
      不会相互影响.

    - QuerySets are lazy. 在不得不访问数据库之前, 所有的过滤筛选等操作都是在内存
      中进行的, 而不去执行底层的 SQL 语句.

    - QuerySet cache. The first time a QuerySet is evaluated – and, hence,
      a database query happens – Django saves the query results in the QuerySet’s
      cache and returns the results that have been explicitly requested. Subsequent
      evaluations of the QuerySet reuse the cached results.

      当取一个 QuerySet 的部分数据时 (通过 extended indexing syntax, 即转换成
      ``OFFSET`` ``LIMIT``), 若本身有 cache, 则直接返回结果, 否则只访问数据库
      进行所需部分数据的查询和返回, 并不进行 cache. 这里的抽象逻辑是, slicing
      和 indexing 这些操作是在一个完整的 QuerySet 上进行的部分截取. 而 cache
      是属于 QuerySet 的, 若有则应该包含它代表的所有数据.

      注意 ``bool(queryset)`` 会计算整个 ``queryset``, 从而填入 cache. 然而
      ``print()`` ``repr()`` 只计算整个 QuerySet 的一个 slice, 因此不会填入
      cache.

      若模型包含 ``ForeignKey`` ``OneToOneField`` field 时, QuerySet 在取实例时
      相当于只将 FK_id 取回来, 而不会自动 JOIN 表查询取到关联的对象数据. 这是
      为了避免不必要的 overhead. 当用户明确要访问 FK object 这个属性时, 才再次
      访问数据库将数据填入 cache, 返回真实的关联对象. 之后再访问该属性时不再
      访问数据库.

    - 同一个 model 的实例之间进行比较时, 比较的是 primary key. 不同 model 的实例
      之间总是不相等的. 但是大小关系没有确定结果. (why not TypeError?)

    - query expressions.

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

        - ``Case``. 接受 positional ``When`` objects 作为 cases, 这些 When objects
          依次执行, 直到有一个为 True 为止, 返回的结果是相应的 When 的 then.
          若没有一个 When 为真, 则返回 ``default=`` 值或 None.

    - delete.

      * 删除时会返回删除的总对象数目和每个类型删除的对象数目. 这么做的一个
        重要原因是模型或表之间有设置了级联删除的.所以很可能一个删除操作一下子级联
        删除了很多不同表中的条目.

      * model instance 和 QuerySet 都有 delete method.

    - update. QuerySet ``.update()`` 中以 kwargs 形式写入要更新的列和值.
      many-to-many field 无法这样更新.

      ``.update()`` 更新操作是批量进行、立即生效的. 它不会使用 model 的 ``.save()``
      method (否则就不是批量执行了), 而是直接生成批量执行的 SQL. 因此各种 model
      层的封装特性, 例如 custom save, auto_now, pre_save/post_save signal 等
      都不会生效.

    - related objects. 一对多、多对多关系中, 正向的 manager object (如果有) 是属性名,
      逆向的 manager object 默认是 ``<lower_model>_set``, 可通过 ``related_name``
      自定义. 在一对一的关系中, 正反向都是对称直接访问的.

      如果用户在查询某模型时, 已知会访问到关联的 FK 对象, 可使用 ``select_related()``
      来强制进行 JOIN 操作, 一次把所有 FK 对象数据取回来, 这样更高效. 避免获取各个
      FK object 时再单独访问数据库. To avoid the much larger result set that would
      result from joining across a ‘many’ relationship, ``select_related`` is limited
      to single-valued relationships - foreign key and one-to-one.

      ``RelatedManager`` 的一些方法: ``add()``, ``create()``, ``remove()``,
      ``clear()``, ``set()``. 这些操作都是立即在数据库生效的.

- aggregation.

  * 两种聚合方式: ``QuerySet.aggregate()``, ``QuerySet.annotate``.

  * ``QuerySet.aggregate()``: 给整个 QuerySet 生成各种聚合值.

    - 需要执行的聚合操作通过 positional args 或 keyword args 来指定.
      返回聚合结果 dict. key 是聚合项, value 是聚合值. key 自动根据
      field name 和聚合操作名生成; 或者通过 keyword 参数指定.

    - 由于返回一个 dict, 所以 ``.aggregate`` 要作为 QuerySet chain 的最后操作.

  * ``QuerySet.annotate()``: 给 QuerySet 里的每个元素生成聚合值. 这不仅仅
    可用于 ``GROUP BY`` 聚合, 还可用于对每行返回所需的运算结果, 即 annotate
    的一般含义.

    - annotate 语法与 aggregate 相同, 但是每个聚合值是 attach 到各个
      元素上的, 成为元素的 attribute.

    - 由于结果成为了 attributes, 返回的仍是一个 QuerySet, 因此可以继续
      operation chain.

    - 使用 annotate 进行多项聚合时必须要谨慎, 很可能结果不对, 并且必要时检查
      生成的 raw sql statements. 多项聚合结果可能错误的原因是 django 简单
      地将多项聚合条件涉及的所有表 join 在一起, 然后再算聚合值.

  * aggregation functions.

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

- view

  * view 这个概念没有什么很好的意义. 应该说, 从一定程度上, HTTP 的请求可以看作是
    对整个 app 的不同视角 (view), 但这种说法有些牵强. 总之, views 就是对 url
    请求的 server 端实现.

  * 每个 view 都必须返回 ``HttpResponse`` instance 或者 raise some exception. 任何其他
    结果 django 都认为是有问题的.

  * 常用的非 200 响应有单独定义的 ``HttpResponse`` 子类.
    ``Http404`` 是一个单独定义的 exception, 为方便使用. django catch 这个异常,
    返回 ``templates/404.html`` 页面.

  * trick: 给 view callable 设置默认参数可以做到让多个 url 指向一个 view callable.

    .. code:: python
      urlpatterns = [
          url(r'^blog/$', views.page),
          url(r'^blog/page(?P<num>[0-9]+)/$', views.page),
      ]
      # View
      def page(request, num="1"):
          pass

  * error handling view. 对于一个请求, 当 urlpatterns 中没有匹配到时, 或者在处理过程中
    抛异常时, django 会返回一个 error-handling view. 在 URLconf 中可以自定义各个常用
    error code 对应的 response view. 例如 ``handler400``, ``handler403``,
    ``handler404``, ``handler500``.

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

  * django 支持同时配置多个模板 backend engine. 包含 django 自己的模板语言和 jinja2.
    ``get_template`` 等操作遍历所有后端找到并返回第一个模板.

- django template system & language

  * components:
    engine, template, template language, context, context processor, loader.
    体会 django 是如何将用变量填充模板这件事模块化成一个个环节和组件对象的.

  * template namespace. 每个 app 下可以有 ``templates/`` 目录, 不同 app 的 templates
    目录在一个 namespace 中, 因此会相互覆盖. 所以需要再创建 ``templates/<app>`` 子目录.

  * 为了结构清晰, 应该把不同 app 的模板放在各自目录下的 ``templates/<app>/`` 下面.

  * template 中 object 的 ``.`` operator 的查找顺序:
    dict key, object attribute, list index.
    若 attribute 是一个 callable, it'll be called with no argument.
    django 不允许 callable 输入变量, 是为了避免对可以执行函数这个功能滥用.
    数据应该在 view 中计算完成再传入 template 进行渲染, 而不是在 template
    中才计算.

    This lookup order can cause some unexpected behavior with objects that override
    dictionary lookup. 例如重定义了 ``__getitem__``, 导致没有 key 时没有 raise
    KeyError, 从而轮不到 attribute lookup.

    若最终没有找到, fallback 至 template backend 的 ``string_if_invalid`` option 值,
    默认是空字符串.

  * 在 template 中使用 symbolic url, 即使用 url 的名字, 而不写死 url 路径在模板中.
    这样可以降低 template 和 URLconf 之间的耦合. 在重构 url 结构时, 不需要修改模板
    文件.

  * 模板的搜索顺序:

    - ``DIRS`` in ``settings.py``.

    - 若 ``APP_DIRS == True``, 每个 app 目录下的 ``templates/`` 目录.

  * template context. 模板在被 render 时, 处在一定的 context 中.
    默认包含 ``object_list``, 即从数据库取到的对象列表. ``object_list``
    还有一个更有意义的名字, 由 model class name 转换而成 (``CamelCase -> camel_case``).

  * 将可重用的 template 模块化, 并用 ``include`` tag 加载它.

  * ``django.shortcuts.render()`` 调用 ``django.template.loader.render_to_string()``
    渲染模板成 string 然后加载至 HttpResponse.

  * 模板有三类语法元素, 变量替换 ``{{ var|filter }}``, tag 执行 ``{% tag var1 var2 %}``,
    注释 ``{# comment #}`` (只能单行, 不允许 newline).

  * filters.

    - ``default``

    - ``length``

    - ``filesizeformat``

    - ``safe``

    - ``escape``

  * tags.

    - ``extends``, 必须是模板中的第一个 tag.

    - ``block``, parent template 中定义的 blocks 越多越好. 这样增加了页面区域的
      模块化, child template 只需覆盖或扩展需要修改的 blocks.
      对于扩展而非覆盖整个 block, 可以用 ``block.super`` tag 引用父模板中的同名
      block 内容.

      使用 ``{% endblock <name> %}`` 增加可读性.

    - ``autoescape``

    - ``load``, 父模板加载的 custom tags/filters 若要在子模板中使用, 需要重新加载.

  * template inheritance.

    Template inheritance allows you to build a base “skeleton” template that
    contains all the common elements of your site and defines ``block``'s that
    child templates can override.

    Content within a ``{% block %}`` tag in a parent template is always used as
    a fallback.

    - common design.

      * ``base.html`` 包含网站基本框架结构、样式风格等.

      * ``base_<section>.html`` 包含各自功能部分的各异的基本框架结构、样式风格.

      * 每个功能部分的具体页面去实现所需功能.

  * escaping. django template 默认 escape output of every variable tag.
    disable auto escaping: 在变量级别上, 使用 ``safe`` filter; 在 block 级别上,
    使用 ``autoescape`` tag 来开启或关闭 auto escaping. ``autoescape`` tag
    的影响包含在 child template 中的同名 block.

    template 中的 string literal 没有被 escape, 而是原样包含在 html 中.

- request and response

  * ``HttpRequest``

    - attributes.

      * ``scheme``. http or https. 这里 https 指的不是说 django server 直接接受
        到的请求是 TLS 加密过的 http 流量, 而是说它通过上游服务器 (例如 nginx)
        设置的特定 header 的值判断出这个请求走的 https 协议. 这个加密的请求在
        上游服务器解密后以 plain http 的形式传递给 django server.

      * ``body``. raw request body as bytes string.

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
    多个值的情况的 dict 的封装. 它是 dict 的子类. 常见的 dict 操作只获取某个
    key 对应的最后一个值. 若要获取整个 list, 使用 list 类方法.

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

    - ``readonly_fields`` 应该是 readonly 的啊, 为啥不管用呢?

    - ``search_fields`` 设置一些可以搜索的列 (包含 related field lookup), 此时
      change list 上面有搜索框.

    - 很多配置项可以设置 AdminSite 级别的全局值, ModelAdmin 级别的 model 局部值,
      值, callable 列级别的独立值.

    - 各种操作的页面模板可以通过相应属性设置为自定义的模板.

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

  * ``makemigrations --dry-run`` 可用来检查当前记录的数据库结构 (通过
    migration files 来体现) 是否和 models 里的模型代码保持一致.


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

  * 旧版本 django 中生成的 migration files 保证能在新版 django 中使用.
    也就是说, migration system 是向后兼容的.

  * 所有 string literal 统一使用 unicode string 或 bytestring. 这不仅是一般
    的 py2py3 统一性要求. 在 django 中, 若要 app 同时兼容 py2py3. 必须这样做.
    因为, py2 默认 bytestring, 这样应用在数据库中的是 bytes, 同样的代码在 py3
    下运行时, 由于 django 看见都是 unicode string, 而数据库中是 bytes, 这样
    要再生成一个 migration 去修改现有数据库结构至支持 unicode string.

  * ``manage.py migrate`` 除了可以 apply migration 之外还可以指定将某个 app 的
    数据库状态确定在某个 migration 上面, 若当前状态已经新于指定的状态, 则
    unapply necessary migrations.

  * django 生成的 migrations 需要仔细检查, 对于复杂的数据库修改, 不能保证不出错,
    必要时需要手动修改甚至手动创建 migrations.

  * ``makemigrations`` 和 ``migrate`` 操作一般不要限制 ``app_label``, 要对所有 apps
    同时进行. 因为 model 之间经常是相互依赖的. 如果只对某个 model 更新数据库状态
    可能 break dependency.
    在特殊情况下, 要限制 migration file 修改在某个 app 中, 此时采用 app label.

  * migration definition.

    - 每个 migration 必须是名为 ``Migration`` 的 class, 且为
      ``django.db.migrations.Migration`` 的子类. 其中包含 ``dependencies``
      ``operations`` 等属性.

    - 每个 migration operation 是 ``Operation`` class 的 (子类的) 实例.

  * data migration.

    - data migration 必须手写, 涉及 ``RunPython`` operation.

  * database operation and state operation.

  * How to move model between apps, without losing any data?
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

  * squash migration 十分有用. 可以用来将过多的 migration 历史合并成一个等价的
    初始版本.

    These files are marked to say they replace the previously-squashed migrations,
    so they can coexist with the old migration files, and Django will intelligently
    switch between them depending where you are in the history. If you’re still
    part-way through the set of migrations that you squashed, it will keep using
    them until it hits the end and then switch to the squashed history, while new
    installs will just use the new squashed migration and skip all the old ones.

    The recommended process is to squash, keeping the old files, commit and
    release, wait until all systems are upgraded with the new release, and
    then remove the old files, commit and do a second release.
    只有当所有项目的实例都已经更新到 squashed migration 的结束点之后时, 才能
    删除它替代的那些原始文件.

    最终, 使用 squashed migration file 替代一系列原始文件的方法是:

    - Deleting all the migration files it replaces.

    - Updating all migrations that depend on the deleted migrations to depend
      on the squashed migration instead.

    - Removing the ``replaces`` attribute in the Migration class of the squashed
      migration.

    当数据库结构之间的关系非常复杂时, 慎用 squash migration. 最好检查 squash
    的结果是否符合当前 models 结构.

- session

- form

  * ``django.forms.Form`` 是 form handling 的核心. A ``Form`` class describes
    a form and determines how it works and appears.

  * A form’s fields are themselves classes; they manage form data, perform
    validation and clean form data when a form is submitted.

  * A form field is represented to a user in the browser as an HTML “widget” -
    a piece of user interface machinery. Each field type has an appropriate
    default ``Widget`` class.

  * So when we handle a model instance in a view, we typically retrieve it
    from the database. When we’re dealing with a form we typically instantiate
    it in the view.

  * When we instantiate a form, we can opt to leave it empty or pre-populate it.

  * 使用同一个 view 和同一个 url 去获取 form 和处理 form data.
    基本逻辑: GET 和 POST with invalid data 时返回 form 本身, 并且由于已经有数据,
    可以在 render 时对错误进行相应提示; POST with valid data 时处理数据返回结果.

  * ``Form`` class.

    - ``Model`` 类属性 maps to 数据库列; ``Form`` 类属性 maps to HTML input 元素.

    - 每个 Form field 不仅负责对数据进行验证, 还负责对数据进行 clean, normalizing
      it to a consistent format.

    - form field types.

      * ``FilePathField``

      * ``ModelChoiceField`` 的参数是待选的 QuerySet.

      * ``ModelMultipleChoiceField`` 的参数是待选的 QuerySet.

      * ``CharField``

    - form field options.

      * ``label`` 定义 ``<label>`` tag 内容.

      * ``max_length`` 定义 ``<input>`` 最大长度, 并具有验证功能.

      * ``help_text`` 在 render 时放在 field 旁边.

      * ``error_messages`` overrides default field validation errors.

    - form methods.

      * ``is_valid()`` method 验证 form data 是否合法并清理数据设置 ``cleaned_data``.
        在背后, 它调用所有 fields 的验证和数据清理逻辑.

    - render form.

      * 考虑到要和各种前端框架的 element 结构层级、样式定义结合, 直接把整个 form
        或者 field 输出为 html 代码根本不实际, 输出太死板. 绝大部分时候还是需要
        仔细在 html 代码中定义好结构和样式, 只用模板变量填入必要的值.

      * ``str(form)`` 即获得 form instance 对应的 html 代码. 注意 rendered Form
        instance 不包含 ``<form>`` element wrapper 和 submit button.

      * ``form.non_field_errors`` 是全局错误.

      * 也可以 ``form.as_table`` ``form.as_p`` ``form.as_ul``.

      * render 后, 每个 input field 的 ``id`` attribute 是 ``id_<field-name>``.

      * ``form[<field-name>]`` 是各个 field 对应的 ``BoundField``.

    - unbound form: no data. when rendered, being empty or containing only
      default values.
      bound form: has data. can tell if data is valid, 若数据非法, 会生成
      相应的错误信息, 可填入模板, 返回给用户.
      ``is_bound`` 属性判断是否 bound.

  * ``BoundField`` class.

    - ``str(boundfield)`` 给出它的 input HTML element.

    - attributes & methods.
    ``.errors`` ``.id_for_label`` ``.label`` ``.label_tag()`` ``.value()``
    ``.html_name`` ``.help_text`` ``.is_hidden`` ``.field``

    ``.errors`` 的 string 形式是一个 ``<ul class="errorlist">`` element,
    但在 loop over 它的时候, 每个 error 只生成纯字符串.

  * csrf token. ``{% csrf_token %}`` 即可添加 form 级别的 CSRF token.
    When submitting a form via POST with CSRF protection enabled you must use
    the ``csrf_token`` template tag as in the preceding example.

  * ``ModelForm`` class.

    - ``ModelForm`` 是 ``Form`` 的一种, 它根据现成的 model 去生成 form.

    - 指定所使用的 ``Model``, 它会 build a form, along with the appropriate fields
      and their attributes, from a Model class. 省去手动写 field 的麻烦.

    - The generated Form class will have a form field for every model field
      specified, in the order specified in the fields attribute.

    - ``ModelForm.__init__`` 中若加入 ``instance=`` 参数, 则是将 form 与一个
      现存的 model instance 关联, 例如为了更新它的一些列. 这样, 在 validation
      时, 可能会修改传入的 model instance. 若验证失败, 传入的 model instance
      可能处于 inconsistent state, 不适合再次使用.

    - 选择需要包含在 form 中的 model fields.
      ``ModelForm`` 要求必须定义 ``Meta.fields`` 或 ``Meta.exclude``.

      It is strongly recommended that you explicitly set all fields that should
      be edited in the form using the ``fields`` attribute. Failure to do so can
      easily lead to security problems when a form unexpectedly allows a user to
      set certain fields, especially when new fields are added to a model.

      ``fields = '__all__'`` 自动包含所有列.

    - model field 和 form field 的对应.

      * ``TextField`` model field 默认的 form field 是 ``CharField``, 并设置 widget
        为 ``Textarea``.

      * ``ForeignKey`` model field 对应 ``ModelChoiceField``.

      * ``ManyToManyField`` model field 对应 ``ModelMultipleChoiceField``.

    - model option 和 form option 的对应.

      * ``blank=True`` 对应 ``required=False``.

      * ``verbose_name=`` 对应 ``label=``.

      * 若 model field 有 ``choices``, form field ``widget`` 默认是 ``Select``.

    - methods.

      * ``.save()``. ``.save()`` 可以直接保存新的 model instance 或更新现有的
        instance (若 constructor 有 ``instance`` 参数). 它会进行验证.
        它调用 ``Model.save()``.
        ``commit=False`` 时并不将数据存入数据库, 而是只返回 model instance.
        若 model 存在 ManyToManyField 需要修改或创建, ``commit=False`` 显然
        不会创建在 form 中选定的那些关联. 这样, 若手动执行 ``Model.save()``
        来保存实例的话, 之后需要使用 ``ModelForm.save_m2m()`` 单独保存选定
        的关联关系至数据库.

  * 当一个 form 与某个 model 对应时, 使用 ``ModelForm``, 否则使用 ``Form`` 即可.

  * 很多对象 render 为 html 形式后会添加标识 id 和样式 class. 方便进行前端自定义.

  * form inheritance. ``Form`` 类继承时, 父类的列在先, 子类的列在后.
    对于多继承, 列的先后顺序根据各父类的远近关系按由远至近的顺序.
    这里的远近关系值的是在 MRO 中的顺序的逆序, 在 MRO 中越靠后越远.

- Export CSV.

  由于 HttpResponse 是 writable file-like object, 可以直接转递给 ``csv.writer``
  ``csv.DictWriter`` 作为 write target.
  若要传输很大的 csv 文件, 需要使用 StreamingHttpResponse. 这需要一些技巧.
  详见 django 文档.

- authentication and authorization. django auth module: ``django.contrib.auth``.

  * 创建用户. ``User.objects.create_user()`` 创建用户.
    ``./manage.py createsuperuser`` 或 ``User.objects.create_superuser()``
    创建超级管理员.

  * 修改密码: 通过 ``./manage.py changepassword`` 和 ``User.set_password()``
    来修改密码.

  * Authentication

    - ``authenticate()`` function 提供认证检验. 若认证成功返回 User object,
      否则 None. 注意它只做检验 (返回相符的 User instance), 不改变状态.

    - ``login()`` 在 ``authenticate()`` 的基础上, 改变认证状态, 并将认证相关信息
      保存在 session 中. 未 login 时, ``request.user`` 是 ``AnonymousUser``,
      login 后成为 ``User``. 两者的 ``is_authenticated`` attribute 的值分别是
      False/True, 可用于判断是否登录了.
      Note that any data set during the anonymous session is retained in the
      session after a user logs in.
      When a user logs in, the user’s ID and the backend that was used for
      authentication are saved in the user’s session. This allows the same
      authentication backend to fetch the user’s details on a future request

    - login url 在 ``settings.LOGIN_URL`` 设置, 默认是 ``/acounts/login``.
      该值应该按照项目中用户模型、view 等的具体情况进行设置. 并且可以设置为
      url pattern name.

    - login redirect url ``settings.LOGIN_REDIRECT_URL``, 登录后的默认跳转路径.

    - logout redirect url ``settings.LOGOUT_REDIRECT_URL``, 登出后的默认跳转路径.

    - ``logout()`` 撤销认证状态和清空 session 信息.

    - authentication views.
      auth views 不提供默认的 templates, 需要自己写模板以加载 context variables.

      若不想直接使用默认的 auth.urls 设置, 可单独使用 views 以对参数进行自定义,
      以及 bind to custom urls.

      * login:
        ``login()``, ``LoginView``.

      * logout:
        ``logout()``, ``LogoutView``.

      * logout then redirect to login:
        ``logout_then_login()``.

      * password change:
        ``password_change()``, ``PasswordChangeView``.

      * password change done:
        ``password_change_done()``, ``PasswordChangeDoneView``.

      * password reset:
        ``password_reset()``, ``PasswordResetView``.

      * password reset done:
        ``password_reset_done()``, ``PasswordResetDoneView``.
        密码重置请求已经发出后显示的页面.

      * password reset confirm:
        ``password_reset_confirm()``, ``PasswordResetConfirmView``.
        点击邮件中的密码重置链接后显示的密码重置页面.

      * password reset complete:
        ``password_reset_complete()``, ``PasswordResetCompleteView``.
        重置密码后提示成功的页面.

    - authentication forms.

      若不想使用 auth views, 可单独使用 auth forms.

      * ``AdminPasswordChangeForm``
        used in admin site.

      * ``AuthenticationForm``

      * ``PasswordChangeForm``

      * ``PasswordResetForm``
        ``.save()`` method 并不修改任何状态, 而是调用 ``.send_mail()`` 发送重置邮件.

      * ``SetPasswordForm``
        form to set new password without entering old password.

      * ``UserChangeForm``
        used in admin site.

      * ``UserCreationForm``

    - ``django.contrib.auth`` app 提供了一系列 authentication urls.
      这些 url 是没有 namespace 的. 在使用时可以直接放在 url root path 上,
      或者 ``include()`` 中设置 namespace.

      * ``login/``

      * ``logout/``

      * ``password_change/``

      * ``password_change/done/``

      * ``password_reset/``

      * ``password_reset/done/``

      * ``reset/<uidb64>/<token>/``

      * ``reset/done/``

  * Permission and Authorization

    - 当 ``django.contrib.auth`` app 存在时, 每个 app 的每个 model 都默认存在
      add, change, delete 三个权限.

    - 权限检查 ``User.has_perm(<app_label>."add|change|delete"_<model>)``

    - 一个用户或一个组可以有任意个权限 (many-to-many). 组具有的权限用户自动具有.

    - 限制操作范围为登录用户: ``login_required`` decorator 和 ``LoginRequiredMixin``.

    - 用户权限检查: ``permission_required`` decorator 和 ``PermissionRequiredMixin``.

    - 通用的 test 检查: ``user_passes_test`` decorator 和 ``UserPassesTestMixin``.

    - ``AccessMixin`` 是以上几个权限控制的 mixin class 的父类, 它具有最一般化的
      性质.

    - ``RequestContext`` 为 template context 自动添加一系列用户、权限相关量.

      * ``user``, 当前用户.

      * ``perms``, 当前用户的权限. ``perms.<app_label>`` 相当于
        ``User.has_model_perms(<app_label>)``.
        ``perms.<app_label>.<perm>`` 相当于 ``User.has_perm(<app_label>.<perm>)``
        ``perms`` 支持使用 ``in`` operator 检查权限, ``<app_label> in perms``
        或 ``<app_label>.<perm> in perms`` 都可以.

  * auth backend.
    ``auth`` app 中的各种上层认证和授权操作实际上要转发给底层 backend 去操作.
    不同类型的 backend 的实现不同, 但符合相同的预定义的 api, 供上层调用.

    - ``AUTHENTICATION_BACKENDS`` 配置 backend list. django 按照 list 顺序进行
      认证尝试.

    - 在 ``authenticate()`` 时, 依次尝试所有的 backend, 直到:

      * 第一个认证成功为止;

      * 或某个 raised ``PermissionDenied``;

      * 或遍历结束整个 list.

    - auth backend 会保存在 session (``django_session`` table) 中, 从而对于一个
      session, 只用已知的 backend. 如果要更改 backends setting 以使用不同的
      backend 来认证, 需要清空 session.

    - 结合使用外部的 auth backend 时, 仍然需要根据 ``AUTH_USER_MODEL`` 对每个
      用户创建系统账户. 因为从逻辑上讲, 这些 user objects 才是这个系统 (django)
      自己的用户. 外部 auth backend 只是提供了一系列用户实体集合. user model
      才是这个系统所需的 user 所具有的属性和功能的表征. 从实现上讲, 没有 user
      model 什么也没法弄, 没有用户概念的实体寄托.

    - ``ModelBackend`` 和 ``RemoteUserBackend`` 不允许 inactive user 认证.
      ``AllowAllUsersModelBackend`` 和 ``AllowAllUsersRemoteUserBackend``
      允许 inactive user 认证.

    - API.

      * ``.get_user(<pk>)`` return user object.

      * ``.authenticate(...)`` return user object or None.

      * ``.get_group_permissions()``

      * ``.get_all_permissions()``

      * ``.has_perm(...)``

      * ``.has_module_perms()``

  * User 和 Group 是 many-to-many 的关系.

  * ``User``

    - fields, attributes

      * ``groups``.

      * ``user_permissions``.

      * ``username``.

      * ``password``. 密码以 hash 形式存放, 符合密码存储的一般准则. 因此不该手动修改
        该属性值.

      * ``email``.

      * ``first_name``.

      * ``last_name``.

    - methods.

      * ``has_module_perms(<app>)``, 判断用户是否在某个 app 中有至少一个权限.

  * ``AnonymousUser`` 虽然不具备很多 ``User`` 的属性和方法, 但是可以检查权限,
    因为很多时候网站是允许匿名用户的.

  * 扩展或自定义 user model.

    - purely behavioral extension, use proxy model.

    - store additional information (profile-like infos) related to a user,
      but not auth-related, use new model with ``OneToOneField`` to ``User``.
      为了在用户创建、删除等操作时两表同步, 需要使用 signal.

    - default User model just does not fit your need, create custom user
      model as ``AUTH_USER_MODEL`` to override the default.

      即使 User model 已经足够, 也应该使用自定义的 user model, 这样方便之后
      进行扩展.
      If you’re starting a new project, it’s **highly recommended** to set up a
      custom user model, even if the default User model is sufficient for you.
      This model behaves identically to the default user model, but you’ll be
      able to customize it in the future if the need arises.

    - Change to custom user model mid-project.
      **HORRIBLE**.

    - Reusable apps shouldn’t implement a custom user model.
      If you need to store per user information in your app, use a ForeignKey
      or OneToOneField to ``settings.AUTH_USER_MODEL``.

    - 由于 ``AUTH_USER_MODEL`` 不一定是 ``django.contrib.auth.models.User``,
      因此在某个 app 中使用 user model 时, 不能直接 import User 类, 而是要
      根据具体场景使用 API ``get_user_model()`` 或者 ``settings.AUTH_USER_MODEL``.

    - 用户相关的信息的存储方式. 若这些信息是 app-specific 的, 而不是用户本身
      的属性或者通用的信息, 则应该存在 app models 中, 添加对 user model 的
      关联关系即可. 若是属于用户本身, 甚至是用户认证相关的属性, 则应该放在
      user model 中.

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

    - ``BaseUserManager``, ``UserManager``:
      自定义的 user model 还需要自定义 user manager.

    - ``AbstractBaseUser``

      * ``USERNAME_FIELD``, the name of field used as identifier, must be unique.

      * ``EMAIL_FIELD``

      * ``REQUIRED_FIELDS``, prompted for when creating superuser.

      * ``is_active``

      * ``get_full_name()``

      * ``get_short_name()``

      * ``get_username()``

      * ``clean()``

      * ``get_email_field_name()``

      * ``normalize_username()``

      * ``is_authenticated``, True for any instance.

      * ``is_anonymous``, False for any instance.

      * ``set_password(...)``

      * ``check_password(...)``

      * ``set_unusable_password()``, 当使用外部认证机制时, 禁用普通密码.

      * ``has_usable_password()``

      * ``get_session_auth_hash()``

    - ``BaseUserManager``

      * ``normalize_email(...)``

      * ``get_by_natural_key(...)``

      * ``make_random_password(...)``

    - ``UserManager``

      * ``create_user(...)``

      * ``create_superuser(...)``

    - 自定义的 user model 还需考虑 builtin auth form, 以及在 admin site 对
      user model 的额外要求.

    - ``PermissionsMixin`` 为自定义的 user model 提供了对 django group &
      permission model 的支持.

      - ``is_superuser``

      - ``get_group_permissions(...)``

      - ``get_all_permissions(...)``

      - ``has_perm(...)``

      - ``has_perms(...)``

      - ``has_module_perms(...)``

  * ``Permission``

    - 创建 Permission object 需要配合合适的 ``ContentType``.

    - 可以通过 ``Model.Meta.permissions`` 来创建与 model 直接相关的自定义权限.

    - caching. ``ModelBackend`` 会在取到一个用户的权限信息后进行 cache. 若在
      一个 request-response cycle 中, 需要修改权限并立即进行验证, 最好从数据库
      重载这个用户. 若不是在一个请求中, 一般没事, 因每次 request object 都会
      初始化 User object (lazily).

  * Group

- django release

  * new feature release (A.B, A.B+1) every 8 months.
    new LTS release (X.2) every 2 years, LTS is supported with security updates
    for 3 years.
    each version following an LTS will bump to the A+1 major version number.
    patch release (A.B.C, A.B.C+1) will be issued as needed.

  * 1.11 LTS is the last version supporting python2.

  * Django 2.0 和 1.11 相比, 不会是特别大的区别, 不会充满 breaking changes,
    而是连续的演进.
