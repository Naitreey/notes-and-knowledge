- index, type, document 三者的关系完全不是和 RDBMS 中的 database, table, entry 对应.
  如果这么想的话, 将导致性能问题. You will be punished!
  原因是 elasticsearch 本质使用的是 lucene, 一个 index 中所有 document 都共享同一个
  mapping, 而没有 type 这一层. type 只是 elasticsearch 抽象出来的层, *不同的 type
  只适合放置 mapping 类似的 document*.
  所以, 及其粗略地讲, index 类似于 RDBMS 中的一组相似的 table, type 类似于 table,
  document 类似于 entry.
  See also https://www.elastic.co/guide/en/elasticsearch/guide/current/mapping.html

- array 的 append 等操作需要使用 script.

- 一些包含 list of objects 的数据需要使用的是 nested datatype. 若对 inner object 里
  key-value 的关联性没有要求, 就没必要使用 nested datatype.
  Nested documents are hidden; we can’t access them directly. To update, add,
  or remove a nested object, we have to reindex the whole document.

- 不同格式、功能的数据放在不同的 index 里, 多 type 谨慎使用. 使用多个 type 时考虑
  `_default_`. 某些数据 index 也许可以使用多个 type, 但需要具体看, 因为 type 更多
  的是数据之间的子分类标识符. 不是完完全全不同的数据结构.

  使用 ``_default_`` 时仍要注意, 它只在新增 type 时起效, 对已有的 type 没有影响.
  所以如果后续修改 ``_default_`` 的 mapping 或设置, 已有的 type 的 schema 不会跟着
  改变.

- Lucene's inverted index 在对一个列进行分词和索引的方式以及对 array 进行展平和索引
  的方式与 mongodb 对 array 进行 multikey index 的方式有些类似, 但意义和用法不同.

- Lucene's inverted index 并不会因为需要搜索新 document 而需要重建. 而是把新 documents
  写入新的 Lucene index segment. 搜索等操作时对所有的 segment 进行遍历.

- 对于将来可能修改 mappings 的 index, 使用 alias, 而不直接使用 index.
  如果只是新增 field, 并没关系; 若是修改现有的 field, 则不得不需要 reindex 数据
  到新的 index.

- 使用 `_version` 来对并行写操作进行冲突处理. 对于顺序 无关的 partial update 操作,
  使用 `retry_on_conflict`.

- 一个 index 需要多少 primary shards? 这需要根据集群的规模来调整. 在分布式中,
  primary shards 越多, 数据约分散, primary & replica shards 的增多可以提高效率.

- 除非需要根据相关性分数排序, 否则搜索时使用 filter 更高效.
  只有搜索时按照相关性排序时 `_score` 才有意义, 其他时候 `_score` 没有意义.

- 字符串需要 full text search 的 field 才用 text, 其他用 keyword.

- near real-time: refresh 创建新 index segment 使得新 document searchable 的时间默认是 1s.
  注意到这个限制只影响搜索, 不影响根据 id 取 doc.

- `_id` 只能用于快速获取, 不能用于 search, aggregation, sort, etc.
  即使是 `_uid` 在很多地方也不能使用.
  这些过多的限制, 要求我们在 `_source` 里也保存一个被索引的唯一标识.

- 取时考虑使用 `_source: false` 或 `_source_include`, `_source_exclude` 来只取得部分结果.

- 使用 HEAD 检查 doc 是否存在

- 使用 `op_type` param 或 `_create` endpoint 来限定操作为新建.

- 若对一个 doc 的不同部分的更新比较罕见, 或者每次需要更新的部分实际上占比较大,
  则简单地存在一个 index 中即可. 必要时结合 nested fieldtype.
  nested 的特点是 root doc 和 nested doc 关系紧密, 因此优点是在 search 时很快,
  但缺点相应地是对 nested field 的任何改动都要 reindex 整个 doc. 所以, 对于 doc
  的一些部分需要频繁增删改时, 这些部分不适合用 nested. (search time 高效, index
  time 低效.)
  为了避免少量修改时 reindex 整个 doc, 可以将其拆成不同的 child doc, 构成 parent
  child 关系.
- 对于 nosql, 往往不能单纯地把一个 document 拆成不同的部分然后 *独立地* 放置在不同的
  index 中. 这将导致搜索难以进行. 因为 nosql 中没有 join query, 对于一个搜索, 需要在
  不同的 indices 中执行同一个搜索, 但是又该怎么综合来自不同 index 的结果呢?
  对于 elasticsearch 或 nosql in general, doc 之间希望是独立的, 也就是说一个 doc
  包含所有相关的信息. 这样才能高效地搜索. 但是在 search time 和 index time 的效率之间
  权衡, 需要考虑 parent-child 这种拆分关系.
- nested 适用于以下条件: 1) 子数据需要保证映射信息完整; 2) 子数据在 doc 中所占比重
  比较小, 即是少量的数据; 3) 这些少量的 array 型数据只要写入就几乎不变, 即更新十分
  罕见.
- 不符合以上条件的 doc 拆分, 则应该使用 parent-child 方式.

- 一个 string term (keyword) 最长为 32766, 因此默认情况下字符串大于这个长度会报错
  `max_bytes_length_exceeded_exception`.
  解决办法: 对该 field 设置 `ingore_above`.

- 若输入的 document 某个 field 的值可能与预期的类型不符, 可以使用 `ignore_malformed`
  忽略对类型不符的值进行 index, 或者使用 `coerce` 强行进行类型转换.

- 一些列设置 `include_in_all` 来避免全文检索, 设置 `index:true|false` 限制是否
  index 该 field.

- debug painless script

  在正常需要写脚本的操作 (例如 scripted update, scripted query, script field
  等操作) 的脚本中, 添加 ``Debug.explain(expr)``, 会把 ``expr``
  的值、类型等信息返回到 response 中, 类似于 ``print()`` 操作.

- 对于 painless 脚本, json 的 list 成为了 java.util.ArrayList, json 的 object
  成为了 java.util.HashMap 或 java.util.LinkedHashMap.

- compound query 之 bool query, 如果 must/must_not/should/filter 中包含多个
  leaf query clause, 则这些 leaf query 需要以 list 方式出现. 例如::

    {
        "from": 0,
        "size": 8,
        "sort": [
            {
                "lastquery": {
                    "order": "desc"
                }
            }
        ],
        "query": {
            "bool": {
                "filter": [
                    {
                        "range": {
                            "lastquery": {
                                "gte": 1498811078088
                            }
                        }
                    },
                    {
                        "range": {
                            "lastquery": {
                                "lte": 1499053691932
                            }
                        }
                    },
                    {
                        "prefix": {
                            "md5": "19"
                        }
                    }
                ]
            }
        }
    }

- 每个 term query 中只能限制一个列的值::

    {
        "query": {
            "term": {"a": 1}
        }
    }

  不能是::

    {
        "query": {
            "term": {
                "a": 1,
                "b": 2
            }
        }
    }

  这种情况需要用 compound bool query::

    {
        "query": {
            "bool": {
                "filter": [
                    {"term": {"a": 1}},
                    {"term": {"b": 2}}
                ]
            }
        }
    }

- 在各个层级上禁止 elasticsearch 进行自动创建:

  * 禁止 node 自动创建 index:

    在 node level 的配置 ``elasticsearch.yaml`` 中::

      action.auto_create_index: false

  * 禁止 index 自动创建 type:

    在 index level 的配置中添加::

      index.mapper.dynamic: false

    或者添加 index template, 让新创建的 index 自动应用以上配置.

  * 禁止 mappings 自动创建 field:

    在 mappings 中的 document level 或者所需的 object level 中设置::

      dynamic: false|"strict"

- 设置 ``dynamic: false|"strict"`` 后将在它影响的范围内关闭 dynamic mapping 相关功能,
  这包括 ``_default_`` mapping, dynamic field detection, dynamic template 等具体功能
  不再起效或者会报错.

- ``_search`` endpoint 可以包含多步操作: query, from, size, aggs.

  注意聚合是搜索的一部分操作. 我们可以既查询又聚合 (从而限制被聚合的数据集).
  如果只要聚合的结果, 而不要查询的 结果, 应该设置 ``size: 0``, 这样可以加快
  整个操作的速度.
