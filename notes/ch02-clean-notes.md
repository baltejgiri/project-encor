# Ch 2 - Spanning Tree Protocol (clean notes)

Related: Ch 3 (Advanced STP Tuning: BPDU guard, BPDU filter), Ch 4 (MST), Ch 5 (EtherChannel: STP sees a port channel as one link)

**Status:** complete, pp 36-57 (Days 15, 16, 18, 19 and 20). DIKTA before reading 3/9 (2026-10-29). Post-chapter DIKTA retake still to do.

---

## Why STP exists

Good design adds redundant links and switches. But redundant Layer 2 paths create **loops**:
- **Broadcasts** and **unknown unicast flooding** go out every port, so they circle the loop forever.
- **Layer 2 has no TTL**, so nothing ever drops the looping frame.
- Links fill up and the switch starts dropping frames.
- The **MAC address table flaps**: the same MAC keeps showing up on different ports.
- CPU and memory climb until the switch can crash.

**STP** keeps the redundant links but **blocks** the extra paths so there is only one loop-free path. **RSTP** does the same job with much faster convergence.

---

## STP Fundamentals

Switches find each other by sending and receiving **BPDUs (bridge protocol data units)**. STP picks one **best switch** (the root bridge), runs a tree algorithm from it, and blocks the redundant ports that would make a loop.

STP versions:
- **802.1D**: the original standard, one tree for the whole network (one VLAN)
- **PVST**: Per-VLAN Spanning Tree
- **PVST+**: Per-VLAN Spanning Tree Plus
- **802.1W RSTP**: Rapid Spanning Tree Protocol
- **802.1S MST**: Multiple Spanning Tree Protocol

**Catalyst switches today run PVST+, RSTP or MST.** All three are backward compatible with 802.1D.

> Bridge = switch here. STP was written before switches existed, so the book uses both words for the same thing.

### 802.1D Port States
**Key Topic**

| State | Forwards data? | Learns MACs? | BPDUs | Notes |
|---|---|---|---|---|
| **Disabled** | No | No | No | Port is shut down |
| **Blocking** | No | No | Receives only | Stops the loop. MAC table not touched |
| **Listening** | No | No | Sends + receives | Lasts the **forward delay (15 s)** |
| **Learning** | No | **Yes** | Sends + receives | Lasts the **forward delay (15 s)** |
| **Forwarding** | **Yes** | Yes | Sends + receives | Final state, normal traffic |
| **Broken** | No | No | - | Config or operational problem; discards frames until fixed |

Order a port goes through: **Blocking -> Listening -> Learning -> Forwarding.**
**Blocking to forwarding takes about 30 seconds** with default timers (listening 15 + learning 15).

### 802.1D Port Types (roles)
- **Root port (RP):** the port that points toward the root bridge (upstream). **Only one RP per switch per VLAN.** The root bridge has no RP.
- **Designated port (DP):** sends BPDUs down a link toward downstream switches. **Only one DP per link.**
- **Blocking port:** not forwarding because STP decided it would make a loop.

### STP Key Terms
- **Root bridge:** the top of the tree. Every other switch calculates its path to it. **All its ports are designated ports and forwarding.**
- **BPDU:** sent to the multicast MAC **01:80:c2:00:00:00**. **Two types:**
  - **Configuration BPDU:** used to pick the root bridge, root ports, designated ports and blocking ports. Fields: STP type, root path cost, root bridge ID, local bridge ID, max age, hello time, forward delay.
  - **TCN (Topology Change Notification) BPDU:** tells other switches the Layer 2 topology changed (explained later in the chapter).
- **Root path cost:** total cost of the path from this switch to the root.
- **System priority:** **4 bits**, default **32,768**. Lower = more likely to be root.
- **System ID extension:** **12 bits**, holds the **VLAN number** of the BPDU. Priority + system ID extension are combined in the bridge ID.
- **Root bridge identifier:** root's priority + system ID extension + system MAC.
- **Local bridge identifier:** this switch's priority + system ID extension + system MAC.

**Bridge ID in one line:** priority (4 bits) + VLAN (12 bits) + MAC (48 bits). That's why VLAN 1 shows priority **32769** (32768 + 1) and VLAN 10 shows **32778**. Because only 4 bits are left for priority, you can only set it in steps of **4096**.

### STP Timers
| Timer | Default | What it does | Command |
|---|---|---|---|
| **Hello** | **2 s** (1-10) | How often a BPDU is sent out a port | `spanning-tree vlan <id> hello-time <s>` |
| **Max age** | **20 s** | How long a port keeps the last BPDU info. If BPDUs stop, the switch trusts the old info until max age runs out | `spanning-tree vlan <id> max-age <s>` |
| **Forward delay** | **15 s** (4-30) | Time spent in **each** of listening and learning | `spanning-tree vlan <id> forward-time <s>` |

### Spanning Tree Path Cost
**Key Topic:** Each interface has an STP cost based on speed. The root path cost = **sum of the costs** of the interfaces on the way to the root. Lower total wins.

- **Short mode:** 16-bit value, the original method and still the default on most switches.
- **Long mode:** 32-bit value with a 20 Tbps reference, built for faster links. Moving to long mode depends on the platform and OS version.

| Link speed | Short mode | Long mode |
|---|---|---|
| 10 Mbps | 100 | 2,000,000 |
| 100 Mbps | 19 | 200,000 |
| **1 Gbps** | **4** | 20,000 |
| 10 Gbps | 2 | 2000 |
| 20 Gbps | 1 | 1000 |
| 100 Gbps | 1 | 200 |
| 1 Tbps | 1 | 20 |
| 10 Tbps | 1 | 2 |

Short mode can't tell 20 Gbps, 100 Gbps and faster links apart (all cost 1). That's why long mode exists.

```
spanning-tree pathcost method long
```
Use the **same method on every switch** in the Layer 2 domain, and audit before changing it, or the topology won't be consistent.

---

## Building the STP Topology (pp 41-47)

### Root bridge election
1. A switch boots and assumes **it is the root**, using its own bridge ID as the root bridge ID.
2. It listens to its neighbors' configuration BPDUs:
   - **Inferior** to its own: ignored.
   - **Preferred** over its own: it updates its BPDUs with the new root bridge ID and the new root path cost.
3. This repeats until every switch agrees on the root.

**What wins:** lowest priority, then lowest system MAC. Older switches often have lower MACs, so without tuning an old switch can become the root by accident.

**Why VLAN 1 shows 32769:** the priority in the BPDU is the priority **plus the sys-id-ext (the VLAN number)**. 32768 + 1 = 32769, and VLAN 10 shows 32778.

### Root path cost
- The root's root path cost is always **0**.
- A BPDU carries the cost to reach the root. It does **not** include the cost of the port it is sent out of.
- The **receiving** switch adds the cost of the port it received the BPDU on.
- Example with 1 Gbps links (cost 4): SW1 advertises 0, SW3 ends up with 4, SW3 advertises 4, SW5 ends up with 8.

### Locating root ports
**Key Topic:** a switch picks its root port (RP) in this order, moving on only if there is a tie:

| # | Lowest value wins | Whose value |
|---|---|---|
| 1 | Path cost to the root | Local total |
| 2 | System priority | Advertising switch |
| 3 | System MAC | Advertising switch |
| 4 | Port priority | Advertising switch (multiple links to the same switch) |
| 5 | Port number | Advertising switch (multiple links to the same switch) |

Steps 4 and 5 use the **upstream** switch's port values, read from the BPDUs it sends. Changing port priority on the downstream switch does not move its root port.

To find the root in a real network: run `show spanning-tree root`, use CDP or LLDP to see which switch is on the root port, connect to it, and repeat until the root cost is 0.

### Locating blocked designated ports
After the root and root ports are known, every other port is a designated port (DP). If two **non-root** switches meet on designated ports, one end has to block.

**Key Topic:** order of comparison:
1. The port is a DP, not an RP.
2. Lower path cost to the root forwards. Higher cost blocks.
3. Lower system priority forwards. The local port blocks if the remote priority is lower.
4. Lower system MAC forwards. The local port blocks if the remote MAC is lower.

The book's example: SW2 and SW3 tie on cost and priority, and SW2 has the lower MAC, so **SW3's** port blocks. SW5 doesn't check port numbers or priorities for its two links to SW4 because SW4 is not in its root path.

### Reading show spanning-tree
`show spanning-tree [vlan <id>]` has three parts: the root bridge, the local bridge, and the port table.

- On the root bridge the output says "This bridge is the root" and all ports are designated.
- `show spanning-tree root` on the root shows cost 0 and an **empty** Root Port field.
- A blocked port shows as **Altn BLK**: an alternate path to the root if the root port fails.
- Port types: **P2p** is a full-duplex link to another switch, **P2p Edge** is a port with PortFast.
- ***TYPE_Inc** means a configuration mismatch with the neighbor, usually the port type or the port mode (access vs trunk).

## Verification of VLANs on Trunk Links (p 48)
`show spanning-tree` lists every VLAN on every port, which is a lot on trunks. To look at one port:

```
show spanning-tree interface gi1/0/1
show spanning-tree interface gi1/0/1 detail
```

- The short version lists each VLAN's role, state, cost and port ID on that port.
- `detail` adds port cost, port priority, transitions to forwarding, link type, the designated bridge and port, and **BPDUs sent and received** per VLAN.
- A root port sends almost no BPDUs and receives many, because configuration BPDUs flow **from the root toward the edge**.
- VLAN missing from a trunk's output? Check the trunk config first. A common cause is the allowed VLAN list (Ch 5).

## STP Topology Changes (pp 49-50)
**Key Topic:** a topology change is a switch failure, a link failure or a link becoming active. In a stable network, configuration BPDUs only flow down from the root. A change sends a message the other way:

1. The switch that detects the link change sends a **TCN BPDU out its root port**.
2. An upstream switch **acknowledges** it and forwards the TCN out its own root port.
3. The root floods a **configuration BPDU with the Topology Change flag** set to all switches.
4. Every switch changes its **MAC address timer from 300 s to the forward delay (15 s)**.
5. MACs quiet for 15 s are flushed, active ones stay. The timer goes back to 300 s after the second configuration BPDU.

**Why flush:** so a switch doesn't keep sending traffic to a host through a port that no longer reaches it.
**Side effect:** more unknown unicast flooding while the table rebuilds.

TCNs are per VLAN, so more hosts in a VLAN means more chances of a TCN and more hosts affected. PortFast (Ch 3) reduces them.

### Tracing TCNs
```
show spanning-tree vlan 10 detail
```
Shows the **number of topology changes**, how long ago the last one happened, and **which interface** it came from. A sudden or continuous rise points to a flapping port or an event on a connected switch.

To find the source: look at the interface it came from. If it goes to a host, you found it. If it goes to a switch, connect there (CDP or your documentation) and run the command again.

## Converging with Direct Link Failures (pp 50-52)
**Direct failure:** Layer 1 signaling brings the port down (power loss, reboot, cable pulled), so STP knows right away.

The book's topology: SW1 is the root, SW2 Gi1/0/3 is designated, and SW3 Gi1/0/2 is blocking.

| Scenario | Link that fails | Impact | Who waits for what | Total |
|---|---|---|---|---|
| 1 | SW2-SW3 | None: traffic already goes through SW1 | Nothing. SW2 and SW3 both send a TCN | No outage |
| 2 | SW1-SW3 | SW3 cut off | SW3 listening 15 + learning 15, **no max age** | **30 s** |
| 3 | SW1-SW2 | SW2 cut off | SW3 max age 20, then SW2 listening 15 + learning 15 | **50 s** |

**Scenario 2, the switch that lost its RP has the blocked port:**
- SW3's root port goes down, so it removes the best BPDU it had from SW1 at once. It can't send a TCN because its root port is down.
- SW1 is the root, so it doesn't send a TCN. It sends the configuration BPDU with the Topology Change flag.
- SW3 doesn't need max age. It starts listening and learning on Gi1/0/2, which becomes the RP.

**Scenario 3, the blocked port is on the other switch:**
- SW2 loses its only root port, assumes it is the root, and advertises its own inferior BPDUs to SW3.
- SW3 discards them because it still gets superior BPDUs from SW1. Its blocked port can't relay SW1's BPDU to SW2.
- SW3's **max age (20 s)** expires, and Gi1/0/2 goes from blocking to listening. It can now forward SW1's BPDU to SW2.
- SW2 sees it is superior, makes Gi1/0/3 the RP and goes through listening and learning.

## Indirect Failures (pp 52-53)
**Indirect failure:** the link stays up, but STP traffic is impaired, filtered or corrupted. No port goes down, so **timers** have to detect it.

The book's example, SW1-SW3 impaired:
1. SW3 stops getting configuration BPDUs on its RP but **keeps the cached entry**. It still discards SW1's BPDUs arriving through SW2 on its blocked port.
2. Max age expires and flushes the cached entry. Gi1/0/2 goes from blocking to listening.
3. SW2 keeps advertising SW1's BPDUs toward SW3.
4. SW3 receives one on Gi1/0/2, marks it the RP, and continues through listening and learning.

**Total: 50 s** (max age 20 + listening 15 + learning 15).

| Failure | Does the switch see the port go down? | Max age? | Time |
|---|---|---|---|
| Direct, blocked port on the same switch | Yes | No | 30 s |
| Direct, blocked port on the other switch | Yes | Yes, on the other switch | 50 s |
| Indirect | No | Yes | 50 s |

## Why 802.1D wasn't enough (p 53)
802.1D has one topology tree, which doesn't scale when larger networks want different trees per VLAN for load balancing and traffic steering. Cisco made **PVST** and **PVST+** for that. Those ideas, plus faster convergence, went into **IEEE 802.1W (RSTP)**.

---

## RSTP (802.1W) Port States (p 54)
**Key Topic**

RSTP has only **three** states:

| State | Forwards data? | Learns MACs? | Notes |
|---|---|---|---|
| **Discarding** | No | No | Replaces 802.1D **disabled, blocking and listening** |
| **Learning** | No (BPDUs only) | Yes | |
| **Forwarding** | Yes | Yes | Final state |

A switch tries an **RSTP handshake** with whatever is on the other end. No handshake = the other side is treated as non-RSTP and the port falls back to **802.1D timing**. That is why a PC (no handshake) still waits about **30 s** after the link comes up, unless the port is portfast/edge (Ch 3).

## RSTP Port Roles (p 54)
- **Root port (RP):** toward the root (or upstream switch). One per VLAN per switch.
- **Designated port (DP):** sends and forwards toward downstream switches and devices. One active DP per link.
- **Alternate port:** a second path toward the root **through a different switch** (blocking, ready to take over).
- **Backup port:** a redundant link onto the **same shared segment** (same collision domain, usually a hub).

## RSTP Port Types (p 54)
- **Edge port:** a host port that can't make a loop. Same thing as **portfast** (Ch 3).
- **Non-edge port:** any port that has received a BPDU.
- **Point-to-point port:** connects to another RSTP switch at **full duplex** (full duplex means only two devices on the link, the quickest way to tell it's a switch).

Hubs only do **half duplex**, so a half-duplex port must use the old 802.1D states.

## Building the RSTP Topology (p 55)
**Key Topic**

RSTP adds switches with a **synchronization** handshake instead of waiting on timers:
1. The two switches check the link is **point-to-point** (full duplex).
2. Each sends a **proposal** (in a configuration BPDU): "my port should be the DP for this segment".
3. Only one DP per segment, so they compare bridge IDs (lowest priority, then lowest MAC). SW1 wins over SW2.
4. The **inferior** switch (SW2) makes its port the **RP** and moves **all its non-edge ports to discarding**. Local switching on those ports stops.
5. SW2 sends an **agreement** (configuration BPDU) back to the root: sync is happening.
6. SW2's RP goes to **forwarding**, and SW1's DP goes to forwarding too.
7. SW2 repeats the process with its own downstream switches.

## RSTP Convergence (p 55)
- RSTP ages out port information after **3 missed hellos**: **6 s** with default timers, instead of the 20 s Max Age.
- With the proposal/agreement handshake, ports go from discarding to forwarding almost at once.
- If a downstream switch **doesn't answer the proposal**, the port falls back to **802.1D** behaviour to avoid a loop.

## Commands I need to know

| Task | Command |
|---|---|
| Long-mode path cost | `spanning-tree pathcost method long` |
| Hello timer | `spanning-tree vlan <id> hello-time <1-10>` |
| Max age | `spanning-tree vlan <id> max-age <s>` |
| Forward delay | `spanning-tree vlan <id> forward-time <4-30>` |
| Show the root bridge | `show spanning-tree root` |
| See the tree for one VLAN | `show spanning-tree vlan <id>` |
| One interface only | `show spanning-tree interface <if> [detail]` |
| Topology change count, age and source | `show spanning-tree vlan <id> detail` |

## Key terms to define from memory
bridge protocol data unit (BPDU), configuration BPDU, designated port (DP), forward delay, hello time, local bridge identifier, Max Age, root bridge, root bridge identifier, root path cost, root port, system priority, system ID extension, topology change notification (TCN)

## DIKTA misses (2026-10-29, 3/9 before reading)
- **Q1:** there are **two** BPDU types: configuration and TCN.
- **Q3:** 802.1D short-mode cost for **1 Gbps = 4** (19 is 100 Mbps).
- **Q5:** a port stays in **listening for 15 s** (the forward delay).
- **Q6:** after a configuration BPDU with the topology change flag, switches **flush the old MAC addresses** from the table (not all of them).
- **Q7 (partial):** RSTP has no **blocking** and no **listening** state (both A and B).
- **Q9:** **False.** RSTP does not wait for the whole network to converge before forwarding.
