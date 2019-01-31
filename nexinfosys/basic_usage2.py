#!/usr/bin/env python3

from nexinfosys import NISClient
c = NISClient("https://one.nis.magic-nexus.eu/nis_api")

print("NISClient created")
c.login("test_user")
print("Logged in")
c.open_session()
print("Session opened")
fname = "https://nextcloud.data.magic-nexus.eu/remote.php/webdav/NIS_beta/CS_format_examples/08_caso_energia_eu_new_commands.xlsx"
n = c.load_workbook(fname, "", "")
print("N worksheets: "+str(n))
r = c.submit()
print("Returned from submit")
success = sum([i.type==3 for i in r]) == 0
for i in r:  # Print issues
    print(str(i))
if success:
    r = c.query_available_datasets()  # Obtain available datasets
    if len(r) > 0:
        for ds in r:  # List available datasets
            print(str(ds))
        # Query for one of the datasets ("ds1" must exist)
        r = c.query_datasets([("ds1", "csv")])
        # Write datasets
        for cnt, f in enumerate(r):
            fd = open(f[0]+"."+f[1], "wb")
            fd.write(f[2])
            fd.close()

# Close session
c.close_session()
# Logout
c.logout()
