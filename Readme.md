# 事件驱动系统化交易框架

In ONE file...

![Architecture](./assets/fig1.png)

## V1

100 行代码 + 1 张图，理解系统化交易事件驱动框架。

量化交易开源社区绝大部分框架都是采用了事件驱动设计模式，比如：

- vnpy
- backtrader

主要的组成部分：

- Engine *
- EventBus *
- DataFeed *
- Strategy *
- Execution
- Portfolio
- Risk
- Other

[>> 视频讲解 v1](https://www.youtube.com/watch?v=wm7QLlzgo2M&t=1s)