# Ch 1 – Lab 1: Spaced Repetition Flashcards

**Lab:** VLAN Trunking
**Completed:** 2026-05-26
**Score:** 10/12 (Q1 bit sizes, Q3 aging-time 0 meaning)

---

**Q1.** An 802.1Q tag is inserted into an Ethernet frame between the source MAC address and the EtherType field. Name the four fields in the tag, their sizes, and what each one does.

> TPID (16 bits) — identifies frame as 802.1Q tagged (value 0x8100). PCP (3 bits) — class of service for Layer 2 QoS. DEI (1 bit) — drop eligible indicator, frame can be dropped during bandwidth contention. VLAN ID (12 bits) — identifies the VLAN. Total tag = 32 bits (4 bytes).

---

**Q2.** A switch receives a frame on a trunk port with no 802.1Q tag. Which VLAN does the switch assign that frame to, and what is the relevant configuration?

> The native VLAN. Both ends of the trunk must match: `switchport trunk native vlan <id>`. If they don't match, CDP logs a mismatch warning and untagged traffic breaks — but tagged VLANs keep working.

---

**Q3.** What does `mac address-table aging-time 0` do on a Cisco IOS switch?

> Disables aging entirely — entries become permanent and never expire on their own. It does NOT cause instant removal. To see aging in action use a short non-zero value like `mac address-table aging-time 10` (minimum non-zero is 10 seconds).

---

**Q4.** SW1's trunk port is configured with `switchport trunk allowed vlan 10,20`. A frame tagged with VLAN 30 arrives on that trunk port. What does SW1 do with it?

> Drops it at ingress. VLAN 30 is not in the allowed list so the frame is discarded before reaching MAC table lookup.

---

**Q5.** `show interfaces trunk` shows VLAN 1 in the allowed list but not in the STP forwarding line. What are the two possible reasons?

> 1. STP blocking — VLAN 1 is in a non-forwarding STP state (blocking, listening, or learning) on that port. 2. VTP pruning — VLAN 1 has been pruned from the trunk.

---

**Q6.** Why is using VLAN 1 as the native VLAN on production trunk links a security risk, and what is the recommended fix?

> All switchports default to VLAN 1, so an unauthorized device can connect and send traffic that traverses every trunk as native (untagged). Fix: configure a dedicated unused VLAN (e.g., VLAN 99) as native VLAN on both trunk ends with no access ports assigned to it — a blackholed native VLAN.

---

**Q7.** You clear the MAC address table on SW1 and immediately ping from PC1 to PC2. Describe what SW1 does with the first frame and why.

> PC1 sends an ARP broadcast (FF:FF:FF:FF:FF:FF). SW1 learns PC1's source MAC on ingress and floods the frame to all ports in the VLAN (broadcast, not unknown unicast). PC2 replies with a unicast ARP reply — SW1 learns PC2's MAC. From this point all frames are forwarded directly (unicast).

---

**Q8.** You need to verify that a trunk is carrying only VLANs 10 and 20 between SW1 and SW2. Which command do you run and what specific field confirms this?

> `show interfaces trunk` — check the "Vlans allowed on trunk" line. Also verify "Vlans allowed and active in management domain" (VLAN exists in database) and "Vlans in STP forwarding state and not pruned" (actually forwarding).

---

**Q9.** What is the command to restrict a trunk to carry only VLANs 10 and 20, and what happens to traffic from any other VLAN arriving on that trunk port?

> `switchport trunk allowed vlan 10,20`. Traffic tagged with any other VLAN is dropped at ingress.

---

**Q10.** You suspect a Layer 2 connectivity issue between PC1 and PC2. List the commands you would run on SW1 and SW2 and what you are looking for in each.

> 1. `show vlan brief` — VLAN exists and is active. 2. `show interfaces trunk` — trunk is up, VLAN is allowed and in STP forwarding state. 3. `show spanning-tree vlan 10` — access port is in forwarding state, not blocking. 4. `show mac address-table interface Gi0/x` — PC MAC is learned on the correct port. 5. `show run interface Gi0/x` — port is in correct access VLAN.

---

**Q11.** What is the difference between `show vlan brief` and `show interfaces trunk`? When would each fail to show a VLAN you expect?

> `show vlan brief` shows the VLAN database — fails to show a VLAN if it was never created with `vlan <id>`. Trunk ports never appear here. `show interfaces trunk` shows trunk port config — fails to show a VLAN if it's not in the allowed list, not in the VLAN database, in STP blocking state, or pruned.

---

**Q12.** A CDP log shows a native VLAN mismatch on SW1 Gi0/0. Without touching SW2, what do you do to resolve it?

> Run `show interfaces trunk` on SW1 — check the Native vlan column to see what SW2 is using. Then match it: `interface Gi0/0` → `switchport trunk native vlan <SW2's native vlan>`.

---

## Review Notes

- **Weak area:** 802.1Q field bit sizes (16 / 3 / 1 / 12 = 32 bits total)
- **Weak area:** `aging-time 0` = no aging (permanent), not instant removal
- Next review: end of Week 1
