# Ch 1 – Lab 3: Forwarding Architectures — CEF, FIB, TCAM, and SDM Templates

## Exam Blueprint Coverage

**Blueprint action verbs:** Interpret, Verify, Compare, Diagnose

ENCOR topics covered:
- Cisco Express Forwarding (CEF) and the FIB
- Adjacency table and ARP resolution
- RIB vs. FIB — what each contains and which one CEF uses
- Layer 2 vs. Layer 3 forwarding decisions
- MAC address table behavior on a Layer 2 switch
- Process switching vs. CEF — comparison and fallback behavior
- Multi-hop Layer 3 forwarding — packet header changes at each hop
- TCAM (Ternary Content Addressable Memory) and SDM templates
- Centralized vs. distributed CEF forwarding architectures
- Software CEF vs. Hardware CEF

## Topology

```
R1 (Lo0: 10.1.1.1/32)          R2 (Lo0: 10.2.2.2/32)          R3 (Lo0: 10.3.3.3/32)
 Gi0/0: 192.168.1.1/24           Gi0/0: 192.168.1.2/24           Gi0/0: 192.168.2.3/24
        |                              |         |
        +--------- SW1 ---------------+    Gi0/1: 192.168.2.2/24
                (IOSvL2)
              192.168.1.0/24                192.168.2.0/24
```

**Nodes:**
| Device | Role | Node Definition |
|--------|------|----------------|
| R1 | Router | IOSv |
| R2 | Router (two hops — hub) | IOSv |
| R3 | Router | IOSv |
| SW1 | Layer 2 Switch | IOSvL2 |

## Pre-Configured Addressing

| Device | Interface | IP Address |
|--------|-----------|------------|
| R1 | GigabitEthernet0/0 | 192.168.1.1/24 |
| R1 | Loopback0 | 10.1.1.1/32 |
| R2 | GigabitEthernet0/0 | 192.168.1.2/24 |
| R2 | GigabitEthernet0/1 | 192.168.2.2/24 |
| R2 | Loopback0 | 10.2.2.2/32 |
| R3 | GigabitEthernet0/0 | 192.168.2.3/24 |
| R3 | Loopback0 | 10.3.3.3/32 |

**Static routes (pre-configured):**
- R1: `10.2.2.2/32` via `192.168.1.2`; `10.3.3.3/32` via `192.168.1.2`; `192.168.2.0/24` via `192.168.1.2`
- R2: `10.1.1.1/32` via `192.168.1.1`; `10.3.3.3/32` via `192.168.2.3`
- R3: `10.1.1.1/32` via `192.168.2.2`; `10.2.2.2/32` via `192.168.2.2`; `192.168.1.0/24` via `192.168.2.2`

## Lab Objectives

1. Verify CEF is enabled on R1, R2, and R3; interpret `show ip cef` output including the prefix, next-hop, and outbound interface fields
2. Interpret the FIB entries for the pre-configured static routes on R1
3. Examine the adjacency table on R1 (`show adjacency detail`) and explain its relationship to ARP and Layer 2 rewrite
4. Generate traffic between R1 Lo0 and R2 Lo0; observe the MAC address table on SW1 and explain what entries appear and why
5. Identify which forwarding path (CEF vs. process switching) handles each packet type
6. Disable CEF on R2 Gi0/0 (`no ip route-cache cef`); compare CPU utilization during sustained ping vs. the CEF baseline — use `show processes cpu` to observe the difference
7. **Multi-hop forwarding trace**: ping from R1 Lo0 (10.1.1.1) to R3 Lo0 (10.3.3.3); on R1 examine `show ip cef 10.3.3.3` and `show adjacency detail`; on R2 examine the same — trace how the Layer 3 destination IP stays constant while Layer 2 source and destination MACs are rewritten at each hop
8. Display `show sdm prefer` on SW1; explain what TCAM is, how it differs from DRAM-based CAM, and what the operational impact is when the TCAM routing table is exhausted
9. Compare centralized CEF (route processor performs all FIB lookups, as on fixed-platform switches) vs. distributed CEF (each line card carries its own FIB copy, as on modular chassis); identify which model IOSvL2 represents and why this distinction matters at scale
10. Re-enable CEF on R2 Gi0/0 and verify recovery using `show ip cef` and `show processes cpu`

## Importing into CML

Import `topology.yaml` from this directory into your CML instance to recreate the lab.
