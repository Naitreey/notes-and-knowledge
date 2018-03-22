# versioning scheme

基于 semantic versioning.

## 考虑
version must be pre-defined before build, before we are sure
app is ready for production. Therefore,
-   cannot rely on git tag. tag is made only when app is ready.
-   cannot be absolutely auto-generated. it must be able to
    contain `major.minor.patch` info, not just branch and hash.

## 版本号的格式
```sh
<major>.<minor>.<patch>[-dev+<branch>.<build>][.dirty]
```

其中,
*   `<patch>` 在程序引入 backwards compatible bug fixes 时递增, 注意
    此时不该引入新功能.
*   `<minor>` 在程序引入 new, backwards compatible functionality 时递增.
    minor version 递增时, patch level 须重置为 0.
*   `<major>` 在程序引入 backward-incompatible changes 时递增.
    major version 递增时, minor & patch level 须重置为 0.
*   major, minor, patch 都是非负整数.
*   `.dirty` 指的是程序代码存在未提交修改.

对于研发阶段, 存在 `-dev` 部分, 其中,
*   `<branch>` 为功能分支;
*   `<build>` 为 commit hash 的前 10 位;

## 版本号的生成

-   确定新版本时, 给相应 commit 打 tag.
-   每次发布一个版本后, 开始新版本开发. 设置 major, minor 为新版本号,
    patch 重置 0, extra version 设置 `dev`.
-   在一个版本结束开发, 进入回归测试阶段时, 去掉 extra version number.

## 版本号的保存

major, minor, patch, extra 等版本号保存在单独的配置文件或代码文件中.
与版本号生成逻辑配合使用.

根据软件使用情况不同, 版本号字符串可以预先生成, 也可以 runtime 再生成.

## 说明

-   一旦某个版本发布, 任何新的修改都必须递增版本号. 代码和版本必须有一一对应
    关系.
-   当 `major=0` 时, 为初始开发阶段. 该阶段没有义务保持向下兼容. 整个项目处于
    非稳定状态, anything can change at any time.
-   pre-release 版本部分在主要版本部分之后, 以 `-` 起始, 直到 `+` 符号或结束.
    build metadata 部分以 `+` 起始, 直到结束.
-   版本优先级. 版本比较时, major, minor, patch 优先级依次降低. 当 major, minor,
    patch 相同时, 预发布版本比正式版优先级低. 两个预发布版本之间比较时, 分别比较
    以 `.` 分隔的各个部分. 在每个部分中, 若为数值, 则数值大的优先级高; 若为字符,
    则按照 ASCII 顺序决定优先级. A larger set of pre-release fields has a
    higher precedence than a smaller set, if all of the preceding identifiers are
    equal.
-   关于 functionality deprecation. When declaring deprecation, increment minor
    version number; when dropping deprecated functionality, increment major version
    number.

## References

-   [Semantic Versioning Specification](https://semver.org/)
