#!/usr/bin/env python3
"""
SAGCO OS Demo Script
Demonstrates all infrastructure components working together
"""

import time
from datetime import timedelta
from src.core import (
    Bootloader,
    SAGCO,
    get_security_manager,
    get_memory_manager,
    get_event_bus,
    get_scheduler,
    get_config,
    get_logger,
    get_package_manager,
    Permission,
    Role,
    MemoryLevel,
    TaskPriority,
)
from src.core.ipc import EventPriority


def demo_banner(title):
    """Print demo section banner"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main():
    """Run comprehensive SAGCO OS demo"""
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              SAGCO OS v0.1.0 - DEMO SCRIPT                ║
║   Strategic Academic Governance & Cognitive Operations    ║
║                                                           ║
║              Owner: Strategickhaos DAO LLC                ║
║              Operator: Dom (Me10101)                      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # ========================================
    # BOOT SEQUENCE
    # ========================================
    demo_banner("1. BOOT SEQUENCE")
    print("Booting SAGCO OS with all infrastructure components...\n")
    
    bootloader = Bootloader()
    success = bootloader.boot()
    
    if not success:
        print("\n❌ Boot failed!")
        return
    
    print("\n✅ Boot successful!")
    
    # ========================================
    # SECURITY & AUTHENTICATION
    # ========================================
    demo_banner("2. SECURITY & AUTHENTICATION")
    
    security = get_security_manager()
    
    print("\n📋 Available users:")
    for username in security.users.keys():
        user_status = security.get_user_status(username)
        print(f"  - {username}: {user_status['roles']}")
    
    print("\n🔐 Authenticating as 'dom'...")
    session = security.authenticate("dom", "changeme")
    print(f"  ✓ Session created: {session.session_id[:16]}...")
    print(f"  ✓ User: {session.user.username}")
    print(f"  ✓ Roles: {[r.name for r in session.user.roles]}")
    
    # Check permissions
    user = session.user
    print(f"\n🔑 Permissions check:")
    print(f"  - Has ADMIN permission: {security.rbac.has_permission(user, Permission.ADMIN)}")
    print(f"  - Has EXECUTE permission: {security.rbac.has_permission(user, Permission.EXECUTE)}")
    
    # ========================================
    # MEMORY MANAGEMENT
    # ========================================
    demo_banner("3. MEMORY MANAGEMENT")
    
    memory = get_memory_manager()
    
    print("\n💾 Storing data in different memory levels:")
    
    # L1 Cache
    memory.put("session_data", {"user": "dom", "active": True}, level=MemoryLevel.L1_CACHE)
    print("  ✓ L1 Cache: session_data")
    
    # L2 Storage with TTL
    memory.put("temp_token", "abc123", level=MemoryLevel.L2_STORAGE, ttl=timedelta(hours=1))
    print("  ✓ L2 Storage: temp_token (expires in 1h)")
    
    # L3 Persistent
    memory.put("user_preferences", {"theme": "dark", "lang": "en"}, level=MemoryLevel.L3_PERSISTENT)
    print("  ✓ L3 Persistent: user_preferences")
    
    # Retrieve
    print("\n📖 Retrieving data:")
    session_data = memory.get("session_data")
    print(f"  ✓ Retrieved: {session_data}")
    
    # Stats
    stats = memory.get_stats()
    print(f"\n📊 Memory stats:")
    print(f"  - L1 size: {stats['l1_size']}")
    print(f"  - L2 size: {stats['l2_size']}")
    print(f"  - L3 size: {stats['l3_size']}")
    print(f"  - Hit rate: {stats['hit_rate']:.0%}")
    
    # ========================================
    # EVENT BUS & IPC
    # ========================================
    demo_banner("4. EVENT BUS & IPC")
    
    event_bus = get_event_bus()
    
    # Track received events
    received_events = []
    
    def event_handler(event):
        received_events.append(event)
        print(f"  📨 Received: {event.event_type} from {event.source}")
    
    print("\n📡 Setting up event subscriptions:")
    event_bus.subscribe("demo.test", event_handler)
    event_bus.subscribe("system.*", event_handler)
    print("  ✓ Subscribed to 'demo.test'")
    print("  ✓ Subscribed to 'system.*'")
    
    print("\n📤 Publishing events:")
    event_bus.publish("demo.test", {"message": "Hello from demo!"}, source="demo_script")
    event_bus.publish("system.health", {"status": "ok"}, source="monitor", priority=EventPriority.HIGH)
    
    time.sleep(0.2)  # Wait for async processing
    
    print(f"\n✅ Processed {len(received_events)} events")
    
    # ========================================
    # TASK SCHEDULER
    # ========================================
    demo_banner("5. TASK SCHEDULER")
    
    scheduler = get_scheduler()
    
    print("\n⏰ Scheduling tasks:")
    
    # Immediate task
    def greet():
        print("    👋 Hello from scheduled task!")
        return "greeting_sent"
    
    task1 = scheduler.schedule(greet, name="Greeting Task")
    print(f"  ✓ Scheduled immediate task: {task1}")
    
    # Delayed task
    def delayed_message():
        print("    ⏳ This message was delayed!")
        return "delayed_complete"
    
    task2 = scheduler.schedule(
        delayed_message,
        name="Delayed Task",
        delay=timedelta(milliseconds=500),
        priority=TaskPriority.HIGH
    )
    print(f"  ✓ Scheduled delayed task (500ms): {task2}")
    
    time.sleep(0.3)
    
    # Check status
    print(f"\n📊 Scheduler stats:")
    stats = scheduler.get_stats()
    print(f"  - Total tasks: {stats['total_tasks']}")
    print(f"  - Completed: {stats['stats']['completed']}")
    print(f"  - Running: {stats['running']}")
    
    time.sleep(0.3)  # Wait for delayed task
    
    # ========================================
    # CONFIGURATION
    # ========================================
    demo_banner("6. CONFIGURATION")
    
    config = get_config()
    
    print(f"\n⚙️  Configuration:")
    print(f"  - Active profile: {config.active_profile}")
    print(f"  - System version: {config.get('system', 'version')}")
    print(f"  - Owner: {config.get('system', 'owner')}")
    print(f"  - Operator: {config.get('system', 'operator')}")
    print(f"  - Log level: {config.get('logging', 'level')}")
    print(f"  - Session timeout: {config.get('security', 'session_timeout_hours')}h")
    
    # ========================================
    # LOGGING
    # ========================================
    demo_banner("7. STRUCTURED LOGGING")
    
    logger = get_logger("demo")
    
    print("\n📝 Logging examples:")
    logger.info("Demo script started", component="demo", version="0.1.0")
    logger.debug("Debug information", details="This is debug level")
    logger.warning("This is a warning", code=404)
    
    print("  ✓ Logged 3 messages")
    
    # ========================================
    # PACKAGE MANAGER
    # ========================================
    demo_banner("8. PACKAGE MANAGER")
    
    pkg_mgr = get_package_manager()
    
    print("\n📦 Installed packages:")
    installed = pkg_mgr.list_installed()
    for pkg in installed:
        print(f"  ✓ {pkg.name} v{pkg.version}")
    
    print(f"\n🔍 Searching for 'api' packages:")
    results = pkg_mgr.search("api")
    for pkg in results[:3]:
        status = "✅ installed" if pkg.installed else "⬜ available"
        print(f"  {status} {pkg.name}: {pkg.description}")
    
    # ========================================
    # SAGCO KERNEL
    # ========================================
    demo_banner("9. SAGCO KERNEL (COGNITIVE LAYERS)")
    
    sagco = SAGCO()
    
    print("\n🧠 Processing cognitive tasks:")
    
    # Test different Bloom levels
    test_inputs = [
        "What is polymorphism?",
        "Explain how inheritance works in Java",
        "Build a REST API endpoint",
        "Debug this memory leak issue",
    ]
    
    for input_text in test_inputs:
        result = sagco.process(input_text)
        print(f"\n  Input: '{input_text}'")
        print(f"  Bloom Level: {result['context']['bloom_level']}")
        print(f"  Layers: {', '.join(result['layers_activated'])}")
        print(f"  Channels: {result['collapse']['channels_covered']}")
    
    # ========================================
    # SYSTEM STATUS
    # ========================================
    demo_banner("10. SYSTEM STATUS")
    
    boot_status = bootloader.get_status()
    
    print(f"\n🖥️  System Information:")
    print(f"  - Version: {boot_status['version']}")
    print(f"  - Boot stage: {boot_status['current_stage']}")
    print(f"  - Boot time: {boot_status['boot_time']:.3f}s")
    print(f"  - Components: {len(boot_status['components'])}")
    
    print(f"\n✅ All systems operational!")
    
    # ========================================
    # SHUTDOWN
    # ========================================
    demo_banner("11. GRACEFUL SHUTDOWN")
    
    print("\nShutting down SAGCO OS...\n")
    bootloader.shutdown()
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║                    DEMO COMPLETE                          ║
║                                                           ║
║   All infrastructure components working successfully!     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()
