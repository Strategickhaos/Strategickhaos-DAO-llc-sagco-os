"""Tests for SAGCO OS Core"""

import pytest
from src.core.sagco import (
    SAGCO,
    BloomLevel,
    CollapseChannel,
    Context,
    CognitiveLayer,
    FoundationLayer,
    ComprehensionLayer,
    ApplicationLayer,
    AnalysisLayer,
    EvaluationLayer,
    SynthesisLayer,
    QuadrilateralCollapse,
    DopamineRefinery,
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
                bloom_level=BloomLevel.APPLY
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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
