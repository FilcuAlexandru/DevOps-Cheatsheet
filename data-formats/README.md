# YAML / JSON / jq

```bash
jq '.items[] | select(.status=="Running") | .name' pods.json   # filter + extract in one line — combines a condition and field selection without a separate pass
jq -r '.[] | [.name,.status] | @csv' data.json                   # converts a JSON array into CSV rows — pick the fields you want, in order
yq '.spec.replicas' deployment.yaml                                 # reads one value out of a YAML file by path — the jq equivalent for YAML
yq -i '.spec.replicas = 3' deployment.yaml                           # updates one value inside a YAML file directly — safer and more scriptable than hand-editing the file
python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" file.yaml   # validate YAML syntax with zero extra tools — Python already ships a YAML parser you can call directly
```

**Enhanced:**
```bash
jq -n --argjson a "$(cat a.json)" --argjson b "$(cat b.json)" '$a * $b'   # deep-merge two JSON objects — $b's keys win on conflict, nested objects merge recursively instead of one replacing the other
yq -o=json '.' config.yaml | jq '.'                                          # convert YAML to JSON in one pipeline — then use jq's full feature set
```

## Health check

1. **Syntax is actually valid** — `jq -e . file.json` (exit code, not just output) or a YAML linter — red flag: any parse error — don't trust a file just because it "looks right" in an editor.
2. **No duplicate keys in YAML** — YAML silently keeps the last occurrence and drops earlier ones — red flag: a linter warning about duplicate keys, which is easy to miss by eye.
3. **Expected fields are actually present** — spot-check with `jq '.expected_field'` — red flag: `null` where you expected a real value — the file parsed fine but doesn't contain what you think it does.

## Troubleshooting

**jq gives a "parse error" on input you're sure is valid:**
```bash
jq -e . file.json > /dev/null            # -e forces a non-zero exit on invalid JSON, without printing anything on success — good for scripting a validity check
cat -A file.json | head -3                 # look for invisible characters — a BOM or CRLF that breaks parsing but hides in a normal editor
```

**yq behaves differently than expected:**
```bash
yq --version                     # confirm which yq — the Go version (mikefarah) and the Python wrapper (kislyuk) have different flag syntax and are easy to mix up
```

**Deeply nested value won't update:**
```bash
yq -i '.spec.template.spec.containers[0].image = "myimage:v2"' deployment.yaml   # array index needed explicitly — a bare .containers.image silently matches nothing if it's actually a list
```

---
