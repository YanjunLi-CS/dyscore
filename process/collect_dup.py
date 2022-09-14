#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os


def loadfile(name):
    data=[]
    # with open(name) as f:
    #     data=f.read().splitlines()
    fp = open(name)
    data = fp.read().splitlines()
    fp.close()
    return data

def getname(name):
    info1=name.split("/")
    info2=info1[-1].replace(".pdbqt","").replace(".mol2","").replace(".smi","").replace(".pdb","")
    return info2

if __name__ == '__main__':
    #CARE add a real name converter
    print "need real name for each compound"
#    sys.exit()
    data=[]
    result={}
    #ori data
    if sys.argv[2]=="false":    #No MF
        field_num=21
        title="TITLE,Active,Score,Stable,LogP,HB,MT,HSPC,VDW,BUMP,HM,RT,Match,Heavy,Vina,RF3,NN,DSX,DSXA,Score2,Xscore"
               #  0     1     2     3      4   5  6   7   8   9    10 11  12    13   14   15  16  17  18  19      20
    else:  #MF flag
        field_num=29
        title="TITLE,Active,Score,Stable,LogP,HB,MT,HSPC,VDW,BUMP,HM,RT,Match,Heavy,Vina,RF3,NN,DSX,DSXA,Score2,Xscore,Add_Heavy,Add_MW,Add_HA,Add_HD,Add_Charge,Add_RT,Add_Xlogp,FP2"
               #  0     1     2     3      4   5  6   7   8   9    10 11  12    13   14   15  16  17  18  19      20      21        22   23     24     25           26     27      28
    #build_dyscore
    #/ufrc/yaxia.yuan/yaxia.yuan/bear/pwwp1/ligand/bb_1028.mol2 Protein_1 Est 2.84 AEst 1.19 Score 5.18 AdjScore 5.30 AveScore 2.18 Stable 0.55 LogP 0.53 HB 0.00 MT 0.00 HSPC 1.69 VDW -135.50 BUMP 4.62 HM 2.60 RT 0.00 HM/HB 1.46 DeltaHM 1.10 Chemical -160.00 Match -4.33 Heavy    18 Weight   264 InnerVDW -3.68
    data=loadfile(sys.argv[1]+"/record/build_dyscore.score")
    count=0
    for line in data:
        if line=="":
            continue
        info=line.split()
        name=getname(info[0])
        if sys.argv[2]=="false":
            result[name]=[name,"0",info[7],info[13],info[15],info[17],info[19],info[21],info[23],info[25],info[27],info[29],info[37],info[39],"NA","NA","NA","NA","NA","NA","NA"]
        else:
            result[name]=[name,"0",info[7],info[13],info[15],info[17],info[19],info[21],info[23],info[25],info[27],info[29],info[37],info[39],"NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA"]

        count+=1
    print "DS count",count

    #vina
    data=loadfile(sys.argv[1]+"/record/vina.dat")
    count=0
    for line in data:
        if line=="":
            continue
        info=line.split()
        name=getname(info[0])
        if name in result:
            result[name][14]=info[4]
            count+=1
    print "Vina count",count

    #rf-score3  (dud)
    data=loadfile(sys.argv[1]+"/record/rf-score3.dat")
    count=0
    for line in data:
        if line=="":
            continue
        info=line.split()
        name=getname(info[0])
        if name in result:
            result[name][15]=info[1]
            count+=1
    print "RF3 count",count
    
    #NNscore
    data=loadfile(sys.argv[1]+"/record/NNscore.dat")
    count=0
    for line in data:
        if line=="":
            continue
        info=line.split()
        name=getname(info[0])
        if name in result:
            result[name][16]=info[1]
            count+=1
    print "NN count",count
    
    #DSXscore
    data=loadfile(sys.argv[1]+"/record/DSXscore.dat")
    count=0
    for line in data:
        if line=="":
            continue
        info=line.split()
        name=getname(info[0])
        if name in result:
            result[name][17]=info[1]
            result[name][18]=info[2]
            count+=1
    print "DSX count",count


    #score2
    data=loadfile(sys.argv[1]+"/record/score2.dat")
    count=0
    for line in data:
        if line=="":
            continue
        info=line.split()
        name=getname(info[0])
        if name in result:
            result[name][19]=info[1]
            count+=1
    print "score2 count",count
    
    #xscore
    data=loadfile(sys.argv[1]+"/record/xscore.dat")
    count=0
    for line in data:
        if line=="":
            continue
        info=line.split()
        name=getname(info[0])
        if name in result:
            result[name][20]=info[1]
            count+=1
    print "xscore count",count

#    title="TITLE,Active,Score,Stable,LogP,HB,MT,HSPC,VDW,BUMP,HM,RT,Match,Heavy,Vina,RF3,NN,DSX,DSXA,Score2,Xscore,Add_Heavy,Add_MW,Add_HA,Add_HD,Add_Charge,Add_RT,Add_Xlogp,FP2"
           #  0     1     2     3      4   5  6   7   8   9    10 11  12    13   14   15  16  17  18  19      20      21        22   23     24     25           26     27      28
    if sys.argv[2]!="false":
        #charge
        data=loadfile(sys.argv[1]+"/record/charge.dat")
        count=0
        for line in data:
            if line=="":
                continue
            info=line.split()
            name=getname(info[0])
            if name in result:
                result[name][25]=info[1]
                count+=1
        print "Charge count",count
        #property  nHeavyAtom nHBAcc nHBAcc2 nHBAcc3 nHBDon nRotB MW XLogP
        data=loadfile(sys.argv[1]+"/record/padel.dat")
        count=0
        for line in data:
            if line=="":
                continue
            info=line.split()
            if len(info)!=9:
                continue
            name=getname(info[0])
            if name in result:
                result[name][21]=info[1]
                result[name][22]=str(round(float(info[7]),2))
                result[name][23]=info[2]
                result[name][24]=info[5]
                result[name][26]=info[6]
                result[name][27]=str(round(float(info[8]),2))
                count+=1
        print "Properties count",count
        #FP2
        data=loadfile(sys.argv[1]+"/record/FP2.dat")
        count=0
        for line in data:
            if line=="":
                continue
            info=line.split()
            name=getname(info[0])
            if name in result:
                result[name][28]=info[1]
                count+=1
        print "FP2 count",count


    print "Output"
    count=0
    if sys.argv[2]=="false":
        fp=open(sys.argv[1]+"/record/collect.csv","w")
    else:
        fp=open(sys.argv[1]+"/record/collect_mf.csv","w")
    fp.write("%s\n" % title)
    for line in result:
        for i in xrange(field_num):
            if result[line][i]=="NA":
                break
        else:
            if result[line][0].find("inactive")>-1:
                result[line][1]="0"
            else:
                result[line][1]="1"
            str=",".join(result[line])
            fp.write("%s\n" % str)
            count+=1
    fp.close()
    print "All write count",count
    print "Done"
        
