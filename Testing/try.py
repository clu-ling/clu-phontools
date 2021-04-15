
import csv
import re
from generate_phrase_pattern import *


# call Phrase object
dictionary = phrase()
arpabet_to_ipa = dictionary.arpabet_to_ipa()

# [1] read the file
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
            #print (row)
       	    spkList.append(row[0])
       	    targetList.append(row[1])
       	    transcriptsList.append(','.join(row[3:]))
    return spkList, targetList, transcriptsList

# [2]
class speaker(object):
    def __init__(self, spkID, targets, transcripts):
        self.spkID = spkID
        self.targets = targets
        self.transcripts = transcripts
        self.analysisResult = None

def createSpk(spkList, targetList, transcriptList):
    preID = 'nobody'
    speakers = []
    for i in range(len(spkList)):
        transcriptALL = re.split(r',', transcriptList[i])
        curID = spkList[i]
        if curID != preID:
            if preID != "nobody":
                speakers.append(speaker(preID, targets, transcripts))
            transcripts = transcriptALL
            targets = [targetList[i]]*len(transcriptALL)
        else:
            transcripts += transcriptALL
            targets += [targetList[i]]*len(transcriptALL)
        preID = curID
    speakers.append(speaker(preID, targets, transcripts))
    return speakers

# [3]
def preProcessTranscript(transcript):
    transcript = transcript.lower()
    transcript = transcript.strip()
    transcript = re.sub('[.?!@#$]', '', transcript)
    return transcript

# [4]
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
        temp = re.split(r'\s+', word)
        for phn in temp:
            pattern_phn_ipa.append(arpabet_to_ipa[phn])



if __name__ == "__main__":
    # [1]
    spkList, targetList, transcriptList = readCSV(
        'filtered_transcriptions_clear_batch1-20.csv')
    # [2]
    speakers = createSpk(spkList, targetList, transcriptList)
    #print (speakers)
    for spk in speakers:
        targets = []
        #print (targets)
        transcripts = []
        #print(transcripts)
        target_phnList = []
        target_phnIpaList = []
        target_stressList = []
        transcript_phnList = []
        transcript_phnIpaList = []
        transcript_stressList = []
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
            # [3]
            transcript = preProcessTranscript(spk.transcripts[i])
            #print (transcript)
            if transcript == "":
                continue
            else:
                targets.append(spk.targets[i])
                transcripts.append(transcript)
                # [4]
                pattern_words, pattern_phn, pattern_phn_ipa, pattern_stress = processPattern(
                    spk.targets[i])
    #             #target_phnList.append(' '.join(pattern_phn))
    #             #target_phnIpaList.append(pattern_phn_ipa)
    #             #target_stressList.append(' '.join(pattern_stress))

    #             transcript_phn, transcript_phn_ipa, transcript_stress = processTranscript(
    #                 transcript)
    #             #transcript_phnList.append(' '.join(transcript_phn))
    #             #transcript_phnIpaList.append(transcript_phn_ipa)
    #             #print transcript_stress
    #             #if transcript_stress is not None:
    #             #    transcript_stressList.append(' '.join(transcript_stress))
    #             #else:
    #             #    transcript_stressList.append(None)

    #             _wrd_acc = calcWordCorrectness(pattern_words, transcript)
    #             wrd_acc.append(_wrd_acc)

    #             #print pattern_words
    #             #print transcript
    #             if _wrd_acc is None or '-' in transcript_phn:
    #                 phn_acc.append(None)
    #                 phn_ins.append(None)
    #                 phn_del.append(None)
    #                 phn_sub.append(None)
    #                 total_phns.append(None)
    #                 IS.append(None)
    #                 IW.append(None)
    #                 DS.append(None)
    #                 DW.append(None)
    #             else:
    #                 _phn_acc, _phn_ins, _phn_del, _phn_sub, _total_phns, if_first_vowel_missing = calcPhonemeErrors(
    #                     pattern_phn_ipa, transcript_phn_ipa)
    #                 phn_acc.append(_phn_acc)
    #                 phn_ins.append(_phn_ins)
    #                 phn_del.append(_phn_del)
    #                 phn_sub.append(_phn_sub)
    #                 total_phns.append(_total_phns)
    #                 #print pattern_stress
    #                 #print transcript_stress
    #                 #print i
    #                 #print spk.spkID
    #                 if if_first_vowel_missing == 1 and pattern_stress[0][0] == '0' and len(''.join(transcript_stress)) == 5:
    #                     transcript_stress = ['1'] + transcript_stress
    #                 print(pattern_words)
    #                 _IS, _IW, _DS, _DW = calcLBE(
    #                     pattern_stress, transcript_stress)
    #                 IS.append(_IS)
    #                 IW.append(_IW)
    #                 DS.append(_DS)
    #                 DW.append(_DW)
    #                 if _IS is not None:
    #                     if pattern_stress[0][0] == '0':
    #                         WS_count += 1
    #                     if pattern_stress[0][0] == '1':
    #                         SW_count += 1
    #     spk.analysisResult = (wrd_acc, phn_acc, phn_ins, phn_del,
    #                           phn_sub, total_phns, IS, IW, DS, DW, SW_count, WS_count)

    #     with open(spk.spkID + '.csv', 'w') as outF:
    #         outF.write(','.join(['target', 'transcript', 'word_acc', 'phn_correct',
    #                              'phn_ins', 'phn_del', 'phn_sub', 'total_phns', 'IS', 'IW', 'DS', 'DW']))
    #         outF.write('\n')
    #         for ind in range(len(wrd_acc)):
    #             outF.write(','.join(
    #                 [targets[ind], transcripts[ind],

    #                  str(wrd_acc[ind]), str(phn_acc[ind]), str(
    #                      phn_ins[ind]), str(phn_del[ind]), str(phn_sub[ind]),
    #                  str(total_phns[ind]), str(IS[ind]), str(IW[ind]), str(DS[ind]), str(DW[ind])]))
    #             outF.write('\n')
    
