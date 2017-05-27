- 现代的计算机中, 不同组件通过各种 bus 进行 communication 的过程更像是计算机网络.
  这种交流过程涉及 protocol, connection, packet 等概念.

- DIMM slot 不是 PCIe slot, 因为内存读写速度比 PCIe 3.0 速度高很多.

- host controller 或 host bus adapter 是某种外部设备的信号协议和 host bus 的信号
  协议之间做转换做适配 (adaptation) 的设备. 这种 host adapter 一般体现为某种扩展卡,
  该卡上可以连接别的信号输入或输出 (例如显卡); 或者是直接集成在主板上, 只留出一个
  外部设备的插口 (例如 SATA).
