# Ch 4 - Multiple Spanning Tree Protocol (clean notes)

Related: Ch 2 (STP and RSTP basics), Ch 3 (Advanced STP Tuning), Ch 5 (EtherChannel)

**Status:** read pp 80-87 (Day 24), notes done for pp 80-87; next: MST Tuning, p 87. DIKTA before reading 4/7 (2026-11-11). Post-chapter DIKTA retake still to do.

---

## Why MST exists

| | Trees | Problem |
|---|---|---|
| **CST** (original 802.1D) | **One** tree for all VLANs | Can't load share: every VLAN blocks the same link (Fig 4-1: SW2 to SW3 traffic must go through SW1, even for a VLAN that only lives on SW2 and SW3). |
| **PVST** (Cisco) | **One tree per VLAN** | Can place the root and block different links per VLAN, but with thousands of VLANs the CPU must process BPDUs for every VLAN and recompute every tree when a big trunk fails. |
| **MST** (802.1s) | **One tree per instance**, many VLANs per instance | The middle ground: VLANs that want the same topology share one tree, called an **MST instance (MSTI)**. |

Fig 4-3: 4 VLANs in 3 instances (VLANs 1-2, VLAN 3, VLAN 4). Add 10 more VLANs into those instances and it's still **3 trees**.

### MST region
**Key Topic**

- A **region** = MST switches with the same high-level config: **name, revision (version) number and VLAN-to-instance map**. All three must match.
- To switches **outside** the region, the whole region looks like **one virtual switch** (Fig 4-4: SW7 blocks its port toward the region because SW5 looks only one hop from the root; SW3 blocks toward SW1 because it sees the region as a whole).

### MST instances (MSTIs)
**Key Topic**

- **IST (internal spanning tree) = instance 0**, always there. It runs on **every port** of every switch in the region, whatever VLANs the port carries.
- The other instances' info is **nested inside the IST BPDU**. So MST sends **one set of BPDUs**, however many instances there are.
- Platforms support at least 16 instances: 0 is the IST, **1-15** carry other VLANs. 1-15 have no special name, just MSTIs.
- By default **every VLAN is in instance 0**.

---

## MST configuration
**Key Topic**

| Step | Command | Notes |
|---|---|---|
| 1 | `spanning-tree mode mst` | Turns on MST |
| 2 (optional) | `spanning-tree mst <inst> priority <0-61440>` or `spanning-tree mst <inst> root {primary \| secondary} [diameter <n>]` | Steps of 4096. primary = 24,576, secondary = 28,672 (same scripts as Ch 3, but per instance) |
| 3 | `spanning-tree mst configuration` then `instance <inst> vlan <vlan-ids>` | Moves VLANs out of instance 0 |
| 4 | `revision <version>` (in config-mst) | Must match on every switch in the region |
| 5 (optional) | `name <region-name>` (in config-mst) | Default name is an empty string |

Example 4-1 (SW1): `root primary` for MST 0, 1 and 2; name ENTERPRISE_CORE, revision 2, instance 1 = VLANs 10,20, instance 2 = VLAN 99. Instance 0 keeps everything else.

---

## MST verification

| Command | What it shows |
|---|---|
| `show spanning-tree mst configuration` | Name, revision, number of instances, and which VLANs are in each instance. Instance 0 lists **all** other VLANs (1-9,11-19,21-98,100-4094), whether they exist on the switch or not. |
| `show spanning-tree` | One block per instance (MST0, MST1...), protocol **mstp**. Shows instances, **not** VLAN numbers. Priority = configured priority **+ instance number** (24576 + 1 = 24577 for MST1), same idea as the sys-id-ext per VLAN. |
| `show spanning-tree mst [inst]` | Compact view **with the VLANs mapped** next to each instance, easier for troubleshooting. MST0 says "Root this switch for the **CIST**". |
| `show spanning-tree mst interface <int>` | One port across all instances: role, state, cost, priority and VLANs per instance, plus edge port, link type, **Boundary** (internal or not), BPDU guard/filter, BPDUs sent/received. |

Costs show as **20000** for a 1 Gb port (long path cost) in MST.

---

## Day 24 lab proof (CML, IOSvL2)

- PVST+ on 5 VLANs: SW3 ran **5 trees** (VLAN 1, 10, 20, 30, 40). With every priority at default, the **lowest MAC** won the root for VLAN 30.
- After MST (region ENCOR, rev 1, instance 1 = 10,20, instance 2 = 30,40): **3 instances** (MST0, MST1, MST2). VLAN 1 stays in **instance 0, the IST**.
- SW1 root for MST1, SW2 root for MST2: **SW3 blocks a different uplink per instance**, so both uplinks carry traffic. SW4 blocks Gi0/1 in both (its two links go to the same switch, SW2).
- MST0 still picked its root by lowest MAC, because no `spanning-tree mst 0` priority was set.
- Old `spanning-tree vlan 1 priority` lines stay in the config but do nothing in MST mode.

---

## DIKTA misses (2026-11-11, 4/7 before reading)
- **Q1:** **A and B.** MST load balances traffic for specific VLANs (VLANs go to instances with different topologies) and cuts the CPU and memory needed for many VLANs (many VLANs share one instance). Not C (MAC table scaling).
- **Q4:** **False.** The MST root bridge does **not** advertise the VLAN-to-instance mappings. Each switch's own local config maps VLANs to instances; the IST carries the BPDUs that build the topology.
- **Q5:** **False.** The MST configuration version is **not** locally significant. Name, revision and VLAN-to-instance mappings must match on every switch in the region.
