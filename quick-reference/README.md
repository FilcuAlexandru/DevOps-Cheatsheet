# Quick Reference

| Need | Command |
|---|---|
| Who's listening on a port | `ss -tulnp` |
| Kill whatever holds a port | `fuser -k PORT/tcp` |
| Biggest dirs under here | `du -sh --max-depth=1 . \| sort -rh` |
| Follow a systemd service log | `journalctl -u svc -f` |
| Logs from a crashed container | `kubectl logs --previous` |
| Diff before applying | `kubectl diff -f file.yaml` |
| Quick TCP check | `nc -zv host port` |
| DNS answer only | `dig +short host` |
| Run heavy job politely | `nice -n 10 ionice -c3 cmd` |
| Recover a "lost" commit | `git reflog` |
| Pretty-print JSON | `python3 -m json.tool file.json` |
| Cert expiry check | `openssl s_client -connect host:443 \| openssl x509 -noout -dates` |
| Start a compose stack | `docker compose up -d` |
| Switch kube context | `kubectl config use-context myctx` |
| Reach a cluster service locally | `kubectl port-forward svc/myapp 8080:80` |
