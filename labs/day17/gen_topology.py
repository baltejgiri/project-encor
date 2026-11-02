"""Generate the Day 17 (Ch 5) CML topology: collapsed core, 4 IOSvL2 switches, fixed MACs, hostname-only configs."""
import yaml
# (switch, iface) pairs per link
# Collapsed core: CORE1/CORE2 in the MDF, ACC1 (Closet 2A) and ACC2 (Closet 3B) dual-homed to both cores.
LINKS = [
    (("CORE1", "Gi0/1"), ("CORE2", "Gi0/1")),  # core interlink bundle, member 1
    (("CORE1", "Gi0/2"), ("CORE2", "Gi0/2")),  # core interlink bundle, member 2
    (("CORE1", "Gi0/3"), ("CORE2", "Gi0/3")),  # core interlink bundle, member 3 (max-bundle / hot standby)
    (("CORE1", "Gi1/0"), ("ACC1", "Gi0/1")),   # ACC1 uplink bundle to CORE1, member 1
    (("CORE1", "Gi1/1"), ("ACC1", "Gi0/2")),   # ACC1 uplink bundle to CORE1, member 2
    (("CORE2", "Gi1/0"), ("ACC1", "Gi0/3")),   # ACC1 single uplink to CORE2 (DTP)
    (("CORE1", "Gi1/2"), ("ACC2", "Gi0/3")),   # ACC2 single uplink to CORE1 (DTP)
    (("CORE2", "Gi1/1"), ("ACC2", "Gi0/1")),   # ACC2 uplink bundle to CORE2, member 1
    (("CORE2", "Gi1/2"), ("ACC2", "Gi0/2")),   # ACC2 uplink bundle to CORE2, member 2
]
POS = {"CORE1": (-200, -150), "CORE2": (200, -150), "ACC1": (-200, 150), "ACC2": (200, 150)}
NUM = {"CORE1": 1, "CORE2": 2, "ACC1": 3, "ACC2": 4}
SLOTS = [f"Gi{s}/{p}" for s in range(4) for p in range(4)]  # slot index = position in this list

def node(i, name):
    n = NUM[name]
    ifs = [{"id": "i0", "label": "Loopback0", "type": "loopback", "mac_address": None}]
    for slot, short in enumerate(SLOTS):
        ifs.append({"id": f"i{slot+1}", "label": "GigabitEthernet" + short[2:], "type": "physical",
                    "slot": slot, "mac_address": f"52:54:00:0{n}:{slot:02x}:0{n}"})
    cfg = f"hostname {name}\nno ip domain-lookup\nvtp mode transparent\nline con 0\n exec-timeout 0 0\n logging synchronous\nend"
    x, y = POS[name]
    return {"id": f"n{i}", "label": name, "node_definition": "iosvl2", "x": x, "y": y,
            "configuration": [{"name": "ios_config.txt", "content": cfg}], "interfaces": ifs,
            "tags": [], "parameters": {}, "hide_links": False}

names = ["CORE1", "CORE2", "ACC1", "ACC2"]
nodes = [node(i, n) for i, n in enumerate(names)]
def iid(sw, ifc): return f"i{SLOTS.index(ifc)+1}"
links = [{"id": f"l{k}", "n1": f"n{names.index(a[0])}", "i1": iid(*a), "n2": f"n{names.index(b[0])}", "i2": iid(*b),
          "label": f"{a[0]}-{a[1]}<->{b[0]}-{b[1]}"} for k, (a, b) in enumerate(LINKS)]
topo = {"lab": {"title": "Day 17 - Lab: Ch 5 collapsed core", "version": "0.3.0",
                "description": "Ch 5 lab day. Hostname-only configs; fixed MACs so every boot is the same."},
        "nodes": nodes, "links": links, "annotations": []}
open("lab-ch05.yaml", "w").write(yaml.safe_dump(topo, sort_keys=False))
print("wrote lab-ch05.yaml:", len(nodes), "nodes", len(links), "links")
