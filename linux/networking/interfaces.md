# Networking — Interfaces


```bash
ip -br a              # brief address list, one line per interface
ip link show           # link state (UP/DOWN), MTU
ethtool eth0            # link speed/duplex — check this when "the network feels slow"
```

```bash
ip addr add 10.0.0.5/24 dev eth0     # add an IP address to an interface (temporary, lost on reboot unless persisted in config)
ip link set eth0 up                    # bring an interface up
ip link set eth0 down                   # bring it down
ethtool -S eth0                          # interface statistics — errors, drops, collisions, useful for chasing packet loss
```
