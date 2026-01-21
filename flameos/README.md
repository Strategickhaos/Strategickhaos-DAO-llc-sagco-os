# FlameOS - SAGCO OS Kernel Build System

This directory contains the build system for the SAGCO OS kernel (FlameOS).

## Prerequisites

Before building, you must install the i686-elf cross-compiler toolchain:

```bash
cd ..
./install-sagco-toolchain.sh
```

This will:
- Download and build binutils 2.41
- Download and build GCC 13.2.0
- Install the cross-compiler to `$HOME/opt/cross`

The process takes approximately 15-30 minutes.

## Building SAGCO OS

After installing the toolchain, add it to your PATH:

```bash
export PATH="$HOME/opt/cross/bin:$PATH"
```

Then build the OS:

```bash
./build-sagco-live.sh
```

## Verifying the Toolchain

Check that the cross-compiler is properly installed:

```bash
i686-elf-gcc --version
```

## Directory Structure

```
flameos/
├── build-sagco-live.sh    # Main build script
└── README.md              # This file
```

## Next Steps

The kernel implementation will be added in future updates. This directory is prepared for the FlameOS kernel source code and build artifacts.
