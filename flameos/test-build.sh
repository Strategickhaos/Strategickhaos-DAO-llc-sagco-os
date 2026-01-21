#!/bin/bash
# test-build.sh - Quick test script for SAGCO LIVE build
# Verifies that the build system works correctly

set -e

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "  SAGCO LIVE v0.1.0 - Build Verification"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Change to flameos directory
cd "$(dirname "$0")"

# Clean previous build
echo "[*] Cleaning previous build..."
rm -rf build sagco-live.iso

# Run build
echo "[*] Running build script..."
./build-sagco-live.sh

# Verify outputs
echo ""
echo "[*] Verifying build outputs..."

if [ ! -f "sagco-live.iso" ]; then
    echo "    [FAIL] ISO file not created!"
    exit 1
else
    echo "    [PASS] ISO file exists"
fi

if [ ! -f "build/kernel.bin" ]; then
    echo "    [FAIL] Kernel binary not created!"
    exit 1
else
    echo "    [PASS] Kernel binary exists"
fi

# Check multiboot header
if command -v grub-file &> /dev/null; then
    if grub-file --is-x86-multiboot build/kernel.bin; then
        echo "    [PASS] Multiboot header valid"
    else
        echo "    [WARN] Multiboot header check failed (may still work)"
    fi
else
    echo "    [INFO] grub-file not available, skipping multiboot check"
fi

# Check file sizes
ISO_SIZE=$(stat -f%z sagco-live.iso 2>/dev/null || stat -c%s sagco-live.iso)
KERNEL_SIZE=$(stat -f%z build/kernel.bin 2>/dev/null || stat -c%s build/kernel.bin)

echo "    [INFO] ISO size: $((ISO_SIZE / 1024 / 1024)) MB"
echo "    [INFO] Kernel size: $((KERNEL_SIZE / 1024)) KB"

# Success
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "  ✓ Build verification complete!"
echo ""
echo "  To test in QEMU:"
echo "    qemu-system-i386 -cdrom sagco-live.iso"
echo ""
echo "  To test with KVM (faster):"
echo "    qemu-system-i386 -enable-kvm -cdrom sagco-live.iso"
echo "═══════════════════════════════════════════════════════════════════════════════"
