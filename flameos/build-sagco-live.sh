#!/usr/bin/env bash
set -e

# ═══════════════════════════════════════════════════════════════════════════════
# SAGCO LIVE BUILD SCRIPT
# Builds the SAGCO OS kernel and creates bootable ISO
# Run after installing toolchain with install-sagco-toolchain.sh
# ═══════════════════════════════════════════════════════════════════════════════

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "                         SAGCO LIVE BUILD SYSTEM                               "
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Check for cross-compiler
if ! command -v i686-elf-gcc &> /dev/null; then
    echo "Error: i686-elf-gcc not found in PATH"
    echo ""
    echo "Please run install-sagco-toolchain.sh first, then add to your PATH:"
    echo "  export PATH=\"\$HOME/opt/cross/bin:\$PATH\""
    echo ""
    exit 1
fi

echo "[*] Cross-compiler found: $(i686-elf-gcc --version | head -n1)"
echo ""
echo "[*] SAGCO Live Build system is ready for implementation"
echo ""
echo "TODO: Add kernel build steps here"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
