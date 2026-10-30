# Ch 2 - Spanning Tree Protocol (clean notes)

Related: Ch 3 (Advanced STP Tuning: BPDU guard, BPDU filter), Ch 4 (MST), Ch 5 (EtherChannel: STP sees a port channel as one link)

**Status:** pp 36-41 read (Day 15 + Day 16). Next session starts at **Building the STP Topology** (p 41).

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

## Commands I need to know (so far)

| Task | Command |
|---|---|
| Long-mode path cost | `spanning-tree pathcost method long` |
| Hello timer | `spanning-tree vlan <id> hello-time <1-10>` |
| Max age | `spanning-tree vlan <id> max-age <s>` |
| Forward delay | `spanning-tree vlan <id> forward-time <4-30>` |
| Show the root bridge | `show spanning-tree root` |

## DIKTA misses (2026-10-29, 3/9 before reading)
- **Q1:** there are **two** BPDU types: configuration and TCN.
- **Q3:** 802.1D short-mode cost for **1 Gbps = 4** (19 is 100 Mbps).
- **Q5:** a port stays in **listening for 15 s** (the forward delay).
- **Q6:** after a configuration BPDU with the topology change flag, switches **flush the old MAC addresses** from the table (not all of them). *Section not read yet.*
- **Q7 (partial):** RSTP has no **blocking** and no **listening** state (both A and B). *Section not read yet.*
- **Q9:** **False.** RSTP does not wait for the whole network to converge before forwarding. *Section not read yet.*
