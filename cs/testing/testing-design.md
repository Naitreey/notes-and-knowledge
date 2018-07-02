# 前言

-   我想要做的不仅仅是单元测试, 而是一整套自动化的功能检验体系. 单元测试是这个体系中的重要一环, 但不是全部.
-   这涉及多个阶段和多个层次的测试. 例如, 在研发阶段, 需要功能性测试和单元测试, 分别是从宏观用户层进行的
    测试和微观实现层进行的测试; 在 CI 阶段, 需要集成测试.
-   一步一步去实践, 从研发阶段的测试做起.
-   仍然很初步, 需要继续学习和体会, 改进.

# methodology

测试驱动开发 (tdd)

## what

...

## why

...

## how

# design

## functional test

从系统外部的视角, 也就是用户视角来检验功能模块. 

用户能看到的是界面, 就从界面测试.

怎么做:

## unit test

类似上面的思路

## on build stage

# tools

selenium, webdriver, unittest, django testing framework, etc

# references

-   obeying testing goat
-   docs
-   wikis

# todos

-   finish reading and understanding tdd and related design patterns
-   实践 tdd 的方法, 实现一些新功能例如...
-   逐步给现有功能添加功能性和单元测试