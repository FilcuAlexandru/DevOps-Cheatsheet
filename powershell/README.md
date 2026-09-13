# PowerShell

*(new territory — the mental model that matters: everything is an object, not text, so you pipe properties, not parsed strings)*

## Basic

```powershell
Get-Location                                       # prints the current working directory — pwd equivalent
Set-Location C:\path                                 # changes the current working directory — cd equivalent
Copy-Item file.txt backup.txt                          # duplicates a file under a new name in the same folder — cp equivalent
Move-Item file.txt archive\                              # moves (or renames, if the destination is a filename) a file — mv equivalent
Remove-Item file.txt                                        # deletes a file — rm equivalent; add -Recurse for a folder and its contents
New-Item -ItemType Directory -Path newfolder                  # creates a new directory — mkdir equivalent
$var = "value"                                                   # assigns a variable for the current session — no export needed like in bash, it's just how assignment works here
$env:PATH                                                          # reads the PATH environment variable — the $env: prefix is how you access any env var
```

```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10   # lists the 10 processes using the most CPU right now, heaviest first — the PowerShell equivalent of top -o %CPU
Get-Service | Where-Object {$_.Status -eq 'Running'}                   # filter, like grep but on real objects — matches on actual properties, not text patterns
Get-ChildItem -Recurse -File | Where-Object {$_.Length -gt 100MB}      # recursively searches the current folder for any file over 100MB — spot what's actually eating disk space
Get-Content log.txt -Wait -Tail 20                                      # streams a file's new lines as they're written — the PowerShell equivalent of tail -f, starts from the last 20 lines
```

**Enhanced:**
```powershell
Get-Command *service*                    # discover cmdlets by keyword — no need to memorize exact cmdlet names ahead of time
Get-Help Get-Process -Full                # full docs for any cmdlet, offline — no need to search online mid-task
$_ | Get-Member                           # inspect what properties/methods an object actually has — the PowerShell equivalent of "what fields does this JSON have"
Invoke-Command -ComputerName host1,host2 -ScriptBlock { Get-Service }   # run something on multiple remote machines at once — one command instead of looping manually
Test-NetConnection host -Port 443          # checks whether a specific TCP port on a host is reachable — the PowerShell equivalent of nc -zv
Get-WinEvent -LogName System -MaxEvents 50 # modern replacement for Get-EventLog
ConvertTo-Json / ConvertFrom-Json          # native JSON handling, no external tool — built into the shell, unlike bash which usually needs jq
Select-Object -ExpandProperty Name         # unwrap a single property instead of the whole object — get just the value you need, not the full object dump
```

**Coming from Python:** `Where-Object` ≈ filter/list comprehension, `ForEach-Object` ≈ map, `Select-Object` ≈ picking dict keys, and the pipe `|` passes live objects, not strings — so `$_.Status` works exactly like accessing an attribute in Python, no parsing required.

## Health check

1. **Execution policy allows the script to run** — `Get-ExecutionPolicy` — red flag: `Restricted` — the script won't run at all, and the error message doesn't always make that obvious.
2. **Required modules are available** — `Get-Module -ListAvailable <module_name>` — red flag: not found — better to know before the script fails halfway through.
3. **Remoting works, if the script needs it** — `Test-WSMan <host>` — red flag: fails — `Invoke-Command` against that host will fail too, for the same underlying reason.

## Troubleshooting

**Script won't run — "execution of scripts is disabled":**
```powershell
Get-ExecutionPolicy                                    # see the current restriction level — confirms why a script won't run before changing anything
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser       # allow locally-written scripts to run — scoped to your user, without loosening policy for the whole machine
```

**Module not found:**
```powershell
Get-Module -ListAvailable <module_name>   # confirm it's actually installed, and where — before assuming an import failure means it's missing entirely
Install-Module <module_name> -Scope CurrentUser   # install for your user only — no admin rights needed, unlike a machine-wide install
```

---
