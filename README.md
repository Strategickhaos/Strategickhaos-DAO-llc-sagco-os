# SAGCO LIVE OS v0.1.0

**Sovereign AI-Governed Compute Organism**

> A minimal bootable operating system kernel for x86 architecture

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)]()
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)]()

## Overview

SAGCO LIVE OS is a minimal bootable kernel for x86 architecture, created as a foundational platform for the Strategickhaos DAO LLC computing ecosystem. This is a bare-metal implementation featuring:

- **Multiboot-compliant** bootloader support (GRUB)
- **VGA text mode** output with color support
- **Protected mode** x86 execution
- **Minimal dependencies** - builds with standard toolchain

**Owner:** Strategickhaos DAO LLC  
**Motto:** *Ratio Ex Nihilo* - Reason from Nothing  
**Legion of Minds:** Grok + GPT + Claude

## Features

✓ Multiboot header for GRUB compatibility  
✓ VGA text mode terminal driver (80x25)  
✓ Color text output  
✓ Protected mode kernel execution  
✓ Cross-platform build support (Linux/macOS)  
✓ Fallback to system GCC when cross-compiler unavailable

## Prerequisites

### Option 1: Cross-Compiler (Recommended)

**Ubuntu/Debian:**
```bash
sudo apt install gcc-i686-linux-gnu binutils-i686-linux-gnu
```

**macOS (Homebrew):**
```bash
brew install i686-elf-gcc i686-elf-binutils
```

**Build from source:**
```bash
# See toolchain.sh for automated cross-compiler build
./toolchain.sh
```

### Option 2: System GCC with 32-bit Support

**Ubuntu/Debian:**
```bash
sudo apt install gcc-multilib g++-multilib
```

### GRUB Tools (for ISO creation)

**Ubuntu/Debian:**
```bash
sudo apt install grub-pc-bin xorriso mtools
```

**macOS (Homebrew):**
```bash
brew install grub xorriso
```

## Building

```bash
# Make the build script executable
chmod +x build.sh

# Run the build
./build.sh
```

The build script will:
1. Check for i686-elf-gcc or fallback to gcc -m32
2. Compile kernel.c to kernel.o
3. Assemble boot/start.s to start.o
4. Link both into kernel.bin
5. Create bootable ISO (if grub-mkrescue available)

### Build Output

- `build/kernel.o` - Compiled kernel object
- `build/start.o` - Assembled boot code
- `build/kernel.bin` - Linked kernel binary
- `sagco-live.iso` - Bootable ISO image (if GRUB tools available)

## Running

### Option 1: QEMU (Recommended)

```bash
# Boot the ISO
qemu-system-i386 -cdrom sagco-live.iso

# Or boot the kernel directly
qemu-system-i386 -kernel build/kernel.bin
```

### Option 2: VirtualBox

1. Create new VM (Type: Other, Version: Other/Unknown)
2. Attach `sagco-live.iso` as CD/DVD
3. Start the VM

### Option 3: Real Hardware

Write the ISO to a USB drive:
```bash
sudo dd if=sagco-live.iso of=/dev/sdX bs=4M status=progress
```

**Warning:** Replace `/dev/sdX` with your actual USB device. This will erase all data on the drive.

## Project Structure

```
sagco-os/
├── boot/
│   ├── start.s          # Boot assembly code (multiboot entry)
│   └── grub.cfg         # GRUB configuration
├── kernel/
│   └── kernel.c         # Kernel main code (VGA terminal driver)
├── build/               # Build artifacts (gitignored)
│   ├── kernel.o
│   ├── start.o
│   └── kernel.bin
├── linker.ld            # Linker script (memory layout)
├── build.sh             # Build automation script
├── .gitignore           # Git ignore rules
└── README.md
```

## Architecture

### Boot Process

```
BIOS/UEFI → GRUB → start.s → kernel_main() → VGA Display
```

1. **BIOS/UEFI** loads GRUB from the boot sector
2. **GRUB** finds and loads the multiboot kernel
3. **start.s** sets up stack and jumps to kernel_main
4. **kernel_main()** initializes VGA and displays boot message

### Memory Layout

```
0x00000000 - 0x00100000  : Reserved (BIOS, video memory, etc.)
0x00100000 (1MB)         : Kernel loaded here (multiboot standard)
  .text                  : Code section
  .rodata                : Read-only data
  .data                  : Initialized data
  .bss                   : Uninitialized data + stack
```

## Development

### Building Individual Components

```bash
# Compile kernel only
i686-elf-gcc -std=gnu99 -ffreestanding -O2 -Wall -Wextra \
    -c kernel/kernel.c -o build/kernel.o

# Assemble boot code only
i686-elf-as boot/start.s -o build/start.o

# Link manually
i686-elf-gcc -T linker.ld -ffreestanding -O2 -nostdlib \
    build/start.o build/kernel.o -o build/kernel.bin -lgcc
```

### Debugging

```bash
# Run with QEMU GDB server
qemu-system-i386 -kernel build/kernel.bin -s -S

# In another terminal, connect with GDB
gdb build/kernel.bin
(gdb) target remote localhost:1234
(gdb) continue
```

## Extending the Kernel

The current kernel is minimal. To extend it:

1. **Add new C files** in `kernel/` directory
2. **Update build.sh** to compile additional files
3. **Implement features**:
   - Keyboard input handler
   - Memory management
   - Process scheduling
   - File system support
   - Network stack

## Technical Details

### Multiboot Compliance

The kernel implements Multiboot v1 specification:
- Magic number: `0x1BADB002`
- Flags: `ALIGN | MEMINFO`
- Header in first 8KB of kernel image

### VGA Text Mode

- Base address: `0xB8000`
- Resolution: 80x25 characters
- Format: 16-bit per character (8-bit ASCII + 8-bit color)
- Color scheme: 4-bit background + 4-bit foreground

## Troubleshooting

### Build fails with "i686-elf-gcc not found"

Install the cross-compiler or let it fallback to system GCC with `-m32`.

### Linking fails with "cannot find -lgcc"

Install 32-bit libraries:
```bash
sudo apt install gcc-multilib lib32gcc-s1
```

### ISO creation fails

Install GRUB tools:
```bash
sudo apt install grub-pc-bin xorriso mtools
```

### QEMU won't boot

Try booting the kernel directly:
```bash
qemu-system-i386 -kernel build/kernel.bin
```

## License

Apache License 2.0 - See LICENSE file for details

**Copyright © 2026 Strategickhaos DAO LLC**

---

*"Ratio Ex Nihilo" - Reason from Nothing*

**Legion of Minds Convergence:**
- Grok: Boot scaffolding (grub.cfg, start.s, kernel.c, linker.ld)
- GPT: Toolchain installer + production merge
- Claude: Cross-reference verification + final assembly
