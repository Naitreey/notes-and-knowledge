# versioning scheme

基于 semantic versioning.

## 版本号的格式

-   研发和测试阶段的版本号, 即非发行版:
    ```sh
    dev.<branch>+<build>[.dirty]
    ```
    其中,
    *   `<branch>` 为程序版本所在分支;
    *   `<build>` 为 commit hash 的前 10 位;
    *   `.dirty` 指的是程序代码存在未提交修改.
-   正式发布阶段的版本号, 即发行版:
    ```sh
    <major>.<minor>.<patch>
    ```
    其中,
    *   `<patch>` 在程序引入 backwards compatible bug fixes 时递增, 注意
        此时不该引入新功能.
    *   `<minor>` 在程序引入 new, backwards compatible functionality 时递增.
        minor version 递增时, patch level 须重置为 0.
    *   `<major>` 在程序引入 backward-incompatible changes 时递增.
        major version 递增时, minor & patch level 须重置为 0.

## 版本号的生成

-   当 HEAD 没有 tag 时, 认为是研发或测试阶段. 此时根据环境自动生成版本号.
-   当 HEAD 有 tag 时, 直接使用 tag 作为版本号.

## 版本号的保存

-   在 source repository 中使用时, 版本号不保存或临时保存.
-   生成安装包时, 版本号保存在配置文件中.

## References

-   [Semantic Versioning Specification](https://semver.org/)
