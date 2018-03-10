TCP: The problem
================
问题: 在有损的、不可靠的环境下, 如何保证数据传输的完整可靠性?
需要解决的问题包含: packet bit error, packet drop, packet reordering,
packet duplication.

- solution 1: Use error-correcting code (ECC) (code -- 编码).

- solution 2: automatic repeat request (ARQ), i.e., simply try again until
  information is successfully received.

ARQ approach is the basis for many communication protocols, including TCP.

ARQ
~~~

overview
========
- TCP: Transmission Control Protocol

- TCP 的 checksum 在 99.9% 的概率上保证了数据的完整和正确, 因此其上的应用层协议不需要
  实现 checksum 来再次验证数据完整性.
  Internet checksum 实际上不是完全可靠, 确实在极其罕见的情况下会让错误漏过, 但
  绝大部分情况下都不需要担心, 只有对数据完整性要求很高的时候, 才需要在应用中 (注意
  仍不是在应用层协议设计中) 检验 hash/checksum.
