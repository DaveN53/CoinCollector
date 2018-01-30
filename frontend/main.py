# Reference the WPF assemblies
import clr
clr.AddReferenceByName("PresentationFramework, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
clr.AddReferenceByName("PresentationCore, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
import System.Windows

from frontend.collector_view import CollectorView, CollectorXAMLView

# Initialization Constants
Application = System.Windows.Application

# Run application
xaml_view = CollectorXAMLView('E:\Dev\CoinCollectorTemplate\CoinCollectorTemplate\MainWindow.xaml')
view = CollectorView()
app = Application()
app.Run(xaml_view.window)