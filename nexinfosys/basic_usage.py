from nexinfosys import NISClient

# IMPORTANT: A "NIS backend" instance must be running at some URL. In this example, it is available at the local
#            computer through "localhost:5000"

# Construct client
c = NISClient("http://localhost:5000/nis_api")
# Login, using default user
c.login()
# Open a session (needed before submission)
c.open_session()
# Load a workbook
fname = "../input_files/08_caso_energia_eu_new_commands.xlsx"
fname = "/home/rnebot/GoogleDrive/AA_MAGIC/nis-backend/backend_tests/z_input_files/v2/Biofuel_NIS.xlsx"
c.load_workbook(fname)
# Submit the workbook (execute, return a list of issues, if empty or no issues with type==3, successful execution)
r = c.submit()
any_error = False
if len(r) > 0:
    for i in r:
        if i["type"] == 3:
            any_error = True
        print(str(i))

if not any_error:
    # Obtain available datasets
    r = c.query_available_datasets()
    if len(r) > 0:
        results = {}
        for ds in r:
            results[ds["name"]] = {d["format"].lower(): d["url"] for d in ds["formats"]}
            print(str(ds))
        # Query for one of the datasets (it is known to exist)
        # r = c.query_datasets([("ds1", "csv", "dataframe")])
        # r = c.query_datasets([("flow_graph", "GML")])
        r = c.download_results([(results["FG"]["gml"])])
        import networkx as nx
        import io
        b = io.BytesIO(r[0])
        g = nx.read_gml(b)
        # Write datasets
        for cnt, f in enumerate(r):
            fd = open("/home/rnebot/" + f[0] + "." + f[1], "wb")
            fd.write(f[2])
            fd.close()

# Close the opened session
c.close_session()
# Logout
c.logout()
# END
print("OK !! ---")
