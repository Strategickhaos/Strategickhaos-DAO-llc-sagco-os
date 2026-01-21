/*
 * ═══════════════════════════════════════════════════════════════════════════════
 * SAGCO LIVE LINKER SCRIPT v0.1.0
 * Strategickhaos DAO LLC - Ratio Ex Nihilo
 * 
 * Defines memory layout for the kernel
 * Entry point at 1MB (standard for multiboot kernels)
 * 
 * January 2026
 * ═══════════════════════════════════════════════════════════════════════════════
 */

/* The bootloader will load us at 1MB physical */
ENTRY(_start)

SECTIONS
{
    /* Begin putting sections at 1 MiB, a conventional place for kernels to be loaded */
    . = 1M;

    /* First put the multiboot header, as it must be in the first 8 KiB of the kernel file */
    .text BLOCK(4K) : ALIGN(4K)
    {
        *(.multiboot)
        *(.text)
    }

    /* Read-only data */
    .rodata BLOCK(4K) : ALIGN(4K)
    {
        *(.rodata)
    }

    /* Read-write data (initialized) */
    .data BLOCK(4K) : ALIGN(4K)
    {
        *(.data)
    }

    /* Read-write data (uninitialized) and stack */
    .bss BLOCK(4K) : ALIGN(4K)
    {
        *(COMMON)
        *(.bss)
    }

    /* The compiler may produce other sections, by default it will put them in a segment
       with the same name. Simply add stuff here as needed. */
}
