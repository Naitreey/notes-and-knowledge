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

- 不同格式、功能的数据放在不同的 index 里, 多 type 谨慎使用. 使用多个 type 时考虑
  `_default_`. 某些数据 index 也许可以使用多个 type, 但需要具体看, 因为 type 更多
  的是数据之间的子分类标识符. 不是完完全全不同的数据结构.

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
