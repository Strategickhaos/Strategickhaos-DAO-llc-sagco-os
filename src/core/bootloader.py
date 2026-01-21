#!/usr/bin/env python3
"""
SAGCO OS Bootloader
System initialization and startup sequence
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
from enum import Enum, auto
import sys


class BootStage(Enum):
    """Boot sequence stages"""
    INIT = auto()
    SECURITY = auto()
    MEMORY = auto()
    IPC = auto()
    SCHEDULER = auto()
    KERNEL = auto()
    SERVICES = auto()
    READY = auto()
    FAILED = auto()


@dataclass
class BootStep:
    """Individual boot step"""
    name: str
    stage: BootStage
    func: Callable
    required: bool = True
    completed: bool = False
    error: Optional[Exception] = None
    duration: float = 0.0


class Bootloader:
    """
    SAGCO OS Bootloader
    Orchestrates system initialization sequence
    """
    
    VERSION = "0.1.0"
    
    def __init__(self):
        self.current_stage = BootStage.INIT
        self.boot_steps: List[BootStep] = []
        self.start_time: Optional[datetime] = None
        self.ready_time: Optional[datetime] = None
        self.components: Dict[str, Any] = {}
        self.errors: List[str] = []
        
        self._define_boot_sequence()
    
    def _define_boot_sequence(self):
        """Define the boot sequence"""
        
        # Stage 1: Security initialization
        self.boot_steps.append(BootStep(
            name="Initialize Security Manager",
            stage=BootStage.SECURITY,
            func=self._init_security,
            required=True
        ))
        
        # Stage 2: Memory management
        self.boot_steps.append(BootStep(
            name="Initialize Memory Manager",
            stage=BootStage.MEMORY,
            func=self._init_memory,
            required=True
        ))
        
        # Stage 3: IPC/Event Bus
        self.boot_steps.append(BootStep(
            name="Initialize Event Bus",
            stage=BootStage.IPC,
            func=self._init_ipc,
            required=True
        ))
        
        # Stage 4: Scheduler
        self.boot_steps.append(BootStep(
            name="Initialize Scheduler",
            stage=BootStage.SCHEDULER,
            func=self._init_scheduler,
            required=True
        ))
        
        # Stage 5: Kernel
        self.boot_steps.append(BootStep(
            name="Initialize SAGCO Kernel",
            stage=BootStage.KERNEL,
            func=self._init_kernel,
            required=True
        ))
        
        # Stage 6: Services
        self.boot_steps.append(BootStep(
            name="Start System Services",
            stage=BootStage.SERVICES,
            func=self._init_services,
            required=False
        ))
    
    def _init_security(self) -> Any:
        """Initialize security manager"""
        from src.core.security import get_security_manager
        security = get_security_manager()
        return security
    
    def _init_memory(self) -> Any:
        """Initialize memory manager"""
        from src.core.memory import get_memory_manager
        memory = get_memory_manager()
        return memory
    
    def _init_ipc(self) -> Any:
        """Initialize IPC/Event bus"""
        from src.core.ipc import get_ipc_manager
        ipc = get_ipc_manager()
        ipc.start()
        return ipc
    
    def _init_scheduler(self) -> Any:
        """Initialize scheduler"""
        from src.core.scheduler import get_scheduler
        scheduler = get_scheduler()
        scheduler.start()
        return scheduler
    
    def _init_kernel(self) -> Any:
        """Initialize SAGCO kernel"""
        from src.core.sagco import SAGCO
        kernel = SAGCO()
        return kernel
    
    def _init_services(self) -> Dict[str, Any]:
        """Initialize additional services"""
        services = {}
        
        # Publish boot event
        if 'ipc' in self.components:
            ipc = self.components['ipc']
            ipc.event_bus.publish(
                event_type="system.boot.services_starting",
                data={"version": self.VERSION},
                source="bootloader"
            )
        
        return services
    
    def boot(self) -> bool:
        """Execute boot sequence"""
        self.start_time = datetime.now()
        print(f"[SAGCO OS BOOTLOADER v{self.VERSION}]")
        print(f"Boot started at: {self.start_time.isoformat()}")
        print("=" * 60)
        
        try:
            for step in self.boot_steps:
                self.current_stage = step.stage
                print(f"\n[{step.stage.name}] {step.name}...")
                
                step_start = datetime.now()
                
                try:
                    result = step.func()
                    step.completed = True
                    step.duration = (datetime.now() - step_start).total_seconds()
                    
                    # Store component reference
                    component_name = step.stage.name.lower()
                    self.components[component_name] = result
                    
                    print(f"  ✓ Completed in {step.duration:.3f}s")
                
                except Exception as e:
                    step.error = e
                    step.duration = (datetime.now() - step_start).total_seconds()
                    error_msg = f"{step.name} failed: {e}"
                    self.errors.append(error_msg)
                    print(f"  ✗ Failed in {step.duration:.3f}s: {e}")
                    
                    if step.required:
                        self.current_stage = BootStage.FAILED
                        print("\n[CRITICAL ERROR] Required boot step failed!")
                        return False
            
            # Boot successful
            self.current_stage = BootStage.READY
            self.ready_time = datetime.now()
            boot_duration = (self.ready_time - self.start_time).total_seconds()
            
            print("\n" + "=" * 60)
            print(f"[BOOT COMPLETE] System ready in {boot_duration:.3f}s")
            print(f"Ready at: {self.ready_time.isoformat()}")
            print("=" * 60)
            
            # Publish boot complete event
            if 'ipc' in self.components:
                ipc = self.components['ipc']
                ipc.event_bus.publish(
                    event_type="system.boot.complete",
                    data={
                        "version": self.VERSION,
                        "boot_time": boot_duration,
                        "components": list(self.components.keys())
                    },
                    source="bootloader"
                )
            
            return True
        
        except Exception as e:
            self.current_stage = BootStage.FAILED
            error_msg = f"Boot sequence failed: {e}"
            self.errors.append(error_msg)
            print(f"\n[FATAL ERROR] {error_msg}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get boot status"""
        return {
            "version": self.VERSION,
            "current_stage": self.current_stage.name,
            "boot_time": (
                (self.ready_time - self.start_time).total_seconds()
                if self.ready_time and self.start_time
                else None
            ),
            "steps": [
                {
                    "name": step.name,
                    "stage": step.stage.name,
                    "completed": step.completed,
                    "duration": step.duration,
                    "error": str(step.error) if step.error else None
                }
                for step in self.boot_steps
            ],
            "components": list(self.components.keys()),
            "errors": self.errors
        }
    
    def shutdown(self) -> None:
        """Graceful shutdown"""
        print("\n[SHUTDOWN] Stopping SAGCO OS...")
        
        # Stop scheduler
        if 'scheduler' in self.components:
            print("  Stopping scheduler...")
            self.components['scheduler'].stop()
        
        # Stop IPC
        if 'ipc' in self.components:
            print("  Stopping IPC...")
            self.components['ipc'].stop()
        
        print("[SHUTDOWN] Complete")


def main():
    """Bootloader entry point"""
    bootloader = Bootloader()
    
    success = bootloader.boot()
    
    if not success:
        print("\nBoot failed. Exiting.")
        sys.exit(1)
    
    # System is now ready
    print("\nSAGCO OS is ready.")
    print("Type 'status' for system status, 'shutdown' to exit.")
    
    # Simple interactive loop
    try:
        while True:
            cmd = input("\nsagco> ").strip().lower()
            
            if cmd == "status":
                import json
                print(json.dumps(bootloader.get_status(), indent=2))
            
            elif cmd == "shutdown" or cmd == "exit" or cmd == "quit":
                bootloader.shutdown()
                break
            
            elif cmd == "help":
                print("Available commands:")
                print("  status    - Show system status")
                print("  shutdown  - Shutdown system")
                print("  help      - Show this help")
            
            elif cmd:
                print(f"Unknown command: {cmd}")
                print("Type 'help' for available commands")
    
    except (KeyboardInterrupt, EOFError):
        print("\n\nInterrupt received.")
        bootloader.shutdown()


if __name__ == "__main__":
    main()
