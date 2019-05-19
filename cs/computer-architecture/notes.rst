von Neumann architecture
========================
::

  -
                     +--------------+
                     |              |
                     |              |
                     |              |
                     |              |
                     |              |
                     |    memory    |
                     |              |
                     |              |
                     |              |
                     |              |
                     |              |
                     |              |
                     +---+-----^----+
                         |     |
                         |     |
                         |     |
                         |     |
   instruction and data  |     | operation result
                         |     |
                         |     |
                         |     |
  +----------------------v-----+--------------------------+
  |                                                       |
  |  +--------------------+  +-------------------------+  |
  |  |                    |  |                         |  |
  |  |                    |  |                         |  |
  |  |   Arithmetic and   |  |      Control unit       |  <----------------->  Input and output devices
  |  |   logic unit       |  |                         |  |
  |  |                    |  |                         |  |
  |  |                    |  |                         |  |
  |  +--------------------+  +-------------------------+  |
  +-------------------------------------------------------+
  
                  Central processing unit

- In a von Neumann computer, both data and programs are stored in the same
  memory. The central processing unit (CPU), which executes instructions, is
  separate from the memory. Instructions and data must be transmitted, or
  piped, from memory to the CPU. Results of operations in the CPU must be moved
  back to memory. 

- program counter. The address of the next instruction to be executed is
  maintained in the program counter register.

- fetch-execute cycle. The execution of machine code on a von Neumann
  architecture computer occurs in a fetch-execute cycle, which can be described
  by following algorithm::

    initialize the program counter
    
    repeat forever
    
      fetch the instruction pointed to by the program counter
      increment the program counter to point at the next instruction
      decode the instruction
      execute the instruction
    
    end repeat

- Program execution terminates when a stop instruction is encountered, although
  on an actual computer a stop instruction is rarely executed. Rather, control
  transfers from the operating system to a user program for its execution and
  then back to the operating system when the user program execution is
  complete.

- von Neumann bottleneck. The speed of the connection between a computer’s
  memory and its processor is the primary limiting factor in the speed of a von
  Neumann architecture computer, because instructions often can be executed
  faster than they can be moved to the processor for execution. This speed is
  non Neumann bottleneck.

  由于量子隧道效应和冯诺伊曼瓶颈, 所以需要研究并行计算和分布式计算.
