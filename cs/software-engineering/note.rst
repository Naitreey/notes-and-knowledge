time estimation
===============

- 大致方法
  
  预估时间时, 一定要明确需求. 如果给出的需求不够清晰, 那就自己将需求细化, 然后
  和对方谈, 双方对需求都达成一致后, 才叫需求明确了.

  对需求拆解得越仔细, 对时间的预估才可能越准确. 细化到什么地步呢? 至少细化到
  都有哪些功能, 每个功能要实现成什么样子.

  光分析需求还不够. 细化需求之后, 必须比较仔细地思考你准备如何实现这些需求,
  使用什么模型、什么技术、数据库大致如何构建、每个模块的业务逻辑大致是什么样子、
  这里面可能遇到哪些问题等等. 也就是说, 必须从需求出发, 列出一个大致的 todo list.
  todo list 中每项最长时间不能大于几天, 这是为了逼你将任务切分得足够细致,
  从而知道自己到底要做什么, 保证对实现步骤有了大体的概念. (如果你对需求的实现
  没有完全或完全没有概念, 那不可能 有比较准确的时间估计.) 这些思考和设计过程即
  使在预估时间时不做, 在真正实现时也是 要做的. 所以这并不是在浪费时间, 事实上,
  这很大程度上是双赢的局面: 你通过细致的 分析, 勾勒出了大致的实现思路和步骤
  (早晚要做的事情); 需求方了解了大致所需时间, 降低了不确定性或焦虑之类的情绪.

  至此为止, 根据你列出的 todo list, 去估计时间. 估计时间时, 还要考虑到休假, 生病,
  其他事物的干扰等花费的时间, 在净时间之外要加上这些 overhead time.

- 文档: 记录你对需求的整理和细化 (需求文档); 记录你对需求实现的设计 (设计文档);

- 根据对方的要求时间精度要求给出相应的预估时间. 如果对方要求的时间跨度比较低
  (比如几个月), 那么你应该给出比较低精度的预估时间 (比如 3-4 个月).
  如果对方的时间精度要求比较高 比如 5 天, 你应该先尝试低精度的预估时间,
  然后被反驳了再给出高精度时间.

- 需求提出方和需求实现方再谈时间方面, 很多时候是个交流问题、心理学问题、博弈问题.

- The person doing a given piece of work has final say on its estimate. No
  managers, leads or committees are allowed to overrule estimates, only
  re-assign work to someone else.

- The more you break tasks down, the more reliable the final estimate will be.
  The effect is twofold: first, over- and under-estimate errors will tend to
  cancel each other out more, and second, to perform the breakdown you end up
  thinking about the work in more detail, improving the overall accuracy.
