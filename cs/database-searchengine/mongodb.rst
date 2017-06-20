- 3.0+ 默认的 storage engine 是 WiredTiger, 之前是 MMAPv1. 前者的好处是
  支持 document level 的 concurrent read write, 后者支持 concurrent read
  in one collection, 但是在 collection level 对 write 有锁.

- ``_id`` field 一定是 unique 的, 这是内秉的, ``_id_`` 不是通过 ``create_index``
  创建的 (所以也不能 ``drop_index``), ``unique`` 不是这个 index 的额外条件. 所以,
  在 ``index_information`` 的输出中, ``_id_`` index 没有 ``"unique": True`` 选项.

- mongo shell 中的 dict 能保证 key 的顺序和输入顺序一致, 但 python3.6 以下的 dict
  不能保证. 若想要在指定查询条件时保证 doc fields 的顺序, 可以使用 ``OrderedDict``.
  若想要让 client 返回的 doc 中 key 的顺序也保证, 需要指定:

  .. code:: python

    MongoClient(document_class=OrderedDict)

  python3.6 的 dict 已经能够保证 key 的定义顺序. 所以在 python3.6 中, 用 dict 就行.

- single field index

  索引的升降顺序无关紧要, 查询从哪个方向都可以进行. 索引的
  升降顺序不影响 sort 操作.

  * `index on embedded field` vs `index on embedded document`

    前者是指定 qualified field ``field.subfield`` 作为 index 的列, 即将 sub-doc
    中的列值加入 index; 后者是将 ``field`` 下的整个 sub-doc 加入 index.

- compound index

  复合索引中, field 的先后顺序很关键, 它决定这个索引中列的排序
  优先级. 先按照 k1 排序, k1 相同时再按照 k2 排序.

- multikey index

  当 doc 中要索引的 field 的值是一个 array, 每个值都会加入索引中, 它们都指向这个 doc.

- index limitations

  * 一个 index entry 的大小必须小于 1KB.

  * 一个 collection 最多能有 64 个 index.

  * fully qualified index names (``<db>.<collection>.<index-name>``) 的长度必须
    小于 128 chars.

  * 一个 compound index 包含的列数必须小于 32.

  * 一个查询不能同时使用 2 种 special index, 例如 geospatial 和 text.

  * 2dsphere index 只能包含图形类数据.

- build index

  * 对于 foreground index building, 在一个 collection 中创建 index 将导致它所在的
    整个数据库在此期间 block 所有操作. 这包括正在进行的 ``create_index``, 用其他
    client 执行的 ``find``, 等. 此外, 在 mongo instance 层, 任何需要获取对所有数据库
    的 read lock or write lock 的操作都会 block.

  * 如果在 build index 过程中仍需要访问数据库, 可以使用 background index building.
    注意正在创建 index 的 client 仍然处于 blocking 状态 (表示正在创建 index); 而其他
    client 可以进行各种操作. 注意, partially-built index 不会被使用, 此时的查询等
    操作如果必须的话将遍历整个数据库.

  * background 比 foreground index building 慢一些, 如果 index 比内存大, 将非常慢.

  * 由于潜在的 blocking 和性能问题, 无论是 foreground or background 索引构建操作,
    都应该在维护期间进行, 而不是在运行期间随时需要随时创建 (这说明数据库结构设计有问题),
    并且使用单独的维护代码创建索引. 业务应用程序应当在启动时检查所需索引是否存在,
    若不存在则报错退出.

  * 默认情况下, 若在构建索引过程中 mongod 死掉了, 重启后将立即开始重建索引 (删除未完成的
    索引, 重新构建). 所以, 如果之前是 background index building, 现在将变成 foreground.
    ``storage.indexBuildRetry`` 控制 mongod 是否自动恢复索引构建.

  * 在奇葩的 tokumx 2.0 版本中, ensure_index 不能随便执行, 在大数据量下会卡得很厉害, 即使
    相应 index 明明已经存在. (不知在正常的 3.4 版本中有没有这个问题.)

- query

  * 在奇葩的 tokumx 2.0 版本中, 大数据量时 ``find`` 后 sort 会卡得很厉害, 也许这实际上
    应归咎于数据结构 index 设计有问题.

- insert

  * 在奇葩的 tokumx 2.0 版本中, 插入新 doc 的操作与 ensure_index, find, sort 等有冲突,
    进行这些操作时不能写入.
