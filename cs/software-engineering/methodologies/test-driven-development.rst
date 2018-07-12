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

why testing in general and why TDD
----------------------------------

- 单独来讲, 自动化的 unit tests, functional tests, acceptance tests 等等最大的
  价值是, 它们提供了低成本高效率可重复的 bug detection mechanism. 这对避免
  regression 问题有很大价值.

- 接上, 由于 regression test 很容易, 所以可以放心地做代码重构.

- 自动化的测试有助于提高程序员的对程序信心和编码过程的愉悦.

- TDD 的思想和方法, 最重要的特点是将测试提前到实现之前. 而不是先实现, 再根据
  实现来写测试. 通过测试代码来具体化需求, 将需求呈现为一个个可以检验的指标. 
  也就是说, 它定义软件整体的行为和各个模块的 API, 以达到驱动软件整体以及各个
  模块的设计和实现的效果.

  In TDD, The tests tell you what to do, what to do next, when you are done.
  They tell you what the design is, what the API is going to be.

- TDD 强制先设计, 再实现. 先考虑怎么用, 再考虑怎么做. 这是由于要先写出测试代码,
  所以程序员要设计程序的整体行为 (即程序如何和外部交互), 以及各个模块的 API (即
  模块之间如何交互), 然后才去填充实现.

  这种方式, 有助于达到一个使用起来更自然更合理的设计.

- 接上, 这种流程强制程序员写出易于测试的代码. 因为必须已经知道相关代码要怎么
  测试了, 已经知道它会怎么去使用了, 才会去写代码本身. 相反, 如果实现之后再写
  测试, 有可能代码本身是不易于测的, 因为没有测试代码去做规范.

  而易于测试的代码自然带有一个更有价值的属性: 低耦合. 否则它不可能易于测试.

- 在写功能代码前先写测试代码让写测试代码这件事更加 stimulating, 因为测试代码
  成为了开发过程的 guideline, 是个必要的成分. 如果完成功能代码后再写测试代码,
  那么写测试这件事更让人觉得这是额外的一项工作, 只是为了保证 *以后* 去检查
  regression bug, 而对当下并没有用, 因为代码已经手工测试过了.

- Better code quality. 与前一点相关, TDD 在帮助实现更好的设计时, 显然也同时帮助
  实现更好的代码质量. 因为要求可测性, 因而有清晰的 API 和功能行为. 这样的功能
  模块达到 high cohesion low coupling. You can bind it to the rest of the
  project as easily as you can test it.
  
- TDD 有助于更有目的地做事, 构建出最小可用的实现, 提高开发效率, 避免不必要的
  复杂度.

- TDD 时, functional tests and acceptance tests 可以做需求文档的具体实例 (user
  story). 而所有测试代码, 尤其是 unit tests 可以作为 API documentation.
  Sometimes, if you forget why you’ve done something a particular way, going
  back and looking at the tests will give you the answer.

- 先写测试再写代码更有趣, 因为是先构建问题 (test failure), 再解决问题 (test pass)
  的过程.

- TDD 似乎能大幅减少 debugging 时间.

- The most magical thing about TDD is: By enforcing a rigorous suite of tests,
  the right algorithm/implementation is just incrementally being derived out of
  those tests. It doesn't mean we don't plan things, design things, do
  architecture. It does mean we got a tool to support incremental development.

- TDD 的功能性测试和单元测试还可以在 interface review 上发挥作用. Interface
  review 比 code review 重要.

questions and concerns
----------------------
- microstepping 所要求的每次 test/code 循环每次只解决一点问题就测试太繁琐了吧?

  * 一开始需要这么做, 是为了强化流程. 当熟悉之后, 可以适当灵活一些.

  * 但一定要抑制不写测试就写代码实现的冲动. 要保证 test/code/test cycle.

  * think ahead, test ahead, implement, test again.

- 每行代码即使是非常 trivial 的操作、函数也要测试?

  * 如果不想这么严格, 其实可以放松一些. 即不绝对测试所有代码.

  * 但是, 这么做是有好处的. 首先, 强制一套所有代码都要测试的规矩, 有助于在复杂
    的实际应用中, 不让任何本该测试的、看上去十分无辜的代码被忽略, 最最终成为
    那最脆弱的一环.

  * 其次, 在实际项目中, 随着产品的迭代, 一个简单的逻辑可能逐渐变得复杂, 如果
    一开始因为简单所以不写测试, 那么要如何决定何时这个逻辑复杂到该写测试代码
    呢? 这个界限可能是很主观、比较不可靠的, 并且需要花时间考虑要不要加测试.
    甚至更糟的是, 由于一开始没有相应的测试, 就懒得写, 一直拖着, 最终变成大麻烦.
    所以, 即使是最简单的逻辑, 从一开始就写上 placeholder test case, 是最稳妥
    的做法.

  * 最后, 既然逻辑 trivial, 测试 trivial, 何不少说废话直接写了得了呢?

- TDD 不是不注重设计. 相反, 前期对需求的分析和功能设计的仔细考虑并没有任何改变.
  只有当相对宏观的设计已经想清楚了, 才开始将需求和设计具体化为功能性测试用例.
  此时, 才开始 TDD 的流程 (即开始开发).

  如果对于能通过测试的实现 (green), 如果不够清晰合理, 及时 refactor. 不是说
  第一次实现时只要通过测试即可, 如果能一次性实现好, 当然最好. 只是说, 不需要
  强求一次性达到最佳实现, 快速做好第一版实现, 如果需要 refacor, 就去 refactor.

terminology
-----------

- expected failure. When a test fails in an expected way. 这可能是因为实现还不
  充分.

- unexpected failure. When a test fails in a way we weren’t expecting. This
  either means that we’ve made a mistake in our tests, or that the tests have
  helped us find a regression, and we need to fix something in our code.

- user story.

  * A concrete instance of user's interaction with the application. It
    describes how the application will work from the point of view of the user.

  * It is used to structure a functional test.

  * A user story has to be a story. So it phrases a complete session of user
    interaction with the software, in a natural language.

- microstepping. test/code cycle must be tiny.

workflow
========

general and detailed workflow
-----------------------------
.. |tdd-workflow| image:: tdd-workflow.png

- in general:
  
  * test/implement/test[/refactor] cycle.

  * be absolutely sure that each bit of code is justified by a test.

  * Working incrementally and step-by-step, with each of them should be small.

- detail (Double-Loop TDD).

  |tdd-workflow|

  1. Write a functional test, describing the new functionality from the user’s
     point of view. Run the test to make sure it fails.

  2. write minimal code to implement the functionality.

     a. Think about how to write code that can get it to pass (or at least to
     get past its current failure). Write some unit tests to define how we want
     our code to behave—the idea is that each line of production code we write
     should be tested by (at least) one of our unit tests. Run the unit tests
     to make sure they fails.

     b. Write the smallest amount of application code we can, just enough to
     get the unit tests to pass.

     c. Think about whether the code needs refactoring. If so, refactor the
     code and ensure it passes the unit tests.

  3. Rerun our functional tests and see if they pass, or get a little further.
     That may prompt us to go back to step 2.

  4. Think about whether the code needs refactoring. If so, go back to step 2
     and refactor the code. Ensure it passes the functional and unit tests.

  以上步骤也称为 Red/Green/Refactor cycle.

- 这种小步伐的 test/code cycle 还有助于 keep development progress. 注意到所有
  的 development expectation 都在 functional tests and unit tests 中得到记录.
  如果忘记上次开发到哪里了, 只需跑一轮测试, 哪里不通过, 就知道开发到哪里了 (因为
  每次一小步, 已经实现的代码部分都相应地测试通过了.)

关于步骤的说明
--------------

* FT 描述的新功能需要在软件的哪个部分添加功能实现, 就在这个部分中写单元测试和
  进行实现. 每个部分所用的语言可能是不同的, 所用的单元测试框架也可以是不同的.
  注意 FT 的实现与具体的单元测试 (和实现) 是独立的.

* Initial tentative design and implementation. 很多时候, 在一个功能或模块 API
  的最初设计和实现过程中, 我们设想的设计在实现时才发现需要调整的地方. 因此,
  不可避免地需要反过来调整设计, 调整测试代码. 在这个尝试性的阶段, 同时修改代码
  实现和测试用例是允许的. 当初始设计基本确定之后, 需要保证不同时修改测试和实现,
  进入 Red/Green/Refactor 流程.
  
With refactoring
----------------
- When refactoring, the code should starts with working state, then move
  incrementally to another working state. 步伐尽量可控, 过程中每一步都要
  保证测试通过, 不要一次性做一大堆修改然后扯着蛋.

  The step-by-step approach, in which you go from working code to working code,
  is really counterintuitive. 甚至中间的一些 working state 极其错误, 完全不合理.
  但这完全是为了不破坏已经建立的局面, 然后一步一步向更好的局面发展.

- You can begin refactoring only when you know you are safe to refactor.
  也就是说, 例如我们已经完成一个功能还没有开始新功能的开发, 或者至少我们现在
  位于 working state. 不要在半截上开始 refactor, 此时应该先记下稍后需要
  refactor.

- Don’t refactor code against failing tests, except for the test you are
  currently working on.

TDD on deployment
-----------------
- TDD 的思路还可以应用于服务器应用部署方面 (非容器化的方式). 一步一步地配置,
  work incrementally, make one change at a time, and run your tests frequently.

  When things (inevitably) go wrong, resist the temptation to flail about and
  make other unrelated changes in the hope that things will start working
  again; instead, stop, go backward if necessary to get to a working state, and
  figure out what went wrong before moving forward again.

  Don't fall into the Refactoring-Cat trap on the server.

About prototyping
-----------------
- prototyping: 尝试和学习一个新的工具, 设计一个新的解决方法时, 可能需要一些
  表达基本思想的原型代码. 这就是在做 prototype. 在 TDD 中也称为 spike.

- 在做原型时, 完全可以不管 TDD 或只有必要的测试代码, 纯粹尝试性的 try if it
  works as expected.

- 在将 prototype 重新整理为系统化的设计和实现时 (de-spike), 再认真地 TDD.

test classifications
====================

- The functional tests are driving what development we do from a high level
  (outside), while the unit tests drive what we do at a low level (internal).

- The functional tests are the ultimate judge of whether your application works
  or not. The unit tests are a tool to help you along the way.

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

- functional test, 在 TDD 只关注于研发阶段, 这里主要指的是功能性的单元测试, 这
  不同于集成测试或系统测试时的功能性测试.

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

- 功能性测试中可以测试 style design 是否按预期加载, 但不严格测试 style 本身.
  例如对前端页面, 测试方法可以是: 大致地测试一下某个页面组件是否在预期位置附近,
  以确定 style 文件被加载 (smoke test for css file loading).

- 注意 TDD 使用的 functional tests 是不同于集成测试或系统测试中的功能性测试.
  
  * TDD 时的 FT 目的是 drive design, testing design during development.
    而集成和系统测试的目的就是测试, 而且是对开发完毕后的软件进行测试.
    
  * TDD 时的 FT 必须执行迅速, 快速给出反馈, 若涉及 external services, 必须
    mock. 而集成测试和系统测试必须是在真实的服务上进行测试.

- 如何组织功能性测试?

  * 对每个 feature, 单独创建一个 test file. 这个 test file 中包含一个或多个
    相关的 test class.

  * 每个 feature 可能需要多个 user stories 从不同方面具体化. 对应于一个 test
    class 的多个 test method. 每个 test method 表达一个完整的 user story.

unit test
---------
- Unit tests test the application from the inside, from the point of view of
  the programmer (about the interactions of the internal components of
  application).

- Test program logic, flows, configuration, etc. that changes. Don't test
  constants, because it's useless -- constants nevers changes it's written as
  is and works as is.

  这里 constant 的含义是广泛的, 不仅仅是写死在代码中的常量, 还包含例如不变的
  模板文件等不会变的固定的 entity.

- 在单元测试中, 需要仔细考虑什么是变的, 什么是不变的, 才能只对变化的部分做测试.

- 如何组织单元测试?

  * 一般情况下, 每个源代码文件对应一个单元测试文件.

  * 对每个 class 和 function, 至少有一个 unit test, 即使只是 placeholder test.
    (See `questions and concerns`_ for reason.)

design patterns
===============

- 功能性测试代码应当是与实现独立的. 即功能性测试不直接引用实现细节 (只检验
  实现). 它是从外部观测. 功能性测试与所测试功能的实现完全可以在两种不同的语言
  中写.

- Each test should only test one thing. Just like each function should only
  does one thing.

  * 对于功能性测试, 一个 test case 只测试一个 user story.

  * 对于单元测试, 一个 test case 只测试被测对象的一个行为点.

  意义:
  
  * 模块化、重用、职责清晰
    
  * 由于每个测试是独立执行的, 每个测试只检测一个问题, 有助于同时检测和发现
    多个问题. 如果将多个不相互依赖的测试逻辑放在一个测试单元中执行, 第一个
    不通过的部分就会 raise exception, 后续的测试则不会执行.

  * It helps you isolate the exact problem you may have, when you later come
    and change your code and accidentally introduce a bug.

- 尽量减少不同测试用例之间的重复. 尽量不重复测试相同的行为点.

- Ensure isolations between test cases.

  * Properly isolated tests can be run in any sequence.

  * Always rebuild your starting state from scratch.

  * 如果多个测试需要共享某个初始状态, each test must cleans up properly after
    itself.

- Carefully deal with tested code containing asynchronous operation.

  * Best solution: 对于异步操作, 如果它接受传入 callback 是最好的. 此时可利用
    callback 去检测结果.

  * Normal solution: Polling the result of async operation. Caller 必须等着
    结果返回, 让异步变成同步. 不能让异步操作就那么溜过去. 设置尽量小的 polling
    interval, 并设置 polling upper bound. (Avoid hardcode single sleep.)

- Do not actually access external services in unit and functional tests.
  External services are not in developer's control, thus introduces
  non-determinism. Also, accesssing external services is usually slow, which
  slows down TDD development cycle. Mock their APIs, so that they are in our
  control and fast.

- Ensure tests are deterministic.
  
  A test is non-deterministic when it passes sometimes and fails sometimes,
  without any noticeable change in the code, tests, or environment. Such tests
  fail, then you re-run them and they pass.

  Non-deterministic tests have two problems:

  * They are useless.

  * They infects the whole test suite. Initially people will look at the
    failure report and notice that the failures are in non-deterministic tests,
    but soon they'll lose the discipline to do that. Once that discipline is
    lost, then a failure in the healthy deterministic tests will get ignored
    too. At that point you've lost the whole game and might as well get rid of
    all the tests.

  Analysis to non-deterministic tests:

  * 不确定性的测试的可能原因: 1) 测试之间没有保证更好的独立性; 2) 异步操作
    在时间上的不确定性导致测试结果不确定; 3) 测试需依赖于外部服务, 后者的
    不确定性 (例如可用性) 导致结果不确定.

  * 如果目前没有时间处理这些不确定性的测试, 先隔离至另一个 test suite. 然后
    及时处理. A danger here is that tests keep getting thrown into quarantine
    and forgotten, which means your bug detection system is eroding.

- 当开始实现一个设计时, split work out into small, achievable tasks. 抑制
  一次实现所有设计的冲动. 每实现一部分功能时, 一定要先写测试.

- 当重构时, move step-by-step, from working state to working state. Being
  the testing goat, not the refactoring cat. Our natural urge is often to dive
  in and fix everything at once... But if we’re not careful, we’ll end up
  like Refactoring Cat, in a situation with loads of changes to our code and
  nothing working again.

- YAGNI. You ain’t gonna need it! Avoid the temptation to write code that you
  think might be useful, just because it suggests itself at the time.

- About testing on design and layout.

  基本原则: Don't test aesthetics in automated tests.
  
  这是因为: 1) 样式设计都是在静态文件中固定写好的, 这相当于常量的地位; 2) 对
  style 的测试容易比较 brittle, 需要经常修改; 3) 样式设计最好是由人类去辨别.
  
  但是, 进行某些基本的 style checking 还是可以的, 以保证比如静态文件正确加载,
  预期的效果大致达成. It is valuable to have some kind of minimal "smoke test"
  which checks that your static files and CSS are working.

  Try to write the minimal tests that will give you confidence that your design
  and layout is working, without testing what it actually is. Aim to leave
  yourself in a position where you can freely make changes to the design and
  layout, without having to go back and adjust tests all the time.

- Sometimes it's useful to skip on a test which is testing something you
  haven't written yet. 但注意及时 unskip it.

- Do not test for developer's stupidity. You should trust yourself (and fellow
  developers) not to do something deliberately stupid, but not something
  accidentally stupid. (If not, you have a much bigger problem.)

Techniques
==========

test double
-----------

mock
^^^^
- Mock 的基本概念是使用一个假的 service call 来替代真实的 service call. 来避免
  在单元测试中需要调用外部服务. service call 本身的设计应该是一个不透明的接口,
  即有规范设计的输入和输出. mock 能够完全替换这个 service call, 则需要具有完全
  相同的接口.

  Mock 必须具有与原操作相同的接口, 才能发挥测试的意义. 即保证功能实现中对外部
  服务的调用是正确的.

- 必要时还需要在单元测试中检查对 service call 的调用输入和输出的检测. 以保证对
  服务的调用确实是符合预期的 (因为 mock 接口正确还不够, 调用参数还需要正确.)

- 在 dynamic language 中, 经常使用 monkey patching 方法来 dynamically
  substitute calls to external services with a mock.

- 以 python 为例, 手动 mock 与单元测试的流程大致为:

  .. code:: python

    def test_foo():

        def fake_call(arg1, arg2, kwarg1=foo, kwarg2=bar):
            fake_call.arg1 = arg1
            fake_call.arg2 = arg2
            fake_call.kwarg1 = kwarg1
            fake_call.kwarg2 = kwarg2
            return value

        # mock
        module.external_call = fake_call
        # call operation being tested
        ret = operation_being_tested(a, b, c)
        # test operation's result and side effects
        # ...
        # test service call
        assert fake_call.arg1 == "something"
        assert fake_call.arg2 == "something else"

- 很多语言已经提供方便的 mock library, 一般无需手动构建替代的 mock function, 也
  无需手动替换方法和调用.
