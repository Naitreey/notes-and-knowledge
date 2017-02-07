- trivial 的 commits 可以合并成一个
- 不要纠结于历史的清晰性, 历史就是历史, 不要轻易调整 commit 的顺序
- 代码比 commit history 重要得多
- 每次 commit 都要写清晰地足够说明问题的 commit message
- 开发过程中及时进行 commit history 的梳理
- 创建新的本地 repo 后的第一件事就是修改 local 的 user.name 和 user.email !!!
- 不要轻易把 master/devel 等主线 branch merge 到 topic branch 里. 这会使 history tree 非常
messy. 如果非要引入相关修改, 首选 rebase.
- topic branch 应尽量短小, 以减少其他人的 topic branch 不包含自己的修改, 却 merge 进入了其他 branch 所造成的信息缺失. 因此, 若一个 topic branch 中包含一些相对独立的修改, 应拆成多个 topic branch, 以加快 merge back 的进度.
