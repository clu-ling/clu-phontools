# -*- coding: utf-8 -*-
import csv
from generate_phrase_pattern import *
import re
import numpy as np
from aline_modified_by_yj import *

# OUTPUT: ['ai','aʊ','tʃ','ei','dʒ','oʊ','ɔi']
dipthong_list = []
dipthong_list_0 = ['ai','aʊ','tʃ','ei','dʒ','oʊ','ɔi']
for each in dipthong_list_0:
    dipthong_list.append(str(each))

# all vowels as one string: OUTPUT: 'iyeEøɛœæaAɨʉəuUoOɔɒIʌʊ'
vowel_list = ['i','y','e','E','ø','ɛ','œ','æ','a','A','ɨ','ʉ','ə','u','U','o','O','ɔ','ɒ','I','ʌ','ʊ']
vowel_list = str(''.join(vowel_list))

# call Phrase object
dictionary = phrase()
arpabet_to_ipa = dictionary.arpabet_to_ipa()


def wer(r, h):
    """
    Calculation of WER with Levenshtein distance.

    Works only for iterables up to 254 elements (uint8).
    O(nm) time ans space complexity.

    Parameters
    ----------
    r : list
    h : list

    Returns
    -------
    int

    Examples
    --------
    >>> wer("who is there".split(), "is there".split())
    1
    >>> wer("who is there".split(), "".split())
    3
    >>> wer("".split(), "who is there".split())
    3
    """
    # initialisation
    import numpy
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8)
    d = d.reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        for j in range(len(h)+1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    # computation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitution = d[i-1][j-1] + 1
                insertion    = d[i][j-1] + 1
                deletion     = d[i-1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    return d[len(r)][len(h)]
    


def readCSV(filename):
    '''
    return a list of speakers, target list and transcript list
    '''
    spkList = []
    targetList = []
    transcriptsList = []
    with open(filename, 'r') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(csvReader, None)
        for row in csvReader:
        	print(row)
        	spkList.append(row[0])
        	targetList.append(row[1])
        	transcriptsList.append(','.join(row[3:]))
    return spkList, targetList, transcriptsList



class speaker(object):
    def __init__(self,spkID,targets,transcripts):
        self.spkID = spkID
        self.targets = targets
        self.transcripts = transcripts
        self.analysisResult = None


def createSpk(spkList,targetList,transcriptList):
    preID = 'nobody'
    speakers = []
    for i in range(len(spkList)):
        transcriptALL = re.split(r',', transcriptList[i])
        curID = spkList[i]
        if curID != preID:
            if preID != "nobody":
                speakers.append(speaker(preID,targets,transcripts))
            transcripts = transcriptALL
            targets = [targetList[i]]*len(transcriptALL)
        else:
            transcripts += transcriptALL
            targets+=[targetList[i]]*len(transcriptALL)
        preID = curID
    speakers.append(speaker(preID, targets, transcripts))
    return speakers


def processPattern(pattern):
    pattern = pattern.lower()
    phrase_test = dictionary.phrase_test.tolist()
    phrase_index = phrase_test.index(pattern)
    pattern_phn = dictionary.phrase_phn[phrase_index]
    pattern_stress = dictionary.phrase_stress[phrase_index]
    pattern_words = phrase_test[phrase_index][0]
    pattern_phn_ipa = []
    for word in pattern_phn:
        word = re.sub('[0-9]+', '', word)
        temp = re.split(r'\s+',word)
        for phn in temp:
            pattern_phn_ipa.append(arpabet_to_ipa[phn])

    pattern_phn_ipa = ''.join(pattern_phn_ipa)
    pattern_phn_ipa = str(pattern_phn_ipa)
    return pattern_words, pattern_phn, pattern_phn_ipa, pattern_stress

def preProcessTranscript(transcript):
    transcript = transcript.lower()
    transcript = transcript.strip()
    transcript = re.sub('[.?!@#$]', '', transcript)
    return transcript

def processTranscript(transcript):
    transcript_phn,transcript_stress = dictionary.string_to_arpabet(transcript)
    if '-' in transcript_phn:
        return transcript_phn,None,None
    transcript_phn_ipa = []
    for word in transcript_phn:
        word = re.sub('[0-9]+', '', word)
        temp = re.split(r'\s+', word)
        for phn in temp:
            transcript_phn_ipa.append(arpabet_to_ipa[phn])

    transcript_phn_ipa = ''.join(transcript_phn_ipa)
    transcript_phn_ipa = str(transcript_phn_ipa)
    return transcript_phn,transcript_phn_ipa, transcript_stress

def calcWordCorrectness(pattern_words,transcript):
    pattern_words_list = re.split(r'\s+',pattern_words)
    transcript_words_list = re.split(r'\s+',transcript)
    total_words = len(pattern_words_list)
    count = 0
    if len(transcript_words_list) - total_words > 3:
        return None
    for word in transcript_words_list:
        if word in pattern_words_list:
            count = count + 1
    if float(count)/float(total_words) > 1:
        return None
    else:
        return float(count)/float(total_words)

    #d = wer(pattern_words_list,transcript_words_list)
    #return float(d)/len(pattern_words_list)



def calcPhonemeErrors(pattern_phn_ipa,transcript_phn_ipa):
# Calculate phoneme correctness
    align_res = align(pattern_phn_ipa, transcript_phn_ipa)
    #print pattern_phn_ipa
    #print transcript_phn_ipa
    align_target = []
    align_trans = []
    for prt in align_res[0]:
        align_target.append(prt[0])
    for prt in align_res[0]:
        align_trans.append(prt[1])

    total_phns = len(pattern_phn_ipa)
    count = 0
    for item in align_res[0]:
        phn_1 = item[0]
        phn_2 = item[1]
        if phn_1 == phn_2:
            count += 1
    phn_correct  = count
# Calculate phoneme insertion
    insert_count = 0
    for item in align_res[0]:
        phn_1 = item[0]
        phn_2 = item[1]
        if phn_1 == '-':
            insert_count += 1


    # Calculate phoneme deletion
    delete_count = 0
    align_phn_pattern = []
    for item in align_res[0]:
        phn_1 = item[0]
        if phn_1 != '-':
            align_phn_pattern.append(phn_1)
        phn_2 = item[1]
        if phn_2 == '-':
            delete_count += 1
    delete_count += total_phns-len(align_phn_pattern)

    # Determine if first vowel is deleted
    if_first_vowel_missing = 0
    for ind,phn in enumerate(pattern_phn_ipa):
        if phn in vowel_list:
            first_vowel_loc = ind
            first_vowel = phn
            break
    if first_vowel_loc == 0 and first_vowel not in align_res[0][0][0]:
        if_first_vowel_missing = 1
    else:
        for item in align_res[0]:
            phn_1 = item[0]
            if first_vowel in phn_1:
                if item[1] == '-':
                    if_first_vowel_missing = 1
                break


    # Calculate phoneme substitution
    sub_count = 0
    track_align = []
    for item in align_res[0]:
        phn_1 = item[0]
        phn_2 = item[1]
        if phn_1 == phn_2:
           track_align.append(0)
        elif phn_2 == '-':
           track_align.append(-1)
        elif phn_1 == '-':
           track_align.append(1)
        elif phn_1 != phn_2:
            sub_count += 1
    return phn_correct, insert_count,delete_count,sub_count,total_phns,if_first_vowel_missing



def calcLBE(pattern_stress,transcript_stress):
# Calculate LBE
    if len(''.join(transcript_stress))>=7 or len(''.join(transcript_stress))<=5:
        return None,None,None,None
    if len(''.join(transcript_stress)) == 6:
        LBE_IS_count = 0
        LBE_IW_count = 0
        LBE_DS_count = 0
        LBE_DW_count = 0

        loc_pattern_stress = []
        for ind_stress in range(len(pattern_stress)):
            if ind_stress == 0:
                loc_pattern_stress.append(len(pattern_stress[ind_stress]))
            else:
                loc_pattern_stress.append(len(pattern_stress[ind_stress]) + loc_pattern_stress[-1])

        loc_transcript_stress = []
        for ind_stress in range(len(transcript_stress)):
            if ind_stress == 0:
                loc_transcript_stress.append(len(transcript_stress[ind_stress]))
            else:
                loc_transcript_stress.append(len(transcript_stress[ind_stress]) + loc_transcript_stress[-1])

        concat_pattern_stress = ''.join(pattern_stress)
        print(transcript_stress)
        print(pattern_stress)
        for stress in loc_transcript_stress:
            if stress not in loc_pattern_stress:
            	print(concat_pattern_stress)
            	print(stress)
            	if concat_pattern_stress[stress]=='1':
            		LBE_IS_count += 1
            	elif concat_pattern_stress[stress]=='0':
                	LBE_IW_count += 1
        for stress in loc_pattern_stress:
            if stress not in loc_transcript_stress:
                if concat_pattern_stress[stress] == '1':
                    LBE_DS_count += 1
                elif concat_pattern_stress[stress] == '0':
                    LBE_DW_count += 1
        LBE_IS=float(LBE_IS_count)
        LBE_IW=float(LBE_IW_count)
        LBE_DS=float(LBE_DS_count)
        LBE_DW=float(LBE_DW_count)
    return LBE_IS,LBE_IW,LBE_DS,LBE_DW



if __name__ == "__main__":
    #transcript_phn, transcript_phn_ipa, transcript_stress = processTranscript("amend astate approach")
    spkList,targetList,transcriptList = readCSV('filtered_transcriptions_clear_batch1-20.csv')
    speakers=createSpk(spkList,targetList,transcriptList)
    for spk in speakers:
        targets = []
        transcripts = []
        target_phnList=[]
        target_phnIpaList=[]
        target_stressList=[]
        transcript_phnList=[]
        transcript_phnIpaList=[]
        transcript_stressList=[]
        wrd_acc = []
        phn_acc = []
        phn_ins = []
        phn_del = []
        phn_sub = []
        total_phns = []
        IS = []
        IW = []
        DS = []
        DW = []
        SW_count = 0
        WS_count = 0
        for i in range(len(spk.targets)):
            #print len(spk.targets)
            #print len(spk.transcripts)
            transcript = preProcessTranscript(spk.transcripts[i])
            if transcript == "":
                continue
            else:
                targets.append(spk.targets[i])
                transcripts.append(transcript)
                pattern_words, pattern_phn, pattern_phn_ipa, pattern_stress = processPattern(spk.targets[i])
                #target_phnList.append(' '.join(pattern_phn))
                #target_phnIpaList.append(pattern_phn_ipa)
                #target_stressList.append(' '.join(pattern_stress))


                transcript_phn, transcript_phn_ipa, transcript_stress = processTranscript(transcript)
                #transcript_phnList.append(' '.join(transcript_phn))
                #transcript_phnIpaList.append(transcript_phn_ipa)
                #print transcript_stress
                #if transcript_stress is not None:
                #    transcript_stressList.append(' '.join(transcript_stress))
                #else:
                #    transcript_stressList.append(None)


                _wrd_acc = calcWordCorrectness(pattern_words,transcript)
                wrd_acc.append(_wrd_acc)

                #print pattern_words
                #print transcript
                if _wrd_acc is None or '-' in transcript_phn:
                    phn_acc.append(None)
                    phn_ins.append(None)
                    phn_del.append(None)
                    phn_sub.append(None)
                    total_phns.append(None)
                    IS.append(None)
                    IW.append(None)
                    DS.append(None)
                    DW.append(None)
                else:
                    _phn_acc,_phn_ins,_phn_del,_phn_sub,_total_phns,if_first_vowel_missing = calcPhonemeErrors(pattern_phn_ipa,transcript_phn_ipa)
                    phn_acc.append(_phn_acc)
                    phn_ins.append(_phn_ins)
                    phn_del.append(_phn_del)
                    phn_sub.append(_phn_sub)
                    total_phns.append(_total_phns)
                    #print pattern_stress
                    #print transcript_stress
                    #print i
                    #print spk.spkID
                    if if_first_vowel_missing == 1 and pattern_stress[0][0]=='0' and len(''.join(transcript_stress))==5:
                        transcript_stress = ['1']+ transcript_stress
                    print(pattern_words)
                    _IS,_IW,_DS,_DW = calcLBE(pattern_stress,transcript_stress)
                    IS.append(_IS)
                    IW.append(_IW)
                    DS.append(_DS)
                    DW.append(_DW)
                    if _IS is not None:
                        if pattern_stress[0][0]=='0':
                            WS_count += 1
                        if pattern_stress[0][0]=='1':
                            SW_count += 1
        spk.analysisResult = (wrd_acc,phn_acc,phn_ins,phn_del,phn_sub,total_phns,IS,IW,DS,DW,SW_count,WS_count)

        with open(spk.spkID + '.csv', 'w') as outF:
            outF.write(','.join(['target','transcript','word_acc','phn_correct','phn_ins','phn_del','phn_sub','total_phns','IS','IW','DS','DW']))
            outF.write('\n')
            for ind in range(len(wrd_acc)):
                outF.write(','.join(
                    [targets[ind], transcripts[ind],
                     
                     str(wrd_acc[ind]), str(phn_acc[ind]), str(phn_ins[ind]),str(phn_del[ind]), str(phn_sub[ind]),
                     str(total_phns[ind]),str(IS[ind]), str(IW[ind]), str(DS[ind]), str(DW[ind])]))
                outF.write('\n')




 pairs = [
    (['01', '1', '10', '1'], ['010', '10', '1']), # address her meeting time -> adjusted reading time
    (['01', '1', '1', '01'], ['01', '1', '1', '0', '1']), # advance but sat appeal -> advance but sat a pail
    (['10', '1', '1', '10'], ['1', '1', '1', '1', '10']),  # bolder ground from justice -> both are grown from justice
    (['01', '01', '01'], ['0', '10', '1', '01']), # divide across retreat -> the body cross returned
  ]


target: ['01', '1', '10', '1']
transcript: ['010', '10', '1']
errors: [
    {
        "error_type": "DW", # deletion before week
        "target_idx": 0,
        "transcript_idx": 0
    }
]

target: ['01', '1', '1', '01']
transcript: ['01', '1', '1', '0', '1']
errors: [
    {
        "error_type": "IS", # Insertion before strong
        "target_idx": 0,
        "transcript_idx": 0
    }
]

target: ['10', '1', '1', '10']
transcript: ['1', '1', '1', '1', '10']
errors: [
    {
        "error_type": "IW", # Insertion before weak
        "target_idx": 0,
        "transcript_idx": 0
    }
]

target: ['01', '01', '01']
transcript: ['0', '10', '1', '01']
errors: [
    {
        "error_type": "IW" + "DS" , # Insertion before weak and deletion before strong
        "target_idx": 0,
        "transcript_idx": 0
    }
]
