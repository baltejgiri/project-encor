# Ch 3 - Advanced STP Tuning (clean notes)

Related: Ch 2 (STP and RSTP basics: root election, root path cost, port roles), Ch 4 (MST), Ch 5 (EtherChannel)

**Status:** complete, pp 58-78 (Days 22-23). DIKTA before reading 4/6 (2026-11-09). Post-chapter DIKTA retake still to do.

---

## STP Topology Tuning

A good design decides **where the root bridge sits** and **which ports block**, instead of leaving it to the lowest MAC address. Things to weigh: the hardware, resiliency and the topology itself. The book uses the same five-switch topology as Chapter 2.

### Placing the root bridge
**Key Topic**

Put the root on a **core switch**, with a **secondary root** next to it, so the tree changes as little as possible when something fails:
- lower the priority on the root as far as it goes
- set the secondary root slightly higher than the root
- ideally raise the priority on every other switch

Two ways to set it:

| Command | What it does |
|---|---|
| `spanning-tree vlan <id> priority <0-61440>` | Sets the number directly. Steps of **4096** only. |
| `spanning-tree vlan <id> root primary` | Script: sets **24,576** |
| `spanning-tree vlan <id> root secondary` | Script: sets **28,672** |

- If another switch is already at 24,576 or lower and would still win, the `root primary` script goes **lower** to try to become root (4096 below the current root).
- It is a script: it runs once and writes a number into the config. It does not keep watching.
- `diameter <n>` tunes the STP timers for the number of Layer 2 hops to the furthest switch. Only the root needs it: the timers travel in the root's BPDUs.

Examples 3-1 and 3-2: SW1 goes 32,769 -> 24,577 with `root primary`, SW2 goes 32,769 -> 28,673 with `root secondary` (the +1 is the system ID extension = VLAN 1).

**Where to put the root:** keep the hops to the furthest switch low, think about which links will block, and pick a switch that can handle traffic crossing it. Usually at the **Layer 2/Layer 3 boundary**.

**Root bridge values (Key Topic):** the best protection against a wrong device taking the root is **priority 0 on the primary** and **4096 on the secondary**, plus **root guard**.

### Root path cost
**Key Topic**

- A switch advertises **its own cost to the root** in its BPDUs. It does **not** add the cost of the port it sends the BPDU out of.
- The **receiving** switch adds the cost of the port the BPDU **came in on**.

Figure 3-2: SW1 advertises 0. SW3 receives it on a cost-4 port, so its cost is 4. SW3 advertises 4 to SW5, SW5 adds its own port cost 4 = **8**.

The root bridge shows no root cost in `show spanning-tree vlan 1`: it says "This bridge is the root".

### Changing port cost
`spanning-tree [vlan <id>] cost <cost>` on the interface.
- Lower the cost on an alternate port to make it forward, or raise the cost on a forwarding port to make it block.
- Without `vlan`, it changes the cost for **all VLANs** on that port.

Example 3-4: SW3 sets Gi1/0/1 (its root port) to cost 1. Now SW3 advertises 1 and SW2 sees 1 + 4 = 5 via SW3, while SW3 sees 4 + 4 = 8 via SW2. SW3 has the better path, so **SW3's Gi1/0/2 becomes designated** and **SW2's Gi1/0/3 becomes alternate (blocking)**. Changing a cost can move the blocked port to a different switch.

### Changing port priority
Port priority only matters when there are **several links between the same two switches** and cost and bridge ID tie. Then the tie-breakers are **port priority, then port number**, and both come from the **upstream** switch (the one closer to the root).

- Default port priority **128**, lower is better, shown as `128.5` (priority.port number).
- `spanning-tree [vlan <id>] port-priority <priority>` on the **upstream** switch's port.

Example 3-6/3-7: SW5 has two links to SW4. SW4 sets Gi1/0/6 to priority 64, so SW5's port facing Gi1/0/6 (Gi1/0/5) becomes the root port and Gi1/0/4 goes to alternate.

---

## Additional STP Protection Mechanisms

### Why loops are so bad
Layer 2 has **no TTL**, so a looping frame never dies. Broadcast and multicast go out every port and keep circling.
Symptoms:
- **high CPU** and **low free memory**
- the MAC table keeps moving MACs between ports
- everything slows down; switches can crash

Common causes:
- STP disabled on a switch
- a load balancer sending the same MAC out several ports
- a virtual switch bridging two physical ports (virtual switches usually don't run STP)
- a user plugging in a dumb switch or hub

Catalyst switches log a **MAC flap**:
`%SW_MATM-4-MACFLAP_NOTIF: Host 70df.2f22.b8c7 in vlan 1 is flapping between port Gi1/0/3 and port Gi1/0/2`
When you see it, check STP on every switch carrying that VLAN.

### Root guard
**Key Topic**

- Per port. Stops a port from **ever becoming a root port**, so a downstream (rogue or misconfigured) switch can't become root.
- If a **superior BPDU** arrives, the port goes **root inconsistent** for that VLAN. It acts like listening: **no traffic**.
- It comes back on its own when the superior BPDUs stop.
- Goes on **designated ports toward switches that should never be root**.
- `spanning-tree guard root`

Placement in Figure 3-1: SW2 Gi1/0/4 (to SW4) and SW3 Gi1/0/5 (to SW5). SW4 and SW5 can never be root, but SW2 can still reach SW1 through SW3 if the SW1-SW2 link fails (that path comes in on SW2's Gi1/0/3, which has no root guard).

### STP portfast
**Key Topic**

A host has one link, so TCNs from host ports are pointless and make the network less stable. Portfast:
- stops **TCN generation** on access ports
- skips listening and learning, so the port **forwards right away** (helps DHCP and PXE)
- if a **BPDU** arrives, portfast is removed from that port and it goes through the normal states
- portfast port = RSTP **edge** port (`P2p Edge` in `show spanning-tree`)

| Task | Command |
|---|---|
| One access port | `spanning-tree portfast` |
| All access ports | `spanning-tree portfast default` (warns you about hubs, switches and bridges) |
| Turn it off on one port | `spanning-tree portfast disable` |
| Trunk to a single host | `spanning-tree portfast trunk` (e.g. a server with one NIC running VMs in several VLANs) |

Check: `show spanning-tree interface <if> detail` says "The port is in the portfast mode".

### BPDU guard
**Key Topic**

- A **BPDU** on a portfast port puts it in **err-disabled**: no traffic at all.
- With portfast on every access port, nobody can create a loop by plugging in a switch.
- Normally configured on **all host-facing portfast ports**.

| Task | Command |
|---|---|
| All portfast ports | `spanning-tree portfast bpduguard default` |
| One port | `spanning-tree bpduguard {enable \| disable}` |
| Check one port | `show spanning-tree interface <if> detail` ("Bpdu guard is enabled") |
| See the port down | `show interfaces status` (Status = err-disabled) |

Syslog when it fires:
```
%SPANTREE-2-BLOCK_BPDUGUARD: Received BPDU on port GigabitEthernet1/0/2 with BPDU Guard enabled. Disabling port.
%PM-4-ERR_DISABLE: bpduguard error detected on Gi1/0/2, putting Gi1/0/2 in err-disable state
```

### Error recovery
Err-disabled ports stay down until someone fixes them, unless you turn on recovery:
- `errdisable recovery cause bpduguard`
- `errdisable recovery interval <30-86400>` (default **300 s**)
- `show errdisable recovery` lists the causes and the ports waiting, with time left

If the switch on the other end is still there, the port recovers, gets a BPDU and goes err-disabled again, over and over (`%PM-4-ERR_RECOVER`, then BLOCK_BPDUGUARD again).

### BPDU filter
**Key Topic**

Stops BPDUs going out of a port.
- **Global** `spanning-tree portfast bpdufilter default`: a portfast port sends 10-12 BPDUs when it comes up. If BPDUs come back, the switches work out who is preferred: the preferred one ignores BPDUs it receives but keeps sending; the other one processes BPDUs from the superior switch but stops sending to it.
- **Interface** `spanning-tree bpdufilter enable`: the port sends **no BPDUs at all**, and the far end's BPDU guard usually err-disables its port.
- Book's warning: most designs **don't need** BPDU filter. It adds complexity and risk (it can hide a loop).

Check: `show spanning-tree interface <if> detail | in BPDU|Bpdu|Ethernet` ("Bpdu filter is enabled", BPDU sent/received counters).

### Unidirectional links
On fiber, one strand sends and one receives. If one strand breaks:
- the line protocol can stay **up**
- BPDUs stop arriving on the downstream switch
- it times out its root port and picks another, so a blocked port starts forwarding out the strand that still works: **loop**

Fixes: **loop guard** or **UDLD**.

### STP loop guard
- A **root or alternate** port that stops getting BPDUs goes **loop inconsistent** instead of becoming designated.
- Recovers when BPDUs come back.
- Global `spanning-tree loopguard default` or per port `spanning-tree guard loop`.
- **Not on portfast ports** (conflicts with the root/alternate port logic).
- Log: `%SPANTREE-2-LOOPGUARD_BLOCK: Loop guard blocking port ... on VLAN0001`
- `show spanning-tree` shows `BKN*` and `*LOOP_Inc`

`show spanning-tree inconsistentports` lists every inconsistent port, one line per VLAN (Loop Inconsistent, Root Inconsistent).

### UDLD (Unidirectional Link Detection)
Each switch sends UDLD packets with its system ID and port ID, and the neighbour echoes them back with its own IDs. It never stops.

| Mode | When a frame is not acknowledged |
|---|---|
| **Normal** | the link is "undetermined", the port stays up |
| **Aggressive** | 8 more packets, 1 s apart; still nothing, the port goes into an error state |

| Task | Command |
|---|---|
| All SFP ports | `udld enable [aggressive]` |
| One port | `udld port [aggressive]` |
| Turn off on one port | `udld port disable` |
| Automatic recovery | `udld recovery [interval <s>]` (default 5 min) |
| Check | `show udld neighbors`, `show udld <if>` |

**Both ends** need UDLD. A good link shows **Bidirectional**.

---

## Commands I need to know

| Task | Command |
|---|---|
| Root / backup root | `spanning-tree vlan <id> root {primary \| secondary} [diameter <n>]` or `spanning-tree vlan <id> priority <p>` |
| Port cost | `spanning-tree [vlan <id>] cost <cost>` |
| Port priority (upstream port) | `spanning-tree [vlan <id>] port-priority <p>` |
| Root guard | `spanning-tree guard root` |
| Portfast | `spanning-tree portfast default`, `spanning-tree portfast`, `spanning-tree portfast trunk` |
| BPDU guard | `spanning-tree portfast bpduguard default`, `spanning-tree bpduguard {enable \| disable}` |
| BPDU filter | `spanning-tree portfast bpdufilter default`, `spanning-tree bpdufilter enable` |
| Loop guard | `spanning-tree loopguard default`, `spanning-tree guard loop` |
| Error recovery | `errdisable recovery cause bpduguard`, `errdisable recovery interval <s>` |
| UDLD | `udld enable [aggressive]`, `udld port [aggressive]` |
| Inconsistent ports | `show spanning-tree inconsistentports` |
| UDLD neighbours | `show udld neighbors` |

## Key terms to define from memory
BPDU filter, BPDU guard, root guard, STP portfast, STP loop guard, Unidirectional Link Detection (UDLD)

## DIKTA misses (2026-11-09, 4/6 before reading)
- **Q2:** **False.** The advertised root path cost does **not** include the cost of the port the BPDU goes out of. The receiving switch adds its own port cost.
- **Q4:** BPDU guard: a syslog message, and the port goes **err-disabled** (D).
