"""
Initial migration - Create all tables
Following database-design principles

Revision ID: 001_initial
Revises: 
Create Date: 2026-01-29 15:30:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all tables"""
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('nombre', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('rol_global', sa.String(50), nullable=False, server_default='member'),
        sa.Column('email_verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('avatar_url', sa.String(500), nullable=True),
        sa.Column('settings', postgresql.JSONB(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
    )
    
    # Create workspaces table
    op.create_table(
        'workspaces',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('nombre', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('owner_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('plan', sa.String(50), nullable=False, server_default='free'),
        sa.Column('settings', postgresql.JSONB(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_index('idx_workspaces_owner', 'workspaces', ['owner_id'])
    
    # Create workspace_members table
    op.create_table(
        'workspace_members',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('workspace_id', sa.String(36), sa.ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('rol', sa.String(50), nullable=False, server_default='member'),
        sa.Column('joined_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.UniqueConstraint('workspace_id', 'user_id', name='uq_workspace_user'),
    )
    op.create_index('idx_workspace_members_workspace', 'workspace_members', ['workspace_id'])
    op.create_index('idx_workspace_members_user', 'workspace_members', ['user_id'])
    
    # Create proyectos table
    op.create_table(
        'proyectos',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('nombre', sa.String(255), nullable=False),
        sa.Column('workspace_id', sa.String(36), sa.ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('tipo', sa.String(50), nullable=False, server_default='otro'),
        sa.Column('estado', sa.String(50), nullable=False, server_default='activo'),
        sa.Column('fecha_inicio', sa.Date(), nullable=True),
        sa.Column('fecha_fin', sa.Date(), nullable=True),
        sa.Column('presupuesto', sa.Numeric(15, 2), nullable=True),
        sa.Column('metadata', postgresql.JSONB(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_index('idx_proyectos_workspace', 'proyectos', ['workspace_id'])
    op.create_index('idx_proyectos_estado', 'proyectos', ['estado'])
    
    # Create proyecto_members table
    op.create_table(
        'proyecto_members',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('proyecto_id', sa.String(36), sa.ForeignKey('proyectos.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('rol', sa.String(50), nullable=False, server_default='viewer'),
        sa.Column('joined_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.UniqueConstraint('proyecto_id', 'user_id', name='uq_proyecto_user'),
    )
    op.create_index('idx_proyecto_members_proyecto', 'proyecto_members', ['proyecto_id'])
    op.create_index('idx_proyecto_members_user', 'proyecto_members', ['user_id'])
    
    # Create folders table
    op.create_table(
        'folders',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('nombre', sa.String(255), nullable=False),
        sa.Column('proyecto_id', sa.String(36), sa.ForeignKey('proyectos.id', ondelete='CASCADE'), nullable=False),
        sa.Column('parent_id', sa.String(36), sa.ForeignKey('folders.id', ondelete='CASCADE'), nullable=True),
        sa.Column('path', sa.String(1000), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_index('idx_folders_proyecto', 'folders', ['proyecto_id'])
    op.create_index('idx_folders_parent', 'folders', ['parent_id'])
    op.create_index('idx_folders_path', 'folders', ['path'])
    
    # Create documentos table
    op.create_table(
        'documentos',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('nombre', sa.String(255), nullable=False),
        sa.Column('proyecto_id', sa.String(36), sa.ForeignKey('proyectos.id', ondelete='CASCADE'), nullable=False),
        sa.Column('folder_id', sa.String(36), sa.ForeignKey('folders.id', ondelete='SET NULL'), nullable=True),
        sa.Column('tipo', sa.String(50), nullable=False, server_default='otro'),
        sa.Column('formato', sa.String(50), nullable=False),
        sa.Column('size_bytes', sa.BigInteger(), nullable=False),
        sa.Column('storage_path', sa.String(500), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('metadata', postgresql.JSONB(), nullable=False, server_default='{}'),
        sa.Column('created_by', sa.String(36), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_index('idx_documentos_proyecto', 'documentos', ['proyecto_id'])
    op.create_index('idx_documentos_folder', 'documentos', ['folder_id'])
    op.create_index('idx_documentos_tipo', 'documentos', ['tipo'])
    
    # Create documento_versions table
    op.create_table(
        'documento_versions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('documento_id', sa.String(36), sa.ForeignKey('documentos.id', ondelete='CASCADE'), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('storage_path', sa.String(500), nullable=False),
        sa.Column('size_bytes', sa.BigInteger(), nullable=False),
        sa.Column('cambios', sa.Text(), nullable=True),
        sa.Column('created_by', sa.String(36), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.UniqueConstraint('documento_id', 'version', name='uq_documento_version'),
    )
    op.create_index('idx_documento_versions_documento', 'documento_versions', ['documento_id'])
    
    # Create actividades table
    op.create_table(
        'actividades',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('proyecto_id', sa.String(36), sa.ForeignKey('proyectos.id', ondelete='CASCADE'), nullable=True),
        sa.Column('workspace_id', sa.String(36), sa.ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=True),
        sa.Column('tipo', sa.String(50), nullable=False),
        sa.Column('entidad_tipo', sa.String(50), nullable=False),
        sa.Column('entidad_id', sa.String(36), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=False),
        sa.Column('metadata', postgresql.JSONB(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_index('idx_actividades_user', 'actividades', ['user_id'])
    op.create_index('idx_actividades_proyecto', 'actividades', ['proyecto_id'])
    op.create_index('idx_actividades_workspace', 'actividades', ['workspace_id'])
    op.create_index('idx_actividades_created', 'actividades', ['created_at'])


def downgrade() -> None:
    """Drop all tables"""
    op.drop_table('actividades')
    op.drop_table('documento_versions')
    op.drop_table('documentos')
    op.drop_table('folders')
    op.drop_table('proyecto_members')
    op.drop_table('proyectos')
    op.drop_table('workspace_members')
    op.drop_table('workspaces')
    op.drop_table('users')
