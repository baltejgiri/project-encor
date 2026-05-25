# Ch 1 – Capstone: Exam-Style Questions

Answer each question without referring to your notes. Use the lab topology to verify your answers after.

---

**Q1.** Before touching any CLI, construct a table mapping every interface in this topology to its type (trunk, access, subinterface, SVI, routed port), its expected operational state (up/up), and the Layer 3 address it should carry. What show command would you run first on each device to confirm whether the intended state matches the actual state?

**Q2.** SW-ACC console shows a CDP log: `%CDP-4-NATIVE_VLAN_MISMATCH: Native VLAN mismatch discovered on GigabitEthernet0/1 (99), with SW-CORE GigabitEthernet0/1 (1)`. What is the exact operational impact on untagged traffic crossing this trunk? Write the two commands — one on each switch — that resolve the mismatch. Which native VLAN value is correct: 1 or 99?

**Q3.** PC2 (10.20.20.10, VLAN 20) is unreachable. `show vlan brief` on SW-ACC shows Gi0/2 assigned to VLAN 20. `show vlan brief` on SW-CORE shows VLAN 20 does not appear in the VLAN database. Explain why PC2 is isolated even though the access port is correctly assigned, and write the single command on SW-CORE that resolves it.

**Q4.** PC1 (10.10.10.10/24) cannot ping its gateway 10.10.10.254. R1's `show interfaces GigabitEthernet0/0.10` output shows the subinterface is up/up and has an IP address. What other output on R1 would reveal the missing configuration, and what is the likely fault? Write the fix command.

**Q5.** SW-CORE has no entry for 172.31.0.0/30 in its routing table. `show interfaces GigabitEthernet0/3` on SW-CORE shows `Hardware is EtherSVI`. What does this output indicate about the current state of the port, and what command fixes it? After the fix, what two additional commands are needed to make the link to R2 operational?

**Q6.** After fixing fault #5, you run a 500-packet ping flood from PC1 to R2 Lo0 (10.99.99.99). R2's CPU spikes to 80%. `show ip cef` on R2 shows the route for 10.10.10.0/24 exists. What does this tell you about the forwarding path? Which show command on R2 confirms that a specific interface is bypassing CEF? Write the fix and the post-fix verification command.

**Q7.** With all five faults resolved, trace the complete Layer 2 and Layer 3 forwarding path for a packet from PC1 (10.10.10.10) to R2 Lo0 (10.99.99.99). Include: the source and destination IP at every hop, the source and destination MAC at every hop, which device performs ARP for which address, and which device's FIB is consulted at each L3 hop.

**Q8.** Construct a fault isolation table for this lab. For each of the five faults, fill in: (a) the diagnostic command that reveals it, (b) the specific indicator in the command output, and (c) the fix command. This table is the kind of systematic reference an engineer would build during a real incident.

**Q9.** After all fixes are applied, PC1 pings PC2 (10.20.20.10). The ping succeeds. Explain why SW-CORE performs a Layer 3 forwarding decision for this ping rather than bridging it at Layer 2 — even though both hosts are on the same physical switch infrastructure.

**Q10.** You want to observe an 802.1Q-tagged frame on the SW-ACC–SW-CORE trunk. Using CML's built-in link capture on that trunk link, describe what you would see for a frame from PC1 (VLAN 10). What TPID value confirms 802.1Q encapsulation? What would the VLAN ID field contain, and what would PCP and DEI be for normal untagged-at-host traffic?

**Q11.** Compare the CEF FIB entry for 10.99.99.99/32 on R1 versus on SW-CORE. What next-hop does each device use, and what adjacency entry must exist on each device for CEF to successfully forward the packet?

**Q12.** A new engineer proposes adding a second default gateway on PC1 pointing to the SW-CORE VLAN 10 SVI (10.10.10.1) as a backup for when R1 is unavailable. Without a first-hop redundancy protocol, why would this not provide automatic failover, and what would PC1 actually do if its primary gateway (10.10.10.254) became unreachable?
