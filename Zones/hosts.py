
from twisted.names.dns import Record_NS, Record_A

pyramid = '198.49.126.190'
neutrino = '198.49.126.149'
wolfwood = '66.35.48.24'
planet = 'mag.ik.nu'
xpdev = '66.219.41.216'
tmrc = '18.150.1.81'
tesla = '78.46.87.228'
intarweb = '198.49.126.149'
cube = '66.35.39.65'
pyramid = '198.49.126.190'
boson = '209.6.87.187'
googleHosting = 'ghs.google.com'
paper = '67.207.132.219'
posterous = '66.216.125.32'
tmtl = '184.106.136.126'

def nameservers(host, *addresses):
    """
    Return NS records and A record glue for the given host.
    """
    if not addresses:
        addresses = [cube, tmrc]
    records = []
    for i, addr in enumerate(addresses):
        records.extend([
                (host, Record_NS('ns%d.twistedmatrix.com' % (i + 1,), ttl='1D')),
                ('ns%d.twistedmatrix.com' % (i + 1,), Record_A(addr, ttl='1D'))])
    return records


def addSubdomains(host, zone, subs):
    """
    Add the given subdomain mapping to the given zone list.
    """
    for (ip, hosts) in subs.items():
        for sub in hosts:
            zone.append((sub + host, Record_A(ip, ttl="1D")))
