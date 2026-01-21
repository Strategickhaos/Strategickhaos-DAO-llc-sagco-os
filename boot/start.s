/* SAGCO LIVE - Multiboot Entry Point
 * This assembly code is the first code executed by the bootloader
 */

.set ALIGN,    1<<0             /* align loaded modules on page boundaries */
.set MEMINFO,  1<<1             /* provide memory map */
.set FLAGS,    ALIGN | MEMINFO  /* multiboot flags */
.set MAGIC,    0x1BADB002       /* magic number for multiboot */
.set CHECKSUM, -(MAGIC + FLAGS) /* checksum of above */

/* Multiboot header */
.section .multiboot
.align 4
.long MAGIC
.long FLAGS
.long CHECKSUM

/* Set up the stack */
.section .bss
.align 16
stack_bottom:
.skip 16384 # 16 KB stack
stack_top:

/* Entry point */
.section .text
.global _start
.type _start, @function
_start:
    /* Set up stack pointer */
    mov $stack_top, %esp

    /* Call the kernel main function */
    call kernel_main

    /* Hang if kernel_main returns */
    cli
1:  hlt
    jmp 1b

/* Set the size of the _start symbol */
.size _start, . - _start
