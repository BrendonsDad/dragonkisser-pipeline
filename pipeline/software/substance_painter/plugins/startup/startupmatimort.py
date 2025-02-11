
from __future__ import annotations

from Qt import QtWidgets

import substance_painter as sp

import pipe.sp
from pipe.sp.matImport import matImportCheck
from pipe.sp.matImport import matImportRegardless   


plugin_widgets: list[QtWidgets.QWidget] = []


def start_plugin():
    # Create text widget for menu
    action = QtWidgets.QAction("Check for New Materials")
    action.triggered.connect(matImportRegardless)

    # Add widget to the File menu
    sp.ui.add_action(sp.ui.ApplicationMenu.Edit, action)

    # Store the widget for proper cleanup later
    plugin_widgets.append(action)
    
    sp.event.DISPATCHER.connect_strong(sp.event.ProjectEditionEntered, do_preflight)

def close_plugin():
    for widget in plugin_widgets:
        sp.ui.delete_ui_element(widget)

    plugin_widgets.clear()
    sp.event.DISPATCHER.disconnect(sp.event.ProjectEditionEntered, do_preflight)


def do_preflight(event: sp.event.Event) -> None:
    matImportCheck()


if __name__ == "__main__":
    window = start_plugin()


