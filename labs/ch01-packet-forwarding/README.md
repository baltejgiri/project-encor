# Ch 1 – Packet Forwarding Lab

## Exam Blueprint Coverage

**Blueprint action verbs:** Interpret, Verify, Compare, Diagnose

ENCOR topics covered:
- Cisco Express Forwarding (CEF) and the FIB
- Adjacency table and ARP resolution
- Layer 2 vs. Layer 3 forwarding decisions
- MAC address table behavior on a Layer 2 switch
- Process switching vs. CEF comparison

## Topology

```
R1 (Lo0: 10.1.1.1/32)                R2 (Lo0: 10.2.2.2/32)
 Gi0/0: 192.168.1.1/24               Gi0/0: 192.168.1.2/24
        |                                    |
        +------------ SW1 ------------------+
                   192.168.1.0/24
```

**Nodes:**
| Device | Role | Node Definition |
|--------|------|----------------|
| R1 | Router | IOSv |
| R2 | Router | IOSv |
| SW1 | Layer 2 Switch | IOSvL2 |

## Pre-Configured Addressing

| Device | Interface | IP Address |
|--------|-----------|------------|
| R1 | GigabitEthernet0/0 | 192.168.1.1/24 |
| R1 | Loopback0 | 10.1.1.1/32 |
| R2 | GigabitEthernet0/0 | 192.168.1.2/24 |
| R2 | Loopback0 | 10.2.2.2/32 |

**Static routes (pre-configured):**
- R1: `10.2.2.2/32` via `192.168.1.2`
- R2: `10.1.1.1/32` via `192.168.1.1`

## Lab Objectives

1. Verify CEF is enabled on R1 and R2
2. Interpret the FIB entries for the pre-configured static routes
3. Examine the adjacency table and explain its relationship to ARP
4. Generate traffic between R1 Lo0 and R2 Lo0; observe the MAC address table on SW1
5. Identify which forwarding path (CEF vs. process switching) handles each packet type
6. Disable CEF on one interface and compare forwarding behavior

## Importing into CML

Import `topology.yaml` from this directory into your CML instance to recreate the lab.
