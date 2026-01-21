#!/usr/bin/env bash
set -e

# ═══════════════════════════════════════════════════════════════════════════════
# SAGCO TOOLCHAIN INSTALLER
# Builds i686-elf cross-compiler from source
# Run once, then use build-sagco-live.sh
# ═══════════════════════════════════════════════════════════════════════════════

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "                      SAGCO TOOLCHAIN INSTALLER                                "
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "This will build the i686-elf cross-compiler toolchain."
echo "Estimated time: 15-30 minutes depending on your system."
echo ""

export PREFIX="$HOME/opt/cross"
export TARGET=i686-elf
export PATH="$PREFIX/bin:$PATH"

# ─────────────────────────────────────────────────────────────────────────────────
# Install build dependencies
# ─────────────────────────────────────────────────────────────────────────────────

echo "[*] Installing build dependencies..."
sudo apt update
sudo apt install -y \
    build-essential \
    bison \
    flex \
    libgmp3-dev \
    libmpc-dev \
    libmpfr-dev \
    texinfo \
    grub-pc-bin \
    xorriso \
    mtools \
    curl \
    qemu-system-x86

mkdir -p "$PREFIX"
mkdir -p "$HOME/src"
cd "$HOME/src"

# ─────────────────────────────────────────────────────────────────────────────────
# Build binutils
# ─────────────────────────────────────────────────────────────────────────────────

echo ""
echo "[*] Downloading binutils..."
if [ ! -f binutils-2.41.tar.xz ]; then
    curl -O https://ftp.gnu.org/gnu/binutils/binutils-2.41.tar.xz
fi

echo "[*] Extracting binutils..."
tar -xf binutils-2.41.tar.xz

echo "[*] Building binutils..."
mkdir -p build-binutils
cd build-binutils
../binutils-2.41/configure \
    --target=$TARGET \
    --prefix="$PREFIX" \
    --with-sysroot \
    --disable-nls \
    --disable-werror
make -j$(nproc)
make install
cd ..

# ─────────────────────────────────────────────────────────────────────────────────
# Build GCC
# ─────────────────────────────────────────────────────────────────────────────────

echo ""
echo "[*] Downloading GCC..."
if [ ! -f gcc-13.2.0.tar.xz ]; then
    curl -O https://ftp.gnu.org/gnu/gcc/gcc-13.2.0/gcc-13.2.0.tar.xz
fi

echo "[*] Extracting GCC..."
tar -xf gcc-13.2.0.tar.xz

echo "[*] Downloading GCC prerequisites..."
cd gcc-13.2.0
contrib/download_prerequisites
cd ..

echo "[*] Building GCC (this takes a while)..."
mkdir -p build-gcc
cd build-gcc
../gcc-13.2.0/configure \
    --target=$TARGET \
    --prefix="$PREFIX" \
    --disable-nls \
    --enable-languages=c \
    --without-headers
make all-gcc -j$(nproc)
make all-target-libgcc -j$(nproc)
make install-gcc
make install-target-libgcc
cd ..

# ─────────────────────────────────────────────────────────────────────────────────
# Verify installation
# ─────────────────────────────────────────────────────────────────────────────────

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "                         TOOLCHAIN INSTALLATION COMPLETE                       "
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "  Cross-compiler installed to: $PREFIX"
echo ""
echo "  Add to your PATH (add to ~/.bashrc for persistence):"
echo "    export PATH=\"$PREFIX/bin:\$PATH\""
echo ""
echo "  Verify with:"
echo "    i686-elf-gcc --version"
echo ""
echo "  Now run:"
echo "    cd flameos && ./build-sagco-live.sh"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
