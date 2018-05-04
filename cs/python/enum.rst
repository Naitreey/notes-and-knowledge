- python 3.4 之后就有 enum module 了.

- 对于已经定义了 members 的 enum class 不能再被 subclass. 但若一个 enum
  仅仅定义了 methods, 没定义任何 member, 可以被继承. 这是为了方便在不同
  enum class 之间共用相同的 methods, behaviors, etc.
