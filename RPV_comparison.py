#!/bin/env python

from DukePlotALot import *
from plotlib import HistStorage,getColorList,getDictValue,HistStorageContainer
import matplotlib.pyplot as plt
from configobj import ConfigObj
try:
    from collections import OrderedDict
except ImportError:
    from ordered import OrderedDict

from rootpy.plotting.views import ScaleView
from rootpy.io import File
from rootpy.io import root_open
from rootpy.plotting.utils import find_all_primitives
from rootpy.plotting import Hist, Graph
import math

def get_hist_from_file(filename):
    tfile = root_open(filename + ".root", "READ")
    try:
        hist = tfile.Get('emu/Stage_0/h1_0_emu_Mass')
    except:
        print(' ')
        print('  help, can not find the histogram')
        print(' ')
        sys.exit(42)
    hist.Rebin(2)
    hist.Scale(1./hist.Integral())
    return _Get_rootpy_hist1d(hist,True)

def _Get_rootpy_hist1d(temp_hist,error=True):
    dummy_hist = Hist(temp_hist.GetNbinsX(), temp_hist.GetXaxis().GetXmin(), temp_hist.GetXaxis().GetXmax())
    dummy_hist.SetTitle(temp_hist.GetName())
    for i in range(0, temp_hist.GetNbinsX()):
        dummy_hist.SetBinContent(i, temp_hist.GetBinContent(i))
        if error:
            dummy_hist.SetBinError(i, temp_hist.GetBinError(i))
            if temp_hist.GetBinError(i) == temp_hist.GetBinContent(i):
                dummy_hist.SetBinError(i, temp_hist.GetBinError(i) * 0.99)
        else:
            dummy_hist.SetBinError(i, 0)
    dummy_hist.xaxis.SetTitle('$' + temp_hist.GetXaxis().GetTitle().replace('#','\\') + '$')
    dummy_hist.yaxis.SetTitle('$' + temp_hist.GetYaxis().GetTitle().replace('#','\\') + '$')
    return dummy_hist

def main():
    print("Now plotting")

    hist_style = sc.style_container(style = 'CMS', useRoot = False,cms=13,lumi=0, cmsPositon = "upper left", legendPosition = 'upper right', kind = 'Graphs')

    hist_1 = get_hist_from_file('/disk1/erdweg/testing/px_normal/SpecialHistos')
    hist_2 = get_hist_from_file('/disk1/erdweg/out/output2015_6_2_17_17/merged/RPVresonantToEMu_M-200_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8')
    # print(type(hist_1),type(hist_2))
    # dummy_hist = hist_1.Clone('ratio2')
    # print('1',type(dummy_hist))
    # dummy_hist.Divide(hist_2)
    # print('2',type(dummy_hist))

    hist_1 = Graph(hist_1.Clone('Spring15'))
    hist_1.SetLineColor('red')
    hist_1.SetTitle('Spring15')
    hist_1.xaxis.SetTitle('$M_{e\mu}$ (GeV)')
    hist_1.yaxis.SetTitle('Events')
    hist_2 = Graph(hist_2.Clone('PHYS14'))
    hist_2.SetLineColor('blue')
    hist_2.SetTitle('PHYS14')
    hist_2.xaxis.SetTitle('$M_{e\mu}$ (GeV)')
    hist_2.yaxis.SetTitle('Events')

    # print('3',type(dummy_hist))

    test = plotter(sig=[hist_1,hist_2],style=hist_style)
    # print('4',type(dummy_hist))
    test.Add_plot('Empty',pos=1, height=15, label='S15/P14')
    # print('4.1',type(dummy_hist))
    # ratio = dummy_hist.Clone('ratio21')
    # print('4.2',type(ratio))
    test.create_plot()
    # print('5',type(ratio))

    tfile = root_open('/disk1/erdweg/testing/px_normal/SpecialHistos.root', "READ")
    d_hist1 = tfile.Get('emu/Stage_0/h1_0_emu_Mass')
    d_hist1.Rebin(2)
    d_hist1.Scale(1./d_hist1.Integral())
    tfile = root_open('/disk1/erdweg/out/output2015_6_2_17_17/merged/RPVresonantToEMu_M-200_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8.root', "READ")
    d_hist2 = tfile.Get('emu/Stage_0/h1_0_emu_Mass')
    d_hist2.Rebin(2)
    d_hist2.Scale(1./d_hist2.Integral())
    print(type(hist_1),type(hist_2))

    ratio = d_hist1.Clone('ratio')
    for ibin,jbin,lbin in zip(ratio,d_hist1,d_hist2):
        if lbin.value != 0:
            ibin.value = jbin.value/lbin.value
            ibin.error = math.sqrt(jbin.error**2/lbin.value**2 + (lbin.error**2 * jbin.value**2)/lbin.value**4)
        else:
            ibin.value = -100
            ibin.error = 0
    # print('6',type(ratio))
    duke_errorbar(ratio, xerr = hist_style.Get_xerr(), emptybins = False, axes = test.Get_axis2(),
                  markersize = hist_style.Get_marker_size(),
                  marker = hist_style.Get_marker_style(),
                  ecolor = hist_style.Get_marker_color(),
                  markerfacecolor = hist_style.Get_marker_color(),
                  markeredgecolor = hist_style.Get_marker_color(),
                  capthick = hist_style.Get_marker_error_cap_width(),
                  zorder = 2.2)

    test.Get_axis1().set_ylim(ymin = 1e-4, ymax = 1)
    test.Get_axis1().set_xlim(xmin = 100, xmax = 300)
    test.Get_axis2().set_ylim(ymin = 0, ymax = 3.)

    test.SavePlot('plots/RPV_comparison.pdf')
    return 42



main()
