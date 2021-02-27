from MIP_analysis import calcPhonemeErrors, calcPhonemeErrorsFromAlignRes


def main():
    # target_ipa = 'ʌkilbʌthIkʊdnɒt'
    # pattern_phn_ipa = 'ʌkaʊntfɔɹhUkʊdnɒk'
    # a = calcPhonemeErrors(target_ipa, pattern_phn_ipa)
    # 'phn_correct, insert_count, delete_count, sub_count, total_phns, if_first_vowel_missing'

    res = [[('æ', 'ə'), ('d', '-'), ('v', 'r'), ('æ', 'æ'), ('n', 'n'), ('-', 't'), ('s', 's'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('s', 's'), ('æ', 'æ'), ('t', 'd'), ('ə', 'ə'), ('p', 'p'), ('i', 'i'), ('l', 'l')]]
    pattern_ipa_str, transcript_ipa_str = res_to_pattern_and_transcript_ipa(res)
    mip_metrics = calcPhonemeErrorsFromAlignRes(pattern_ipa_str, transcript_ipa_str, res)
    pass


def res_to_pattern_and_transcript_ipa(res):
    a = res[0]
    pattern_ipa_list = []
    transcript_ipa_list = []
    for target_ipa, participant_ipa in a:
        if target_ipa != '-':
            pattern_ipa_list.append(target_ipa)
        if participant_ipa != '-':
            transcript_ipa_list.append(participant_ipa)
    pattern_ipa_str22 = ''.join(pattern_ipa_list)
    transcript_ipa_str22 = ''.join(transcript_ipa_list)
    return pattern_ipa_str22, transcript_ipa_str22


if __name__ == "__main__":
    main()
