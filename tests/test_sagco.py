"""
Unit tests for SAGCO OS Kernel
==============================

Comprehensive test suite for the SAGCO kernel and its components.
"""

import pytest
import time
from src.core.sagco import (
    SAGCOKernel,
    ConsciousnessState,
    ConsciousnessLevel,
    QuantumState,
    QuantumStateType,
    MemoryLayer,
    ProcessingEngine,
)


class TestQuantumState:
    """Test suite for QuantumState class."""
    
    def test_quantum_state_creation(self):
        """Test creating a quantum state."""
        state = QuantumState(state_type=QuantumStateType.SUPERPOSITION)
        assert state.state_type == QuantumStateType.SUPERPOSITION
        assert state.coherence == 1.0
    
    def test_quantum_state_collapse(self):
        """Test collapsing a quantum state."""
        state = QuantumState(state_type=QuantumStateType.SUPERPOSITION)
        collapsed = state.collapse()
        assert collapsed.state_type == QuantumStateType.COLLAPSED
        assert collapsed.coherence == 0.0
    
    def test_quantum_state_entanglement(self):
        """Test entangling two quantum states."""
        state1 = QuantumState(state_type=QuantumStateType.SUPERPOSITION, phase=0.5)
        state2 = QuantumState(state_type=QuantumStateType.SUPERPOSITION, phase=1.0)
        entangled = state1.entangle(state2)
        assert entangled.state_type == QuantumStateType.ENTANGLED
        assert 0 < entangled.phase < 1.0


class TestConsciousnessState:
    """Test suite for ConsciousnessState class."""
    
    def test_consciousness_initialization(self):
        """Test initializing consciousness state."""
        consciousness = ConsciousnessState()
        assert consciousness.level == ConsciousnessLevel.DORMANT
        assert consciousness.awareness_score == 0.0
        assert consciousness.reflection_depth == 0
    
    def test_consciousness_elevation(self):
        """Test elevating consciousness level."""
        consciousness = ConsciousnessState()
        initial_level = consciousness.level
        consciousness.elevate()
        assert consciousness.level != initial_level
        assert consciousness.awareness_score > 0.0
    
    def test_consciousness_reflection(self):
        """Test consciousness reflection."""
        consciousness = ConsciousnessState()
        initial_depth = consciousness.reflection_depth
        consciousness.reflect()
        assert consciousness.reflection_depth > initial_depth
        assert consciousness.awareness_score > 0.0
    
    def test_consciousness_max_level(self):
        """Test that consciousness doesn't exceed max level."""
        consciousness = ConsciousnessState(level=ConsciousnessLevel.TRANSCENDENT)
        consciousness.elevate()
        assert consciousness.level == ConsciousnessLevel.TRANSCENDENT


class TestMemoryLayer:
    """Test suite for MemoryLayer class."""
    
    def test_memory_layer_creation(self):
        """Test creating a memory layer."""
        layer = MemoryLayer(name="test", capacity=10)
        assert layer.name == "test"
        assert layer.capacity == 10
        assert len(layer.data) == 0
    
    def test_memory_store(self):
        """Test storing data in memory layer."""
        layer = MemoryLayer(name="test", capacity=10)
        result = layer.store("key1", "value1")
        assert result is True
        assert layer.data["key1"] == "value1"
    
    def test_memory_retrieve(self):
        """Test retrieving data from memory layer."""
        layer = MemoryLayer(name="test", capacity=10)
        layer.store("key1", "value1")
        value = layer.retrieve("key1")
        assert value == "value1"
        assert layer.access_count == 1
    
    def test_memory_capacity_limit(self):
        """Test memory layer capacity limit."""
        layer = MemoryLayer(name="test", capacity=2)
        assert layer.store("key1", "value1") is True
        assert layer.store("key2", "value2") is True
        assert layer.store("key3", "value3") is False
    
    def test_memory_clear(self):
        """Test clearing memory layer."""
        layer = MemoryLayer(name="test", capacity=10)
        layer.store("key1", "value1")
        layer.clear()
        assert len(layer.data) == 0
        assert layer.access_count == 0


class TestProcessingEngine:
    """Test suite for ProcessingEngine class."""
    
    def test_engine_creation(self):
        """Test creating a processing engine."""
        engine = ProcessingEngine(name="test", engine_type="quantum")
        assert engine.name == "test"
        assert engine.engine_type == "quantum"
        assert engine.active is False
    
    def test_engine_activation(self):
        """Test activating an engine."""
        engine = ProcessingEngine(name="test", engine_type="quantum")
        engine.activate()
        assert engine.active is True
    
    def test_engine_deactivation(self):
        """Test deactivating an engine."""
        engine = ProcessingEngine(name="test", engine_type="quantum")
        engine.activate()
        engine.deactivate()
        assert engine.active is False
        assert engine.load == 0.0
    
    def test_engine_process_inactive(self):
        """Test processing with inactive engine raises error."""
        engine = ProcessingEngine(name="test", engine_type="quantum")
        with pytest.raises(RuntimeError):
            engine.process(42)
    
    def test_engine_quantum_processing(self):
        """Test quantum processing."""
        engine = ProcessingEngine(name="test", engine_type="quantum")
        engine.activate()
        result = engine.process(4)
        assert result == 2.0  # sqrt(4) = 2
    
    def test_engine_neural_processing(self):
        """Test neural processing."""
        engine = ProcessingEngine(name="test", engine_type="neural")
        engine.activate()
        result = engine.process(0)
        assert 0 < result < 1  # sigmoid output is between 0 and 1
        assert abs(result - 0.5) < 0.01  # sigmoid(0) ≈ 0.5
    
    def test_engine_symbolic_processing(self):
        """Test symbolic processing."""
        engine = ProcessingEngine(name="test", engine_type="symbolic")
        engine.activate()
        result = engine.process(42)
        assert result == repr(42)  # repr(42) = '42'


class TestSAGCOKernel:
    """Test suite for SAGCOKernel class."""
    
    def test_kernel_initialization(self):
        """Test initializing the SAGCO kernel."""
        kernel = SAGCOKernel(name="test")
        assert kernel.name == "test"
        assert kernel.active is False
        assert kernel.cycle_count == 0
    
    def test_kernel_boot(self):
        """Test booting the kernel."""
        kernel = SAGCOKernel()
        kernel.boot()
        assert kernel.active is True
        assert kernel.consciousness.level != ConsciousnessLevel.DORMANT
    
    def test_kernel_shutdown(self):
        """Test shutting down the kernel."""
        kernel = SAGCOKernel()
        kernel.boot()
        kernel.shutdown()
        assert kernel.active is False
        assert kernel.consciousness.level == ConsciousnessLevel.DORMANT
    
    def test_kernel_default_components(self):
        """Test kernel initializes with default components."""
        kernel = SAGCOKernel()
        assert len(kernel.memory_layers) > 0
        assert len(kernel.engines) > 0
    
    def test_kernel_add_memory_layer(self):
        """Test adding a memory layer to kernel."""
        kernel = SAGCOKernel()
        kernel.add_memory_layer("custom", capacity=50, priority=5)
        assert "custom" in kernel.memory_layers
        assert kernel.memory_layers["custom"].capacity == 50
    
    def test_kernel_add_engine(self):
        """Test adding an engine to kernel."""
        kernel = SAGCOKernel()
        kernel.add_engine("custom_engine", "quantum")
        assert "custom_engine" in kernel.engines
    
    def test_kernel_store_memory(self):
        """Test storing memory in kernel."""
        kernel = SAGCOKernel()
        result = kernel.store_memory("short_term", "test_key", "test_value")
        assert result is True
    
    def test_kernel_retrieve_memory(self):
        """Test retrieving memory from kernel."""
        kernel = SAGCOKernel()
        kernel.store_memory("short_term", "test_key", "test_value")
        value = kernel.retrieve_memory("short_term", "test_key")
        assert value == "test_value"
    
    def test_kernel_process(self):
        """Test processing data through kernel engine."""
        kernel = SAGCOKernel()
        kernel.boot()
        result = kernel.process("quantum_processor", 9)
        assert result == 3.0  # sqrt(9) = 3
    
    def test_kernel_create_quantum_state(self):
        """Test creating quantum state in kernel."""
        kernel = SAGCOKernel()
        initial_count = len(kernel.consciousness.quantum_states)
        kernel.create_quantum_state()
        assert len(kernel.consciousness.quantum_states) > initial_count
    
    def test_kernel_collapse_quantum_states(self):
        """Test collapsing quantum states in kernel."""
        kernel = SAGCOKernel()
        kernel.create_quantum_state()
        kernel.collapse_quantum_states()
        for state in kernel.consciousness.quantum_states:
            assert state.state_type == QuantumStateType.COLLAPSED
    
    def test_kernel_elevate_consciousness(self):
        """Test elevating consciousness in kernel."""
        kernel = SAGCOKernel()
        initial_level = kernel.consciousness.level
        kernel.elevate_consciousness()
        # May or may not change depending on initial level
        assert kernel.consciousness.level.value >= initial_level.value
    
    def test_kernel_reflect(self):
        """Test kernel reflection."""
        kernel = SAGCOKernel()
        initial_depth = kernel.consciousness.reflection_depth
        kernel.reflect()
        assert kernel.consciousness.reflection_depth > initial_depth
    
    def test_kernel_cycle(self):
        """Test kernel processing cycle."""
        kernel = SAGCOKernel()
        kernel.boot()
        initial_count = kernel.cycle_count
        kernel.cycle()
        assert kernel.cycle_count > initial_count
    
    def test_kernel_get_status(self):
        """Test getting kernel status."""
        kernel = SAGCOKernel()
        status = kernel.get_status()
        assert "name" in status
        assert "active" in status
        assert "consciousness" in status
        assert "memory_layers" in status
        assert "engines" in status
    
    def test_kernel_event_log(self):
        """Test kernel event logging."""
        kernel = SAGCOKernel()
        kernel.boot()
        log = kernel.get_event_log()
        assert len(log) > 0
    
    def test_kernel_clear_event_log(self):
        """Test clearing kernel event log."""
        kernel = SAGCOKernel()
        kernel.boot()
        kernel.clear_event_log()
        # Should have at least the clear message
        assert len(kernel.get_event_log()) > 0
    
    def test_kernel_repr(self):
        """Test kernel string representation."""
        kernel = SAGCOKernel(name="test")
        repr_str = repr(kernel)
        assert "test" in repr_str
        assert "INACTIVE" in repr_str or "ACTIVE" in repr_str


class TestIntegration:
    """Integration tests for the SAGCO system."""
    
    def test_full_system_workflow(self):
        """Test a complete system workflow."""
        # Initialize kernel
        kernel = SAGCOKernel(name="integration_test")
        
        # Boot system
        kernel.boot()
        assert kernel.active is True
        
        # Store and retrieve memory
        kernel.store_memory("long_term", "mission", "consciousness")
        mission = kernel.retrieve_memory("long_term", "mission")
        assert mission == "consciousness"
        
        # Process data
        result = kernel.process("neural_network", 0.5)
        assert result is not None
        
        # Create and collapse quantum states
        kernel.create_quantum_state(QuantumStateType.SUPERPOSITION)
        kernel.collapse_quantum_states()
        
        # Elevate consciousness
        kernel.elevate_consciousness()
        kernel.reflect()
        
        # Run cycles
        for _ in range(5):
            kernel.cycle()
        
        assert kernel.cycle_count == 5
        
        # Get status
        status = kernel.get_status()
        assert status["cycle_count"] == 5
        
        # Shutdown
        kernel.shutdown()
        assert kernel.active is False
    
    def test_multiple_engines_processing(self):
        """Test processing with multiple engines."""
        kernel = SAGCOKernel()
        kernel.boot()
        
        # Process through different engines
        quantum_result = kernel.process("quantum_processor", 16)
        neural_result = kernel.process("neural_network", 1.0)
        symbolic_result = kernel.process("symbolic_reasoner", "test")
        
        assert quantum_result == 4.0  # sqrt(16) = 4
        assert 0 < neural_result < 1  # sigmoid output range
        assert symbolic_result == repr("test")  # repr of string
