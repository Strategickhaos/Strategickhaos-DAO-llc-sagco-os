/* SAGCO LIVE v0.1.0 - Sovereign AI-Governed Compute Organism
 * Owner: Strategickhaos DAO LLC
 * Motto: Ratio Ex Nihilo
 * 
 * A minimal 32-bit x86 kernel bootable via GRUB
 */

#include <stdint.h>
#include <stddef.h>

/* VGA text mode buffer */
#define VGA_MEMORY 0xB8000
#define VGA_WIDTH 80
#define VGA_HEIGHT 25

/* VGA color codes */
enum vga_color {
    VGA_BLACK = 0,
    VGA_BLUE = 1,
    VGA_GREEN = 2,
    VGA_CYAN = 3,
    VGA_RED = 4,
    VGA_MAGENTA = 5,
    VGA_BROWN = 6,
    VGA_LIGHT_GREY = 7,
    VGA_DARK_GREY = 8,
    VGA_LIGHT_BLUE = 9,
    VGA_LIGHT_GREEN = 10,
    VGA_LIGHT_CYAN = 11,
    VGA_LIGHT_RED = 12,
    VGA_LIGHT_MAGENTA = 13,
    VGA_YELLOW = 14,
    VGA_WHITE = 15,
};

static inline uint8_t vga_entry_color(enum vga_color fg, enum vga_color bg) {
    return fg | bg << 4;
}

static inline uint16_t vga_entry(unsigned char uc, uint8_t color) {
    return (uint16_t) uc | (uint16_t) color << 8;
}

size_t strlen(const char* str) {
    size_t len = 0;
    while (str[len])
        len++;
    return len;
}

/* Terminal state */
static size_t terminal_row;
static size_t terminal_column;
static uint8_t terminal_color;
static uint16_t* terminal_buffer;

void terminal_initialize(void) {
    terminal_row = 0;
    terminal_column = 0;
    terminal_color = vga_entry_color(VGA_LIGHT_CYAN, VGA_BLACK);
    terminal_buffer = (uint16_t*) VGA_MEMORY;
    for (size_t y = 0; y < VGA_HEIGHT; y++) {
        for (size_t x = 0; x < VGA_WIDTH; x++) {
            const size_t index = y * VGA_WIDTH + x;
            terminal_buffer[index] = vga_entry(' ', terminal_color);
        }
    }
}

void terminal_setcolor(uint8_t color) {
    terminal_color = color;
}

void terminal_putentryat(char c, uint8_t color, size_t x, size_t y) {
    const size_t index = y * VGA_WIDTH + x;
    terminal_buffer[index] = vga_entry(c, color);
}

void terminal_putchar(char c) {
    if (c == '\n') {
        terminal_column = 0;
        if (++terminal_row == VGA_HEIGHT)
            terminal_row = 0;
        return;
    }
    terminal_putentryat(c, terminal_color, terminal_column, terminal_row);
    if (++terminal_column == VGA_WIDTH) {
        terminal_column = 0;
        if (++terminal_row == VGA_HEIGHT)
            terminal_row = 0;
    }
}

void terminal_write(const char* data, size_t size) {
    for (size_t i = 0; i < size; i++)
        terminal_putchar(data[i]);
}

void terminal_writestring(const char* data) {
    terminal_write(data, strlen(data));
}

void terminal_writeline(const char* data) {
    terminal_writestring(data);
    terminal_putchar('\n');
}

void print_header(void) {
    terminal_setcolor(vga_entry_color(VGA_YELLOW, VGA_BLACK));
    terminal_writeline("===============================================================================");
    terminal_setcolor(vga_entry_color(VGA_LIGHT_CYAN, VGA_BLACK));
    terminal_writeline("                           SAGCO LIVE v0.1.0");
    terminal_writeline("              Sovereign AI-Governed Compute Organism");
    terminal_setcolor(vga_entry_color(VGA_YELLOW, VGA_BLACK));
    terminal_writeline("===============================================================================");
    terminal_putchar('\n');
}

void print_info(void) {
    terminal_setcolor(vga_entry_color(VGA_WHITE, VGA_BLACK));
    terminal_writeline("  Status: KERNEL BOOTED");
    terminal_writeline("  Owner:  Strategickhaos DAO LLC");
    terminal_writeline("  Motto:  Ratio Ex Nihilo");
    terminal_putchar('\n');
}

void print_status(void) {
    terminal_setcolor(vga_entry_color(VGA_LIGHT_GREEN, VGA_BLACK));
    terminal_writeline("  [*] VGA initialized");
    terminal_writeline("  [*] Interrupts disabled");
    terminal_writeline("  [*] Awaiting FlameLang integration...");
    terminal_putchar('\n');
}

void print_footer(void) {
    terminal_setcolor(vga_entry_color(VGA_YELLOW, VGA_BLACK));
    terminal_writeline("===============================================================================");
    terminal_setcolor(vga_entry_color(VGA_LIGHT_MAGENTA, VGA_BLACK));
    terminal_writeline("  Legion of Minds: Claude + GPT + Grok = Convergence");
    terminal_setcolor(vga_entry_color(VGA_YELLOW, VGA_BLACK));
    terminal_writeline("===============================================================================");
}

/* Kernel entry point */
void kernel_main(void) {
    /* Initialize terminal interface */
    terminal_initialize();
    
    /* Display SAGCO branding */
    print_header();
    print_info();
    print_status();
    print_footer();
    
    /* Halt the CPU - kernel is complete */
    while(1) {
        __asm__ volatile ("hlt");
    }
}
