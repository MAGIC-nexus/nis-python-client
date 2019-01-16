from nis.client import NISClient

# Construct client
c = NISClient("http://localhost:5000/nis_api")
# Login, using default user
r = c.login()
# Open a session (needed before submission)
r = c.open_session()
# Load a workbook
fname = "../input_files/08_caso_energia_eu_new_commands.xlsx"
c.load_workbook(fname)
# Submit the workbook (execute, return a list of issues, if empty or no issues with type==3, successful execution)
r = c.submit()
if len(r) > 0:
    for i in r:
        print(str(i))
else:
    # Obtain available datasets
    r = c.query_available_datasets()
    if len(r) > 0:
        for ds in r:
            print(str(ds))
        # Query for one of the datasets (it is known to exist)
        r = c.query_datasets([("ds1", "csv")])
        # Write datasets
        for cnt, f in enumerate(r):
            fd = open("/home/rnebot/" + f[0] + "." + f[1], "wb")
            fd.write(f[2])
            fd.close()

# Close the opened session
r = c.close_session()
# Logout
r = c.logout()
# END
print("OK !! ---")
