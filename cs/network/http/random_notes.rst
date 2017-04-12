- 对于文件下载, 返回与文件类型相符的 `Content-Type`, 而不是 `application/octet-stream`.
  后者仅用于你不知道这个文件到底是什么类型的时候.
  配合 `Content-Disposition: attachment; filename="<name>"` 来告知浏览器该 resource
  是要保存到本地的, 并设置默认的文件名.
  ref: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition

- 文本类在传输时需要压缩, jpeg, png 等图片本身就是压缩过的, 进一步压缩可能并不会减小
  体积, 甚至可能增大体积, 而浪费了计算资源.

- 压缩算法的选择. 对于 gzip 和 deflate 应该选择 gzip.

  gzip 和 deflate 都使用的 zlib format, Lempel-Ziv coding (LZ77) 算法. 引用:

    we have 2 compression mechanisms that use the same algorithm for compression,
    but a different algorithm for headers and checksum.

  对于 checksum, 前者用 CRC-32, 后者用 ADLER32. CRC-32 is slower than ADLER32.
  (只慢一点.)

  但是:

    Turns out many browsers over the years implemented an incorrect deflate algorithm.

  所以应该使用 gzip.

  ref: http://stackoverflow.com/questions/388595/why-use-deflate-instead-of-gzip-for-text-files-served-by-apache

- `Transfer-Encoding` 为 `chunked` 的情况是 response body 的长度在传输完成之前是
  不确定的. 所以没有 `Content-Length`, 需要 end of transfer indicator, 且需要
  persistent connection (也许通过 keep-alive?).
  一种可能的情况是, client 依据 `chunked` transfer-encoding 来通过 socket 接受
  response body, 然后依据 `Content-Encoding` 来解压缩.
