"""Tests for SAGCO OS Core"""

import pytest

from src.core.sagco import (
    SAGCO,
    AnalysisLayer,
    ApplicationLayer,
    BloomLevel,
    CollapseChannel,
    ComprehensionLayer,
    Context,
    DopamineRefinery,
    EvaluationLayer,
    FoundationLayer,
    QuadrilateralCollapse,
    SynthesisLayer,
    Task,
)


class TestSAGCO:
    """Test suite for SAGCO kernel"""

    def setup_method(self):
        self.sagco = SAGCO()

    def test_status(self):
        """Test system status report"""
        status = self.sagco.status()
        assert status["system"] == "SAGCO OS"
        assert status["version"] == "0.1.0"
        assert status["status"] == "OPERATIONAL"
        assert len(status["layers"]) == 6

    def test_parse_input_question(self):
        """Test parsing a question"""
        context = self.sagco.parse_input("What is encapsulation?")
        assert context.input_type == "question"
        assert "what is" in context.triggers

    def test_parse_input_assignment(self):
        """Test parsing an assignment"""
        context = self.sagco.parse_input("Complete the discussion post about OOP")
        assert context.input_type == "assignment"

    def test_parse_input_project(self):
        """Test parsing a project request"""
        context = self.sagco.parse_input("Build a REST API for the system")
        assert context.input_type == "project"

    def test_bloom_mapping_remember(self):
        """Test mapping to REMEMBER level"""
        context = self.sagco.parse_input("What is the definition of polymorphism?")
        level = self.sagco.map_to_bloom(context)
        assert level == BloomLevel.REMEMBER

    def test_bloom_mapping_understand(self):
        """Test mapping to UNDERSTAND level"""
        context = self.sagco.parse_input("Explain how inheritance works")
        level = self.sagco.map_to_bloom(context)
        assert level == BloomLevel.UNDERSTAND

    def test_bloom_mapping_apply(self):
        """Test mapping to APPLY level"""
        context = self.sagco.parse_input("Implement a binary search algorithm")
        level = self.sagco.map_to_bloom(context)
        assert level == BloomLevel.APPLY

    def test_bloom_mapping_analyze(self):
        """Test mapping to ANALYZE level"""
        context = self.sagco.parse_input("Debug this memory leak")
        level = self.sagco.map_to_bloom(context)
        assert level == BloomLevel.ANALYZE

    def test_bloom_mapping_evaluate(self):
        """Test mapping to EVALUATE level"""
        context = self.sagco.parse_input("Which database should I use?")
        level = self.sagco.map_to_bloom(context)
        assert level == BloomLevel.EVALUATE

    def test_bloom_mapping_create(self):
        """Test mapping to CREATE level"""
        context = self.sagco.parse_input("Design a new architecture for this system")
        level = self.sagco.map_to_bloom(context)
        assert level == BloomLevel.CREATE

    def test_process_returns_valid_structure(self):
        """Test that process returns expected structure"""
        result = self.sagco.process("Explain OOP principles")
        assert "version" in result
        assert "context" in result
        assert "layers_activated" in result
        assert "artifacts" in result
        assert "collapse" in result
        assert "timestamp" in result


class TestCognitiveLayers:
    """Test individual cognitive layers"""

    def test_foundation_layer_triggers(self):
        layer = FoundationLayer()
        context = Context(raw_input="What is a variable?")
        assert layer.matches(context)

    def test_comprehension_layer_triggers(self):
        layer = ComprehensionLayer()
        context = Context(raw_input="Explain how this works")
        assert layer.matches(context)

    def test_application_layer_triggers(self):
        layer = ApplicationLayer()
        context = Context(raw_input="Build a new component")
        assert layer.matches(context)

    def test_analysis_layer_triggers(self):
        layer = AnalysisLayer()
        context = Context(raw_input="Debug this error")
        assert layer.matches(context)

    def test_evaluation_layer_triggers(self):
        layer = EvaluationLayer()
        context = Context(raw_input="Which is better for this use case?")
        assert layer.matches(context)

    def test_synthesis_layer_triggers(self):
        layer = SynthesisLayer()
        context = Context(raw_input="Design a new system")
        assert layer.matches(context)


class TestQuadrilateralCollapse:
    """Test quadrilateral collapse verification"""

    def test_single_channel_coverage(self):
        from src.core.sagco import Artifact

        artifacts = [
            Artifact(
                artifact_type="code",
                content="test",
                channel=CollapseChannel.KINESTHETIC,
                bloom_level=BloomLevel.APPLY,
            )
        ]
        result = QuadrilateralCollapse.collapse(artifacts)
        assert result["coverage_ratio"] == 0.25
        assert not result["fully_collapsed"]

    def test_full_collapse(self):
        from src.core.sagco import Artifact

        artifacts = [
            Artifact("code", "test", CollapseChannel.KINESTHETIC, BloomLevel.APPLY),
            Artifact("diagram", "test", CollapseChannel.SPATIAL, BloomLevel.ANALYZE),
            Artifact("explanation", "test", CollapseChannel.NARRATIVE, BloomLevel.UNDERSTAND),
            Artifact("json", "test", CollapseChannel.SYMBOLIC, BloomLevel.REMEMBER),
        ]
        result = QuadrilateralCollapse.collapse(artifacts)
        assert result["coverage_ratio"] == 1.0
        assert result["fully_collapsed"]


class TestDopamineRefinery:
    """Test dopamine scoring system"""

    def test_calculate_score(self):
        score = DopamineRefinery.calculate(points=30, urgency=5)
        assert score.dopamine_value == 150
        assert score.points_possible == 30
        assert score.urgency_factor == 5

    def test_prioritize_tasks(self):
        tasks = [
            DopamineRefinery.calculate(20, 2),  # 40
            DopamineRefinery.calculate(30, 5),  # 150
            DopamineRefinery.calculate(35, 3),  # 105
        ]
        prioritized = DopamineRefinery.prioritize(tasks)
        assert prioritized[0].dopamine_value == 150
        assert prioritized[1].dopamine_value == 105
        assert prioritized[2].dopamine_value == 40


class TestTask:
    """Test suite for Task class demonstrating OOP encapsulation"""

    def test_task_initialization(self):
        """Test task is properly initialized"""
        task = Task("Implement OOP principles", 30, 5)
        assert task.getTitle() == "Implement OOP principles"
        assert task.getPoints() == 30
        assert task.getUrgency() == 5
        assert task.getStatus() == "pending"

    def test_calculate_priority(self):
        """Test priority calculation (encapsulated logic)"""
        task = Task("Complete discussion post", 20, 4)
        priority = task.calculatePriority()
        assert priority == 80  # 20 * 4

    def test_mark_complete(self):
        """Test marking task as complete"""
        task = Task("Debug code", 15, 3)
        assert task.getStatus() == "pending"
        task.markComplete()
        assert task.getStatus() == "completed"

    def test_mark_in_progress(self):
        """Test marking task as in progress"""
        task = Task("Write tests", 25, 2)
        assert task.getStatus() == "pending"
        task.markInProgress()
        assert task.getStatus() == "in_progress"

    def test_encapsulation_private_attributes(self):
        """Test that private attributes follow naming convention"""
        task = Task("Test encapsulation", 10, 1)
        # Verify that private attributes are prefixed with underscore
        assert hasattr(task, "_title")
        assert hasattr(task, "_points")
        assert hasattr(task, "_urgency")
        assert hasattr(task, "_status")

    def test_task_repr(self):
        """Test string representation"""
        task = Task("Review PR", 5, 2)
        repr_str = repr(task)
        assert "Review PR" in repr_str
        assert "5" in repr_str
        assert "2" in repr_str
        assert "pending" in repr_str

    def test_multiple_tasks_priority_comparison(self):
        """Test comparing priorities of multiple tasks"""
        task1 = Task("Low priority", 10, 1)
        task2 = Task("High priority", 30, 5)
        task3 = Task("Medium priority", 20, 3)

        assert task2.calculatePriority() > task3.calculatePriority()
        assert task3.calculatePriority() > task1.calculatePriority()
        assert task2.calculatePriority() == 150
        assert task3.calculatePriority() == 60
        assert task1.calculatePriority() == 10

    def test_task_state_transitions(self):
        """Test valid state transitions"""
        task = Task("State test", 15, 2)
        assert task.getStatus() == "pending"

        task.markInProgress()
        assert task.getStatus() == "in_progress"

        task.markComplete()
        assert task.getStatus() == "completed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
