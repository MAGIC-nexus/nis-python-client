"""
Client to NIS Backend
"""

import io
from typing import List, Tuple
from enum import Enum
import pandas as pd

from nis.req_client import RequestsClient


class NISClientState(Enum):
    LOGGED_OUT = 1,  # Not logged
    LOGGED_IN = 2,   # Logged, but no session
    SESSION_INITIATED = 3,  # Logged, with initiated session


class NISClientDatasetFormat(Enum):
    CSV = 1,
    XLSX = 2,
    GML = 3,
    GRAPH_ML = 4,


class NISClient:
    def __init__(self, url: str):
        # No connection key
        self._api_key = None  # type: str
        self._state = NISClientState.LOGGED_OUT
        if not url.endswith("/"):
            url += "/"
        self._req_client = RequestsClient(url)
        self._dataframe_names = []  # type: List[str]
        self._dataframes = []  # type: List[pd.DataFrame]

    def check_backend_available(self):
        # TODO Just check that there is a NIS backend at URL self._url. Use requests
        r = self._req_client.get("test")
        if r.status_code == 200:
            return "hello" in r.json()
        else:
            return False

    def login(self, user: str="test_user", api_key: str=None):
        if self._state == NISClientState.LOGGED_IN:
            raise Exception("Already logged in. Call 'logout' before calling 'login'.")
        elif self._state == NISClientState.SESSION_INITIATED:
            raise Exception("Logged in and session initiated. First 'close_session', second 'logout', before calling 'login'.")

        self._api_key = api_key
        # Call "login"
        r = self._req_client.post("isession")
        if r.status_code == 204:
            r = self._req_client.put("isession/identity?user="+user, None)
            if r.status_code == 200:
                self._state = NISClientState.LOGGED_IN
            else:
                r = self._req_client.delete("isession")  # Close interactive session
                if r.status_code != 200:
                    raise Exception("Could not close interactive session")

        return self._state == NISClientState.LOGGED_IN

    def logout(self):
        if self._state == NISClientState.LOGGED_OUT:
            raise Exception("Already logged out. Call 'login' before calling 'logout'.")
        elif self._state == NISClientState.SESSION_INITIATED:
            raise Exception("Session initiated. Call 'close_session' before calling 'login'.")

        r = self._req_client.delete("isession/identity")
        if r.status_code == 200:
            r = self._req_client.delete("isession")  # Close interactive session
            if r.status_code == 200:
                self._state = NISClientState.LOGGED_OUT
            else:
                raise Exception("Could not close interactive session")
        else:
            raise Exception("Could not logout user")

        return self._state == NISClientState.LOGGED_OUT

    def open_session(self):
        uuid = None
        read_version_state = False
        create_new = True
        allow_saving = False
        cs_name = None

        if self._state == NISClientState.LOGGED_OUT:
            raise Exception("Not logged in. Call 'login' first")
        elif self._state == NISClientState.SESSION_INITIATED:
            raise Exception("Session already open. Close it using 'close_session'.")

        # Open reproducible session
        p_uuid = "uuid=" + (uuid if uuid else "")
        p_read = "read_version_state=" + str(read_version_state)
        p_cr_new = "create_new=" + str(create_new)
        p_allow = "allow_saving=" + str(allow_saving)
        p_cs_name = "cs_name=" + (str(cs_name) if cs_name else "")

        params = p_uuid
        params += ("&" if params != "" else "") + p_read
        params += ("&" if params != "" else "") + p_cr_new
        params += ("&" if params != "" else "") + p_allow
        params += ("&" if params != "" else "") + p_cs_name
        params = "?"+params if params != "" else ""

        r = self._req_client.post("isession/rsession"+params)
        if r.status_code == 204:
            self._state = NISClientState.SESSION_INITIATED
        else:
            raise Exception("Could not open session")

        return self._state == NISClientState.SESSION_INITIATED

    def close_session(self):
        if self._state == NISClientState.LOGGED_OUT:
            raise Exception("Not logged in. Call 'login' first, then 'open_session'")
        elif self._state == NISClientState.LOGGED_IN:
            raise Exception("Session already closed.")

        # Close reproducible session
        save = False
        cs_uuid = None
        cs_name = None

        save_before_close = "save_before_close=" + ("True" if save else "False")
        cs_uuid_param = "cs_uuid=" + (cs_uuid if cs_uuid else "")
        p_cs_name = "cs_name="+(str(cs_name) if cs_name else "")

        params = save_before_close
        params += ("&" if params != "" else "") + cs_uuid_param
        params += ("&" if params != "" else "") + p_cs_name

        r = self._req_client.delete("isession/rsession?"+params)
        if r.status_code == 200:
            self._state = NISClientState.LOGGED_IN
        else:
            raise Exception("Could not close session")

        return self._state == NISClientState.LOGGED_IN

    def reset_commands(self):
        self._dataframe_names.clear()
        self._dataframes.clear()

    def load_workbook(self, fname):
        # Load a XLSX workbook into memory, as dataframes
        xl = pd.ExcelFile(fname)
        for sheet_name in xl.sheet_names:
            df = xl.parse(sheet_name, header=0)
            # Manage columns
            cols = []
            for col in df.columns:
                col_parts = col.split(".")
                if col.lower().startswith("unnamed"):
                    cols.append("")
                elif len(col_parts) > 1:
                    try:
                        int(col_parts[1])  # This is the case of "col.1"
                        cols.append(col_parts[0])
                    except:  # This is the case of "col_part.col_part" (second part is string)
                        cols.append(col)
                else:
                    cols.append(col)

            df.columns = cols
            self._dataframes.append(df)
            self._dataframe_names.append(sheet_name)

    def _generate_in_memory_excel(self):
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine="xlsxwriter")
        for idx, sheet_name in enumerate(self._dataframe_names):
            header = sheet_name.lower() != "metadata"
            self._dataframes[idx].to_excel(writer, sheet_name=sheet_name, index=False)
        writer.save()
        return output.getvalue()

    def append_command(self, name: str, df: pd.DataFrame):
        for n in self._dataframe_names:
            if n.lower() == name.lower():
                raise Exception("Duplicated name '"+name+"' for a command.")

        if not isinstance(df, pd.DataFrame):
            raise Exception("'df' parameter must be a Pandas DataFrame")

        self._dataframes.append(df)
        self._dataframe_names(name)

    def submit(self) -> List:
        if self._state == NISClientState.LOGGED_OUT:
            raise Exception("Not logged in. Call 'login' first, then 'open_session'")
        elif self._state == NISClientState.LOGGED_IN:
            raise Exception("Call 'open_session' before submitting")

        # Convert dataframes to workbook
        xlsx = self._generate_in_memory_excel()
        # f = open("/home/rnebot/prueba.xlsx", "wb")
        # f.write(xlsx)
        # f.close()

        execute = True
        exec = "True" if execute else "False"

        r = self._req_client.post("isession/rsession/generator?execute=" + exec+"&register=False", xlsx, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        if r.status_code == 200:
            # Return the issues
            d = r.json()
            if "issues" in d:
                return d["issues"]
        else:
            return []

    def query_available_datasets(self, filter: str=None):
        if self._state == NISClientState.LOGGED_OUT:
            raise Exception("Not logged in. Call 'login' first, then 'open_session' and 'submit'")
        elif self._state == NISClientState.LOGGED_IN:
            raise Exception("Call 'open_session' before querying for available datasets")

        # Obtain a list of datasets and the type
        r = self._req_client.get("isession/rsession/state_query/datasets")
        if r.status_code == 200:
            r2 = r.json()
            if "datasets" in r2:
                return r2["datasets"]
            else:
                return []
        else:
            raise Exception("Could not retrieve the available datasets")

    def query_datasets(self, datasets: List[Tuple[str, NISClientDatasetFormat]]):
        """
        Obtain one or more datasets in the specified format
        :param datasets:
        :return:
        """
        res = []
        for t in datasets:
            ds_name = t[0]
            ds_format = t[1]
            format = "csv"
            r = self._req_client.get("isession/rsession/state_query/datasets/"+ds_name+"."+format)
            if r.status_code == 200:
                res.append((ds_name, format, r.content))
        return res

    # --------------- SYNTAX FUNCTIONS ---------------

    def validate_cell(self, command_type: str, column_name: str, value: str):
        """
        Validate syntax of cell, given the command type and column under which the value is specified

        :param command_type: Command type
        :param column_name: Column in command type
        :param value: Specific cell value
        :return:
        """

    def list_of_available_command_types(self):
        """
        List of commands
        :return:
        """

    def fields_for_command_type(self, command_type: str):
        """
        Fields expected by command type
        :param command_type: Name of t
        :return:
        """

    def examples_for_command_type(self, command_type: str):
        """
        Examples of command type. Returns a list of CSVs or URLs (pointing to case studies using this command type)

        :param command_type: Command type
        :return:
        """

    def description_for_command_type(self, command_type: str):
        """
        A text describing the purpose and semantics of the command type

        :param command_type: Command type
        :return:
        """