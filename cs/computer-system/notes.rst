- 现代的计算机中, 不同组件通过各种 bus 进行 communication 的过程更像是计算机网络.
  这种交流过程涉及 protocol, connection, packet 等概念.

- DIMM slot 不是 PCIe slot, 因为内存读写速度比 PCIe 3.0 速度高很多.

- host controller 或 host bus adapter 是某种外部设备的信号协议和 host bus 的信号
  协议之间做转换做适配 (adaptation) 的设备. 这种 host adapter 一般体现为某种扩展卡,
  该卡上可以连接别的信号输入或输出 (例如显卡); 或者是直接集成在主板上, 只留出一个
  外部设备的插口 (例如 SATA).

- SATA 协议是支持 hotplug 的, 如果 SATA controller 实现了相应的功能, 就能 hotplug.
  注意要在拔下之前先 unmount filesystem.

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

  其他所有 bus 的工频都是基于这个频率衍生出来的, 比如 CPU, DRAM, PCIe, 等.
  其中, CPU core, L3 cache, DRAM 等的基础频率是名为 base clock frequency 的频率.
  这些组件及相关 bus 在收到 BCLK frequency 之后再转换成所需的更高的频率. 例如,
  CPU 的频率是 BCLK frequency * cpu multiplier.

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

- CPU uncore 或 system agent 中包含 memory controller, DMA controller,
  integrated GPU (iGPU), PCI-e controller, L3 cache, QPI controller,
  thunderbolt controller, 等.

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

- 主板的 BIOS 软件存在 flash memory 上 (NOR or NAND), 由于是 flash memory, 可以重写
  以升级 BIOS.

  主板的设置保存在 CMOS 存储上. CMOS 是 volatile 的, 需要通电以维持数据. 它的电力
  由主板上的电池提供. 所以把主板电池扣下来或者采用特定的 CMOS 短路机制可以重置
  主板设置. (重置 CMOS 应该能够重置主板密码吧?)

- 主板上的电池用于维持 CMOS 数据以及维持 Real Time Clock (RTC).

- reset button 如何工作的:

  按了 reset button 之后, 主板给所有设备发送 reset signal.
  由于 CPU 被 reset, 所以从固定的 reset vector 地址处开始执行. 对于 cold
  boot, northbridge (uncore) 把这个地址请求转发到 firmware flash memory 上;
  对于 soft boot, BIOS 已经在内存中了, 所以该地址请求直接转发到内存中的对应
  地址上. 总之, CPU 从 reset vector 处开始执行, 即开始执行 BIOS, 从而开始了
  boot sequence. BIOS 在 soft boot 时, 会跳过 POST 过程.

- Bootup sequence

  #. PSU 接通, 主板 chipset 等待 PSU 稳定下来, 期间给 CPU 发送 reset signal,
     防止 CPU 过早启动. chipset 收到 PSU 发送的 Power Good signal 之后, 停止
     抑制 CPU 运行.

  #. CPU 从主板 firmware (EEPROM/flash memory) 上的固定地址位置开始执行,
     即 UEFI/BIOS 开始接管启动流程.

  #. BIOS 进行 Power On Self-Test (POST), 检查 CPU, 中断控制器、DMA controllers
     以及 chipset 的其他设备, DRAM, 显卡, 硬盘等等. 并对这些硬件进行基本的配置.
     如今 POST 已经不会仔细检查 RAM 了, 否则会太慢, 只进行很基本的检查以及读取
     SPD info 来配置 CPU memory controller.

  #. BIOS 把自己加载到内存中. 此后, BIOS 程序只在内存中运行.

  #. BIOS 启动显卡, 点亮屏幕, 输出 POST 以及其他检测信息.

  #. BIOS 检查 USB, 硬盘, 键盘等 peripherals, 并输出相应信息.

  #. BIOS 读取系统时间, 读取 CMOS 存储的配置.

  #. BIOS 根据 CMOS 保存的启动顺序选择从哪个存储设备启动, 并从该设备读取
     bootloader 程序至内存. 若该存储设备是硬盘, 对于 BIOS-MBR, BIOS 读取
     MBR 来加载 bootloader; 对于 UEFI-GPT, UEFI 读取 EFI System Partition (ESP)
     来加载所需 bootloader.

  #. BIOS 将 CPU 控制权移交 bootloader. 自己仍在内存中, 成为 runtime service,
     供 bootloader 和 OS 使用.

  #. bootloader 使用 BIOS 访问存储设备, 读取自己的配置.

  #. bootloader 根据某个配置, 使用 BIOS 访问存储设备和文件系统, 找到并将 kernel
     和 initramfs 读入内存.

  #. bootloader 执行 kernel 并添加指定的命令行参数, 将 CPU 控制权移交 kernel.

- firmware 是主板的软件, UEFI/BIOS 是这个软件提供的面向操作系统的 interface.
  主板的 firmware 主要提供两种服务, boot service 和 runtime service.
  在启动时, 它主要提供硬件检查和配置以及加载 OS bootloader 的服务;
  在运行时, boot loader 使用 BIOS/UEFI firmware 来访问存储设备等, OS 使用 firmware
  来进行某些硬件控制.

- firmware 和 OS 各需要一套 driver, 以访问硬件. 显然 firmware 这套驱动要基础很多,
  只包含很基础的功能.

- 如今几乎所有的 PC/server 等类型的计算机的主板都使用的是遵循 UEFI 标准的固件.
  Linux/Windows/macOS 等都是 UEFI-aware 的, 意思是它们的 bootloader 能够在 bootup
  过程中调用 UEFI boot service 去访问硬件 (在 OS kernel 加载之前), 并且在 OS kernel
  运行过程中, 可以调用 UEFI runtime service 去进行某些硬件操作 (比如 RTC, fans, ACPI,
  suspend-to-RAM).

  OS kernel 通过自己的 driver 直接访问绝大部分硬件, 原因是:

  * kernel driver 可以灵活地使用设备的全部功能和发挥其性能;

  * 通过 UEFI/BIOS 转发会低效一些;

  * BIOS 运行在 real mode, 在 kernel 和 BIOS 之间切换需要切换 CPU 的模式 3 遍, 更低效.

  但仍有少量硬件操作需要依赖 UEFI/BIOS, 比如机箱风扇控制, RTC 的读写, ACPI 电源管理,
  suspend-to-RAM 等.

- BIOS 运行时 CPU 处于 16-bit real mode, 读取 MBR、加载 bootloader 和 bootloader
  的初始执行, 都是在 16-bit real mode 下.
  bootloader (e.g., GRUB) 的任务之一就是切换 CPU 到 protected mode.

  对于 UEFI 系统, UEFI 开始执行后很快就切换到 protected mode. 而 ESP 分区上的所有
  EFI applications 都是在 protected mode 中执行的. 注意到这些 ``.efi`` 应用都是
  PE32 executable, 使用的虚拟内存.

- UEFI 的设计要求易于扩展, 功能丰富、灵活. 这些自然要求 UEFI firmware 是运行在
  protected mode 或 long mode 中的, 并且具有模块化的设计 (EFI applications).

  UEFI 相对于 BIOS firmware 的一些优点:

  * 支持 GPT, 向后兼容 MBR.

  * 模块化设计 (EFI application).

  * 运行于 protected/long mode, 而不是 real mode. 能够实现复杂的 EFI application,
    从而可以构建灵活的 pre-OS environment.

- UEFI-GPT 组合在分区时要有 ESP 分区, 放置 EFI application, 包含 bootloaders 等.

- 几种 firmware 和硬盘分区的组合:

  * BIOS-MBR

  * BIOS-GPT

  * UEFI-MBR

  * UEFI-GPT

- flash memory 有两种: NOR flash 和 NAND flash.

  flash memory 中每个存储单元 (cell) 使用的是 floating-gate MOSFET.
  NOR flash 和 NAND flash 的导电逻辑 (什么输入对应什么输出) 分别类似于数电中的
  NOR gate 和 NAND gate, 故得名.

  NOR flash 的读写是 byte-level 的 random-access, 擦除是以 block 为单位.
  主要应用在嵌入式方面, 用来做 firmware 等 ROM (例如 motherboard BIOS/UEFI firmware)
  和 XIP memory 之类.

  NAND flash 的读写是 page-level 的 random-access, 擦除是以 block 为单位.
  它的设计目的就是代替传统机械硬盘, 大大提升读写速度. 因此它模拟 block device
  的交互逻辑. 由于去掉了 NOR flash 中 cell 的一些结构 (相当于从并联改成串联),
  可以把密度做高, 容量做大. 主要用于做大容量存储, 替代机械硬盘, 例如 SSD.

  flash memory 的一些限制:

  * 数据清除 (erasure) 必须以 block 为单位 (注意 erasure 不是 rewrite);

  * memory blocks 只支持固定数量的 program-erase (P/E, 写入-清除) 周期;

  * 对一个 cell 进行大量 read 操作会导致周围的 cell 的状态改变, 从而导致数据错误;

  由于这些麻烦的存在, flash memory 需要以下特殊处理:

  * 使用处理了这些问题的 flash memory 专用 filesystem; 或者添加用于处理这些问题的硬件
    flash controller, 从而在软件层面可以使用任意文件系统 (因在物理层有 controller 在
    处理这些麻烦).

  * 一个 flash memory 的真实大小比它的可用大小要大得到, 为了处理这些麻烦, 它需要大量
    的额外空间来记录额外的信息和数据.

- flash memory 技术里也用到了量子力学, floating-gate MOSFET 中通过势井和量子隧穿效应
  控制电子.

- DIMM 的各种参数和信息保存在了 DIMM 上的一个 EEPROM 中, 是标准的 SPD 信息形式.
  主板在 Power On Self-Test 过程中, 会通过 SMBus 读取 DIMM 的 SPD 配置信息,
  对 CPU uncore memory controller 进行配置.

- 主板风扇接口们 (一般 4pin 支持 PWM, 3pin 则不支持.)

  * CPU_FAN

    CPU 风扇接口, 若主板检测到 CPU 风扇没有正常工作, 会报警并终止系统运行.

  * CPU_OPT

    与 CPU_FAN 一样直接受到 CPU 温度的影响, 可能用于有些散热器提供了两个风扇的情况.

  * CHA_FAN

    机箱风扇接口.

  * AIO_PUMP

    专门给 All-in-One liquid cooler 使用的. 平时使用的水冷散热器就是 AIO liquid cooler,
    因为它把水冷所需的所有零件 (radiator, pump, tube, fans, water) 等都方便地弄在一起了.
    如果系统中需要第二套水冷, 比如给显卡水冷, 则可以插在 AIO_PUMP.

  * H_AMP_FAN

    高电流风扇接口, 支持高于普通电流需求的风扇, 或者用 splitter 接上两个
    普通电流风扇.

  * EXT_FAN

    扩展风扇接口, 可以额外接数个风扇.

  PWM fans 通过 PWM signal (Pulse-Width Modulation) 来控制风扇转速, PWM signal
  通过第四个 pin 来传输.

- Desktop Management Interface (DMI) 貌似是一个与 SMBIOS 相关但包含的范围更广的概念.
  总之, 系统中的硬件信息可以统一地标准化地从 DMI/SMBIOS table 中读取.
  它包含从 BIOS firmware 中读取的 SMBIOS 标准化数据. OS kernel 一般实现了
  DMI table 的收集和构建.

- NUMA 在有多个 CPU socket 的 server 中才有意义, 对单个 socket 的 desktop PC 没有意义.
  因为它涉及对 memory locality 的优化.

- multi-channel memory architecture 需要 CPU 和主板共同支持.

  要利用多个 "通道" 的好处需要将内存插在不同的通道中. 每个通道是一个完整的 64bit 数据
  流. 每个通道的末端可能插不止一根 DIMM 内存条, 但同一时刻只能访问它们中的一根, 所以
  一个通道上增加内存条数目只增加内存总量不提高内存访问 throughput.

  多个通道存在两种模式: unganged 和 ganged.

  * ganged mode 下, 多个通道合成一个通道, 这样带宽就是 64*N bit, 可以每次读写 64*N bit.
    但是实际上更多时候这样宽不能被很好利用, 实际效果不一定好.

  * unganged mode 下, 多个通道独立工作, 独立读写, 这有助于提高 concurrent processing
    的效率. 默认多通道内存架构工作在这个模式下.
