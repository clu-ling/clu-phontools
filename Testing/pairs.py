from try_another import Phrase, LexicalBoundaryErrorReport
import json

p = Phrase()
l = LexicalBoundaryErrorReport

pairs = [
    (['01', '0', '1', '0', '1'], ['01', '1', '1', '1', '1']),
    (['01', '0', '1', '01'], ['01', '10', '01']),
    (['01', '0', '1', '01'], ['01', '1', '1', '01']),
    (['01', '0', '1', '01'], ['01', '1', '1', '1', '1']),
    (['01', '0', '1', '01'], ['01', '1', '0', '01']),
    (['01', '0', '1', '01'], ['01', '1', '1', '01']),
    (['01', '01', '01'], ['01', '01', '0', '1']),
    (['01', '01', '01'], ['01', '1', '1', '0', '1']),
    (['01', '01', '01'], ['1', '100', '10']),
    (['01', '01', '01'], ['010', '1', '01']),
    (['01', '01', '01'], ['01', '0', '1', '01']),
    (['01', '01', '01'], ['1', '100', '01']),
    (['01', '01', '01'], ['1', '0', '0', '1', '01'])
]

for target, transcript in pairs:
    print(f"target:\t{target}")
    print(f"transcript:\t{transcript}")
    errors = p.calc_lbes(target, transcript)
    print(errors)
    #error_report= json.dumps([error.to_dict() for error in errors], indent=4)
    #print(f"errors: {error_report}")
    print()
