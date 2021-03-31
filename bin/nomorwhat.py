

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

def format_sents(s):
    endofsent = ['#', '#', '#']
    sents = []
    sent = s.strip().split(' ')
    for word in sent:
        sents.append(word.split('/'))
    sents.append(endofsent)
    sents.append(endofsent)
    return sents
