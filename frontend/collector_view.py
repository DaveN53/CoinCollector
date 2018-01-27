# Reference the WPF assemblies
import clr
clr.AddReferenceByName("PresentationFramework, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
clr.AddReferenceByName("PresentationCore, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
clr.AddReference('WindowsBase')
import System.Windows
from System.Windows.Threading import DispatcherTimer as Timer

Window = System.Windows.Window
StackPanel = System.Windows.Controls.StackPanel
Label = System.Windows.Controls.Label
Button = System.Windows.Controls.Button

class CollectorView(Window):

    def __init__(self):
        self.stack = StackPanel()
        self.Content = self.stack

        self.value_label = Label()
        self.value_label.FontSize = 48
        self.value_label.Content = 'Test'
        self.stack.Children.Add(self.value_label)

        timer = Timer()
        timer.Tick += self.update_view
        timer.Interval = System.TimeSpan.FromSeconds(1)
        timer.Start()

    def update_view(self, sender, args):
        self.value_label.Content = System.DateTime.Now.ToLongTimeString()
