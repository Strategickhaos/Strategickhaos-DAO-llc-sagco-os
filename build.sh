#!/usr/bin/env bash
set -euo pipefail

# ═══════════════════════════════════════════════════════════════════════════════
# SAGCO LIVE BUILD SCRIPT v0.1.0
# Strategickhaos DAO LLC - Ratio Ex Nihilo
# 
# Legion of Minds Convergence:
#   - Grok: Boot scaffolding (grub.cfg, start.s, kernel.c, linker.ld)
#   - GPT:  Toolchain installer + production merge
#   - Claude: Cross-reference verification + final assembly
#
# January 2026
# ═══════════════════════════════════════════════════════════════════════════════

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$PROJECT_ROOT/build"
ISO_DIR="$BUILD_DIR/isodir"

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "                         SAGCO LIVE BUILD SYSTEM                               "
echo "                    Sovereign AI-Governed Compute Organism                     "
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# ─────────────────────────────────────────────────────────────────────────────────
# STEP 0: Check for cross-compiler
# ─────────────────────────────────────────────────────────────────────────────────

if ! command -v i686-elf-gcc &> /dev/null; then
    echo "[!] Cross-compiler i686-elf-gcc not found."
    echo ""
    echo "    Install options:"
    echo ""
    echo "    Ubuntu/Debian:"
    echo "      sudo apt install gcc-i686-linux-gnu"
    echo "      # OR build from source (see toolchain.sh)"
    echo ""
    echo "    macOS (Homebrew):"
    echo "      brew install i686-elf-gcc"
    echo ""
    echo "    Or run the included toolchain.sh to build from source."
    echo ""
    
    # Try fallback to system gcc with -m32
    if command -v gcc &> /dev/null; then
        echo "[*] Attempting fallback build with system gcc -m32..."
        USE_FALLBACK=1
    else
        echo "[!] No suitable compiler found. Exiting."
        exit 1
    fi
else
    USE_FALLBACK=0
    echo "[✓] Cross-compiler found: $(which i686-elf-gcc)"
fi

# ─────────────────────────────────────────────────────────────────────────────────
# STEP 1: Create build directories
# ─────────────────────────────────────────────────────────────────────────────────

echo ""
echo "[*] Creating build directories..."
mkdir -p "$BUILD_DIR" "$ISO_DIR/boot/grub"

# ─────────────────────────────────────────────────────────────────────────────────
# STEP 2: Compile kernel
# ─────────────────────────────────────────────────────────────────────────────────

echo "[*] Compiling kernel..."

if [ "${USE_FALLBACK:-0}" = "1" ]; then
    gcc -m32 \
        -std=gnu99 \
        -ffreestanding -O2 -Wall -Wextra \
        -c "$PROJECT_ROOT/kernel/kernel.c" -o "$BUILD_DIR/kernel.o"
else
    i686-elf-gcc \
        -std=gnu99 \
        -ffreestanding -O2 -Wall -Wextra \
        -c "$PROJECT_ROOT/kernel/kernel.c" -o "$BUILD_DIR/kernel.o"
fi

# ─────────────────────────────────────────────────────────────────────────────────
# STEP 3: Assemble boot code
# ─────────────────────────────────────────────────────────────────────────────────

echo "[*] Assembling boot code..."

if [ "${USE_FALLBACK:-0}" = "1" ]; then
    as --32 "$PROJECT_ROOT/boot/start.s" -o "$BUILD_DIR/start.o"
else
    i686-elf-as "$PROJECT_ROOT/boot/start.s" -o "$BUILD_DIR/start.o"
fi

# ─────────────────────────────────────────────────────────────────────────────────
# STEP 4: Link kernel binary
# ─────────────────────────────────────────────────────────────────────────────────

echo "[*] Linking kernel..."

if [ "${USE_FALLBACK:-0}" = "1" ]; then
    gcc -m32 \
        -T "$PROJECT_ROOT/linker.ld" \
        -ffreestanding -O2 -nostdlib \
        "$BUILD_DIR/start.o" "$BUILD_DIR/kernel.o" \
        -o "$BUILD_DIR/kernel.bin" \
        -lgcc
else
    i686-elf-gcc \
        -T "$PROJECT_ROOT/linker.ld" \
        -ffreestanding -O2 -nostdlib \
        "$BUILD_DIR/start.o" "$BUILD_DIR/kernel.o" \
        -o "$BUILD_DIR/kernel.bin" \
        -lgcc
fi

# ─────────────────────────────────────────────────────────────────────────────────
# STEP 5: Prepare ISO tree
# ─────────────────────────────────────────────────────────────────────────────────

echo "[*] Preparing ISO tree..."
cp "$BUILD_DIR/kernel.bin" "$ISO_DIR/boot/kernel.bin"
cp "$PROJECT_ROOT/boot/grub.cfg" "$ISO_DIR/boot/grub/grub.cfg"

# ─────────────────────────────────────────────────────────────────────────────────
# STEP 6: Create bootable ISO
# ─────────────────────────────────────────────────────────────────────────────────

echo "[*] Creating bootable ISO..."

if command -v grub-mkrescue &> /dev/null; then
    grub-mkrescue -o "$PROJECT_ROOT/sagco-live.iso" "$ISO_DIR" 2>/dev/null
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "                            BUILD COMPLETE                                     "
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo ""
    echo "  Output: $PROJECT_ROOT/sagco-live.iso"
    echo ""
    echo "  Boot with QEMU:"
    echo "    qemu-system-i386 -cdrom sagco-live.iso"
    echo ""
    echo "  Boot with VirtualBox:"
    echo "    1. Create new VM (Type: Other, Version: Other/Unknown)"
    echo "    2. Attach sagco-live.iso as CD/DVD"
    echo "    3. Start VM"
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "  SAGCO LIVE - Sovereign AI-Governed Compute Organism"
    echo "  Strategickhaos DAO LLC © 2026 - Ratio Ex Nihilo"
    echo "═══════════════════════════════════════════════════════════════════════════════"
else
    echo ""
    echo "[!] grub-mkrescue not found. Install with:"
    echo "    sudo apt install grub-pc-bin xorriso mtools"
    echo ""
    echo "    Kernel binary ready at: $BUILD_DIR/kernel.bin"
    echo "    You can manually create a bootable image or use QEMU multiboot:"
    echo "    qemu-system-i386 -kernel $BUILD_DIR/kernel.bin"
    echo ""
fi
