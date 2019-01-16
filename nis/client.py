"""
Client to NIS Backend
"""
from typing import List, Tuple
from enum import Enum
import pandas as pd


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
        self._url = url
        self._key = None  # No connection key
        self._state = NISClientState.LOGGED_OUT
        self._dataframe_names = []  # type: List[str]
        self._dataframes = []  # type: List[pd.DataFrame]

    def check_backend(self):
        pass
        # TODO Just check that there is a NIS backend at URL self._url. Use requests

    def login(self, user: str="default", key: str=None):
        self._key = key
        # TODO Call "login" (no KEY for now)

    def open_session(self):
        if self._state == NISClientState.LOGGED_OUT:
            raise Exception("Not logged in. Call 'login' first")
        elif self._state == NISClientState.SESSION_INITIATED:
            raise Exception("Session already open. Close it using 'close_session'.")

        # TODO Open interactive session and reproducible session

    def close_session(self):
        if self._state == NISClientState.LOGGED_OUT:
            raise Exception("Not logged in. Call 'login' first")
        elif self._state == NISClientState.LOGGED_IN:
            raise Exception("Session already closed.")

        # TODO Open interactive session and reproducible session

    def reset_commands(self):
        self._dataframe_names.clear()
        self._dataframes.clear()

    def load_workbook(self, fname):
        pass
        # Load a XLSX workbook into memory, as dataframes

    def append_command(self, name: str, df: pd.DataFrame):
        self._dataframes.append(df)
        self._dataframe_names(name)

    def submit(self, reset: bool=True) -> List:
        pass
        # TODO Convert dataframes to workbook, then submit
        #      Return the issues

    def query_available_datasets(self, filter: str=None):
        pass
        # TODO Obtain a list of datasets and the type

    def query_datasets(self, datasets: List[Tuple[str, NISClientDatasetFormat]]):
        """
        Obtain one or more datasets in the specified format
        :param datasets:
        :return:
        """
        pass

