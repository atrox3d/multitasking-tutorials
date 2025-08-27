# examples from various YT videos


# scalene MacOS

**in case of error:**

    ImportError: dlopen(/Users/***/code/python/multitasking/multitasking-tutorials/.venv/lib/python3.12/site-packages/scalene/get_line_atomic.abi3.so, 0x0002): bad bind opcode 0x00

```bash
uv remove scalene

uv pip install --no-binary scalene scalene
````

**how to run profiler**

```bash
uv run -m scalene --html --outfile profile_report.html ./coreyschafer/async/real_world_example_sync1.py
````


