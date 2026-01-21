#!/usr/bin/env python3
"""
SAGCO OS Logging System
Structured logging with multiple outputs and log levels
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List
from datetime import datetime
from enum import Enum
from pathlib import Path
import json
import sys


class LogLevel(Enum):
    """Log severity levels"""
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


@dataclass
class LogEntry:
    """Structured log entry"""
    timestamp: datetime
    level: LogLevel
    message: str
    component: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    exception: Optional[Exception] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        entry = {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level.name,
            "component": self.component,
            "message": self.message
        }
        if self.metadata:
            entry["metadata"] = self.metadata
        if self.exception:
            entry["exception"] = str(self.exception)
        return entry
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())
    
    def to_text(self) -> str:
        """Convert to human-readable text"""
        parts = [
            f"[{self.timestamp.isoformat()}]",
            f"[{self.level.name}]",
            f"[{self.component}]",
            self.message
        ]
        if self.exception:
            parts.append(f"Exception: {self.exception}")
        return " ".join(parts)


class Logger:
    """
    Structured logger for SAGCO OS components
    Supports multiple output formats and destinations
    """
    
    def __init__(
        self,
        component: str,
        level: LogLevel = LogLevel.INFO,
        output_format: str = "json",
        outputs: Optional[List[str]] = None
    ):
        self.component = component
        self.level = level
        self.output_format = output_format
        self.outputs = outputs or ["console"]
        self.log_file: Optional[Path] = None
        self.entries: List[LogEntry] = []
        self.max_entries = 1000
    
    def _should_log(self, level: LogLevel) -> bool:
        """Check if message should be logged"""
        return level.value >= self.level.value
    
    def _write_output(self, entry: LogEntry) -> None:
        """Write log entry to configured outputs"""
        if self.output_format == "json":
            output = entry.to_json()
        else:
            output = entry.to_text()
        
        # Console output
        if "console" in self.outputs:
            if entry.level.value >= LogLevel.ERROR.value:
                print(output, file=sys.stderr)
            else:
                print(output)
        
        # File output
        if "file" in self.outputs and self.log_file:
            try:
                with open(self.log_file, 'a') as f:
                    f.write(output + "\n")
            except Exception as e:
                print(f"[LOGGER ERROR] Failed to write to log file: {e}", file=sys.stderr)
    
    def _log(
        self,
        level: LogLevel,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
        exception: Optional[Exception] = None
    ) -> None:
        """Internal log method"""
        if not self._should_log(level):
            return
        
        entry = LogEntry(
            timestamp=datetime.now(),
            level=level,
            message=message,
            component=self.component,
            metadata=metadata or {},
            exception=exception
        )
        
        # Store entry
        self.entries.append(entry)
        if len(self.entries) > self.max_entries:
            self.entries.pop(0)
        
        # Write to outputs
        self._write_output(entry)
    
    def debug(self, message: str, **metadata) -> None:
        """Log debug message"""
        self._log(LogLevel.DEBUG, message, metadata)
    
    def info(self, message: str, **metadata) -> None:
        """Log info message"""
        self._log(LogLevel.INFO, message, metadata)
    
    def warning(self, message: str, **metadata) -> None:
        """Log warning message"""
        self._log(LogLevel.WARNING, message, metadata)
    
    def error(self, message: str, exception: Optional[Exception] = None, **metadata) -> None:
        """Log error message"""
        self._log(LogLevel.ERROR, message, metadata, exception)
    
    def critical(self, message: str, exception: Optional[Exception] = None, **metadata) -> None:
        """Log critical message"""
        self._log(LogLevel.CRITICAL, message, metadata, exception)
    
    def set_level(self, level: LogLevel) -> None:
        """Change log level"""
        self.level = level
    
    def set_log_file(self, filepath: Path) -> None:
        """Set log file path"""
        self.log_file = filepath
        filepath.parent.mkdir(parents=True, exist_ok=True)
        if "file" not in self.outputs:
            self.outputs.append("file")
    
    def get_recent_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent log entries"""
        recent = self.entries[-limit:]
        return [entry.to_dict() for entry in recent]


class LogManager:
    """
    Central log management for SAGCO OS
    Manages loggers for all components
    """
    
    def __init__(self):
        self.loggers: Dict[str, Logger] = {}
        self.global_level = LogLevel.INFO
        self.global_format = "json"
        self.global_outputs = ["console"]
        self.stats = {
            "total_logs": 0,
            "by_level": {level.name: 0 for level in LogLevel}
        }
    
    def get_logger(self, component: str) -> Logger:
        """Get or create logger for component"""
        if component not in self.loggers:
            self.loggers[component] = Logger(
                component=component,
                level=self.global_level,
                output_format=self.global_format,
                outputs=self.global_outputs.copy()
            )
        return self.loggers[component]
    
    def set_global_level(self, level: LogLevel) -> None:
        """Set log level for all loggers"""
        self.global_level = level
        for logger in self.loggers.values():
            logger.set_level(level)
    
    def set_global_format(self, format_type: str) -> None:
        """Set output format for all loggers"""
        self.global_format = format_type
        for logger in self.loggers.values():
            logger.output_format = format_type
    
    def set_global_outputs(self, outputs: List[str]) -> None:
        """Set outputs for all loggers"""
        self.global_outputs = outputs
        for logger in self.loggers.values():
            logger.outputs = outputs.copy()
    
    def set_log_file(self, filepath: Path) -> None:
        """Set log file for all loggers"""
        for logger in self.loggers.values():
            logger.set_log_file(filepath)
    
    def get_all_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent logs from all components"""
        all_entries = []
        for logger in self.loggers.values():
            all_entries.extend(logger.entries)
        
        # Sort by timestamp
        all_entries.sort(key=lambda e: e.timestamp, reverse=True)
        
        return [entry.to_dict() for entry in all_entries[:limit]]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get logging statistics"""
        total_entries = sum(len(logger.entries) for logger in self.loggers.values())
        
        return {
            "total_loggers": len(self.loggers),
            "components": list(self.loggers.keys()),
            "total_entries": total_entries,
            "global_level": self.global_level.name,
            "global_format": self.global_format,
            "global_outputs": self.global_outputs
        }


def get_log_manager() -> LogManager:
    """Get singleton log manager"""
    if not hasattr(get_log_manager, '_instance'):
        get_log_manager._instance = LogManager()
    return get_log_manager._instance


def get_logger(component: str) -> Logger:
    """Convenience function to get logger"""
    return get_log_manager().get_logger(component)
