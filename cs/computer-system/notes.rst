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

- 整个主板上的各个组件需要的时钟频率都是从一处生成然后再转换成各种总线所需的
  频率的. 原始的时钟频率可能有两个来源:

  * 对于过去的设备, 基础时钟频率由 clock generator 生成, 再应用于 FSB 上.

  * 对于现在的设备, 基础时钟频率由 PCH 生成, 再通过各种与之连接的总线转换和传递出去.

  其他所有 bus 的工频都是
  基于这个频率衍生出来的, 比如 CPU, DRAM, PCIe, 等. 其中, CPU 的工作频率是
  clock frequency * cpu multiplier.

- Double data rate (DDR) 可以将传输频率提高为 FSB/QPI 上时钟频率的两倍.
  (QDR -- quad 则能变成 4 倍.) 注意 DDR 不仅仅要内存 DIMM 条支持, 还需要
  总线去生成 DDR 的传输频率, 即需要 CPU 和内存之间的 memory bus 支持.

- CPU 和 RAM 的速度差异中很重要的一部分原因是 CPU 时钟频率和 memory bus 的
  时钟频率的差异. 也就是说, 因为这个总线的传输频率相对 CPU 的频率慢很多, 所以需要在
  CPU 里面设置缓存 (L1,2,3 cache), 以保证所需数据的实时获取.

- 主板 (上面的 memory bus) 支持的内存频率以及 CPU memory controller 支持的内存频率
  (即 uncore 访问内存的频率) 限制了对内存的频率选择. 如果内存的频率比 CPU 支持的
  频率高, 内存也只会 downclock 至 memory controller speed.

- 现在的 CPU 已经整合了 northbridge 的部分功能 (整合后成为了 CPU 的 uncore),
  包括 memory controller, 一部分 PCIe lanes 等. 北桥的其他功能和南桥的全部功能
  整合为 PCH, 仍称为 chipset. 原来的北桥和南桥之间的通信, 即现在的 CPU uncore
  和 PCH 之间的通信, 通过 DMI 进行.

  QPI 大致可认为是一种与 CPU 内部和 CPU 之间的 bus, 在 CPU uncore 中有 QPI controller.
  QPI 代替 FSB 在 CPU core 和 uncore (即之前的部分北桥) 之间通信, 并且在 CPU 之间通信
  也使用 QPI.

- 注意 DMI 3.0 每条 lane 速度与 PCI-e v3 相近, 基本上 1GB/s, 但 DMI 3.0 只有 4 条 lanes.
  所以 throughput 最大只有 4GB/s.

- CPU 中有 MMU, 也有 IOMMU. 一些设备有自己的 IOMMU, 例如显卡的 GART.

- MMU 在做 virtual memory address -> physical memory address 的转换时, 若发现
  要转换的虚拟内存地址在 page table 中, 但没有对应的物理内存地址, 则向 CPU core
  发送 valid page fault 信号. CPU 将控制权移交 kernel, kernel 看到 valid page fault
  则将对应的物理内存 swap 回 RAM 中.
  若发现要转换的虚拟内存地址根本不在 page table 中, 则 signal invalid page fault.
  kernel 对应地进行处理, 将请求进程 segfault 掉 (并 coredump) 或者是 bus error.

- 对于 x86-64 CPU, MMU 一般支持 4KB 的 page table entry (PTE), 并且支持 1GB 的 huge page.

- DMA 指的是这样的内存和设备之间的数据传输: CPU 只负责发起传输, 而不干涉、监控
  传输过程, 整个传输过程由设备和内存两者之间协商进行, CPU 去做别的事情, 传输完成后
  CPU 收到设备的中断. 因此, DMA 可以发生在 peripheral 和 ram 之间, 可以发生在 ram
  内部的不同区域, 甚至可以发生在 cpu cache 和 ram 之间.

  DMA 分为 first-party DMA 和 third-party DMA. 后者是通过一个专用的 DMA controller
  (peripheral processor) 模块协调设备之间的 DMA 数据传输; 前者是通过 bus mastering
  机制, 由需要传输数据的设备要求控制 bus, 然后发起并进行 DMA 传输. 在 PCI-e 的现代
  系统中, 都是 first-party DMA, 即 bus mastering 机制.

  对于 PCI-e bus 系统, PCH 上的 PCI-e bus controller 是 bus arbitrator.
  设备向它发起 mastering request. 获得许可后, 设备的 DMA 操作指令经由 PCI-e bus
  至 PCH, 经由 DMI 至 CPU uncore (memory controller), 经由 DDR4 memory bus 至
  DIMM RAM 设备.

- Modern memory buses are designed to connect directly to DRAM chips. 这大致意味着
  memory bus 本身的速度上限相对于 DIMM 本身的速度可能是一个高阶量, 可以不去考虑.
  只考虑内存条本身的数据传输速度即可.
