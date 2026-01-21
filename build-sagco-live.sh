#!/bin/bash
# SAGCO LIVE - Main Build Script
# Builds the kernel and creates a bootable ISO

set -e

echo "========================================="
echo "Building SAGCO LIVE v0.1.0"
echo "========================================="

# Configuration
KERNEL_NAME="sagco.bin"
ISO_NAME="sagco-live.iso"

# Check for required tools
echo "[*] Checking dependencies..."

if ! command -v grub-mkrescue &> /dev/null; then
    echo "[!] grub-mkrescue not found. Install with:"
    echo "    sudo apt install grub-pc-bin xorriso mtools"
    exit 1
fi

# Detect cross-compiler or native compiler
if command -v i686-elf-gcc &> /dev/null; then
    CC="i686-elf-gcc"
    echo "[✓] Using cross-compiler: i686-elf-gcc"
elif command -v gcc &> /dev/null; then
    CC="gcc"
    echo "[!] Warning: Using native gcc instead of i686-elf-gcc"
    echo "    For best results, run ./toolchain.sh to install cross-compiler"
else
    echo "[!] No compiler found. Install gcc or run ./toolchain.sh"
    exit 1
fi

# Clean previous build
echo "[*] Cleaning previous build..."
rm -rf build isodir
mkdir -p build

# Compile assembly boot code
echo "[*] Compiling boot loader (start.s)..."
$CC -m32 -c boot/start.s -o build/start.o

# Compile kernel
echo "[*] Compiling kernel (kernel.c)..."
$CC -m32 -c kernel/kernel.c -o build/kernel.o -std=gnu99 -ffreestanding -O2 -Wall -Wextra -fno-pie

# Link kernel
echo "[*] Linking kernel..."
if [ "$CC" = "i686-elf-gcc" ]; then
    # Cross-compiler can use libgcc
    $CC -m32 -T linker.ld -o build/$KERNEL_NAME -ffreestanding -O2 -nostdlib build/start.o build/kernel.o -lgcc
else
    # Native gcc - link without libgcc and disable PIE
    $CC -m32 -T linker.ld -o build/$KERNEL_NAME -ffreestanding -O2 -nostdlib -no-pie build/start.o build/kernel.o
fi

# Verify multiboot header
echo "[*] Verifying multiboot header..."
if command -v grub-file &> /dev/null; then
    if grub-file --is-x86-multiboot build/$KERNEL_NAME; then
        echo "[✓] Multiboot header verified"
    else
        echo "[!] Warning: Multiboot header verification failed"
    fi
fi

# Create ISO directory structure
echo "[*] Creating ISO structure..."
mkdir -p isodir/boot/grub

# Copy kernel and GRUB config
cp build/$KERNEL_NAME isodir/boot/
cp boot/grub.cfg isodir/boot/grub/

# Create bootable ISO
echo "[*] Creating bootable ISO..."
grub-mkrescue -o $ISO_NAME isodir

# Show result
echo ""
echo "========================================="
echo "[✓] Build complete!"
echo "========================================="
echo ""
echo "ISO created: $ISO_NAME"
echo ""
echo "To test in QEMU, run:"
echo "  qemu-system-i386 -cdrom $ISO_NAME"
echo ""
echo "To test in VirtualBox/VMware:"
echo "  1. Create a new VM (32-bit x86)"
echo "  2. Attach $ISO_NAME as CD-ROM"
echo "  3. Boot from CD-ROM"
echo ""
