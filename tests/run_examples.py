#!/usr/bin/env python3
"""Runs every program in examples/ and compares its output with the .out file.

    python3 tests/run_examples.py            # Python interpreter
    python3 tests/run_examples.py --impl java
    python3 tests/run_examples.py --impl all

Both implementations must produce byte-identical output for the same program.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = sorted((ROOT / "examples").glob("*.my"))
BUILD = ROOT / "build"


def python_command(program: Path) -> list[str]:
    return [sys.executable, str(ROOT / "PMystic" / "mystic" / "mystic.py"), str(program)]


def java_command(program: Path) -> list[str]:
    return ["java", "-cp", str(BUILD), "JMystic.mystic.Mystic", str(program)]


def compile_java() -> None:
    if shutil.which("javac") is None:
        sys.exit("javac not found: install a JDK or run with --impl python")
    sources = [str(p) for p in (ROOT / "JMystic" / "mystic").glob("*.java")]
    subprocess.run(["javac", "-d", str(BUILD), *sources], check=True)


def run(impl: str) -> int:
    command = python_command if impl == "python" else java_command
    failures = 0
    for program in EXAMPLES:
        expected = program.with_suffix(".out").read_text()
        result = subprocess.run(
            command(program), capture_output=True, text=True, timeout=30
        )
        actual = result.stdout + result.stderr
        ok = actual == expected
        failures += not ok
        print(f"  {'ok  ' if ok else 'FAIL'} {impl:6} {program.name}")
        if not ok:
            print("    expected:", repr(expected))
            print("    actual:  ", repr(actual))
    return failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--impl", choices=["python", "java", "all"], default="python")
    args = parser.parse_args()

    impls = ["python", "java"] if args.impl == "all" else [args.impl]
    if "java" in impls:
        compile_java()

    failures = sum(run(impl) for impl in impls)
    if failures:
        sys.exit(f"{failures} example(s) failed")
    print("all examples passed")


if __name__ == "__main__":
    main()
