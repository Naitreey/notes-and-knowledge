overview
========

- Refactoring is the process of improving the code without changing its
  functionality.

- refactoring cat.

  * 作, 作, 作... 作死了... 为了避免作死, 应该配合单元测试, 一步一步来.

concepts
========
- Keep refactoring and functionality changes entirely separate.
  
  There’s always a tendency to skip ahead a couple of steps, to make a couple
  of tweaks to the behaviour while you’re refactoring, but pretty soon you’ve
  got changes to half a dozen different files, you’ve totally lost track of
  where you are, and nothing works any more.

- Don't Repeat Yourself (DRY).

- Three strikes and refactor. 一旦逻辑类似或甚至完全重复的代码出现达到 3 次,
  就一定要重构并统一, 从而能够 DRY. 我更习惯 2 次就重构.

- Before you do a refactor, commit. After you do a refactor, commit.

cooperation with testing
========================
- The first rule is that you can’t refactor without tests.

- When refactoring, work on either the code or the tests, but not both at once.
  也就是, 如果要修改实现, 先保证 refactored implementation passes current
  tests.  如果要修改功能、从而修改单元测试定义, 就先修正你的测试代码定义,
  然后再 refactor 代码满足新的测试.
