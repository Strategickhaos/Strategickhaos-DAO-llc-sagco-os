# OOP Principles in Rust for FlameLang

## Overview
Rust implements Object-Oriented Programming (OOP) principles without traditional classes and inheritance. Instead, it uses structs, traits, and composition to achieve encapsulation, abstraction, inheritance-like behavior, and polymorphism—avoiding common pitfalls like the diamond problem while ensuring memory safety through ownership.

## 1. Encapsulation (Data Hiding & Safety)

**Definition**: Bundle data and behavior together, exposing only what's necessary while keeping implementation details private.

**Rust Implementation**: 
- Structs and enums with `pub`/private fields
- Methods in `impl` blocks
- Module system with `pub` keyword controlling visibility

**FlameLang Example**:
```rust
pub struct FlameIR {
    decls: Vec<Declaration>,      // Private: internal AST structure
    exprs: Vec<Expression>,        // Private: hidden from users
    proofs: Vec<BoundedProof>,     // Private: Angle mod 2π validation
}

impl FlameIR {
    pub fn new() -> Self { /* ... */ }
    pub fn transform(&self) -> Result<CompiledOutput> { /* ... */ }
    // Users access via public methods, internals remain encapsulated
}
```

**SAGCO OS Connection**: 
- Refinery functions like `gen_binaural()` encapsulate wave mathematics and sampling rate logic
- Users call high-level APIs without knowing numpy/scipy implementation details
- Cargo.toml `[lib] path="src/lib.rs"` exposes API safely

## 2. Abstraction (Hide Implementation, Expose Interface)

**Definition**: Focus on "what" an operation does, not "how" it does it. Define contracts without implementation details.

**Rust Implementation**:
- Traits define method signatures that types must implement
- Associated types and constants in traits
- Default implementations for common behavior

**FlameLang Example**:
```rust
pub trait Transform {
    fn apply(&self, input: &FlameType) -> Result<FlameType>;
    fn validate_bounds(&self) -> bool;
}

pub enum FlameOp {
    Bend(BendTransform),
    Codon(CodonMap),
}

impl Transform for BendTransform {
    fn apply(&self, input: &FlameType) -> Result<FlameType> {
        // DNA mapping logic abstracted away
    }
}

// Users call transform.apply() without knowing DNA map internals
```

**SAGCO OS Connection**:
- `refinery()` abstracts phases: audio/visual/symbolic processing as trait methods
- Emotion classification abstracted through trait interfaces
- Cargo categories `["compilers"]` abstracts flamelang as a development tool

## 3. Inheritance (Code Reuse)

**Definition**: Reuse code from parent structures. Rust avoids traditional inheritance to prevent complexity.

**Rust Implementation**:
- **Composition**: Structs contain other structs
- **Trait Implementation**: Types implement multiple traits for shared behavior
- **Default Trait Methods**: Provide reusable implementations

**FlameLang Example**:
```rust
// Composition: FlameType composes primitives with constraints
pub enum FlameType {
    Angle(f64),    // Composes Float + modulo 2π constraint
    Vector(Vec<f64>),
    Bounded { value: f64, min: f64, max: f64 },
}

// Trait-based inheritance: Multiple types share Transform behavior
impl Transform for FlameType {
    fn apply(&self, op: &FlameOp) -> Result<FlameType> {
        match self {
            FlameType::Angle(a) => op.apply_to_angle(a),
            FlameType::Vector(v) => op.apply_to_vector(v),
            // Each variant "inherits" transform capability
        }
    }
}
```

**SAGCO OS Connection**:
- Channels inherit `BaseChannel` trait (Symbolic composes classification/binary)
- Dependencies like `thiserror` provide "inherited" error handling patterns
- Cargo workspace can compose multiple crates (flamelang + refinery)

## 4. Polymorphism (Same Interface, Different Behavior)

**Definition**: Call the same method on different types with behavior specific to each type.

**Rust Implementation**:
- **Static Polymorphism**: Generics with trait bounds (compile-time)
- **Dynamic Polymorphism**: Trait objects with `dyn Trait` (runtime)
- **Enum Dispatch**: Match on variants for different behaviors

**FlameLang Example**:
```rust
// Static polymorphism with generics
pub fn run_transforms<T: Transform>(input: T, layers: Vec<Layer>) -> Result<Output> {
    layers.iter().fold(Ok(input), |acc, layer| {
        acc.and_then(|data| layer.transform(data))
    })
}

// Dynamic polymorphism with trait objects
pub fn compose_pipeline(transforms: Vec<Box<dyn Transform>>) -> Pipeline {
    Pipeline { stages: transforms }
}

// Enum dispatch
match operation {
    FlameOp::Linguistic(l) => l.transform(data),  // Different behavior
    FlameOp::Numeric(n) => n.transform(data),     // Different behavior
}
```

**SAGCO OS Connection**:
- `compose_midi(emotion)` is polymorphic on input (calm vs. alert produces different scales)
- Cargo features `["native-compile"]` enable polymorphic builds (toggle LLVM backend)
- Same `refinery()` interface handles different emotion types polymorphically

## Rust's Advantage: Safety + OOP

Rust's OOP implementation is "leaner" and safer:
- **Ownership** enforces memory safety (no null pointers, no data races)
- **Traits** enable multiple "inheritance" without diamond problem
- **Zero-cost Abstractions**: OOP features compile to efficient machine code
- **Explicit over Implicit**: No hidden virtual function tables, clear performance model

## FlameLang Architecture as OOP

The 5-layer transformation pipeline demonstrates all OOP principles:

1. **Encapsulation**: Each layer (Linguistic, Numeric, Geometric, Bound, Symbolic) encapsulates its transformation logic
2. **Abstraction**: `Transform` trait abstracts the concept of a layer operation
3. **Composition**: Layers compose smaller operations (lexer → parser → IR)
4. **Polymorphism**: Same `transform()` call works across all layer types

```rust
// Pipeline as OOP flow
pub struct Pipeline {
    layers: Vec<Box<dyn Transform>>,  // Polymorphic layer collection
}

impl Pipeline {
    pub fn execute(&self, source: &str) -> Result<CompiledOutput> {
        // Encapsulated: Users don't see intermediate representations
        let ir = self.parse(source)?;
        self.layers.iter().try_fold(ir, |acc, layer| {
            layer.transform(acc)  // Polymorphic dispatch
        })
    }
}
```

## Production-Ready Features

The Cargo.toml is optimized for production deployment (K8s via Helm/Podman):

- **Dependencies**: Core compilation stack (inkwell for LLVM, logos for lexer, lalrpop for parser)
- **Features**: Toggle `native-compile` for LLVM backend in production
- **Release Profile**: 
  - `lto = true`: Link-time optimization for smaller binaries
  - `codegen-units = 1`: Maximum optimization at expense of compile time
  - `strip = true`: Remove debug symbols
  - `opt-level = 3`: Full optimization
- **Dev Profile**: 
  - `opt-level = 1`: Fast compilation with basic optimization
  - `debug = true`: Keep debug info for proof validation and bounded checks

This configuration makes FlameLang suitable for:
- Container deployment (small, optimized binaries)
- Development iteration (fast debug builds)
- Formal verification (debug symbols preserve proof information)
