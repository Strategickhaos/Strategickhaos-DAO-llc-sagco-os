/* SAGCO LIVE Linker Script
 * Defines memory layout for the kernel
 */

/* Entry point for the kernel */
ENTRY(_start)

SECTIONS
{
    /* Kernel starts at 1MB in physical memory */
    . = 1M;

    /* Multiboot header must be first */
    .multiboot ALIGN(4K) : {
        *(.multiboot)
    }

    /* Read-only data (text segment) */
    .text ALIGN(4K) : {
        *(.text)
    }

    /* Read-only data */
    .rodata ALIGN(4K) : {
        *(.rodata)
    }

    /* Read-write data (initialized) */
    .data ALIGN(4K) : {
        *(.data)
    }

    /* Read-write data (uninitialized) and stack */
    .bss ALIGN(4K) : {
        *(COMMON)
        *(.bss)
    }
}
