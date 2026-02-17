# PILi Quarts - SQLite Local Database Configuration

## Database: SQLite (Local Development)

**Purpose**: Local testing before Supabase deployment

### Connection String
```
DATABASE_URL=sqlite:///./pili_quarts_local.db
```

### Features
- ✅ Compatible with PostgreSQL/Supabase
- ✅ No installation required
- ✅ File-based (portable)
- ✅ Perfect for local testing
- ✅ Easy migration to Supabase

### Migration Path
```
SQLite (Local) → PostgreSQL (Supabase)
```

### Tables

#### documents
- id (INTEGER PRIMARY KEY)
- type (TEXT) - 'proyecto-simple', 'cotizacion-simple', etc.
- title (TEXT)
- data (JSON)
- color_scheme (TEXT)
- logo (TEXT)
- font (TEXT)
- user_id (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

#### pili_conversations
- id (INTEGER PRIMARY KEY)
- user_id (TEXT)
- chat_type (TEXT) - 'electricidad', 'puesta-tierra', etc.
- messages (JSON)
- extracted_data (JSON)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

#### projects
- id (INTEGER PRIMARY KEY)
- name (TEXT)
- type (TEXT) - 'simple', 'complex'
- status (TEXT)
- progress (INTEGER)
- budget (REAL)
- data (JSON)
- user_id (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### Setup

```bash
# Backend will create database automatically
python -m uvicorn main:app --reload
```

### Migration to Supabase

When ready to deploy:
1. Export SQLite data
2. Update DATABASE_URL to Supabase
3. Run migrations
4. Import data

**File**: `pili_quarts_local.db` (auto-created in backend folder)
