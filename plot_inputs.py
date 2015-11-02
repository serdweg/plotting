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

def get_binning_from_hist(file_name, hist_name, plot_range, debug=False, min_binning = 1):
    res_file = File(file_name, "read")
    res_hist = res_file.Get(hist_name)
    binning = [plot_range[0]]
    value = plot_range[0]
    while(binning[-1] < plot_range[1]):
        value = res_hist.Eval(binning[-1])
        value *= binning[-1]
        if value < min_binning:
            if debug:
                print('appending %f, last value: %f'%(min_binning,binning[-1]))
            binning.append(binning[-1]+min_binning)
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

# 
basedir="/disk1/erdweg/television/BACKGROUND/merged/"
# lumi = 40.8 + 16.3 + 25.028
lumi = 1620.957
# lumi = 981.610
lumisc = float(lumi)/float(1000)

xs= ConfigObj("/disk1/erdweg/plotting/xs_Phys14.cfg")
bghists=HistStorage(xs,lumi,xstype=None,path=basedir)

bglist=OrderedDict()

bglist["DY"]=[
 'ZToEE_NNPDF30_13TeV_M_50_120_PH-skimid3044',
 'ZToEE_NNPDF30_13TeV_M_120_200_PH-skimid3023',
 'ZToEE_NNPDF30_13TeV_M_200_400_PH-skimid2867',
 'ZToEE_NNPDF30_13TeV_M_400_800_PH-skimid2872',
 'ZToEE_NNPDF30_13TeV_M_800_1400_PH-skimid3012',
 'ZToEE_NNPDF30_13TeV_M_1400_2300_PH-skimid2854',
 'ZToEE_NNPDF30_13TeV_M_2300_3500_PH-skimid2853',
 'ZToEE_NNPDF30_13TeV_M_3500_4500_PH-skimid2857',
 'ZToEE_NNPDF30_13TeV_M_4500_6000_PH-skimid2856',
 'ZToEE_NNPDF30_13TeV_M_6000_Inf_PH-skimid2892',
 'ZToMuMu_NNPDF30_13TeV_M_50_120_PH-skimid3048',
 'ZToMuMu_NNPDF30_13TeV_M_120_200_PH-skimid2559',
 'ZToMuMu_NNPDF30_13TeV_M_200_400_PH-skimid2310',
 'ZToMuMu_NNPDF30_13TeV_M_400_800_PH-skimid2855',
 'ZToMuMu_NNPDF30_13TeV_M_800_1400_PH-skimid2860',
 'ZToMuMu_NNPDF30_13TeV_M_1400_2300_PH-skimid2862',
 'ZToMuMu_NNPDF30_13TeV_M_2300_3500_PH-skimid2865',
 'ZToMuMu_NNPDF30_13TeV_M_3500_4500_PH-skimid2864',
 'ZToMuMu_NNPDF30_13TeV_M_4500_6000_PH-skimid3040',
 'ZToMuMu_NNPDF30_13TeV_M_6000_Inf_PH-skimid2866',
]
bglist["W"]=[
 'WJetsToLNu_13TeVMLM_MG-skimid3006',
 'WJetsToLNu_HT-100To200_13TeVMLM_MG-skimid2910',
 'WJetsToLNu_HT-200To400_13TeVMLM_MG-skimid2932',
 'WJetsToLNu_HT-400To600_13TeVMLM_MG-skimid3000',
 'WJetsToLNu_HT-600To800_13TeVMLM_MG-skimid2905',
 'WJetsToLNu_HT-800To1200_13TeVMLM_MG-skimid2834',
 'WJetsToLNu_HT-1200To2500_13TeVMLM_MG-skimid2913',
 'WJetsToLNu_HT-2500ToInf_13TeVMLM_MG-skimid2914',
]
bglist["single Top"]=[
 'ST_tW_top_5f_inclusiveDecays_13TeV-v2_PH-skimid2861',
 'ST_tW_antitop_5f_inclusiveDecays_13TeV_PH-skimid2858',
 'ST_t-channel_top_4f_leptonDecays_13TeV_PH-skimid2845',
 'ST_t-channel_antitop_4f_leptonDecays_13TeV_PH-skimid2805',
]
bglist["QCD jet"]=[
 'QCD_Pt-15to20_MuEnrichedPt5_13TeV_P8-skimid2723',
 'QCD_Pt-20to30_MuEnrichedPt5_13TeV_P8-skimid2747',
 'QCD_Pt-20to30_MuEnrichedPt5_13TeV_ext1_P8-skimid2848',
 'QCD_Pt-30to50_MuEnrichedPt5_13TeV_ext1_P8-skimid2897',
 'QCD_Pt-50to80_MuEnrichedPt5_13TeV_ext1_P8-skimid2713',
 'QCD_Pt-80to120_MuEnrichedPt5_13TeV_P8-skimid2696',
 'QCD_Pt-80to120_MuEnrichedPt5_13TeV_ext1_P8-skimid2737',
 'QCD_Pt-120to170_MuEnrichedPt5_13TeV_P8-skimid2850',
 'QCD_Pt-170to300_MuEnrichedPt5_13TeV_P8-skimid2715',
 'QCD_Pt-300to470_MuEnrichedPt5_13TeV_P8-skimid2753',
 'QCD_Pt-470to600_MuEnrichedPt5_13TeV_P8-skimid3039',
 'QCD_Pt-600to800_MuEnrichedPt5_13TeV_P8-skimid2502',
 'QCD_Pt-800to1000_MuEnrichedPt5_13TeV_P8-skimid2735',
 'QCD_Pt-1000toInf_MuEnrichedPt5_13TeV_P8-skimid2727',
]
bglist["Diboson"]=[
 'WWTo2L2Nu_13TeV_PH-skimid2859',
 'WWTo4Q_13TeV-v2_PH-skimid2871',
 'WWToLNuQQ_13TeV_PH-skimid2863',
 'WZTo3LNu_13TeV_PH-skimid3032',
 'ZZTo2L2Nu_13TeV_PH-skimid3046',
 'ZZTo4L_13TeV_PH-skimid3045',
]
bglist["TTbar"]=[
 'TT_13TeV_PH-skimid2903',
 'TT_13TeV_ext3_PH-skimid2901',
 'TT_Mtt-1000toInf_13TeV_ext1_PH-skimid2989',
 'TT_Mtt-700to1000_13TeV_ext1_PH-skimid2868',
]

# bglist["TTbar bulk"]=[
 # 'TT_13TeV_PH-skimid2903',
 # 'TT_13TeV_ext3_PH-skimid2901',
# ]
# 
# bglist["TTbar 700"]=[
 # 'TT_Mtt-700to1000_13TeV_ext1_PH-skimid2868',
# ]
# 
# bglist["TTbar 1000"]=[
 # 'TT_Mtt-1000toInf_13TeV_ext1_PH-skimid2989',
# ]

colorList={}
colorList["W"]="lightblue"
colorList["Diboson"]="y"
colorList["single Top"]="darkmagenta"
colorList["QCD jet"]="darkblue"
colorList["TTbar"]="chartreuse"
colorList["TTbar bulk"]="chartreuse"
colorList["TTbar 700"]="blue"
colorList["TTbar 1000"]="red"
colorList["WW"]="green"
colorList["DY"]="pink"
colorList['RPV M=500']="magenta"
colorList['RPV M=1000']="red"

bghists.additionalWeight = {
 'ZToEE_NNPDF30_13TeV_M_50_120_PH-skimid3044':lumisc,
 'ZToEE_NNPDF30_13TeV_M_120_200_PH-skimid3023':lumisc,
 'ZToEE_NNPDF30_13TeV_M_200_400_PH-skimid2867':lumisc,
 'ZToEE_NNPDF30_13TeV_M_400_800_PH-skimid2872':lumisc,
 'ZToEE_NNPDF30_13TeV_M_800_1400_PH-skimid3012':lumisc,
 'ZToEE_NNPDF30_13TeV_M_1400_2300_PH-skimid2854':lumisc,
 'ZToEE_NNPDF30_13TeV_M_2300_3500_PH-skimid2853':lumisc,
 'ZToEE_NNPDF30_13TeV_M_3500_4500_PH-skimid2857':lumisc,
 'ZToEE_NNPDF30_13TeV_M_4500_6000_PH-skimid2856':lumisc,
 'ZToEE_NNPDF30_13TeV_M_6000_Inf_PH-skimid2892':lumisc,
 'ZToMuMu_NNPDF30_13TeV_M_50_120_PH-skimid3048':lumisc,
 'ZToMuMu_NNPDF30_13TeV_M_120_200_PH-skimid2559':lumisc,
 'ZToMuMu_NNPDF30_13TeV_M_200_400_PH-skimid2310':lumisc,
 'ZToMuMu_NNPDF30_13TeV_M_400_800_PH-skimid2855':lumisc,
 'ZToMuMu_NNPDF30_13TeV_M_800_1400_PH-skimid2860':lumisc,
 'ZToMuMu_NNPDF30_13TeV_M_1400_2300_PH-skimid2862':lumisc,
 'ZToMuMu_NNPDF30_13TeV_M_2300_3500_PH-skimid2865':lumisc,
 'ZToMuMu_NNPDF30_13TeV_M_3500_4500_PH-skimid2864':lumisc,
 'ZToMuMu_NNPDF30_13TeV_M_4500_6000_PH-skimid3040':lumisc,
 'ZToMuMu_NNPDF30_13TeV_M_6000_Inf_PH-skimid2866':lumisc,
 'WJetsToLNu_13TeVMLM_MG-skimid3006':lumisc,
 'WJetsToLNu_HT-100To200_13TeVMLM_MG-skimid2910':lumisc,
 'WJetsToLNu_HT-200To400_13TeVMLM_MG-skimid2932':lumisc,
 'WJetsToLNu_HT-400To600_13TeVMLM_MG-skimid3000':lumisc,
 'WJetsToLNu_HT-600To800_13TeVMLM_MG-skimid2905':lumisc,
 'WJetsToLNu_HT-800To1200_13TeVMLM_MG-skimid2834':lumisc,
 'WJetsToLNu_HT-1200To2500_13TeVMLM_MG-skimid2913':lumisc,
 'WJetsToLNu_HT-2500ToInf_13TeVMLM_MG-skimid2914':lumisc,
 'ST_tW_top_5f_inclusiveDecays_13TeV-v2_PH-skimid2861':lumisc,
 'ST_tW_antitop_5f_inclusiveDecays_13TeV_PH-skimid2858':lumisc,
 'ST_t-channel_top_4f_leptonDecays_13TeV_PH-skimid2845':lumisc,
 'ST_t-channel_antitop_4f_leptonDecays_13TeV_PH-skimid2805':lumisc,
 'QCD_Pt-15to20_MuEnrichedPt5_13TeV_P8-skimid2723':lumisc,
 'QCD_Pt-20to30_MuEnrichedPt5_13TeV_P8-skimid2747':lumisc,
 'QCD_Pt-20to30_MuEnrichedPt5_13TeV_ext1_P8-skimid2848':lumisc,
 'QCD_Pt-30to50_MuEnrichedPt5_13TeV_ext1_P8-skimid2897':lumisc,
 'QCD_Pt-50to80_MuEnrichedPt5_13TeV_ext1_P8-skimid2713':lumisc,
 'QCD_Pt-80to120_MuEnrichedPt5_13TeV_P8-skimid2696':lumisc,
 'QCD_Pt-80to120_MuEnrichedPt5_13TeV_ext1_P8-skimid2737':lumisc,
 'QCD_Pt-120to170_MuEnrichedPt5_13TeV_P8-skimid2850':lumisc,
 'QCD_Pt-170to300_MuEnrichedPt5_13TeV_P8-skimid2715':lumisc,
 'QCD_Pt-300to470_MuEnrichedPt5_13TeV_P8-skimid2753':lumisc,
 'QCD_Pt-470to600_MuEnrichedPt5_13TeV_P8-skimid3039':lumisc,
 'QCD_Pt-600to800_MuEnrichedPt5_13TeV_P8-skimid2502':lumisc,
 'QCD_Pt-800to1000_MuEnrichedPt5_13TeV_P8-skimid2735':lumisc,
 'QCD_Pt-1000toInf_MuEnrichedPt5_13TeV_P8-skimid2727':lumisc,
 'WWTo2L2Nu_13TeV_PH-skimid2859':lumisc,
 'WWTo4Q_13TeV-v2_PH-skimid2871':lumisc,
 'WWToLNuQQ_13TeV_PH-skimid2863':lumisc,
 'WZTo3LNu_13TeV_PH-skimid3032':lumisc,
 'ZZTo2L2Nu_13TeV_PH-skimid3046':lumisc,
 'ZZTo4L_13TeV_PH-skimid3045':lumisc,
 'TT_13TeV_PH-skimid2903':lumisc*1.138,
 'TT_13TeV_ext3_PH-skimid2901':lumisc*1.138,
 'TT_Mtt-1000toInf_13TeV_ext1_PH-skimid2989':lumisc*1.138/3.7,
 'TT_Mtt-700to1000_13TeV_ext1_PH-skimid2868':lumisc*1.138,
}

bghists.addFileList(bglist)

dat_hist=HistStorage(xs,lumi,path="/disk1/erdweg/television/DATA_25/merged/",isData=True)
dat_hist.addFile("allData")
# dat_hist.addFile("Data_Run2015B-PromptReco_251162_252126_SingleMuon-skimid81")
# dat_hist.addFile("Data_Run2015C-PromptReco_253888_254914_SingleMuon-skimid48")
# dat_hist.addFile("../../DATA_25/merged/Data_Run2015C-PromptReco_253888_254914_SingleMuon-skimid48")

basedir="/disk1/erdweg/television/SIGNAL/merged/"
sghist=HistStorage(xs,lumi,path=basedir,xstype=None)
sglist=OrderedDict()

sglist['RPV M=500']=[
 'RPVresonantToEMu_M-500_LLE_LQD-001_13TeV_CA-skimid3002',
]
sglist['RPV M=1000']=[
 'RPVresonantToEMu_M-1000_LLE_LQD-001_13TeV_CA-skimid3022',
]
sghist.additionalWeight = {'RPVresonantToEMu_M-500_LLE_LQD-001_13TeV_CA-skimid3002':lumisc}
sghist.additionalWeight.update({'RPVresonantToEMu_M-1000_LLE_LQD-001_13TeV_CA-skimid3022':lumisc})
sghist.addFileList(sglist)
histContainer=HistStorageContainer(bg=bghists,data=dat_hist,sg=sghist)

bghists.initStyle(style="bg",colors=colorList)
sghist.initStyle(style="sg",colors=colorList)
