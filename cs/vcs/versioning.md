# versioning scheme

基于 semantic versioning.

## 版本号的格式

-   研发和测试阶段的版本号, 即非发行版:
    ```sh
    dev.<branch>+<build>[.dirty]
    ```
    其中,
    *   `<branch>` 为功能分支;
    *   `<build>` 为 commit hash 的前 10 位;
    *   `.dirty` 指的是程序代码存在未提交修改.
-   正式发布阶段的版本号, 即发行版:
    ```sh
    <major>.<minor>.<patch>
    ```
    其中, major, minor, patch 都是非负整数.
    *   `<patch>` 在程序引入 backwards compatible bug fixes 时递增, 注意
        此时不该引入新功能.
    *   `<minor>` 在程序引入 new, backwards compatible functionality 时递增.
        minor version 递增时, patch level 须重置为 0.
    *   `<major>` 在程序引入 backward-incompatible changes 时递增.
        major version 递增时, minor & patch level 须重置为 0.
-   某个版本在正式发布之前, 若需要进行整体测试, 内测, 回归测试等, 使用
    预发布版本:
    ```sh
    <major>.<minor>.<patch>-(alpha[.<N>]|beta[.<N>])
    ```

## 版本号的生成

-   当 HEAD 没有 tag 时, 认为是研发或测试阶段. 此时根据环境自动生成版本号.
-   当 HEAD 有 tag 时, 直接使用 tag 作为版本号.

## 版本号的保存

-   在 source repository 中使用时, 版本号不保存或临时保存.
-   生成安装包时, 版本号保存在配置文件中.

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
