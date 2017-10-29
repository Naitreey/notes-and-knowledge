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

- 现在的 CPU 已经整合了 northbridge/southbridge 的部分功能 (整合后成为了 CPU 的
  uncore), 包括 memory controller, graphics PCIe lanes 等. 北桥和南桥的其他功能
  整合为 PCH, 仍称为 chipset. 原来的北桥和南桥之间的通信, 即现在的 CPU uncore
  和 PCH 之间的通信, 通过 DMI/FDI 进行.

- QPI 大致可认为是一种与 CPU 内部和 CPU 之间的 bus, 在 CPU uncore 中有 QPI controller.
  QPI 代替 FSB 在 CPU core 和 uncore (即之前的部分北桥) 之间通信, 并且在 CPU 之间通信
  也使用 QPI.

- CPU uncore 或 system agent 中包含 memory controller, DMA controller,
  integrated GPU (iGPU), PCI-e controller, L3 cache, QPI controller,
  thunderbolt controller, 等.

- CPU 的 Graphics PCI-e lanes 连接到主板上的 PCI-e slots 上, 一般是与 2 至 3 个 x16
  的 PCI-e 插槽像连. 构成 SLI 或 CrossFire 配置. 每个插槽的有效 lane 数目取决于插槽的
  使用方式以及 CPU 支持的最大 PCI-e lanes 数目.

- PCH 的功能包含对 non-graphics PCI-e lanes 的控制, 基础时钟频率的生成和转换,
  peripheral devices 与 CPU, memory 等相互访问时的中继 (FDI, DMI) 等.

- 注意 DMI 3.0 每条 lane 速度与 PCI-e v3 相近, 基本上 1GB/s, 但 DMI 3.0 只有 4 条 lanes.
  所以 throughput 最大只有 4GB/s.

- intel 虚拟化相关技术 (包含 VT-x, VT-d, 等) 的 cpu flag 是 ``vmx``.

- MMU 在做 virtual memory address -> physical memory address 的转换时, 若发现
  要转换的虚拟内存地址在 page table 中, 但没有对应的物理内存地址, 则向 CPU core
  发送 valid page fault 信号. CPU 将控制权移交 kernel, kernel 看到 valid page fault
  则将对应的物理内存 swap 回 RAM 中.
  若发现要转换的虚拟内存地址根本不在 page table 中, 则 signal invalid page fault.
  kernel 对应地进行处理, 将请求进程 segfault 掉 (并 coredump) 或者是 bus error.

- 对于 x86-64 CPU, MMU 一般支持 4KB 的 page table entry (PTE), 并且支持 1GB 的 huge page.

- CPU 中有 MMU, 也有 IOMMU. intel 称 IOMMU 为 VT-d 技术.

  peripheral device 在通过 DMA 机制访问内存时需要使用 IOMMU. 也就是说, CPU 首先
  把需要访问的 DMA 地址和读写长度传递给设备, 告诉设备可以开始传输了, 然后自己就
  不管了; 设备 DMA 访问内存需要通过 IOMMU 进行, IOMMU 将 DMA 地址转换成物理地址,
  再进行读写.

  在 linux 中, IOMMU 被识别为 ``dmar<N>`` (DMA remapping) interrupt device.

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

- 如何访问 DRAM 中存储的一个 bit: 向 DIMM 上一个确定的 memory chip 发送请求,
  给出要访问的 memory bank array 的编号, 给出这个 array 上要访问的 word line (行)
  和 bit line (列) 编号.

- 在 protective MBR 中写入了 bootstrap code 的 GPT 分区表可以在 BIOS-based system 中
  使用, 只要 bootloader 和 OS 本身都支持 GPT, 即它们本身可以直接识别和访问 GPT 分区表.
  例如 grub2 在 protective MBR 区域 (first LBA) 中写入 MBR 分区表所需的 Bootstrap code,
  这样在 BIOS 系统中也可以加载 grub bootloader.

- MBR 的大小总是 512 bytes; GPT 中各项的长度以 LBA 为单位, 总大小并不固定.

- LBA (Logical Block Addressing) 地址的单位与 HDD 的 logical block sector 大小一致, 即
  对于 512n/512e LBA 单位为 512B, 对于 4Kn LBA 单位为 4096B.

- 新的 HDD 的 sector size 都是 4KiB (Advanced Format), 这样比 512 bytes 的 sector size
  存储效率更高. 选择 4KiB 的原因是 virtual memory page size 一般是 4KiB.

  为了向后兼容, 4K HDD 有两种, 512e 和 4Kn. 前者兼容 legacy OS, 这些 OS 对 HDD 的读写以
  512 bytes 为单位; 后者只能用在较新的 OS 中, 这些 OS 的 IO 操作全部都是 4K-aligned,
  无论 logical sector size 是 512B 或 4KB.

- physical sector size vs logical sector size

  前者是 HDD 的实际上在存储时的 sector 大小, 后者是 HDD 能接受的最小 sector 大小.

  对于不同种类的 HDD, logical/physical sector size 分别是:

  512n: 512B/512B
  512e: 512B/4096B
  4Kn:  4096B/4096B

  512e 的固件对非 4K 对齐的写操作有一个 read-modify-write 的过程, 因此才能支持最小
  512B 的操作单元, 然而代价是性能降低.

  legacy OS 只能使用 512n 和 512e 的 HDD, 因为它们的读写以 512B 为单位.
  legacy OS 使用 512e 时有性能损耗.
  modern OS 三种都可以使用, 因为它们的读写是 4K-aligned.
  modern OS 使用 512e 时, partition boundary 需要是 4K 对齐的, 才能避免性能损耗.

  BIOS 显然读硬盘时以 512B 为单位, 因此不能访问 4Kn, 不能读 4Kn 上的 protective MBR,
  不能加载 bootloader, 但对于 512e 没问题.
  UEFI 可以直接使用 4Kn.

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

- 买内存、SSD 之类的也要看价格走势, 小心买亏了. 查看例如 DRAMeXchange 的走势图.

- flash memory 技术里也用到了量子力学, floating-gate MOSFET 中通过势井和量子隧穿效应
  控制电子.

- DIMM 的各种参数和信息保存在了 DIMM 上的一个 EEPROM 中, 是标准的 SPD 信息形式.
  主板在 Power On Self-Test 过程中, 会通过 SMBus/I2C 读取 DIMM 的 SPD 配置信息,
  对 CPU uncore memory controller 进行配置.

- SMBus 很大程度上是 I2C bus 的一个更严格定义的子集. 在实际 implementation 中,
  两种总线经常配置成兼容的, 在同一个 bus 上运行. 在 Linux 下 SMBus 及 I2C 设备
  统一归类为 i2c 设备. 加载 i2c-dev kernel module 后, 显示为 ``/dev/i2c-*``.

  在一般的主板上, SMBus 和 I2C bus 设备都存在, 而且. 哪些是哪些用 ``i2cdetect -l``
  来检查. 一般可以发现, 绝大部分都是 I2C 设备, 只有个别是 SMBus 设备.

  在计算机系统中, I2C (以及 SMBus) 一般用于:
  与 DIMM 交互, 访问 SPD data;
  管理 PCIe 设备 (SMBus);
  访问 CMOS;
  控制显示器的显示设置;
  控制扬声器音量;
  获取 sensor;
  读 RTC;
  开启、关闭一些设备的电源供应;
  等等.

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

- ACPI

  ACPI 的主要目的是, 在 OS 运行时, 将硬件配置、电源管理、硬件状态监控等琐碎的底层
  硬件操作从 BIOS/UEFI firmware 转移至 OS. 这样, OS 在运行时, 无需调用 firmware
  runtime service, 可直接进行这些管理配置操作. 优点是更灵活, 更高效.

  为什么要将这些配置和管理驱动以 bytecode 形式存在 firmware 中, 而不是放在一般
  与操作系统一起的硬件驱动中? 原因是, 考虑到这些硬件配置和管理等操作实际上都是
  与具体主板密切相关的, 或者说这些操作该如何进行是直接由主板的硬件实现来决定的,
  所以由主板自己来提供一种不依赖于操作系统的管理方式 (即 bytecode), 才会比较统一.

  主板 firmware 中保存有 ACPI tables, 表中包含 ACPI Machine Language bytecode 程序.
  OS kernel 实现了 AML bytecode 的解释器. OS 运行时, 从 firmware 里读取 ACPI tables
  至内存, 执行所需的 AML bytecode 来对相应硬件进行管理.

  注意, 在 OS 运行时, ACPI 接管对全部设备的配置和电源管理, 任何需要对设备进行这些
  操作的上层驱动都需要调用 ACPI 来进行.

  ACPICA 是 OS 部分的 ACPI specs 的 reference implementation, Linux 使用的就是这个.

  ACPI power states (G: global state, S: sleep state)

  * G0, S0: working: computer is running, CPU executes instructions.

  * G1: sleeping

    - S1: power on suspend: power to CPU and RAM is maintained,
      CPU stops executing instructions. Other devices may be off.

    - S2: CPU off, RAM powered. 大致上可看作 S1, S3 的中间态, 类似于 S3, 没有实际实现.

    - S3: suspend to RAM (sleep): CPU off, RAM powered.

    - S4: suspend to disk (hiberation): RAM saved to disk, system powered down.

  * G2, S5: soft off: system powered down, no state saved. PSU 开启,
    保持主板或至少电源按钮通电, 从而可以返回 S0.

  * G3: mechanical off: PSU 关闭, 主板断电, 此时可以拆机.

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

- Wake-on-LAN 要求处于 power-off 状态的机器的网卡并没有完全断电, 而是处于低功耗的监听模式,
  能够接收 link-layer frame, 解析并识别 magic packet 里面的 MAC 地址与自己的一致, 然后
  通过某种方式向主板发送 wakeup 信号.

  跨网段发送 WOL packet, 可以使用 unicast IP 地址, 而不是 subnet broadcast
  (255.255.255.255), 这样 unicast 送到目的机器的 NIC. 但由于 ARP 表的过期时间,
  到达目的网段后无法网关无法转换成目的机器 MAC 地址, 从而失败. 所以, 在目的网段,
  需要一些其他配置, 来配合 WOL.

general
-------

- TDP. PC 各组件的重要功率指标. 它表示一个组件在正常的实际运行中的最大发热功率.
  它并不是该组件的理论发热功率上限, 后者在极限情况下才会达到, 并不符合实际情况.

  一个组件的实际使用功率上限会基本相同或略大于它的 TDP. 因此, 电源提供的功率应当
  至少大于各组件 TDP 之和, 比较理想的是 1.5 倍.


firmware
--------

- 主板的 BIOS 软件存在 flash memory 上 (NOR or NAND), 由于是 flash memory, 可以重写
  以升级 BIOS.

  主板的设置保存在 CMOS 存储上. CMOS 是 volatile 的, 需要通电以维持数据. 它的电力
  由主板上的电池提供. 所以把主板电池扣下来或者采用特定的 CMOS 短路机制可以重置
  主板设置. (重置 CMOS 应该能够重置主板密码吧?)

- 主板上的电池用于维持 CMOS 数据以及维持 Real Time Clock (RTC).

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
  在运行时, bootloader 使用 BIOS/UEFI firmware 来访问存储设备等, OS 使用 firmware
  来进行某些硬件控制.

- firmware 和 OS 各需要一套 driver, 以访问硬件. 显然 firmware 这套驱动要基础很多,
  只包含很基础的功能.

- 如今几乎所有的 PC/server 等类型的计算机的主板都使用的是遵循 UEFI 标准的固件.
  Linux/Windows/macOS 等都是 UEFI-aware 的, 意思是它们的 bootloader 能够在 bootup
  过程中调用 UEFI boot service 去访问硬件 (在 OS kernel 加载之前), 并且在 OS kernel
  运行过程中, 可以调用 UEFI runtime service 去进行某些硬件操作 (比如 RTC, fans,
  suspend-to-RAM, 等).

  OS kernel 尽量通过自己的 driver 直接访问几乎所有硬件, 原因是:

  * kernel driver 可以灵活地使用设备的全部功能和发挥其性能;

  * 通过 UEFI/BIOS 转发会低效一些;

  * BIOS 运行在 real mode, 在 kernel 和 BIOS 之间切换需要切换 CPU 的模式 3 遍
    (triple fault) 很低效.

  但仍有极少量硬件操作需要依赖 UEFI/BIOS, 比如 suspend-to-RAM.
  基本上在 OS 常态运行期间, kernel 已经不再需要 BIOS/UEFI 提供的 runtime service,
  从而不需要控制权转换或 CPU 模式转换, 而是自己直接访问硬件.

- BIOS 运行时 CPU 处于 16-bit real mode, 读取 MBR、加载 bootloader 和 bootloader
  的初始执行, 都是在 16-bit real mode 下.
  bootloader (e.g., GRUB) 的任务之一就是切换 CPU 到 protected mode.

  对于 UEFI 系统, UEFI 开始执行后很快就切换到 protected mode. 而 ESP 分区上的所有
  EFI applications 都是在 protected mode 中执行的. 注意到这些 ``.efi`` 应用都是
  PE32 executable, 使用的虚拟内存.

  因此, BIOS 系统中的 grub 与 UEFI 系统中的 grub 应该是不同的.

- UEFI 的设计要求易于扩展, 功能丰富、灵活. 这些自然要求 UEFI firmware 是运行在
  protected mode 或 long mode 中的, 并且具有模块化的设计 (EFI applications).

  UEFI 相对于 BIOS firmware 的一些优点:

  * 支持 GPT, 向后兼容 MBR.

  * 模块化设计 (EFI application).

  * 运行于 protected/long mode, 而不是 real mode. 能够实现复杂的 EFI application,
    从而可以构建灵活的 pre-OS environment.

- 由于 x86 CPU 启动时运行在 real mode, 要求 BIOS 软件在这个模式下运行, 而且 BIOS 由于
  历史原因, 一直只在 real mode 中运行, 因此很不灵活, 且直接依赖于 x86 CPU real mode.
  与之对应, UEFI 在启动后迅速切换 CPU 至自己所需的 mode, 比如 protected mode, long mode.
  因此 UEFI 是 CPU-independent 的架构.

- UEFI-MBR 或 UEFI-GPT 组合在分区时要有 ESP 分区, 放置 EFI application,
  包含 bootloaders (比如 grub), UEFI shell 等. ESP 分区的文件系统是 UEFI 规定的 FAT fs,
  这样 UEFI 才有能力去访问.

  注意 UEFI 不是说一定要和 GPT 分区方式配合.

- 几种 bootup 组合方式:

  * BIOS-MBR

    BIOS (或者 UEFI 在 CSM 模式下) 读取 MBR 分区表 LBA0, 执行 bootstrap code,
    后者加载 bootloader.

  * BIOS-GPT

    GPT 的 LBA0 是 protective MBR, 可以设置在安装 bootloader 时, 与 MBR 相同, 将
    bootstrap code 写入 protective MBR. 这样 BIOS 可以和平时一样, 不去管分区表,
    直接读 LBA0 来加载 bootloader. 由于 BIOS 不认识 GPT 分区表, 此后 bootloader
    需靠自己访问硬盘.

  * UEFI-MBR

    UEFI 从 MBR 中找到 ESP 分区, 访问 ESP 分区加载 bootloader.

  * UEFI-GPT

    UEFI 从 GPT 中找到 ESP 分区 (根据 GPT 规定的 partition type GUID),
    访问 ESP 分区加载 bootloader.

- UEFI boot manager 存储有多个 entry, 每条是一个 boot config, 对应加载一个 ESP 中的
  application. 这与 BIOS 不同, 对于 BIOS 系统, 启动顺序列表中只有不同的设备, 选定
  设备后如何启动是预设的机制.

- grub 的 EFI application 是 ``grubx64.efi``. 若开启了 secure boot, 需执行 ``shim.efi``,
  后者通过 UEFI 认证后再加载 ``grubx64.efi``.

- Option ROM. BIOS 和 UEFI 都有 option ROM 概念, 即 peripherals 可以提供固件,
  作为 firmware plugin 在启动时加载. 例子: 所有显卡都有 Option ROM 用于在启动
  期间控制视频信号输出, 在 POST 期间它就被主板固件加载, 否则 POST 之后屏幕不会
  点亮.

- reset button 如何工作的:

  按了 reset button 之后, 主板给所有设备发送 reset signal.
  由于 CPU 被 reset, 所以从固定的 reset vector 地址处开始执行. 对于 cold
  boot, northbridge (uncore) 把这个地址请求转发到 firmware flash memory 上;
  对于 soft boot, BIOS 已经在内存中了, 所以该地址请求直接转发到内存中的对应
  地址上. 总之, CPU 从 reset vector 处开始执行, 即开始执行 BIOS, 从而开始了
  boot sequence. BIOS 在 soft boot 时, 会跳过 POST 过程.

processor
---------

- CISC and RISC design

  * CISC 和 RISC 的区别在于指令集中是否包含 complex instruction, 这种指令即进行运算
    (arithmetics) 又进行内存的读写 (memory load/store). 而不在于谁的指令数量、种类多.

  * 典型的 CISC 是 x86 架构; 典型的 RISC 是 ARM 架构. 前者主导 PC 和 server 市场;
    后者主导移动端和嵌入式 (IoT) 市场. 比较典型的 RISC PC/server 是 SPARC 架构.

- x86 architecture

  * Byte-addressing is possible and words are stored in memory with little-endian
    byte order. Unaligned memory access is allowed for all valid word sizes.

  * 第一代 x86 CPU 是 intel 8086.

  * 当代的 x86 CPU 支持 16bit (real mode), 32bit (protected mode), 64bit (long mode)
    三类运行模式. 8086 是第一代 16bit, 80386 是第一代 32bit, AMD Opteron 是第一代
    64bit.

  * The term "x86" came into being because the names of several successors to
    Intel's 8086 processor end in "86", including the 80186, 80286, 80386 and
    80486 processors.

  * intel x86 架构要求完全向后兼容至 8086, 因此所有 x86 架构的 CPU 刚启动时都处于
    16-bit real mode, 只能访问 2**20 即 1MiB 内存. Real mode 是 8086 和 80186 的运行模式.

  * x86 cpu 支持那么多 extensions (see lscpu output), 其实有很多都是为了向后兼容而保留
    的. 平时运行时, 那么多并不能全用上.

  * processor modes.

    - real mode.

      20bit (1MiB) segmented memory address space. No memory protection,
      unlimited software access to all addressable memory, I/O memory, peripheral
      hardware. No multitasking. No code privilege levels. 考虑到 UEFI 的普及, 如今
      real mode 除了启动 CPU 的一瞬间之外, 已经不再使用. 除了还在使用 BIOS 的机器.

    - protected mode.

      虚拟内存, paging, safe multitasking, privilege levels (ring).
      首先在 80286 上出现. 80386 及之后的 cpu 支持从 protected mode 回到 real mode.

      80286 及以后支持 16-bit protected mode, 80386 及以后支持 32-bit protected mode.

    - virtual 8086 mode. 模拟 8086 processor, 在受保护环境下运行 real mode program.
      或者说, 在 protected mode OS 中运行 real mode program.

    - system management mode. all normal execution, including the operating
      system, is suspended. A special separate software, which is usually part
      of the firmware or a hardware-assisted debugger, is then executed with
      high privileges.

    - long mode. 64-bit programs are run in a sub-mode called 64-bit mode,
      while 32-bit programs and 16-bit protected mode programs are executed in
      a sub-mode called compatibility mode. Real mode or virtual 8086 mode
      programs cannot be natively run in long mode.

  * x86 processor 支持 5 privilege levels (5 rings).
    ring 0 大致是 kernel, ring 3 是 user app.
    ring -1 是 hypervisor, 用于 x86 virtualization, 由 VT-x extension 提供.
    没必要使用所有的 rings, 事实上 Linux, Windows 只使用 0 和 3, 对应 kernel/user
    land.

- x86 architecture with 64bit extension

  * x86 with 64bit extension 的 intel CPU 支持运行在 long mode, 即访问 64-bit
    内存地址. 在 linux 下, 支持 x86-64 指令集的 CPU 具有 ``lm`` flag (即 long mode).

  * x86-64 架构支持 page table entry 包含 No-eXecute (NX) bit, 以区分可执行和不可执行的
    内存区域. NX bit 的 CPU flag 是 ``nx``.

  * x86-64 的一些重要好处:

    * It is faster under most circumstances

    * inherently more secure due to the nature of Address space layout randomization
      (ASLR) in combination with Position-independent code (PIC) and the NX Bit which
      is not available in the stock i686 kernel due to disabled PAE.

    * If your computer has more than 4GB of RAM, only a 64-bit OS will be able to fully
      utilize it.

- Unix, Linux, OS/2, Windows NT 3.x and later, 被认为是 modern OS 的重要原因就是
  它们在运行过程中 CPU 始终处于 protected mode, kernel 自己 (通过 driver) 访问硬件,
  而不再需要在 real/protected mode 之间切换以及 firmware 的介入.

memory
------

bus & IO
--------

- USB

  * 标准: 1.0, 1.1, 2.0, 3.0, 3.1.

  * 速度: Low Speed (1.0), Full Speed (1.1), High Speed (2.0), Super Speed (3.0),
          Super Speed+ (3.1).

  * 插头类型:

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

  * Host controller interface (HCI): HCI 是 usb 控制端硬件实现的控制接口, 它在
    即主板或 usb 扩展卡上实现, 用于控制 usb 硬件设备. 在操作系统中实现了 HCI 的驱动,
    即 Host Controller Driver (HCD). HCI 有以下几代:

    - Open Host Controller Interface (OHCI) 和 Universal Host Controller Interface (UHCI).
      For USB 1.0 low speed & USB 1.1 full speed (两者都支持这两种速度).
      Linux driver 是 ohci_hcd 和 uhci_hcd.

    - Enhanced Host Controller Interface (EHCI). For USB 2.0, high speed.
      Linux driver 是 ehci_hcd.

    - eXtensible Host Controller Interface (XHCI). 替代 OHCI/UHCI/EHCI,
      支持所有过去的 USB 标准, 新的 USB 3.0 SuperSpeed 和 3.1 SuperSpeed+,
      以及未来的标准.
      Linux driver 是 xhci_hcd.

- thunderbolt

  * 在一条 cable 中 multiplex PCIe, DisplayPort 等多种协议的信号, 并提供 DC power.
    thunderbolt cable 一端连接 host motherboard 上的 thunderbolt controller, 另一端
    连接 hub 上的 thunderbolt controller. 在 motherboard 上, thunderbolt controller
    连接 PCIe 和 DisplayPort 等等总线; 在 hub 上, 连接 PCIe 和 DP 等设备.

  * Connector. thunderbolt 1/2: MiniDP, thunderbolt 3: USB type-C.

  * bus protocols: PCIe, DisplayPort, HDMI, USB.

  * speed:
    thunderbolt 1: two channels, 10Gb/s each.
    thunderbolt 2: 20Gb/s.
    thunderbolt 3: 40Gb/s.

    At the physical level, the bandwidth of Thunderbolt 1 and Thunderbolt 2 are
    identical, and Thunderbolt 1 cabling is thus compatible with Thunderbolt 2
    interfaces. At the logical level, Thunderbolt 2 enables channel
    aggregation, whereby the two previously separate 10 Gbit/s channels can be
    combined into a single logical 20 Gbit/s channel.

  * 连接方式: hub or daisy chain.

  * thunderbolt 是基于 MiniDP 的, 是后者的继承.

  * DMA attack vulnerability. 由于 thunberbolt 把系统 PCIe bus 外接出来, 可直接
    插入外置的 PCIe 设备连接主板. 因此设备可以从硬件层直接发起 DMA, 访问内存.
    这需要靠正确配置的 IOMMU 来防范.

- memory-mapped IO vs port-mapped IO

  port-mapped IO 是出现得比较早的, 因为在早期, 访问内存和设备 IO 这两件事比较适合
  分开处理, 那时 cpu 的地址寄存器比较小, 只够存物理内存地址的长度, 不能再多出来
  几个 bits 构成包含设备地址的 extended address space.

  对于基于 port-mapped IO 的系统, 有 memory address space 和 IO address space
  两种. 前者就是 RAM 访问, 后者是 peripheral device 访问. 在 IO address space
  中, 一个设备使用的地址范围中, 第一个地址被称为 IO port 或 IO base address.
  由于 CPU 对内存和设备的读写是不同的, 对设备进行 IO 需要使用 (不同于内存的)
  专门设计的指令. 因此使用 port-mapped IO 的 CPU, 需要实现更复杂的逻辑,
  带来了更多的麻烦.

  对于基于 memory-mapped IO 的系统, 只有 memory address space, 但其中的一部分是
  分配给 RAM, 其他部分按需分配给各个 peripheral device. 由于 CPU 对内存和设备
  的读写使用通用的指令, 这样的 CPU 逻辑相对简单一些, 更易于编程, 运行更快.

  PMIO 实现方式: IO address space, CPU IO 指令, CPU IO pin, IO bus.
  MMIO 实现方式: memory address space, CPU 内存指令, address code decoder.

  peripheral device 进行 IO 的流程:
  1. driver 通过 MMIO/PMIO 方式向设备的寄存器写入 DMA 相关信息
     (要读写的 DMA 地址和读写长度等);
  2. driver 启动设备 DMA;
  3. 设备通过 IOMMU 进行 DMA, 完成 IO 过程;
  4. 设备向 CPU 发送 interrupt, 告知 IO 已经完成;
  5. kernel 的 interrupt handler 中, driver 进行清理工作, 包括清理 DMA mapping,
     清理数据 buffer, etc.

  x86 架构的系统, 两种 IO 都有使用. 且应该主要是在使用 MMIO.
  在 linux 中, MMIO 映射可以通过 ``/proc/iomem`` 找到, 尤其是对于 PCIe 设备,
  还可以通过 ``lspci -vvv`` 看到; PMIO 映射可以通过 ``/proc/ioports`` 找到.

  在 OS 中, usersapce 应用一般不能直接访问映射的内存地址或 IO 地址. 这些只有
  device driver 能直接访问.

connector
~~~~~~~~~
- COM. 一种 IBM PC Compatible 上面的古老的串口接口. 现在 PC 上已经没有了, 部分旧
  PC 上仍保留一个 COM header, 用于接入.

Video
-----

- HSA 架构是在 CPU 和 GPU 之间共享 RAM 和 Graphics RAM 以及统一的任务调度队列.
  将 GPU/GRAM 提升到和 CPU/RAM 同样的地位, 并做抽象层统一, 对外作为一个整体
  提供 API. 这样做的好处时, 简化涉及 GPU/GRAM 的任务处理逻辑, 尤其是避免数据
  复制以及简化任务调度.

  HSA 在 SOC (即移动端) 上用的很多.

video card
~~~~~~~~~~
- A modern video card is also a computer unto itself.

- 主要供应商: AMD, Nvidia

- integrated graphics

  * CPU 上的集成显卡又称为 Accelerated Processing Unit (APU).

  * 集成显卡一般可以在 firmware 中禁用, 而选择使用独立显卡.

  * 集成显卡的缺点:

    - 与 CPU 共用计算资源, cooling system 等;

    - 占用一部分 RAM 作为显存;

    - GPU 图形运算需要大量的内存读写, 集成显卡需要和 CPU 竞争 RAM 读写, 而
      且 main RAM 本来就很慢 (相对于 GRAM).

- 现在显卡的 TDP 一般很高, 远高于 PCIe 能提供的功率, 需要额外从 PSU 直接供电.

- AMD CrossFireX 和 Nvidia SLI 提供多显卡并联运行. 这些显卡一般需要是相同的型号.

- framebuffer 在 Graphics RAM 中. 它包含一帧图像输出所需的完整数据, 即一个 bitmap.
  The information in the buffer typically consists of color values for every
  pixel to be shown on the display. The total amount of memory required for the
  framebuffer depends on the resolution of the output signal, and on the color
  depth or palette size.

- Video firmware 与主板 firmware 功能类似, 用于初始化配置显卡. 它被主板固件在
  启动的极早期 (POST 期间或之后) 调用, 以配置显卡并激活图像输出.

  It may contain information on the memory timing, operating speeds and
  voltages of the graphics processor, RAM, and other details which can
  sometimes be changed.

  The modern Video BIOS does not support all the functions of the video card,
  being only sufficient to identify and initialize the card to display one of a
  few frame buffer or text display modes. 完整的显卡功能和配置要靠 OS 下的
  显卡驱动去运行.

- 显存相对于主内存而言, 是非常高速的. GDDR5, GDDR5X 之类的都有几百 GB/s 速度.

GPU
~~~

- Graphics acceleration. 不使用 CPU 运算将图形点阵化再传给显卡输出, 而是将
  原始的 graphics drawing commands 直接传给 GPU, 后者负责点阵化构建 framebuffer.
  节省大量 CPU 时间, 并提高输出效率.

  While early accelerators focused on improving the performance of 2D GUI
  systems, most modern accelerators focus on producing 3D imagery in real time.
  A common design is to send commands to the graphics accelerator using a
  library such as OpenGL or Direct3D. The graphics driver then translates those
  commands to instructions for the accelerator's graphics processing unit
  (GPU). The GPU uses those microinstructions to compute the rasterized
  results. Those results are bit blitted to the framebuffer. The framebuffer's
  signal is then produced in combination with built-in video overlay devices
  (usually used to produce the mouse cursor without modifying the framebuffer's
  data) and any analog special effects that are produced by modifying the
  output signal. An example of such analog modification was the spatial
  anti-aliasing technique used by the 3dfx Voodoo cards. These cards add a
  slight blur to output signal that makes aliasing of the rasterized graphics
  much less obvious.

- 当代 GPU 完全为 3D 加速渲染设计和优化, 2D 渲染需要通过 3D 渲染来模拟.

- GPU accelerated video decoding. 当代 GPU 支持 MPEG primitives 等视频处理
  功能. 可以将部分视频解码和处理工作从 CPU 移至 GPU.

- GPGPU: GPU 本来是专门为 3D/2D 图形输出优化的, 而这些运算中一般涉及大量的矢量
  和矩阵运算, 也就是说 GPU 实际上很适合用于做科学计算和并行计算.

  使用 GPU 训练神经网络的效率可以达到 CPU 的 250 倍.

OpenGL
~~~~~~

- OpenGL is a cross-language, cross-platform API standard for hardware
  accelerated 2D/3D graphics rendering.

  user space 程序调用 API 进行图像操作; API 可能直接由显卡驱动提供, 也可能是由
  什么中间件提供, 后者再调用显卡驱动.

- 由于 OpenGL 定义了一系列 GPU 硬件必须支持的功能的通用 API, 所以它需要显卡
  硬件去实现这些功能. 因此一款特定的显卡最高支持的 OpenGL 版本是固定的.

- API implementations for different platforms.
  WebGL (javascript), Windows WGL, X window system GLX (C),
  OSX CGL, iOS components (C), Android components (C, Java)

- GPU vendors 可在 OpenGL core API 之外提供 customized extensions.
  All extensions are collected in, and defined by, the OpenGL Registry.

  The features introduced by each new version of OpenGL are typically formed
  from the combined features of several widely implemented extensions,
  especially extensions of type ARB or EXT.

- official docs.
  The Red Book --- OpenGL Programming Guide.
  The Orange Book --- OpenGL Shading Language.

OpenCL
~~~~~~

- OpenCL 是为了能够在 HSA 架构平台中各组件上运行程序所创造的编程语言.

bus & connector
~~~~~~~~~~~~~~~

- DisplayPort.
  
  * 数据传输使用 packet 机制, 类似于 ethernet 或 PCIe.

  * 可同时传输视频和音频信号或传输其中任一. 还可以传输 USB 协议信号.

  * DP is free to implement.

- HDMI.

  * bckward compatible with single-link DVI.

- DP vs HDMI

  * 大部分功能相同.

  * HDMI 收费, DP 理论上免费.

  * DP 1.4 throughput (32.4Gib/s) 高于 HDMI 2.0b (14.4Gib/s).
