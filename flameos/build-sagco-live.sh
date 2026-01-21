#!/bin/bash
# build-sagco-live.sh - Build script for SAGCO LIVE v0.1.0
# Strategickhaos DAO LLC - Ratio Ex Nihilo

set -e

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "  Building SAGCO LIVE v0.1.0"
echo "  Sovereign AI-Governed Compute Organism"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Configuration
BUILD_DIR="build"
ISO_DIR="$BUILD_DIR/isodir"
KERNEL_BIN="$BUILD_DIR/kernel.bin"
ISO_FILE="sagco-live.iso"

# Detect compiler
if command -v i686-elf-gcc &> /dev/null; then
    CC="i686-elf-gcc"
    AS="i686-elf-as"
    echo "[*] Using cross-compiler: i686-elf-gcc"
elif command -v gcc &> /dev/null; then
    CC="gcc -m32"
    AS="as --32"
    echo "[*] Using system GCC with 32-bit mode"
else
    echo "[!] Error: No suitable compiler found"
    echo "    Install i686-elf-gcc or ensure gcc supports 32-bit compilation"
    exit 1
fi

# Clean previous build
echo "[*] Cleaning previous build..."
rm -rf "$BUILD_DIR" "$ISO_FILE"

# Create build directories
echo "[*] Creating build directories..."
mkdir -p "$BUILD_DIR"
mkdir -p "$ISO_DIR/boot/grub"

# Assemble start.s
echo "[*] Assembling boot code..."
$AS boot/start.s -o "$BUILD_DIR/start.o"

# Compile kernel.c
echo "[*] Compiling kernel..."
$CC -std=gnu99 -ffreestanding -O2 -Wall -Wextra -c kernel/kernel.c -o "$BUILD_DIR/kernel.o"

# Link kernel
echo "[*] Linking kernel..."
if command -v i686-elf-gcc &> /dev/null; then
    i686-elf-gcc -T linker.ld -o "$KERNEL_BIN" -ffreestanding -O2 -nostdlib "$BUILD_DIR/start.o" "$BUILD_DIR/kernel.o" -lgcc
else
    gcc -m32 -T linker.ld -o "$KERNEL_BIN" -ffreestanding -O2 -nostdlib "$BUILD_DIR/start.o" "$BUILD_DIR/kernel.o" -lgcc
fi

# Verify multiboot header
echo "[*] Verifying multiboot header..."
if command -v grub-file &> /dev/null; then
    if grub-file --is-x86-multiboot "$KERNEL_BIN"; then
        echo "    ✓ Multiboot header confirmed"
    else
        echo "    ! Warning: Multiboot header not detected (might still work)"
    fi
else
    echo "    ? grub-file not found, skipping verification"
fi

# Copy files to ISO directory
echo "[*] Preparing ISO structure..."
cp "$KERNEL_BIN" "$ISO_DIR/boot/kernel.bin"
cp boot/grub.cfg "$ISO_DIR/boot/grub/grub.cfg"

# Create bootable ISO
echo "[*] Creating bootable ISO..."
if command -v grub-mkrescue &> /dev/null; then
    grub-mkrescue -o "$ISO_FILE" "$ISO_DIR" 2>/dev/null || {
        echo "[!] grub-mkrescue failed, trying alternative..."
        grub-mkrescue -o "$ISO_FILE" "$ISO_DIR"
    }
else
    echo "[!] Error: grub-mkrescue not found"
    echo "    Install grub-pc-bin or grub-common package"
    exit 1
fi

# Success
if [ -f "$ISO_FILE" ]; then
    ISO_SIZE=$(du -h "$ISO_FILE" | cut -f1)
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "  ✓ Build successful!"
    echo "  ISO: $ISO_FILE ($ISO_SIZE)"
    echo ""
    echo "  To test in QEMU:"
    echo "    qemu-system-i386 -cdrom $ISO_FILE"
    echo ""
    echo "  To boot on real hardware:"
    echo "    dd if=$ISO_FILE of=/dev/sdX bs=4M"
    echo "    (Replace /dev/sdX with your USB drive)"
    echo "═══════════════════════════════════════════════════════════════════════════════"
else
    echo "[!] Error: ISO creation failed"
    exit 1
fi
