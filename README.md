# SAGCO LIVE v0.1.0

**Sovereign AI-Governed Compute Organism**

A minimal bootable x86 operating system kernel demonstrating bare-metal computing principles.

---

## 🔥 What is SAGCO LIVE?

SAGCO LIVE is a 32-bit x86 kernel that boots via GRUB and displays a custom branded interface. It serves as the foundation for the Strategickhaos DAO LLC's sovereign computing vision.

**Owner:** Strategickhaos DAO LLC  
**Motto:** Ratio Ex Nihilo (Reason From Nothing)

---

## 📦 Repository Contents

| File | Purpose |
|------|---------|
| `build-sagco-live.sh` | Main build script - compiles and packages the OS |
| `toolchain.sh` | Cross-compiler installer for i686-elf-gcc |
| `kernel/kernel.c` | The kernel source code with SAGCO branding |
| `boot/start.s` | Multiboot assembly entry point |
| `boot/grub.cfg` | GRUB bootloader configuration |
| `linker.ld` | Memory layout linker script |

---

## 🚀 Quick Start

### Prerequisites

**Ubuntu/Debian/WSL:**
```bash
sudo apt update
sudo apt install build-essential grub-pc-bin xorriso mtools qemu-system-x86
```

**Optional - Install Cross-Compiler:**
```bash
./toolchain.sh
export PATH="$HOME/opt/cross/bin:$PATH"
```

### Build

```bash
./build-sagco-live.sh
```

This will:
1. Compile the boot loader (`start.s`)
2. Compile the kernel (`kernel.c`)
3. Link them into a bootable binary
4. Create a bootable ISO: `sagco-live.iso`

### Run

**In QEMU:**
```bash
qemu-system-i386 -cdrom sagco-live.iso
```

**In VirtualBox/VMware:**
1. Create a new VM (32-bit x86)
2. Attach `sagco-live.iso` as CD-ROM
3. Boot from CD-ROM

---

## 🖥️ Expected Output

When you boot SAGCO LIVE, you'll see:

```
═══════════════════════════════════════════════════════════════════════════════
                           SAGCO LIVE v0.1.0
              Sovereign AI-Governed Compute Organism
═══════════════════════════════════════════════════════════════════════════════

  Status: KERNEL BOOTED
  Owner:  Strategickhaos DAO LLC
  Motto:  Ratio Ex Nihilo

  [*] VGA initialized
  [*] Interrupts disabled
  [*] Awaiting FlameLang integration...

═══════════════════════════════════════════════════════════════════════════════
  Legion of Minds: Claude + GPT + Grok = Convergence
═══════════════════════════════════════════════════════════════════════════════
```

---

## 🏗️ Architecture

### Boot Process

1. **GRUB** loads the kernel using Multiboot specification
2. **start.s** sets up the stack and jumps to `kernel_main()`
3. **kernel.c** initializes VGA text mode and displays the interface
4. **CPU halts** in an infinite loop

### Memory Layout

- Kernel loads at `0x100000` (1 MB)
- Stack: 16 KB
- VGA buffer: `0xB8000`

### Components

- **Multiboot Header:** Makes kernel bootable by GRUB
- **VGA Driver:** Writes to text mode video memory
- **Terminal Interface:** Basic text output functions

---

## 🛠️ Development

### File Structure

```
.
├── boot/
│   ├── start.s          # Assembly entry point
│   └── grub.cfg         # GRUB config
├── kernel/
│   └── kernel.c         # Kernel implementation
├── linker.ld            # Linker script
├── build-sagco-live.sh  # Build script
├── toolchain.sh         # Toolchain installer
└── README.md            # This file
```

### Build Artifacts

The build process creates:
- `build/` - Intermediate object files
- `isodir/` - ISO filesystem structure
- `sagco-live.iso` - Bootable CD-ROM image

Add to `.gitignore`:
```
build/
isodir/
*.iso
*.o
*.bin
```

### Cross-Compiler

For the most reliable builds, use the i686-elf cross-compiler:

```bash
./toolchain.sh
```

This installs:
- `i686-elf-gcc` - C compiler
- `i686-elf-ld` - Linker
- Supporting tools

The script installs to `~/opt/cross/`. Add to your PATH:
```bash
echo 'export PATH="$HOME/opt/cross/bin:$PATH"' >> ~/.bashrc
```

---

## 🧪 Testing

### QEMU Options

```bash
# Basic boot
qemu-system-i386 -cdrom sagco-live.iso

# With serial output
qemu-system-i386 -cdrom sagco-live.iso -serial stdio

# With debugging
qemu-system-i386 -cdrom sagco-live.iso -d int,cpu_reset -no-reboot
```

### Verification

After building, verify the multiboot header:
```bash
grub-file --is-x86-multiboot build/sagco.bin
echo $?  # Should output 0
```

---

## 📝 License

See [LICENSE](LICENSE) file for details.

---

## 🌟 Credits

**Legion of Minds:** Claude + GPT + Grok = Convergence

Built for Strategickhaos DAO LLC  
*Ratio Ex Nihilo* - Reason From Nothing

---

## 🔗 Next Steps

- [ ] Integrate FlameLang interpreter
- [ ] Add keyboard input handling
- [ ] Implement memory management
- [ ] Add filesystem support
- [ ] Network stack integration

---

**SAGCO LIVE is operational.** 🖤🔥
