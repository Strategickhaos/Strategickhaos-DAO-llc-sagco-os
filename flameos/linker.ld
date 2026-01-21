/* linker.ld - Linker script for SAGCO LIVE kernel */

ENTRY(_start)

SECTIONS
{
    . = 1M;

    .boot :
    {
        *(.multiboot)
    }

    .text :
    {
        *(.text)
    }

    .rodata :
    {
        *(.rodata)
    }

    .data :
    {
        *(.data)
    }

    .bss :
    {
        *(.bss)
    }
}
