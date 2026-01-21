"""
Tests demonstrating the four core OOP principles in SAGCO OS.

This test suite demonstrates:
1. Encapsulation - Task class with private attributes and public methods
2. Abstraction - CognitiveLayer abstract base class
3. Inheritance - Layer subclasses inheriting from CognitiveLayer
4. Polymorphism - Different layer implementations of execute()
"""

import pytest
from src.core.sagco import (
    Task,
    CognitiveLayer,
    FoundationLayer,
    ComprehensionLayer,
    ApplicationLayer,
    AnalysisLayer,
    EvaluationLayer,
    SynthesisLayer,
    Context,
    BloomLevel,
)


class TestEncapsulation:
    """
    Test encapsulation - bundling data with methods that operate on it
    while restricting direct access to internal details.
    """
    
    def test_task_encapsulates_internal_state(self):
        """Task class encapsulates attributes and exposes them via methods"""
        task = Task("Write unit tests", 25, 4)
        
        # Internal state is private (Python convention with _)
        assert hasattr(task, "_title")
        assert hasattr(task, "_points")
        assert hasattr(task, "_urgency")
        assert hasattr(task, "_status")
        
        # Access is provided through public methods
        assert task.getTitle() == "Write unit tests"
        assert task.getPoints() == 25
        assert task.getUrgency() == 4
        assert task.getStatus() == "pending"
    
    def test_encapsulated_business_logic(self):
        """Internal logic is hidden inside methods"""
        task = Task("Code review", 20, 5)
        
        # calculatePriority() encapsulates the priority calculation logic
        # Users don't need to know how priority is calculated
        priority = task.calculatePriority()
        assert priority == 100  # Internal logic: points * urgency
        
        # The calculation formula is hidden from external code
        # This prevents breaking changes if we modify the formula
    
    def test_state_modification_through_methods(self):
        """State changes happen through controlled methods"""
        task = Task("Deploy application", 35, 5)
        
        # Can't directly set _status (would violate encapsulation)
        # Instead, use public methods that enforce business rules
        assert task.getStatus() == "pending"
        
        task.markInProgress()
        assert task.getStatus() == "in_progress"
        
        task.markComplete()
        assert task.getStatus() == "completed"


class TestAbstraction:
    """
    Test abstraction - focusing on what an object does rather than how it does it.
    Base classes define interfaces without specifying implementation details.
    """
    
    def test_cognitive_layer_provides_abstract_interface(self):
        """CognitiveLayer defines required methods without implementation"""
        # CognitiveLayer is a base class that defines the interface
        layer = FoundationLayer()
        
        # All layers must have these attributes
        assert hasattr(layer, "level")
        assert hasattr(layer, "name")
        assert hasattr(layer, "triggers")
        
        # All layers must implement these methods
        assert hasattr(layer, "matches")
        assert hasattr(layer, "execute")
    
    def test_layers_follow_common_interface(self):
        """All cognitive layers follow the same abstract interface"""
        layers = [
            FoundationLayer(),
            ComprehensionLayer(),
            ApplicationLayer(),
            AnalysisLayer(),
            EvaluationLayer(),
            SynthesisLayer(),
        ]
        
        # All layers have the same interface
        for layer in layers:
            assert isinstance(layer, CognitiveLayer)
            assert hasattr(layer, "matches")
            assert hasattr(layer, "execute")
            assert hasattr(layer, "level")
            assert isinstance(layer.level, BloomLevel)
    
    def test_abstraction_hides_implementation_details(self):
        """Users work with abstract interface, not implementation"""
        context = Context(raw_input="What is encapsulation?")
        layer = FoundationLayer()
        
        # User calls matches() without knowing how it's implemented
        result = layer.matches(context)
        assert isinstance(result, bool)
        
        # User calls execute() without knowing the internal processing
        artifacts = layer.execute(context)
        assert isinstance(artifacts, list)


class TestInheritance:
    """
    Test inheritance - new classes reuse and extend existing code.
    Subclasses inherit features from base class while adding specialization.
    """
    
    def test_layers_inherit_from_cognitive_layer(self):
        """All layer classes inherit from CognitiveLayer base class"""
        layers = [
            FoundationLayer(),
            ComprehensionLayer(),
            ApplicationLayer(),
            AnalysisLayer(),
            EvaluationLayer(),
            SynthesisLayer(),
        ]
        
        # All layers are instances of CognitiveLayer
        for layer in layers:
            assert isinstance(layer, CognitiveLayer)
    
    def test_inherited_attributes_and_methods(self):
        """Subclasses inherit attributes and methods from base class"""
        layer = ApplicationLayer()
        
        # Inherited from CognitiveLayer.__init__
        assert hasattr(layer, "level")
        assert hasattr(layer, "name")
        assert hasattr(layer, "triggers")
        assert hasattr(layer, "modules")
        
        # Inherited method from CognitiveLayer
        context = Context(raw_input="Build a REST API")
        can_match = layer.matches(context)
        assert can_match is True
    
    def test_subclasses_extend_base_functionality(self):
        """Subclasses add specialized behavior while reusing base code"""
        foundation = FoundationLayer()
        comprehension = ComprehensionLayer()
        application = ApplicationLayer()
        
        # Each subclass has different Bloom level (specialized)
        assert foundation.level == BloomLevel.REMEMBER
        assert comprehension.level == BloomLevel.UNDERSTAND
        assert application.level == BloomLevel.APPLY
        
        # But all use the same inherited matching logic
        assert hasattr(foundation, "matches")
        assert hasattr(comprehension, "matches")
        assert hasattr(application, "matches")
    
    def test_inheritance_reduces_code_duplication(self):
        """Common functionality is defined once in base class"""
        # All layers share the same matches() implementation from base class
        # No need to rewrite this logic in each subclass
        
        layers = [FoundationLayer(), ComprehensionLayer(), ApplicationLayer()]
        
        for layer in layers:
            # Same method implementation inherited from CognitiveLayer
            assert callable(layer.matches)
            # Each layer customizes with different triggers
            assert len(layer.triggers) > 0


class TestPolymorphism:
    """
    Test polymorphism - different objects respond differently to the same method call.
    Multiple layer classes implement execute() differently, producing different results.
    """
    
    def test_layers_implement_execute_differently(self):
        """Each layer type implements execute() with different behavior"""
        context = Context(raw_input="Test input")
        
        foundation = FoundationLayer()
        comprehension = ComprehensionLayer()
        application = ApplicationLayer()
        
        # Same method name, different results
        artifacts_1 = foundation.execute(context)
        artifacts_2 = comprehension.execute(context)
        artifacts_3 = application.execute(context)
        
        # All return lists of artifacts (same interface)
        assert isinstance(artifacts_1, list)
        assert isinstance(artifacts_2, list)
        assert isinstance(artifacts_3, list)
        
        # But each produces different artifact types
        assert artifacts_1[0].artifact_type == "definition"
        assert artifacts_2[0].artifact_type == "explanation"
        assert artifacts_3[0].artifact_type == "code"
    
    def test_polymorphic_behavior_with_different_bloom_levels(self):
        """Different layers produce artifacts at different Bloom levels"""
        context = Context(raw_input="Test")
        
        layers = [
            (FoundationLayer(), BloomLevel.REMEMBER),
            (ComprehensionLayer(), BloomLevel.UNDERSTAND),
            (ApplicationLayer(), BloomLevel.APPLY),
            (AnalysisLayer(), BloomLevel.ANALYZE),
            (EvaluationLayer(), BloomLevel.EVALUATE),
            (SynthesisLayer(), BloomLevel.CREATE),
        ]
        
        # Each layer's execute() produces artifacts at its Bloom level
        for layer, expected_level in layers:
            artifacts = layer.execute(context)
            assert artifacts[0].bloom_level == expected_level
    
    def test_polymorphism_enables_flexible_processing(self):
        """Code can work with layers generically without knowing exact type"""
        context = Context(raw_input="Design and build a system")
        
        # List of different layer types
        layers = [
            ApplicationLayer(),
            AnalysisLayer(),
            SynthesisLayer(),
        ]
        
        # Process with each layer without knowing specific type
        results = []
        for layer in layers:
            # Same method call works for all layer types
            if layer.matches(context):
                artifacts = layer.execute(context)
                results.extend(artifacts)
        
        # Different layers produced different results
        assert len(results) > 0
        artifact_types = [a.artifact_type for a in results]
        # At least one layer matched and produced artifacts
        assert len(artifact_types) >= 1
        # All matched layers used the same interface (polymorphism)
        for artifact in results:
            assert hasattr(artifact, "artifact_type")
            assert hasattr(artifact, "bloom_level")


class TestOOPPrinciplesTogether:
    """
    Test how all four OOP principles work together in the system.
    """
    
    def test_complete_oop_workflow(self):
        """Demonstrate all four principles working together"""
        # 1. ENCAPSULATION: Task with private state
        task = Task("Design microservices", 40, 5)
        priority = task.calculatePriority()
        
        # 2. ABSTRACTION: Work with layers through common interface
        layers = [
            FoundationLayer(),
            ComprehensionLayer(),
            ApplicationLayer(),
            SynthesisLayer(),
        ]
        
        # 3. INHERITANCE: All layers inherit from CognitiveLayer
        for layer in layers:
            assert isinstance(layer, CognitiveLayer)
        
        # 4. POLYMORPHISM: Different execute() implementations
        context = Context(raw_input="Design a new architecture")
        results = []
        
        for layer in layers:
            if layer.matches(context):
                artifacts = layer.execute(context)
                results.extend(artifacts)
        
        # System works cohesively using all four principles
        assert priority == 200  # Encapsulation
        assert len(layers) > 0  # Abstraction & Inheritance
        assert len(results) > 0  # Polymorphism
    
    def test_benefits_of_oop_design(self):
        """OOP principles enable modularity and maintainability"""
        # Can add new layer types without changing existing code
        # Can modify Task internal logic without breaking external code
        # Can process different layer types with same code
        
        task = Task("Add new feature", 30, 3)
        context = Context(raw_input="Implement authentication")
        
        # System is modular - components work independently
        assert task.calculatePriority() == 90
        
        # System is extensible - can add new layers
        layers = [ApplicationLayer(), AnalysisLayer()]
        for layer in layers:
            layer.execute(context)
        
        # No errors - system is well-designed with OOP principles


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
