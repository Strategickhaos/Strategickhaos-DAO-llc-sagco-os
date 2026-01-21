"""SAGCO OS - Strategic Academic Governance & Cognitive Operations"""
from .sagco import SAGCO, BloomLevel, CollapseChannel, Context, Artifact
from .security import SecurityManager, get_security_manager, Permission, Role
from .memory import MemoryManager, get_memory_manager, MemoryLevel
from .ipc import EventBus, get_event_bus, IPCManager, get_ipc_manager
from .scheduler import Scheduler, get_scheduler, TaskPriority, TaskStatus
from .bootloader import Bootloader, BootStage
from .config import ConfigManager, get_config
from .logger import Logger, LogManager, get_logger, get_log_manager, LogLevel
from .packages import PackageManager, get_package_manager, Package

__version__ = "0.1.0"
__all__ = [
    # Core kernel
    "SAGCO", "BloomLevel", "CollapseChannel", "Context", "Artifact",
    # Security
    "SecurityManager", "get_security_manager", "Permission", "Role",
    # Memory
    "MemoryManager", "get_memory_manager", "MemoryLevel",
    # IPC
    "EventBus", "get_event_bus", "IPCManager", "get_ipc_manager",
    # Scheduler
    "Scheduler", "get_scheduler", "TaskPriority", "TaskStatus",
    # Boot
    "Bootloader", "BootStage",
    # Config
    "ConfigManager", "get_config",
    # Logging
    "Logger", "LogManager", "get_logger", "get_log_manager", "LogLevel",
    # Packages
    "PackageManager", "get_package_manager", "Package",
]
