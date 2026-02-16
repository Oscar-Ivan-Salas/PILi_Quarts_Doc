#!/usr/bin/env python
"""
Test Runner Script
Following testing-patterns: Easy test execution
"""
import sys
import subprocess
from pathlib import Path


def run_tests(test_type: str = "all", coverage: bool = True, verbose: bool = True):
    """
    Run tests with pytest.
    
    Args:
        test_type: Type of tests to run (all, unit, integration, slow)
        coverage: Whether to generate coverage report
        verbose: Verbose output
    """
    # Base command
    cmd = ["pytest"]
    
    # Add verbosity
    if verbose:
        cmd.append("-v")
    
    # Add coverage
    if coverage:
        cmd.extend(["--cov=modules", "--cov-report=html", "--cov-report=term"])
    
    # Add test type marker
    if test_type != "all":
        cmd.extend(["-m", test_type])
    
    # Run
    print(f"🧪 Running {test_type} tests...")
    print(f"Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    
    if result.returncode == 0:
        print("\n✅ All tests passed!")
        if coverage:
            print(f"\n📊 Coverage report: {Path(__file__).parent / 'htmlcov' / 'index.html'}")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run PILi Quarts tests")
    parser.add_argument(
        "--type",
        choices=["all", "unit", "integration", "slow"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--no-coverage",
        action="store_true",
        help="Disable coverage report"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Less verbose output"
    )
    
    args = parser.parse_args()
    
    run_tests(
        test_type=args.type,
        coverage=not args.no_coverage,
        verbose=not args.quiet
    )


if __name__ == "__main__":
    main()
