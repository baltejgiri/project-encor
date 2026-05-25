# Ch 1 – Lab 3: Forwarding Architectures — Exam-Style Questions

Answer each question without referring to your notes. Use the lab topology to verify your answers after.

---

**Q1.** What command confirms that CEF is globally enabled on a Cisco IOS router? What does the output tell you about per-interface CEF status?

**Q2.** On R1, a static route exists for `10.2.2.2/32` via `192.168.1.2`. What two tables are built by CEF to forward packets destined for `10.2.2.2`? Describe the role of each.

**Q3.** You run a verification command and see an entry marked `(incomplete)` in the adjacency table for `192.168.1.2`. What does this mean, and what must happen before CEF can forward packets to that next-hop?

**Q4.** A packet arrives at R1 destined for `10.2.2.2`. Describe the complete Layer 2 and Layer 3 forwarding process — from the moment R1 looks up the destination in its FIB to the moment the frame leaves R1's Gi0/0 interface.

**Q5.** SW1 is a Layer 2 switch. When R1 sends a frame to R2 for the first time, what does SW1 do with the frame if R2's MAC address is not yet in its MAC address table? What term describes this behavior?

**Q6.** After traffic flows between R1 Lo0 and R2 Lo0, you check SW1's MAC address table. What MAC addresses do you expect to see, and on which ports? Why does SW1 not learn the Loopback0 MAC addresses?

**Q7.** What is the difference between process switching and CEF? In what scenario would a router fall back to process switching even when CEF is enabled globally?

**Q8.** You disable CEF on R2's Gi0/0 interface with `no ip route-cache cef`. What forwarding mechanism takes over? How would you observe the impact on CPU utilization during a sustained ping?

**Q9.** Interpret the following partial FIB output. What does each field tell you?

```
10.2.2.2/32   via 192.168.1.2,  GigabitEthernet0/0,  receive
```

**Q10.** A network engineer claims that CEF and the routing table always contain identical entries. Is this accurate? Explain when they might differ and why.

**Q11.** What command displays the Layer 2 rewrite information (destination MAC, source MAC, encapsulation type) that CEF will use when forwarding to a specific next-hop?

**Q12.** R1 has a default route pointing to R2. A packet arrives destined for `8.8.8.8`. Trace the exact lookup sequence R1 performs in the FIB to find the forwarding entry for this destination.

**Q13.** What is the difference between the RIB (Routing Information Base) and the FIB (Forwarding Information Base)? Which one does CEF use to make forwarding decisions, and what process is responsible for populating the FIB from the RIB?

**Q14.** `show sdm prefer` on SW1 shows the "default" template is active rather than the "routing" template. What is the operational impact of this on the switch's ability to perform IP routing? What command changes the SDM template, and what must happen for the change to take effect?

**Q15.** Describe the difference between centralized CEF and distributed CEF. On a modular chassis with distributed CEF, what happens to forwarding if the route processor (supervisor) fails? On a fixed-platform switch like SW1 in this lab, which model applies?

**Q16.** You disable CEF globally on R2 with `no ip cef` and then run a 1000-packet ping flood from R1 Lo0 to R3 Lo0 (two hops through R2). Which show command on R2 reveals that process switching is handling the packets? What would `show processes cpu` look like, and which IOS process would show elevated CPU usage?
