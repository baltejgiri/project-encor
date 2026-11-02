"""Generate the Day 18 (Ch 2, pp 41-47) CML topology: 5 IOSvL2 switches shaped like the book's Figure 2-1.
Fixed MACs so the root bridge, root ports and blocked ports are the same on every boot.
Inter-switch links are pre-built 802.1Q trunks (VLANs 1 and 10) so the lab is only about STP."""
import yaml

# (switch, iface) pairs per link
LINKS = [
    (("SW1", "Gi0/1"), ("SW2", "Gi0/1")),
    (("SW1", "Gi0/2"), ("SW3", "Gi0/1")),
    (("SW2", "Gi0/2"), ("SW3", "Gi0/2")),   # non-root link: which end blocks (MAC tie-break)
    (("SW2", "Gi1/0"), ("SW4", "Gi0/1")),   # double link SW2-SW4, cabled crossed on purpose:
    (("SW2", "Gi0/3"), ("SW4", "Gi0/2")),   #   SW4's root port follows SW2's port ID, not its own
    (("SW3", "Gi0/3"), ("SW5", "Gi0/1")),
    (("SW4", "Gi1/0"), ("SW5", "Gi1/0")),   # non-root link, equal root cost 8 on both ends
]
POS = {"SW1": (0, -200), "SW2": (-200, -50), "SW3": (200, -50), "SW4": (-200, 150), "SW5": (200, 150)}
# Bridge MAC = Gi0/0 MAC = 52:54:00:1N:00:1N (1N keeps them unique from the Day 17 lab, which uses 0N). SW1 lowest; SW3 below SW2 and SW5 below SW4 (opposite of the book).
NUM = {"SW1": 1, "SW3": 2, "SW2": 3, "SW5": 4, "SW4": 5}
SLOTS = [f"Gi{s}/{p}" for s in range(4) for p in range(4)]  # slot index = position in this list
TRUNKS = {}
for a, b in LINKS:
    for sw, ifc in (a, b):
        TRUNKS.setdefault(sw, []).append(ifc)


def node(i, name):
    n = NUM[name]
    ifs = [{"id": "i0", "label": "Loopback0", "type": "loopback", "mac_address": None}]
    for slot, short in enumerate(SLOTS):
        ifs.append({"id": f"i{slot+1}", "label": "GigabitEthernet" + short[2:], "type": "physical",
                    "slot": slot, "mac_address": f"52:54:00:1{n}:{slot:02x}:1{n}"})
    trunks = "".join(f"interface GigabitEthernet{ifc[2:]}\n switchport trunk encapsulation dot1q\n"
                     f" switchport mode trunk\n switchport nonegotiate\n" for ifc in sorted(TRUNKS[name]))
    unused = "".join(f"interface GigabitEthernet{ifc[2:]}\n shutdown\n" for ifc in SLOTS if ifc not in TRUNKS[name])
    cfg = (f"hostname {name}\nno ip domain-lookup\nvtp mode transparent\nvlan 10\n name DATA\n"
           f"{trunks}{unused}line con 0\n exec-timeout 0 0\n logging synchronous\nend")  # unused ports shut: STP output shows only cabled ports
    x, y = POS[name]
    return {"id": f"n{i}", "label": name, "node_definition": "iosvl2", "x": x, "y": y,
            "configuration": [{"name": "ios_config.txt", "content": cfg}], "interfaces": ifs,
            "tags": [], "parameters": {}, "hide_links": False}


names = ["SW1", "SW2", "SW3", "SW4", "SW5"]
nodes = [node(i, n) for i, n in enumerate(names)]
def iid(sw, ifc): return f"i{SLOTS.index(ifc)+1}"
links = [{"id": f"l{k}", "n1": f"n{names.index(a[0])}", "i1": iid(*a), "n2": f"n{names.index(b[0])}", "i2": iid(*b),
          "label": f"{a[0]}-{a[1]}<->{b[0]}-{b[1]}"} for k, (a, b) in enumerate(LINKS)]
topo = {"lab": {"title": "Day 18 - Lab: Ch 2 building the STP topology", "version": "0.3.0",
                "description": "Ch 2 pp 41-47. Trunks pre-built (VLANs 1, 10); fixed MACs so every boot is the same."},
        "nodes": nodes, "links": links, "annotations": []}
open("lab-ch02-stp-topology.yaml", "w").write(yaml.safe_dump(topo, sort_keys=False))
print("wrote lab-ch02-stp-topology.yaml:", len(nodes), "nodes", len(links), "links")
