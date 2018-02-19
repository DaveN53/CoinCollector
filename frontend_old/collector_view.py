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
from frontend_old.xaml_view import XAMLView
from core.robinhood.robinhood_trader import RobinHoodTrader
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

class CollectorView(Window):

    def __init__(self):
        self.xaml_view = XAMLView('E:\Dev\CoinCollectorTemplate\CoinCollectorTemplate\MainWindow.xaml')
        self.window = self.xaml_view.window
        self.robinhood_trader = RobinHoodTrader()
        self.update()
        '''
        self.stack = StackPanel()
        self.Content = self.stack

        self.value_label = Label()
        self.value_label.FontSize = 48
        self.value_label.Content = 'Test'
        self.stack.Children.Add(self.value_label)

        self.curr_box = ComboBox()
        self.stack.Children.Add(self.curr_box)

        self.gain_box = TextBox()
        self.stack.Children.Add(self.gain_box)
        '''

        timer = Timer()
        timer.Tick += self.update_view
        timer.Interval = System.TimeSpan.FromSeconds(5)
        timer.Start()

    def load_ui_from_xaml(self):
        self.mainwin = XamlReader.Load(self.ui_file)

    def update_view(self, sender, args):
        self.update()

    def update(self):
        data = self.robinhood_trader.quote_data('ETH')
        self.xaml_view.tabs['dashboard']['robinhood']['eth_current'].Content = data['bid_price']
