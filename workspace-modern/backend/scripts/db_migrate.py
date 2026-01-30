#!/usr/bin/env python
"""
Database Migration Scripts
Utility scripts for managing database migrations
Following deployment-procedures
"""
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> int:
    """Run command and print output"""
    print(f"\n🔧 {description}...")
    print(f"Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    
    if result.returncode == 0:
        print(f"✅ {description} - Success!")
    else:
        print(f"❌ {description} - Failed!")
    
    return result.returncode


def init_db():
    """Initialize database with migrations"""
    print("=" * 60)
    print("DATABASE INITIALIZATION")
    print("=" * 60)
    
    # Run migrations
    result = run_command(
        ["alembic", "upgrade", "head"],
        "Running migrations"
    )
    
    if result != 0:
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ DATABASE INITIALIZED SUCCESSFULLY!")
    print("=" * 60)


def create_migration(message: str):
    """Create new migration"""
    print("=" * 60)
    print(f"CREATING MIGRATION: {message}")
    print("=" * 60)
    
    result = run_command(
        ["alembic", "revision", "--autogenerate", "-m", message],
        "Generating migration"
    )
    
    if result != 0:
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ MIGRATION CREATED!")
    print("=" * 60)
    print("\n📝 Review the migration file before running 'upgrade'")


def upgrade_db(revision: str = "head"):
    """Upgrade database to revision"""
    print("=" * 60)
    print(f"UPGRADING DATABASE TO: {revision}")
    print("=" * 60)
    
    result = run_command(
        ["alembic", "upgrade", revision],
        f"Upgrading to {revision}"
    )
    
    if result != 0:
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ DATABASE UPGRADED!")
    print("=" * 60)


def downgrade_db(revision: str = "-1"):
    """Downgrade database by revision"""
    print("=" * 60)
    print(f"DOWNGRADING DATABASE TO: {revision}")
    print("=" * 60)
    
    # Confirm
    confirm = input("⚠️  Are you sure you want to downgrade? (yes/no): ")
    if confirm.lower() != "yes":
        print("❌ Downgrade cancelled")
        return
    
    result = run_command(
        ["alembic", "downgrade", revision],
        f"Downgrading to {revision}"
    )
    
    if result != 0:
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ DATABASE DOWNGRADED!")
    print("=" * 60)


def show_history():
    """Show migration history"""
    print("=" * 60)
    print("MIGRATION HISTORY")
    print("=" * 60)
    
    run_command(
        ["alembic", "history", "--verbose"],
        "Fetching history"
    )


def show_current():
    """Show current revision"""
    print("=" * 60)
    print("CURRENT REVISION")
    print("=" * 60)
    
    run_command(
        ["alembic", "current"],
        "Fetching current revision"
    )


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Database migration utilities")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Init command
    subparsers.add_parser("init", help="Initialize database with migrations")
    
    # Create migration command
    create_parser = subparsers.add_parser("create", help="Create new migration")
    create_parser.add_argument("message", help="Migration message")
    
    # Upgrade command
    upgrade_parser = subparsers.add_parser("upgrade", help="Upgrade database")
    upgrade_parser.add_argument("--revision", default="head", help="Target revision")
    
    # Downgrade command
    downgrade_parser = subparsers.add_parser("downgrade", help="Downgrade database")
    downgrade_parser.add_argument("--revision", default="-1", help="Target revision")
    
    # History command
    subparsers.add_parser("history", help="Show migration history")
    
    # Current command
    subparsers.add_parser("current", help="Show current revision")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_db()
    elif args.command == "create":
        create_migration(args.message)
    elif args.command == "upgrade":
        upgrade_db(args.revision)
    elif args.command == "downgrade":
        downgrade_db(args.revision)
    elif args.command == "history":
        show_history()
    elif args.command == "current":
        show_current()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
