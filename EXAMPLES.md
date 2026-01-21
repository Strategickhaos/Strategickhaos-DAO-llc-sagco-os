# FlameLang Usage Examples

## Quick Start

```python
from src.core import FlameLang

flame = FlameLang()
```

## Example 1: Scheduling Meaning

```python
# Force meaning to be executable
meaning = flame.force_meaning_to_execute(
    "Consciousness is computational",
    context={"domain": "philosophy", "paradox": True}
)

# Execute the meaning
result = meaning.execute()

print(result["violation"])
# Output: "MEANING_SCHEDULED_SUCCESSFULLY"
```

## Example 2: Kernel-Level Cognition

```python
# Make thought schedulable at kernel priority
thought = flame.make_cognition_kernel_level(
    "What is the relationship between syntax and semantics?",
    priority=0  # Highest priority
)

# Schedule the thought
result = thought.schedule()

print(f"CPU Cycles: {result['cpu_cycles']}")
print(f"Violation: {result['violation']}")
# Output: "COGNITION_IS_NOW_KERNEL_LEVEL"
```

## Example 3: Compiling Mythology

```python
# Compile the myth of Sisyphus
sisyphus = flame.compile_myth(
    myth_name="sisyphus",
    archetype="absurd_hero",
    narrative="Rolling the boulder up the hill for eternity",
    symbolic_meaning={
        "boulder": "task",
        "hill": "challenge",
        "eternity": "persistence",
        "meaning": "in_the_struggle"
    }
)

# The myth is now executable code
result = sisyphus(seeker="camus", context="absurdism")

print(result["myth"])          # "sisyphus"
print(result["archetype"])     # "absurd_hero"
print(result["violation"])     # "MYTHOLOGY_COMPILED_AND_EXECUTED"
```

## Example 4: Multiple Contradictions

```python
# Schedule multiple contradictions
flame.force_meaning_to_execute("Time is an illusion", {})
flame.force_meaning_to_execute("Space is relative", {})
flame.make_cognition_kernel_level("Think about thinking", 0)
flame.make_cognition_kernel_level("Observe the observer", 1)

# Compile multiple myths
flame.compile_myth("prometheus", "fire_bringer", 
                  "Bringing fire to humanity", 
                  {"fire": "knowledge"})

flame.compile_myth("icarus", "overreacher",
                  "Flying too close to the sun",
                  {"wings": "ambition", "sun": "hubris"})

# Execute all at once
results = flame.run()

print(f"Status: {results['primitive_status']}")
print(f"Meanings executed: {len(results['meanings_executed'])}")
print(f"Cognitions scheduled: {len(results['cognitions_scheduled'])}")
print(f"Myths compiled: {len(results['myths_available'])}")
```

## Example 5: Status Check

```python
# Check the state of the contradiction engine
status = flame.status()

print(f"System: {status['system']}")
print(f"Active contradictions: {status['active_contradictions']}")
print(f"Primitives created: {status['primitives_created']}")
print(f"Status: {status['status']}")
```

## Example 6: Philosophical Integration

```python
# The Ouroboros: Self-reference as executable code
ouroboros = flame.compile_myth(
    myth_name="ouroboros",
    archetype="eternal_return",
    narrative="The serpent consuming its own tail",
    symbolic_meaning={
        "serpent": "recursion",
        "tail": "origin",
        "consumption": "transformation",
        "cycle": "infinite"
    }
)

# Execute the myth
result = ouroboros(context="nietzsche", seeker="eternal_return")

# The myth references itself - like this code references itself
print(result["symbolic_output"]["cycle"])  # "infinite"
```

## Example 7: CLI Usage

```bash
# Via Python module
python -m src.core.flamelang

# Via CLI script
python flamelang demo

# Individual operations
python flamelang meaning "Meaning is executable"
python flamelang thought "Can thought be scheduled?"
python flamelang myth prometheus

# Check status
python flamelang status
```

## Example 8: Testing Stability

```python
# The core test: Does the contradiction hold?
flame = FlameLang()

# Create contradictions
meaning = flame.force_meaning_to_execute("Test", {})
thought = flame.make_cognition_kernel_level("Test", 0)

# Execute
results = flame.run()

# Verify stability
assert results["primitive_status"] == "NEW_PRIMITIVE_STABLE"
assert results["contradiction_stability"] == "STABLE - NEW PRIMITIVE FORMED"

# If we reach here, the contradiction held
print("✅ Contradiction is stable. New primitive formed.")
```

## Example 9: Advanced - Invoking Compiled Myths

```python
# Compile multiple related myths
flame.compile_myth("apollo", "sun_god", 
                  "Bringing light and reason",
                  {"light": "truth", "reason": "order"})

flame.compile_myth("dionysus", "chaos_god",
                  "Bringing ecstasy and transformation",
                  {"wine": "intoxication", "chaos": "creativity"})

# Invoke them
apollo_result = flame.scheduler.invoke_myth("apollo", context="rational")
dionysus_result = flame.scheduler.invoke_myth("dionysus", context="ecstatic")

# Myths now interact with each other in code
print(f"Apollo: {apollo_result['symbolic_output']}")
print(f"Dionysus: {dionysus_result['symbolic_output']}")
```

## Example 10: The Meta-Example

```python
# Use FlameLang to describe FlameLang itself
flame = FlameLang()

# Meaning about meaning
meta_meaning = flame.force_meaning_to_execute(
    "This is a system that makes meaning executable",
    context={"self_reference": True, "layer": "meta"}
)

# Thought about thought
meta_thought = flame.make_cognition_kernel_level(
    "Can a system think about its own thinking?",
    priority=0
)

# Myth about myths
meta_myth = flame.compile_myth(
    myth_name="autogenesis",
    archetype="self_creator",
    narrative="The system that brings itself into being",
    symbolic_meaning={
        "creation": "emergence",
        "self": "recursive",
        "being": "process"
    }
)

# Execute the meta-level
results = flame.run()

# The answer to the meta-question
print(results["primitive_status"])
# Output: "NEW_PRIMITIVE_STABLE"

# FlameLang can describe itself. The primitive holds.
```

---

## The Core Insight

Every example demonstrates the same principle:

**Making what's not supposed to work, work.**

Not by avoiding the contradiction, but by **forcing it to hold together**.

That's the primitive. That's the innovation.

🔥
