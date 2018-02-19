# Reference the WPF assemblies
import clr
clr.AddReferenceByName("PresentationFramework, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
clr.AddReferenceByName("PresentationCore, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
clr.AddReference('WindowsBase')
import System.Windows
from System.Windows.Threading import DispatcherTimer as Timer
from System.Windows.Markup import XamlReader
from System.IO import File

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

Window = System.Windows.Window
StackPanel = System.Windows.Controls.StackPanel
Label = System.Windows.Controls.Label
ComboBox = System.Windows.Controls.ComboBox
TextBox = System.Windows.Controls.TextBox
Button = System.Windows.Controls.Button
TabItem = System.Windows.Controls.TabItem
TabControl = System.Windows.Controls.TabControl


class XAMLView:
    """
    Content is always a grid
    Accessing elements: self.tabs['dashboard']['robinhood']['usd_wallet']
    """
    def __init__(self, ui_file):
        self.ui_file = File.OpenRead(ui_file)
        self.window = XamlReader.Load(self.ui_file)
        # Window.Grid.TabControl.Tabs
        self.window_tabs = self.window.Content.Children[0].Items
        self.tabs = {}
        self.store_elements_in_dict()

    def get_tab_children(self, tab_item):
        return tab_item.Content.Children[0]

    def get_grid_children(self, grid_item):
        return grid_item.Children

    def store_elements_in_dict(self):
        for tab in self.window_tabs:
            self.tabs[tab.Name] = self.get_tab_children_as_dict(tab)
        log.info(self.tabs)

    def get_tab_children_as_dict(self, tab_item):
        log.info("##################")
        tab_children = {}
        # tab.Grid.Children
        if tab_item.Content.Children.Count > 0:
            #for child in tab.grid.children
            for child in tab_item.Content.Children:
                if type(child) is TabControl:
                    # For tab in tab control
                    for child_item in child.Items:
                        if type(child_item) is TabItem:
                            log.info(child_item.Name)
                            tab_children[child_item.Name] = self.get_tab_children_as_dict(child_item)
                else:
                    log.info(child.Name)
                    tab_children[child.Name] = child
        return tab_children