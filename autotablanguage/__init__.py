# -*- coding: utf-8 -*-
#
#  Auto Tab by Language plugin for gedit
#
#  Copyright (C) 2011, Hertatijanto Hartono <dvertx@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
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
Auto Tab by Language plugin package
2010-01-02  Version 1.0

Description:
This plugin tries to provide programmers with automatic tab settings when
certain document types are being viewed and edited. Programmers who writes
codes in several programming languages might find this useful, since they
can configure the tab setting to suit the indenting style they want for
each programming language.


Files:
autotablang.gedit-plugin       -- Plugin.
autotablanguage/               -- Package directory
    __init__.py                -- Package module loaded by Gedit.
    autotablang.py             -- Plugin and plugin helper classes.
    autotabconf.py             -- Configuration window class.
    autotabconf.glade          -- Configuration window layout from Glade.

"""
from autotablang import AutoTabLangPlugin

