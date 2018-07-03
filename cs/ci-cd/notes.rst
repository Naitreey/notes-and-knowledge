continuous integration
======================

- workflow

  A commit to your source revision control system would trigger a build on your
  CI system, which would then push a new image to your Docker Registry if the
  build is successful. A notification from the Registry would then trigger a
  deployment on a staging environment, or notify other systems that a new image
  is available.

- 构建后可以自动在 staging environment 运行一套 staging system, 用于自动化的
  集成测试.
