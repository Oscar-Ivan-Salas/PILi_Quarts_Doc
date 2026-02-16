# Database Migrations Guide - PILi Quarts

## 📊 Database Migrations Overview

Complete database migration system using **Alembic** for PILi Quarts backend.

**Status**: ✅ Ready for production  
**Database**: PostgreSQL  
**ORM**: SQLAlchemy 2.0  
**Migration Tool**: Alembic

---

## 📁 Migration Files

### Configuration Files

| File | Purpose |
|------|---------|
| `alembic.ini` | Alembic configuration |
| `alembic/env.py` | Migration environment setup |
| `alembic/script.py.mako` | Migration template |
| `alembic/versions/001_initial.py` | Initial migration (9 tables) |

### Utility Scripts

| Script | Purpose |
|--------|---------|
| `scripts/db_migrate.py` | Migration utilities |
| `scripts/seed_db.py` | Seed demo data |

---

## 🚀 Quick Start

### 1. Setup Database

```bash
# Create PostgreSQL database
createdb pili_quarts

# Or using psql
psql -U postgres
CREATE DATABASE pili_quarts;
\q
```

### 2. Configure Environment

```bash
# Set DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@localhost/pili_quarts
```

### 3. Run Migrations

```bash
# Initialize database
python scripts/db_migrate.py init

# Or manually
alembic upgrade head
```

### 4. Seed Data (Optional)

```bash
# Add demo data
python scripts/seed_db.py
```

---

## 📋 Database Schema

### Tables Created (9 total)

1. **users** - User accounts
2. **workspaces** - Organizations
3. **workspace_members** - Workspace memberships
4. **proyectos** - Construction projects
5. **proyecto_members** - Project teams
6. **folders** - Document folders (tree structure)
7. **documentos** - Files with metadata
8. **documento_versions** - File version history
9. **actividades** - Audit log

---

## 🔧 Migration Commands

### Using Utility Script

```bash
# Initialize database
python scripts/db_migrate.py init

# Create new migration
python scripts/db_migrate.py create "add_new_field"

# Upgrade to latest
python scripts/db_migrate.py upgrade

# Upgrade to specific revision
python scripts/db_migrate.py upgrade --revision abc123

# Downgrade one step
python scripts/db_migrate.py downgrade

# Downgrade to specific revision
python scripts/db_migrate.py downgrade --revision abc123

# Show migration history
python scripts/db_migrate.py history

# Show current revision
python scripts/db_migrate.py current
```

### Using Alembic Directly

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Upgrade to latest
alembic upgrade head

# Upgrade one step
alembic upgrade +1

# Downgrade one step
alembic downgrade -1

# Downgrade to base
alembic downgrade base

# Show current revision
alembic current

# Show history
alembic history --verbose

# Show SQL without executing
alembic upgrade head --sql
```

---

## 📊 Initial Migration Details

### Migration: `001_initial`

**Creates 9 tables with**:
- Primary keys (UUID)
- Foreign keys with cascades
- Indexes for performance
- JSONB columns for metadata
- Timestamps (created_at, updated_at)
- Unique constraints
- Default values

**Tables**:

#### 1. users
```sql
- id (PK)
- email (unique, indexed)
- nombre
- password_hash
- rol_global (owner/admin/member/viewer/guest)
- email_verified
- avatar_url
- settings (JSONB)
- created_at, updated_at, last_login
```

#### 2. workspaces
```sql
- id (PK)
- nombre
- slug (unique, indexed)
- descripcion
- owner_id (FK -> users)
- plan (free/pro/enterprise)
- settings (JSONB)
- created_at, updated_at
```

#### 3. workspace_members
```sql
- id (PK)
- workspace_id (FK -> workspaces)
- user_id (FK -> users)
- rol (owner/admin/member/viewer)
- joined_at
- UNIQUE(workspace_id, user_id)
```

#### 4. proyectos
```sql
- id (PK)
- nombre
- workspace_id (FK -> workspaces)
- descripcion
- tipo (residencial/comercial/industrial/otro)
- estado (activo/pausado/completado/cancelado)
- fecha_inicio, fecha_fin
- presupuesto
- metadata (JSONB)
- created_at, updated_at
```

#### 5. proyecto_members
```sql
- id (PK)
- proyecto_id (FK -> proyectos)
- user_id (FK -> users)
- rol (gerente/ingeniero/tecnico/viewer)
- joined_at
- UNIQUE(proyecto_id, user_id)
```

#### 6. folders
```sql
- id (PK)
- nombre
- proyecto_id (FK -> proyectos)
- parent_id (FK -> folders, self-reference)
- path (indexed)
- created_at, updated_at
```

#### 7. documentos
```sql
- id (PK)
- nombre
- proyecto_id (FK -> proyectos)
- folder_id (FK -> folders)
- tipo (cotizacion/informe/plano/contrato/otro)
- formato (pdf/docx/xlsx/dwg/otro)
- size_bytes
- storage_path
- version
- metadata (JSONB)
- created_by (FK -> users)
- created_at, updated_at
```

#### 8. documento_versions
```sql
- id (PK)
- documento_id (FK -> documentos)
- version
- storage_path
- size_bytes
- cambios
- created_by (FK -> users)
- created_at
- UNIQUE(documento_id, version)
```

#### 9. actividades
```sql
- id (PK)
- user_id (FK -> users)
- proyecto_id (FK -> proyectos)
- workspace_id (FK -> workspaces)
- tipo (crear/editar/eliminar/compartir/comentar/otro)
- entidad_tipo (proyecto/documento/workspace/usuario/otro)
- entidad_id
- descripcion
- metadata (JSONB)
- created_at (indexed)
```

---

## 🌱 Seed Data

### Demo Data Included

```bash
python scripts/seed_db.py
```

**Creates**:
- 2 users (admin, test)
- 1 workspace
- 2 projects
- 3 folders

**Login Credentials**:
- Admin: `admin@piliquarts.com` / `admin123`
- Test: `test@piliquarts.com` / `test123`

---

## 🔄 Migration Workflow

### Creating New Migration

1. **Modify Models**
```python
# modules/database/models/user.py
class User(Base):
    # Add new field
    phone = Column(String(20), nullable=True)
```

2. **Generate Migration**
```bash
python scripts/db_migrate.py create "add_user_phone"
```

3. **Review Migration**
```bash
# Check alembic/versions/XXXX_add_user_phone.py
```

4. **Apply Migration**
```bash
python scripts/db_migrate.py upgrade
```

### Rolling Back

```bash
# Downgrade one step
python scripts/db_migrate.py downgrade

# Downgrade to specific revision
python scripts/db_migrate.py downgrade --revision abc123
```

---

## 🛡️ Best Practices

### 1. Always Review Generated Migrations

```bash
# Generate migration
alembic revision --autogenerate -m "description"

# Review the file before applying
cat alembic/versions/XXXX_description.py
```

### 2. Test Migrations

```bash
# Test upgrade
alembic upgrade head

# Test downgrade
alembic downgrade -1

# Test upgrade again
alembic upgrade head
```

### 3. Backup Before Production

```bash
# Backup database
pg_dump pili_quarts > backup_$(date +%Y%m%d).sql

# Run migration
alembic upgrade head
```

### 4. Use Transactions

Alembic automatically wraps migrations in transactions for PostgreSQL.

### 5. Version Control

```bash
# Commit migrations to git
git add alembic/versions/
git commit -m "Add migration: description"
```

---

## 🐛 Troubleshooting

### Issue: "Target database is not up to date"

```bash
# Check current revision
alembic current

# Check history
alembic history

# Stamp database with current revision
alembic stamp head
```

### Issue: "Can't locate revision"

```bash
# Check alembic_version table
psql pili_quarts -c "SELECT * FROM alembic_version;"

# Stamp with correct revision
alembic stamp <revision_id>
```

### Issue: Migration fails

```bash
# Rollback
alembic downgrade -1

# Fix migration file
# Re-run
alembic upgrade head
```

---

## 📈 Production Deployment

### 1. Pre-Deployment

```bash
# Backup database
pg_dump -h production-host -U user pili_quarts > backup.sql

# Test migration on staging
alembic upgrade head --sql > migration.sql
# Review migration.sql
```

### 2. Deployment

```bash
# Run migration
alembic upgrade head

# Verify
alembic current
```

### 3. Rollback Plan

```bash
# If issues occur
alembic downgrade -1

# Restore backup if needed
psql -h production-host -U user pili_quarts < backup.sql
```

---

## 📚 Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Database migrations ready for production! 🚀**
