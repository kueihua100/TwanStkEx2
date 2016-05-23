# -*- coding: utf-8 -*-

from sys import exit

# matplotlib requires wxPython 2.8+
import wxversion
try:
    wxversion.ensureMinimal('2.8')
except:
    exit("wxPython version error: matplotlib requires wxPython 2.8+!!")

import wx
import datetime as dtime

from pandas.io.data import DataReader
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg

g_stk_canvas = None
g_stk_plot = None

def PlotHistoryDayPrice(stk_canvas, stk_plot, stock_num = None):
    '''
    1. The data from Yahoo! Finance is not grabbed by calling url apis, is by using Pandas APIs.
    2. This program is to get TWSE data only, if wants OTC data, need to modify code.
    '''

    #Clear the current axes
    stk_plot.cla()
    #Turn the axes grids on 
    stk_plot.grid(True)

    #if not assign stock num, give a default one
    if not stock_num:
        stock_num = "^twii"

    #data start from:
    startday = dtime.date(2000, 1, 1)

    #check for TSEC weighted index
    if stock_num == "^twii":
        stock_title= "{} day price".format("TSEC weighted index")
        stock_str = stock_num
    else:
        stock_title= "{} day price".format(stock_num)
        #append ".TW" after stock_num to tell yahoo!Finance to query TWSE stock data.
        # If want to query OTC, please add ".TWO"
        stock_str = "{}.TW".format(stock_num)
    #print stock_str
    
    #plot title
    stk_plot.set_title(stock_title)

    #about how the DataReader() works, please refer to data.py from pandas
    try:
        stock_data = DataReader(stock_str, 'yahoo', startday)
        #plot date and price
        stk_plot.plot(stock_data.index, stock_data['Close'])
        #show
        stk_canvas.draw()
    except:
        # If error happened, show a dialog instead of exit the ap.
        #exit("Error happened!!\n")
        msg = "Fetch stock data error!\nPlease check the stock num or try again!!"
        dlg = wx.MessageDialog(stk_canvas, msg, 'Error', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
    
def StkPlotPanel(parent_widget):
    '''
    1. Create wxPython canvas: The FigureCanvas contains the figure and does event handling.
    '''
    plot_panel = wx.Panel(parent_widget)
    
    #Setup figure
    stock_fig = Figure()
    stock_canvas = FigureCanvasWxAgg(plot_panel, -1, stock_fig)
    global g_stk_canvas
    g_stk_canvas = stock_canvas
    
    #stock_plt = plt.subplot2grid((1, 1), (0, 0), colspan=1)
    stock_plt = stock_fig.add_subplot(1, 1, 1)
    global g_stk_plot
    g_stk_plot = stock_plt

    # Now put stock_canvas into a box
    box2 = wx.BoxSizer(wx.VERTICAL)
    box2.Add(stock_canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
    plot_panel.SetSizer(box2)
    
    #return plot_panel to be added into main_panel for re-sizing handling
    return plot_panel

def OnInput(event):
    stock_num = event.GetString()
    print "[OnInput] stock num is: %s" % stock_num

    #show historical day price
    PlotHistoryDayPrice(g_stk_canvas, g_stk_plot, stock_num)
    
def main():
    '''
    1. Use wxPython to UI for user to input stock num that will query.
    2. The data from Yahoo! Finance is not grabbed by calling url apis, is by using Pandas APIs.
    '''
    
    #init wx App:
    app = wx.App()
    
    #init top level frame and panel
    main_frame = wx.Frame(None, -1, "TwanStkEx2")
    main_panel = wx.Panel(main_frame)

    # widget layout as below:
    # ---------------------------
    # -   Text: input_control   -  (1 box put 2 widgets in the "input panel")
    # ---------------------------
    # -                         -
    # -    stk_panel            -  (1 box to 1 plot in thr Stk_panel)
    # -                         -
    # -                         -
    # ---------------------------
    
    #create input panel:
    input_panel = wx.Panel(main_panel)
    #create stk panel:
    stk_panel = StkPlotPanel(main_panel)
    
    #create info/input widgets:
    stock_text = wx.StaticText(input_panel, -1, "Stock num:")
    stock_input = wx.TextCtrl(input_panel, -1, "^twii", style=wx.TE_PROCESS_ENTER)
    stock_input.Bind(wx.EVT_TEXT_ENTER, OnInput)
    
    #put info/input widgets into a box
    box1 = wx.BoxSizer()
    box1.Add(stock_text, 1, wx.LEFT|wx.Top, 10)
    #add 10 padding/border to stock_text widget
    box1.Add(stock_input, 1, wx.LEFT|wx.Top, 10)
    #info/input widgets into input panel
    input_panel.SetSizer(box1)

    #put input_panel and stk_panel into a box
    box3 = wx.BoxSizer(wx.VERTICAL)
    box3.Add(input_panel, 0)
    box3.Add(stk_panel, 1, wx.LEFT | wx.TOP | wx.GROW)
    main_panel.SetSizer(box3)
    
    #show historical day price
    PlotHistoryDayPrice(g_stk_canvas, g_stk_plot)
    
    #show UI
    main_frame.Show(1)
    #start UI event loop
    app.MainLoop()
    
if __name__ == '__main__':
    main()