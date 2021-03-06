#!/usr/bin/env python
# encoding: utf-8
from . import muNewMenu    as NewMenu
from . import fmForm       as Form
from . import wgmultiline  as multiline
import weakref
import curses

class MenuViewerController(object):
    def __init__(self, menu=None):
        self.setMenu(menu)
        self.create()
        self._menuStack = []
        self._editing = False


    def create(self):
        pass
    
    
    def setMenu(self, mnu):
        self._menuStack = []
        self._setMenuWithoutResettingStack(mnu)
    
    def _setMenuWithoutResettingStack(self, mnu):
        self._menu = mnu
        self._DisplayArea._menuListWidget.value = None
        
    def _goToSubmenu(self, mnu):
        self._menuStack.append(self._menu)
        self._menu = mnu

    def _returnToPrevious(self):
        self._menu = self._menuStack.pop()


    def _executeSelection(self, sel):
        self._editing = False
        return sel()
        
    def edit(self):
        try:
            if self._menu is None:
                pass #raise ValueError("No Menu Set")
        except AttributeError:
            pass #raise ValueError("No Menu Set")
        self._editing = True
        while self._editing:
            if self._menu is not None:
                self._DisplayArea.name = self._menu.name
            self._DisplayArea.display()
            self._DisplayArea._menuListWidget.value = None
            self._DisplayArea._menuListWidget.cursor_line = 0
            _menulines = []
            _actionsToTake = []
            if len(self._menuStack) > 0:
                _menulines.append('<-- Back')
                _returnToPreviousSet = True
                _actionsToTake.append((self._returnToPrevious, ))
            else:
                _returnToPreviousSet = False
            for itm in self._menu.getItemObjects():
                if isinstance(itm, NewMenu.MenuItem):
                    _menulines.append(itm.getText())
                    _actionsToTake.append((self._executeSelection, itm.do))
                elif isinstance(itm, NewMenu.NewMenu):
                    _menulines.append('%s -->' % itm.name)
                    _actionsToTake.append((self._goToSubmenu, itm))
                else:
                    raise ValueError("menu %s contains objects I don't know how to handle." % self._menu.name)
            
            self._DisplayArea._menuListWidget.values = _menulines
            self._DisplayArea.display()
            self._DisplayArea._menuListWidget.edit()
            _vlu = self._DisplayArea._menuListWidget.value
            if _vlu is None:
                self.editing = False
                return None
            try:
                _fctn = _actionsToTake[_vlu][0]
                _args = _actionsToTake[_vlu][1:]
            except IndexError:
                try:
                    _fctn = _actionsToTake[_vlu]
                    _args = []
                except IndexError:
                    # Menu must be empty.
                    return False
            _return_value = _fctn(*_args)
        
        return _return_value
            


class MenuDisplay(MenuViewerController):
    def __init__(self, lines=15, columns=26, show_atx=5, show_aty=2, *args, **keywords):
        self._DisplayArea = MenuDisplayScreen(lines=lines, columns=columns, show_atx=show_atx, show_aty=show_aty, )
        super(MenuDisplay, self).__init__(*args, **keywords)

class MenuDisplayFullScreen(MenuViewerController):
    def __init__(self, *args, **keywords):
        self._DisplayArea = MenuDisplayScreen()
        super(MenuDisplayFullScreen, self).__init__(*args, **keywords)


class MenuDisplayScreen(Form.Form):
    def __init__(self, *args, **keywords):
        super(MenuDisplayScreen, self).__init__(*args, **keywords)
        self._menuListWidget = self.add(multiline.MultiLine, return_exit=True)

class HasMenus(object):
    MENU_KEY = "^X"
    def initialize_menus(self):
        self._NMDisplay = MenuDisplay()
        self._NMenuList = []
        self._MainMenu  = NewMenu.NewMenu
        self.add_handlers({self.__class__.MENU_KEY: self.root_menu})
        
        
    def new_menu(self, name=None):
        _mnu = NewMenu.NewMenu(name=name)
        self._NMenuList.append(_mnu)
        return weakref.proxy(_mnu)
        
    def root_menu(self, *args):
        _root_menu = NewMenu.NewMenu(name="Menus")
        for mnu in self._NMenuList:
            _root_menu.addSubmenu(mnu)            
        self._NMDisplay.setMenu(_root_menu)
        self._NMDisplay.edit()
        
    def popup_menu(self, menu):
        self.setMenu(menu)
        self.edit()



        
