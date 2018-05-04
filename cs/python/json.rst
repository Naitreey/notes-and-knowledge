- 注意 json format 不支持 binary data 这种类型. 所有的 binary data 都必须使用某种数字
  进制编码成字符串, 才能用 json format 来传递.

  由于 json 数据要求是纯文本, 因此 ``json.dumps`` 的结果一定是 `str` 而不会是 `bytes`.

- 如果需要经常对某个数据结构进行 json 的转换, 可通过扩展 JSONDecoder/JSONEncoder
  来实现. 使用时 ``json.loads`` ``json.dumps`` 之类操作加上自定义的 encoder/decoder,
  这样很方便.
