/*
 * ═══════════════════════════════════════════════════════════════════════════════
 * SAGCO LIVE BOOT ASSEMBLY v0.1.0
 * Strategickhaos DAO LLC - Ratio Ex Nihilo
 * 
 * Multiboot-compliant boot code for x86
 * Sets up stack and calls kernel_main()
 * 
 * January 2026
 * ═══════════════════════════════════════════════════════════════════════════════
 */

/* Multiboot header constants */
.set ALIGN,    1<<0                 /* align loaded modules on page boundaries */
.set MEMINFO,  1<<1                 /* provide memory map */
.set FLAGS,    ALIGN | MEMINFO      /* this is the Multiboot 'flag' field */
.set MAGIC,    0x1BADB002           /* 'magic number' lets bootloader find the header */
.set CHECKSUM, -(MAGIC + FLAGS)     /* checksum of above, to prove we are multiboot */

/*
 * Multiboot header - must be in first 8KB of kernel image
 */
.section .multiboot
.align 4
.long MAGIC
.long FLAGS
.long CHECKSUM

/*
 * Stack allocation (16KB)
 */
.section .bss
.align 16
stack_bottom:
.skip 16384  # 16 KiB
stack_top:

/*
 * Entry point
 */
.section .text
.global _start
.type _start, @function
_start:
    /* Set up the stack */
    mov $stack_top, %esp

    /* Call the kernel main function */
    call kernel_main

    /* Infinite loop if kernel_main returns */
    cli
1:  hlt
    jmp 1b

/*
 * Set the size of the _start symbol to the current location '.' minus its start.
 * This is useful when debugging or when you implement call tracing.
 */
.size _start, . - _start
