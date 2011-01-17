from twisted.names.authority import getSerial

tmtl = '184.106.136.126'
subs = [] # ['', 'www.']
name = 'divmod.com'

zone = [
    SOA(
        # For whom we are the authority
        name,

        # This nameserver's name
        mname = "ns1.twistedmatrix.com",

        # Mailbox of individual who handles this
        rname = "exarkun.twistedmatrix.com",

        # Unique serial identifying this SOA data
        # <4-year> <2-month> <2-day> <2-counter>
        serial = getSerial(),

        # Time interval before zone should be refreshed
        refresh = "1D",

        # Interval before failed refresh should be retried
        retry = "15M",

        # Upper limit on time interval before expiry
        expire = "1D",

        # Minimum TTL
        minimum = "1D",

        # Default TTL for records in this zone
        ttl="1D",
    ),

    NS(name, 'ns1.twistedmatrix.com'),
    NS(name, 'ns2.twistedmatrix.com'),

    MX(name, 100, 'tm.tl', ttl=5 * 60),

    A('ampere.' + name, '78.46.87.228', ttl="1H"),

    CNAME('about.' + name, 'ampere.divmod.com'),
    CNAME('developer.' + name, 'ampere.divmod.com'),
    CNAME('blogs.' + name, 'ghs.google.com'),
    CNAME('news.' + name, 'ghs.google.com'),
    CNAME('google679526e42ed3328d.divmod.com', 'google.com'),
]

for sub in subs:
    zone.append(A(sub + name, tmtl, ttl="1H"))
