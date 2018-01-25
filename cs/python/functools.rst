- 由于 ``update_wrapper()`` 需要 wrapper, wrapped 两个参数, 别忘了相应的
  ``wraps()`` 函数需要以 wrapped 为参数, 返回一个 decorator 作用在 wrapper
  function 上.

- ``lru_cache`` 的原理是在它 wrap 函数的 wrapper 里放一个 cache dict,
  通过匹配 args, kwargs, type 来获取 cached value. 对每个这样的函数, 都新
  创建了一个 dict cache, 注意这带来的内存影响.

- ``partial`` 类似 haskell 中的 higher-order function.

- ``partialmethod`` 与 partial 类似, 但是专门用于构建 partial method definiton.
  它的 ``func`` 参数应该是一个 descriptor or callable, 且 func 本身是一个
  method definition. partialmethod 构建的效果是会把 func 的第一个参数 self
  留出来, 只填充后面的参数. 这种效果一个简单的 partial 不能直接做到. 此外, 
  partialmethod 给出的是一个 descriptor, 不是 callable, 所以只有赋值到一个
  class object 上, 作为 method 来使用, 才有实际用处. 
