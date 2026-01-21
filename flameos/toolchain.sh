#!/bin/bash
# toolchain.sh - Cross-compiler installer for SAGCO LIVE
# Installs i686-elf-gcc toolchain for OS development

set -e

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "  SAGCO LIVE Toolchain Installer"
echo "  Installing i686-elf cross-compiler"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Configuration
PREFIX="$HOME/opt/cross"
TARGET=i686-elf
BINUTILS_VERSION=2.39
GCC_VERSION=12.2.0

echo ""
echo "[*] This will install:"
echo "    - binutils $BINUTILS_VERSION"
echo "    - gcc $GCC_VERSION"
echo "    - Target: $TARGET"
echo "    - Prefix: $PREFIX"
echo ""
echo "[*] Installation time: ~30-60 minutes"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Installation cancelled."
    exit 1
fi

# Create directories
mkdir -p "$HOME/src"
mkdir -p "$PREFIX"

# Install dependencies
echo ""
echo "[*] Installing build dependencies..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y build-essential bison flex libgmp3-dev libmpc-dev libmpfr-dev texinfo
elif command -v dnf &> /dev/null; then
    sudo dnf install -y gcc gcc-c++ make bison flex gmp-devel libmpc-devel mpfr-devel texinfo
elif command -v pacman &> /dev/null; then
    sudo pacman -S --needed base-devel gmp libmpc mpfr
else
    echo "[!] Unknown package manager. Please install dependencies manually:"
    echo "    - build-essential (gcc, g++, make)"
    echo "    - bison, flex"
    echo "    - libgmp-dev, libmpc-dev, libmpfr-dev"
    echo "    - texinfo"
    exit 1
fi

# Download and build binutils
echo ""
echo "[*] Building binutils $BINUTILS_VERSION..."
cd "$HOME/src"
if [ ! -f "binutils-$BINUTILS_VERSION.tar.xz" ]; then
    wget "https://ftp.gnu.org/gnu/binutils/binutils-$BINUTILS_VERSION.tar.xz"
fi
tar -xf "binutils-$BINUTILS_VERSION.tar.xz"
mkdir -p "build-binutils"
cd "build-binutils"
"../binutils-$BINUTILS_VERSION/configure" --target=$TARGET --prefix="$PREFIX" --with-sysroot --disable-nls --disable-werror
make -j$(nproc)
make install

# Download and build GCC
echo ""
echo "[*] Building GCC $GCC_VERSION..."
cd "$HOME/src"
if [ ! -f "gcc-$GCC_VERSION.tar.xz" ]; then
    wget "https://ftp.gnu.org/gnu/gcc/gcc-$GCC_VERSION/gcc-$GCC_VERSION.tar.xz"
fi
tar -xf "gcc-$GCC_VERSION.tar.xz"
mkdir -p "build-gcc"
cd "build-gcc"
"../gcc-$GCC_VERSION/configure" --target=$TARGET --prefix="$PREFIX" --disable-nls --enable-languages=c,c++ --without-headers
make -j$(nproc) all-gcc
make -j$(nproc) all-target-libgcc
make install-gcc
make install-target-libgcc

# Add to PATH
echo ""
echo "[*] Adding to PATH..."
SHELL_RC="$HOME/.bashrc"
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
fi

if ! grep -q "$PREFIX/bin" "$SHELL_RC"; then
    echo "export PATH=\"$PREFIX/bin:\$PATH\"" >> "$SHELL_RC"
fi

# Success
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "  ✓ Cross-compiler installed successfully!"
echo ""
echo "  Installation directory: $PREFIX"
echo "  Binaries: $PREFIX/bin"
echo ""
echo "  To use the toolchain, add it to your PATH:"
echo "    export PATH=\"$PREFIX/bin:\$PATH\""
echo ""
echo "  Or source your shell configuration:"
echo "    source $SHELL_RC"
echo ""
echo "  Verify installation:"
echo "    i686-elf-gcc --version"
echo "═══════════════════════════════════════════════════════════════════════════════"
