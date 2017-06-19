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
