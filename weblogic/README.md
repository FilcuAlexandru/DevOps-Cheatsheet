# WebLogic

```bash
java weblogic.WLST                                             # start WLST interactively — a Jython shell for exploring and managing the domain live
java weblogic.WLST <script.py>                                   # run a WLST script non-interactively — the way to automate repeatable admin tasks instead of typing them each time
$DOMAIN_HOME/bin/startWebLogic.sh                                  # start the admin server in the foreground — first-boot errors print directly instead of hiding in a log you have to go find
$DOMAIN_HOME/bin/startManagedWebLogic.sh <server_name> <admin_url>   # start a managed server, pointing at the admin server — needed for it to register and pull its config
nmConnect() / nmStart('<server_name>')                               # start a server via Node Manager instead of the shell script — Node Manager can restart it automatically if it crashes, a plain script start can't
```

```python
# inside WLST
connect('<username>', '<password>', 't3://<host>:<port>')   # connect to a running admin server — required before any other WLST command against a live domain works
domainRuntime()                                                # switch to the domain runtime MBean tree — live runtime state, as opposed to static persisted config
cd('/ServerRuntimes/<server_name>/JMSRuntime')                   # navigate the MBean tree like a filesystem — cd/ls work the same way you'd expect from a shell
state('<server_name>')                                             # RUNNING / ADMIN / FAILED etc — the actual state of one managed server, not just whether its process exists
ls()                                                                 # list MBeans/attributes at the current tree location — discover what's available without external docs
serverConfig()                                                        # switch to the domain config MBean tree — persisted config, not live state
cd('/Servers/<server_name>')                                            # navigate the config tree for one managed server's static configuration — persisted settings, not the live runtime view
cmo.getListenPort()                                                       # read one attribute off the current MBean — cmo = current management object
shutdown('<server_name>', 'Server')                                         # graceful shutdown of a managed server via WLST — lets in-flight requests finish, unlike killing the process outright
```

```bash
$DOMAIN_HOME/bin/stopWebLogic.sh                          # stop the admin server via the vendor script — the supported way, avoids an unclean process kill
$DOMAIN_HOME/bin/startNodeManager.sh                         # start Node Manager first — nmStart() calls in WLST need it running to actually work
tail -f $DOMAIN_HOME/servers/AdminServer/logs/AdminServer.log   # tail the admin server's own log — separate from managed server logs, admin-specific issues show up here only
ls $DOMAIN_HOME/servers/                                            # list every managed server defined in this domain — confirms what actually exists before troubleshooting one by name
```

**Enhanced:**
```bash
kill -3 <pid>                                    # trigger a thread dump to stdout/stderr log without restarting the JVM — first move on a hang, not a restart
jstack <pid> > threaddump_$(date +%s).txt          # cleaner thread dump straight to a file — easier to diff between two hangs than scrolling console output
keytool -list -v -keystore trust.jks               # inspect a truststore's certs and expiry dates — the recurring fix for SSLHandshakeException
keytool -importcert -alias <alias> -file <cert.pem> -keystore trust.jks   # add a renewed CA cert to an existing truststore — the actual fix once you've confirmed an expired cert is the problem
```

```python
# inside WLST — JMS queue depth, the fast way to confirm a backlog before digging further
cd('/ServerRuntimes/<server_name>/JMSRuntime/<server_name>.jms/JMSServers/<jms_server_name>/Destinations/<queue_name>')
print cmo.getMessagesCurrentCount()   # messages sitting in the queue right now — a growing count with no consumers means something downstream stopped processing
print cmo.getConsumersCurrentCount()  # active consumers — zero consumers with a growing count means nobody's draining it
```

**Enhanced — logs and monitoring:**
```bash
tail -f $DOMAIN_HOME/servers/<server_name>/logs/<server_name>.log       # tail a managed server's own log directly — the fastest way to watch what one specific server is doing right now
grep -i "SEVERE\|<Error>" $DOMAIN_HOME/servers/<server_name>/logs/<server_name>.log | tail -50   # last 50 severe/error lines — fast triage without opening the whole log file
curl -s "http://<host>:<jolokia_port>/jolokia/read/com.bea:Type=ServerRuntime,Name=<server_name>/State"   # read server state over Jolokia JMX-HTTP, no WLST session needed — useful from monitoring scripts
netstat -an | grep <port>                                                                                    # confirm the port is listening at the OS level — independent of the app layer
openssl s_client -connect <host>:<port> -showcerts                                                             # inspect the cert a WebLogic SSL listener presents — from outside the JVM
keytool -list -v -keystore identity.jks | grep -A1 "Valid from"                                                  # check an identity keystore's own cert expiry — a different problem from a truststore issue, don't assume it's the same fix
```

## Health check

1. **Server state** — check the admin console or `state('<server_name>')` in WLST — red flag: anything other than `RUNNING`.
2. **Thread status** — a thread dump (`kill -3 <pid>`) — red flag: a high count of `STUCK` threads — this is the actual cause of most "server is up but not responding" tickets.
3. **Heap usage** — GC logs or `jmap -heap <pid>` — red flag: heap usage sustained near max with frequent full GCs — the server is thrashing, not just busy.

## Troubleshooting

**Managed server won't start:**
```bash
tail -100 $DOMAIN_HOME/servers/<server_name>/logs/<server_name>.log   # the actual startup error is almost always in the last lines — start reading from the bottom, not the top
ps -ef | grep <server_name>                                              # confirm it isn't already running under a stale process before retrying — a duplicate start attempt fails in a confusing way
```

**Server running but unresponsive (hung):**
```bash
kill -3 <pid>                                # thread dump first, always — a restart destroys the evidence of what caused the hang
grep -c "BLOCKED" threaddump.txt               # a high BLOCKED count usually means lock contention — not the same fix as raw overload, don't just add capacity
```

**OutOfMemoryError:**
```bash
grep -i "OutOfMemoryError" $DOMAIN_HOME/servers/<server_name>/logs/<server_name>.log   # confirm it's heap, not PermGen/Metaspace — the message names which one
jmap -heap <pid>                                                                          # current heap usage breakdown — only works while the process is still alive, capture it before restarting
```
Heap OOM is a capacity/leak question (raise -Xmx or find what's not being released); Metaspace OOM is almost always a classloader leak from repeated redeployments.

---
