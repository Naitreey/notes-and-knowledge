terminology
===========
- regression. When new code breaks some aspect of the application which used to
  work.

test classification
===================

不同类型测试的宏观关系图:

.. code::

                                                      +
                                                      |
                                                      |
                                                      | functional test
                                                      |
                                                      |
                                                      |
                                    functionality 1   |                  functionality 2
                                                      |
                                                      v                                                      ......
                                                                        +----------------+
                             +----------------------------+------------------------------------------+------------------
                             |                            |             |                |           |
  presentation layer         |                            |             |                |           |
                             |     +-----------+          |             |                |           |
                             |     | unit test |          |             |                |           |
                             +------------------------------------------------------------------------------------------
                             |     +-----------+          |             |                |           |
                             |                            |             |                |           |
                             |                            |             |                |           |
                             |                            |             |                |           |
     inner layer1            |                            |             |                |           |
                             |                            |             |                |           |
                             |     +-----------+          |             |                |           |
                             |     | unit test |          |             |                |           |
                             +------------------------------------------+ integration-----------------------------------
                             |     +-----------+          |             | test           |           |
                             |                            |             |                |           |
                             |                            |             |                |           |
                             |                            |             |                |           |
                             |                            |             |                |           |
                             |                            |             |                |           |
         .                   |                            |             |                |           |
         .                   |                            |             |                |           |
         .                   |                            |             |                |           |
         .                   |                            |             |                |           |
                             |                            |             |                |           |
                             |                            |             |                |           |
                             |                            |             |                |           |
                             |     +-----------+          |             |                |           |
                             |     | unit test |          |             |                |           |
                             +------------------------------------------------------------------------------------------
                             |     +-----------+          |             +----------------+           |
                             |                            |                                          |
                             |                            |                                          |
     core layer              |                            |                                          |
                             |                            |                                          |
                             |                            |                                          |
                             |                            |                                          |
                             +----------------------------+------------------------------------------+------------------


在产品研发的不同阶段, 各种测试的作用:

- 在需求确定后, 进行宏观功能设计. 宏观功能设计完成后, 具体化为功能性测试.

- 研发人员将需求具体化为研发阶段的功能性测试.

- 根据功能性测试, 实现各个模块和实现层.

- 对于每个模块和实现层, 通过单元测试设计模块实现, 检测模块行为.

- 对一个功能的各个模块实现完毕后, 通过集成测试打通各个模块和实现层, 检测模块之
  间的交互是否符合预期.

- 集成测试通过后, 使用研发阶段的功能性测试来打磨整个功能的外部行为, 检查从用户
  的角度整个功能的外部表现是否符合需求.

- 每个服务的开发都按照上述方式进行. 各个服务构成系统整体, 进行系统测试.

- 系统测试通过后, 测试人员使用功能性测试检验系统整体是否符合需求.

unit testing
------------

integration testing
-------------------

- It is a low level testing performed after unit testing.
  
- It is both black box and white box testing approach so it requires the
  knowledge of the two modules and the interface.

- Integration testing is performed by developers as well test engineers.

- Here the testing is performed on interface between individual module thus any
  defect found is only for individual modules and not the entire system.

system testing
--------------
- A system test checks the integration of multiple systems in your application.
  例如, 测试当 web server, db server, queue, static file server, etc. 全部接通
  时, 整个系统是否按照预期行为运行.

- Both functional and non-functional testing are covered like sanity,
  usability, performance, stress an load.

- It is a high level testing performed after integration testing.

- Here the testing is performed on the system as a whole including all the
  external interfaces, so any defect found in it is regarded as defect of whole
  system

- 对于功能性测试部分, 可以基于研发阶段的功能性测试的验证内容来改写.

- 测试人员进行的系统测试一般是在一个单独的 staging environment 中进行的.

- 自动化的功能测试系统还有助于检测 staging environment 上的应用系统的配置
  和部署情况.

- 系统测试在很大程度上可以由功能测试来代替, 可以不单独进行.

functional testing
------------------
- A functional test or acceptance test is meant to test that our system works
  from the point of view of the user.

- A FT is often a full-stack, end-to-end test.

- 功能性测试可以分两种:

  * 在研发阶段进行的功能测试. 这种 FT 的目的是为需求实现提供正确性反馈, 在 TDD
    中还有从整体上驱动开发的意义. 这种功能性测试应该要比较快, 以提供相对迅速的
    反馈, 支持下一步研发.

  * 在构建阶段以及人工测试阶段进行的功能性测试, 这种测试需要全面, 可以很慢.
    它必须运行在整个系统之上, 不能存在 isolation.

- 在 CI 过程中运行的 FTs, 如果以 failure 方式结束, 应该记录一些信息以便 debug.
  例如, 出错时的浏览器截图, 此时实际的 html 页面.

  * 对于截图和 html dump, 记录以下 metadata: test file, test class, test
    method, window id, time.

smoke testing
-------------
- A smoke test is a quick run through of a site;  it focuses on critical
  functionality to ensure the site can perform basic features. 

- It should only takes a couple of minutes to complete, up to ten minutes at
  most. What is great about smoke tests is you can perform them either daily or
  every other day.

- The term came to software testing from a similar hardware test -where the
  device passed if it did not catch fire (or smoked) the first time it was
  turned on!

regression testing
------------------

- A regression test is an in-depth, thorough examination of a site. It tests
  all of the complex user stories and detailed nuances of the site.

- It may take many hours to complete. Performing a regression test ensures any
  changes made did not negatively impact any of the functionality of the site.
  A regression test will cover every feature, new and old, along with bug fix
  checks to make sure bugs did not reappear in the software.

design patterns
===============
- slow tests and fast tests.

  * integration/functional/system/regression tests can be slow.

  * unittests (both low-level modular tests and high-level functional tests)
    must be fast.

- 小心不要直接 running integration/system tests against clones of production data.
  至少要将 sensitive content 以及用户真实 profile 等信息做处理后再使用. 这不仅仅是
  避免隐私泄露. 更重要的是, 避免测试操作直接影响真实用户, 例如给真实用户发了邮件、
  短信等.

References
==========

.. [SmokeVSRegression] `WHAT’S THE DIFFERENCE BETWEEN SMOKE TESTING & REGRESSION TESTING? <https://www.bytelion.com/smoke-testing-vs-regression-testing/>`_
.. [IntegrationVSSystemTesting] `What is the difference between system and integration testing? <https://www.quora.com/What-is-the-difference-between-system-and-integration-testing>`_
