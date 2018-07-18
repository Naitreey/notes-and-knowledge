analysis
========
- git annex + bup

  :pros:
         - 由于在 git database 中只保存 symlink, checkout/status/commit 等等
           速度都很快.

  :cons:
         - 会修改 pre-commit hook, 这样需要手动和我自己的 pre-commit hook 来合并,
           但这个修改对每个 repo 是一次性的, 所以还可以接受.

         - git annex 和 bup 并不能很好的协作. 整个流程并不自然, 比较繁琐.
           git annex 虽支持 bup 作为 remote, 却需要 bup 的 local 和 remote
           两端, 不能只要一个 local 的 bup 存储或一个 remote bup 存储.
           这样必有一个是没用的.

         - git annex 的存储 `.git/annex` 只能是一个个完整的文件. 并没有任何存储的
           节省. 不能用 bup 的存储作为本地的 `.git/annex`.

         - git annex 的操作步骤比 git lfs 繁琐.

         - git annex 会把每个推到 bup 的文件在 bup 中创建一个分支. 太傻逼了.
           而且设置了 `remote.<name>.annex-bup-split-options` 为 `-n <branch>`
           也没用, 因为它会再加一个 `-n`.

- git lfs

  :cons:
         - checkout/status/commit 等等都太卡了.

         - 和 git annex 一样, 不会减少空间占用.

- 结论:
  * git annex 单独使用可用来进行大文件版本管理, 它足够迅速. 但缺点是占用空间大.
    若不介意硬盘空间占用则可用.

  * bup 单独使用可以用来做大文件版本管理, 它对存储的使用比较高效. 若对硬盘空间
    比较介意则可用.

  * 目前, 将 git annex 和 bup 结合使用还有很多缺陷, 但基本可用.
    使用方式如下:

    - 每个 client 包含一个 local git repo (含 git annex).
      remote 包含一个 bare git repo 和 bup repo.

    - client 中, 设置 git remote 为 上述 remote bare git repo 和 remote bup repo.

    - 本地使用时, 只在 `.git/annex` 中保留最新版本的 annexed files (保证读取效率).

    - 从 local 向 remote 同步时, local git repo 如常 push 至 remote git repo,
      再将 annexed files 的各版本 copy 至 remote bup repo.
      (``git annex copy --to=<remote-bup> --not --in=<remote-bup>``)

    - 从 remote 向 local 同步时, local git repo 如常从 remote git repo 中 fetch,
      再将本地缺少的文件从 remote bup 中 get 至本地.

    此外, 也可以在 client 上加上一个 local bup repo, 这样的好处是 client 具有全部
    大文件的历史数据, 可完全脱离 remote bup repo 来工作. 但缺点是, 在流程上更繁琐,
    且存在本地重复存储.

- 仍需解决的问题:
  bup 作为 remote 使用时, 需要解决产生大量分支的问题. 这既是不必要的、混乱的
  (为什么不能在 push 到 bup 时指定保存的分支?), 长期使用又会有潜在问题 (当一个 bup
  中达到数千个分支时会有效率问题).
  一个临时的解决办法是, 单独为每个 git annex repo 创建一个 bup remote repo. 只用来
  存储这个 annex repo 的大文件.
