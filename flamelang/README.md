# FlameLang v2.0.0

FlameLang is a physics-native programming language with a 5-layer transformation pipeline, designed for the SAGCO OS ecosystem. It demonstrates Object-Oriented Programming principles in Rust while correlating with Saupe's random fractal theory.

## 🔥 Features

- **5-Layer Compilation Pipeline**: Linguistic → Numeric → Geometric → Bound → Symbolic
- **Physics-Native Types**: Unit circle angles, bounded values, vector operations
- **OOP in Rust**: Encapsulation, abstraction, composition, and polymorphism
- **Production-Ready**: Optimized build profiles for deployment
- **Fractal Architecture**: Simple rules generate complex computations (D ≈ 1.55)

## 🏗️ Architecture

FlameLang demonstrates OOP principles without traditional classes:

### 1. Encapsulation
```rust
pub struct FlameIR {
    declarations: Vec<String>,  // Private
    expressions: Vec<String>,   // Private
}

impl FlameIR {
    pub fn add_declaration(&mut self, decl: String) { /* Public API */ }
}
```

### 2. Abstraction
```rust
pub trait Transform {
    fn apply(&self, input: &FlameType) -> Result<FlameType, FlameError>;
}
```

### 3. Composition (not Inheritance)
```rust
pub struct Pipeline {
    layers: Vec<Box<dyn Transform>>,  // Composes transforms
}
```

### 4. Polymorphism
```rust
pipeline.add_layer(IdentityTransform);
pipeline.add_layer(ScaleTransform { factor: 2.0 });
// Same interface, different behavior
```

## 📦 Building

### Development Build
```bash
cargo build
cargo test
cargo run
```

### Production Build
```bash
# With LLVM backend
cargo build --release --features native-compile

# Without LLVM (faster compile)
cargo build --release
```

### Check Compilation
```bash
cargo check
```

## 🔧 Dependencies

- **thiserror**: Error handling
- **inkwell** (optional): LLVM backend for native compilation
- **logos**: Lexer generation
- **lalrpop**: Parser generation

## 📊 Build Profiles

### Release Profile
- **LTO**: Link-time optimization enabled
- **Codegen Units**: 1 (maximum optimization)
- **Panic**: Abort (smaller binary)
- **Strip**: Debug symbols removed
- **Opt Level**: 3 (full optimization)

### Dev Profile
- **Opt Level**: 1 (fast compilation with basic optimization)
- **Debug**: true (preserves proof information)

## 📚 Documentation

- **[OOP_PRINCIPLES.md](OOP_PRINCIPLES.md)**: Detailed explanation of OOP in Rust
- **[FRACTAL_THEORY.md](FRACTAL_THEORY.md)**: Correlation with Saupe's random fractals

## 🎯 Usage

```rust
use flamelang::{Pipeline, FlameType, ScaleTransform};

// Create compilation pipeline
let mut pipeline = Pipeline::new("My Pipeline".to_string());
pipeline.add_layer(ScaleTransform { factor: 2.0 });

// Compile
let source = FlameType::Integer(42);
let result = pipeline.execute(source)?;
```

## 🧪 Testing

```bash
# Run all tests
cargo test

# Run tests with output
cargo test -- --nocapture

# Run specific test
cargo test test_angle_normalization
```

## 🚀 Production Deployment

FlameLang is optimized for containerized deployment:

```bash
# Build optimized binary
cargo build --release --features native-compile

# Binary location
./target/release/flamec

# Size optimization achieved through:
# - LTO (link-time optimization)
# - Strip (remove debug symbols)
# - Single codegen unit
# - Full optimization (opt-level 3)
```

## 📐 Fractal Theory Connection

FlameLang's architecture exhibits fractal properties:
- **Chaos Game**: Layers as iterative random transforms
- **Self-Similar**: Each layer mirrors pipeline structure
- **Fractal Dimension**: D ≈ 1.55 (H=0.45 from simulation)
- **Bounded**: Type system constrains attractor basins

Simple source code → Iterative transformations → Complex physics/DNA computations

## 🔬 Mathematical Properties

- **Angle Type**: Always bounded [0, 2π), living on unit circle
- **Bounded Type**: Enforced constraints at compile time
- **Type Safety**: Rust's ownership prevents null/undefined behavior
- **Proof Preservation**: Debug builds maintain proof information

## 📜 License

MIT License - see [../LICENSE](../LICENSE)

## 🏢 Author

Strategickhaos DAO LLC  
security@strategickhaos.ai

## 🔗 Links

- Repository: https://github.com/strategickhaos/dao-llc/skh-flamelang
- SAGCO OS: https://github.com/Strategickhaos/Strategickhaos-DAO-llc-sagco-os
- Crates.io: [flamelang](https://crates.io/crates/flamelang)

---

**"Simple rules, infinite detail—the fractal is the program."** 🔥
