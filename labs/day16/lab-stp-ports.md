# Day 16 Lab · Work Order WO-1602

**From:** Network Operations
**Project:** Access block, Spanning Tree port audit
**Time box:** 20 minutes

## Design

- Three access switches cabled in a triangle, all links in VLAN 1.
- SW1 and SW2 are joined by two links for extra capacity.
- Spanning Tree stays at the switch default mode.

## Cabling

| Switch | Interface | Connects to |
|--------|-----------|-------------|
| SW1    | Gi0/1     | SW2 Gi0/1   |
| SW1    | Gi0/2     | SW3 Gi0/1   |
| SW2    | Gi0/2     | SW3 Gi0/2   |
| SW1    | Gi0/3     | SW2 Gi0/3   |

## Tasks

1. Bridge IDs: Record the bridge ID of every switch for VLAN 1 and split the priority into its parts. Which switch is the root bridge, and what decided it?
2. Root ports: For each non-root switch, record its root port and root path cost.
3. Parallel links: SW1 and SW2 are joined by two links. Record the role and state at both ends of both links and explain what decided each one.
4. Designated ports: For every link, name the switch that owns the designated port and why it won.
5. Observation: Shut the forwarding link between SW1 and SW2. Record what happens to the other one and roughly how long until it forwards. Then bring the link back.

## Notes

- Switches are IOSvL2 in Cisco Modeling Labs; console only.
- Lab files: `lab-stp-ports.yaml` (import into your own CML).
