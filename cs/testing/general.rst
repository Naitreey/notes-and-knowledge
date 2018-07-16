terminology
===========
- regression. When new code breaks some aspect of the application which used to
  work.

test classification
===================

unit testing
------------

functional testing
------------------

integration testing
-------------------
- Testing the collection and interface modules to check whether they give the
  expected result.

- Only Functional testing is performed to check whether the two modules when
  combined give correct outcome.

- It is a low level testing performed after unit testing

- It is both black box and white box testing approach so it requires the
  knowledge of the two modules and the interface.

- Integration testing is performed by developers as well test engineers.

- Here the testing is performed on interface between individual module thus any
  defect found is only for individual modules and not the entire system

system testing
--------------
- Testing the completed product to check if it meets the specification
  requirements.

- Both functional and non-functional testing are covered like sanity,
  usability, performance, stress an load.

- It is a high level testing performed after integration testing.

- Here the testing is performed on the system as a whole including all the
  external interfaces, so any defect found in it is regarded as defect of whole
  system

- 对于功能性测试部分, 可以基于功能性单元测试的验证内容来改写.

- 测试人员进行的系统测试一般是在一个单独的 staging environment 中进行的.

- 自动化的功能测试系统还有助于检测 staging environment 上的应用系统的配置
  和部署情况.

- 在研发阶段, 自动化的集成测试和系统测试脚本 (或系统) 也是很有帮助的.
  因为, 研发时当一个功能开发完毕 (已经通过了单元测试与功能性的单元测试),
  还需要检查多个服务集成时是否通畅, 各种行为是否符合预期, 等等. 此时,
  集成测试和系统测试脚本就能用上.

acceptance testing
------------------

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
