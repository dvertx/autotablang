# -*- coding: utf-8 -*-
#
#  Auto Tab by Language plugin for gedit
#
#  Copyright (C) 2011, Hertatijanto Hartono <dvertx@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330,
#  Boston, MA 02111-1307, USA.

"""
2010-01-02  Version 1.0

This module provides the main plugin object which interacts with gedit.

See __init__.py for plugin's description.

Classes:
AutoTabLangPlugin
AutoTabLangWindowHelper

"""

import os
import re
import gtk
import gedit
import gtksourceview2
from gettext import gettext as _

from autotabconf import AutoTabLangConfigHelper

# Menu items
ui_str = """
<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_3"/>
      <menuitem name="AutoTabLang" action="AutoTabLangConf"/>
    </menu>
  </menubar>
</ui>
"""

class AutoTabLangWindowHelper:
    def __init__(self, plugin, window):
        self._window = window
        self._plugin = plugin

        # Insert menu items
        self._insert_menu()

    def deactivate(self):
        # Remove any installed menu items
        self._remove_menu()

        self._window = None
        self._plugin = None
        self._action_group = None

    def _insert_menu(self):
        # Get the GtkUIManager
        manager = self._window.get_ui_manager()

        # Create a new action group
        self._action_group = gtk.ActionGroup("AutoTabLangPluginActions")
        self._action_group.add_actions([("AutoTabLangConf",
                                          None,
                                          _("Manage Auto Tab by Language"),
                                          None,
                                          _("Configure tab settings of each language"),
                                          self.on_configure_activate)])

        # Insert the action group
        manager.insert_action_group(self._action_group, -1)

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)

    def _remove_menu(self):
        # Get the GtkUIManager
        manager = self._window.get_ui_manager()

        # Remove the ui
        manager.remove_ui(self._ui_id)

        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()

    def update_ui(self):
        self._action_group.set_sensitive(self._window.get_active_document() != None)

    # Menu activate handlers
    def on_configure_activate(self, action):
        self._plugin.create_configure_dialog()


class AutoTabLangPlugin(gedit.Plugin):
    """
    The main plugin class object

    """

    def __init__(self):
        gedit.Plugin.__init__(self)
        self._window = None
        self._instances = {}
        self.plugin_path = None
        self.config_ui = None

        self.tab_handler_id = None
        self.tabstate_handler_id = None

        self.languages = []
        self.language_tab = []
        self.language_space = []

    def activate(self, window):
        self._window = window
        self.tab_handler_id = window.connect("active-tab-changed", self.on_window_tab_changed)
        self.tabstate_handler_id = window.connect("active-tab-state-changed", self.on_window_tab_state_changed)
        self.plugin_path = os.path.dirname(os.path.realpath(__file__))
        self._instances[window] = AutoTabLangWindowHelper(self, window)
        self._parse_config_file()

    def _parse_config_file(self):
        self.config_file_name = os.path.join(self.plugin_path, 'autotablang.cfg')
        if os.path.exists(self.config_file_name):
            # Set global options from config file entries
            for line in open(self.config_file_name):
                params = self._split(line)
                self.languages.append(params[0])
                self.language_tab.append(int(params[1]))
                if params[2] == 'True':
                    self.language_space.append(True)
                else:
                    self.language_space.append(False)
        else:
            manager = gtksourceview2.LanguageManager()
            self.languages = manager.get_language_ids()
            self.languages.sort()
            for line in self.languages:
                self.language_tab.append(0)
                self.language_space.append(False)

            self._set_config_file()

    def _set_config_file(self):
        self.conf_file = open(self.config_file_name, 'wb')
        for index, name in enumerate(self.languages):
            self.conf_file.write("%s=%s,%s\n" % (name,
                    str(self.language_tab[index]), self.language_space[index]))

        self.conf_file.close()

    def _split(self, string):
        newstr = re.sub('\s$', '', string)
        cleanlist = re.split('[=,]', newstr)
        return cleanlist

    def _change_tab_setting(self, doc, language_id):
        """
            The setting change is applied to currently viewed document only.
            Global tab setting is not affected.

        """
        for index, lang_id in enumerate(self.languages):
            if language_id == lang_id:
                if self.language_tab[index]:
                    view = self._window.get_active_view()
                    view.set_tab_width(self.language_tab[index])
                    view.set_insert_spaces_instead_of_tabs(self.language_space[index])

    def on_window_tab_changed(self, window, tab):
        doc = tab.get_document()
        doc_language = doc.get_language()
        if doc_language:
            doc_language_id = doc_language.get_id()
            self._change_tab_setting(doc, doc_language_id)

    def on_window_tab_state_changed(self, window):
        doc = window.get_active_document()
        doc_language = doc.get_language()
        if doc_language:
            doc_language_id = doc_language.get_id()
            self._change_tab_setting(doc, doc_language_id)

    def deactivate(self, window):
        self._set_config_file()

        del self.languages[:]
        del self.language_tab[:]
        del self.language_space[:]

        self._instances[window].deactivate()
        del self._instances[window]

        window.disconnect(self.tab_handler_id)
        window.disconnect(self.tabstate_handler_id)

    def is_configurable(self):
        return True

    def create_configure_dialog(self):
        if not self.config_ui:
            self.config_ui = AutoTabLangConfigHelper(self, self._window)
        return self.config_ui.dialog

    def update_ui(self, window):
        self._instances[window].update_ui()

