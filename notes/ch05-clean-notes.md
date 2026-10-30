# Ch 5 - VLAN Trunks and EtherChannel Bundles (clean notes)

Related: Ch 1 (VLANs, trunks, 802.1Q), Ch 2 (STP: why a second link gets blocked)

**Status:** complete, pp 94-123 (Days 9-14).

---

## VLAN Trunking Protocol (VTP)
**Key Topic:** Cisco proprietary. Before APIs, adding a VLAN to 100 switches meant logging in to 100 switches. With VTP you create the VLAN **once on a VTP server** and it is sent to every **client** in the same **VTP domain**.

### VTP roles (four)
| Role | Creates/edits VLANs? | Applies updates? | Forwards updates? |
|---|---|---|---|
| **Server** | Yes | Yes | Yes |
| **Client** | **No** (can't configure VLANs locally) | Yes | Yes |
| **Transparent** | Local only | **No** | **Yes** (passes them on) |
| **Off** | Local only | No | **No** |

There is **no "proxy" role.** Transparent vs off: both keep their own VLANs, but transparent still forwards VTP to the next switch and off does not.

### VTP versions
- **v1** is the default. v1 and v2 only carry VLANs **1-1005**.
- **v3** carries the full range **1-4094**. Most switches can run v3.
- A domain can have **more than one server**. Servers take updates from other servers just like clients do.
- In **v3** only the **primary server** can add or remove VLANs: `vtp primary` (exec command, not config mode).

### VTP advertisements
VTP is sent as **multicast** across **trunk** links.
- **Summary:** every **300 seconds** or when a VLAN is added/removed/changed. Has the version, domain, **configuration revision number** and time stamp. It does **not** list the VLANs.
- **Subset:** sent after a VLAN change. Has the actual VLAN details.
- **Client request:** a client asks for the subset. Happens when a switch sees a summary with a **higher revision** than its own.

### VTP configuration
```
vtp version {1 | 2 | 3}
vtp domain <name>          ! changing the domain resets the revision to 0
vtp mode {server | client | transparent | off}
vtp password <password>    ! optional, recommended
vtp primary                ! v3 only, exec mode, on the server
```
Verify: `show vtp status` (version, domain, mode, number of VLANs, configuration revision). Each VLAN created on the server adds 1 to the revision (3 VLANs: 1 -> 4). Ignore the MST and UNKNOWN feature lines for ENCOR.

### The VTP disaster
**Key Topic:** **Reset the revision number to 0** on any switch before it joins a VTP domain. If a moved switch has a **higher revision**, the other switches take its VLAN database. If that database is missing VLANs, **those VLANs are deleted across the whole domain.** Easy reset: change the VTP domain name.

---

## Dynamic Trunking Protocol (DTP)
**Key Topic:** Cisco protocol that lets two switch ports **negotiate a trunk**. DTP is sent every **30 seconds**. **The VTP domain must match** on both switches for DTP to work.

| Mode | Command | Behaviour |
|---|---|---|
| **Trunk** | `switchport mode trunk` | Always trunk, and still sends DTP |
| **Dynamic desirable** | `switchport mode dynamic desirable` | Acts as access, **sends and listens** for DTP, becomes trunk if it agrees |
| **Dynamic auto** | `switchport mode dynamic auto` | Acts as access, **only responds** to DTP. **Default on Catalyst** |

| | Trunk | Desirable | Auto |
|---|---|---|---|
| **Trunk** | Trunk | Trunk | Trunk |
| **Desirable** | Trunk | Trunk | Trunk |
| **Auto** | Trunk | Trunk | **Access** |

**Auto + auto = no trunk.** Nobody starts the negotiation.

Verify: `show interfaces [id] trunk`. The Mode column shows **auto**, **desirable**, or **on** (static trunk).

### Turning DTP off
**Key Topic:**
```
switchport mode trunk
switchport nonegotiate
```
`switchport nonegotiate` stops the port from negotiating, so it won't form a trunk with a desirable or auto port. `show interfaces <id> switchport` then shows **Negotiation of Trunking: Off**.

**Best practice:** set both ends statically (`switchport mode access` or `switchport mode trunk`) so there's no guessing.

---

## EtherChannel Bundles

### Why
A link is full. A faster port usually isn't available. A second cable seems easy, but **STP blocks the second link** to stop a loop.

**EtherChannel** joins physical links into **one logical link**. Other names: **port channel**, EtherChannel bundle. The standard is **IEEE 802.3ad** link aggregation.
- The physical ports are **member interfaces**.
- **STP sees only the logical link**, so nothing is blocked. Bandwidth = all active members together, load balanced.
- Works for **Layer 2 (access or trunk)** and **Layer 3 (routed)** ports. Not loopbacks.
- Other Cisco platforms (not Catalyst) only use the name "port channel".

**Main benefits:** more bandwidth, and **fewer topology changes**. A member link going down doesn't trigger an STP or routing recalculation while at least one member is still up.

### Static (on) vs dynamic
- **Static (`mode on`):** **no health check.** If the link degrades but line protocol stays up, the switch keeps sending traffic down it and you get random packet loss.
- Example: switches joined through **DWDM**, taps, IPS or Layer 2 firewalls. A failure in the middle (between DWDM-1 and DWDM-2) is not seen by the switches, because their own ports to the DWDM gear are still up. A static channel keeps load balancing onto the dead path.
- A **dynamic protocol** (LACP or PAgP) notices the missing packets and removes that member. Most engineers prefer dynamic.

### PAgP vs LACP
**Key Topic:** Both ends must use the **same protocol**.

| | **PAgP** | **LACP** |
|---|---|---|
| Who made it | **Cisco proprietary** (came first) | **Open standard** (IEEE) |
| Multicast MAC | 0100:0CCC:CCCC (protocol code 0x0104) | 0180:C200:0002 |
| Starts the channel | **Desirable** | **Active** |
| Only responds | **Auto** | **Passive** |
| Doesn't form | auto + auto | passive + passive |

Rule: **at least one side must start it** (desirable or active).

### Configuration
**Key Topic:**
```
interface range gi1/0/1-2
 channel-group 1 mode on                          ! static
 channel-group 1 mode {active | passive}          ! LACP
 channel-group 1 mode {auto | desirable} [non-silent]   ! PAgP
interface port-channel 1
 switchport mode trunk                            ! settings go on the port channel
```
- **PAgP silent mode** is the default: lets a port form a channel with a device that isn't PAgP capable and rarely sends packets. **`non-silent`** makes the port wait for PAgP packets first. Use it between PAgP switches; the link comes up faster.
- Put members in the right mode **first** (Layer 2, or `no switchport` for Layer 3). The **member type decides** whether the channel is Layer 2 or Layer 3.
- All other settings go on the **port-channel interface**.
- While only one side is configured, the log shows `Gi1/0/1 suspended: LACP currently not enabled on the remote port`.

### Verifying
`show etherchannel summary` - check the port-channel status first. It should be **SU**. **Flags are case sensitive.**

Port-channel (logical) flags:
| Flag | Meaning |
|---|---|
| **U** | In use, working |
| **D** | Down |
| **M** | Not in use, **min-links not met** |
| **S** | Layer 2 |
| **R** | Layer 3 (routed) |

Member flags:
| Flag | Meaning |
|---|---|
| **P** | Bundled, forwarding |
| **H** | **Hot-standby** (max-bundle reached), LACP only |
| **I** | Individual (stand-alone), no LACP seen |
| **s** | Suspended |
| **w** | Waiting to be aggregated |
| **r** | Module removed |

Other commands:
- `show interfaces port-channel <id>` - normal interface stats, member list, **BW = sum of active members** (2 x 1 Gbps = 2,000,000 Kbit). QoS and routing costs follow this bandwidth.
- `show etherchannel port` - detailed per member: mode, LACP/PAgP flags, priority, partner info, **Load** (hex). Lots of output.
- `show lacp neighbor [detail]` - neighbor system ID, priority, fast/slow.
- `show lacp sys-id` - local LACP system priority + MAC. Use it to check all members go to the **same** device.
- `show pagp neighbor` - partner name, device ID, partner port.
- `show lacp counters` / `show pagp counters` - sent and received should **both increase**. If Sent goes up and Recv doesn't, look at the physical link or the remote config. Clear with `clear lacp counters` / `clear pagp counters`.

---

## Advanced LACP Options
These are **LACP only.** PAgP doesn't have them.

### LACP fast
- Normal LACP: a packet every **30 s**. Three missed = **90 s** before a bad member is removed.
- **LACP fast:** a packet every **1 s**, so the member is removed in **3 s**.
- `lacp rate fast` on the **member interfaces**. **Both switches must match** (all fast or all slow). Check with `show lacp internal` (flag **F** = fast, **S** = slow).

### Minimum links
- By default the port channel comes up with **one** member.
- `port-channel min-links <n>` on the port-channel interface. Below n members, the channel goes **down** and shows **(SM)**: `MINLINKS_NOTMET`.
- Only needs to be on one side, but configure both to make troubleshooting easier.

### Maximum links
- `lacp max-bundle <n>` on the port-channel interface. Extra members become **Hot-standby (H)**.
- Used to keep active links at **powers of two** (2, 4, 8) so the hash spreads traffic evenly.
- Only needs to be on the **primary switch**, but configure both sides.

### Who decides which links stay active
- **LACP system priority** picks the **primary switch**: **lower wins**. `lacp system-priority <n>` (global). Default 32768. If tied, lower MAC.
- The primary switch picks active members by **LACP port priority**: **lower wins**, then **lower interface number**. `lacp port-priority <n>` (interface).
- Example: max-bundle 1, set Gi1/0/2 port-priority 1 -> Gi1/0/2 becomes P, Gi1/0/1 becomes H.

---

## Troubleshooting EtherChannel
**Key Topic:** a port channel is one logical interface, so **every member must match**:
- **Port type:** all Layer 2 or all Layer 3
- **Port mode:** all access or all trunk
- **Native VLAN** (trunks)
- **Allowed VLANs** (trunks)
- **Speed**
- **Duplex**
- **MTU** (Layer 3 members)
- **Load interval**
- **Storm control**

Also check:
- Each member link goes between the **same two devices** only.
- All member ports are active (not shut).
- Modes work together: on + on, LACP with at least one **active**, PAgP with at least one **desirable**.
- Everything matches except LACP port priority.
- LACP/PAgP packets are sent **and received** on both sides.

---

## Load Balancing
**Key Topic:** **No round robin per packet.** The switch runs a **hash** on header fields, and the same flow always uses the same member link. Global command:
```
port-channel load-balance <hash>
show etherchannel load-balance
```
Hash options: src-mac, dst-mac, src-dst-mac, src-ip, dst-ip, src-dst-ip, src-dest-ip-only, src-port, dst-port, src-dst-port, src-mixed-ip-port, dst-mixed-ip-port, src-dst-mixed-ip-port. Newer IOS XE can add the VLAN.

- Uneven use? Change the hash.
- Channel to a **router**: don't hash on MAC. The router's MAC is always the same, so every frame lands on one link. Use IP or TCP/UDP ports.
- `show etherchannel load-balance` lists what's used for **non-IP, IPv4 and IPv6** (example: src-dst-mixed-ip-port).
- Hash is binary: use **2, 4 or 8** members. **3 links balance badly.**
- See per-link load in `show etherchannel port` (Load, in hex).

---

## Commands I need to know

| Task | Command |
|---|---|
| VTP version / domain / mode | `vtp version {1\|2\|3}`, `vtp domain <name>`, `vtp mode {server\|client\|transparent\|off}` |
| VTP v3 primary server | `vtp primary` (exec) |
| DTP actively try trunk | `switchport mode dynamic desirable` |
| DTP respond only | `switchport mode dynamic auto` |
| Turn off DTP | `switchport nonegotiate` |
| Static EtherChannel | `channel-group <id> mode on` |
| LACP | `channel-group <id> mode {active\|passive}` |
| PAgP | `channel-group <id> mode {auto\|desirable} [non-silent]` |
| LACP rate | `lacp rate {fast\|slow}` |
| Min links | `port-channel min-links <n>` |
| Max links | `lacp max-bundle <n>` |
| LACP system priority | `lacp system-priority <n>` |
| LACP port priority | `lacp port-priority <n>` |
| Hash | `port-channel load-balance <hash>` |
| Show | `show vtp status`, `show interfaces [id] trunk`, `show interfaces <id> switchport`, `show etherchannel summary`, `show interfaces port-channel <id>`, `show etherchannel port`, `show lacp neighbor [detail]`, `show lacp sys-id`, `show lacp counters`, `show lacp internal`, `show pagp neighbor`, `show pagp counters`, `show etherchannel load-balance` |

## Key terms to define from memory
Dynamic Trunking Protocol (DTP), EtherChannel bundle, LACP interface priority, LACP system priority, load-balancing hash, member links, VLAN Trunking Protocol (VTP)

## DIKTA misses (2026-10-21: 5/11, retake 2026-10-27: 9/11)
- **Q2:** **False.** The summary advertisement has the revision number, not the VLANs. The **subset** carries the VLAN changes.
- **Q3:** **False.** A domain can have **many** VTP servers (in v3 only one is **primary**).
- **Q4:** a moved switch with a higher revision sends its VLAN database and **VLANs get deleted** domain-wide.
- **Q8 (partial):** EtherChannel works on **access, trunk and routed** ports (A, B, C). Not loopback.
- **Q9:** benefits = **more bandwidth** and **fewer topology changes** (A, B). Not per-packet load balancing.
- **Q11:** **False.** Only **LACP** can set the maximum members (`lacp max-bundle`). PAgP can't.

## Lab notes
- Advanced LACP commands (`lacp rate fast`, `port-channel min-links`, `lacp max-bundle`) didn't all run on the CML switches on Day 13. Still to be tested in a later lab, on each CML switch image.
