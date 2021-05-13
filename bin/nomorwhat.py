import re


def format_sents(s):
    """ Takes a string (a sentence) and returns it as a list of token/lemma/annotation.
    Also appends end of sentence characters to each sentence.
    """
    endofsent = ['#', '#', '#']
    sents = []
    sent = s.strip().split(' ')
    for word in sent:
        sents.append(word.split('/'))
    sents.append(endofsent)
    sents.append(endofsent)
    return sents


def check_macro(macro_name, anal):
    """
    
    """
    macro_res = False
    if macros['macros'][macro_name]['type'] == 'list':
        if anal[0] in macros['macros'][macro_name]['value']:
            macro_res = True
        else:
            macro_res = False
    elif macros['macros'][macro_name]['type'] == 'regex':
        if macros['macros'][macro_name]['regexp_type'] == 'search':
            macro_res = re.search(macros['macros'][macro_name]['value'], anal[2])
        else:
            pass
    elif macros['macros'][macro_name]['type'] == 'ends':
        macro_res = anal[2].endswith(macros['macros'][macro_name]['value'])
    elif macros['macros'][macro_name]['type'] == 'complex':
        if macros['macros'][macro_name]['compl_type'] == 'and': 
            all_true = True
            for macro in macros['macros'][macro_name]['sub_macros']:
                if not check_macro(macro, anal):
                    all_true = False
                    break
            macro_res = all_true
        elif macros['macros'][macro_name]['compl_type'] == 'or':
            one_true = False
            for macro in macros['macros'][macro_name]['sub_macros']:
                if check_macro(macro, anal):
                    one_true = True
                    break
            macro_res = one_true
    elif macros['macros'][macro_name]['type'] == 'neg':
        macro_res = not check_macro(macros['macros'][macro_name]['sub_macro'], anal)
            
    return macro_res


def NUM_rules(window, curr_POS):
    first_right_word, first_right_lemma, first_right_annot = window[0]
    second_right_word, second_right_lemma, second_right_annot = window[1]
    
    if re.search("FN|SZN|MN|NU", first_right_annot):  # if the next token is a nominal, or a postposition,
        # the word gets a "none"
        curr_POS = curr_POS.replace('NOM', 'semmi')
        
    elif check_macro('not_kop_v', window[0]):  # if the next token is verb, but not a copula, the word is a nominative
        curr_POS = curr_POS.replace('NOM', 'nom')
        
    elif check_macro('def_art', window[0]):  # or re.search('HA', first_right_annot): # if the next token is
        # a definite article or an adverb, the word is a nominative
        curr_POS = curr_POS.replace('NOM', 'nom')

    else:
        curr_POS = curr_POS.replace('NOM', 'defsemmi')
        if check_macro('PUNCT', window[1]) or check_macro('def_art', window[1]) or re.search('HA', second_right_annot) \
                or check_macro('V', window[1]):
            curr_POS = curr_POS.replace('defsemmi', 'semmi')
        
    return curr_POS

    
def ADJ_rules(window, curr_POS):
    first_right_word, first_right_lemma, first_right_annot = window[0]
    # print(window)
    second_right_word, second_right_lemma, second_right_annot = window[1]
    
    if check_macro('NUs', window[0]):  # if the next token is postposition(al like element), the word gets a 'none'
        curr_POS = curr_POS.replace('NOM', 'semmi')
    
    elif check_macro('not_kop_v', window[0]):  # if the next token is a verb, but not a copula, the word is a nominative
        curr_POS = curr_POS.replace('NOM', 'nom')
    
    elif check_macro('szn', window[0]):  # before a numeral: default value
        curr_POS = curr_POS.replace('NOM', 'nulla')
        
        if check_macro('PSE', window[1]):  # if the second token has a poss. suff.
            curr_POS = curr_POS.replace('nulla', 'gen')
        else:  # otherwise
            curr_POS = curr_POS.replace('nulla', 'nom')
    
    elif check_macro('full_stop', window[0]):  # if the next token is a fix outsider, this word must be the end of an NP,
        # thus 'nom'
        curr_POS = curr_POS.replace('NOM', 'nom')
    
    else:  # otherwise
        curr_POS = curr_POS.replace('NOM', 'defsemmi')
        if check_macro('full_stop', window[1]) or check_macro('V', window[1]):  # if there is a punct.mark in the window
            curr_POS = curr_POS.replace('defsemmi', 'semmi')
            
    return curr_POS


def NOUN_rules(window, curr_POS, curr_word, token):
    first_right_word, first_right_lemma, first_right_annot = window[0]
    second_right_word, second_right_lemma, second_right_annot = window[1]
    if check_macro('NUs', window[0]):  # if the next token is postposition(al like element), the word gets a 'none'
        curr_POS = curr_POS.replace('NOM', 'semmi')

    elif check_macro('not_gen', token):
        curr_POS = curr_POS.replace('NOM', 'nom')
        # print('notgen')

    elif check_macro('PSE', window[0]):
        curr_POS = curr_POS.replace('NOM', 'gen')

    elif check_macro('not_kop_v', window[0]) or check_macro('pl', window[0]):  # or first_right_annot == 'IK':
        curr_POS = curr_POS.replace('NOM', 'nom')
        # print('notkop')
    elif check_macro('TULN', window[0]):
        curr_POS = curr_POS.replace('NOM', 'nulla')

        if not check_macro('cimunevu', window[1]):
            curr_POS = curr_POS.replace('nulla', 'nom')
            # print('cimunevu')
    elif check_macro('NPMod', window[0]):
        curr_POS = curr_POS.replace('NOM', 'nulla')
        # print("hurra")
        if check_macro('PSE', window[1]) and not re.search('PSe3', curr_POS):
            curr_POS = curr_POS.replace('nulla', 'gen')
        elif check_macro('V', window[1]) or check_macro('PUNCT', window[1]) or check_macro('vonatk',
                                                                                           window[1]) or re.search(
                'PSe3', curr_POS):
            curr_POS = curr_POS.replace('nulla', 'nom')
            #  print('V')
    elif check_macro('full_stop', window[0]) or first_right_word == ':' or first_right_word == '!':
        curr_POS = curr_POS.replace('NOM', 'nom')
        #  print('fullstop')
    else:
        curr_POS = curr_POS.replace('NOM', 'nulla')

        if check_macro('V', window[1]) or check_macro('PUNCT', window[1]) or check_macro('vonatk', window[1]) or \
                re.search('PSe3', curr_POS) or second_right_word == "#":
            curr_POS = curr_POS.replace('nulla', 'nom')
            #  print('masoikV')

    return curr_POS


def nom_or_what(s, macro):
    global macros
    macros = macro
    sent = format_sents(s)
    new_sent = []  # to store a sentence with the novel tags
    to_write_later = []  # to store the NOM token and the window to create the annotation file later
    for i in range(len(sent)):

        token = sent[i]
        curr_word = token[0]
        curr_lemma = token[1]
        curr_POS = token[2]

        if curr_word != "#":  # if the given token is not the end of a sentence

            window = sent[i + 1:i + 3]

            if check_macro('NOM', token):  # if the given token is a suffixless nominal

                if check_macro('Noun_tree', token):  # if the given token is a noun, or a plural adjective, participle
                    curr_POS = NOUN_rules(window, curr_POS, curr_word, token)
                    # print(token)

                elif check_macro('Adj_tree', token):  # if the given token is a singular adjective or participle
                    curr_POS = ADJ_rules(window, curr_POS)

                elif check_macro('Num_tree', token):  # if the given token is a numeral
                    curr_POS = NUM_rules(window, curr_POS)

                new_token = curr_word + ' ' + curr_lemma + ' ' + curr_POS
                to_write_later.append((window, new_token))  # a tuple of the window of the given token and
                # the full (novel) annotation of the token

        new_sent.append(curr_word + '/' + curr_lemma + '/' + curr_POS)

    return (new_sent, to_write_later)

    # print(' '.join(new_sent))


def write_to_annot_file(new_sent, to_write, outp, i):
    """
    Function to write the sentences into a file preparing it for the manual annotation.
    
    param:
    new_sent: A sentence as a list of tokens as word/lemma/tag.
    to_write: A list containing tuples of the windows and the annotations of the suffixless nominals.
    outp: The output file.
    i: The number of the current sentence.
    """
    outp.writelines(str(i) + '. ' + ' '.join([token.split('/')[0] for token in new_sent]) + '\n')
    [outp.writelines(
        ('-' + nom.split()[0] + ' ' + window[0][0] + ' ' + window[1][0] + '\n', nom + '\n', nom + '\n', nom + '\n')) for
     (window, nom) in to_write]
    outp.writelines(('\n', '\n'))
