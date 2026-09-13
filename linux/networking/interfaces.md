# Networking — Interfaces


```bash
ip -br a              # brief address list, one line per interface — a fast readable summary instead of ifconfig's verbose output
ip link show           # link state (UP/DOWN) and MTU — confirms the interface is actually up before checking anything higher-level
ethtool eth0            # link speed/duplex — check this when "the network feels slow"
```

```bash
ip addr add 10.0.0.5/24 dev eth0     # add an IP to an interface — temporary, lost on reboot unless persisted
ip link set eth0 up                    # bring an interface up — required after adding an address or restoring a disabled interface
ip link set eth0 down                   # bring it down — the opposite of the line above, useful before reconfiguring an interface
ethtool -S eth0                          # interface statistics — errors, drops, collisions, useful for chasing packet loss
```
