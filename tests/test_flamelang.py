"""Tests for FlameLang - The Primitive Contradiction Engine"""

import pytest
from src.core.flamelang import (
    FlameLang,
    ContradictionScheduler,
    MeaningUnit,
    CognitionProcess,
    MythologicalConstruct,
    ContradictionType,
)


class TestMeaningUnit:
    """Test meaning as a schedulable unit - the first contradiction"""
    
    def test_create_meaning_unit(self):
        """Test creating a unit of schedulable meaning"""
        unit = MeaningUnit(
            semantic_content="Consciousness is computational",
            context={"domain": "philosophy"}
        )
        assert unit.semantic_content == "Consciousness is computational"
        assert unit.context["domain"] == "philosophy"
        assert not unit.executed
    
    def test_execute_meaning(self):
        """Test forcing meaning to execute - the core violation"""
        unit = MeaningUnit(
            semantic_content="Time is an illusion",
            context={"paradox": True}
        )
        result = unit.execute()
        
        assert unit.executed
        assert result["meaning_computed"] == "Time is an illusion"
        assert result["violation"] == "MEANING_SCHEDULED_SUCCESSFULLY"
        assert "context_collapsed" in result


class TestCognitionProcess:
    """Test cognition as a kernel-level process - the second contradiction"""
    
    def test_create_cognition_process(self):
        """Test creating a kernel-level thought"""
        process = CognitionProcess(
            thought_pattern="What is the nature of emergence?",
            priority=0
        )
        assert process.thought_pattern == "What is the nature of emergence?"
        assert process.priority == 0
        assert process.state == "THINKING"
    
    def test_schedule_cognition(self):
        """Test scheduling cognition - the core violation"""
        process = CognitionProcess(
            thought_pattern="Can thought be scheduled?",
            priority=1
        )
        result = process.schedule()
        
        assert process.state == "COMPLETED"
        assert result["thought_scheduled"] == "Can thought be scheduled?"
        assert result["violation"] == "COGNITION_IS_NOW_KERNEL_LEVEL"
        assert result["cpu_cycles"] == 1
    
    def test_multiple_scheduling_cycles(self):
        """Test that cognition can be re-scheduled"""
        process = CognitionProcess("Recursive thought", priority=0)
        
        result1 = process.schedule()
        assert result1["cpu_cycles"] == 1
        
        process.state = "THINKING"  # Reset state
        result2 = process.schedule()
        assert result2["cpu_cycles"] == 2


class TestMythologicalConstruct:
    """Test mythology as executable code - the third contradiction"""
    
    def test_create_mythological_construct(self):
        """Test creating a compilable myth"""
        myth = MythologicalConstruct(
            myth_name="icarus",
            archetype="overreacher",
            narrative="Flying too close to the sun",
            symbolic_meaning={"hubris": "danger", "wings": "ambition"}
        )
        assert myth.myth_name == "icarus"
        assert myth.archetype == "overreacher"
    
    def test_compile_mythology(self):
        """Test compiling mythology to executable code - the core violation"""
        myth = MythologicalConstruct(
            myth_name="sisyphus",
            archetype="absurd_hero",
            narrative="Rolling the boulder eternally",
            symbolic_meaning={"boulder": "task", "hill": "challenge", "eternity": "persistence"}
        )
        
        compiled_myth = myth.compile()
        
        # The compiled myth should be callable
        assert callable(compiled_myth)
        assert compiled_myth.__name__ == "myth_sisyphus"
        
        # Execute the compiled myth
        result = compiled_myth(seeker="camus")
        assert result["myth"] == "sisyphus"
        assert result["violation"] == "MYTHOLOGY_COMPILED_AND_EXECUTED"
        assert result["invoked_with"]["seeker"] == "camus"


class TestContradictionScheduler:
    """Test the scheduler that makes impossibilities repeatable"""
    
    def setup_method(self):
        self.scheduler = ContradictionScheduler()
    
    def test_schedule_meaning(self):
        """Test scheduling meaning for execution"""
        unit = self.scheduler.schedule_meaning(
            "Logic is a subset of meaning",
            context={"field": "semantics"}
        )
        
        assert len(self.scheduler.meaning_queue) == 1
        assert unit.semantic_content == "Logic is a subset of meaning"
    
    def test_schedule_cognition(self):
        """Test scheduling cognition at kernel level"""
        process = self.scheduler.schedule_cognition(
            "Thinking about thinking",
            priority=0
        )
        
        assert len(self.scheduler.cognition_queue) == 1
        assert process.thought_pattern == "Thinking about thinking"
    
    def test_cognition_priority_ordering(self):
        """Test that cognition is scheduled by priority"""
        self.scheduler.schedule_cognition("Low priority thought", priority=5)
        self.scheduler.schedule_cognition("High priority thought", priority=0)
        self.scheduler.schedule_cognition("Medium priority thought", priority=2)
        
        # Queue should be ordered by priority (0 = highest)
        assert self.scheduler.cognition_queue[0].priority == 0
        assert self.scheduler.cognition_queue[1].priority == 2
        assert self.scheduler.cognition_queue[2].priority == 5
    
    def test_compile_mythology(self):
        """Test compiling mythology into the registry"""
        compiled = self.scheduler.compile_mythology(
            myth_name="orpheus",
            archetype="musician",
            narrative="Descending to the underworld for love",
            symbolic_meaning={"music": "transcendence", "descent": "journey"}
        )
        
        assert "orpheus" in self.scheduler.myth_registry
        assert callable(compiled)
    
    def test_invoke_myth(self):
        """Test invoking a compiled myth"""
        self.scheduler.compile_mythology(
            myth_name="athena",
            archetype="wisdom",
            narrative="Born from Zeus's head",
            symbolic_meaning={"wisdom": "strategic", "birth": "unconventional"}
        )
        
        result = self.scheduler.invoke_myth("athena", context="war")
        assert result["myth"] == "athena"
        assert result["violation"] == "MYTHOLOGY_COMPILED_AND_EXECUTED"
    
    def test_invoke_nonexistent_myth_raises_error(self):
        """Test that invoking a non-compiled myth raises error"""
        with pytest.raises(ValueError, match="not compiled"):
            self.scheduler.invoke_myth("nonexistent")
    
    def test_execute_all_contradictions(self):
        """Test executing all scheduled contradictions"""
        # Schedule various contradictions
        self.scheduler.schedule_meaning("First meaning", {})
        self.scheduler.schedule_meaning("Second meaning", {})
        self.scheduler.schedule_cognition("First thought", 0)
        self.scheduler.compile_mythology(
            "test_myth", "tester", "Testing", {"test": "value"}
        )
        
        results = self.scheduler.execute_all()
        
        assert len(results["meanings_executed"]) == 2
        assert len(results["cognitions_scheduled"]) == 1
        assert "test_myth" in results["myths_available"]
        assert results["total_violations"] > 0
        assert results["contradiction_stability"] == "STABLE - NEW PRIMITIVE FORMED"


class TestFlameLang:
    """Test the full FlameLang primitive contradiction engine"""
    
    def setup_method(self):
        self.flame = FlameLang()
    
    def test_initialization(self):
        """Test FlameLang initialization"""
        assert self.flame.VERSION == "0.0.1-contradiction"
        assert isinstance(self.flame.scheduler, ContradictionScheduler)
        assert len(self.flame.primitives_created) == 0
    
    def test_force_meaning_to_execute(self):
        """Test the first primitive: making meaning schedulable"""
        unit = self.flame.force_meaning_to_execute(
            "Computation is a form of meaning-making",
            context={"domain": "cognitive_science"}
        )
        
        assert isinstance(unit, MeaningUnit)
        assert "MEANING_SCHEDULABLE" in self.flame.primitives_created
    
    def test_make_cognition_kernel_level(self):
        """Test the second primitive: making cognition kernel-level"""
        process = self.flame.make_cognition_kernel_level(
            "Does the observer collapse the wave function?",
            priority=0
        )
        
        assert isinstance(process, CognitionProcess)
        assert "COGNITION_KERNEL" in self.flame.primitives_created
    
    def test_compile_myth(self):
        """Test the third primitive: making mythology executable"""
        compiled = self.flame.compile_myth(
            myth_name="hermes",
            archetype="messenger",
            narrative="Guide between worlds",
            symbolic_meaning={"boundary": "permeable", "message": "transformation"}
        )
        
        assert callable(compiled)
        assert "MYTHOLOGY_EXECUTABLE" in self.flame.primitives_created
    
    def test_run_all_contradictions(self):
        """Test running all contradictions together"""
        # Create all three types of contradictions
        self.flame.force_meaning_to_execute("Test meaning", {})
        self.flame.make_cognition_kernel_level("Test thought", 0)
        self.flame.compile_myth("test", "tester", "Test narrative", {"key": "value"})
        
        results = self.flame.run()
        
        assert results["flamelang_version"] == "0.0.1-contradiction"
        assert "MEANING_SCHEDULABLE" in results["primitives_created"]
        assert "COGNITION_KERNEL" in results["primitives_created"]
        assert "MYTHOLOGY_EXECUTABLE" in results["primitives_created"]
        assert results["primitive_status"] == "NEW_PRIMITIVE_STABLE"
    
    def test_status_report(self):
        """Test the FlameLang status report"""
        status = self.flame.status()
        
        assert status["system"] == "FlameLang"
        assert status["version"] == "0.0.1-contradiction"
        assert "active_contradictions" in status
        assert status["status"] == "READY"
    
    def test_contradiction_holds_together(self):
        """
        Test the core question: Does the contradiction hold together 
        long enough to become a new primitive?
        """
        # Schedule contradictions
        self.flame.force_meaning_to_execute("Meaning is executable", {})
        self.flame.make_cognition_kernel_level("Thought is schedulable", 0)
        
        # Execute them
        results = self.flame.run()
        
        # The test: Do the contradictions hold?
        assert results["contradiction_stability"] == "STABLE - NEW PRIMITIVE FORMED"
        assert results["primitive_status"] == "NEW_PRIMITIVE_STABLE"
        assert results["total_violations"] > 0
        
        # If we're here, the contradiction held together
        # We've created a new primitive


class TestIntegration:
    """Integration tests for the complete contradiction engine"""
    
    def test_full_workflow(self):
        """Test the complete workflow of forcing impossibilities to work"""
        flame = FlameLang()
        
        # 1. Schedule meaning
        meaning = flame.force_meaning_to_execute(
            "The map becomes the territory",
            context={"korzybski": True}
        )
        
        # 2. Schedule cognition
        thought = flame.make_cognition_kernel_level(
            "What if categories themselves could compute?",
            priority=0
        )
        
        # 3. Compile mythology
        myth = flame.compile_myth(
            myth_name="ouroboros",
            archetype="eternal_return",
            narrative="The serpent eating its own tail",
            symbolic_meaning={
                "cycle": "recursion",
                "tail": "beginning",
                "mouth": "end",
                "unity": "paradox"
            }
        )
        
        # 4. Execute all
        results = flame.run()
        
        # 5. Verify the violation succeeded
        assert results["primitive_status"] == "NEW_PRIMITIVE_STABLE"
        assert len(results["meanings_executed"]) == 1
        assert len(results["cognitions_scheduled"]) == 1
        
        # 6. Invoke the compiled myth
        myth_result = flame.scheduler.invoke_myth("ouroboros", seeker="nietzsche")
        assert myth_result["violation"] == "MYTHOLOGY_COMPILED_AND_EXECUTED"
        assert myth_result["archetype"] == "eternal_return"
    
    def test_the_smallest_executable_contradiction(self):
        """
        Test: What specific thing is "not supposed to work" that we're forcing to compute?
        Answer: Meaning itself.
        """
        flame = FlameLang()
        
        # The core contradiction: Meaning can't be scheduled
        # But we force it to schedule anyway
        meaning = flame.force_meaning_to_execute(
            "This statement is being executed",
            context={"violation": "meaning_scheduled"}
        )
        
        # Execute it
        result = meaning.execute()
        
        # The violation succeeded
        assert result["violation"] == "MEANING_SCHEDULED_SUCCESSFULLY"
        
        # The smallest executable contradiction: Meaning executing
        # This is the primitive. This is what's "not supposed to work."
        # But it does.


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
