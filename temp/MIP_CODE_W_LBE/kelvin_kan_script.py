from MIP_analysis import calcPhonemeErrors, calcPhonemeErrorsFromAlignRes, processPattern, processTranscript, calcLBE, \
    calcWordCorrectness
import pandas as pd
import numpy as np


def main():
    # target_ipa = 'ʌkilbʌthIkʊdnɒt'
    # pattern_phn_ipa = 'ʌkaʊntfɔɹhUkʊdnɒk'
    # a = calcPhonemeErrors(target_ipa, pattern_phn_ipa)
    # 'phn_correct, insert_count, delete_count, sub_count, total_phns, if_first_vowel_missing'

    res = [[('æ', 'ə'), ('d', '-'), ('v', 'r'), ('æ', 'æ'), ('n', 'n'), ('-', 't'), ('s', 's'), ('b', 'b'), ('ʌ', 'ʌ'), ('t', 't'), ('s', 's'), ('æ', 'æ'), ('t', 'd'), ('ə', 'ə'), ('p', 'p'), ('i', 'i'), ('l', 'l')]]
    pattern_ipa_str, transcript_ipa_str = res_to_pattern_and_transcript_ipa(res)
    mip_metrics = calcPhonemeErrorsFromAlignRes(pattern_ipa_str, transcript_ipa_str, res)
    pass


def calcPhonemeErrorsFromAlignRes2(res):
    pattern_ipa_str, transcript_ipa_str = res_to_pattern_and_transcript_ipa([res])
    mip_metrics = calcPhonemeErrorsFromAlignRes(pattern_ipa_str, transcript_ipa_str, [res])
    return mip_metrics


def res_to_pattern_and_transcript_ipa(res):
    a = res[0]
    ###################
    pattern_ipa_list = []
    transcript_ipa_list = []
    for target_ipa, participant_ipa in a:
        if target_ipa != '-':
            pattern_ipa_list.append(target_ipa)
        if participant_ipa != '-':
            transcript_ipa_list.append(participant_ipa)
    ###################
    # above can be replaced with the below
    # pattern_ipa_list = [target_ipa for target_ipa, _ in a if target_ipa != '-']
    # transcript_ipa_list = [participant_ipa for _, participant_ipa in a if participant_ipa != '-']

    pattern_ipa_str22 = ''.join(pattern_ipa_list)
    transcript_ipa_str22 = ''.join(transcript_ipa_list)
    return pattern_ipa_str22, transcript_ipa_str22


def convert_index_to_group(index):
    return int(np.floor(index / 8))


def gen_mip_metrics_csv():
    xl = pd.ExcelFile(r'C:\Users\Kelvin\Desktop\MIP_MA_LBE\MIP_CODE_W_LBE\SampleSet_PD_ATX_KT.xlsx')

    pd_df = xl.parse('Disagree- PD')
    pd_df = pd_df.reset_index()
    pd_df['group'] = pd_df['index'].apply(convert_index_to_group)
    transcript_df = pd_df.iloc[0::8]
    transcript_index = range(0, len(pd_df), 8)
    pd_df = pd_df.drop(index=transcript_index)

    pd_df_pivoted = pd_df.pivot(columns='Target', values='Transcript', index='group').reset_index()
    pd_df_pivoted2 = pd_df_pivoted.merge(transcript_df, on='group')
    pd_df_pivoted2.rename(columns={np.nan: 'participant ipa'})
    pd_df_pivoted2[['phn_correct_original', 'insert_count_original', 'delete_count_original', 'sub_count_original', 'total_phns_original','if_first_vowel_missing_original']] = pd_df_pivoted2['alignments'].apply(gen_mips_from_alignments)
    pd_df_pivoted2[['phn_correct_participant', 'insert_count_participant', 'delete_count_participant', 'sub_count_participant', 'total_phns_participant', 'if_first_vowel_missing_participant']] = pd_df_pivoted2['suggested alignments'].apply(gen_mips_from_alignments)
    pd_df_pivoted2.to_csv('sampleset_pd.csv', index=False)
    
    
    
    atx_df = xl.parse('Disagree- ATX', header=None)
    atx_df = atx_df.reset_index()
    atx_df['group'] = atx_df['index'].apply(convert_index_to_group)
    atx_df = atx_df.rename(columns={0: 'Target', 1: 'Transcript'})

    transcript_df = atx_df.iloc[0::8]
    transcript_index = range(0, len(atx_df), 8)
    atx_df = atx_df.drop(index=transcript_index)

    atx_df_pivoted = atx_df.pivot(columns='Target', values='Transcript', index='group').reset_index()
    atx_df_pivoted2 = atx_df_pivoted.merge(transcript_df, on='group')
    atx_df_pivoted2.rename(columns={np.nan: 'participant ipa'})
    atx_df_pivoted2[['phn_correct_original', 'insert_count_original', 'delete_count_original', 'sub_count_original', 'total_phns_original','if_first_vowel_missing_original']] = atx_df_pivoted2['alignments'].apply(gen_mips_from_alignments)
    atx_df_pivoted2[['phn_correct_participant', 'insert_count_participant', 'delete_count_participant', 'sub_count_participant', 'total_phns_participant', 'if_first_vowel_missing_participant']] = atx_df_pivoted2['suggested alignment'].apply(gen_mips_from_alignments)
    atx_df_pivoted2.to_csv('sampleset_atx.csv', index=False)

    pass


def gen_mips_from_alignments(alignment_str):
    try:
        alignment = eval(alignment_str)
        phn_correct, insert_count, delete_count, sub_count, total_phns, if_first_vowel_missing = calcPhonemeErrorsFromAlignRes2(alignment)
    except Exception as e:
        print(alignment_str)
        print(repr(e))
        phn_correct, insert_count, delete_count, sub_count, total_phns, if_first_vowel_missing = np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
    return pd.Series([phn_correct, insert_count, delete_count, sub_count, total_phns, if_first_vowel_missing])


def calc_lexical_boundary_errors():
    calc_lexical_boundary_errors_helper(r"C:\Users\Kelvin\Desktop\MIP_MA_LBE\MIP_CODE_W_LBE\sampleset_atx.csv")
    calc_lexical_boundary_errors_helper(r"C:\Users\Kelvin\Desktop\MIP_MA_LBE\MIP_CODE_W_LBE\sampleset_pd.csv")


def calc_lexical_boundary_errors_helper(file_path) -> object:
    """given csv of alignments generate a new csv with lexical_boundary_error and call it <name>_w_LBE.csv"""
    df = pd.read_csv(file_path, encoding='latin-1')
    df[['IS', 'IW', 'DS', 'DW']] = df.apply(calc_LBE_original, axis=1)
    df.to_csv(file_path.replace('.csv', '_w_LBE.csv'), index=False)


def calc_LBE_original(row):
    try:
        pattern_words, pattern_phn, pattern_phn_ipa, pattern_stress = processPattern(row['Target'])

        transcript_phn, transcript_phn_ipa, transcript_stress = processTranscript(row['Transcript'])

        _wrd_acc = calcWordCorrectness(pattern_words, row['Transcript'])

        if _wrd_acc is None or '-' in transcript_phn:
            _IS, _IW, _DS, _DW = None, None, None, None
        else:
            _phn_acc, _phn_ins, _phn_del, _phn_sub, _total_phns, if_first_vowel_missing = calcPhonemeErrors(pattern_phn_ipa,
                                                                                                            transcript_phn_ipa)
            if if_first_vowel_missing == 1 and pattern_stress[0][0] == '0' and len(''.join(transcript_stress)) == 5:
                transcript_stress = ['1'] + transcript_stress
            _IS, _IW, _DS, _DW = calcLBE(pattern_stress, transcript_stress)
    except:
        return pd.Series([None, None, None, None])
    return pd.Series([_IS, _IW, _DS, _DW])


if __name__ == "__main__":
    # main()
    # gen_mip_metrics_csv()
    calc_lexical_boundary_errors()