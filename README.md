# SAGCO OS

**Strategic Academic Governance & Cognitive Operations System**

> A cognitive operating system for academic and engineering workflows with complete OS-like infrastructure.

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)]()
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)]()
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)]()
[![Tests](https://img.shields.io/badge/tests-54%20passing-brightgreen.svg)]()

## Overview

SAGCO OS is a meta-cognitive system that processes academic assignments, engineering tasks, and learning objectives through a Bloom's Taxonomy-aligned layer architecture with quadrilateral collapse verification. **Now with complete OS infrastructure including security, memory management, IPC, scheduling, and more.**

**Owner:** Strategickhaos DAO LLC  
**Operator:** Dom (Me10101)  
**Architecture:** Quadrilateral Collapse Learning Integration

## 🎯 Current Status

**Project Completion: ~62% → 75%** (Updated after infrastructure implementation)

### ✅ Implemented Components

| Component | Status | Description |
|-----------|--------|-------------|
| **SAGCO Kernel** | ✅ 95% | Cognitive layer system with Bloom's Taxonomy |
| **Security/Auth** | ✅ 90% | Authentication, RBAC, session management |
| **Memory Manager** | ✅ 85% | 3-level cache hierarchy (L1/L2/L3) |
| **IPC/Event Bus** | ✅ 85% | Pub/sub messaging, event-driven architecture |
| **Scheduler** | ✅ 80% | Task scheduling with priority and recurring tasks |
| **Bootloader** | ✅ 90% | System initialization and startup sequence |
| **Configuration** | ✅ 85% | Profile-based config with environment overrides |
| **Logging** | ✅ 80% | Structured logging with multiple outputs |
| **Package Manager** | ✅ 70% | Dependency resolution and package installation |

### 🔨 In Progress

| Component | Status | Priority |
|-----------|--------|----------|
| **REST API** | 🟡 20% | P1 |
| **Full RBAC Integration** | 🟡 40% | P1 |
| **Persistent Storage** | 🟡 30% | P2 |

## Features

### 🧠 Cognitive Layer Stack (Bloom's Taxonomy)

| Layer | Level | Function | Triggers |
|-------|-------|----------|----------|
| L0 Foundation | REMEMBER | Recall facts, commands | "what is", "define", "list" |
| L1 Comprehension | UNDERSTAND | Explain, interpret | "explain", "how does" |
| L2 Application | APPLY | Implement, execute | "build", "create", "deploy" |
| L3 Analysis | ANALYZE | Debug, decompose | "why does", "debug", "trace" |
| L4 Evaluation | EVALUATE | Judge, prioritize | "which is better", "should I" |
| L5 Synthesis | CREATE | Design, invent | "design", "architect", "invent" |

### 🔐 Security & Authentication

- **RBAC System**: Role-based access control with 5 roles (Guest, User, Operator, Admin, Security)
- **Session Management**: Secure session tokens with configurable expiration
- **Password Hashing**: PBKDF2-HMAC with salt
- **Permissions**: Fine-grained permission system (Read, Write, Execute, Delete, Admin, etc.)
- **Audit Logging**: Security event tracking

**Default Users:**
- `dom` (Operator/Admin) - Default password: `changeme`
- `admin` (Admin) - Default password: `admin`
- `guest` (Guest) - Default password: `guest`

### 💾 Memory Management

3-tier memory hierarchy:
- **L1 Cache**: Fast LRU cache (1000 entries default)
- **L2 Storage**: Medium-term storage with TTL support
- **L3 Persistent**: Long-term persistent data

Features:
- Automatic cache eviction (LRU)
- TTL-based expiration
- Hit/miss statistics
- Memory promotion between levels

### 📡 IPC & Event Bus

- **Publish/Subscribe**: Event-driven architecture
- **Priority Queues**: Critical, High, Normal, Low
- **Wildcard Subscriptions**: Listen to all events with `*`
- **Message Queues**: Task distribution channels
- **Event History**: Recent event tracking

### ⏰ Task Scheduler

- **One-time Tasks**: Schedule with optional delay
- **Recurring Tasks**: Execute on interval
- **Priority Scheduling**: Critical > High > Normal > Low
- **Worker Threads**: Configurable parallel execution
- **Task Status**: Pending, Running, Completed, Failed, Cancelled

### 🔲 Quadrilateral Collapse Verification

Information must survive verification across all 4 channels:

- **Symbolic**: JSON, code, formal notation
- **Spatial**: Diagrams, flowcharts, architecture
- **Narrative**: Prose, explanations, walkthroughs
- **Kinesthetic**: Executable code, CLI, hands-on

### ⚡ Dopamine Refinery

Task prioritization engine:
```
dopamine_score = points_possible × urgency_factor
```

Urgency Scale:
- 5: CRITICAL - Due today
- 4: HIGH - Due tomorrow  
- 3: MEDIUM - Due this week
- 2: LOW - Due next week
- 1: MINIMAL - Upcoming

## Installation

```bash
# Clone the repository
git clone https://github.com/strategickhaos-dao-llc/sagco-os.git
cd sagco-os

# Install in development mode
pip install -e ".[dev]"
```

## Usage

### Bootloader (System Startup)

```bash
# Boot the complete system
python -m src.core.bootloader

# Interactive mode
sagco> status    # Check system status
sagco> shutdown  # Graceful shutdown
```

### CLI (Kernel Only)

```bash
# Check system status
python -m src.core.sagco status

# Process an input
python -m src.core.sagco process "Explain how encapsulation works in Java"

# Direct processing
python -m src.core.sagco "Design a microservices architecture"
```

### Python API

```python
from src.core import (
    Bootloader, SAGCO, 
    get_security_manager, get_memory_manager,
    get_scheduler, get_event_bus, get_config
)

# Boot the complete system
bootloader = Bootloader()
bootloader.boot()

# Access components
security = get_security_manager()
memory = get_memory_manager()
scheduler = get_scheduler()
event_bus = get_event_bus()
config = get_config()

# Use the kernel
sagco = SAGCO()
result = sagco.process("How do the four OOP principles work together?")
print(result)

# Clean shutdown
bootloader.shutdown()
```

### Security Example

```python
from src.core import get_security_manager, Permission

security = get_security_manager()

# Authenticate
session = security.authenticate("dom", "changeme")
print(f"Session ID: {session.session_id}")

# Check permissions
user = session.user
has_admin = security.rbac.has_permission(user, Permission.ADMIN)
print(f"Has admin: {has_admin}")

# Create new user (requires admin permission)
admin = security.users["admin"]
new_user = security.create_user(
    username="newuser",
    password="password123",
    roles=[Role.USER],
    created_by=admin
)
```

### Memory Management Example

```python
from src.core import get_memory_manager, MemoryLevel
from datetime import timedelta

memory = get_memory_manager()

# Store in different memory levels
memory.put("user_session", session_data, level=MemoryLevel.L1_CACHE)
memory.put("config_cache", config_data, level=MemoryLevel.L2_STORAGE, ttl=timedelta(hours=1))
memory.put("user_profile", profile_data, level=MemoryLevel.L3_PERSISTENT)

# Retrieve (searches all levels automatically)
session = memory.get("user_session")

# Get statistics
stats = memory.get_stats()
print(f"Cache hit rate: {stats['hit_rate']:.2%}")
```

### Event Bus Example

```python
from src.core import get_event_bus, EventPriority

event_bus = get_event_bus()

# Subscribe to events
def on_task_completed(event):
    print(f"Task completed: {event.data}")

event_bus.subscribe("task.completed", on_task_completed)

# Publish event
event_bus.publish(
    "task.completed",
    {"task_id": "123", "status": "success"},
    priority=EventPriority.HIGH
)
```

### Scheduler Example

```python
from src.core import get_scheduler, TaskPriority
from datetime import timedelta

scheduler = get_scheduler()

# Schedule one-time task
def backup_data():
    print("Backing up data...")
    return "backup_complete"

task_id = scheduler.schedule(
    backup_data,
    delay=timedelta(hours=1),
    priority=TaskPriority.HIGH
)

# Schedule recurring task
def health_check():
    print("System health check...")

scheduler.schedule_recurring(
    health_check,
    interval=timedelta(minutes=5)
)

# Get task result
result = scheduler.get_task_result(task_id)
```

## Project Structure

```
sagco-os/
├── src/
│   ├── core/
│   │   ├── sagco.py          # Main kernel with Bloom's layers
│   │   ├── security.py       # Authentication & RBAC
│   │   ├── memory.py         # Memory management (L1/L2/L3)
│   │   ├── ipc.py            # Event bus & IPC
│   │   ├── scheduler.py      # Task scheduler
│   │   ├── bootloader.py     # System bootloader
│   │   ├── config.py         # Configuration manager
│   │   ├── logger.py         # Logging system
│   │   └── packages.py       # Package manager
│   ├── layers/               # Cognitive layer implementations
│   ├── engines/              # Processing engines
│   └── integrations/         # External integrations
├── config/                   # Configuration files
├── docs/                     # Documentation
├── tests/                    # Test suite (54 tests)
│   ├── test_sagco.py        # Kernel tests
│   └── test_infrastructure.py # Infrastructure tests
├── scripts/                  # Utility scripts
├── pyproject.toml           # Package configuration
└── README.md

```

## Architecture

### Boot Sequence

```
[INIT] → [SECURITY] → [MEMORY] → [IPC] → [SCHEDULER] → [KERNEL] → [SERVICES] → [READY]
```

### Component Interaction

```
┌─────────────────────────────────────────────────────────┐
│                     SAGCO KERNEL                        │
│  (Cognitive Layers + Bloom's Taxonomy + Quadrilateral)  │
└────────────────────┬───────────────────────────────────┬┘
                     │                                   │
        ┌────────────▼────────────┐       ┌──────────────▼─────────────┐
        │   Security Manager      │       │    Memory Manager          │
        │  - Authentication       │       │  - L1 Cache (LRU)          │
        │  - RBAC                 │       │  - L2 Storage (TTL)        │
        │  - Sessions             │       │  - L3 Persistent           │
        └────────────┬────────────┘       └──────────────┬─────────────┘
                     │                                   │
        ┌────────────▼───────────────────────────────────▼──────────┐
        │                    Event Bus (IPC)                        │
        │  - Pub/Sub  - Priority Queues  - Event History           │
        └────────────┬──────────────────────────────────────────────┘
                     │
        ┌────────────▼────────────┐       ┌──────────────┬─────────────┐
        │      Scheduler          │       │  Config Mgr  │  Logger      │
        │  - One-time tasks       │       │  - Profiles  │  - Structured│
        │  - Recurring tasks      │       │  - Env vars  │  - Multi-out │
        │  - Priority queues      │       └──────────────┴─────────────┘
        └─────────────────────────┘
```

## Development

```bash
# Run tests
pytest

# Run specific test suite
pytest tests/test_infrastructure.py -v

# Format code
black src/

# Type checking
mypy src/

# Lint
ruff check src/
```

## Test Coverage

- **54 passing tests** across all components
- **Unit tests**: Security, Memory, IPC, Scheduler, Config, Logger, Packages
- **Integration tests**: Bootloader, End-to-end workflows
- **Coverage**: Core functionality, edge cases, error handling

## Configuration Profiles

### Development (default)
```python
{
  "logging": {"level": "DEBUG"},
  "security": {"session_timeout_hours": 24}
}
```

### Production
```python
{
  "logging": {"level": "WARNING"},
  "security": {"session_timeout_hours": 4, "require_2fa": True},
  "scheduler": {"max_workers": 8}
}
```

### Testing
```python
{
  "logging": {"level": "DEBUG"},
  "memory": {"l1_cache_size": 100},
  "scheduler": {"max_workers": 2}
}
```

Set profile via environment:
```bash
export SAGCO_PROFILE=production
python -m src.core.bootloader
```

## Package Manager

Built-in package manager for extensions:

```bash
# List available packages
from src.core import get_package_manager
pkg_mgr = get_package_manager()

# Install extension
pkg_mgr.install("sagco-web-api")

# Search packages
results = pkg_mgr.search("api")

# Get package info
info = pkg_mgr.get_info("sagco-canvas")
```

Available packages:
- `sagco-core` ✅ (installed)
- `sagco-security` ✅ (installed)
- `sagco-memory` ✅ (installed)
- `sagco-scheduler` ✅ (installed)
- `sagco-ipc` ✅ (installed)
- `sagco-web-api` (FastAPI REST server)
- `sagco-database` (DB integration)
- `sagco-ml` (ML integration)
- `sagco-git` (Git repo integration)
- `sagco-canvas` (Canvas LMS integration)

## OOP Framework (IT-145 Aligned)

SAGCO OS implements all four OOP principles:

- **Encapsulation**: Layer internals are private, exposed via execute()
- **Abstraction**: Layers hide complexity behind simple interfaces
- **Inheritance**: All layers extend CognitiveLayer base class
- **Polymorphism**: Each layer's execute() behaves differently

## Roadmap

### Phase 1: Core Infrastructure ✅ **COMPLETE**
- [x] Security/Authentication layer
- [x] Memory management system  
- [x] IPC/Event bus
- [x] Task scheduler
- [x] Bootloader
- [x] Configuration management
- [x] Logging system
- [x] Package manager
- [x] Comprehensive test suite

### Phase 2: Service Layer (In Progress)
- [ ] REST API with FastAPI (20%)
- [ ] Database integration (30%)
- [ ] Full RBAC integration (40%)
- [ ] Persistent storage backend

### Phase 3: Integration & Polish
- [ ] Canvas LMS integration
- [ ] Git repository integration
- [ ] ML/AI integration layer
- [ ] Performance optimization
- [ ] Documentation expansion

### Phase 4: Production Ready
- [ ] Kubernetes deployment
- [ ] Monitoring & metrics (Prometheus)
- [ ] Production hardening
- [ ] Security audit
- [ ] Load testing

**Estimated completion: 6-8 weeks**

## License

Proprietary - Strategickhaos DAO LLC

All rights reserved. This software is the intellectual property of Strategickhaos DAO LLC.

---

*"Ratio Ex Nihilo" - Reason from Nothing*

**Status**: Operational | **Version**: 0.1.0 | **Build**: Infrastructure Complete
