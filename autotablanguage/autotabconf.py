# -*- coding: utf-8 -*-
#
#  Configuration module of Auto Tab by Language plugin for gedit
#
#  Copyright (C) 2011, Hertatijanto Hartono <dvertx@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
2011-01-02  for Auto Tab by Language plugin version 1.0

This module provides dialog box for configuring Auto Tab by Language plugin.

"""

import os
import gtk

class AutoTabLangConfigHelper:

    info_text = """
    Change tab width on the list
    to an indenting setting you
    want for a particular language.
    Mark "use spaces" column if
    spaces are to be used instead
    of tab characters.

    """

    def __init__(self, plugin, window):
        self._window = window
        self._plugin = plugin

        glade_file = os.path.join(self._plugin.plugin_path, 'autotabconf.glade')
        self.builder = gtk.Builder()
        self.builder.add_from_file(glade_file)
        self.dialog = self.builder.get_object("maindialog")
        self.treeview = self.builder.get_object("treeview")
        self.langstore = self.builder.get_object("langstore")
        self.info = self.builder.get_object("helptext")
        self._set_info_text()
        self._set_dialog_list()
        self.builder.connect_signals(self)
        self.dialog.set_transient_for(self._window)
        self.dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.dialog.show()

    def _set_info_text(self):
        textbuffer = self.info.get_buffer()
        textbuffer.set_text(self.info_text)

    def _set_dialog_list(self):
        for index, language in enumerate(self._plugin.languages):
            if self._plugin.language_tab[index]:
                self.langstore.append([index+1, language,
                    self._plugin.language_tab[index],
                    self._plugin.language_space[index]])
            else:
                self.langstore.append([index+1, language, 0, False])

    def on_tab_width_edited(self, cell, path, new_text):
        value = int(new_text)
        self.langstore[path][2] = value
        self._plugin.language_tab[int(path)] = value
        if not value:
            self.langstore[path][3] = False
            self._plugin.language_space[int(path)] = False
        return

    def on_use_space_toggled(self, cell, path):
        self.langstore[path][3] = not self.langstore[path][3]
        self._plugin.language_space[int(path)] = self.langstore[path][3]

    def on_ok_clicked(self, event):
        self.dialog.destroy()

    def deactivate(self, event=None):
        self.langstore.clear()

        self._plugin.config_ui = None
        self._window = None
        self._plugin = None

