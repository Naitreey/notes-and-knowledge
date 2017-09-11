tools comparison
================

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

- agentless and agent-based

  * agent-based 的方式在机器很多、容器很多时, 会不会导致控制端响应不过来?
    以及这样导致的网络负荷问题.

  * agentless 方式需要借助某种通用方式连接 nodes, 一般是 ssh. 因此需要
    在每个节点上单独开账户, 并保存 ssh 密码.
