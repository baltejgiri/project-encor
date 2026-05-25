# Ch 1 – Lab 2: Layer 3 Interfaces — SVIs, Subinterfaces, and Routed Ports

## Exam Blueprint Coverage

**Blueprint action verbs:** Configure, Verify, Compare, Interpret

ENCOR topics covered:
- Switch Virtual Interfaces (SVIs) with IPv4 and IPv6
- Router subinterfaces with 802.1Q encapsulation
- Routed switch ports (`no switchport`) with IPv4 and IPv6
- Primary and secondary IPv4 addresses on an interface
- Multiple IPv6 global unicast addresses on a single interface
- Layer 3 verification commands on switches and routers
- Conditions required for an SVI to reach line-protocol up state

## Topology

```
R1 (IOSv)                           SW1 (IOSvL2)
Gi0/0 ──────── trunk ──────────── Gi0/0
Gi0/0.10: 10.10.10.254/24           Gi0/1 ── access VLAN10 ── PC1 (IOSv)
           172.16.10.254/24 (2nd)   Gi0/2 ── access VLAN20 ── PC2 (IOSv)
           2001:db8:10::1/64        Gi0/3 ── no switchport ── R2 Gi0/0
Gi0/0.20: 10.20.20.254/24
           2001:db8:20::1/64        SVIs:
                                      VLAN10: 10.10.10.1/24
                                               2001:db8:10::2/64
                                      VLAN20: 10.20.20.1/24
                                               2001:db8:20::2/64
                                    Gi0/3 routed: 172.30.0.1/30
                                                   2001:db8:30::1/64

R2 (IOSv)
Gi0/0: 172.30.0.2/30
        2001:db8:30::2/64
```

**Nodes:**
| Device | Role | Node Definition |
|--------|------|----------------|
| R1 | Router (subinterfaces) | IOSv |
| R2 | Router (routed point-to-point) | IOSv |
| SW1 | Layer 3 Switch (SVIs + routed port) | IOSvL2 |
| PC1 | End Host | IOSv |
| PC2 | End Host | IOSv |

## Pre-Configured State (loaded with topology)

- VLANs 10 and 20 created on SW1
- SW1 Gi0/0 configured as 802.1Q trunk toward R1
- SW1 Gi0/1 → access VLAN 10 (to PC1)
- SW1 Gi0/2 → access VLAN 20 (to PC2)
- PC1: 10.10.10.10/24, default gateway 10.10.10.254 (R1 subinterface)
- PC2: 10.20.20.10/24, default gateway 10.20.20.254 (R1 subinterface)

**Left for you to configure:** all L3 addressing (SVIs, subinterfaces, routed port on SW1 Gi0/3, R2 interfaces)

## Lab Objectives

1. Configure `no switchport` on SW1 Gi0/3 and assign both IPv4 and IPv6 addresses; verify with `show interfaces Gi0/3` that it operates as a routed port
2. Configure SVIs for VLAN 10 and VLAN 20 on SW1 with dual-stack addresses (IPv4 + IPv6)
3. Configure R1 Gi0/0 subinterfaces with `encapsulation dot1Q`; assign primary IPv4, secondary IPv4 (`172.16.10.254/24`), and IPv6 on Gi0/0.10; assign IPv4 and IPv6 on Gi0/0.20
4. Assign a second IPv6 global unicast address to R1 Gi0/0.10 (`2001:db8:10::ff/64`); verify both global addresses appear in `show ipv6 interface GigabitEthernet0/0.10`
5. Verify all L3 interfaces using `show ip interface brief`, `show ipv6 interface brief`, and `show interfaces`
6. Compare the output of `show interfaces` for an SVI versus a `no switchport` routed port — identify what differs
7. Diagnose why the SW1 VLAN 20 SVI shows `line protocol is down` (shut down PC2's access port, then bring it back up) — explain the conditions required for an SVI to be up/up
8. Trace the Layer 3 forwarding path from PC1 (10.10.10.10) to R2 Gi0/0 (172.30.0.2) — identify the gateway used and each MAC rewrite hop

## Importing into CML

Import `topology.yaml` from this directory into your CML instance to recreate the lab.
