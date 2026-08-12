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

### Shebang and permissions

- `#!/usr/bin/env bash` — portable bash lookup  
- `chmod +x` — executable bit  
- Prefer `./script.sh` over `bash script.sh` once executable  

### `set -euo pipefail`

| Option | Effect |
|--------|--------|
| `-e` | Exit on command failure |
| `-u` | Error on unset variables |
| `-o pipefail` | Pipeline fails if any stage fails |

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
| `"${var:-default}"` | Default if unset/empty |

## Arguments

```bash
echo "script=$0"
echo "argc=$#"
echo "arg1=${1:-}"
shift                 # drop $1
```

## Conditionals

```bash
if [[ -f /etc/redhat-release ]]; then
  echo "RHEL-like host"
elif [[ -d /opt/ciss ]]; then
  echo "app dir exists"
else
  echo "unknown layout"
fi

[[ -n "${CISS_ENV:-}" ]] || { echo "CISS_ENV required" >&2; exit 1; }
```

| Test | Meaning |
|------|---------|
| `-f` | regular file |
| `-d` | directory |
| `-x` | executable |
| `-n` / `-z` | non-empty / empty string |
| `==`, `!=`, `-eq`, `-lt` | string / integer compares inside `[[ ]]` |

Prefer `[[ ... ]]` over legacy `[ ... ]` in bash.

## Loops

```bash
for f in /var/log/*.log; do
  [[ -e "$f" ]] || continue
  echo "log=$f"
done

while read -r line; do
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
| non-zero | failure (`1` generic, `2` usage) |

```bash
./check-disk.sh
echo $?    # last exit code
```

## Pipes and redirection

```bash
cmd > out.txt          # stdout to file
cmd 2> err.txt         # stderr
cmd > out.txt 2>&1     # both
cmd | tee out.txt      # screen + file
cmd1 | cmd2 | cmd3
```

## Safe patterns for admins

1. **Dry-run flags** when you write mutators (`echo` the `systemctl` first).  
2. **Confirm prompts** for destructive ops.  
3. **No secrets in repo** — read from env or a root-only file.  
4. **ShellCheck** when available (`shellcheck script.sh`).  
5. **Idempotent-ish** — “create dir if missing” rather than fail second run.  

```bash
install -d -m 755 "$HOME/ciss-lab"
```

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

(`/dev/tcp` is bash-specific; fine on RHEL bash.)

### Timestamped backup

```bash
ts=$(date +%Y%m%d-%H%M%S)
cp -a /etc/myapp.conf "myapp.conf.bak.${ts}"
```

## Drill (40 min)

1. Write `host-report.sh` that prints: hostname, RHEL release, disk, memory, listening ports summary.  
2. Accept optional output file: `./host-report.sh /tmp/report.txt`.  
3. Exit `2` on bad args; `1` on failure; `0` on success.  
4. Run under `bash -n host-report.sh` (syntax check).  
5. Commit on `DR-###` with a clear message (CISS GitLab lab).  

## Integrity

- Scripts that touch production need review — treat like application code.  
- Do not embed tokens, private keys, or classified host lists.

## Further reading

| Topic | Source |
|-------|--------|
| Bash manual | `man bash` · [GNU Bash manual](https://www.gnu.org/software/bash/manual/) |
| ShellCheck | [shellcheck.net](https://www.shellcheck.net/) |
| Style | Google shell style guide (search title) — useful defaults |
| RHEL commands | Course **RHEL 7 and Essential Linux Commands** |

## Next

**Package management** — yum/dnf, npm, pip/uv, Maven/Java artifacts, and when to use which.
