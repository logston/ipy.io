def get_ephemeral_port_range():
    with open('/proc/sys/net/ipv4/ip_local_port_range') as fp:
        port_range = fp.read()
    port_range = port_range.strip()
    port_range = port_range.split()
    return map(int, port_range)


EPHEMERAL_PORT_RANGE = list(get_ephemeral_port_range())

