tools comparison
================
- fabric vs configuration management system.

  * Fabric is an excellent choice for executing scripts in one or more remote
    systems. 它的用处就在于此, high-level 的 (更多的时候比 paramiko 易用) 的
    remote execution library.
   
  * 然而对于配置管理系统, remote execution 只是一部分, 例如还有配置状态声明,
    配置状态保证与检查. 所以需要专门的配置管理系统. Fabric 之类的远程执行
    library 可以是它的一个组成部分.

- ansible vs salt vs puppet vs chef

  * ansible: agentless
    salt: agent-based
    puppet: agent-based
    chef: agent-based

  * ansible (stars: 25000+) -- unknown
    salt (stars: 8000+) -- unknown
    puppet (stars: 4600+) -- used by so many companies
    chef (stars: 4900+) -- facebook

  * ansible -- python2
    salt -- python2
    puppet -- ruby
    chef -- ruby

  * ansible 适合进行 orchestration 类型的任务.
    进行大集群的 state change, 原始的 ansible 可能不合适, 需要 ansible tower.
    ansible 顺序对每个机器执行操作, 很慢.

  * puppet 适合维持大集群的配置状态.

- agentless and agent-based

  * agentless 需要 master 端去 push, 遵从 push model;
    agent-based 需要各 minion 端去 pull, 遵从 pull model.
    push model doesn't scale very well.

  * agent-based 的方式在机器很多、容器很多时, 会不会导致控制端响应不过来?
    以及这样导致的网络负荷问题.

  * agentless 方式需要借助某种通用方式连接 nodes, 一般是 ssh. 因此需要
    在每个节点上单独开账户, 并保存 ssh 密码.

  * agentless 方式只需维护控制端, 不涉及到对各节点上的 agent 软件升级、配置
    等问题.

  * 面对不同网络环境的问题.
    如果节点分布在不同的私有网络中, 例如分布在多个机房中, 一个外部的 master
    控制端难以直接主动访问各个节点. 若要访问, 必须通过 VPN 或者在各个机房的
    入口处对所有机器设置端口映射. 这是非常繁琐的, non-scalable 的. 这时,
    push model 就不合适. 由于各个节点可以访问外网, pull model 就方便很多.
