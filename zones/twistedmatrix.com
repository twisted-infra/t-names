
from twisted.names.authority import getSerial

name = 'twistedmatrix.com'

from hosts import cube, dornkirk, tmtl, oloid, wolfwood, xpdev, planet, nameservers, addSubdomains, googleHosting

subs = {
    cube: ['', 'cube.', 'projects.', 'reality.', 'irc.', 'ftp.', 'saph.',
           'java.', 'www.', 'smtp.', 'mail.', 'buildbot.', 'speed.'],
    wolfwood: ['cvs.', 'wolfwood.', 'svn.'],
    oloid: ['oloid.'],
    dornkirk: ['dornkirk.'],
    xpdev: ['xpdev.'],
}

zone = [
    SOA(
        # For whom we are the authority
        name,

        # This nameserver's name
        mname = "ns1.twistedmatrix.com",

        # Mailbox of individual who handles this
        rname = "radix.twistedmatrix.com",

        # Unique serial identifying this SOA data
        # <4-year> <2-month> <2-day> <2-counter>
        serial = getSerial(),

        # Time interval before zone should be refreshed
        refresh = "5M",

        # Interval before failed refresh should be retried
        retry = "15M",

        # Upper limit on time interval before expiry
        expire = "1H",

        # Minimum TTL
        minimum = "5M",

        ttl="5M",
    ),

    MX(name, 5, 'mail.' + name, ttl='1H'),

    CNAME('planet.twistedmatrix.com', planet, ttl='1D'),
    CNAME('radix.twistedmatrix.com', googleHosting, ttl='1D'),
    CNAME('washort.twistedmatrix.com', googleHosting, ttl='1D'),
    CNAME('glyph.twistedmatrix.com', googleHosting, ttl='1D'),
    CNAME('secret.glyph.twistedmatrix.com', googleHosting, ttl='1D'),
    CNAME('labs.twistedmatrix.com', googleHosting, ttl='1D'),
] + nameservers(name)

addSubdomains(name, zone, subs)
