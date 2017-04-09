- 对于文件下载, 返回与文件类型相符的 `Content-Type`, 而不是 `application/octet-stream`.
  后者仅用于你不知道这个文件到底是什么类型的时候.
  配合 `Content-Disposition: attachment; filename="<name>"` 来告知浏览器该 resource
  是要保存到本地的, 并设置默认的文件名.
  ref: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition
