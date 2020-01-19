def get_bridge_name(vlan: int, vxlan: str = None):
    if vxlan is None:
        return "v" + vlan
    if vlan is None:
        return "vx" + vxlan
    return "v" + vlan + "vx" + vxlan
