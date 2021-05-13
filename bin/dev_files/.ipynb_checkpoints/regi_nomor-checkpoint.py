# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    author: ligetinagy
    last update: 2017.11.12.

    nom-or-what
"""
import re
from itertools import zip_longest

# unused now:
kopulativusz_name = 'kop'
nom_or_kop_name = 'nomorkop'

input_file_name = 'small_test.txt'
output_file_name = 'small_eval.txt'

# MACROS:


def macro_NPMod(POStag):
    """
    defines if a token is an macro_NPMod or not
    :param POStag: list of token, lemma, annotation.with.dots
    :return: true if it is an macro_NPMod, false otherwise
    """
    return re.search('MN|SZN|MIB|MIF|MIA', POStag)


# still incomplete:
nu_mn_list = {'alatti', 'általi', 'elleni', 'előli', 'előtti', 'felőli', 'fölötti', 'helyetti', 'iránti', 'képesti',
              'körüli', 'közötti', 'melletti', 'mellőli', 'miatti', 'mögötti', 'nélküli', 'szerinti', 'végetti',
              'utáni', 'közti'}


def macro_nu_mosaic(first_right_token, first_right_annot):
    return first_right_token in nu_mn_list or first_right_token in {'című', 'nevű'} or first_right_annot == 'NU'


def macro_clause_starter(curr_POStag, window_1_token, window_1_anal):
    # connectives
    return 'IGE' in window_1_anal or window_1_token in {'ami', 'aki', 'hogy', 'de', '!', '?', '.'} \
           or 'PSe3' in curr_POStag


def macro_a_az_det(first_right_token, first_right_annot):
    return first_right_token in {'a', 'az'} and first_right_annot == 'DET'


def macro_conjunctionwords(first_right_token, first_right_annot):
    # particles and friends
    return first_right_token in {'is', 'sem', 'nem', 'pedig', '!', '?', '.'} or 'NM' in first_right_annot


def macro_ige_not_van(first_right_lemma, first_right_annot):
    # [IGE][_MIB]
    return 'IGE' in first_right_annot and 'van' != first_right_lemma and '_' not in first_right_annot


def readtext(inp_fname):
    """
    read input file of test sentences
    sentence / line
    appends end-of-sentence characters

    :return: list of sentences
    """

    endofsent = ['#', '#', '#']
    sents = []
    with open(inp_fname, encoding='UTF-8') as infile:
        for line in infile:
            sentencelist = []
            sent = line.strip().split(' ')
            for word in sent:
                sentencelist.append(word.split('/'))
            sentencelist.append(endofsent)  # XXX This is the same list as one line below
            sentencelist.append(endofsent)
            sents.append(sentencelist)

    return sents


# https://stackoverflow.com/a/7946411
def grouper(n, iterable, fillvalue=None):
    # "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def write_out_anal(anal, j, sent, o_file):
    o_file.writelines(('-' + sent[j] + ' ' + sent[j + 1] + ' ' + sent[j + 2] + '\n',
                       ' '.join(anal) + '\n',
                       ' '.join(anal) + '\n',
                       ' '.join(anal) + '\n'))


def nyomorwhat(sents, out_fileh):
    """
    simulates nyom-or-what searcher

    :param out_fileh:
    :param sents: list of test sentences
    :return: None
    """
    for n, sentence in enumerate(sents):
        sent = [token_w_anal[0] for token_w_anal in sentence]
        out_fileh.write('\n \n{0}: {1}\n'.format(n, ' '.join(sent)))

        for j, (_, _, curr_POStag) in enumerate(sentence):
            if curr_POStag == '#':
                break
            window = sentence[j + 1:j + 3]
            # pool = sentence[MN.NOM0:j]
            # maradek = sentence[j + 1:len(sentence) - 2]
            first_right_token, first_right_lemma, first_right_annot = window[0]
            # here come the rules
            rules(sent, j, window, curr_POStag, first_right_token, first_right_lemma, first_right_annot, out_fileh)
    return


def rules(sent, j, window, curr_POStag, first_right_token, first_right_lemma, first_right_annot, outfile):
    if curr_POStag.endswith('NOM'):
        # MN + PL == FN + PL
        if re.search('FN|DET_NM', curr_POStag) or (macro_NPMod(curr_POStag) and 'PL' in curr_POStag) or \
                'TULN' == curr_POStag:
            # if it is a noun; noun rules here; plural NPMods as well
            if macro_nu_mosaic(first_right_token, first_right_annot):
                # before postpositions, alatti-feletti and című-nevű: semmi
                curr_POStag = curr_POStag.replace('NOM', 'semmi')
            # Words can never be gen
            elif curr_POStag[0].title() in {'Mindez', 'Az', 'Ez', 'Ami', 'Aki'}:
                print(curr_POStag)
                curr_POStag = curr_POStag.replace('NOM', 'nom')
            elif 'PSe' in first_right_annot:
                curr_POStag = curr_POStag.replace('NOM', 'gen')

            elif macro_ige_not_van(first_right_lemma, first_right_annot) or \
                    first_right_annot == 'IK' or first_right_token == 'TULN' or 'PL' in first_right_annot:
                # before verbs, verbal particles, proper names and pronouns: nom;
                curr_POStag = curr_POStag.replace('NOM', 'nom')

            elif macro_NPMod(window[0][2]):
                # before macro_NPMod: nom or gen
                curr_POStag = curr_POStag.replace('NOM', 'nulla')
                # check the next token
                if 'PS' in window[1][2] and 'PSe3' not in curr_POStag:
                    curr_POStag = curr_POStag.replace('nulla', 'gen')
                elif macro_clause_starter(curr_POStag, window[1][0], window[1][2]):
                    # check the second in the window
                    curr_POStag = curr_POStag.replace('nulla', 'nom')

            elif macro_a_az_det(first_right_token, first_right_annot) or \
                    macro_conjunctionwords(first_right_token, first_right_annot):
                # before article, is, sem, dot or comma: nomorkop
                # this is a cheat: now only NOM
                curr_POStag = curr_POStag.replace('NOM', 'nom')

            else:
                # otherwise default, 'question mark in the table'
                curr_POStag = curr_POStag.replace('NOM', 'nulla')
                if macro_clause_starter(curr_POStag, window[1][0], window[1][2]):
                    # check the second in the window
                    curr_POStag = curr_POStag.replace('nulla', 'nom')

            write_out_anal(curr_POStag, j, sent, outfile)
        elif re.search('MN|MIB|MIF|MIA|OKEP', curr_POStag):
            # if it is an adjective; adj rules here
            print(curr_POStag)
            if macro_nu_mosaic(first_right_token, first_right_annot):
                # before postpositions, alatti-feletti and című-nevű: semmi
                curr_POStag = curr_POStag.replace('NOM', 'semmi')

            elif macro_ige_not_van(first_right_lemma, first_right_annot):
                # if the next one is a verb: nom
                curr_POStag = curr_POStag.replace('NOM', 'nom')

            elif 'SZN' in first_right_annot:
                # before a num: nom or gen
                curr_POStag = curr_POStag.replace('NOM', 'nulla')
                if 'PSe' in window[1][2]:
                    curr_POStag = curr_POStag.replace('nulla', 'gen')
                else:
                    curr_POStag = curr_POStag.replace('nulla', 'nom')

            elif macro_a_az_det(first_right_token, first_right_annot) or \
                    macro_conjunctionwords(first_right_token, first_right_annot):
                # before article, is, sem, dot or comma: nomorkop
                # this is a cheat: now only NOM
                curr_POStag = curr_POStag.replace('NOM', 'nom')

            else:
                # otherwise default
                curr_POStag = curr_POStag.replace('NOM', 'defsemmi')
                if 'SPUNCT' in window[1][2]:
                    curr_POStag = curr_POStag.replace('defsemmi', 'semmi')

            write_out_anal(curr_POStag, j, sent, outfile)
        elif 'SZN' in curr_POStag:
            # if it is a numeral; num rules here

            if re.search('FN|SZN|MN|NU', first_right_annot):
                curr_POStag = curr_POStag.replace('NOM', 'semmi')

            elif macro_ige_not_van(first_right_lemma, first_right_annot) or \
                    macro_a_az_det(first_right_token, first_right_annot) or \
                    'HA' in first_right_annot:
                # cheating
                curr_POStag = curr_POStag.replace('NOM', 'nom')
            else:
                # default
                curr_POStag = curr_POStag.replace('NOM', 'defsemmi')

            write_out_anal(curr_POStag, j, sent, outfile)
        else:
            outfile.write('---valamire nem gondoltál!\n---{0}\n'.format(' '.join(curr_POStag)))


if __name__ == '__main__':
    sentlist = readtext(input_file_name)
    with open(output_file_name, 'w') as out_file:
        nyomorwhat(sentlist, out_file)

