- trivial 的 commits 可以合并成一个

- 不要纠结于历史的清晰性, 历史就是历史, 不要轻易调整 commit 的顺序

- 代码比 commit history 重要得多

- 每次 commit 都要写清晰地足够说明问题的 commit message

- 开发过程中及时进行 commit history 的梳理

- 创建新的本地 repo 后的第一件事就是修改 local 的 user.name 和 user.email !!!

- 不要轻易把 master/devel 等主线 branch merge 到 topic branch 里. 这会使 history tree 非常
messy. 如果非要引入相关修改, 首选 rebase.

- topic branch 应尽量短小, 以减少其他人的 topic branch 不包含自己的修改,
  却 merge 进入了其他 branch 所造成的信息缺失. 因此, 若一个 topic branch
  中包含一些相对独立的修改, 应拆成多个 topic branch, 以加快 merge back 的进度.

- git submodule vs git subtree

  * git subtree 是基于一些复杂、繁琐的命令, 例如 ``git read-tree --prefix=<prefix>``,
    ``git merge -s subtree``, 实现的 subtree 相关操作封装.
    从 ``git log --graph`` 可以看出 ``git subtree (add|merge) -P <prefix>``
    大致上就是将完全不同历史的 commit tree 通过 shift root 至指定的 `prefix`
    之后做 merge.

  * git subtree 提供了方便的 split 操作, 以重建独立的 subtree 的 commit tree.

  * 以 subtree 方式加入的 subproject 从各个方面都实实在在成为了 superproject
    的一部分. (因为是 `read-tree`.) 不存在 submodule 那样的完全独立的父子关系.
    subtree 仅有与引入 `commit` 相关的历史.

  * 由于 subtree 实际上是 superproject 的一部分, 所以对 subtree 的修改就是对
    superproject 自身的修改, 不存在 submodule 那样繁琐的双重 commit 操作 (在
    submodule 中 commit, 再在 superproject 中更新 submodule 的 commit).

  * git submodule 的很多操作步骤都很繁琐. 例如, 删除 submodule, 修改 submodule
    的默认 remote, submodule 中 commit 与 superproject 中的同步更新, etc. 相比
    之下, git subtree 由于只是一个目录, 就是在 superproject 中进行的操作, 没有
    增加复杂度.

  * git subtree 将 dependency 的代码十分透明地合并成为 superproject 自身的代码,
    这要求 developer 十分清楚某个 subtree 实际上属于其他 repo. 否则, git subtree
    带来的代码重复可能导致 code inconsistency.

  ref: https://www.atlassian.com/blog/git/alternatives-to-git-submodule-git-subtree

- Which to use `git submodule` or `git subtree`

  * 对于非 deps, submodule/subtree 都仅适用于有必要将代码分散到不同 repo 中的情况.

  * 对于 deps, 则需要使用 submodule/subtree. (前提是有必要集成 deps 的源代码, 而不是
    通过 package manager 安装 deps.)

  * 我不知道 submodule subtree 哪个更好. 但目前看来, submodule 能干的 subtree 都能干,
    而且流程更简单无痛. 所以我更愿意用 subtree.
