overview
========
- Testing Goat. the unofficial mascot of TDD in the Python testing community.

  * Stubborn: 告诉你一定要先写测试, 保证测试 fails, 然后再写功能代码.

  * One step at a time, so that never falls. 每新增一小块功能, 就按照
    test/implement/test cycle 去循环地实现.

- TDD 的软件开发方法就像物理学中研究事物的方法. 在物理学中, 我们认识事物的
  唯一方式是通过观测和实验. 如果对一个事物的观测结果或实验数据符合我们对某种
  已知物理概念的认知 (数学模型), 那它就是什么.  我们从来不关心一个事物 "所谓
  的本质" 是什么, 因为观测到的才是有效的, 我们从来无法确知也无需关心那 "本质".
  (如果一个模型能精确地描述一个物理现象, 那这个模型就是好的, 就代表了我们对
  该物理现象的认识.)

  在 TDD 中, 我们通过测试代码构建对软件的行为预期, 这就是在构建软件的行为模型.
  能通过测试的应用就是符合行为模型的应用, 就是符合用户需求的应用. 这种思路的
  一个重要推论是, 能通过测试的代码自然具有合适的内部结构 (本质). 行为决定本质,
  行为等价于本质. 对行为的约束会自然形成恰当的内部结构. 所以软件行为的定义和
  验证的重要性是很高的, 然后才是设计实现.

questions and concerns
----------------------
- microstepping 所要求的每次 test/code 循环每次只解决一点问题就测试太繁琐了吧?

- 每行代码即使是非常 trivial 的操作也要测试?

- Testing the tiniest thing, and taking ridiculously many small steps?

terminology
-----------

- expected failure.

- user story.

  * A concrete instance of user's interaction with the application. It
    describes how the application will work from the point of view of the user.

  * It is used to structure a functional test.

  * A user story has to be a story. So it phrases a complete session of user
    interaction with the software, in a natural language.

- microstepping. test/code cycle must be tiny.

workflow
========

- in general:
  
  * test/implement/test cycle.

  * microstepping: be absolutely sure that each bit of code is justified by a
    test.

- detail.

  1. We start by writing a functional test, describing the new functionality
     from the user’s point of view.

  2. Once we have a functional test that fails, we start to think about how to
     write code that can get it to pass (or at least to get past its current
     failure). We now use one or more unit tests to define how we want our code
     to behave—the idea is that each line of production code we write should be
     tested by (at least) one of our unit tests.

  3. Once we have a failing unit test, we write the smallest amount of
     application code we can, just enough to get the unit test to pass. We may
     iterate between steps 2 and 3 a few times, until we think the functional
     test will get a little further.

  4. Now we can rerun our functional tests and see if they pass, or get a little
     further. That may prompt us to write some new unit tests, and some new
     code, and so on.

test classification
===================

- The functional tests are driving what development we do from a high level
  (outside), while the unit tests drive what we do at a low level (internal).

- Functional tests should help you build an application with the right
  functionality, and guarantee you never accidentally break it. Unit tests
  should help you to write code that’s clean and bug free.

- functional tests 校验应用对外的功能, 只要应用的功能逻辑不变, functional tests
  的逻辑就应该是不变的. unit tests 校验程序模块对内的功能, 同样地程序模块的 API
  不变, unit tests 的逻辑就应该不变. 还存在应用的外部功能不变, 但程序实现修改的
  情况, 此时就是 functional tests 不变, 但 unit tests 需要根据模块实现的变化进行
  相应的改变.

functional test (FT)
--------------------

- functional test a.k.a. acceptance test or end-to-end test, black-box test.

- FTs test how application *functions* from the user's point of view.

- The main point is that these kinds of tests look at how the whole application
  functions, from the outside, from end user's point of view, rather than from
  the programmer's point of view.

- 因为 FT 具有最终的视角, an FT can be a precise specification for your
  application. It tends to track what you might call a *User Story*, and
  follows how the user might work with a particular feature and how the app
  should respond to them.

- An application's functional tests should tell the user story or covers the
  specification in an programmatical way. The specification can be made more
  explicit by comments etc.

- When creating a new FT, we can write the comments first, to capture the key
  points of the user story or specification.

- 即使需求通过 specification 的形式呈现, 一组功能性测试本身必然是基于某个
  具体的 user story 来呈现和校验的 (user story 是 specification 的具体呈现). We
  use comments to explain the User Story in our functional tests, by forcing us
  to make a coherent story out of the test, it makes sure we’re always testing
  from the point of view of the user.

unit test
---------
- Unit tests test the application from the inside, from the point of view of
  the programmer (about the interactions of the internal components of
  application).

TEMP
====

FOr now
-----------

- Test-Driven Development with Python: Obey the Testing Goat: Using Django, Selenium, and JavaScript

  * online version: http://www.obeythetestinggoat.com/pages/book.html

  * source: https://github.com/hjwp/Book-TDD-Web-Dev-Python/

- django test topics

- unittest and other tools in python

- selenium wiki https://en.wikipedia.org/wiki/Selenium_(software)

  and doc https://www.seleniumhq.org/

- geckodriver

- web driver in general

- homebrew

For then
------------
- wiki https://en.wikipedia.org/wiki/Test-driven_development

- https://softwareengineering.stackexchange.com/a/57309/163588

- Test Driven Development: By Example

- Growing Object-Oriented Software, Guided by Tests

