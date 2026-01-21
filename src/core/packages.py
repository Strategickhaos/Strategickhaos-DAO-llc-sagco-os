#!/usr/bin/env python3
"""
SAGCO OS Package Manager
Simple package installation and dependency management
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Set
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
import json


class PackageStatus(Enum):
    """Package installation status"""
    AVAILABLE = auto()
    INSTALLING = auto()
    INSTALLED = auto()
    FAILED = auto()
    REMOVING = auto()


@dataclass
class Package:
    """Software package"""
    name: str
    version: str
    description: str = ""
    dependencies: List[str] = field(default_factory=list)
    installed: bool = False
    install_date: Optional[datetime] = None
    status: PackageStatus = PackageStatus.AVAILABLE
    metadata: Dict[str, Any] = field(default_factory=dict)


class PackageRegistry:
    """
    Package registry for SAGCO OS
    Defines available cognitive packages and extensions
    """
    
    PACKAGES = {
        "sagco-core": Package(
            name="sagco-core",
            version="0.1.0",
            description="SAGCO OS core kernel",
            installed=True,
            status=PackageStatus.INSTALLED
        ),
        "sagco-security": Package(
            name="sagco-security",
            version="0.1.0",
            description="Security and authentication module",
            dependencies=["sagco-core"],
            installed=True,
            status=PackageStatus.INSTALLED
        ),
        "sagco-memory": Package(
            name="sagco-memory",
            version="0.1.0",
            description="Memory management system",
            dependencies=["sagco-core"],
            installed=True,
            status=PackageStatus.INSTALLED
        ),
        "sagco-scheduler": Package(
            name="sagco-scheduler",
            version="0.1.0",
            description="Task scheduler",
            dependencies=["sagco-core"],
            installed=True,
            status=PackageStatus.INSTALLED
        ),
        "sagco-ipc": Package(
            name="sagco-ipc",
            version="0.1.0",
            description="Inter-process communication",
            dependencies=["sagco-core"],
            installed=True,
            status=PackageStatus.INSTALLED
        ),
        # Extension packages (not yet installed)
        "sagco-web-api": Package(
            name="sagco-web-api",
            version="0.1.0",
            description="REST API server with FastAPI",
            dependencies=["sagco-core", "sagco-security"]
        ),
        "sagco-database": Package(
            name="sagco-database",
            version="0.1.0",
            description="Database integration layer",
            dependencies=["sagco-core", "sagco-memory"]
        ),
        "sagco-ml": Package(
            name="sagco-ml",
            version="0.1.0",
            description="Machine learning integration",
            dependencies=["sagco-core"]
        ),
        "sagco-git": Package(
            name="sagco-git",
            version="0.1.0",
            description="Git repository integration",
            dependencies=["sagco-core"]
        ),
        "sagco-canvas": Package(
            name="sagco-canvas",
            version="0.1.0",
            description="Canvas LMS integration",
            dependencies=["sagco-core", "sagco-web-api"]
        )
    }


class PackageManager:
    """
    Package manager for SAGCO OS
    Handles package installation, updates, and dependency resolution
    """
    
    def __init__(self):
        self.registry = PackageRegistry.PACKAGES.copy()
        self.installed: Dict[str, Package] = {}
        self.install_dir = Path.home() / ".sagco" / "packages"
        self.install_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize with pre-installed packages
        for name, pkg in self.registry.items():
            if pkg.installed:
                self.installed[name] = pkg
    
    def list_available(self) -> List[Package]:
        """List all available packages"""
        return list(self.registry.values())
    
    def list_installed(self) -> List[Package]:
        """List installed packages"""
        return list(self.installed.values())
    
    def search(self, query: str) -> List[Package]:
        """Search for packages"""
        results = []
        query_lower = query.lower()
        for pkg in self.registry.values():
            if (query_lower in pkg.name.lower() or
                query_lower in pkg.description.lower()):
                results.append(pkg)
        return results
    
    def get_package(self, name: str) -> Optional[Package]:
        """Get package by name"""
        return self.registry.get(name)
    
    def is_installed(self, name: str) -> bool:
        """Check if package is installed"""
        return name in self.installed
    
    def _resolve_dependencies(
        self,
        package: Package,
        resolved: Optional[Set[str]] = None,
        seen: Optional[Set[str]] = None
    ) -> List[str]:
        """Resolve package dependencies"""
        if resolved is None:
            resolved = set()
        if seen is None:
            seen = set()
        
        if package.name in seen:
            raise ValueError(f"Circular dependency detected: {package.name}")
        
        seen.add(package.name)
        
        for dep_name in package.dependencies:
            if dep_name not in resolved:
                dep_pkg = self.registry.get(dep_name)
                if not dep_pkg:
                    raise ValueError(f"Dependency not found: {dep_name}")
                
                self._resolve_dependencies(dep_pkg, resolved, seen)
        
        resolved.add(package.name)
        return list(resolved)
    
    def install(self, package_name: str, force: bool = False) -> bool:
        """Install package with dependencies"""
        pkg = self.registry.get(package_name)
        if not pkg:
            print(f"Package not found: {package_name}")
            return False
        
        if self.is_installed(package_name) and not force:
            print(f"Package already installed: {package_name}")
            return True
        
        print(f"Installing {package_name} v{pkg.version}...")
        
        try:
            # Resolve dependencies
            install_order = self._resolve_dependencies(pkg)
            
            # Install dependencies first
            for dep_name in install_order:
                if dep_name == package_name:
                    continue
                
                if not self.is_installed(dep_name):
                    dep_pkg = self.registry[dep_name]
                    print(f"  Installing dependency: {dep_name}")
                    dep_pkg.status = PackageStatus.INSTALLING
                    
                    # Simulate installation
                    dep_pkg.installed = True
                    dep_pkg.install_date = datetime.now()
                    dep_pkg.status = PackageStatus.INSTALLED
                    self.installed[dep_name] = dep_pkg
            
            # Install main package
            pkg.status = PackageStatus.INSTALLING
            
            # Simulate installation
            pkg.installed = True
            pkg.install_date = datetime.now()
            pkg.status = PackageStatus.INSTALLED
            self.installed[package_name] = pkg
            
            print(f"✓ Successfully installed {package_name}")
            return True
        
        except Exception as e:
            pkg.status = PackageStatus.FAILED
            print(f"✗ Installation failed: {e}")
            return False
    
    def remove(self, package_name: str, force: bool = False) -> bool:
        """Remove package"""
        if not self.is_installed(package_name):
            print(f"Package not installed: {package_name}")
            return False
        
        # Check if other packages depend on this
        if not force:
            dependents = []
            for name, pkg in self.installed.items():
                if package_name in pkg.dependencies:
                    dependents.append(name)
            
            if dependents:
                print(f"Cannot remove {package_name}: required by {', '.join(dependents)}")
                print("Use --force to remove anyway")
                return False
        
        pkg = self.installed[package_name]
        pkg.status = PackageStatus.REMOVING
        
        print(f"Removing {package_name}...")
        
        # Simulate removal
        pkg.installed = False
        pkg.install_date = None
        pkg.status = PackageStatus.AVAILABLE
        del self.installed[package_name]
        
        print(f"✓ Successfully removed {package_name}")
        return True
    
    def upgrade(self, package_name: str) -> bool:
        """Upgrade package to latest version"""
        if not self.is_installed(package_name):
            print(f"Package not installed: {package_name}")
            return False
        
        print(f"Upgrading {package_name}...")
        # In a real implementation, this would check for new versions
        # For now, just reinstall
        return self.install(package_name, force=True)
    
    def get_info(self, package_name: str) -> Optional[Dict[str, Any]]:
        """Get package information"""
        pkg = self.registry.get(package_name)
        if not pkg:
            return None
        
        return {
            "name": pkg.name,
            "version": pkg.version,
            "description": pkg.description,
            "dependencies": pkg.dependencies,
            "installed": pkg.installed,
            "install_date": pkg.install_date.isoformat() if pkg.install_date else None,
            "status": pkg.status.name,
            "metadata": pkg.metadata
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get package manager statistics"""
        return {
            "total_packages": len(self.registry),
            "installed_packages": len(self.installed),
            "available_packages": len(self.registry) - len(self.installed),
            "install_dir": str(self.install_dir)
        }


def get_package_manager() -> PackageManager:
    """Get singleton package manager"""
    if not hasattr(get_package_manager, '_instance'):
        get_package_manager._instance = PackageManager()
    return get_package_manager._instance
