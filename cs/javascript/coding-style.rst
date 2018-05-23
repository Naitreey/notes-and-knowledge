- constants are capitalized with words separated by ``_``.

- callback hell: js 允许任意形式的 function expression 直接作为 first class
  entity. 因此, 可能出现多层 nested callback function. (python 不存在这个
  问题, 因为 lambda function 功能有限, 更一般的函数仍需要通过 function
  declaration statement 去定义.)

  problem:

  * hard to read

  * too much unnecessary details

  solution:

  * make your code shallow. 将 callback 定义在单独的 module 中, 只引用名字.

  * async functions.
