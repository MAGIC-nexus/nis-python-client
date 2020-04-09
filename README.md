# Python client for NIS Backend 

A Python client package to operate with NIS-Backend

NIS stands for Nexus Information System. It is a software system (a set of software components) being developed
inside project MAGIC (H2020 grant 689669). 

## Getting started

### Prerequisites

* Python 3.x
* A NIS backend instance has to be running and accessible. The URL of the API endpoint is the required parameter for the construction of the client. See the example in "Basic Usage" section below. For instructions on executing **nis-backend** please check <a href="https://github.com/MAGIC-nexus/nis-backend/blob/develop/README.md" target="_blank">README.md</a> at Github.

### Installing 
```bash
pip install nexinfosys-client
```

### Basic Usage
```python
from nexinfosys import NISClient

c = NISClient("http://localhost:5000/nis_api") # Construct client
c.login("test_user")  # Login, using test user
c.open_session()  # Open a session (needed before submission)
fname = "<path to XLSX specifying a case study (accessible to the Python interpreter executing this script)>"
c.load_workbook(fname)  # Load a workbook (see DMP's annex "Case study formatting reference") 
# Submit the workbook (execute, return a list of issues, if empty or no issues with type==3, successful execution)
r = c.submit()
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
```

## Authors

* **Rafael Nebot**. Instituto Tecnológico de Canarias, SA. Departamento de Computación

## License

This project is licensed under the BSD-3 License - see the [LICENSE](LICENSE) file for details

## Acknowledgements

The development of this software was supported by the European Union’s Horizon 2020 research and innovation programme
under Grant Agreement No. 689669 (MAGIC). This work reflects the authors' view only; the funding agencies are not 
responsible for any use that may be made of the information it contains.
