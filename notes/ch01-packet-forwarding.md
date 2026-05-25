# Ch 1 – Packet Forwarding: Study Notes

**Week:** 1 (May 25–31, 2026)
**Status:** In Progress

---

## Key Concepts

### VLANs and 802.1Q Trunking

<!-- What stood out from the reading? Key rules, gotchas, things you had to look up. -->

### 802.1Q Frame Fields

| Field | Size | Purpose |
|-------|------|---------|
| TPID | 16 bits | |
| PCP | 3 bits | |
| DEI | 1 bit | |
| VLAN ID | 12 bits | |

### CAM Table and MAC Learning

<!-- How does the learn/flood/forward cycle work in your own words? -->

### Layer 2 Forwarding Process

<!-- Walk through what happens from the moment a host sends a frame to an unknown destination. -->

### SVIs, Subinterfaces, and Routed Ports

| Interface Type | When to Use | Key Command |
|---------------|-------------|-------------|
| SVI | | `interface VlanX` |
| Subinterface | | `encapsulation dot1Q` |
| Routed port | | `no switchport` |

### IPv4 and IPv6 Addressing

<!-- Secondary IPv4, multiple IPv6 addresses — what surprised you or needed re-reading? -->

### CEF and Forwarding Architectures

| Concept | Notes |
|---------|-------|
| Process switching | |
| Software CEF | |
| Hardware CEF | |
| FIB | |
| RIB | |
| Adjacency table | |
| TCAM | |
| SDM templates | |
| Centralized forwarding | |
| Distributed forwarding | |

---

## Commands to Remember

```
! Layer 2 verification


! Layer 3 verification


! CEF and forwarding


! SDM templates

```

---

## Lab Observations

### Lab 1 – VLAN Trunking
<!-- What did you see in the packet capture? What happened during the native VLAN mismatch? -->

### Lab 2 – L3 Interfaces
<!-- What caused the SVI to go line-protocol down? What did the show output look like? -->

### Lab 3 – Forwarding Architectures
<!-- What did the FIB look like at each hop during the multi-hop trace? CPU before/after CEF? -->

### Capstone
<!-- Which fault was hardest to diagnose and why? -->

---

## Things That Tripped Me Up

<!-- Misconceptions corrected, tricky exam gotchas, anything worth flagging for spaced repetition. -->

---

## Open Questions

<!-- Anything still unclear after the week — bring these to the Week 2 flashcard review. -->

---

## Weekly Mock Test Score

**Score:** &nbsp; / 20
**Weak areas:**
