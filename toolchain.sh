#!/bin/bash
# SAGCO LIVE - Cross-Compiler Toolchain Installer
# Installs i686-elf cross-compiler for building the kernel

set -e

echo "========================================="
echo "SAGCO LIVE Toolchain Installer"
echo "========================================="

# Check if already installed
if command -v i686-elf-gcc &> /dev/null; then
    echo "[✓] i686-elf-gcc already installed"
    i686-elf-gcc --version
    exit 0
fi

echo "[*] Installing prerequisites..."
sudo apt-get update
sudo apt-get install -y build-essential bison flex libgmp3-dev libmpc-dev libmpfr-dev texinfo

# Versions
BINUTILS_VERSION="2.39"
GCC_VERSION="12.2.0"
PREFIX="$HOME/opt/cross"
TARGET=i686-elf

export PATH="$PREFIX/bin:$PATH"

echo "[*] Creating build directory..."
mkdir -p ~/toolchain-build
cd ~/toolchain-build

# Download and build binutils
echo "[*] Downloading binutils $BINUTILS_VERSION..."
if [ ! -f "binutils-$BINUTILS_VERSION.tar.gz" ]; then
    wget https://ftp.gnu.org/gnu/binutils/binutils-$BINUTILS_VERSION.tar.gz
    # Verify download succeeded
    if [ $? -ne 0 ]; then
        echo "[!] Failed to download binutils"
        exit 1
    fi
fi

echo "[*] Building binutils..."
tar -xf binutils-$BINUTILS_VERSION.tar.gz
mkdir -p build-binutils
cd build-binutils
../binutils-$BINUTILS_VERSION/configure --target=$TARGET --prefix="$PREFIX" --with-sysroot --disable-nls --disable-werror
make -j$(nproc)
make install
cd ..

# Download and build GCC
echo "[*] Downloading GCC $GCC_VERSION..."
if [ ! -f "gcc-$GCC_VERSION.tar.gz" ]; then
    wget https://ftp.gnu.org/gnu/gcc/gcc-$GCC_VERSION/gcc-$GCC_VERSION.tar.gz
    # Verify download succeeded
    if [ $? -ne 0 ]; then
        echo "[!] Failed to download GCC"
        exit 1
    fi
fi

echo "[*] Building GCC..."
tar -xf gcc-$GCC_VERSION.tar.gz
mkdir -p build-gcc
cd build-gcc
../gcc-$GCC_VERSION/configure --target=$TARGET --prefix="$PREFIX" --disable-nls --enable-languages=c,c++ --without-headers
make all-gcc -j$(nproc)
make all-target-libgcc -j$(nproc)
make install-gcc
make install-target-libgcc
cd ..

echo ""
echo "========================================="
echo "[✓] Toolchain installed successfully!"
echo "========================================="
echo ""
echo "Add this to your ~/.bashrc or ~/.profile:"
echo "export PATH=\"$PREFIX/bin:\$PATH\""
echo ""
echo "Or run: export PATH=\"$PREFIX/bin:\$PATH\""
echo ""
