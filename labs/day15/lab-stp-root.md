# Day 15 Lab · Work Order WO-1501

**From:** Network Operations
**Project:** Access block, Spanning Tree baseline
**Time box:** 20 minutes

## Design

- Three access switches cabled in a triangle, all links in VLAN 1.
- Spanning Tree stays at the switch default mode.
- SW3 is the planned core of this block.

## Cabling

| Switch | Interface | Connects to |
|--------|-----------|-------------|
| SW1    | Gi0/1     | SW2 Gi0/1   |
| SW1    | Gi0/2     | SW3 Gi0/1   |
| SW2    | Gi0/2     | SW3 Gi0/2   |

## Tasks

1. Baseline: Before changing anything, record which switch is the root bridge for VLAN 1 and why it won the election.
2. Cost record: For SW1 and SW2, record the cost to reach the root and show where that number comes from.
3. Port record: List every port with its role and state. One link carries no traffic: which port blocks it?
4. Change request: SW3 must be the root bridge for VLAN 1. Prove it from all three switches.
5. Observation: Bounce one forwarding link on a non-root switch. Record the states the port passes through and roughly how long it takes to forward again.

## Notes

- Switches are IOSvL2 in Cisco Modeling Labs; console only.
- Lab files: `lab-stp-root.yaml` (import into your own CML).
