# (before, from shell "pip install nexinfosys-client")

# Install or declare necessary library
.libPaths( c("~/R-packages", "/opt/conda/lib/R/library") )
#install.packages("reticulate")
library("reticulate")

# Import "nis-client"
nexinfosys <- import("nexinfosys")
c <- nexinfosys$NISClient("https://one.nis.magic-nexus.eu/nis_api")

# Login
c$login("test_user")
# Open a session
c$open_session()
# Load a NIS formatted workbook (using MAGIC's internal document repository)
fname <- "https://nextcloud.data.magic-nexus.eu/remote.php/webdav/NIS_beta/CS_format_examples/08_caso_energia_eu_new_commands.xlsx"
n <- c$load_workbook(fname, "", "")
# Submit workbook to "nis-backend". "r" can contain a list of issues if the workbook has errors.
r <- c$submit()

# List of all available datasets
r <- c$query_available_datasets()
# Obtain a dataset in a specific format
ds <- c$query_datasets(c(tuple("ds1", "csv", "dataframe")))
# Transform result to native R data.frame
df <- py_to_r(ds[[1]][[3]])

# Cleanup, logout
c$close_session()
c$logout()