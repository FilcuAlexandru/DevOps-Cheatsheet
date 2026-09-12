# WebLogic

```bash
java weblogic.WLST                                             # start the WebLogic Scripting Tool (interactive Jython shell)
java weblogic.WLST <script.py>                                   # run a WLST script non-interactively
$DOMAIN_HOME/bin/startWebLogic.sh                                  # start the admin server directly (foreground, useful for first-boot errors)
$DOMAIN_HOME/bin/startManagedWebLogic.sh <server_name> <admin_url>   # start a managed server, pointing at the admin server
nmConnect() / nmStart('<server_name>')                               # WLST: start a server via Node Manager instead of the shell script directly
```

```python
# inside WLST
connect('<username>', '<password>', 't3://<host>:<port>')   # connect to a running admin server
domainRuntime()                                                # switch to the domain runtime MBean tree
cd('/ServerRuntimes/<server_name>/JMSRuntime')                   # navigate the MBean tree like a filesystem
state('<server_name>')                                             # RUNNING / ADMIN / FAILED etc, for one managed server
ls()                                                                 # list MBeans/attributes at the current tree location
serverConfig()                                                        # switch to the domain config MBean tree (persisted config, not live runtime state)
cd('/Servers/<server_name>')                                            # navigate the config tree for one managed server's static configuration
cmo.getListenPort()                                                       # read one attribute directly off the current MBean (cmo = current management object)
shutdown('<server_name>', 'Server')                                         # graceful shutdown of a managed server via WLST instead of killing the process
```

```bash
$DOMAIN_HOME/bin/stopWebLogic.sh                          # stop the admin server via the vendor script
$DOMAIN_HOME/bin/startNodeManager.sh                         # start Node Manager, required before nmStart() calls work
tail -f $DOMAIN_HOME/servers/AdminServer/logs/AdminServer.log   # tail the admin server's own log (separate from managed server logs)
ls $DOMAIN_HOME/servers/                                            # list every managed server defined in this domain
```

**Enhanced:**
```bash
kill -3 <pid>                                    # trigger a thread dump to stdout/stderr log without restarting the JVM — first move on a hang, not a restart
jstack <pid> > threaddump_$(date +%s).txt          # cleaner thread dump straight to a file, easier to diff between two hangs
keytool -list -v -keystore trust.jks               # inspect a truststore's certs and expiry dates — the recurring fix for SSLHandshakeException
keytool -importcert -alias <alias> -file <cert.pem> -keystore trust.jks   # add a renewed CA cert to an existing truststore
```

```python
# inside WLST — JMS queue depth, the fast way to confirm a backlog before digging further
cd('/ServerRuntimes/<server_name>/JMSRuntime/<server_name>.jms/JMSServers/<jms_server_name>/Destinations/<queue_name>')
print cmo.getMessagesCurrentCount()   # messages sitting in the queue right now
print cmo.getConsumersCurrentCount()  # active consumers — zero consumers with a growing count means nobody's draining it
```

**Enhanced — logs and monitoring:**
```bash
tail -f $DOMAIN_HOME/servers/<server_name>/logs/<server_name>.log       # tail a managed server's own log directly
grep -i "SEVERE\|<Error>" $DOMAIN_HOME/servers/<server_name>/logs/<server_name>.log | tail -50   # last 50 severe/error lines, fast triage
curl -s "http://<host>:<jolokia_port>/jolokia/read/com.bea:Type=ServerRuntime,Name=<server_name>/State"   # read server state over Jolokia JMX-HTTP, no WLST session needed — useful from monitoring scripts
netstat -an | grep <port>                                                                                    # confirm the managed server's port is actually listening at the OS level, independent of what the app layer reports
openssl s_client -connect <host>:<port> -showcerts                                                             # inspect exactly what certificate a WebLogic SSL listener is presenting, from outside the JVM entirely
keytool -list -v -keystore identity.jks | grep -A1 "Valid from"                                                  # check an identity keystore's own cert expiry, not just the truststore
```

## Health check

1. **Server state** — check the admin console or `state('<server_name>')` in WLST — red flag: anything other than `RUNNING`.
2. **Thread status** — a thread dump (`kill -3 <pid>`) — red flag: a high count of `STUCK` threads — this is the actual cause of most "server is up but not responding" tickets.
3. **Heap usage** — GC logs or `jmap -heap <pid>` — red flag: heap usage sustained near max with frequent full GCs — the server is thrashing, not just busy.

## Troubleshooting

**Managed server won't start:**
```bash
tail -100 $DOMAIN_HOME/servers/<server_name>/logs/<server_name>.log   # the actual startup error is almost always in the last lines
ps -ef | grep <server_name>                                              # confirm it isn't already running under a stale process before retrying
```

**Server running but unresponsive (hung):**
```bash
kill -3 <pid>                                # thread dump first, always — a restart destroys the evidence of what caused the hang
grep -c "BLOCKED" threaddump.txt               # a high count of BLOCKED threads usually points to lock contention, not raw overload
```

**OutOfMemoryError:**
```bash
grep -i "OutOfMemoryError" $DOMAIN_HOME/servers/<server_name>/logs/<server_name>.log   # confirm it's heap, not PermGen/Metaspace — the message names which one
jmap -heap <pid>                                                                          # current heap usage breakdown, if the process is still alive
```
Heap OOM is a capacity/leak question (raise -Xmx or find what's not being released); Metaspace OOM is almost always a classloader leak from repeated redeployments.

---
