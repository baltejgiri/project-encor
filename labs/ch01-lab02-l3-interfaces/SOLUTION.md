# Ch 1 – Lab 2: Layer 3 Interfaces — Exam-Style Questions

Answer each question without referring to your notes. Use the lab topology to verify your answers after.

---

**Q1.** What is the functional difference between a Switch Virtual Interface (SVI) and a routed port (`no switchport`) on a Layer 3 switch? Describe a scenario where you would choose an SVI and a scenario where you would choose a routed port.

**Q2.** You configure `no switchport` on SW1 Gi0/3 and assign IP addresses. What command on SW1 confirms that Gi0/3 is now operating as a Layer 3 routed port rather than a Layer 2 switchport? What specific field in the output distinguishes a routed port from a switchport?

**Q3.** On R1, you configure a subinterface for VLAN 10 using `encapsulation dot1Q 10`. You also want R1 to terminate untagged frames arriving on the physical Gi0/0 interface. What command accomplishes this, and what IOS term describes an interface configured this way?

**Q4.** R1 Gi0/0.10 has a primary IPv4 address of `10.10.10.254/24` and a secondary address of `172.16.10.254/24`. What does `show ip route` on R1 look like for these two subnets? What is the purpose of a secondary address, and how does R1 decide which source IP to use for a ping originating from this interface?

**Q5.** You assign two IPv6 global unicast addresses to R1 Gi0/0.10: `2001:db8:10::1/64` and `2001:db8:10::ff/64`. What command verifies that both addresses are active? In addition to these two, what other IPv6 address type is automatically present on this interface, and what is it derived from?

**Q6.** SW1's VLAN 20 SVI is configured with an IP address but shows `line protocol is down`. List every condition that must be true simultaneously for an SVI to reach `up/up` state.

**Q7.** Compare the output of `show interfaces` for SW1's VLAN 10 SVI versus SW1's Gi0/3 routed port. What fields appear in one output but not the other, and what does that tell you about how IOS treats these two interface types internally?

**Q8.** PC1 (10.10.10.10/24, default gateway 10.10.10.254 on R1 Gi0/0.10) sends a packet to R2 Gi0/0 (172.30.0.2). Trace the complete Layer 2 and Layer 3 forwarding path for this packet — include the source and destination MAC addresses at every hop, and identify which device performs each ARP resolution.

**Q9.** What is the difference between `show ip interface brief` and `show ip interface`? Name two pieces of information visible in `show ip interface` that do not appear in `show ip interface brief`.

**Q10.** On SW1, you run `show ip interface brief` and see the VLAN 10 SVI listed as `administratively down`. You also run the same command on R1 and see Gi0/0.10 listed as `up/up`. What is the most likely cause of the SVI being administratively down, and what single command resolves it?

**Q11.** R1 Gi0/0.10 has `encapsulation dot1Q 10` configured. What happens if you send a frame tagged with VLAN 10 to R1 Gi0/0 but the `encapsulation dot1Q 10` line is missing from the subinterface configuration? What symptom would you observe from PC1's perspective?

**Q12.** SW1 has both an SVI for VLAN 10 (10.10.10.1/24) and R1 has a subinterface for VLAN 10 (10.10.10.254/24). PC1 uses R1's address as its default gateway. If PC1 sends a packet destined for the 172.30.0.0/30 network, explain why the SW1 SVI alone cannot forward this packet without a routing protocol or static route, even though SW1 is a Layer 3 switch.
