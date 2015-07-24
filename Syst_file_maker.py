#!/bin/env python

from DukePlotALot import *
from plotlib import HistStorage,getColorList,getDictValue,HistStorageContainer
import matplotlib.pyplot as plt
import ROOT as r
import numpy as np
from configobj import ConfigObj
try:
    from collections import OrderedDict
except ImportError:
    from ordered import OrderedDict
from rootpy.io import File
from rootpy.plotting.views import ScaleView
import array
import style_class as sc

def get_binning_from_hist(file_name, hist_name, plot_range, debug=False):
    res_file = File(file_name, "read")
    res_hist = res_file.Get(hist_name)
    binning = [plot_range[0]]
    value = plot_range[0]
    while(binning[-1] < plot_range[1]):
        value = res_hist.Eval(binning[-1])
        value *= binning[-1]
        if value < 1:
            if debug:
                print('appending 1, last value: %f'%binning[-1])
            binning.append(binning[-1]+1)
        else:
            if debug:
                print('appending %f, last value: %f'%(round(value),binning[-1]))
            binning.append(binning[-1]+round(value))
    if binning[-1] > plot_range[1]:
        binning[-1] = plot_range[1]
    res_file.Close()
    if debug:
        print(binning)
    return binning

def fit_histo(hist,function='exp([0]*x+[1]) *x^[2]',funcbeg=450,funcend=2000,fitbeg=150,fitend=1500):
    return hist
    # r.Math.MinimizerOptions.SetDefaultMinimizer("Minuit2","Combined")
    # r.Math.MinimizerOptions.SetDefaultMaxIterations(500000000)#if minimizer = GLS
    # r.Math.MinimizerOptions.SetDefaultMaxFunctionCalls(500000000)#if minimizer = minuit
    # r.Math.MinimizerOptions.SetDefaultTolerance(0.0001)
    func = r.TF1("f1",function, funcbeg, funcend)

    start_vals = [-0.0217012, -14.2804, 4.08996]

    for i in range(len(start_vals)):
        func.SetParameter(i,start_vals[i])

    # func.SetNpx(hist.GetNbinsX())
    fit_res = hist.Fit(func,"+SQ","", fitbeg, fitend)
    fit_res.Print("Q")
    fit_status = int(fit_res)
    print "status:",fit_status

    dummy_bins = int(funcend)
    histFit = Hist(hist.GetNbinsX(),0,hist.GetNbinsX()*hist.GetBinWidth(1))

    dummy_file = r.TFile('%s.root'%hist.GetTitle(),'RECREATE')
    hist.Write()
    func.Write()
    # rebinfactor=hist.GetBinWidth(1)
    # print "rebinfactor:",rebinfactor
    # raw_input('bla')
    for i in range(0, hist.FindBin(funcbeg)):
        histFit.SetBinContent(i,hist.GetBinContent(i))
        histFit.SetBinError(i,hist.GetBinError(i))
    for i in range(hist.FindBin(funcbeg), hist.GetNbinsX()):
        histFit.SetBinContent(i,(func.Integral(hist.GetBinLowEdge(i),hist.GetBinLowEdge(i)+hist.GetBinWidth(i))/hist.GetBinWidth(i)))
        try:
            histFit.SetBinError(i,np.sqrt(histFit.GetBinContent(i)))
        except:
            print "No good fit use the hist"
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            print(sys.exc_info()[2])
            dummy_file.Close()
            return hist
    histFit.Write()
    dummy_file.Close()

    return histFit

def main():

    basedir="/disk1/erdweg/out/output2015_7_21_14_52/merged/"
    lumi=1000.

    xs= ConfigObj("/disk1/erdweg/plotting/xs_Phys14.cfg")

    bghists=HistStorage(xs,lumi,xstype=None,path=basedir)

    bglist=OrderedDict()

    bglist["DY"]=[
     'DYJetsToLL_M-10to50_13TeV-FXFX_MC',
     'DYJetsToLL_M-50_13TeV-FXFX_MC',
     'DYJetsToLL_M-100to200_13TeV-FXFX_MC',
     'DYJetsToLL_M-200to400_13TeV-FXFX_MC',
     'DYJetsToLL_M-400to500_13TeV-FXFX_MC',
     'DYJetsToLL_M-500to700_13TeV-FXFX_MC',
     'DYJetsToLL_M-700to800_13TeV-FXFX_MC',
     'DYJetsToLL_M-800to1000_13TeV-FXFXRaw_MC',
     'DYJetsToLL_M-1000to1500_13TeV-FXFX_MC',
     'DYJetsToLL_M-1500to2000_13TeV-FXFX_MC',
     'DYJetsToLL_M-2000to3000_13TeV-FXFX_MC',
    ]
    bglist["W"]=[
     'WJetsToLNu_13TeV-FXFX_MC',
     'WJetsToLNu_HT-100To200_13TeVMLM_MG',
     'WJetsToLNu_HT-200To400_13TeVMLM_MG',
     'WJetsToLNu_HT-400To600_13TeVMLM_MG',
     'WJetsToLNu_HT-600ToInf_13TeVMLM_MG',
    ]
    bglist["single Top"]=[
     'ST_t-channel_4f_leptonDecays_13TeV-_MC',
     'ST_tW_top_5f_inclusiveDecays_13TeV_PH',
     'ST_t-channel_5f_leptonDecays_13TeV-_MC',
     'ST_s-channel_4f_leptonDecays_13TeV-_MC',
     'ST_tW_antitop_5f_inclusiveDecays_13TeV_PH',
    ]
    bglist["QCD jet"]=[
     'QCD_Pt-15to20_MuEnrichedPt5_13TeV_P8',
     'QCD_Pt-20to30_MuEnrichedPt5_13TeV_P8',
     'QCD_Pt-20toInf_MuEnrichedPt15_13TeV_P8',
     'QCD_Pt-30to50_MuEnrichedPt5_13TeV_P8',
     'QCD_Pt-50to80_MuEnrichedPt5_13TeV_P8',
     'QCD_Pt-80to120_MuEnrichedPt5_13TeV_P8',
     'QCD_Pt-120to170_MuEnrichedPt5_13TeV_P8',
     'QCD_Pt-170to300_MuEnrichedPt5_13TeV_P8',
     'QCD_Pt-300to470_MuEnrichedPt5_13TeV_P8',
     'QCD_Pt-470to600_MuEnrichedPt5_13TeV_P8',
     'QCD_Pt-600to800_MuEnrichedPt5_13TeV_P8',
     'QCD_Pt-800to1000_MuEnrichedPt5_13TeV_P8',
     'QCD_Pt-1000toInf_MuEnrichedPt5_13TeV_P8',
    ]
    bglist["Diboson"]=[
     'WW_13TeV_P8',
     'WZ_13TeV_P8',
     'ZZ_13TeV_P8'
    ]
    bglist["TTbar"]=[
     'TT_13TeV_PH',
     'TT_Mtt-1000toInf_13TeV_MCRUN2_74_V9_ext1-v2_PH',
     ]

    colorList={}
    colorList["W"]="lightblue"
    colorList["Diboson"]="y"
    colorList["single Top"]="darkmagenta"
    colorList["QCD jet"]="darkblue"
    colorList["TTbar"]="chartreuse"
    colorList["WW"]="green"
    colorList["DY"]="red"

    bghists.addFileList(bglist)

    colorList2=getColorList(15)
    bghists.colorList=colorList

    basedir="/disk1/erdweg/out/output2015_6_2_17_17/merged/"

    sghist=HistStorage(xs,lumi,path=basedir)

    sglist=[
     'RPVresonantToEMu_M-200_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8',
     'RPVresonantToEMu_M-500_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8',
     'RPVresonantToEMu_M-1000_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8',
     'RPVresonantToEMu_M-1400_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8',
     'RPVresonantToEMu_M-2000_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8',
     'RPVresonantToEMu_M-3000_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8',
     'RPVresonantToEMu_M-4000_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8',
     'RPVresonantToEMu_M-4000_LLE_LQD_01_TuneCUETP8M1_13TeV-calchep-pythia8',
     'RPVresonantToEMu_M-4000_LLE_LQD_02_TuneCUETP8M1_13TeV-calchep-pythia8',
     'RPVresonantToEMu_M-4000_LLE_LQD_05_TuneCUETP8M1_13TeV-calchep-pythia8',
     'RPVresonantToEMu_M-5000_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8',
     'RPVresonantToEMu_M-6000_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8'
    ]
    sghist.addFileList(sglist)

    special_colors = {
     'Ele_syst_Scale':'red',
     'Muon_syst_Scale':'blue',
     'Muon_syst_Resolution':'green',
     'Tau_syst_Scale':'pink',
     'MET_syst_Scale':'teal',
     'Jet_syst_Scale':'magenta',
     'Jet_syst_Resolution':'gray',
    }

    syst_part=      ["Ele", "Muon", "Tau", "MET", "Jet"]
    syst_type=      ["Scale", "Resolution"]
    syst_updown=    ["Up", "Down"]
    hists=[]
    hists.append("emu/Stage_0/h1_0_emu_Mass")
    for part in syst_part:
        for itype in syst_type:
            if (part == 'Ele' or part == 'Tau' or part == 'MET') and itype == 'Resolution':
                continue
            for updown in syst_updown:
                hists.append("emu/Stage_0/sys/h1_0_emu_Mass_%s_syst_%s%s"%(part,itype,updown))

    histContainer=HistStorageContainer(bg=bghists,sg=sghist)

    bghists.initStyle(style="bg")
    sghist.initStyle(style="sg")

    useROOOT=False

    hist_style = sc.style_container(style = 'CMS' ,cmsPositon="upper left", useRoot = useROOOT,cms = 13, lumi = 1000)

    bg_outFile=File("syst/bg_for_limit.root", "recreate")

    sigOut={}
    for sig in sghist.files:
        sigOut[sig]=File("syst/%s.root"%(sig), "recreate")

    syst_hists=OrderedDict()
    mainHist=None
    rel_systhist=OrderedDict()
    systcolors=getColorList(len(hists))

    sghist.getHist("h_counters")
    for sig in sigOut:
        sigOut[sig].WriteObject(sghist.hists[sig],"h_counters")

    for hist in hists:

        histContainer.getHist(hist)
        histContainer.setTitle("M_T [GeV]")
        histContainer.rebin(vector=get_binning_from_hist('res_unc.root','func',[0,4000]))

        allbg=bghists.getAllAdded()
        if allbg.integral() <1:
            print "ignored hist: ",hist
            continue
        allbg = fit_histo(allbg)
        allbg.SetTitle(hist.replace("emu/Stage_0/h1_0_emu_Mass","Main"))
        allbg.decorate(fillstyle = '0',linewidth = 1,linecolor = systcolors.pop())

        if hist=="emu/Stage_0/h1_0_emu_Mass":
            mainHist=allbg
        else:
            rel_systhist[hist] = (allbg/mainHist)
            rel_systhist[hist].SetTitle(hist.replace("emu/Stage_0/h1_0_emu_Mass",""))
            rel_systhist[hist].GetYaxis().SetTitle("rel uncertainty")
            for ibin in rel_systhist[hist].bins():
                ibin.value=ibin.value-1.
        syst_hists[hist]=allbg

        if hist=="emu/Stage_0/h1_0_emu_Mass":
            bg_outFile.WriteObject(allbg,"Main")
        else:
             bg_outFile.WriteObject(allbg,hist.replace("emu/Stage_0/h1_0_emu_Mass","Main"))
        print hist.replace("emu/Stage_0/h1_0_emu_Mass","Main")

        for sig in sigOut:
            if hist=="emu/Stage_0/h1_0_emu_Mass":
                sigOut[sig].WriteObject(sghist.hists[sig],"Main")
            else:
                sigOut[sig].WriteObject(sghist.hists[sig],hist.replace("emu/Stage_0/h1_0_emu_Mass","Main"))

        bgs=histContainer.getBGList()
        for ih in bgs:
            ih.SetTitle(ih.GetTitle().replace("emu/Stage_0/h1_0_emu_Mass"," "))

        test = plotter(hist=bgs,style=hist_style,cmsPositon="upper left",useRoot = useROOOT)

        test.Set_axis(xmin=0,xmax=3000)

        name=hist.replace("/","")


        plot=test.create_plot()
        test.SavePlot('syst/%s.png'%(name))
        test.SavePlot('syst/%s.pdf'%(name))
        del test

    test = plotter(sig=syst_hists.values(),style=hist_style,useRoot = useROOOT)
    test.create_plot()
    test.SavePlot('syst/allsyst.png')
    test.SavePlot('syst/allsyst.pdf')
    del test


    test = plotter(sig=rel_systhist.values(),style=hist_style,useRoot = useROOOT)
    test.Set_axis(logy=False,ymin=-0.5,ymax=1.,xmin=0,xmax=3000)
    test.create_plot()
    test.SavePlot('syst/relsyst.png')
    test.SavePlot('syst/relsyst.pdf')
    del test

    rel_systhist_abs=OrderedDict()
    for part in syst_part:
        for itype in syst_type:
            if (part == 'Ele' or part == 'Tau' or part == 'MET') and itype == 'Resolution':
                continue
            rel_systhist_abs["emu/Stage_0/sys/h1_0_emu_Mass_%s_syst_%s"%(part,itype)] = rel_systhist["emu/Stage_0/sys/h1_0_emu_Mass_%s_syst_%s%s"%(part,itype,'Up')]
            rel_systhist_abs["emu/Stage_0/sys/h1_0_emu_Mass_%s_syst_%s"%(part,itype)].SetTitle(rel_systhist_abs["emu/Stage_0/sys/h1_0_emu_Mass_%s_syst_%s"%(part,itype)].GetTitle().replace('Up','').replace('emu/Stage_0/sys/h1_0_emu_Mass_',''))
            rel_systhist_abs["emu/Stage_0/sys/h1_0_emu_Mass_%s_syst_%s"%(part,itype)].SetColor(special_colors[rel_systhist_abs["emu/Stage_0/sys/h1_0_emu_Mass_%s_syst_%s"%(part,itype)].GetTitle()])
            rel_systhist_abs["emu/Stage_0/sys/h1_0_emu_Mass_%s_syst_%s"%(part,itype)].GetXaxis().SetTitle('$M_{e\mu}$ (GeV)')
            for (ibin,jbin,kbin) in zip(rel_systhist_abs["emu/Stage_0/sys/h1_0_emu_Mass_%s_syst_%s"%(part,itype)],rel_systhist["emu/Stage_0/sys/h1_0_emu_Mass_%s_syst_%s%s"%(part,itype,'Up')],rel_systhist["emu/Stage_0/sys/h1_0_emu_Mass_%s_syst_%s%s"%(part,itype,'Down')]):
                if abs(jbin.value) > abs(kbin.value):
                    ibin.value=abs(jbin.value)
                else:
                    ibin.value=abs(kbin.value)

    stat_hist = allbg.clone('MC statistic')
    for ibin in stat_hist:
        ibin.value = 0
    stat_hist.SetTitle('MC statistic')
    stat_hist.SetName('MC statistic')
    stat_hist.SetColor('orange')
    for (ibin,jbin) in zip(stat_hist,mainHist):
        if jbin.value != 0:
            # print(ibin.idx,jbin.value,jbin.error)
            ibin.value = abs(jbin.error / jbin.value)
        else:
            # print(ibin.idx,'  setting zero')
            ibin.value = 0.0

    rel_systhist_abs['MC statistic'] = stat_hist

    sum_hist = allbg.clone('Sum')
    for ibin in sum_hist:
        ibin.value = 0
    sum_hist.SetTitle('Sum')
    sum_hist.SetName('Sum')
    sum_hist.SetColor('black')
    for item in rel_systhist_abs:
        for (ibin,jbin) in zip(sum_hist,rel_systhist_abs[item]):
            ibin.value += (jbin.value**2)

    for ibin in sum_hist:
        ibin.value = np.sqrt(ibin.value)
        if ibin.value > 2:
            ibin.value = 0

    rel_systhist_abs['sum'] = sum_hist

    sys_hist = allbg.clone('Sys')
    for ibin in sys_hist:
        ibin.value = 0
    sys_hist.SetTitle('Sys')
    sys_hist.SetName('Sys')
    sys_hist.SetColor('black')
    for item in rel_systhist_abs:
        if 'statistic' in item:
            continue
        for (ibin,jbin) in zip(sys_hist,rel_systhist_abs[item]):
            ibin.value += (jbin.value**2)

    for ibin in sys_hist:
        ibin.value = np.sqrt(ibin.value)
        if ibin.value > 2:
            ibin.value = 0

    sum_outFile=File("syst/for_plotting.root", "recreate")
    sys_hist.Write()
    stat_hist.Write()
    sum_outFile.Close()

    test = plotter(sig=rel_systhist_abs.values(),style=hist_style,useRoot = useROOOT)
    test.Set_axis(logy=False,ymin=0.,ymax=0.6,xmin=0,xmax=1000)
    test.create_plot()
    test.SavePlot('syst/relsyst_comb.png')
    test.SavePlot('syst/relsyst_comb.pdf')
    del test


    bg_outFile.Close()
    for sig in sigOut:
        sigOut[sig].Close()

    return 42



main()
