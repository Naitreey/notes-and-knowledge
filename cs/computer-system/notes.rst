- 现代的计算机中, 不同组件通过各种 bus 进行 communication 的过程更像是计算机网络.
  这种交流过程涉及 protocol, connection, packet 等概念.

- DIMM slot 不是 PCIe slot, 因为内存读写速度比 PCIe 3.0 速度高很多.

- host controller 或 host bus adapter 是某种外部设备的信号协议和 host bus 的信号
  协议之间做转换做适配 (adaptation) 的设备. 这种 host adapter 一般体现为某种扩展卡,
  该卡上可以连接别的信号输入或输出 (例如显卡); 或者是直接集成在主板上, 只留出一个
  外部设备的插口 (例如 SATA).

- 一般情况下 SAS 接口和总线协议等可以兼容 SATA, 但反之不行.

- M.2 是 form factor standard. 它定义的是 expansion card 的外观尺寸和接口类型等
  信息, 而没有定义通信协议. 所以与它配合可以使用 USB, PCIe 或 SATA controller.

- AHCI 和 NVMe 都是 HBA 的 driver specification.
  AHCI 是为 rotating media 设计的, 对 SSD 比较低效; NVMe 是专门为使用 PCIe bus 的 SSD
  设计的统一标准, 利用了 SSD 特性和操作系统的并行特性等, 比 AHCI (配合 SATA bus 或 PCIe
  bus) SSD 读写都快很多.

- 一个设备不需要驱动不是说它真的不需要驱动, 而是说它遵从某种标准规范, 使用某种
  标准驱动, 而在大部分情况下, 这种标准驱动的 kernel module 已经安装好了.

- USB

  * 标准: 1.0, 2.0, 3.0, 3.1.

  * 速度: Low Speed (1.0), Full Speed (1.0), High Speed (2.0), Super Speed (3.0),
          Super Speed+ (3.1).

  * 接口类型:

    - plug: type-A, type-B, type-C.

    - receptacle: type-A, type-B, type-C, type-AB

    - 子类型: standard, mini, micro

    注意 USB 标准的设计考虑的是计算机 (host) 和其他设备之间的连接, 这种连接在设计时
    考虑了方向性 (例如供电的方向性, 避免过载等). 为了在物理连接上能强制实施这种方向性,
    USB cable 的两端一般采用不同类型的 connector, 例如 standard-A 和 micro-B. 由于
    host 一般是计算机等大型设备, A 端一般采用的是 standard 子类型, 而 B 端一般采用
    mini 或 micro 类型, 或者另一端不是 B 而是 C.

    cable 两端都不是 standard-A 的情况出现在 USB On-The-GO 中, 也就是说两个便携设备之间
    直连的情况.
