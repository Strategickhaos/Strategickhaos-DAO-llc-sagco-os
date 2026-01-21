# Strategickhaos-DAO-llc-sagco-os
SAGCO OS v0.1.0 is operational

## SAGCO Toolchain Installation

To build SAGCO OS from source, you need to install the i686-elf cross-compiler toolchain:

```bash
./install-sagco-toolchain.sh
```

This script will:
- Install required build dependencies (build-essential, bison, flex, etc.)
- Download and build binutils 2.41
- Download and build GCC 13.2.0 with C language support
- Install the cross-compiler to `$HOME/opt/cross`

**Estimated time:** 15-30 minutes depending on your system.

After installation, add the toolchain to your PATH:

```bash
export PATH="$HOME/opt/cross/bin:$PATH"
```

For persistence, add this line to your `~/.bashrc`.

## Building FlameOS

Once the toolchain is installed, you can build the SAGCO OS kernel:

```bash
cd flameos
./build-sagco-live.sh
```

See [flameos/README.md](flameos/README.md) for more details on the kernel build system.
