//! FlameLang Compiler Binary
//!
//! This is the main entry point for the FlameLang compiler (`flamec`).
//! It demonstrates the full compilation pipeline with all 5 layers.

use flamelang::{FlameType, Pipeline, IdentityTransform, ScaleTransform, Transform};

fn main() {
    println!("FlameLang Compiler v2.0.0");
    println!("Physics-native programming language with 5-layer transformation pipeline");
    println!();
    
    // Demonstrate OOP principles in action
    demonstrate_encapsulation();
    demonstrate_abstraction();
    demonstrate_composition();
    demonstrate_polymorphism();
    
    // Run example compilation
    example_compilation();
}

/// Demonstrate Encapsulation: Data hiding through private fields
fn demonstrate_encapsulation() {
    println!("=== Encapsulation Demo ===");
    
    // FlameType encapsulates angle normalization
    let angle = FlameType::new_angle(7.0);  // > 2π, will be normalized
    println!("Created angle (input 7.0 rad): {:?}", angle);
    
    // Bounded type encapsulates validation
    match FlameType::new_bounded(5.0, 0.0, 10.0) {
        Ok(bounded) => println!("Created bounded value: {:?}", bounded),
        Err(e) => println!("Bound error: {}", e),
    }
    
    println!();
}

/// Demonstrate Abstraction: Focus on "what", not "how"
fn demonstrate_abstraction() {
    println!("=== Abstraction Demo ===");
    
    // Transform trait abstracts the concept of transformation
    let transform = IdentityTransform;
    let input = FlameType::Integer(42);
    
    println!("Transform: {}", transform.name());
    println!("Input: {:?}", input);
    
    match transform.apply(&input) {
        Ok(output) => println!("Output: {:?}", output),
        Err(e) => println!("Error: {}", e),
    }
    
    println!();
}

/// Demonstrate Composition: Building complex behavior from simple parts
fn demonstrate_composition() {
    println!("=== Composition Demo ===");
    
    // Pipeline composes multiple transforms
    let mut pipeline = Pipeline::new("Example Pipeline".to_string());
    pipeline.add_layer(IdentityTransform);
    pipeline.add_layer(ScaleTransform { factor: 2.0 });
    pipeline.add_layer(ScaleTransform { factor: 3.0 });
    
    println!("Pipeline '{}' with {} layers", pipeline.name, pipeline.layer_count());
    
    let input = FlameType::Integer(5);
    println!("Input: {:?}", input);
    
    match pipeline.execute(input) {
        Ok(output) => println!("Output after 3 layers: {:?}", output),
        Err(e) => println!("Error: {}", e),
    }
    
    println!();
}

/// Demonstrate Polymorphism: Same interface, different behavior
fn demonstrate_polymorphism() {
    println!("=== Polymorphism Demo ===");
    
    // Same transform.apply() call works on different types
    let scale = ScaleTransform { factor: 2.0 };
    
    let inputs = vec![
        ("Integer", FlameType::Integer(10)),
        ("Angle", FlameType::new_angle(std::f64::consts::PI / 4.0)),
        ("Vector", FlameType::Vector(vec![1.0, 2.0, 3.0])),
    ];
    
    for (name, input) in inputs {
        println!("Input type: {}", name);
        println!("  Before: {:?}", input);
        
        match scale.apply(&input) {
            Ok(output) => println!("  After:  {:?}", output),
            Err(e) => println!("  Error: {}", e),
        }
    }
    
    println!();
}

/// Example compilation demonstrating the 5-layer pipeline concept
fn example_compilation() {
    println!("=== 5-Layer Pipeline Example ===");
    println!("FlameLang's architecture mirrors Saupe's random fractals:");
    println!("Simple source → Iterative transforms → Complex output");
    println!();
    
    // Simulated 5-layer pipeline
    // In production, these would be: Linguistic, Numeric, Geometric, Bound, Symbolic
    let mut pipeline = Pipeline::new("5-Layer Flamelang Pipeline".to_string());
    
    // Layer 1: Linguistic (lexing/parsing) - simulated as identity
    pipeline.add_layer(IdentityTransform);
    
    // Layer 2: Numeric (type inference) - simulated as identity
    pipeline.add_layer(IdentityTransform);
    
    // Layer 3: Geometric (angle/vector ops) - simulated as scale
    pipeline.add_layer(ScaleTransform { factor: 1.5 });
    
    // Layer 4: Bound (validation) - simulated as identity
    pipeline.add_layer(IdentityTransform);
    
    // Layer 5: Symbolic (codegen) - simulated as final scale
    pipeline.add_layer(ScaleTransform { factor: 2.0 });
    
    println!("Pipeline: {}", pipeline.name);
    println!("Layers: {}", pipeline.layer_count());
    println!();
    
    // Example source value (in production, this would be parsed source code)
    let source = FlameType::Integer(10);
    println!("Source value: {:?}", source);
    
    // Execute pipeline
    match pipeline.execute(source) {
        Ok(result) => {
            println!("Compiled result: {:?}", result);
            println!();
            println!("✓ Compilation successful!");
            println!("Fractal dimension D ≈ 1.55 (H=0.45)");
            println!("Simple input → Complex physics/DNA computation");
        }
        Err(e) => {
            println!("Compilation error: {}", e);
        }
    }
    
    println!();
    println!("For detailed OOP explanations, see: OOP_PRINCIPLES.md");
    println!("For fractal theory correlation, see: FRACTAL_THEORY.md");
}
