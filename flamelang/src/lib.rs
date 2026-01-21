//! # FlameLang
//!
//! FlameLang is a physics-native programming language with a 5-layer transformation pipeline.
//! It demonstrates Object-Oriented Programming principles in Rust through:
//! - Encapsulation via structs and modules
//! - Abstraction via traits
//! - Composition instead of inheritance
//! - Polymorphism through generics and trait objects
//!
//! ## Architecture
//!
//! The compiler follows a layered approach:
//! 1. **Linguistic Layer**: Lexing and parsing (logos + lalrpop)
//! 2. **Numeric Layer**: Type inference and numeric transformations
//! 3. **Geometric Layer**: Angle and vector operations (unit circle)
//! 4. **Bound Layer**: Constraint validation and proof checking
//! 5. **Symbolic Layer**: Code generation (LLVM IR via inkwell)
//!
//! ## OOP in Rust
//!
//! See `OOP_PRINCIPLES.md` for detailed explanation of how Rust implements
//! encapsulation, abstraction, inheritance-like patterns, and polymorphism.
//!
//! ## Fractal Theory
//!
//! See `FRACTAL_THEORY.md` for correlation with Saupe's random fractals,
//! showing how FlameLang generates complex computations from simple rules.

use thiserror::Error;

/// Errors that can occur during compilation
#[derive(Error, Debug)]
pub enum FlameError {
    #[error("Lexical error: {0}")]
    LexError(String),
    
    #[error("Parse error: {0}")]
    ParseError(String),
    
    #[error("Type error: {0}")]
    TypeError(String),
    
    #[error("Bound check failed: {0}")]
    BoundError(String),
    
    #[error("Codegen error: {0}")]
    CodegenError(String),
}

/// Type system for FlameLang demonstrating OOP principles
///
/// This enum shows:
/// - Encapsulation: Internal representation hidden
/// - Composition: Types compose primitives with constraints
/// - Polymorphism: Different variants, same interface
#[derive(Debug, Clone, PartialEq)]
pub enum FlameType {
    /// Angle on unit circle, always bounded [0, 2π)
    Angle(f64),
    
    /// Vector in n-dimensional space
    Vector(Vec<f64>),
    
    /// Bounded numeric value with constraints
    Bounded { value: f64, min: f64, max: f64 },
    
    /// Integer type
    Integer(i64),
    
    /// Boolean type
    Boolean(bool),
}

impl FlameType {
    /// Create a new Angle, automatically normalizing to [0, 2π)
    pub fn new_angle(radians: f64) -> Self {
        let normalized = radians.rem_euclid(2.0 * std::f64::consts::PI);
        FlameType::Angle(normalized)
    }
    
    /// Create a new bounded value, validating constraints
    pub fn new_bounded(value: f64, min: f64, max: f64) -> Result<Self, FlameError> {
        if value < min || value > max {
            Err(FlameError::BoundError(
                format!("Value {} not in range [{}, {}]", value, min, max)
            ))
        } else {
            Ok(FlameType::Bounded { value, min, max })
        }
    }
}

/// Transform trait - demonstrates abstraction in Rust
///
/// This trait abstracts the concept of a transformation operation.
/// Any type implementing this trait can be used polymorphically
/// in the compilation pipeline.
pub trait Transform {
    /// Apply transformation to a FlameType value
    fn apply(&self, input: &FlameType) -> Result<FlameType, FlameError>;
    
    /// Validate that this transform preserves required bounds
    fn validate_bounds(&self) -> bool {
        true  // Default: assume valid
    }
    
    /// Get the name of this transform (for debugging/logging)
    fn name(&self) -> &str;
}

/// Intermediate Representation - demonstrates encapsulation
///
/// This struct encapsulates the compiler's internal state.
/// External code interacts only through public methods.
#[derive(Debug)]
pub struct FlameIR {
    /// Declarations (private - encapsulated)
    declarations: Vec<String>,
    
    /// Expressions (private - encapsulated)
    expressions: Vec<String>,
    
    /// Type information (private - encapsulated)
    types: Vec<FlameType>,
}

impl FlameIR {
    /// Create a new empty IR
    pub fn new() -> Self {
        FlameIR {
            declarations: Vec::new(),
            expressions: Vec::new(),
            types: Vec::new(),
        }
    }
    
    /// Add a declaration (public interface)
    pub fn add_declaration(&mut self, decl: String) {
        self.declarations.push(decl);
    }
    
    /// Add an expression (public interface)
    pub fn add_expression(&mut self, expr: String) {
        self.expressions.push(expr);
    }
    
    /// Add type information (public interface)
    pub fn add_type(&mut self, ty: FlameType) {
        self.types.push(ty);
    }
    
    /// Get count of declarations (public interface - read-only access)
    pub fn declaration_count(&self) -> usize {
        self.declarations.len()
    }
    
    /// Get count of expressions (public interface - read-only access)
    pub fn expression_count(&self) -> usize {
        self.expressions.len()
    }
}

impl Default for FlameIR {
    fn default() -> Self {
        Self::new()
    }
}

/// Compilation pipeline - demonstrates OOP composition
///
/// This struct composes multiple transformation layers,
/// showing how Rust achieves inheritance-like code reuse
/// through composition rather than class inheritance.
pub struct Pipeline {
    /// Layered transformations (composition)
    layers: Vec<Box<dyn Transform>>,
    
    /// Name of the pipeline
    pub name: String,
}

impl Pipeline {
    /// Create a new pipeline
    pub fn new(name: String) -> Self {
        Pipeline {
            layers: Vec::new(),
            name,
        }
    }
    
    /// Add a transformation layer (demonstrates polymorphism)
    pub fn add_layer<T: Transform + 'static>(&mut self, transform: T) {
        self.layers.push(Box::new(transform));
    }
    
    /// Execute the pipeline (demonstrates polymorphic dispatch)
    pub fn execute(&self, mut value: FlameType) -> Result<FlameType, FlameError> {
        for (idx, layer) in self.layers.iter().enumerate() {
            println!("Applying layer {}: {}", idx, layer.name());
            
            // Validate bounds before applying
            if !layer.validate_bounds() {
                return Err(FlameError::BoundError(
                    format!("Layer {} failed bound validation", layer.name())
                ));
            }
            
            // Apply transformation (polymorphic call)
            value = layer.apply(&value)?;
        }
        
        Ok(value)
    }
    
    /// Get number of layers
    pub fn layer_count(&self) -> usize {
        self.layers.len()
    }
}

/// Example transform: Identity (no-op)
pub struct IdentityTransform;

impl Transform for IdentityTransform {
    fn apply(&self, input: &FlameType) -> Result<FlameType, FlameError> {
        Ok(input.clone())
    }
    
    fn name(&self) -> &str {
        "Identity"
    }
}

/// Example transform: Scale numeric values
pub struct ScaleTransform {
    pub factor: f64,
}

impl Transform for ScaleTransform {
    fn apply(&self, input: &FlameType) -> Result<FlameType, FlameError> {
        match input {
            FlameType::Integer(n) => Ok(FlameType::Integer(((*n as f64) * self.factor) as i64)),
            FlameType::Bounded { value, min, max } => {
                FlameType::new_bounded(value * self.factor, min * self.factor, max * self.factor)
            }
            FlameType::Vector(v) => {
                Ok(FlameType::Vector(v.iter().map(|x| x * self.factor).collect()))
            }
            FlameType::Angle(a) => {
                Ok(FlameType::new_angle(a * self.factor))
            }
            _ => Ok(input.clone()),
        }
    }
    
    fn name(&self) -> &str {
        "Scale"
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_angle_normalization() {
        let angle1 = FlameType::new_angle(0.0);
        let angle2 = FlameType::new_angle(2.0 * std::f64::consts::PI);
        let angle3 = FlameType::new_angle(-std::f64::consts::PI);
        
        // All should normalize correctly
        match angle1 {
            FlameType::Angle(a) => assert!((a - 0.0).abs() < 1e-10),
            _ => panic!("Expected Angle"),
        }
        
        match angle2 {
            FlameType::Angle(a) => assert!(a < 0.1),  // Should wrap to ~0
            _ => panic!("Expected Angle"),
        }
        
        match angle3 {
            FlameType::Angle(a) => assert!(a > std::f64::consts::PI - 0.1),
            _ => panic!("Expected Angle"),
        }
    }
    
    #[test]
    fn test_bounded_validation() {
        let valid = FlameType::new_bounded(5.0, 0.0, 10.0);
        assert!(valid.is_ok());
        
        let invalid = FlameType::new_bounded(15.0, 0.0, 10.0);
        assert!(invalid.is_err());
    }
    
    #[test]
    fn test_pipeline_execution() {
        let mut pipeline = Pipeline::new("test".to_string());
        pipeline.add_layer(IdentityTransform);
        pipeline.add_layer(ScaleTransform { factor: 2.0 });
        
        let input = FlameType::Integer(5);
        let result = pipeline.execute(input).unwrap();
        
        match result {
            FlameType::Integer(n) => assert_eq!(n, 10),
            _ => panic!("Expected Integer"),
        }
    }
    
    #[test]
    fn test_flame_ir_encapsulation() {
        let mut ir = FlameIR::new();
        ir.add_declaration("let x = 5".to_string());
        ir.add_expression("x + 10".to_string());
        
        // Can only access through public interface
        assert_eq!(ir.declaration_count(), 1);
        assert_eq!(ir.expression_count(), 1);
        
        // Cannot directly access ir.declarations (it's private)
    }
}
