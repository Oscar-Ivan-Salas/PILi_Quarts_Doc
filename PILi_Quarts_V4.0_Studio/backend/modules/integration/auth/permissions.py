"""
Integration Module - Permission System
Enterprise-grade role-based access control (RBAC)
Following vulnerability-scanner and architecture skills
"""
from enum import Enum
from typing import List, Set
from functools import wraps
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


class Permission(str, Enum):
    """
    System permissions.
    
    Following architecture: Clear permission naming
    Following vulnerability-scanner: Principle of least privilege
    """
    # Workspace permissions
    WORKSPACE_VIEW = "workspace:view"
    WORKSPACE_CREATE = "workspace:create"
    WORKSPACE_EDIT = "workspace:edit"
    WORKSPACE_DELETE = "workspace:delete"
    WORKSPACE_MANAGE_MEMBERS = "workspace:manage_members"
    
    # Project permissions
    PROJECT_CREATE = "project:create"
    PROJECT_VIEW = "project:view"
    PROJECT_EDIT = "project:edit"
    PROJECT_DELETE = "project:delete"
    PROJECT_MANAGE_MEMBERS = "project:manage_members"
    
    # Document permissions
    DOCUMENT_CREATE = "document:create"
    DOCUMENT_VIEW = "document:view"
    DOCUMENT_EDIT = "document:edit"
    DOCUMENT_DELETE = "document:delete"
    DOCUMENT_APPROVE = "document:approve"
    DOCUMENT_SHARE = "document:share"
    
    # Folder permissions
    FOLDER_CREATE = "folder:create"
    FOLDER_VIEW = "folder:view"
    FOLDER_EDIT = "folder:edit"
    FOLDER_DELETE = "folder:delete"
    
    # User permissions
    USER_VIEW = "user:view"
    USER_EDIT = "user:edit"
    USER_DELETE = "user:delete"
    
    # Admin permissions
    ADMIN_ACCESS = "admin:access"
    ADMIN_SETTINGS = "admin:settings"
    ADMIN_USERS = "admin:users"


class Role(str, Enum):
    """
    User roles with hierarchical permissions.
    
    Following architecture: Role hierarchy
    """
    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
    GUEST = "guest"


# Role-Permission mapping
ROLE_PERMISSIONS: dict[Role, Set[Permission]] = {
    Role.OWNER: {p for p in Permission},  # All permissions
    
    Role.ADMIN: {
        # Workspace
        Permission.WORKSPACE_VIEW,
        Permission.WORKSPACE_EDIT,
        Permission.WORKSPACE_MANAGE_MEMBERS,
        # Project
        Permission.PROJECT_CREATE,
        Permission.PROJECT_VIEW,
        Permission.PROJECT_EDIT,
        Permission.PROJECT_DELETE,
        Permission.PROJECT_MANAGE_MEMBERS,
        # Document
        Permission.DOCUMENT_CREATE,
        Permission.DOCUMENT_VIEW,
        Permission.DOCUMENT_EDIT,
        Permission.DOCUMENT_DELETE,
        Permission.DOCUMENT_APPROVE,
        Permission.DOCUMENT_SHARE,
        # Folder
        Permission.FOLDER_CREATE,
        Permission.FOLDER_VIEW,
        Permission.FOLDER_EDIT,
        Permission.FOLDER_DELETE,
        # User
        Permission.USER_VIEW,
    },
    
    Role.EDITOR: {
        # Workspace
        Permission.WORKSPACE_VIEW,
        # Project
        Permission.PROJECT_VIEW,
        Permission.PROJECT_EDIT,
        # Document
        Permission.DOCUMENT_CREATE,
        Permission.DOCUMENT_VIEW,
        Permission.DOCUMENT_EDIT,
        Permission.DOCUMENT_SHARE,
        # Folder
        Permission.FOLDER_CREATE,
        Permission.FOLDER_VIEW,
        Permission.FOLDER_EDIT,
        # User
        Permission.USER_VIEW,
    },
    
    Role.VIEWER: {
        # Workspace
        Permission.WORKSPACE_VIEW,
        # Project
        Permission.PROJECT_VIEW,
        # Document
        Permission.DOCUMENT_VIEW,
        # Folder
        Permission.FOLDER_VIEW,
        # User
        Permission.USER_VIEW,
    },
    
    Role.GUEST: {
        # Minimal permissions
        Permission.WORKSPACE_VIEW,
        Permission.PROJECT_VIEW,
        Permission.DOCUMENT_VIEW,
    },
}


def has_permission(user_role: Role, permission: Permission) -> bool:
    """
    Check if role has specific permission.
    
    Following clean-code: Single Responsibility
    Following vulnerability-scanner: Permission validation
    
    Args:
        user_role: User's role
        permission: Permission to check
    
    Returns:
        True if role has permission, False otherwise
    """
    if user_role not in ROLE_PERMISSIONS:
        logger.warning(f"Unknown role: {user_role}")
        return False
    
    return permission in ROLE_PERMISSIONS[user_role]


def has_any_permission(user_role: Role, permissions: List[Permission]) -> bool:
    """Check if role has any of the specified permissions"""
    return any(has_permission(user_role, p) for p in permissions)


def has_all_permissions(user_role: Role, permissions: List[Permission]) -> bool:
    """Check if role has all specified permissions"""
    return all(has_permission(user_role, p) for p in permissions)


def require_permission(permission: Permission):
    """
    Decorator to require specific permission.
    
    Following api-patterns: Permission-based access control
    
    Usage:
        @router.delete("/projects/{id}")
        @require_permission(Permission.PROJECT_DELETE)
        async def delete_project(id: UUID, user: TokenData = Depends(get_current_user)):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get user from kwargs (injected by FastAPI)
            user = kwargs.get('user') or kwargs.get('current_user')
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            user_role = Role(user.rol)
            
            if not has_permission(user_role, permission):
                logger.warning(
                    f"Permission denied: {user.email} ({user_role}) "
                    f"attempted {permission}"
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied: {permission.value} required"
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def get_user_permissions(user_role: Role) -> List[str]:
    """
    Get all permissions for a role.
    
    Following clean-code: Expose useful information
    
    Args:
        user_role: User's role
    
    Returns:
        List of permission strings
    """
    if user_role not in ROLE_PERMISSIONS:
        return []
    
    return [p.value for p in ROLE_PERMISSIONS[user_role]]


def can_access_workspace(user_role: Role, workspace_role: Role) -> bool:
    """
    Check if user can access workspace based on roles.
    
    Following architecture: Business logic separation
    
    Args:
        user_role: User's global role
        workspace_role: User's role in specific workspace
    
    Returns:
        True if access allowed
    """
    # Owner and admin always have access
    if user_role in [Role.OWNER, Role.ADMIN]:
        return True
    
    # Check workspace-specific role
    return has_permission(workspace_role, Permission.WORKSPACE_VIEW)


def can_manage_project(user_role: Role, project_role: Role) -> bool:
    """Check if user can manage project"""
    if user_role in [Role.OWNER, Role.ADMIN]:
        return True
    
    return has_permission(project_role, Permission.PROJECT_EDIT)
