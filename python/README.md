# Python

```bash
python3 -m venv .venv && source .venv/bin/activate   # isolated environment — always do this before pip install, avoids polluting the system Python
pip install -r requirements.txt        # install a project's dependencies — the standard step after cloning a repo, before anything else runs
pip freeze > requirements.txt            # snapshot exactly what's installed — pin these versions so someone else's install matches yours
pip list --outdated                        # what's got newer versions available — confirms what's actually outdated instead of guessing
python3 -m http.server 8000        # instant file server, zero setup — great for pulling a file off a box with no other transfer option
python3 -m json.tool file.json      # pretty-print / validate JSON from the CLI — no separate tool needed, Python already has this built in
python3 -c "import socket; print(socket.gethostbyname('host'))"   # quick one-liner DNS check — confirms resolution works without leaving Python or installing dig
python3 -m pdb script.py             # drop into the debugger on script start — steps through from the very first line instead of adding breakpoints manually
python3 -m timeit "sorted([3,1,2])"   # microbenchmark a snippet — isolates timing for one specific piece of code, not a whole script
```

**Enhanced:**
```bash
python3 -X importtime script.py 2> importtime.log   # profile what's actually slow at startup — surprisingly often a heavy import, not your own code
python3 -c "import cProfile,pstats,sys; cProfile.run('exec(open(sys.argv[1]).read())', 'out.prof')" script.py && python3 -m pstats out.prof   # profile a whole script's runtime, then explore hot functions interactively — snakeviz turns the raw profile into a readable visual
```

## Health check

1. **Correct interpreter/environment active** — `which python3` — red flag: points outside the venv you expect — the #1 cause of "it's installed but Python can't find it."
2. **Dependencies are consistent** — `pip check` — red flag: any reported conflict — a silently broken dependency graph causes confusing failures later, not immediately.
3. **No syntax errors before you even run it** — `python3 -m py_compile script.py` — red flag: any `SyntaxError` — catches typos before they cost you a debugging session.

## Troubleshooting

**`ModuleNotFoundError` despite `pip install`:**
```bash
which python3 && which pip           # confirm both point into the SAME environment — installing into one venv and running another is the #1 cause
pip show <package_name>                # confirms whether it's actually installed in the currently active environment — not just installed somewhere on the system
```

**Script works locally but fails in CI/production:**
```bash
python3 --version              # version mismatches between environments are common and easy to overlook — this catches one before it causes a confusing bug
pip freeze > actual-versions.txt   # compare against requirements.txt — an unpinned dependency can silently upgrade and break behavior
```

---
