"""Main application program."""

from UI_ctrl import UI_ctrl
from DB_connector import DB_connector

if __name__ == "__main__":

    # Make connection-object first.
    connection = DB_connector()

    # Make UI-object.
    UI = UI_ctrl(connection)
    UI.main()
