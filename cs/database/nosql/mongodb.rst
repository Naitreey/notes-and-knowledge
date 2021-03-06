- 3.0+ 默认的 storage engine 是 WiredTiger, 之前是 MMAPv1. 前者的好处是
  支持 document level 的 concurrent read write, 后者支持 concurrent read
  in one collection, 但是在 collection level 对 write 有锁.

- mongo shell 中的 dict 能保证 key 的顺序和输入顺序一致, 但 python3.6 以下的 dict
  不能保证. 若想要在指定查询条件时保证 doc fields 的顺序, 可以使用 ``OrderedDict``.
  若想要让 client 返回的 doc 中 key 的顺序也保证, 需要指定:

  .. code:: python

    MongoClient(document_class=OrderedDict)

  python3.6 的 dict 已经能够保证 key 的定义顺序. 所以在 python3.6 中, 用 dict 就行.

- single field index

  索引的升降顺序不影响 sort 操作.

  * `index on embedded field` vs `index on embedded document`

    前者是指定 qualified field ``field.subfield`` 作为 index 的列, 即将 sub-doc
    中的列值加入 index; 后者是将 ``field`` 下的整个 sub-doc 加入 index.

- compound index

  复合索引中, field 的先后顺序很关键, 它决定这个索引中列的排序
  优先级. 先按照 k1 排序, k1 相同时再按照 k2 排序. 列的顺序直接影响一组查询条件
  能否使用这个索引.

  复合索引不仅支持对所有索引列的查询, 还支持对索引列的 prefix 部分的查询.
  例如 ``{a:1, b:-1, c:1}`` 支持对 a, a/b, a/c 组合的查询. 虽然对 a/c 的组合查询
  效率不如专门的 a,c 复合索引效率高.

  compound index 中, 各个列的 sort order (ascending|descending) 直接影响可以使用它
  的排序条件.

- multikey index

  当 doc 中要索引的 field 的值是一个 array, 每个值都会加入索引中, 它们都指向这个 doc.

- index limitations

  * 一个 index entry 的大小必须小于 1KB.

  * 一个 collection 最多能有 64 个 index.

  * fully qualified index names (``<db>.<collection>.<index-name>``) 的长度必须
    小于 128 chars. 因此如果 index specs 中涉及的列比较复杂, 最好自定义 index name.

  * 一个 compound index 包含的列数必须小于 32.

  * 一个查询不能同时使用 2 种 special index, 例如 geospatial 和 text.

  * 2dsphere index 只能包含图形类数据.

- unique index

  ``_id`` field 一定是 unique 的, 这是内秉的, ``_id_`` 不是通过 ``create_index``
  创建的 (所以也不能 ``drop_index``), ``unique`` 不是这个 index 的额外条件. 所以,
  在 ``index_information`` 的输出中, ``_id_`` index 没有 ``"unique": True`` 选项.

  MongoDB cannot create a unique index on the specified index field(s) if
  the collection already contains data that would violate the unique constraint
  for the index.

  注意: "unique" index 的 unique 之意是能够通过 index 的 fields 的值的组合 *唯一地*
  确定一个 document (一行数据). 因此, 如果一个 index 包含 array field 或 array 中的
  doc 的 field, unique index 并不要求对于某个 doc 这个 array 中列的值唯一, 而是要求
  对于不同的 doc 中这个 array 中列值唯一. 因为, 因为如果一个 doc 中 array 值重复,
  它们都指向的是这个 doc, 并没有违反唯一性, 而且实际上在 multikey index 中, 这些
  重复的值只会 index 一遍.

  由于不存在的列值被认为是 null, 若有两个以上的 doc 中不存在该列, 将无法创建
  unique index. 此时, 可以通过构建 unique partial index 来过滤掉那些不合适的 docs.

- build index

  * index design is not supposed to be universal. Rather, it's supposed to fit
    in the business needs. 当业务逻辑变更时, drop 没用的 index, create 新的 index.

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

  * 如果一个 doc 不包含要 index 的 field, 等价于这个列的值为 null.

  * 在奇葩的 tokumx 2.0 版本中, ensure_index 不能随便执行, 在大数据量下会卡得很厉害, 即使
    相应 index 明明已经存在. (不知在正常的 3.4 版本中有没有这个问题.)

- index and sort

  索引的升序降序不影响查询, 但可能会影响排序 (例如复合索引时).
  If the query planner cannot obtain the sort order from an index,
  it will sort the results in memory. Sort operations that do not use
  an index will abort when they use 32 megabytes of memory.

  由于 index 可以从正向 (forward) 和反向 (backward) 来遍历, 一个 index (无论
  single field 还是 compound) 支持遵从它的顺序以及它的逆序的排序操作.
  例如 ``{a:1, b:-1}`` 支持 ``.sort({a:1, b:-1})`` 以及 ``.sort({a:-1, b:1})``,
  但不支持 ``{a:1, b:1}``.

  若查询后指定的排序操作可以完全通过 index 来解决, 则 mongodb 直接按照 sort 操作
  指定的顺序来遍历索引取出 docs. 因此, 不再需要单独的 SORT stage. 故此时 explain()
  中不会包含 SORT stage, 不然的话会有 SORT stage.

  若要用索引进行 string comparison, 需要指定和索引相同的 collation 规则.

  在以下情况时, 排序操作会使用索引来完成:

  * 排序规则是相应索引规则的严格前缀条件.

    对于复合索引, 虽然查询时可以匹配包含 prefix 的条件以及 a/c, a/d 之类的非严格前缀条件,
    但是对于排序必须是严格的. 这是很自然的, 因为只有严格前缀遍历时才有确定的顺序关系;
    而在查询时, 只需要在索引中有匹配即可.

  * 排序规则是相应索引规则的中间某一段, 但在查询条件中要求包含一系列的 equality 条件,
    这些条件限定了前缀取值要唯一.

    An index can support sort operations on a non-prefix subset of the index key pattern.
    To do so, the query must include equality conditions on all the prefix keys that
    precede the sort keys.

    例如:

    .. code:: javascript
      db.data.find( { a: 5, b: { $lt: 3} } ).sort( { b: 1 } )

- query

  * 在奇葩的 tokumx 2.0 版本中, 大数据量时 ``find`` 后 sort 会卡得很厉害, 也许这实际上
    应归咎于数据结构 index 设计有问题.

  * covered queries: 如果查询条件、排序条件以及所需返回的 fields 完全可以通过 index
    来解决, 整个查询过程将不需要访问 docs 数据, 这会非常快.

  * stages of query operation:
    IXSCAN, COLLSCAN, FETCH, PROJECTION, LIMIT, SORT_KEY_GENERATOR, SORT,
    AND_SORTED, AND_HASH, OR, SUBPLAN, EOF...

  * debug query 时为了看清执行流程等细节应使用 ``explain()``, 并将 verbosity 设为
    ``executionStats`` 或者 ``allPlansExecution``.
    explain 有两种用法, ``cursor.explain(...)`` 以及 ``db.collection.explain(...).<op>``.
    前者只支持对 ``find()`` 等返回 cursor object 的操作进行解释, 后者则支持更多种操作,
    因 ``<op>`` 可以是 aggregate, count, distinct, find, group, remove, update, etc.

- insert

  * 在奇葩的 tokumx 2.0 版本中, 插入新 doc 的操作与 ensure_index, find, sort 等有冲突,
    进行这些操作时不能写入.

- operators

  * ``$or``: 当 ``$or`` 里面的所有 clause 的执行都有相应的 index 可以使用时,
    整个 $or clause 才会使用 index. 否则将对整个 collection 进行遍历. 注意不
    能将 $or clause 中的共同部分简化出来::

      db.data.find({a:1, $or: [{b:2}, {c:3}]})
      db.data.find({$or: [{a:1, b:2}, {a:1, c:3}]})

    两者不相等. 若有 a/b 和 a/c 的两个 index, 第一个查询不会使用索引, 第二个会使用.

    当 $or 使用了索引时, ``explain()`` 中有 OR stage, 其中的 inputStages 包含每个
    子查询条件执行的步骤.

- mongodb 里的 Date 类型是 BSON 的 UTC datetime, 也就是说保存的是 UTC 时区的时间,
  实际上是 int64 的 milliseconds since Unix Epoch.
  
  在使用 pymongo driver 时, 应该使用 ``datetime.utcnow`` 来获取这样的 datetime object;
  或者使用包含时区信息的 local datetime object, 后者在存储时会被 pymongo driver 自动
  转换为 UTC 时间.

  从数据库中获取 Date object 时, 默认得到的是 UTC 时间, naive datetime object.
  在 ``CodecOptions`` 选项中设置 ``tz_aware=True`` 以及 ``tzinfo`` 为所需时区,
  则得到 timezone-aware datetime object.

- ``.count()`` 可以在逻辑上可以认为是最简单的聚合, 即没有 query specs, 没有 grouping
  (整个表为一组), 只有 count 操作.
