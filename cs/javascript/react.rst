overview
========
- 在使用 React 构建前端的情景下, frontend and backend's 各自的功能是什么?
 
  * Frontend 完全负责展示. UI components are defined by JS code (React), not by
    backend template system.

  * Backend 负责提供 REST 数据 API. 前后端之间只通过 API 交换数据, 前后端完全
    解耦合.

- React 将前端的 UI 结构 (即 HTML 页面) 与操纵 UI 的交互逻辑 (即传统的前端 JS
  代码) 整合在一起. 这样真正做到了 view & control 的整合与封装. 这样, 做到了
  前端的真正的组件化与 OOP.

  与之相比, 传统的前端, 无论使用什么 UI component 和代码设计模式, 对一个组件的
  构建, 都需要分到两块相互孤立的代码中: 即 UI 放在一个 html 代码中, 初始化和
  交互等放在另一个 js 代码中. 明明是强耦合的相互关联, 却不得不分开写, 很不统一.

feature
=======
- declarative

- component-based

- learn once, write anywhere.
