# start.s - Multiboot assembly entry point for SAGCO LIVE
# 32-bit x86 assembly

.set ALIGN,    1<<0
.set MEMINFO,  1<<1
.set FLAGS,    ALIGN | MEMINFO
.set MAGIC,    0x1BADB002
.set CHECKSUM, -(MAGIC + FLAGS)

.section .multiboot
.align 4
.long MAGIC
.long FLAGS
.long CHECKSUM

.section .bss
.align 16
stack_bottom:
.skip 16384  # 16 KB stack
stack_top:

.section .text
.global _start
.type _start, @function

_start:
    # Set up the stack
    mov $stack_top, %esp

    # Call the kernel main function
    call kernel_main

    # If kernel_main returns, halt the CPU
    cli
1:  hlt
    jmp 1b

.size _start, . - _start
