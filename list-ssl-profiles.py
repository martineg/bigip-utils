#! /usr/bin/env python

# list ssl profiles associated with vips
# will load login credentials and hostname from a yml config file, should contain a dict bigip with hostname, username and password:
# ---
# bigip:
#   - hostname: bigip.fqdn
#   - username: admin
#   - password: password

import sys
import yaml
import bigsuds

try:
    cfg = sys.argv[1]
    credentials = yaml.load(open(cfg))['bigip']
except:
    print "unable to load credentials file"
    sys.exit(1)

lb = bigsuds.BIGIP(**credentials)
vips = lb.LocalLB.VirtualServer.get_list()

for v in vips:
    vip_profiles = lb.LocalLB.VirtualServer.get_profile([v])
    for p in vip_profiles[0]:
        if p['profile_type'] == 'PROFILE_TYPE_CLIENT_SSL':
          print "%s: %s" % (v, p['profile_name'])

