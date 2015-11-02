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

def get_hist_from_file(filename,histname,rebinfac = 2, doNorm = True):
    tfile = root_open(filename + ".root", "READ")
    try:
        hist = tfile.Get(histname)
    except:
        print(' ')
        print('  help, can not find the histogram')
        print(' ')
        sys.exit(42)
    hist.Rebin(rebinfac)
    if doNorm:
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

def make_plot(hist_name = 'emu/Stage_0/h1_0_emu_Mass', rebin = 40, y1_mi= 1e-4, y1_ma = 1, x_mi= 0, x_ma= 900, y2_mi= 0., y2_ma= 2., doRatio = True, label = '$M_{e\mu}$ (GeV)'):
    print("Now plotting: %s"%hist_name)

    hist_style = sc.style_container(style = 'CMS', useRoot = False,cms=13,lumi=0, cmsPositon = "upper left", legendPosition = 'upper right', kind = 'Graphs')

    hist_50 = get_hist_from_file('/disk1/erdweg/television/DATA_50/merged/allData',hist_name,rebinfac = rebin)
    hist_25 = get_hist_from_file('/disk1/erdweg/television/DATA_25/merged/allData',hist_name,rebinfac = rebin)

    hist_50 = Graph(hist_50.Clone('50ns'))
    hist_50.SetLineColor('red')
    hist_50.SetTitle('50ns')
    hist_50.xaxis.SetTitle(label)
    hist_50.yaxis.SetTitle('Events')
    hist_25 = Graph(hist_25.Clone('25ns'))
    hist_25.SetLineColor('blue')
    hist_25.SetTitle('25ns')
    hist_25.xaxis.SetTitle(label)
    hist_25.yaxis.SetTitle('Events')

    test = plotter(sig=[hist_50,hist_25],style=hist_style)
    if doRatio:
        test.Add_plot('Empty',pos=1, height=15, label='50ns/25ns')
    test.create_plot()
    if doRatio:
        tfile = root_open('/disk1/erdweg/television/DATA_50/merged/allData.root', "READ")
        d_hist1 = tfile.Get(hist_name)
        d_hist1.Rebin(rebin)
        d_hist1.Scale(1./d_hist1.Integral())
        tfile = root_open('/disk1/erdweg/television/DATA_25/merged/allData.root', "READ")
        d_hist2 = tfile.Get(hist_name)
        d_hist2.Rebin(rebin)
        d_hist2.Scale(1./d_hist2.Integral())
    
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

    test.Get_axis1().set_ylim(ymin = y1_mi, ymax = y1_ma)
    test.Get_axis1().set_xlim(xmin = x_mi, xmax = x_ma)
    if doRatio:
        test.Get_axis2().set_ylim(ymin = y2_mi, ymax = y2_ma)

    test.SavePlot('plots/BX_comparison'+hist_name.split('/')[-1]+'.pdf')
    return 42

def main():
    make_plot(hist_name = 'emu/Stage_0/h1_0_emu_Mass', rebin = 40)
    make_plot(hist_name = 'Ctr/h1_Ctr_Vtx_weighted', rebin = 1, x_mi= 0, x_ma= 40, doRatio = False, label = '$N_{vtx}$')
    make_plot(hist_name = 'emu/Stage_0/h1_0_emu_eta_ele', rebin = 1, x_mi= -3, x_ma= 3., y2_mi= 0., y2_ma= 2., label = '$\eta$')
    make_plot(hist_name = 'emu/Stage_0/h1_0_emu_pT_ele', rebin = 1, y1_mi= 1e-4, y1_ma = 1, x_mi= 0, x_ma= 400, label = '$p_{T}^{e}$ (GeV)')
    make_plot(hist_name = 'emu/Stage_0/h1_0_emu_eta_muo', rebin = 1, x_mi= -3, x_ma= 3., y2_mi= 0., y2_ma= 2., label = '$\eta$')
    make_plot(hist_name = 'emu/Stage_0/h1_0_emu_pT_muo', rebin = 1, y1_mi= 1e-4, y1_ma = 1, x_mi= 0, x_ma= 400, label = '$p_{T}^{\mu}$ (GeV)')

main()
