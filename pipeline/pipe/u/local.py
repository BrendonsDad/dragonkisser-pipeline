from __future__ import annotations

from substance_painter import ui
import unreal

from Qt import QtWidgets

from software.baseclass import DCCLocalizer


class _UnrealLocalizer(DCCLocalizer):
    def __init__(self) -> None:
        super().__init__("unreal")

    def get_main_qt_window(self) -> QtWidgets.QWidget | None:
        return ui.get_main_window()

    def is_headless(self) -> bool:
        return False


_l = _UnrealLocalizer()

get_main_qt_window = _l.get_main_qt_window
is_headless = _l.is_headless
