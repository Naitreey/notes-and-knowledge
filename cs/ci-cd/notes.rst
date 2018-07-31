continuous integration
======================

workflow
--------

- A commit to your source revision control system would trigger a build on your
  CI system, which would then push a new image to your Docker Registry if the
  build is successful. A notification from the Registry would then trigger a
  deployment on a staging environment, or notify other systems that a new image
  is available.

- 首先需要执行源代码仓库下的所有单元测试、集成测试和研发阶段的功能性测试.

- 测试通过后才可以构建.

- 构建后自动在 staging environment 运行一套 staging system.
  
- 然后执行完善的自动化功能性测试.
