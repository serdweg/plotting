#!/bin/env python

from DukePlotALot import *

from plotlib import HistStorage, getColorList, getDictValue, HistStorageContainer
try:
    from collections import OrderedDict
except ImportError:
    from ordered import OrderedDict

from rootpy.plotting.views import ScaleView

import style_class as sc

def create_test_histos():
    # set the random seed
    ROOT.gRandom.SetSeed(42)
    np.random.seed(42)

    # signal distribution
    signal = 126 + 10 * np.random.randn(1000)
    signal_obs = 126 + 10 * np.random.randn(1000)

    # create histograms
    h1 = Hist(30, 40, 200, title='Background', markersize=0)
    h2 = h1.Clone(title='Signal')
    h3 = h1.Clone(title='Pseudo Data')

    # fill the histograms with our distributions
    h1.FillRandom('landau', 10000)
    map(h2.Fill, signal)
    h3.FillRandom('landau', 10000)
    map(h3.Fill, signal_obs)

    return h1, h2, h3

bag_hist, sig_hist, dat_hist = create_test_histos()

bag_hist.fillstyle = 'solid'
bag_hist.fillcolor = 'green'
bag_hist.linecolor = 'green'
bag_hist.linewidth = 0
bag_hist.yaxis.SetTitle('Events')
bag_hist.xaxis.SetTitle('Mass (GeV)')

sig_hist.fillstyle = '0'
sig_hist.fillcolor = 'red'
sig_hist.linecolor = 'red'
sig_hist.linewidth = 1
sig_hist.yaxis.SetTitle('Events')
sig_hist.xaxis.SetTitle('Mass (GeV)')

bag_hist.Scale(0.5)
bag_hist_2 = bag_hist.Clone(title='Background 2')
bag_hist_2.fillcolor = 'y'
bag_hist_2.linecolor = 'y'

hist_style = sc.style_container(style = 'CMS', useRoot = False)
hist_style.Set_additional_text('plot dummy')

test = plotter(hist=[bag_hist_2,bag_hist], sig = [sig_hist], cms = 13, lumi = 19700, style=hist_style)
test.Add_data(dat_hist)
test.Set_axis(ymin = 20, ymax = 5*1e3)
test.make_plot('bla_plt.pdf')
