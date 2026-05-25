# Ch 1 – Lab 1: VLANs, Trunking, and 802.1Q — Exam-Style Questions

Answer each question without referring to your notes. Use the lab topology to verify your answers after.

---

**Q1.** An 802.1Q tag inserts four fields between the source MAC address and the EtherType field of a standard Ethernet frame. Name each field, state its size in bits, and describe its purpose.

**Q2.** What hexadecimal value in the TPID field identifies a frame as 802.1Q-tagged? What does a receiving device do when it sees this value?

**Q3.** PC1 (VLAN 10) sends its first frame to PC2 (VLAN 10, on SW2). SW1 has no entry for PC2's MAC address. Describe every step SW1 takes from receiving the frame to getting it toward PC2 — include the term that describes the forwarding behavior and explain why it is safe on a switch.

**Q4.** After the exchange in Q3, you run `show mac address-table` on SW1 and SW2. What MAC addresses do you expect to see on each switch, and on which ports? Explain why the MAC address of a host is associated with the port the frame *arrived* on, not the port it was forwarded out of.

**Q5.** What is the difference between the MAC address table (software) and the CAM (Content Addressable Memory) hardware? Why is a CAM lookup O(1) regardless of how many entries exist in the table?

**Q6.** You run `clear mac address-table dynamic` on SW1, then immediately ping from PC1 to PC2. The first ping succeeds after a short delay but subsequent pings are faster. Explain the frame path for the first ping and for the second ping, and identify what changed between them.

**Q7.** You change SW2's native VLAN to 99 while SW1 keeps native VLAN 1. SW1's console shows a CDP log message about a native VLAN mismatch. What is the exact operational impact of this mismatch on untagged traffic crossing the trunk? What two commands — one on each switch — resolve it?

**Q8.** Interpret the following partial output from `show interfaces trunk` on SW1:

```
Port        Mode         Encapsulation  Status        Native vlan
Gi0/0       on           802.1q         trunking      1

Port        Vlans allowed on trunk
Gi0/0       1-4094

Port        Vlans allowed and active in management domain
Gi0/0       1,10,20

Port        Vlans in spanning tree forwarding state and not pruned
Gi0/0       10,20
```

What does the difference between "VLANs allowed on trunk" and "VLANs in spanning tree forwarding state and not pruned" tell you about VLAN 1?

**Q9.** You want the SW1–SW2 trunk to carry only VLANs 10 and 20. Write the command to restrict the trunk, and explain what happens to a frame tagged with VLAN 30 that arrives on SW1's trunk port after this change.

**Q10.** PC3 is on VLAN 20 (SW2). PC1 is on VLAN 10 (SW1). PC3 pings PC1 and gets no reply. Using only Layer 2 diagnostic commands (no routing commands), list the commands you would run in sequence and what each output would tell you about the point of failure.

**Q11.** A frame arrives on SW1's trunk port Gi0/0 tagged with VLAN 30. VLAN 30 does not exist in SW1's VLAN database. What does SW1 do with the frame?

**Q12.** Compare what happens when a frame arrives on a trunk port tagged with a VLAN that exists in the database but is not in the allowed VLAN list, versus a VLAN that is allowed but whose port is in STP blocking state for that VLAN.
