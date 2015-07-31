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

def main():

    basedir="/disk1/erdweg/out/output2015_7_21_14_52/merged/"
    lumi = 40.028
    lumisc = float(lumi)/float(1000)

    xs= ConfigObj("/disk1/erdweg/plotting/xs_Phys14.cfg")
    bghists=HistStorage(xs,lumi,xstype=None,path=basedir)
    # bghists.setDataDriven("dataDrivenQCD")

    bglist=OrderedDict()

    # bglist["DY"]=[
     # 'DYToMuMu_13TeVPhys14DR-AVE20BX25_tsg_PHYS14_25_V3-v1MINI_P8',
     # 'DYToEE_13TeVPhys14DR-AVE20BX25_tsg_PHYS14_25_V3-v1MINI_P8'
     # 'DYJetsToEEMuMu_M-1400To2300_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v1MINI_MG',
     # 'DYJetsToEEMuMu_M-200To400_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v1MINI_MG',
     # 'DYJetsToEEMuMu_M-2300To3500_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v2MINI_MG',
     # 'DYJetsToEEMuMu_M-3500To4500_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v1MINI_MG',
     # 'DYJetsToEEMuMu_M-400To800_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v1MINI_MG',
     # 'DYJetsToEEMuMu_M-4500To6000_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v1MINI_MG',
     # 'DYJetsToEEMuMu_M-6000To7500_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v1MINI_MG',
     # 'DYJetsToEEMuMu_M-7500To8500_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v1MINI_MG',
     # 'DYJetsToEEMuMu_M-800To1400_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v1MINI_MG',
     # 'DYJetsToEEMuMu_M-8500To9500_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v2MINI_MG',
     # 'DYJetsToEEMuMu_M-9500_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v2MINI_MG',
    # ]
    # bglist["W"]=['WJetsToLNu_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v1MINI_MG',
     # 'WJetsToLNu_HT-100to200_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v1MINI_MG',
     # 'WJetsToLNu_HT-200to400_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v1MINI_MG',
     # 'WJetsToLNu_HT-400to600_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v1MINI_MG',
     # 'WJetsToLNu_HT-600toInf_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v1MINI_MG',
     # ]
    # bglist["single Top"]=['T_tW-channel-DR_13TeV-CSA14Phys14DR-PU20bx25_PHYS14_25_V1-v1MINI_PH',
     # 'Tbar_tW-channel-DR_13TeV-CSA14Phys14DR-PU20bx25_PHYS14_25_V1-v1MINI_PH',
     # ]
    # bglist["QCD jet"]=[
     # 'QCD_Pt-15to30_13TeVPhys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v1MINI_P8',
     # 'QCD_Pt-30to50_13TeVPhys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v1MINI_P8',
     # 'QCD_Pt-50to80_13TeVPhys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v2MINI_P8',
     # 'QCD_Pt-80to120_13TeVPhys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v2MINI_P8',
     # 'QCD_Pt-120to170_13TeVPhys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v2MINI_P8',
     # 'QCD_Pt-300to470_13TeVPhys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v2MINI_P8',
     # 'QCD_Pt-470to600_13TeVPhys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v2MINI_P8',
     # 'QCD_Pt-600to800_13TeVPhys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v1MINI_P8',
     # 'QCD_Pt-800to1000_13TeVPhys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v2MINI_P8',
     # 'QCD_Pt-1000to1400_13TeVPhys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v1MINI_P8',
     # 'QCD_Pt-1400to1800_13TeVPhys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v1MINI_P8',
     # 'QCD_Pt-1800to2400_13TeVPhys14DR-PU20bx25_trkalmb_PHYS14_25_V1-v2MINI_P8',
     # 'QCD_Pt-2400to3200_13TeVPhys14DR-PU20bx25_trkalmb_PHYS14_25_V1-v1MINI_P8',
     # 'QCD_Pt-3200_13TeVPhys14DR-PU20bx25_trkalmb_PHYS14_25_V1-v1MINI_P8',
    # ]
    # bglist["Diboson"]=['WZJetsTo3LNu_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v1MINI_MG',
     # 'ZZTo4L_13TeVPhys14DR-PU20bx25_PHYS14_25_V1-v1MINI_PH',
     # 'WWToLLNuNu_13TeV_PHYS14_PU20bx25_powheg'
    # ]
    # bglist["TTbar"]=['TT_13TeVPhys14DR-PU20bx25_tsg_PHYS14_25_V1-v1MINI_P8'
     # ]

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
    colorList["DY"]="pink"
    colorList['RPV M=500']="magenta"
    colorList['RPV M=1000']="red"

    bghists.additionalWeight = {
     'DYJetsToLL_M-10to50_13TeV-FXFX_MC':lumisc,
     'DYJetsToLL_M-50_13TeV-FXFX_MC':lumisc,
     'DYJetsToLL_M-100to200_13TeV-FXFX_MC':lumisc,
     'DYJetsToLL_M-200to400_13TeV-FXFX_MC':lumisc,
     'DYJetsToLL_M-400to500_13TeV-FXFX_MC':lumisc,
     'DYJetsToLL_M-500to700_13TeV-FXFX_MC':lumisc,
     'DYJetsToLL_M-700to800_13TeV-FXFX_MC':lumisc,
     'DYJetsToLL_M-800to1000_13TeV-FXFXRaw_MC':lumisc,
     'DYJetsToLL_M-1000to1500_13TeV-FXFX_MC':lumisc,
     'DYJetsToLL_M-1500to2000_13TeV-FXFX_MC':lumisc,
     'DYJetsToLL_M-2000to3000_13TeV-FXFX_MC':lumisc,
     'WJetsToLNu_13TeV-FXFX_MC':lumisc,
     'WJetsToLNu_HT-100To200_13TeVMLM_MG':lumisc,
     'WJetsToLNu_HT-200To400_13TeVMLM_MG':lumisc,
     'WJetsToLNu_HT-400To600_13TeVMLM_MG':lumisc,
     'WJetsToLNu_HT-600ToInf_13TeVMLM_MG':lumisc,
     'ST_t-channel_4f_leptonDecays_13TeV-_MC':lumisc,
     'ST_tW_top_5f_inclusiveDecays_13TeV_PH':lumisc,
     'ST_t-channel_5f_leptonDecays_13TeV-_MC':lumisc,
     'ST_s-channel_4f_leptonDecays_13TeV-_MC':lumisc,
     'ST_tW_antitop_5f_inclusiveDecays_13TeV_PH':lumisc,
     'QCD_Pt-15to20_MuEnrichedPt5_13TeV_P8':lumisc,
     'QCD_Pt-20to30_MuEnrichedPt5_13TeV_P8':lumisc,
     'QCD_Pt-20toInf_MuEnrichedPt15_13TeV_P8':lumisc,
     'QCD_Pt-30to50_MuEnrichedPt5_13TeV_P8':lumisc,
     'QCD_Pt-50to80_MuEnrichedPt5_13TeV_P8':lumisc,
     'QCD_Pt-80to120_MuEnrichedPt5_13TeV_P8':lumisc,
     'QCD_Pt-120to170_MuEnrichedPt5_13TeV_P8':lumisc,
     'QCD_Pt-170to300_MuEnrichedPt5_13TeV_P8':lumisc,
     'QCD_Pt-300to470_MuEnrichedPt5_13TeV_P8':lumisc,
     'QCD_Pt-470to600_MuEnrichedPt5_13TeV_P8':lumisc,
     'QCD_Pt-600to800_MuEnrichedPt5_13TeV_P8':lumisc,
     'QCD_Pt-800to1000_MuEnrichedPt5_13TeV_P8':lumisc,
     'QCD_Pt-1000toInf_MuEnrichedPt5_13TeV_P8':lumisc,
     'WW_13TeV_P8':lumisc,
     'WZ_13TeV_P8':lumisc,
     'ZZ_13TeV_P8':lumisc,
     'TT_13TeV_PH':lumisc,
     'TT_Mtt-1000toInf_13TeV_MCRUN2_74_V9_ext1-v2_PH':lumisc,
    }

    bghists.addFileList(bglist)

    dat_hist=HistStorage(xs,lumi,path=basedir,isData=True)
    # dat_hist.addFile("Data")

    hists=[#'Taus/h1_1_Tau_eta',
    #'Taus/h1_1_Tau_phi',
    #'Taus/h1_2_Tau_pt',
    #'Taus/h1_Tau_pt_resolution_0_500',
    #'Eles/h1_Ele_pt_resolution_0_500',
    #'Eles/h1_Ele_pt_resolution_500_1000',
    # 'Eles/h1_2_Ele_pt',
    #'Muons/h1_Muon_pt_resolution_0_500',
    #'Muons/h1_Muon_pt_resolution_500_1000',
    # 'Muons/h1_2_Muon_pt',
    'emu/Stage_0/h1_0_emu_Mass',
    #'mutau/Stage_0/h1_0_mutau_Mass',
    #'mutau/Stage_6/h1_6_mutau_Mass',
    #'Ctr/h1_Ctr_Vtx_unweighted',
    #'Ctr/h1_Ctr_Vtx_weighted',
    #'Ctr/h1_Ctr_Vtx_emu_unweighted',
    #'Ctr/h1_Ctr_Vtx_emu_weighted',
    #'Ctr/h1_Ctr_HT',
    #'Ctr/h1_Ctr_pT_hat',
    #'emu/Stage_0/h1_0_emu_Mass_resolution',
    #'mutau/Stage_0/h1_0_mutau_Mass_resolution'
    ]

    basedir="/disk1/erdweg/out/output2015_6_2_17_17/merged/"
    sghist=HistStorage(xs,lumi,path=basedir)
    sglist=OrderedDict()
 
    sglist['RPV M=500']=[
     'RPVresonantToEMu_M-500_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8',
    ]
    sglist['RPV M=1000']=[
     'RPVresonantToEMu_M-1000_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8',
    ]
    # sghist.additionalWeight = {'RPVresonantToEMu_M-500_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8':lumisc}
    # sghist.additionalWeight.update({'RPVresonantToEMu_M-1000_LLE_LQD_001_TuneCUETP8M1_13TeV-calchep-pythia8':lumisc})
    sghist.addFileList(sglist)
    histContainer=HistStorageContainer(bg=bghists,data=dat_hist,sg=sghist)

    binning={
            "Taus/h1_2_Tau_pt":10,
            "Muons/h1_2_Muon_pt":20,
            "Eles/h1_2_Ele_pt":20,
            # "emu/Stage_0/h1_0_emu_Mass":10,
            # "mutau/Stage_0/h1_0_mutau_Mass":range(200,300,20)+range(300,400,50)+range(400,1600,100)+range(1600,2000,200),
            # "mutau/Stage_6/h1_6_mutau_Mass":range(200,300,20)+range(300,400,50)+range(400,1600,100)+range(1600,2000,200),
            "_met_et":30,
    }

    binning.update({"emu/Stage_0/h1_0_emu_Mass":get_binning_from_hist('res_unc.root','func',[0,4000])})
    # binning.update({"emu/Stage_0/h1_0_emu_Mass":range(0,6000,5)})

    xranges={
            "Taus/h1_2_Tau_pt":[0,2000],
            "Muons/h1_2_Muon_pt":[0,2000],
            "Eles/h1_2_Ele_pt":[0,2000],
            "emu/Stage_0/h1_0_emu_Mass":[50,3000],
            "mutau/Stage_0/h1_0_mutau_Mass":[0,2000],
            "mutau/Stage_6/h1_6_mutau_Mass":[0,2000],
            "emu/Stage_0/h1_0_emu_Mass_resolution":[-2,2],
            "mutau/Stage_0/h1_0_mutau_Mass_resolution":[-2,2],
            "Taus/h1_Tau_pt_resolution_0_500":[-2,2],
            "Eles/h1_Ele_pt_resolution_0_500":[-2,2],
            "Eles/h1_Ele_pt_resolution_500_1000":[-2,2],
            "Muons/h1_Muon_pt_resolution_0_500":[-2,2],
            "Muons/h1_Muon_pt_resolution_500_1000":[-2,2],
            "Ctr/h1_Ctr_Vtx_unweighted":[0,40],
            "Ctr/h1_Ctr_Vtx_weighted":[0,40],
            "Ctr/h1_Ctr_Vtx_emu_unweighted":[0,40],
            "Ctr/h1_Ctr_Vtx_emu_weighted":[0,40],
    }

    bghists.initStyle(style="bg",colors=colorList)
    sghist.initStyle(style="sg",colors=colorList)

    for hist in hists:
        print("Now plotting: " + hist)
        histContainer.getHist(hist)

        binf=getDictValue(hist,binning)
        if binf is not None:
            # dat_hist.rebin(width=binf)
            bghists.rebin(width=1,vector=binf)
            sghist.rebin(width=1,vector=binf)
        # bghists.colorList=colorList
        # sghist.colorList=colorList
        # bghists.setStyle(bgcolors=colorList)
        # dat_hist.getHistList()[0].SetTitle("data")

        hist_style = sc.style_container(style = 'CMS', useRoot = False,cms=13,lumi=lumi)

        dummy = bghists.getAllAdded()
        dummy.xaxis.SetTitle('')
        dummy.yaxis.SetTitle('')
        dummy.SaveAs('plots/' + hist.replace("/","") + '.root')

        test = plotter(hist=bghists.getHistList(), sig = sghist.getHistList(),style=hist_style)
        # test.Add_data(dat_hist.getHistList()[0])
        # test.Add_plot('Signi',pos=0, height=15)

        #test.Add_plot('DiffRatio',pos=1, height=15)
        # test.Add_plot('Signi',pos=2, height=15)
        # test.Add_plot('Diff',pos=1, height=15)
        # plt.xkcd()
        hist_style.Set_error_bands_fcol(['gray','orange'])
        hist_style.Set_error_bands_ecol(['black','black'])
        hist_style.Set_error_bands_labl(['Systematics','Statistic'])

        # test.Add_plot('Ratio',pos=2, height=15)
        if hist == 'emu/Stage_0/h1_0_emu_Mass':
            sys_file=File('syst/for_plotting.root', "read")
        
            test.Add_error_hist([sys_file.Get('Sys'),sys_file.Get('MC statistic')], band_center = 'ref', stacking = 'Nosum')
            # test.Add_error_hist([sys_file.Get('MC statistic')], band_center = 'ref', stacking = 'Nosum')

        test._cms_text_x         = 0.12
        test._cms_text_y         = 0.91
# 
        # mxrange=getDictValue(hist,xranges)
        if hist in xranges.keys():
            test.Set_axis(logx=True,logy=True,xmin=xranges[hist][0],xmax=xranges[hist][1],ymin=1e-6,ymax=1e3)
            #test.Set_axis(logx=False,logy=True,xmin=0,xmax=500,ymin=1e-6,ymax=1e3)

        name=hist.replace("/","")

        test.make_plot('plots/%s.pdf'%(name))
    return 42



main()
