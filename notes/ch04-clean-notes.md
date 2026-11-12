# Ch 4 - Multiple Spanning Tree Protocol (clean notes)

Related: Ch 2 (STP and RSTP basics), Ch 3 (Advanced STP Tuning), Ch 5 (EtherChannel)

**Status:** Ch 4 finished. Read pp 80-87 (Day 24) and pp 87-91 (Day 25); notes done for the whole chapter. DIKTA before reading 4/7 (2026-11-11). Post-chapter DIKTA retake still to do.

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

## The one idea that makes the rest of Ch 4 click

**MST builds trees per instance, not per VLAN.** A switch never asks "where does VLAN 30 go?". It asks "where does instance 2 go?", and every VLAN in instance 2 follows that answer.
- The tree is built from **BPDUs on physical links**. It does **not** look at which VLANs a trunk allows or which VLAN an access port is in.
- So if the trunk config and the instance tree disagree, the **tree wins** and the VLAN loses its path. Both misconfigurations below are this one idea.

---

## MST tuning (pp 87-89)

Same knobs as Ch 3, just with `mst <instance>` in front, so you can tune each instance on its own.

| Knob | Command (interface) | Where you set it | Why there |
|---|---|---|---|
| **Port cost** | `spanning-tree mst <inst> cost <cost>` | On the switch **choosing** its root port (downstream) | Cost adds to **your own** root path cost. Lower cost on one uplink = that uplink becomes your root port. |
| **Port priority** | `spanning-tree mst <inst> port-priority <0-240>` (steps of 16, default 128) | On the switch **sending** the BPDU (upstream) | Priority is part of the **sender's** port ID. It only matters as the last tie-breaker: equal cost, same upstream bridge. Lower wins. |

- Ex 4-6: SW3 Gi1/0/1 `mst 0 cost 1`. Before: Gi1/0/1 Root, Gi1/0/2 Altn BLK. After: Gi1/0/2 changed from Altn to **Desg** FWD.
- Ex 4-7: SW4 Gi1/0/5 `mst 0 port-priority 64`. The Prio.Nbr column shows **64.5** instead of 128.5. It changes what SW4 *advertises* on that port, so it only affects the switch on the other end.
- Order of tie-breakers is still the Ch 2 list: lowest root path cost, then lowest sender bridge ID, then lowest sender port priority, then lowest sender port number.

---

## Common MST misconfigurations (pp 89-90)

### 1. VLAN assignment to the IST
- The **IST (instance 0) runs on every link in the region**, whatever VLAN a port is in.
- Fig 4-5: two links between SW1 (root) and SW2. Gi1/0/1 is a trunk carrying VLAN 20 (instance 1), Gi1/0/2 is an **access port in VLAN 10**, and VLAN 10 is in the **IST**.
  - You'd expect PC-A to PC-B (VLAN 10) to use Gi1/0/2.
  - But the IST sees two links to the root, so SW2 blocks one for instance 0. It picks **Gi1/0/2** (worse sender port ID from SW1).
  - Result: VLAN 10's only link is blocked, so VLAN 10 is cut.
- **Fixes:** move VLAN 10 out of the IST into an MSTI, **or** allow the IST VLANs on every inter-switch trunk.

### 2. Trunk link pruning
- Pruning VLANs off trunks is a normal way to load balance in PVST+, **but not inside one MST instance**.
- Fig 4-6: VLANs 10 and 20 in the same instance. A junior engineer prunes VLAN 20 off SW1-SW2 and VLAN 10 off SW1-SW3. Users on SW1 and SW3 lose the servers on SW2: the trunks changed, **the instance tree didn't**.
- **Rule: prune all VLANs of the same MSTI together on a trunk (all or none).** To load balance, put VLANs in different instances and tune cost/priority/root per instance.

---

## MST region boundary (pp 90-91)
**Key Topic**

- **Boundary port** = a port facing a switch in a **different MST region**, or one that receives **802.1D or 802.1w (RSTP) BPDUs**. `show spanning-tree mst interface` shows `Boundary: internal` for ports inside the region.
- **MSTIs never leave the region.** Only the IST talks to the outside, as the **CST**. That's why the region looks like one big switch from outside.
- **PVST simulation:** PVST+/RPVST+ switches don't understand the IST BPDU. So the boundary port sends **one PVST+ BPDU per VLAN, all copied from the IST** (one topology to many VLANs). It starts only when a PVST BPDU arrives on that port.
- Inbound, the boundary does **not** map PVST+ VLANs to MSTIs. It uses only the **VLAN 1** PVST+ BPDU for the IST.

Two designs when mixing MST with PVST+/RPVST+:

| Design | What happens |
|---|---|
| **MST region is the root for all VLANs** (recommended) | Make the IST priority better than any PVST+ switch. Every boundary port floods the same IST info for every VLAN; the PVST+ switch sees one root and does the blocking itself (Fig 4-7). That PVST+ switch can still load balance with per-VLAN cost on its uplinks. |
| **MST region is not the root for any VLAN** | Boundary ports can only forward or block **all VLANs together**, no load balancing (the IST must stay consistent). |

- **PVST simulation check:** if a boundary port gets a **better BPDU for just some VLAN** (the region would be root for some VLANs and not others), the switch blocks the port as **root inconsistent**. It may cut off switches below it, but it keeps the topology loop free.

---

## Day 25 lab proof (CML, IOSvL2)

- Per-instance **cost** on SW4's own uplink moved only instance 2. `show spanning-tree mst 1` was identical before and after, which proved instance 1 didn't move.
- To move instance 1 **without touching SW4**, cost was useless (it's local to SW4). **Port priority on SW2** worked, because SW4's two uplinks tie on cost and the same upstream bridge, so SW2's port ID decides.
- Ticket: one VLAN of an instance pruned off the trunk that instance forwards on. The other VLAN of the same instance kept working, and the instance's other path stayed blocked, so the pruned VLAN had **no path at all**. Exactly Fig 4-6.

---

## Key terms (book list, own words)

| Term | Meaning |
|---|---|
| **CST** (Common Spanning Tree) | One tree for all VLANs (802.1D). In MST, the IST is what the outside world sees as the CST. |
| **IST** (internal spanning tree) | Instance 0. Runs on every port in the region, holds all unmapped VLANs, carries the BPDUs for all instances. |
| **MSTI** (MST instance) | Instances 1-15: a group of VLANs that share one tree inside the region. |
| **MST region** | Switches with the same name, revision and VLAN-to-instance map. |
| **MST region boundary** | A port facing another region or an 802.1D/802.1w/PVST+ switch. |
| **PVST simulation check** | Blocks a boundary port as root inconsistent when it gets a better PVST+ BPDU for some VLANs, to keep the IST consistent. |

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
