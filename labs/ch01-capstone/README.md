# Ch 1 – Capstone: Part I Integrated Troubleshooting Lab

## Exam Blueprint Coverage

**Blueprint action verbs:** Interpret, Configure, Verify, Troubleshoot, Compare, Diagnose, Construct

ENCOR topics covered (all Chapter 1 pillars):
- VLANs, trunking, and 802.1Q frame analysis
- CAM table and Layer 2 forwarding
- SVIs, subinterfaces, and routed ports (IPv4 + IPv6)
- CEF, FIB, adjacency table, and process switching
- Layer 2 and Layer 3 diagnostic commands

## Scenario

You have been handed a multi-layer campus network that was recently deployed. The network has **five pre-injected faults** that must all be found and resolved before any end-to-end connectivity exists. Start by constructing your understanding of the intended design from the topology, then diagnose each fault using Layer 2 and Layer 3 show commands before touching any configuration.

## Topology

```
                R1 (IOSv)
               Gi0/0 — trunk
                    |
             SW-CORE (IOSvL2)
            /         |        \
        Gi0/1       Gi0/2      Gi0/3 (no switchport — routed)
    trunk→SW-ACC   VLAN30          |
          |        (server)      R2 (IOSv)
      SW-ACC (IOSvL2)             Gi0/0: 172.31.0.2/30
      Gi0/1: VLAN10 → PC1        Lo0:   10.99.99.99/32
      Gi0/2: VLAN20 → PC2
      Gi0/3: VLAN10 → PC3
```

**Nodes:**
| Device | Role | Node Definition |
|--------|------|----------------|
| R1 | Router (subinterfaces) | IOSv |
| R2 | Router (remote destination) | IOSv |
| SW-CORE | Core Layer 3 Switch | IOSvL2 |
| SW-ACC | Access Layer Switch | IOSvL2 |
| PC1 | End Host | IOSv |
| PC2 | End Host | IOSv |
| PC3 | End Host | IOSv |

## Intended Addressing (what the network should look like when working)

| Device | Interface | Address |
|--------|-----------|---------|
| R1 | Gi0/0.10 | 10.10.10.254/24 + 2001:db8:10::1/64 |
| R1 | Gi0/0.20 | 10.20.20.254/24 + 2001:db8:20::1/64 |
| R1 | Gi0/0.30 | 10.30.30.254/24 + 2001:db8:30::1/64 |
| SW-CORE | VLAN10 SVI | 10.10.10.1/24 + 2001:db8:10::2/64 |
| SW-CORE | VLAN20 SVI | 10.20.20.1/24 + 2001:db8:20::2/64 |
| SW-CORE | VLAN30 SVI | 10.30.30.1/24 + 2001:db8:30::1/64 |
| SW-CORE | Gi0/3 (no switchport) | 172.31.0.1/30 |
| R2 | Gi0/0 | 172.31.0.2/30 |
| R2 | Lo0 | 10.99.99.99/32 |
| PC1 | Gi0/0 | 10.10.10.10/24, GW 10.10.10.254 |
| PC2 | Gi0/0 | 10.20.20.10/24, GW 10.20.20.254 |
| PC3 | Gi0/0 | 10.10.10.11/24, GW 10.10.10.254 |

Static routes pre-configured on R1 and SW-CORE for reachability to R2 Lo0.

## Pre-Injected Faults

The topology loads with **five faults** present. Do NOT look at the startup configs until you have diagnosed each fault from show command output.

| # | Area | Symptom |
|---|------|---------|
| 1 | Trunking | Native VLAN mismatch between SW-ACC and SW-CORE |
| 2 | VLAN database | PC2 is completely isolated |
| 3 | Subinterface | PC1 cannot reach its default gateway (R1) |
| 4 | CEF | R2 is forwarding via process switching instead of CEF |
| 5 | Routed port | SW-CORE Gi0/3 is still a switchport — R2 has no L3 path to the network |

## Lab Objectives

1. **Construct** a full addressing and interface configuration plan on paper before opening any CLI session — map every interface type (trunk, access, subinterface, SVI, routed port) to its intended state
2. **Diagnose** fault #1: identify the native VLAN mismatch using CDP output on SW-ACC or SW-CORE; determine the operational impact on untagged traffic; fix it on both sides
3. **Diagnose** fault #2: PC2 (VLAN 20) is fully unreachable; `show mac address-table` shows no PC2 entry; determine whether the problem is the VLAN database, the port assignment, the SVI, or the trunk — fix the root cause
4. **Diagnose** fault #3: PC1 cannot ping 10.10.10.254; use `show interfaces GigabitEthernet0/0.10` on R1 to determine what is missing from the subinterface configuration; fix it
5. **Diagnose** fault #5: SW-CORE shows no directly connected route for 172.31.0.0/30; `show interfaces GigabitEthernet0/3` on SW-CORE reveals the issue — apply the fix and verify L3 connectivity to R2
6. **Diagnose** fault #4: R2's CPU is elevated during ping floods; use `show ip cef` and `show processes cpu` on R2 to confirm process switching is in effect; re-enable CEF and compare CPU before and after
7. **Verify** end-to-end: confirm PC1, PC2, and PC3 can all reach R2 Lo0 (10.99.99.99); use `show mac address-table`, `show arp`, `show ip cef`, `show ipv6 interface brief`, and `show interfaces trunk` together to confirm full operational state
8. **Packet capture**: right-click the SW-ACC–SW-CORE trunk link in the CML topology canvas → Capture; filter `eth.type == 0x8100` to observe 802.1Q-tagged frames; identify the TPID, PCP, DEI, and VLAN ID fields for traffic from PC1

## Importing into CML

Import `topology.yaml` from this directory into your CML instance to recreate the lab. **Do not pre-read the startup configs** — the faults are meant to be discovered through show commands.
