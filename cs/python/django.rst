project and app
===============

- project vs app.

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

project
-------

* 由于 django 设计的 project 代码 import 逻辑 -- 即 project 目录需要在 ``sys.path``
  中, 导致 django project 不适合整个打包为 python package 然后用 pip 安装至
  site-packages 目录. 因为这样的效果是在 ``sys.path`` 中包含 site-packages 的子目录.
  结果就是 import 时可能存在覆盖问题.

  整个 django project 适合打包成 rpm/deb, 放在 ``/usr/lib`` 下.

  然而, 一个 django project 中的每个 app, 都应该可以打包成 python package 用 pip
  安装.

* project 目录可以作为一个全局 app 来使用. 全局的模板, 全局的静态文件, 全局的 url,
  全局的管理命令等, 都可以放在这个全局 app 中.

* project structure.

app
---

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

* app structure.

  - ``mixins.py``. 所有在本 app 中定义的 mixin classes. 这些 mixins 可能不仅仅
    是 views 会用到, forms, models 等也可能使用. 所以单独拿出来.

  - ``tasks.py``. 需要使用 task queue 时, 放置所有任务.

  - ``validators.py``. 放置所有自定义的 forms/models validators.

  - ``fields.py``. 放置所有自定义的 model fields.

* special global app.

  - structure.

URLconf
=======

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

* view shortcut functions.

  - ``django.shortcuts.render()``

  - ``django.shortcuts.redirect()``

    * return ``HttpResponseRedirect``.

    * 输入 model, redirect to ``Model.get_absolute_url()``.

    * 输入 view name (with args, kwargs), redirect to ``reverse()`` url.

    * 输入 absolute/relative url, redirect to that url.

    * ``permanent=True``, return 301 (Moved Permanently) rather than 302 (Found).

  - ``django.shortcuts.get_object_or_404()``

    ``QuerySet.get()`` a single object from a Model/Manager/QuerySet, 满足 args
    和 kwargs 设置的过滤条件. 语法与 ``Q`` objects + field lookup syntax 相同.

    由于是直接 raise ``Http404``, 所以这只适合在 view 中使用.

  - ``django.shortcuts.get_list_or_404()``

    ``QuerySet.filter()`` a list of objects, 其他同上.

* view, template, form/formset 等的构建.

  前端构建的传至后端的 form data 必须要能再次回到前端填充成原始的 form
  输入内容. 也就是说, Form, BaseFormSet 等的实例必须包含能重新构建前端
  form 填充形式的所有数据. 不要在前端 form 和 django form/formset 之间
  进行数据格式转换, 这是多此一举的, 而且非常麻烦.

  form/formset 没必要和 model 一致 (也就是说没必要用 modelform), 而是完全
  由前端业务逻辑决定的. 但是, form 中的各项最好和页面模板中的 html form
  项是一致的. 这样从 POST 数据构建 form, ``form_valid``, ``form_invalid``
  等的处理和数据重填都很方便.

  如果想要传递某些 form 项但不希望用户输入, 则使用 hidden input type (配合
  js 进行输入), 而不是直接从 form 中去掉这项. 注意 view 中逻辑需要对 hidden
  input 的数据合法性进行验证.

* form validation. 不要在 view 本身的逻辑中写 form 本身数据 validation 逻辑,
  要归入 form class 的定义中, 对于 model form 的情况, 还可考虑是否应当
  再归入 model class 中, 即从 model 层对数据的合法性进行进一步限制.

  但对于 form data 是否 suspicious 之类的检查, 需要在 view 中进行.

Class-based views
-----------------

- class-based views 相对于 function-based views 的一些好处

  * Organization of code related to specific HTTP methods (GET, POST, etc.) can
    be addressed by separate methods instead of conditional branching.

  * Object oriented techniques such as mixins (multiple inheritance) can be used
    to factor code into reusable components.

- 处理每个 request, View class 都会实例化一个新的 instance. 所以在
  写 view class 时不要担心状态存留问题.

- ``View``, base view class. 所有 class-based views 都是它的子类.

- attributes.

  * 所有传入 constructor 的 kwargs 都会成为 instance attributes.

  * 除此之外, ``request``, url pattern 匹配的 ``args`` & ``kwargs``
    都会成为 view instance attributes.

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

- view mixins.

  * ``TemplateResponseMixin``

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

  * ``MultipleObjectMixin``

    It provides both get_queryset() and paginate_queryset().
    It uses the queryset or model attribute on the view class to get
    queryset.

    - ``model`` 定义这个 view 是操作在什么 model 上的.
      Specifying ``model = SomeModel`` is really just shorthand for saying
      ``queryset = SomeModel.objects.all()``.

    - ``queryset`` 自定义数据集.

    - ``context_object_name``

    - ``get_queryset()`` method 动态自定义获取的数据集.

  * ``MultipleObjectTemplateResponseMixin``

  * ``ContextMixin``

    Every built in view which needs context data, such as for rendering a
    template (including TemplateResponseMixin above), should call
    get_context_data() passing any data they want to ensure is in there as
    keyword arguments. get_context_data() returns a dictionary; in
    ContextMixin it simply returns its keyword arguments, but it is common
    to override this to add more members to the dictionary.

    - ``get_context_data()`` 自定义 context.

  * ``SingleObjectMixin``

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

  * ``SingleObjectTemplateResponseMixin``

  * ``FormMixin``

    - ``form_class``

    - ``success_url``

    - ``form_valid()`` POST valid data 时调用.

    - ``form_invalid()`` POST invalid data 时调用.

  * ``ModelFormMixin``

    - ``fields`` 选择生成的 ModelForm 要包含的 fields.
      该参数或者 ``form_class`` 必选一.

    - ``model``, ``get_object().__class__`` ``queryset.model``
      三者之一决定这个 view 所使用的 ``ModelForm`` 是什么.

    - 若未提供 ``success_url``, 使用 ``Model.get_absolute_url()``.

    - ``form_valid()`` 调用 ``form.save()`` 保存 model instance.

    - ModelFormMixin 和一些 form 类型的 view 结合, 成为具体的
      CreateView, UpdateView.

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

file upload
===========

* 上传文件都是 ``UploadedFile`` instance.

* 使用 ``.chunk()`` method 或者 ``.read(<size>)`` 来渐进地读取文件内容,
  避免大文件占用过多内存.

* upload handler.

  - 默认 ``MemoryFileUploadHandler`` 和 ``TemporaryFileUploadHandler``.
    效果是小文件读入内存, 大文件写入硬盘.

* settings.

  - ``FILE_UPLOAD_MAX_MEMORY_SIZE``

  - ``FILE_UPLOAD_TEMP_DIR``

  - ``MEDIA_ROOT``

template
========

general
-------

template backend
~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~

- Context object 在通用 API 中是纯粹的 dict.

template loaders
~~~~~~~~~~~~~~~~

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

* string literal. 模板的 tag 中出现的 string literal 将原样出现在 html 中,
  注意这些 string literal 是 verbatim 出现在 html 中, python string 的各种
  ``\`` 转义是不支持的. 或者说, 这些字符串相当于 python raw string.

* 为了结构清晰, 应该把不同 app 的模板放在各自目录下的 ``templates/<app>/`` 下面.

* template 中 object 的 ``.`` operator 的查找顺序:
  dict key, object attribute, list index.
  若 attribute 是一个 callable, it'll be called with no argument.
  django 不允许 callable 输入变量, 是为了避免对可以执行函数这个功能滥用.
  数据应该在 view 中计算完成再传入 template 进行渲染, 而不是在 template
  中才计算.

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

filters
~~~~~~~

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

- ``cut``

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
~~~~

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

- ``block``, parent template 中定义的 blocks 越多越好. 这样增加了页面区域的
  模块化, child template 只需覆盖或扩展需要修改的 blocks.

  * 对于扩展而非覆盖整个 block, 可以用 ``block.super`` tag 引用父模板中的同名
    block 内容.

  * 使用 ``{% endblock <name> %}`` 增加可读性.

  * template blocks 表达的是模板结构的继承关系, 所有的 block 在 compile time
    resolve 成为模板代码 (类似 cpp 和 c 的关系). 此后再也没有 block tag.
    在 runtime, 模板代码去 render context, 生成页面.
    因此, 不能通过某种 runtime 条件判断让 block 出现、消失或重定义.

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

- ``debug``, 输出 debug 信息.

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
~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~
django template 默认 escape output of every variable tag.
template 中的 string literal 没有被 html escape, 而是原样包含在 html 中.

disable auto escaping:

- 在变量级别上, 使用 ``safe`` filter.
  
- 在 block 级别上, 使用 ``autoescape`` tag 来开启或关闭 auto escaping.
  ``autoescape`` tag 的影响包含在 child template 中的同名 block.

- 在代码中, 使用 ``make_safe()``

安全性问题. 默认对模板变量的 auto-escaping 有助于避免 XSS attack. 若要
disable auto-escaping, 需小心谨慎.

context objects
~~~~~~~~~~~~~~~

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

static file
===========

* static file namespace 与 template namespace 机制类似.

* template tags.

  - 使用 ``static`` template tag 来自动根据 ``STATIC_URL`` 生成 static file
    的 url, 不要把静态文件的 url 写死在 html 里. 这样, 真正的 url 会根据
    ``STATICFILES_STORAGE`` 的机制去生成, 这样只需要设置
    ``StaticFilesStorage`` 或 某个 CDN 的 storage 实现, 就可以轻易切换所有
    url 的指向, 真正做到了单一变量没有重复.

    ``static`` tag 支持 ``as``, 只赋值不输出.

  - ``get_static_prefix``, 获取 STATIC_URL, 自定义 url 补全, 支持 ``as``.

  - ``get_media_prefix``

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

- 全局性质的 (属于整个 project 而不属于某个 app 的) templates 和 static files 应该放在
  ``$BASE_DIR/<project-name>/{templates,static}``.

test
====

* model 层的 test 的测试点是测试 model 的正确性、合理性;
  view 层的 test (配合 urlconf) 测试的是操作是否符合预期.
  因此前者手动操作数据库, 而后者模仿 useragent 用 client.

* 每个 test method 执行结束后数据库状态都会被重置.

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

migration
=========

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
  必要时需要手动修改甚至手动创建 migrations. 对于自动生成的 migrations, 尤其是
  ``squashmigrations`` 生成的 migration file, 一定要测试可用.

* ``makemigrations`` 和 ``migrate`` 操作一般不要限制 ``app_label``, 要对所有 apps
  同时进行. 因为 model 之间经常是相互依赖的. 如果只对某个 model 更新数据库状态
  可能 break dependency.
  在特殊情况下, 要限制 migration file 修改在某个 app 中, 此时采用 app label.

* migration definition.

  - 每个 migration 必须是名为 ``Migration`` 的 class, 且为
    ``django.db.migrations.Migration`` 的子类. 其中包含 ``dependencies``
    ``operations`` 等属性.

  - 每个 migration operation 是 ``Operation`` class 的 (子类的) 实例.

* 若要在 migration 中删除/重命名某个 model 或者删除它的数据, 必须设置
  dependency 保证依赖于原 model 和数据的 migration 执行在先.

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

* 在 migration 中无法访问 model 中定义的 methods. 解决办法是在 migration 中
  再定义一遍. 由于 migration 只代表在确定历史状态下的操作, 所以这种重复不造成
  问题.

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

* 只有用户明确 logout 时, 才会主动从 session store 中删除这条 session entry
  (通过 ``logout()``). 对于 persistent session store, session 从不自动删除,
  即使过期. 因此需要定期执行 ``clearsessions`` 命令删除过期 session.
  对于 cache-based session store, 显然不存在这个问题.

form
====

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

    * ``FileField``, bound 之后的值 ``.value()`` 是 ``UploadedFile`` instance.

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

    * ``blank=True`` 对应 ``required=False``. 由于默认 Field option ``blank=False``,
      因此默认 ``required=True``.

    * ``verbose_name=`` 对应 ``label=``.

    * 若 model field 有 ``choices``, form field ``widget`` 默认是 ``Select``.

  - methods.

    * ``.save()``

      ``.save()`` 可以直接保存新的 model instance 或更新现有的
      instance (若 constructor 有 ``instance`` 参数). 它会进行验证.
      它调用 ``Model.save()``.

      ``commit=False`` 时并不将数据存入数据库, 而是只返回 model instance.
      若 model 存在 ManyToManyField 需要修改或创建, ``commit=False`` 显然
      不会创建在 form 中选定的那些关联. 这样, 若手动执行 ``Model.save()``
      来保存实例的话, 之后需要使用 ``ModelForm.save_m2m()`` 单独保存选定
      的关联关系至数据库.

      若 model 中定义了 ``FileField`` 且 form 中传入了相应文件, ``.save()``
      会自动将文件保存至 ``upload_to`` 位置.

* 当一个 form 与某个 model 对应时, 使用 ``ModelForm``, 否则使用 ``Form`` 即可.

* 很多对象 render 为 html 形式后会添加标识 id 和样式 class. 方便进行前端自定义.

* form inheritance. ``Form`` 类继承时, 父类的列在先, 子类的列在后.
  对于多继承, 列的先后顺序根据各父类的远近关系按由远至近的顺序.
  这里的远近关系值的是在 MRO 中的顺序的逆序, 在 MRO 中越靠后越远.

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
    还可以设置 ``field = None`` 在子类中去掉特定列.

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

* ``abstract``, whether is abstract model.

* ``app_label``, 定义 model 所属的 app.

  对于在其他 app 中已经定义的 model, 可在 import
  过程中修改 ``model._meta.app_label`` 的值修改它所属 app.

  注意无论是在 Meta 中修改还是其他修改方式, 这直接改变了 django 看待这个 model
  所属于的 app. 因此这导致相应的 migration 必须被创建和应用. 因此, 不能通过
  这个方式修改 django contrib app 的 models. 因为这会修改这些应用的 migrations.

* ``db_table``

* ``default_related_name``, 对于 relation field, ``related_name`` 的默认值.
  默认是 ``<model>_set``. 同时也是 ``related_query_name`` 的默认值.

* ``get_latest_by``, ``QuerySet.latest()`` ``QuerySet.earliest()`` 默认
  使用的 field name.

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

* ``default_manager_name``. 指定 ``Model._default_manager`` 使用哪个名字的 manager.

model field
-----------

* options.

  Many of Django’s model fields accept options that they don’t do anything with.
  This behavior simplifies the field classes, because they don’t need to
  check for options that aren’t necessary. They just pass all the options
  to the parent class and then don’t use them later on.

  - primary key:

    可以用 ``primary_key=True`` 设置某个 field 为 primary key, 否则 django 自动
    给 model 添加 id field 作为 primary key

    .. code:: python
      id = models.AutoField(primary_key=True)

    The primary key field is read-only. If you change the value of the primary key
    on an existing object and then save it, a new object will be created alongside
    the old one.

  - ``default`` 仅在 SQL 中创建 entry 时该列的值未指定时生效, 而不是
    ``field=None`` 时. 后者情况是指定了该列, 但值是 null. 默认情况下
    ``default=None``, 但是否能顺利使用该 default value, 还要看该列是否允许
    null, 即 ``null=`` 的配置.

  - ``blank`` 若为 True, form 中允许该项为空

  - ``null`` 默认是 False, 此时 create table 时有 ``NOT NULL``, 且不允许
    field 值为 None; 若 True, create table 时有 ``NULL``, 且允许 field 值
    为 None.

    ``blank`` 是规定 form validation 时是否允许空值.
    两者的意义是不同的.
    ``null`` 和 ``blank`` 的默认值都是 ``False``.

  - ``choices`` 设置 field 的可选值, 其值是 a iterable of ``(value, description)``
    pairs. 每个选项的值的 symbolic enum 形式和整个选项 列表应设置在 model
    class 中. 这是为了方便后续在查询等操作中使用. 设置该选项后, 默认的 form
    形式会变成 (multiple) select box. Given a model instance, the display
    value for a choices field can be accessed using the ``get_FOO_display()``
    method.

  - ``help_text`` 设置该列值的更详细的帮助信息. ModelForm 会使用它.
    其字符串值在 form 中直接显示, 不会被 escape. 因此可以加入 html 语法.

  - ``error_messages`` overrides default validation error messages.

  - ``verbose_name``, 对于非关系型 field, 该参数是第一个 kwarg, 因此经常以
    positional 形式写出; 对于关系型 field 必须以 kwarg 形式写出.

  - ``db_index``, 是否创建 single field index.

  - ``validators``, 指定 validators. 这些 validators 会在 form validation
    或 model instance validation 的时候生效.

* ``Field`` methods.

  - Field deconstruction: ``Field.deconstruct()``

  - ``db_type()`` 给出底层数据库对应的实际 field type.
    若这个方法返回 None, 则生成的 SQL 会直接跳过这个 Field.

  - ``rel_db_type()`` 决定指向这个 Field 的 Field 的数据库类型.
    这被 ForeignKey, OneToOneField 等使用. 也就是说, 当创建一个 field A reference
    另一个 field B 时, B 的 ``rel_db_type()`` 决定 A 的数据库类型.

  - ``from_db_value()``

  - ``to_python()``

  - ``get_prep_value()``

  - ``get_db_prep_value()``

* custom field type.

  - You can’t change the base class of a custom field because Django won’t
    detect the change and make a migration for it. Instead, you must create a
    new custom field class and update your models to reference it.

* field types. 所有 field types 都是 ``Field`` 子类.

  - IP address 用 ``GenericIPAddressField``.

  - 实数一般用 ``FloatField``, 精确要求时考虑 ``DecimalField``.

  - 整数有 ``IntegerField``, ``PositiveIntegerField``, ``BigIntegerField``,
    ``SmallIntegerField``, ``PositiveSmallIntegerField``.

  - ``DateField`` ``DateTimeField``

    * 在 python 中以 datetime.date, datetime.datetime 分别表示.

    * ``auto_now_add`` 适合做 create time;
      ``auto_now`` 适合做 update time.
      这些参数在调用 ``Model.save()`` 来保存时才有效, 通过其他途径修改数据
      时不会生效.

      若只是想设置默认值, 那就用 ``default=``, 别用这两个选项.

      ``auto_now``, ``auto_now_add`` 和 ``default`` 是互斥的.

      设置这两个参数, 意味着该列不能手动修改, 并且即使包含在了 form 中,
      也不是必须输入的项 (即不是 required). 因此, django 自动设置
      ``editable=False`` 和 ``blank=True``.

  - 若要允许在 ``BooleanField`` 中存 NULL, 使用 ``NullBooleanField``.

  - ``SlugField`` 要配合 ``slugify`` 函数使用, 只应该在创建 instance 时保存该列值.

  - ``FilePathField`` 要求值必须是满足路径匹配条件的文件路径.

  - ``JSONField``. postgresql 可以使用 native JSONField, 对于 mysql 可以使用
    django-jsonfield module 用 TextField/CharField 模拟.

* relation field: many-to-one.

  - 多对一的映射关系用 ``django.db.models.ForeignKey`` 实现.

  - foreign key field 的名字应该是所指向的 model 的名字的全小写版本.

  - ForeignKey field 默认设置 ``db_index=True``, 即默认建立该列的索引.

  - ``ForeignKey`` field 在数据库中命名为 ``<field>_id``, 除非用 ``db_column``
    自定义.

  - 若 ``ForeignKey`` field 支持 ``null=True``, 则对这个属性赋值 None 即可去掉关联.

  - 对各种 relationship field, 若要指向可能尚未定义的列, 用字符串
    ``[app_label.]model`` 代替 model object.

  - constructor parameters.

    * ``on_delete``

      虽然默认是 ``CASCADE``, 但 django 2.0 之后将变成 required parameter.
      如果对象之间的关系不是必须的, ``on_delete`` 应该设置成别的值:

      - 若该条数据必须随指向的数据共存亡, ``django.db.models.CASCADE``.

      - 若只要 FK 关系仍存在就禁止删除原数据, ``django.db.models.PROTECT``.

      - 若需设置为 NULL 以表示不指向任何东西, ``django.db.models.SET_NULL``.

      - 若需设置为默认指向的东西, ``django.db.models.SET_DEFAULT``.

      - 若需自定义设置逻辑, ``django.db.models.SET(value|callable)``.

      - 啥也不干, 由数据库决定该怎么办, ``django.db.models.DO_NOTHING``.

    * ``limit_choices_to``, 限制 ModelForm 中该列的赋值范围.

    * ``related_name``, 自定义从 related object 反向获取时, related manager
      的名字. 默认是 ``Meta.default_related_name``, 后者的默认值是
      ``<model>_set``. 若不让 django 创建反向关系, set related_name to '+' or
      end it with '+'.

    * ``related_query_name``, 在 field lookup syntax 中, 从 related model
      向这个 model 反向查询时, 使用的名字. 若有设置 related_name 或
      Meta.default_related_name, 默认使用它们中的一个, 否则默认为 model name.

    * ``to_field``, 关联的 model 的 field, 默认是 primary key. 关联的 field
      必须有 unique constraint.

    * ``db_constraint``

    * ``swappable``, 默认 True 即可. 与 swappable AUTH_USER_MODEL 相关, 为了
      支持 custom user model.

* relation field: one-to-one.

  - 一对一关系一般用于一个模型作为另一个模型的延伸、扩展、附加属性等.
    ``OneToOneField`` 在 model 继承时用于定义父表和子表通过哪一列来关联.

  - OneToOneField 本质上是 ForeignKey 的一种特例. 前者是后者的子类.

  - one-to-one field 在 mysql 中实现时, 实际上是一个普通的 field (类型与指向
    的 model 的 primary key 一致), 配合 unique key constraint 以及 foreign key
    reference constraint.

  - OTO field 的 ``parent_link`` 结合 conrete model inheritance 时有特殊作用,
    它让父类的 field 可在子类即 OTO field 所在 model 中直接访问.

* relation field: many-to-many.

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

    * ``symmetrical``, 与 recursive M2M relationship 相关.

    * ``through``

      through model. 多对多关系实际上是通过一个关系表来实现的. 这个关系表的 model
      可通过 ``ManyToManyField.through`` attribute 获得. 并可以通过 ``through``
      option 来指定单独创建的 through model, 这可用于在 through model 中加入额外的
      状态信息等列.

      ``.through`` 属性在 field instance 是一个 RelatedManager to through model.

* recursive relationship: 若 relation field 需要与自身表建立关联, 使用
  ``"self"`` 作为 ``to`` 参数值.

  lazy relationship: 若 relation field 需与可能尚未建立的 model 建立关联,
  使用 ``[<app_label>.]<model>``.

model index
-----------

index 通过 ``Model.Meta.indexes`` option 指定, a list of Index objects.

``Index`` object.

* ``fields``, 指定单一索引或复合索引的列, 以及方向. 语法和 QuerySet.order_by
  相同.

* ``name``, index name.

* ``db_tablespace``.

model instance & form instance validations
------------------------------------------

* instantiation.

  - 在创建 model instance 时, 对于 FK field, 有两种指定方式:
    ``<FK-field>=<FK-model-object>``, ``<FK>_id=<FK-model-object>.{id|pk}``.
    这不同于 field lookup, 不支持 id 和 object 交叉混合的方式.

* 在定义 model class 时, 要考虑应该在 model 层就限制的数据合法性要求.
  这包括:

  - 对于 model field, ``validators``.
    对于自定义 model fields, 还可以自定义 field 的 clean methods 等.

  - 对于 model 内各数据之间的制约关系, 自定义 model 的 clean methods 等.

* model instance validation.

  ``.save()`` 时不会自动调用 ``.full_clean()`` (因 form 验证时会执行它),
  若 model instance 不是来源于上层 form, 这验证操作必须手动执行. 或者
  等着数据库下层报错.

  ``Model.full_clean()`` 默认只进行数据库层 data integrity 方面的检验.
  field 中的很多限制条件, 例如 ``choices``, ``blank``, 以及一些 field type, 例如
  ``FilePathField`` 等, 本身不能限制存储的值, 因为这些条件不能在数据库中表达.
  这些条件只有配合 ``ModelForm`` 使用, 才能有用.

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
- 对于 model class 在实例化时, Django doesn’t hit the database until you
  explicitly call ``save()``.

- ``INSERT`` 和 ``UPDATE`` 都是用 ``.save()`` 实现.

- 对实例中 ``ForeignKey`` ``OneToOneField`` 等指向单一 model 实例的 field 赋值时
  使用相应 model 的 instance 即可.
  实例中的 ``ManyToManyField`` 实际上是一个 Manager object, 需要用 ``.add()`` 给
  这个集合中增加关联关系. ``.add()`` 接受一次传入多个对象, 建立多个映射.

QuerySet
--------
- QuerySet 封装了 database entries 数据以及对数据的 CRUD 和聚合等操作.

- 获取对象的各个方法在 ``Manager`` 和 ``QuerySet`` 中都有 (在 QuerySet 中定义,
  expose to Manager 中), 且可以串联在一起. ``.delete()`` 是唯一的 QuerySet 有
  但 Manager 的没有的方法 (为了避免误删全部).

CRUD
~~~~
* attributes & methods.

  - ``ordered``, QuerySet 是否有排序.

  - ``.all()``

  - ``.filter()``

  - ``.exclude()``

  - ``.get()``, 生成的 sql 与 ``.filter()`` 的相同, 也就是说取回的
    queryset 可能是多行的, 没有在数据库层做 LIMIT 1 之类的限制.
    而是在 python 中检查返回的是否为一行, 若不是则 raise DoesNotExist
    或者 MultipleObjectsReturned.

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

  - ``exists()``, 判断某项是否在 queryset 中. 这比 ``in`` operator 高效,
    后者必须遍历整个 queryset.

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

- ``select_related()``.
  如果用户在查询某模型时, 已知会访问到关联的 FK 对象, 可使用 ``select_related()``
  来强制进行 JOIN 操作, 一次把所有 FK 对象数据取回来, 这样更高效. 避免获取各个
  FK object 时再单独访问数据库. To avoid the much larger result set that would
  result from joining across a ‘many’ relationship, ``select_related`` is limited
  to single-valued relationships - foreign key and one-to-one.

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

aggregation
~~~~~~~~~~~

* 两种聚合方式: ``QuerySet.aggregate()``, ``QuerySet.annotate``.

* ``QuerySet.aggregate()``: 给整个 QuerySet 生成各种聚合值.

  - 需要执行的聚合操作通过 positional args 或 keyword args 来指定.
    返回聚合结果 dict. key 是聚合项, value 是聚合值. key 自动根据
    field name 和聚合操作名生成; 或者通过 keyword 参数指定.

  - 由于返回一个 dict, 所以 ``.aggregate`` 要作为 QuerySet chain 的最后操作.

* ``QuerySet.annotate()``:

  给 QuerySet 里的每个元素生成聚合值. 这不仅仅可用于 ``GROUP BY`` 聚合,
  还可用于对每行返回所需的运算结果, 即 annotate 的一般含义. 使用这个一般
  意义, 还可以进行 sql ``SELECT name AS name2`` 操作:
  ``queryset.annotate(name2=F("name"))``.

  - annotate 语法与 aggregate 相同, 但是每个聚合值是 attach 到各个
    元素上的, 成为元素的 attribute.

  - 由于结果成为了 attributes, 返回的仍是一个 QuerySet, 因此可以继续
    operation chain.

  - annotate 增加的 attributes 可以在后续的 operation chain 中使用, 例如
    用于进一步 ``filter()``.

  - 使用 annotate 进行多项聚合时必须要谨慎, 很可能结果不对, 并且必要时检查
    生成的 raw sql statements. 多项聚合结果可能错误的原因是 django 简单
    地将多项聚合条件涉及的所有表 join 在一起, 然后再算聚合值.

  - 一般意义的 GROUP BY 操作:

    若 queryset operation chain 中, ``.annotate()`` 前面有 ``.values()``
    或 ``.values_list()`` 且它们指定了列参数 (不是无参的), 则 annotate 时
    的 GROUP BY 会使用这些列来分组, 不再使用原 model 的 pk. 此时, annotate
    的结果不再与各个 model instance 对应. 这样, 生成的组不再局限于 model
    instance.

    注意, 此时 ``.values()`` ``.values_list()`` 选择的列, 以及 ``.annotate()``
    中新增的列, 是在 GROUP BY 之后进行的. SQL 对应为
    SELECT `values, values_list columns and annotate columns` FROM `some_table`
    GROUP BY `values and values_list columns`.

    需要明确, 当 annotate 出现在 ``.values()`` ``.values_list()`` 后面时,
    并不是说只剩下了它们选择出来的列, 而是在最终构建的复合表 (包含 GROUP 之后)
    中取出这些列. 所以, annotate 仍然可以访问所有在这个复合表中存在的列, 它
    不限于 values, values_list 的列.

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

raw SQL
~~~~~~~
``QuerySet.raw()`` 和 ``Manager.raw()``.
输入 SQL statements, 输出 ``RawQuerySet``.

Should be used sparingly and carefully.

Field lookups
~~~~~~~~~~~~~
各种过滤和获取的方法的参数语法, 对应到 SQL ``WHERE`` clause.
Syntax: ``<field>[__<field>...][__<lookuptype>]=value``.
若省略 lookuptype, 默认是 ``exact``.
常用 lookuptypes: ``exact``, ``iexact``, ``contains``, ``icontains``,
``startswith``, ``endswith``, ``istartswith``, ``iendswith``.

* 对 foreign key field 指定条件, 可以用以下方式进行判断: 1. FK 列 与 FK object
  实例进行比较; 2. FK 列 与 FK 值进行比较; 3. 使用 ``<FK>_id`` 虚拟的列
  和 FK 值进行比较.

* 对 many-to-many 关系进行 lookup 时, 由于实质上是在 through table 中对
  FK 指向的 entry 进行匹配, 所以虽然起点处写的是 plural 形式, 但实际上是
  单行的匹配概念: 对这个对象关联的所有对象进行单行的匹配, 只要有一行匹配
  上了, 就认为 main object 符合条件. e.g.,

  - ``Group.objects.filter(users=jack)``, 筛选包含 jack 的组. 对每个组 join
    through table, 然后进行单行匹配筛选.

  - ``Group.objects.filter(users__in=[jack, michael, jane])``, 筛选包含这些
    用户的组.

  注意, 由于 table JOIN 操作, 这样的匹配很容易在结果集中出现重复的 object,
  所以需要对结果去重.

* 对于表达关系的列, 可以从多至一的方向深入被指向的模型进行筛选, 这抽象了各种
  SQL ``JOIN``.

* 这种过滤可以反向进行, 即从一至多的方向进行筛选. 注意这与属性访问时得到
  RelatedManager 虽然语法相通, 但意义不同. 这里是通过对 related model 的行
  指定筛选条件, 来筛选 main object.

  reverse lookup 的起点是那个 model 中设置的 relation field 的
  related_query_name 值. 在此之后再指定 related model 中的 field 和条件.

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

query expressions
~~~~~~~~~~~~~~~~~

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

- related manager. 一对多、多对多关系中, 正向的 manager object (如果有) 是属性名,
  逆向的 manager object 默认是 ``<lower_model>_set``, 可通过 ``related_name``
  自定义. 在一对一的关系中, 正反向都是对称直接访问的.

- ``RelatedManager`` 的一些方法: ``add()``, ``create()``, ``remove()``,
  ``clear()``, ``set()``. 这些操作都是立即在数据库生效的.

BaseManager
~~~~~~~~~~~
attributes.

* ``auto_created``. 该 manager 是否是自动创建, 而不是在 model class 中明确定义的.

* ``model``. The attached model class.

Manager
~~~~~~~

每个 model 都有至少一个 ``Manager`` instance, 用于进行 table-level operations.
``Manager`` instance is accessible only via model class, rather than from
model instances, to enforce a separation between “table-level” operations and
“record-level” operations.

Manager object 是对某个 model 进行表级别的数据库的起点. 它将所有合适的 QuerySet
methods 都 attach 到这个 manager class 上. 它的本质是从 manager object 上访问
任何 queryset method 的时候, 都立即创建一个 QuerySet object, 然后就是正常的
queryset methods 操作.

methods.

- 从 QuerySet 复制过来的各种 methods. 复制标准:

  * Public methods are copied by default.

  * Private methods are not copied by default.

  * ``queryset_only=True`` methods are not copied.

  * ``queryset_only=False`` methods (even if private) are copied.

specify manager in model
~~~~~~~~~~~~~~~~~~~~~~~~
- 当定义 model 时, 若不明确指定 manager (无论是修改 manager name 还是 custom
  manager class), 则会自动生成 ``objects = Manager()`` manager. 若明确设置,
  可以设置任意个 managers. This is an easy way to define common “filters” for
  your models.

- default manager.

  ``Model.Meta.default_manager_name`` 或 model class 中第一个定义的
  manager object 当作 ``_default_manager``.

  当程序逻辑需要使用未知 model 的 manager 时, 应使用 default manager,
  而不该假设 ``objects`` manager 存在.

- base manager. 当通过一个 model instance 访问 related objects 时, 使用
  related model 的 ``_base_manager`` 获取 queryset (再筛选出关联的 entries),
  而不是使用 ``_default_manager``. 这是因为 default manager 可能进行了一些
  过滤和限制. 而默认情况下 base manager 不使用 model class 中定义的一系列 
  managers. 而是使用最通用的 ``django.db.models.Manager``.

  ``Model.Meta.base_manager_name`` 可以指定使用预定义的某个 manager 作为
  base manager.

custom manager
~~~~~~~~~~~~~~
subclass ``django.db.models.Manager`` 以进行自定义.

- 添加 custom manager method. 用处: 当需要对 models 添加 table-level 的功能
  和操作时 (而不是对 row-level 即具体 model instance 的方法.)

- customize initial queryset. override ``get_queryset()`` method.
  ``Manager.all()`` method 的返回值与之一致.

若自定义了 QuerySet 的 methods, 然后希望这些方法也 expose 到 manager 中,
需要使用 ``QuerySet.as_manager`` classmethod 创建 manager class. 它调用
``BaseManager.from_queryset`` class method.

自定义的 manager class 必须能够 shallow copied by ``copy.copy()``.

in model inheritance
~~~~~~~~~~~~~~~~~~~~
- model 继承 parent model 定义的 managers. 标准的 python inheritance 机制.

- 若 model 和 parents 都没定义 managers, 自动创建 ``objects`` manager.

- default manager 若没指定, 使用该 model 中定义的第一个 manager 或 parent
  model 的 default manager.

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
  逻辑时, 就可以通过这个 hook 加入代码.

* low-level APIs.

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
~~~~~~~~
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
~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~
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

  * ``email_user()``. 为啥有这么个奇葩的方法放在这里?

User
~~~~
User 只是将抽象的 AbstractUser 具体化成实际模型所建立的 placeholder class.
它本身并不定义任何额外的内容, 除了 Meta.swappable. 这样便于 project 自己
去自定义 User model. 即直接 subclass AbstractUser 即可.

- fields, attributes

  * ``groups``.

  * ``user_permissions``.

- methods.

  * ``has_module_perms(<app>)``, 判断用户是否在某个 app 中有至少一个权限.

AnonymousUser
~~~~~~~~~~~~~
AnonymousUser implements basic interface of AbstractUser.

``AnonymousUser`` 虽然不具备很多 ``User`` 的属性和方法, 但是可以进行
认证检查和权限检查. 因为很多时候网站是允许匿名用户的.

在权限方面, AnonymousUser 没有任何组权限, 但注意对于它个人的权限并不一定
是什么都没有, 而是取决于 auth backend.

在认证方面, AnonymousUser 的 ``is_authenticated`` ``is_anonymous`` 分别是
只读的 False/True.

扩展和自定义 user model
~~~~~~~~~~~~~~~~~~~~~~~

- proxy model to auth.User: purely behavioral extension, use proxy model.

- one-to-one relation to user model:
  store additional information (profile-like infos) related to a user,
  but not auth-related, create new model with ``OneToOneField`` to user model.

  为了在用户创建、删除等操作时两表同步, 需要使用 signal.
  在 admin site 中使用 InlineModelAdmin 同时编辑 user model 和 profile model
  信息.

- custom user model:
  default User model just does not fit your need, create custom user
  model as ``AUTH_USER_MODEL`` to override the default. AUTH_USER_MODEL
  的形式和 relationship field 中引用 field 的形式相同: ``[app_label.]model``.

  即使 User model 已经足够, 也应该使用自定义的 user model, 这样方便之后
  进行扩展.
  If you’re starting a new project, it’s **highly recommended** to set up a
  custom user model, even if the default User model is sufficient for you.
  This model behaves identically to the default user model, but you’ll be
  able to customize it in the future if the need arises.

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

- 用户相关的信息的存储位置.

  * 若这些信息是 app-specific 的, 而不是用户本身的属性、通用的信息或认证和权限
  相关的信息, 则应该存在 app models 中, 添加对 user model 的 one-to-one
  relation, 这样是解耦合的.

  理由: 1. 当多个 app 需要添加相似的 user model 关系, 若直接与 user model 建立
  关系, 则可能出现冲突, 因此降低了 app 的重用价值. 若与 app 自己的 user profile
  model 建立关系, 在由它统一与 user model建立关系, 则大大降低了冲突的可能.
  2. 假如需要途中替换 user model, 若统一通过 profile model 间接建立关联, 则
  每个 app 只需更新 profile model 与 user model 的关联; 若各 model 直接与 user
  model 关联, 则需要更新所有关联.

  * 若是属于用户本身, 甚至是用户认证相关的属性, 才应该放在 user model 中.

  然而这涉及到在创建 user model instance 时需要创建 one-to-one relation
  model instance. 尤其是调用 auth app 提供的各种 create_user, create_superuser
  之类的方法时需要自动创建关联表中的实例, 这样才能保持解耦合效果 (若不能自动
  创建, 而需要 override 用户创建方法加上 one-to-one field 的话, 则又耦合回来
  了). 做到自动创建, 需要使用 signal framework.

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

Permission and Authorization
----------------------------

- 每个 app 的每个 model 都默认存在 add, change, delete 三个权限. 这些权限
  是在 Model.Meta.default_permissions 定义的.

- 权限检查 ``User.has_perm(<app_label>."add|change|delete"_<model>)``

- 一个用户或一个组可以有任意个权限 (many-to-many). 组具有的权限用户自动具有.

Permission
~~~~~~~~~~
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
~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

  ``settings.LOGIN_URL``, default ``/accounts/login``. 该值可以设置为
  url pattern name.

  ``settings.LOGIN_REDIRECT_URL``, 登录后的默认跳转路径.

  ``settings.LOGOUT_REDIRECT_URL``, 登出后的默认跳转路径.

authentication views
~~~~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~~~

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
~~~~

- ``auth.urls`` 提供了完整的 auth urls 和 view 实现. 这些 url 是没有
  namespace 的. 在使用时可以直接放在 url root path 上, 或者 ``include()``
  中设置 namespace.

authentication signals
~~~~~~~~~~~~~~~~~~~~~~

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

  * ``get_user()``, takes a user_id – which could be a username, database ID or
    whatever, but has to be the primary key of your user object – and returns a
    user object.

  * ``authenticate()``, takes a request argument and credentials as keyword
    arguments, return a user object that matches those credentials if the
    credentials are valid. If they’re not valid, it should return None.

  Optional: 权限类方法. 在 AbstractUser 上调用这些方法时, 会 delegate 至各个
  定义了这些方法的 backend 去执行. 即遍历 AUTHENTICATION_BACKENDS 检查是否定义了
  所需的方法.

  各个 backend 给出的权限的并集是用户的相应部分权限.

  * ``get_group_permissions()``

  * ``get_all_permissions()``
    
  * ``has_perm()``

  * ``has_module_perms()``

ModelBackend
~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~~~~~~~~
允许 inactive user 认证. 但仍然没有任何权限.

这是 ModelBackend 的子类.

RemoteUserBackend
~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
允许 inactive user 认证. 但仍然没有任何权限.

这是 RemoteUserBackend 的子类.

middlewares
-----------

AuthenticationMiddleware
~~~~~~~~~~~~~~~~~~~~~~~~

根据 request 中 cookie 保存的 session 信息进行自动的用户识别和认证, 避免每次访问
都要登录.

调用 ``auth.get_user()`` 操作, 后者从 session 中获取到 user id 之后, 还会校验
存储的 session auth hash 与从 user instance 中计算得到的是否一致. 若不一致,
则 flush session, 设置 AnonymousUser. 对于 AbstractBaseUser, 效果是在修改密码
后会自动登出用户, 要求 重新登录.

若认证成功返回 user instance, 否则返回 AnonymousUser.
无论认证的结果是什么用户, 都保存在 ``request.user`` 上.

RemoteUserMiddleware
~~~~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

没有 header 时也不 logout user. 它是 RemoteUserMiddleware 的子类.

Useful for setups when the external authentication via ``REMOTE_USER`` is only
expected to happen on some "logon" URL and the rest of the application wants to
use Django's authentication mechanism.

view mixins & decorators
------------------------
以下 decorators and mixins 提供在各个 app 的 view 中提供用户认证和权限管理.

decorators
~~~~~~~~~~

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
~~~~~~
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
MRO 的最左边.

- ``LoginRequiredMixin``

- ``PermissionRequiredMixin``

  class attribute.

  * permission_required.

- ``UserPassesTestMixin``

  methods.

  * ``test_func()``. 要进行的检查.

context processors
------------------

django.contrib.auth.context_processors.auth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

applications
============

配置 app
--------
settings.INSTALLED_APPS 中一定要写 path to AppConfig class, 即
``<app>.apps.<app>Config``. 这是应用自定义 app config 的最佳方式.

若 INSTALLED_APPS 中只有 app module path, 则 django checks for
``<module>.default_app_config`` for app config class. 这仅用作
向后兼容.

若没找到自定义的 app config, fallback 至 ``django.apps.AppConfig``.
但这样就无法使用 custom app config.

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

- ``Signal.connect()``

- ``django.dispatch.receiver()`` decorator.

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
~~~~~~~~~
添加 ``csrf_token`` form input. 作为 form data 的一部分 POST 至服务端.

ajax post
~~~~~~~~~
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

- ``CSRF_COOKIE_SECURE``

- ``CSRF_HEADER_NAME``

- ``CSRF_FAILURE_VIEW``

- ``CSRF_TRUSTED_ORIGINS``

Pagination
==========

- 若 pagination 是由前端 js library 去实现 (例如 datatables), 只传递给后端所需
  页的第一个记录的 id 以及记录数目, 则没必要在 view 中使用纯后端的 paginator.
  只需返回前端任何它需要的数据即可.

Serialization
=============

JSON
----

- DjangoJSONEncoder 在 ``json.JSONEncoder`` 基础上, 额外支持:
  datetime.datetime, datetime.date, datetime.time, datetime.timedelta,
  decimal.Decimal, django.utils.functional.Promise, uuid.UUID.

django-admin
============

* ``./manage.py shell`` 启动 shell 并加载项目相关 django 配置; 这相当于
  执行了:

    .. code:: python

      os.environ['DJANGO_SETTINGS_MODULE'] = "<project>.settings"
      import django; django.setup()

* ``makemigrations --dry-run`` 可用来检查当前记录的数据库结构 (通过
  migration files 来体现) 是否和 models 里的模型代码保持一致.

* ``clearsessions`` 清除过期的 session data. django 不提供自动清理
  session 的机制. 可以定期执行这个命令手动清除过期的 session.

* ``runserver``.

  对于 runserver 输出的请求相应日志, 每一行是在该请求结束后才输出, 因此
  才记录有 method, url, http version, status code 等信息.

* ``dbshell``

  似乎不会使用平时 django 运行时传入的 OPTIONS 参数.

在独立的程序或脚本中使用 django
===============================

- 使用当前项目完整配置.
  .. code:: python

    os.environ['DJANGO_SETTINGS_MODULE'] = "<project>.settings"
    import django; django.setup()

django release
==============

- new feature release (A.B, A.B+1) every 8 months.
  new LTS release (X.2) every 2 years, LTS is supported with security updates
  for 3 years.
  each version following an LTS will bump to the A+1 major version number.
  patch release (A.B.C, A.B.C+1) will be issued as needed.

- 1.11 LTS is the last version supporting python2.

- Django 2.0 和 1.11 相比, 不是特别大的区别, 不充满 breaking changes,
  而是连续的演进. 只是版本号规范的重新定义.

plugins
=======

reusable django packages 可以从 django packages 网站查询. 这个网站的好处是,
对于一个 package, 它上面有详细信息, 包含版本支持情况, 最近更新时间, 有多少
人在使用, 以及同类 packages 之间的比较 grid.

django-nested-admin
-------------------

django-jsonfield
----------------

django-auth-ldap
----------------

添加一个 LDAPBackend 即可. 不需要单独的 middleware. 所以在 LDAP 认证之后,
登录状态与平时一样, 通过 session + AuthenticationMiddleware 维持.



authentication
~~~~~~~~~~~~~~
authentication methods.

1. Search/bind.
   Connecting to the LDAP server either anonymously or with a fixed account and
   searching for the distinguished name of the authenticating user. Then we can
   attempt to bind again with the user’s password.

2. Direct bind.
   Derive the user’s DN from his username and attempt to bind as the user
   directly.

user
~~~~
``LDAPBackend.authenticate()`` 在认证成功后会建立对应的 django 用户. 然后,

- 根据配置的 DN entry attributes 更新 user model fields.

- 执行 ``populate_user`` signal handlers, 进行任意的自定义修改.

- 根据 ldap 里组的情况, 设置用户和组的 M2M 关系.

对应的 django user 会设置 unusable password.

settings
~~~~~~~~
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
