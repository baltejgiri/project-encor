# Ch 1 – Lab 1: VLANs, Trunking, and 802.1Q Frame Analysis

## Exam Blueprint Coverage

**Blueprint action verbs:** Interpret, Configure, Verify, Compare, Diagnose

ENCOR topics covered:
- VLAN creation and access port assignment
- 802.1Q trunking configuration and verification
- 802.1Q frame structure: TPID, PCP, DEI, VLAN ID fields
- CAM table operation and MAC address learning
- Unknown unicast flooding behavior
- Native VLAN mismatch detection and resolution
- Layer 2 diagnostic commands

## Topology

```
PC1 (IOSv)        PC2 (IOSv)
Gi0/0 VLAN 10     Gi0/0 VLAN 10
     |                  |
  SW1 Gi0/1          SW2 Gi0/1
       \                /
        SW1 ---trunk--- SW2       ← packet capture this link
       (IOSvL2)        (IOSvL2)
        Gi0/0          Gi0/0
                          |
                       SW2 Gi0/2
                          |
                        PC3 (IOSv)
                        VLAN 20
```

**Nodes:**
| Device | Role | Node Definition |
|--------|------|----------------|
| SW1 | Layer 2 Switch | IOSvL2 |
| SW2 | Layer 2 Switch | IOSvL2 |
| PC1 | End Host | IOSv |
| PC2 | End Host | IOSv |
| PC3 | End Host | IOSv |

## Addressing

| Device | Interface | VLAN | IP Address |
|--------|-----------|------|------------|
| PC1 | Gi0/0 | 10 | 10.10.10.1/24 |
| PC2 | Gi0/0 | 10 | 10.10.10.2/24 |
| PC3 | Gi0/0 | 20 | 10.20.20.1/24 |

## Pre-Configured State (loaded with topology)

- VLANs 10 and 20 created on both switches
- SW1 Gi0/1 → access VLAN 10 (PC1)
- SW2 Gi0/1 → access VLAN 10 (PC2)
- SW2 Gi0/2 → access VLAN 20 (PC3)
- IP addresses on PC1, PC2, PC3

**Left for you to configure:** trunk between SW1 Gi0/0 and SW2 Gi0/0

## Lab Objectives

1. Configure an 802.1Q trunk between SW1 Gi0/0 and SW2 Gi0/0
2. Verify the trunk with `show interfaces trunk` — interpret every field
3. **Packet capture**: right-click the SW1–SW2 link in the CML topology canvas → select **Capture**. Filter on `eth.type == 0x8100` in Wireshark to isolate 802.1Q-tagged frames. Identify the TPID, PCP, DEI, and VLAN ID fields in the frame
4. Verify MAC table population on both switches after pinging between PC1 and PC2
5. Observe flooding: clear the MAC table (`clear mac address-table dynamic`), then re-ping; observe what SW1 does with the frame before PC2's MAC is learned
6. Diagnose a native VLAN mismatch: change SW2's native VLAN to 99 (`switchport trunk native vlan 99`) and observe the CDP warning on SW1; explain the impact on untagged traffic, then resolve it
7. Compare `show mac address-table` before and after traffic; explain how the aging timer affects entries
8. Use Layer 2 diagnostic commands: `show interfaces Gi0/0`, `show interfaces counters`, `show vlan brief`, `show spanning-tree vlan 10`

## Importing into CML

Import `topology.yaml` from this directory into your CML instance to recreate the lab.
