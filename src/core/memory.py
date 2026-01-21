#!/usr/bin/env python3
"""
SAGCO OS Memory Manager
Manages system state, caching, and data persistence
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List
from datetime import datetime, timedelta
from enum import Enum, auto
import json
import pickle
from collections import OrderedDict


class MemoryLevel(Enum):
    """Memory hierarchy levels"""
    L1_CACHE = auto()      # Fast, small cache
    L2_STORAGE = auto()    # Medium-term storage
    L3_PERSISTENT = auto() # Long-term persistence


@dataclass
class MemoryEntry:
    """Entry in memory system"""
    key: str
    value: Any
    level: MemoryLevel
    created_at: datetime = field(default_factory=datetime.now)
    accessed_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    ttl: Optional[timedelta] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """Check if entry has expired"""
        if self.ttl is None:
            return False
        return datetime.now() > (self.created_at + self.ttl)
    
    def touch(self) -> None:
        """Update access time and count"""
        self.accessed_at = datetime.now()
        self.access_count += 1


class LRUCache:
    """Least Recently Used cache implementation"""
    
    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self.cache: OrderedDict[str, MemoryEntry] = OrderedDict()
    
    def get(self, key: str) -> Optional[MemoryEntry]:
        """Get value from cache"""
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        if entry.is_expired():
            del self.cache[key]
            return None
        
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        entry.touch()
        return entry
    
    def put(self, key: str, entry: MemoryEntry) -> None:
        """Put value in cache"""
        if key in self.cache:
            self.cache.move_to_end(key)
        
        self.cache[key] = entry
        
        # Evict least recently used if over capacity
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
    
    def delete(self, key: str) -> bool:
        """Delete from cache"""
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
    
    def size(self) -> int:
        """Get current cache size"""
        return len(self.cache)


class MemoryManager:
    """
    Central memory management system for SAGCO OS
    Handles caching, state management, and persistence
    """
    
    def __init__(self):
        self.l1_cache = LRUCache(capacity=1000)  # Fast cache
        self.l2_storage: Dict[str, MemoryEntry] = {}  # Medium-term storage
        self.l3_persistent: Dict[str, MemoryEntry] = {}  # Persistent data
        self.stats = {
            "reads": 0,
            "writes": 0,
            "hits": 0,
            "misses": 0,
            "evictions": 0
        }
    
    def get(
        self,
        key: str,
        default: Any = None,
        level: Optional[MemoryLevel] = None
    ) -> Any:
        """
        Get value from memory hierarchy
        Searches L1 -> L2 -> L3 unless specific level specified
        """
        self.stats["reads"] += 1
        
        # Check specific level if requested
        if level == MemoryLevel.L1_CACHE:
            entry = self.l1_cache.get(key)
            if entry:
                self.stats["hits"] += 1
                return entry.value
            self.stats["misses"] += 1
            return default
        
        elif level == MemoryLevel.L2_STORAGE:
            entry = self.l2_storage.get(key)
            if entry and not entry.is_expired():
                entry.touch()
                self.stats["hits"] += 1
                return entry.value
            self.stats["misses"] += 1
            return default
        
        elif level == MemoryLevel.L3_PERSISTENT:
            entry = self.l3_persistent.get(key)
            if entry:
                entry.touch()
                self.stats["hits"] += 1
                return entry.value
            self.stats["misses"] += 1
            return default
        
        # Search all levels (L1 -> L2 -> L3)
        entry = self.l1_cache.get(key)
        if entry:
            self.stats["hits"] += 1
            return entry.value
        
        entry = self.l2_storage.get(key)
        if entry and not entry.is_expired():
            entry.touch()
            self.stats["hits"] += 1
            # Promote to L1
            self.l1_cache.put(key, entry)
            return entry.value
        
        entry = self.l3_persistent.get(key)
        if entry:
            entry.touch()
            self.stats["hits"] += 1
            # Promote to L1
            self.l1_cache.put(key, entry)
            return entry.value
        
        self.stats["misses"] += 1
        return default
    
    def put(
        self,
        key: str,
        value: Any,
        level: MemoryLevel = MemoryLevel.L1_CACHE,
        ttl: Optional[timedelta] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Store value at specified memory level"""
        self.stats["writes"] += 1
        
        entry = MemoryEntry(
            key=key,
            value=value,
            level=level,
            ttl=ttl,
            metadata=metadata or {}
        )
        
        if level == MemoryLevel.L1_CACHE:
            self.l1_cache.put(key, entry)
        elif level == MemoryLevel.L2_STORAGE:
            self.l2_storage[key] = entry
        elif level == MemoryLevel.L3_PERSISTENT:
            self.l3_persistent[key] = entry
    
    def delete(self, key: str) -> bool:
        """Delete key from all memory levels"""
        deleted = False
        deleted |= self.l1_cache.delete(key)
        if key in self.l2_storage:
            del self.l2_storage[key]
            deleted = True
        if key in self.l3_persistent:
            del self.l3_persistent[key]
            deleted = True
        return deleted
    
    def exists(self, key: str) -> bool:
        """Check if key exists in any level"""
        return (
            self.l1_cache.get(key) is not None or
            key in self.l2_storage or
            key in self.l3_persistent
        )
    
    def clear_level(self, level: MemoryLevel) -> None:
        """Clear all entries at specified level"""
        if level == MemoryLevel.L1_CACHE:
            self.l1_cache.clear()
        elif level == MemoryLevel.L2_STORAGE:
            self.l2_storage.clear()
        elif level == MemoryLevel.L3_PERSISTENT:
            self.l3_persistent.clear()
    
    def clear_all(self) -> None:
        """Clear all memory levels"""
        self.l1_cache.clear()
        self.l2_storage.clear()
        self.l3_persistent.clear()
    
    def cleanup_expired(self) -> int:
        """Remove expired entries from L2, return count"""
        expired_keys = [
            key for key, entry in self.l2_storage.items()
            if entry.is_expired()
        ]
        for key in expired_keys:
            del self.l2_storage[key]
        return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        hit_rate = 0.0
        total_requests = self.stats["reads"]
        if total_requests > 0:
            hit_rate = self.stats["hits"] / total_requests
        
        return {
            "l1_size": self.l1_cache.size(),
            "l2_size": len(self.l2_storage),
            "l3_size": len(self.l3_persistent),
            "total_entries": self.l1_cache.size() + len(self.l2_storage) + len(self.l3_persistent),
            "stats": self.stats.copy(),
            "hit_rate": hit_rate
        }
    
    def snapshot(self) -> Dict[str, Any]:
        """Create memory snapshot (for debugging/backup)"""
        return {
            "timestamp": datetime.now().isoformat(),
            "l1_cache": [
                {
                    "key": k,
                    "value": str(e.value)[:100],  # Truncate for safety
                    "access_count": e.access_count
                }
                for k, e in list(self.l1_cache.cache.items())[:10]  # Sample only
            ],
            "l2_storage_keys": list(self.l2_storage.keys()),
            "l3_persistent_keys": list(self.l3_persistent.keys()),
            "stats": self.get_stats()
        }


def get_memory_manager() -> MemoryManager:
    """Get singleton memory manager instance"""
    if not hasattr(get_memory_manager, '_instance'):
        get_memory_manager._instance = MemoryManager()
    return get_memory_manager._instance
