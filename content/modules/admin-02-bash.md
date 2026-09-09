# Bash Programming for Admins

## Learning outcomes

After this module you can:

- Write small **bash scripts** with arguments, variables, and exit codes  
- Use **conditionals**, **loops**, and **functions** for lab automation  
- Handle errors with `set -euo pipefail` (and know when to relax it)  
- Redirect **stdout/stderr** and use pipes safely  
- Keep secrets out of scripts; make scripts **reviewable** (like code)  

## Why bash

Bash is the default glue on RHEL: install steps, health checks, backup wrappers, “run this after deploy.”

| Good bash use | Bad bash use |
|---------------|--------------|
| 20–100 line automation | 5,000-line business logic (use Java/Python) |
| Wrapping `systemctl`, `curl`, `mvn` | Parsing complex JSON without tools |
| Idempotent-ish lab setup | Hard-coded production passwords |

SE link: a script is a **design artifact** — name it, version it in Git, cite the DR on the branch.

## Script skeleton

```bash
#!/usr/bin/env bash
# check-disk.sh — report disk use over threshold (lab)
set -euo pipefail

THRESHOLD="${1:-80}"
HOST="$(hostname -f 2>/dev/null || hostname)"

usage() {
  echo "Usage: $0 [threshold_percent]" >&2
  exit 2
}

[[ "${1:-}" == "-h" || "${1:-}" == "--help" ]] && usage

echo "Host: ${HOST}"
echo "Threshold: ${THRESHOLD}%"

df -P -h | tail -n +2 | while read -r fs size used avail pct mount; do
  num="${pct%\%}"
  if (( num >= THRESHOLD )); then
    echo "WARN ${mount} at ${pct} (${fs})"
  fi
done
```

```bash
chmod +x check-disk.sh
./check-disk.sh 70
```

### Every flag and trick in that script

Nothing in the example is “mystery syntax.” Each bit is in this table; the rest of the module drills them.

| Bit | Meaning |
|-----|---------|
| `#!/usr/bin/env bash` | Portable shebang — find `bash` on `$PATH` |
| `set -euo pipefail` | Strict mode — table in the next subsection. **Not** the same as `[[ -e ]]` |
| `hostname -f` | Print the **F**QDN. `2>/dev/null` discards the error if `-f` is unavailable, then we fall back to `hostname` |
| `"${1:-80}"` | Use `$1` if set and non-empty, otherwise `80` |
| `"${1:-}"` | Same form; default is empty (used in the `-h` test) |
| `df -P -h` | `-P` POSIX portable (one filesystem per line, no wrapping — required so `read` gets six fields). `-h` human sizes |
| `tail -n +2` | Start at line **2** — drop the `df` header |
| `read -r` | **r**aw: do not treat `\` as an escape. Always use `-r` unless you have a reason not to |
| `${pct%\%}` | Strip the shortest suffix matching `%` (`80%` → `80`) |
| `(( num >= THRESHOLD ))` | **Arithmetic** test on integers. Different from `[[ ]]` string/file tests |
| `>&2` | Write to stderr (covered under redirection) |
| `exit 2` | Usage error. `0` = success, `1` = generic failure, `2` = bad args |

### Shebang and permissions

- `#!/usr/bin/env bash` — portable bash lookup  
- `chmod +x` — executable bit (`+x` = add execute for the file’s mode)  
- Prefer `./script.sh` over `bash script.sh` once executable  
- `bash -n script.sh` — **syntax check only**, do not run. Use this before you execute a new script (drill item 4)

### `set -euo pipefail`

| Option | Effect |
|--------|--------|
| `-e` | **E**xit the script when a command fails (non-zero status) |
| `-u` | Error on **u**nset variables |
| `-o pipefail` | Pipeline fails if **any** stage fails (not only the last) |

`set -e` is a **shell option**. It is not the file test `[[ -e "$path" ]]` (exists) used in loops below. Interns mix these up — say both names out loud when you teach this slide.

For intentional failures (`grep` no match), handle explicitly or temporarily `set +e`.

## Variables and quoting

```bash
NAME="CISS"
echo "$NAME"          # prefer quoted expansions
echo "${NAME}_lab"

# Bad: word splitting / globbing surprises
# cp $file $dest
# Good:
cp -- "$file" "$dest"
```

| Form | Use |
|------|-----|
| `"$var"` | Default safe expansion |
| `'literal'` | No expansion |
| `"${var:-default}"` | Default if unset or empty |
| `"${var%suffix}"` | Strip shortest matching suffix (`${pct%\%}` in the skeleton) |
| `cp --` | End of options — a filename starting with `-` is not a flag |

## Arguments

```bash
echo "script=$0"
echo "argc=$#"
echo "arg1=${1:-}"
shift                 # drop $1; $2 becomes $1
```

| Special | Meaning |
|---------|---------|
| `$0` | Script name as invoked |
| `$1`, `$2`, … | Positional arguments |
| `$#` | Argument count |
| `"$@"` | All args, each a separate word (prefer this) |
| `"$*"` | All args joined as one string (fine for a log line) |
| `$?` | Exit status of the last command |
| `shift` | Discard `$1` and renumber the rest |

## Conditionals

```bash
if [[ -f /etc/os-release ]]; then
  echo "RHEL-like host: $(. /etc/os-release; echo $NAME $VERSION_ID)"
elif [[ -d /opt/ciss ]]; then
  echo "app dir exists"
else
  echo "unknown layout"
fi

[[ -n "${CISS_ENV:-}" ]] || { echo "CISS_ENV required" >&2; exit 1; }
```

| Test | Meaning |
|------|---------|
| `-e` | Path **exists** (regular file, directory, or symlink) |
| `-f` | Exists **and** is a regular file |
| `-d` | Exists **and** is a directory |
| `-x` | Exists **and** is executable by you |
| `-s` | Exists **and** is a non-empty file |
| `-n` / `-z` | String is non-empty / empty |
| `==` / `!=` | String compare inside `[[ ]]` |
| `-eq` `-ne` `-lt` `-le` `-gt` `-ge` | Integer compare inside `[[ ]]` |
| `(( n >= 80 ))` | Arithmetic compare (integers). Used in the skeleton |

Prefer `[[ ... ]]` over legacy `[ ... ]` in bash.

`[[ -e ]]` vs `set -e`: the first is a **path test**; the second is “abort the script on failure.” Same letter, different language.

## Loops

`for` walks a list. `while read` walks lines.

| Word / flag | Meaning |
|-------------|---------|
| `continue` | Skip the rest of **this** iteration; go to the next item |
| `break` | Leave the loop entirely |
| `read -r` | Read one line; `-r` = raw (`\` is not an escape) |

The glob loop uses `[[ -e "$f" ]]` on purpose. If `/var/log/*.log` matches **nothing**, bash leaves the **literal** string `/var/log/*.log`. `-e` is false, so `continue` skips it. (`-f` would also skip the literal, but would skip directories too; `-e` is the “did this glob hit a real path?” test.)

```bash
for f in /var/log/*.log; do
  [[ -e "$f" ]] || continue   # skip unmatched glob; -e = exists
  echo "log=$f"
done

while read -r line; do        # -r = raw
  echo "saw:$line"
done < /etc/hosts
```

## Functions and exit codes

```bash
die() { echo "ERROR: $*" >&2; exit 1; }

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "missing command: $1"
}

need_cmd curl
need_cmd jq   # only if required
```

| Code | Convention |
|------|------------|
| `0` | success |
| `1` | generic failure |
| `2` | usage / bad arguments |

`"$*"` in `die` is intentional: the error message is one string. Use `"$@"` when you must preserve argument boundaries (passing through to another command).

```bash
./check-disk.sh
echo $?    # last exit code
```

## Pipes and redirection

```bash
cmd > out.txt          # stdout to file
cmd 2> err.txt         # stderr
cmd > out.txt 2>&1     # both
cmd >/dev/null 2>&1    # discard both
cmd | tee out.txt      # screen + file
cmd1 | cmd2 | cmd3
```

| Bit | Meaning |
|-----|---------|
| `>` | Truncate/create file, write stdout |
| `>>` | Append stdout |
| `2>` | Redirect stderr |
| `2>&1` | Send stderr to wherever stdout currently goes |
| `< file` | Stdin from file (`while read` above) |
| `/dev/null` | Bit bucket |

## Safe patterns for admins

1. **Dry-run flags** when you write mutators (`echo` the `systemctl` first).  
2. **Confirm prompts** for destructive ops.  
3. **No secrets in repo** — read from env or a root-only file.  
4. **ShellCheck** when available (`shellcheck script.sh`).  
5. **Idempotent-ish** — “create dir if missing” rather than fail second run.  

```bash
install -d -m 755 "$HOME/ciss-lab"
```

| Flag | Meaning |
|------|---------|
| `install -d` | Create a **d**irectory (and parents), like `mkdir -p` |
| `-m 755` | Set **m**ode (owner rwx, group/other r-x) |

## Mini patterns you will reuse

### Wait for port

```bash
wait_port() {
  local host=$1 port=$2
  for i in $(seq 1 30); do
    if bash -c "echo >/dev/tcp/${host}/${port}" 2>/dev/null; then
      return 0
    fi
    sleep 1
  done
  return 1
}
wait_port 127.0.0.1 61616 || die "ActiveMQ not listening"
```

| Bit | Meaning |
|-----|---------|
| `local` | Variable scoped to the function |
| `seq 1 30` | Print integers 1 through 30 (30 tries) |
| `/dev/tcp/HOST/PORT` | Bash-specific TCP probe; fine on RHEL bash |
| `return 0` / `return 1` | Function success / failure (does not exit the script) |

### Timestamped backup

```bash
ts=$(date +%Y%m%d-%H%M%S)
cp -a /etc/myapp.conf "myapp.conf.bak.${ts}"
```

`cp -a` = **a**rchive: copy recursively and preserve mode, owner, timestamps, and links. Same flag as in admin-01.

## Drill (40 min)

1. Write `host-report.sh` that prints: hostname, `/etc/os-release` VERSION_ID, disk (`df -hT`), memory, `nmcli device status`, listening ports (`ss -lntp` summary).  
2. Accept optional output file: `./host-report.sh /tmp/report.txt`.  
3. Exit `2` on bad args; `1` on failure; `0` on success.  
4. Run under `bash -n host-report.sh` (syntax check only — `-n` = no-execute).  
5. Commit on `DR-###` with a clear message (CISS GitLab lab).  

## Integrity

- Scripts that touch production need review — treat like application code.  
- Do not embed tokens, private keys, or classified host lists.

## Further reading

| Topic | Source |
|-------|--------|
| Bash manual | `man bash` · [GNU Bash manual](https://www.gnu.org/software/bash/manual/) |
| Test operators | `help test` · `man bash` (CONDITIONAL EXPRESSIONS) |
| ShellCheck | [shellcheck.net](https://www.shellcheck.net/) |
| Style | Google shell style guide (search title) — useful defaults |
| RHEL commands | Course **RHEL 10.2 and Essential Linux Commands** |

## Next

**Package management** — DNF 5, npm, pip/uv, Maven/Java artifacts, and when to use which.
