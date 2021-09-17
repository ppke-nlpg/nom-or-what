#!/usr/bin/env python
# coding: utf-8

import re


def evaluate_nom_or_what(annotated_file):
    manu_manu = {"nom_nom":0,"nom_suff":0,"suff_nom":0,"gen_gen":0,"gen_suff":0,
                 "suff_suff":0,"suff_gen":0,"none_none":0,"defnone_defnone":0,"defnone_none":0,"none_defnone":0, "other":0}
    manu_algo = {"nom_nom":0,"nom_suff":0,"suff_nom":0,"gen_gen":0,"gen_suff":0,
                 "suff_suff":0,"suff_gen":0,"none_none":0,"defnone_defnone":0,"defnone_none":0,"none_defnone":0, "other":0}
    full_algo = {"nom_nom":0,"nom_suff":0,"suff_nom":0,"gen_gen":0,"gen_suff":0,
                 "suff_suff":0,"suff_gen":0,"none_none":0,"defnone_defnone":0,"defnone_none":0,"none_defnone":0, "other":0}
    nom_nom = 0
    nom_suff = 0 
    suff_nom = 0
    gen_gen = 0
    gen_suff = 0 
    suff_suff = 0 
    suff_gen = 0
    none_none = 0
    defnone_defnone = 0
    defnone_none = 0
    none_defnone = 0
    xne = 0
    other = 0
    postag =0
    vok = 0    
    full_nom_nom = 0
    full_nom_suff = 0 
    full_suff_nom = 0
    full_gen_gen = 0
    full_gen_suff = 0 
    full_suff_suff = 0 
    full_suff_gen = 0
    full_none_none = 0
    full_defnone_defnone = 0
    full_defnone_none = 0
    full_none_defnone = 0
    full_other = 0
    full_nom_nom_algo = 0
    full_nom_suff_algo = 0 
    full_suff_nom_algo = 0
    full_gen_gen_algo = 0
    full_gen_suff_algo = 0 
    full_suff_suff_algo = 0 
    full_suff_gen_algo = 0
    full_none_none_algo = 0
    full_defnone_defnone_algo = 0
    full_defnone_none_algo = 0
    full_none_defnone_algo = 0
    full_other_algo = 0
    postag_full_algo = 0
    xne_full_algo = 0
    vok_full_algo = 0
    inf = open(annotated_file, 'r')
    for line in inf:
        if len(line)>2:
            if re.search("^[^0-9\-]", line.strip()):
                annot_manual_full_sent_line = line
                annot_manual_full_sent = line.split()[2]
                annot_manual_window_line = inf.readline()
                annot_manual_window = annot_manual_window_line.strip().split()[2]
                annot_automatic_line = inf.readline()
                annot_automatic = annot_automatic_line.strip().split()[2]
                if annot_manual_full_sent.endswith('postag_error'):
                    postag+=1
                elif annot_manual_full_sent.endswith("xne"):
                    xne+=1
                elif annot_manual_full_sent.endswith('vok'):
                    vok+= 1
                else:
                    # full match between full sentence based annot - manual, window-based annot
                    if annot_manual_full_sent == annot_manual_window:
                        if annot_manual_full_sent.endswith("nom"):
                            manu_manu["nom_nom"]+=1
                        elif annot_manual_full_sent.endswith("gen"):
                            manu_manu["gen_gen"]+=1
                        elif annot_manual_full_sent.endswith("suff"):
                            manu_manu["suff_suff"]+=1
                        elif annot_manual_full_sent.endswith("defnone"):
                            manu_manu["defnone_defnone"]+=1
                        elif annot_manual_full_sent.endswith(".none"):
                            manu_manu["none_none"]+=1
                            
                    else:
                        # no match, not xne, not vok, not postag
                        if annot_manual_full_sent.endswith("nom") and annot_manual_window.endswith("suff"):
                            manu_manu["nom_suff"]+= 1
                        elif annot_manual_full_sent.endswith("gen") and annot_manual_window.endswith("suff"):
                            manu_manu["gen_suff"]+= 1
                        elif annot_manual_full_sent.endswith("suff") and annot_manual_window.endswith("nom"):
                            manu_manu["suff_nom"]+=1
                        elif annot_manual_full_sent.endswith("suff") and annot_manual_window.endswith("gen"):
                            manu_manu["suff_gen"]+=1
                        elif annot_manual_full_sent.endswith("defnone") and annot_manual_window.endswith(".none"):
                            manu_manu["defnone_none"]+=1
                        elif annot_manual_full_sent.endswith(".none") and annot_manual_window.endswith("defnone"):
                            manu_manu["none_defnone"]+=1
                        else:
                            manu_manu["other"]+=1
                            
                    # egyezés, teljes mondat - algo:
                    if annot_manual_full_sent == annot_automatic:
                        if annot_manual_full_sent.endswith("nom"):
                            full_algo["nom_nom"]+=1
                        elif annot_manual_full_sent.endswith("gen"):
                            full_algo["gen_gen"]+=1
                        elif annot_manual_full_sent.endswith("suff"):
                            full_algo["suff_suff"]+=1
                        elif annot_manual_full_sent.endswith("defnone"):
                            full_algo["defnone_defnone"]+=1
                        elif annot_manual_full_sent.endswith(".none"):
                            full_algo["none_none"]+=1
                    else:
                        # ha nem egyezik, nem anmk, nem vok, nem postag
                        if annot_manual_full_sent.endswith("nom") and annot_automatic.endswith("suff"):
                            full_algo["nom_suff"]+= 1
                        elif annot_manual_full_sent.endswith("gen") and annot_automatic.endswith("suff"):
                            full_algo["gen_suff"]+= 1
                        elif annot_manual_full_sent.endswith("suff") and annot_automatic.endswith("nom"):
                            full_algo["suff_nom"]+=1
                        elif annot_manual_full_sent.endswith("suff") and annot_automatic.endswith("gen"):
                            full_algo["suff_gen"]+=1
                        elif annot_manual_full_sent.endswith("defnone") and annot_automatic.endswith(".none"):
                            full_algo["defnone_none"]+=1
                        elif annot_manual_full_sent.endswith(".none") and annot_automatic.endswith("defnone"):
                            full_algo["none_defnone"]+=1
                        else:
                            full_algo["other"]+=1
                            
                    # egyezés, kézi ablak - algo:
                    if annot_manual_window == annot_automatic:
                        if annot_manual_window.endswith("nom"):
                            manu_algo["nom_nom"]+=1
                        elif annot_manual_window.endswith("gen"):
                            manu_algo["gen_gen"]+=1
                        elif annot_manual_window.endswith("suff"):
                            manu_algo["suff_suff"]+=1
                        elif annot_manual_window.endswith("defnone"):
                            manu_algo["defnone_defnone"]+=1
                        elif annot_manual_window.endswith(".none"):
                            manu_algo["none_none"]+=1
                    else:
                        # ha nem egyezik, nem anmk, nem vok, nem postag
                        if annot_manual_window.endswith("nom") and annot_automatic.endswith("suff"):
                            manu_algo["nom_suff"]+= 1
                        elif annot_manual_window.endswith("gen") and annot_automatic.endswith("suff"):
                            manu_algo["gen_suff"]+= 1
                        elif annot_manual_window.endswith("suff") and annot_automatic.endswith("nom"):
                            manu_algo["suff_nom"]+=1
                        elif annot_manual_window.endswith("suff") and annot_automatic.endswith("gen"):
                            manu_algo["suff_gen"]+=1
                        elif annot_manual_window.endswith("defnone") and annot_automatic.endswith(".none"):
                            manu_algo["defnone_none"]+=1
                        elif annot_manual_window.endswith(".none") and annot_automatic.endswith("defnone"):
                            manu_algo["none_defnone"]+=1
                        else:
                            manu_algo["other"]+=1
                            
    print("xne = " + str(xne))
    print("postag = " + str(postag))
    print("vok = "+ str(vok))
    print()
    print("Kézi-kézi eredmények:")
    print()
    for key in manu_manu:
        print(key,manu_manu[key])
    print()
    print()
    print("Kézi - algoritmus:")
    print()
    for key in manu_algo:
        print(key,manu_algo[key])
    print()
    print()
    print("Teljes mondat - algoritmus:")
    print()
    for key in full_algo:
        print(key,full_algo[key])
    print()


evaluate_nom_or_what("annotated_1000.txt")

