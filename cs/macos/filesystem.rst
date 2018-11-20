- HFS 和 APFS 中, alias 相当于 linux 中的 symlink. 但不同的是, alias 是
  实际上是 hardlink to data blocks, alias 与原文件名本身是等价的. 这有
  一个有趣的副作用: 移动文件不影响文件本身 (?)
