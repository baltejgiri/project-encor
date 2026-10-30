# Lab · Work Order WO-1601 (planned for the pp 48-53 session)

**From:** Network Operations
**Project:** Access block, Spanning Tree change monitoring
**Time box:** 20 minutes

## Design

- The same three access switches cabled in a triangle (WO-1501).
- All three links become 802.1Q trunks. VLAN 1 and VLAN 10 exist on every switch.
- Spanning Tree stays at the switch default mode.

## Cabling

| Switch | Interface | Connects to |
|--------|-----------|-------------|
| SW1    | Gi0/1     | SW2 Gi0/1   |
| SW1    | Gi0/2     | SW3 Gi0/1   |
| SW2    | Gi0/2     | SW3 Gi0/2   |

## Tasks

1. Trunks: Build the design. For VLAN 1 and VLAN 10, record the root bridge and every switch's root port. Are the two trees the same? Why?
2. Change counter: On every switch, record how many topology changes VLAN 1 has seen, when the last one happened and which interface it came from.
3. Direct failure: Fail one forwarding link that touches the root bridge. Record which switches notice it, what they send, and how long until traffic has a path again.
4. Recovery: Restore the link. Record what the change counters show now on all three switches and explain the difference between them.
5. Question: Which of your failures made the switches age out MAC addresses faster, and for how long?

## Notes

- Switches are IOSvL2 in Cisco Modeling Labs; console only.
- Lab files: `lab-stp-changes.yaml` (import into your own CML).
