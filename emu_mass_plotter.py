#!/bin/env python

from plot_inputs import *

def main():

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

    for hist in hists:
        print("Now plotting: " + hist)
        histContainer.getHist(hist)

        binf=getDictValue(hist,binning)
        if binf is not None:
            dat_hist.rebin(width=1,vector=binf)
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
        test.Add_data(dat_hist.getHistList()[0])

        #test.Add_plot('Diff',pos=1, height=15)
        # plt.xkcd()
        hist_style.Set_error_bands_fcol(['gray','orange'])
        hist_style.Set_error_bands_ecol(['black','black'])
        hist_style.Set_error_bands_labl(['Systematics','Statistic'])
        # hist_style.Set_xerr()

        # test.Add_plot('Ratio',pos=2, height=15)
        if hist == 'emu/Stage_0/h1_0_emu_Mass':
            sys_file=File('syst/for_plotting.root', "read")
        
            test.Add_error_hist([sys_file.Get('Sys'),sys_file.Get('MC statistic')], band_center = 'ref', stacking = 'Nosum')
            # test.Add_error_hist([sys_file.Get('MC statistic')], band_center = 'ref', stacking = 'Nosum')

        test.Add_plot('Diff',pos=0, height=12)

        test.Add_plot('DiffRatio',pos=1, height=12)
        test.Add_plot('Signi',pos=2, height=12)
# 
        # mxrange=getDictValue(hist,xranges)
        if hist in xranges.keys():
            test.Set_axis(logx=True,logy=True,xmin=xranges[hist][0],xmax=xranges[hist][1],ymin=1e-6,ymax=1e3)
            #test.Set_axis(logx=False,logy=True,xmin=0,xmax=500,ymin=1e-6,ymax=1e3)

        name=hist.replace("/","")

        test.create_plot()

        test.Get_axis0().set_ylim(ymin = -1.2, ymax = 2.2)
        test.Get_axis2().set_ylim(ymin = -2, ymax = 13)
        test.Get_axis3().set_ylim(ymin = -2, ymax = 2.0)

        test.SavePlot('plots/%s.pdf'%(name))
    return 42



main()
