#!/usr/bin/env python3
"""
SAGCO OS Security & Authentication Layer
Implements authentication, authorization, and RBAC
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, List, Dict, Any, Set
from datetime import datetime, timedelta
import hashlib
import secrets
import json


class Permission(Enum):
    """System permissions"""
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    DELETE = auto()
    ADMIN = auto()
    SECURITY_AUDIT = auto()
    PACKAGE_MANAGE = auto()
    CONFIG_MANAGE = auto()


class Role(Enum):
    """RBAC roles"""
    GUEST = auto()          # Read-only access
    USER = auto()           # Basic operations
    OPERATOR = auto()       # Dom's default role - operational control
    ADMIN = auto()          # Full system access
    SECURITY = auto()       # Security audit capabilities


@dataclass
class User:
    """User account"""
    username: str
    user_id: str
    roles: List[Role] = field(default_factory=list)
    permissions: Set[Permission] = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Session:
    """User session"""
    session_id: str
    user: User
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    ip_address: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_valid(self) -> bool:
        """Check if session is still valid"""
        if not self.user.active:
            return False
        if self.expires_at and datetime.now() > self.expires_at:
            return False
        return True


class RBACManager:
    """Role-Based Access Control manager"""
    
    # Default role permissions
    ROLE_PERMISSIONS = {
        Role.GUEST: {Permission.READ},
        Role.USER: {Permission.READ, Permission.WRITE, Permission.EXECUTE},
        Role.OPERATOR: {
            Permission.READ, Permission.WRITE, Permission.EXECUTE,
            Permission.DELETE, Permission.CONFIG_MANAGE
        },
        Role.ADMIN: {
            Permission.READ, Permission.WRITE, Permission.EXECUTE,
            Permission.DELETE, Permission.ADMIN, Permission.CONFIG_MANAGE,
            Permission.PACKAGE_MANAGE
        },
        Role.SECURITY: {
            Permission.READ, Permission.SECURITY_AUDIT, Permission.ADMIN
        }
    }
    
    @classmethod
    def get_permissions(cls, roles: List[Role]) -> Set[Permission]:
        """Get combined permissions for roles"""
        permissions = set()
        for role in roles:
            permissions.update(cls.ROLE_PERMISSIONS.get(role, set()))
        return permissions
    
    @classmethod
    def has_permission(cls, user: User, permission: Permission) -> bool:
        """Check if user has specific permission"""
        if permission in user.permissions:
            return True
        
        role_permissions = cls.get_permissions(user.roles)
        return permission in role_permissions
    
    @classmethod
    def require_permission(cls, user: User, permission: Permission) -> None:
        """Raise exception if user lacks permission"""
        if not cls.has_permission(user, permission):
            raise SecurityError(
                f"User '{user.username}' lacks permission: {permission.name}"
            )


class SecurityError(Exception):
    """Security-related errors"""
    pass


class AuthenticationError(SecurityError):
    """Authentication failures"""
    pass


class AuthorizationError(SecurityError):
    """Authorization failures"""
    pass


class SecurityManager:
    """Main security manager for SAGCO OS"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, Session] = {}
        self.password_hashes: Dict[str, str] = {}
        self.rbac = RBACManager()
        self._initialize_default_users()
    
    def _initialize_default_users(self):
        """
        Create default system users
        
        WARNING: Default passwords are for development/demo only.
        In production, these should be changed immediately or disabled.
        Consider setting SAGCO_REQUIRE_PASSWORD_CHANGE=true in production.
        """
        # Default operator (Dom)
        dom = User(
            username="dom",
            user_id="dom-me10101",
            roles=[Role.OPERATOR, Role.ADMIN],
            metadata={
                "full_name": "Dom Garza",
                "organization": "Strategickhaos DAO LLC",
                "password_must_change": True  # Force password change on first production use
            }
        )
        self.users["dom"] = dom
        # SECURITY WARNING: Change default password in production!
        self.password_hashes["dom"] = self._hash_password("changeme")
        
        # System admin
        admin = User(
            username="admin",
            user_id="sys-admin",
            roles=[Role.ADMIN],
            metadata={"password_must_change": True}
        )
        self.users["admin"] = admin
        # SECURITY WARNING: Change default password in production!
        self.password_hashes["admin"] = self._hash_password("admin")
        
        # Guest account (read-only, safe for production)
        guest = User(
            username="guest",
            user_id="guest",
            roles=[Role.GUEST],
        )
        self.users["guest"] = guest
        self.password_hashes["guest"] = self._hash_password("guest")
    
    def _hash_password(self, password: str, salt: Optional[str] = None) -> str:
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        hash_obj = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # iterations
        )
        return f"{salt}${hash_obj.hex()}"
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            salt, hash_value = password_hash.split('$')
            new_hash = self._hash_password(password, salt)
            return new_hash == password_hash
        except (ValueError, AttributeError):
            return False
    
    def authenticate(
        self,
        username: str,
        password: str,
        session_duration: timedelta = timedelta(hours=8)
    ) -> Session:
        """Authenticate user and create session"""
        user = self.users.get(username)
        if not user:
            raise AuthenticationError(f"User '{username}' not found")
        
        if not user.active:
            raise AuthenticationError(f"User '{username}' is inactive")
        
        stored_hash = self.password_hashes.get(username)
        if not stored_hash or not self._verify_password(password, stored_hash):
            raise AuthenticationError("Invalid password")
        
        # Create session
        session_id = secrets.token_urlsafe(32)
        session = Session(
            session_id=session_id,
            user=user,
            expires_at=datetime.now() + session_duration
        )
        
        user.last_login = datetime.now()
        self.sessions[session_id] = session
        
        return session
    
    def validate_session(self, session_id: str) -> Session:
        """Validate and return session"""
        session = self.sessions.get(session_id)
        if not session:
            raise AuthenticationError("Invalid session")
        
        if not session.is_valid():
            del self.sessions[session_id]
            raise AuthenticationError("Session expired")
        
        return session
    
    def logout(self, session_id: str) -> None:
        """End user session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def create_user(
        self,
        username: str,
        password: str,
        roles: List[Role],
        created_by: User
    ) -> User:
        """Create new user account"""
        # Require admin permission
        self.rbac.require_permission(created_by, Permission.ADMIN)
        
        if username in self.users:
            raise SecurityError(f"User '{username}' already exists")
        
        user = User(
            username=username,
            user_id=f"user-{secrets.token_hex(8)}",
            roles=roles
        )
        
        self.users[username] = user
        self.password_hashes[username] = self._hash_password(password)
        
        return user
    
    def change_password(
        self,
        username: str,
        old_password: str,
        new_password: str
    ) -> None:
        """Change user password"""
        user = self.users.get(username)
        if not user:
            raise AuthenticationError(f"User '{username}' not found")
        
        stored_hash = self.password_hashes.get(username)
        if not stored_hash or not self._verify_password(old_password, stored_hash):
            raise AuthenticationError("Invalid old password")
        
        self.password_hashes[username] = self._hash_password(new_password)
    
    def grant_role(self, username: str, role: Role, granted_by: User) -> None:
        """Grant role to user"""
        self.rbac.require_permission(granted_by, Permission.ADMIN)
        
        user = self.users.get(username)
        if not user:
            raise SecurityError(f"User '{username}' not found")
        
        if role not in user.roles:
            user.roles.append(role)
    
    def revoke_role(self, username: str, role: Role, revoked_by: User) -> None:
        """Revoke role from user"""
        self.rbac.require_permission(revoked_by, Permission.ADMIN)
        
        user = self.users.get(username)
        if not user:
            raise SecurityError(f"User '{username}' not found")
        
        if role in user.roles:
            user.roles.remove(role)
    
    def get_user_status(self, username: str) -> Dict[str, Any]:
        """Get user status information"""
        user = self.users.get(username)
        if not user:
            raise SecurityError(f"User '{username}' not found")
        
        permissions = self.rbac.get_permissions(user.roles)
        
        return {
            "username": user.username,
            "user_id": user.user_id,
            "roles": [r.name for r in user.roles],
            "permissions": [p.name for p in permissions],
            "active": user.active,
            "created_at": user.created_at.isoformat(),
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "metadata": user.metadata
        }
    
    def audit_log(self, action: str, user: User, details: Dict[str, Any]) -> None:
        """
        Log security audit event
        
        Note: This is a placeholder implementation for v0.1.0.
        Production implementation (v0.2.0) will include:
        - Persistent audit log to secure storage
        - Tamper-proof log signing
        - Log rotation and archival
        - Integration with SIEM systems
        
        For now, logs are output to structured logger for visibility.
        """
        from src.core.logger import get_logger
        
        logger = get_logger("security.audit")
        event = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "user": user.username,
            "user_id": user.user_id,
            "details": details
        }
        
        # Log as JSON to security audit logger
        logger.info(f"SECURITY AUDIT: {action}", **event)
        
        # TODO (v0.2.0): Write to persistent audit log database
        # TODO (v0.2.0): Implement log signing for tamper detection


def get_security_manager() -> SecurityManager:
    """Get singleton security manager instance"""
    if not hasattr(get_security_manager, '_instance'):
        get_security_manager._instance = SecurityManager()
    return get_security_manager._instance
