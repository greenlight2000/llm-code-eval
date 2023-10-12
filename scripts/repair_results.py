import re

from pathlib import Path
from datasets import load_dataset


def repair_diff_tag(example, invalid_positive_diff_tag_code_uids, invalid_negative_diff_tag_code_uids):
    code_uid = example['code_uid']
    if code_uid in invalid_positive_diff_tag_code_uids:
        example['diff_tag'] = 1
    elif code_uid in invalid_negative_diff_tag_code_uids:
        example['diff_tag'] = 0

    return example


def repair_smell(example, mapping):
    code_uid = example['code_uid']
    if code_uid in mapping.keys():
        example['smell'] = mapping.get(code_uid)

    return example


def repair_hidden_unit_tests(example, mapping):
    code_uid = example['code_uid']
    if code_uid in mapping.keys():
        example['hidden_unit_tests'] = mapping.get(code_uid)

    return example


def repair_code_test_data_wizardcoder():
    check_code_test_data_wizardcoder_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'check') / Path('wizardcoder') / Path('check_code_test_data_wizardcoder.jsonl')
    repair_code_test_data_wizardcoder_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'repair') / Path('wizardcoder') / Path('repair_code_test_data_wizardcoder.jsonl')

    mapping = {
        '7b16d6b2850c3f5c22debfbf00654009': "[{'input': '1990 1', 'output': ['9190']}, {'input': '300 0', 'output': ['300']}, {'input': '1034 2', 'output': ['3104']}, {'input': '9090000078001234 6', 'output': ['9907000008001234']}, {'input': '', 'output': ['']}]",
        '742bda22649603fa31ce596e36ecf9ad': "[{'input': '12\\ntoosmallword', 'output': ['NO']}, {'input': '35\\nTheQuickBrownFoxJumpsOverTheLazyDog', 'output': ['YES']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        '3f1473b75e501f802593e723cc2aecb1': "[{'input': 'abcd', 'output': ['0']}, {'input': 'ababa', 'output': ['3']}, {'input': 'zzz', 'output': ['2']}, {'input': 'abcabcabc', 'output': ['3']}, {'input': 'abcabcdefgabc', 'output': ['3']}]",
        'f019491af76df7f8d3b735e99349717a': "[{'input': '4 2 100000007', 'output': ['14']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        '2c04b42e8c8c1ad429e444aef500adef': "[{'input': '11\\n00000000008', 'output': ['1']}, {'input': '22\\n0011223344556677889988', 'output': ['2']}, {'input': '11\\n31415926535', 'output': ['0']}, {'input': '10\\n1234567890', 'output': ['0']}, {'input': '', 'output': ['']}]",
        '2f7816d44bdfa720760720f54fb0e3b1': "[{'input': '100010001', 'output': ['yes']}, {'input': '100', 'output': ['no']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        '1e893aa51d1c23c5787c90d8a946c7bb': "[{'input': '7\\nABACABA', 'output': ['AB']}, {'input': '5\\nZZZAA', 'output': ['ZZ']}, {'input': '10\\nABABABABABA', 'output': ['AB']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        '1ee6d560c74fa0a059b8abf9c4b047f7': "[{'input': '10\\nrocesfedoc', 'output': ['codeforces']}, {'input': '16\\nplmaetwoxesisiht', 'output': ['thisisexampletwo']}, {'input': '1\\nz', 'output': ['z']}, {'input': '10\\nabcdeabcde', 'output': ['abcdeabcde']}, {'input': '10\\ndefghijefgh', 'output': ['defghijefgh']}]",
        '770d421bfb5c6df811ba45baa8e43a4a': "[{'input': '8\\nbacabcab', 'output': ['4']}, {'input': '4\\nbcda', 'output': ['3']}, {'input': '6\\nabbbbb', 'output': ['5']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        'd713cd16583d2ff8099c0477deb72d23': "[{'input': '9', 'output': ['504']}, {'input': '7', 'output': ['210']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        '72f78d9ae9f025807e729b822077ace2': "[{'input': '10\\nrocesfedoc', 'output': ['codeforces']}, {'input': '16\\nplmaetwoxesisiht', 'output': ['thisisexampletwo']}, {'input': '1\\nz', 'output': ['z']}, {'input': '10\\nabcde', 'output': ['abcde']}, {'input': '10\\ndeforces', 'output': ['codeforces']}]",
        'e0936e5e62ffeda0bcb32579b1a80625': "[{'input': 'Is it a melon?', 'output': ['NO']}, {'input': 'Is it an apple?', 'output': ['YES']}, {'input': 'Is it a banana?', 'output': ['YES']}, {'input': 'Is it an apple and a banana?', 'output': ['YES']}, {'input': 'Is it a pear?', 'output': ['NO']}]",
        '1cea85e2f66b233a93c24d60fe669bbc': "[{'input': '4', 'output': ['6']}, {'input': '6', 'output': ['12']}, {'input': '10', 'output': ['28']}, {'input': '15', 'output': ['56']}, {'input': '20', 'output': ['100']}]",
        '6f2f01bc8e3eb2456c1a859c8ef6e3d3': "[{'input': '.......A\\n........\\n........\\n........\\n........\\n........\\n........\\nM.......', 'output': ['WIN']}, {'input': '.......A\\n........\\n........\\n........\\n........\\n........\\nSS......\\nM.......', 'output': ['LOSE']}, {'input': '.......A\\n........\\n........\\n........\\n........\\n.S......\\nS.......\\nMS......', 'output': ['LOSE']}, {'input': '.......A\\n........\\n........\\n........\\n........\\n.S......\\nS.......\\nM.......', 'output': ['WIN']}, {'input': '', 'output': ['']}]",
        '487c13218d4e38dfa69397e5d1a8d66f': "[{'input': 'abcd', 'output': ['0']}, {'input': 'ababa', 'output': ['3']}, {'input': 'zzz', 'output': ['2']}, {'input': 'abcabcabc', 'output': ['3']}, {'input': 'abcabcdefgabc', 'output': ['6']}]",
        'c7185703101804a6da5a22475a72f139': "[{'input': 'code\\nedoc', 'output': ['YES']}, {'input': 'abb\\naba', 'output': ['NO']}, {'input': 'code\\ncode', 'output': ['NO']}, {'input': 'abcde\\nedcba', 'output': ['YES']}, {'input': 'abcde\\nedcb', 'output': ['NO']}]",
        '64a8de51f0cd1a62244b393fad5dd07d': "[{'input': '3000', 'output': ['1']}, {'input': '10000', 'output': ['10']}, {'input': '1000000000', 'output': ['100000000']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        '607cfc90cbbdd84013355718b776f850': "[{'input': '42', 'output': ['1 2']}, {'input': '5', 'output': ['0 2']}, {'input': '12', 'output': ['1 0']}, {'input': '13', 'output': ['1 1']}, {'input': '15', 'output': ['1 2']}]",
        '5d47a35580bfefd1f36a6d946932b48b': "[{'input': '3 2', 'output': ['3']}, {'input': '5 4', 'output': ['25']}, {'input': '7 6', 'output': ['129']}, {'input': '11 10', 'output': ['1048575']}, {'input': '13 12', 'output': ['1048576']}]",
        'c7a2a21610b7bbd676b6c6db3f6c6cb0': "[{'input': 'harry potter', 'output': ['hap']}, {'input': 'john doe', 'output': ['jdoe']}, {'input': 'jane doe', 'output': ['jdoe']}, {'input': 'abc def', 'output': ['abcdef']}, {'input': 'aaa bbb', 'output': ['aaa']}]",
        '7b81a4801fc6c454082998b70a435eae': "[{'input': 'QAQAQYSYIOIWIN', 'output': ['4']}, {'input': 'QAQQQZZYNOIWIN', 'output': ['3']}, {'input': 'QAQ', 'output': ['1']}, {'input': 'QQQ', 'output': ['1']}, {'input': 'AAAA', 'output': ['1']}]",
        '21396af87304a95563d5b4b4a9eebdfd': "[{'input': '3', 'output': ['3']}, {'input': '11', 'output': ['0']}, {'input': '1', 'output': ['1']}, {'input': '10', 'output': ['0']}, {'input': '50', 'output': ['5']}]"
    }

    dataset = load_dataset('json', split='train', data_files=str(check_code_test_data_wizardcoder_result_path))
    dataset.cleanup_cache_files()
    print(dataset)

    dataset = dataset.map(lambda example: repair_hidden_unit_tests(example, mapping))
    print(dataset)

    dataset.to_json(repair_code_test_data_wizardcoder_result_path, lines=True)


def repair_code_review_eval_wizardcoder():
    code_review_eval_wizardcoder_log_path = Path(__file__).parent.parent / Path('logs') / Path('wizardcoder') / Path(
        'code_review_eval_wizardcoder.log')
    with open(code_review_eval_wizardcoder_log_path, mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        invalid_diff_tag_code_uids = []  # diff_tag = 2
        invalid_positive_diff_tag_code_uids = []  # diff_tag = 1
        invalid_negative_diff_tag_code_uids = []  # diff_tag = 0
        for i in range(len(lines)):
            diff_tag = None
            if 'code uid:' in lines[i]:
                code_uid = lines[i].split('code uid:')[-1].strip()
                for j in range(i, len(lines)):
                    if 'diff_tag:' in lines[j]:
                        diff_tag = lines[j].split('diff_tag:')[-1].strip()
                        break
                if diff_tag == '2':
                    invalid_diff_tag_code_uids.append(code_uid)
                    response_content = []
                    capture = False
                    for j in range(i, len(lines)):
                        if 'response:' in lines[j]:
                            capture = True
                            lines[j] = lines[j].split('response:')[-1].strip()
                        if 'output tokens:' in lines[j]:
                            invalid_diff_tag_response = '\n'.join(response_content).strip().lower()

                            good_content_1 = 'no review comments are required.'
                            good_content_2 = 'no review comments required.'
                            good_content_3 = 'does not require any review comments'
                            good_content_4 = 'requires no review comments'
                            good_content_5 = 'is a good quality'
                            good_content_6 = 'meets the requirements of a good quality code review'
                            good_content_7 = 'the code quality is good'
                            good_content_8 = 'the quality of the code is good'

                            poor_content_1 = 'requires review comments'
                            poor_content_2 = 'not meeting the requirements'
                            poor_content_3 = 'the quality of the code is poor'
                            poor_content_4 = 'is not a good quality'
                            poor_content_5 = 'should be reviewed with a higher level of scrutiny'
                            poor_content_6 = 'requires careful review'

                            if good_content_1 in invalid_diff_tag_response \
                                    or good_content_2 in invalid_diff_tag_response \
                                    or good_content_3 in invalid_diff_tag_response \
                                    or good_content_4 in invalid_diff_tag_response \
                                    or good_content_5 in invalid_diff_tag_response \
                                    or good_content_6 in invalid_diff_tag_response \
                                    or good_content_7 in invalid_diff_tag_response \
                                    or good_content_8 in invalid_diff_tag_response:
                                invalid_negative_diff_tag_code_uids.append(code_uid)
                            elif poor_content_1 in invalid_diff_tag_response \
                                    or poor_content_2 in invalid_diff_tag_response \
                                    or poor_content_3 in invalid_diff_tag_response \
                                    or poor_content_4 in invalid_diff_tag_response \
                                    or poor_content_5 in invalid_diff_tag_response \
                                    or poor_content_6 in invalid_diff_tag_response:
                                invalid_positive_diff_tag_code_uids.append(code_uid)
                            else:
                                print(code_uid)
                                print(invalid_diff_tag_response)
                            break
                        if capture:
                            response_content.append(lines[j].strip())
        print(len(invalid_diff_tag_code_uids))  # 791
        print(len(invalid_positive_diff_tag_code_uids))  # 11
        print(len(invalid_negative_diff_tag_code_uids))  # 767
        print(len(invalid_positive_diff_tag_code_uids) + len(invalid_negative_diff_tag_code_uids))  # 778 / 791
        # 4
        invalid_positive_diff_tag_code_uids.append('d65061d0958f492fb4f51d38020ca241')
        invalid_positive_diff_tag_code_uids.append('1826de56fc6f49f0b89a64ee44e96350')
        invalid_positive_diff_tag_code_uids.append('38f2a48391fe4bbc82a0fd2a1fdb6982')
        invalid_positive_diff_tag_code_uids.append('60eb9be1f6dd46be90837036dc0d2a4e')

    check_code_review_eval_wizardcoder_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'check') / Path('wizardcoder') / Path('check_code_review_eval_wizardcoder.jsonl')
    repair_code_review_eval_wizardcoder_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'repair') / Path('wizardcoder') / Path('repair_code_review_eval_wizardcoder.jsonl')

    dataset = load_dataset('json', split='train', data_files=str(check_code_review_eval_wizardcoder_result_path))
    dataset.cleanup_cache_files()
    print(dataset)

    dataset = dataset.map(lambda example: repair_diff_tag(example, invalid_positive_diff_tag_code_uids,
                                                          invalid_negative_diff_tag_code_uids))
    print(dataset)

    dataset.to_json(repair_code_review_eval_wizardcoder_result_path, lines=True)


def repair_code_test_data_vicuna():
    check_code_test_data_vicuna_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'check') / Path('vicuna') / Path('check_code_test_data_vicuna.jsonl')
    repair_code_test_data_vicuna_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'repair') / Path('vicuna') / Path('repair_code_test_data_vicuna.jsonl')

    mapping = {
        'ef40b724e511308ccea6397eaf03087d': "[{'input': '5\\n)))))()', 'output': ['5']}, {'input': '3\\n(()', 'output': ['4']}, {'input': '2\\n(((', 'output': ['0']}, {'input': '4\\n((((', 'output': ['0']}, {'input': '6\\n)((((((', 'output': ['0']}]",
        '60963d7db9b16b782869efad9cbe0603': "[{'input': '... ... ...\\n... ... ...\\n... ... ...\\n\\n... ... ...\\n... x.. ...\\n\\n... ... ...\\n... ... ...\\n... ... ...\\n... x.. ...\\n\\n... ... ...\\n... ... ...\\n... ... ...\\n7 4', 'output': ['... ... ... \\n... ... ... \\n... ... ... \\n\\n... ... ... \\n... ... ... \\n... x.. ... \\n\\n!!! ... ... \\n!!! ... ... \\n!!! ... ...']}, {'input': 'xoo x.. x..\\nooo ... ...\\nooo ... ...\\n\\nx.. x.. x..\\n... ... ...\\n... ... ...\\n\\nx.. x.. x..\\n... ... ...\\n... ... ...\\n7 4', 'output': ['xoo x!! x!! \\nooo !!! !!! \\nooo !!! !!! \\n\\nx!! x!! x!! \\n!!! !!! !!! \\n!!! !!! !!! \\n\\nx!! x!! x!! \\n!!! !!! !!! \\n!!! !!! !!!']}, {'input': 'o.. ... ...\\n... ... ...\\n... ... ...\\n\\n... xxx ...\\n... xox ...\\n... ooo ...\\n\\n... ... ...\\n... ... ...\\n... ... ...\\n5 5', 'output': ['o!! !!! !!! \\n!!! !!! !!! \\n!!! !!! !!! \\n\\n!!! xxx !!! \\n!!! xox !!! \\n!!! ooo !!! \\n\\n!!! !!! !!! \\n!!! !!! !!! \\n!!! !!! !!!']}, {'input': '... ... ...\\n... ... ...\\n... ... ...\\n... ... ...\\n... ... ...\\n... ... ...\\n... x.. ...\\n\\n... ... ...\\n... ... ...\\n... ... ...\\n... x.. ...\\n\\n... ... ...\\n... ... ...\\n7 4', 'output': ['... ... ... \\n... ... ... \\n... ... ... \\n\\n... ... ... \\n... ... ... \\n... x.. ... \\n\\n!!! ... ... \\n!!! ... ... \\n!!! ... ...']}, {'input': '', 'output': ['']}]",
        '742bda22649603fa31ce596e36ecf9ad': "[{'input': 'abcdefghijklmnopqrstuvwxyz', 'output': ['YES']}, {'input': 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'output': ['YES']}, {'input': 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'output': ['YES']}, {'input': 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'output': ['YES']}, {'input': '', 'output': ['']}]",
        'd1d6257f91fbbd267127477970d88022': "[{'input': '4\\n1 1 0 1', 'output': ['3']}, {'input': '6\\n0 1 0 0 1 0', 'output': ['4']}, {'input': '1\\n0', 'output': ['1']}, {'input': '10\\n0 1 0 0 1 0 0 0 1 0 0', 'output': ['5']}, {'input': '', 'output': ['']}]",
        'db45c4213b4b97c426871fe91634fae0': "[{'input': 'QAQAQYSYIOIWIN', 'output': ['4']}, {'input': 'QAQQQZZYNOIWIN', 'output': ['3']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        '2f7816d44bdfa720760720f54fb0e3b1': "[{'input': '01010101', 'output': ['yes']}, {'input': '10101010', 'output': ['no']}, {'input': '11011011', 'output': ['yes']}, {'input': '11111111', 'output': ['no']}, {'input': '1010101010101010', 'output': ['yes']}]",
        '28edecddfde5fe488a99740254e4b6bc': "[{'input': '8.549e2', 'output': ['854.9']}, {'input': '8.549e3', 'output': ['8549']}, {'input': '0.33e0', 'output': ['0.33']}, {'input': '1.234e-5', 'output': ['0.000123']}, {'input': '123.456e7', 'output': ['123456']}]",
        'a01207ee0161127628f9b9182f1eb4ee': "[{'input': '11\\n00000000008', 'output': ['1']}, {'input': '22\\n0011223344556677889988', 'output': ['2']}, {'input': '11\\n31415926535', 'output': ['0']}, {'input': '11\\n0000000000800000', 'output': ['1']}, {'input': '', 'output': ['']}]",
        '0b45b8015a747797dd5485bf6af45dce': "[{'input': '6 1', 'output': ['3']}, {'input': '60 5', 'output': ['237178099']}, {'input': '1000000000 100000', 'output': ['1000000000']}, {'input': '1000000000000 100000', 'output': ['1000000000000']}, {'input': '', 'output': ['']}]",
        'e5bc00404301ef2a118826c60a184232': "[{'input': 'abcdefghijklmnopqrstuvwxyz', 'output': ['YES']}, {'input': 'abcdefghijklmnopqrstuvwxyz123456789', 'output': ['NO']}, {'input': 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'output': ['NO']}, {'input': 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'output': ['NO']}, {'input': '', 'output': ['']}]",
        '7b81a4801fc6c454082998b70a435eae': "[{'input': 'QAQAQYSYIOIWIN', 'output': ['4']}, {'input': 'QAQQQZZYNOIWIN', 'output': ['3']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        '6641d80a5bda4ca0c4e46aa2da489db9': "[{'input': '5\\n5555\\n555\\n55\\n5', 'output': ['0']}, {'input': '6\\n6666\\n666\\n66\\n6', 'output': ['0']}, {'input': '7\\n7777\\n777\\n77\\n7', 'output': ['0']}, {'input': '8\\n8888\\n888\\n88\\n8', 'output': ['0']}, {'input': '9\\n9999\\n999\\n99\\n9', 'output': ['0']}]"
    }

    dataset = load_dataset('json', split='train', data_files=str(check_code_test_data_vicuna_result_path))
    dataset.cleanup_cache_files()
    print(dataset)

    dataset = dataset.map(lambda example: repair_hidden_unit_tests(example, mapping))
    print(dataset)

    dataset.to_json(repair_code_test_data_vicuna_result_path, lines=True)


def repair_code_smell_eval_gpt4():
    check_code_smell_eval_gpt4_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'check') / Path('gpt4') / Path('check_code_smell_eval_gpt4.jsonl')
    repair_code_smell_eval_gpt4_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'repair') / Path('gpt4') / Path('repair_code_smell_eval_gpt4.jsonl')

    mapping = {
        'e9aea3f62f52457fa1fbfe82addbec7c': "long method",
        'ad7f11861fbf4883becfa561bad8fc36': "long method",
        'fa20381cfcc44ec9a14da8653e9f66cd': "long method",
        'b46a94e293ac464a8244294641a63a1f': "long method",
        '99c31742e2284eac90dcc9c1cea60977': "large class",
        '4e7d4de4b7f242deba18ea428b739b2e': "long method",
        'a9079c2f9c8342288c445787de224245': "large class",
        'd724d0a851a547a78f510aa8a1b43ae1': "long method",
        '2d5a4120383a4b8fb50a835b540e5c69': "data class",
        '1415ea65e9db44118fbcca92779f6416': "long method",
        '5141dfad903041cd8019ce6b36de5305': "long method",
        'e753a203eddf40678352b473cd73f09d': "long method",
        '8a225ce457fe4f8b86f5d381d065a5c8': "long method"
    }

    dataset = load_dataset('json', split='train', data_files=str(check_code_smell_eval_gpt4_result_path))
    dataset.cleanup_cache_files()
    print(dataset)

    dataset = dataset.map(lambda example: repair_smell(example, mapping))
    print(dataset)

    dataset.to_json(repair_code_smell_eval_gpt4_result_path, lines=True)


def repair_code_test_data_gpt4():
    check_code_test_data_gpt4_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'check') / Path('gpt4') / Path('check_code_test_data_gpt4.jsonl')
    repair_code_test_data_gpt4_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'repair') / Path('gpt4') / Path('repair_code_test_data_gpt4.jsonl')

    mapping = {
        '2f7816d44bdfa720760720f54fb0e3b1': "[{'input': '1000000', 'output': ['yes']}, {'input': '1111111', 'output': ['no']}, {'input': '1010101010101', 'output': ['yes']}, {'input': '1001', 'output': ['no']}, {'input': '11000000', 'output': ['yes']}]",
        'b74d1efc8dc7c743f39b0603ef78ded1': "[{'input': 'WUBWUBIWUBWUBAMWUBWUBX', 'output': ['I AM X']}, {'input': 'WUBWUBLOVEWUBWUBTHEWUBWAYWUBYOUWUBLIEWUB', 'output': ['LOVE THE WAY YOU LIE']}, {'input': 'WUBWUBWUBBOHEMIANWUBRHAPSODYWUBWUBWUB', 'output': ['BOHEMIAN RHAPSODY']}, {'input': 'WUBWUBSMOKEWUBONWUBTHEWUBWATERWUB', 'output': ['SMOKE ON THE WATER']}, {'input': 'WUBWUBWUBWUBSTAIRWAYWUBTOWUBHEAVENWUBWUBWUBWUB', 'output': ['STAIRWAY TO HEAVEN']}]",
        '7b81a4801fc6c454082998b70a435eae': "[{'input': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'output': ['0']}, {'input': 'QQQQAAAA', 'output': ['16']}, {'input': 'QAQQAQQA', 'output': ['10']}, {'input': 'QWERTYUIOP', 'output': ['0']}, {'input': 'AAQQQAAQQQ', 'output': ['18']}]",
    }

    dataset = load_dataset('json', split='train', data_files=str(check_code_test_data_gpt4_result_path))
    dataset.cleanup_cache_files()
    print(dataset)

    dataset = dataset.map(lambda example: repair_hidden_unit_tests(example, mapping))
    print(dataset)

    dataset.to_json(repair_code_test_data_gpt4_result_path, lines=True)


def repair_code_smell_eval_gpt3():
    check_code_smell_eval_gpt3_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'check') / Path('gpt3') / Path('check_code_smell_eval_gpt3.jsonl')
    repair_code_smell_eval_gpt3_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'repair') / Path('gpt3') / Path('repair_code_smell_eval_gpt3.jsonl')

    mapping = {
        'ad7f11861fbf4883becfa561bad8fc36': "long method",
        '0abeecbb2bd847ed95266193e193af5d': "long method"
    }

    dataset = load_dataset('json', split='train', data_files=str(check_code_smell_eval_gpt3_result_path))
    dataset.cleanup_cache_files()
    print(dataset)

    dataset = dataset.map(lambda example: repair_smell(example, mapping))
    print(dataset)

    dataset.to_json(repair_code_smell_eval_gpt3_result_path, lines=True)


def repair_code_test_data_gpt3():
    check_code_test_data_gpt3_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'check') / Path('gpt3') / Path('check_code_test_data_gpt3.jsonl')
    repair_code_test_data_gpt3_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'repair') / Path('gpt3') / Path('repair_code_test_data_gpt3.jsonl')

    mapping = {
        'e40e73c16a57fbbfbcb77982030e15f0': "[{'input': '0 0 0 0 9\\n0 0 0 0 0\\n0 0 0 0 0\\n0 0 0 0 0\\n7 0 0 0 0', 'output': ['32']}, {'input': '0 43 21 18 2\\n3 0 21 11 65\\n5 2 0 1 4\\n54 62 12 0 99\\n87 64 81 33 0', 'output': ['620']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        '2f8dd925dd6a7b0ba31981760e264222': "[{'input': 'BBBSSC\\n6 4 1\\n1 2 3\\n4', 'output': ['2']}, {'input': 'BBC\\n1 10 1\\n1 10 1\\n21', 'output': ['7']}, {'input': 'BSC\\n1 1 1\\n1 1 3\\n1000000000000', 'output': ['200000000001']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        'db45c4213b4b97c426871fe91634fae0': "[{'input': 'QAQAQYSYIOIWIN', 'output': ['4']}, {'input': 'QAQQQZZYNOIWIN', 'output': ['3']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        '4c82f84bb04eecfb71da878b973f0c1d': "[{'input': '0 0 0 0 9\\n0 0 0 0 0\\n0 0 0 0 0\\n0 0 0 0 0\\n7 0 0 0 0', 'output': ['32']}, {'input': '0 43 21 18 2\\n3 0 21 11 65\\n5 2 0 1 4\\n54 62 12 0 99\\n87 64 81 33 0', 'output': ['620']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        'b74d1efc8dc7c743f39b0603ef78ded1': "[{'input': 'WUBWUBWUBABCWUBWUBWUB', 'output': ['ABC']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        '7b81a4801fc6c454082998b70a435eae': "[{'input': 'QAQAQYSYIOIWIN', 'output': ['4']}, {'input': 'QAQQQZZYNOIWIN', 'output': ['3']}, {'input': 'QAQQAQAQQAQQAQ', 'output': ['28']}, {'input': 'QQQQQQQQQQQQQQQ', 'output': ['0']}, {'input': 'AAAAAAAAAAAAAAA', 'output': ['0']}]"
    }

    dataset = load_dataset('json', split='train', data_files=str(check_code_test_data_gpt3_result_path))
    dataset.cleanup_cache_files()
    print(dataset)

    dataset = dataset.map(lambda example: repair_hidden_unit_tests(example, mapping))
    print(dataset)

    dataset.to_json(repair_code_test_data_gpt3_result_path, lines=True)


def repair_code_review_eval_gpt3():
    check_code_review_eval_gpt3_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'check') / Path('gpt3') / Path('check_code_review_eval_gpt3.jsonl')
    repair_code_review_eval_gpt3_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'repair') / Path('gpt3') / Path('repair_code_review_eval_gpt3.jsonl')

    invalid_positive_diff_tag_code_uids = [
        'd11c831c4ba44fdf91f2dc7405bffb12',
        'b202f6391cb949fd8be4457503e95c8c',
        'd0e166628ccb4d05a4e6c34c895a4256',
        '7b4205b54c604db185349d2ac5c3f474',
        '428465548d3b4fb0828182f14989f813',
        'cb0ccdb26f904d549c10f72b9ae52785',
        'af63737485294d98ba95066844e15a3b',
        '89a0a444954d4a1085e4c396aeed45d9',
        '9c19f8ed31334e86b5e853bb9ac09c34',
        'efa0d59fda3c47febac0f947f141157f',
        'e02de47394eb499fb560d3f00906326a',
        '561e7e4a324e4f3199eae8c32d21b678',
        '5e1759fb14c54c3aaba2f5740777e9c2',
        'bc0b5f0b961644fc965065f9473fe842',
        'b032fd8dff7d4cc1a5893794fcbca377',
        '68a86df048b9458caff1f69a0c8ba962',
        '3f50f8a0a54c444fa7c79e1969aa4fb8',
        '42974fe647bc4bc1a49d7969e9ca2192',
        '717172904ca94b40965ff92f799bd61c',
        '16cc07fcf0824861b4e7d93f5599ddd0',
        '8801311a9f2740b1a0493576ac9731a5',
        '807ea5bfe049449a8c8137aea3dbec2f'
    ]  # diff_tag = 1
    invalid_negative_diff_tag_code_uids = []  # diff_tag = 0
    dataset = load_dataset('json', split='train', data_files=str(check_code_review_eval_gpt3_result_path))
    dataset.cleanup_cache_files()
    print(dataset)

    dataset = dataset.map(lambda example: repair_diff_tag(example, invalid_positive_diff_tag_code_uids,
                                                          invalid_negative_diff_tag_code_uids))
    print(dataset)

    dataset.to_json(repair_code_review_eval_gpt3_result_path, lines=True)


def repair_code_test_data_llama2():
    check_code_test_data_llama2_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'check') / Path('llama2') / Path('check_code_test_data_llama2.jsonl')
    repair_code_test_data_llama2_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'repair') / Path('llama2') / Path('repair_code_test_data_llama2.jsonl')

    mapping = {
        '0f7d73539239e586bb5c45a78404c2aa': "[{'input': '6 3\\n1 1 1 0 1 0', 'output': ['3']}, {'input': '5 2\\n0 0 0 1 0', 'output': ['1']}, {'input': '4 1\\n1 0 1 0', 'output': ['1']}, {'input': '10 5\\n1 1 1 1 1 0 0 0 0', 'output': ['4']}, {'input': '', 'output': ['']}]",
        '57ea84cc35e8283d0afea7bee5d3b93f': "[{'input': '3000', 'output': ['1']}, {'input': '10000', 'output': ['5']}, {'input': '2342', 'output': ['2']}, {'input': '123456', 'output': ['10']}, {'input': '42', 'output': ['3']}]",
        'ae3d1f11850895d2d6f7cd2ec2cd8273': "[{'input': '2', 'output': ['25']}, {'input': '10', 'output': ['50']}, {'input': '100', 'output': ['500']}, {'input': '1000', 'output': ['5000']}, {'input': '2147483647', 'output': ['54321675725']}]",
        '3c4dba385b37b5ef1b611d3cd8ee1040': "[{'input': '5', 'output': ['3']}, {'input': '10', 'output': ['5']}, {'input': '2', 'output': ['1']}, {'input': '4', 'output': ['2']}, {'input': '9', 'output': ['4']}]",
        '9557af7f6c0ea2ff51c70a2f5223221a': "[{'input': '10 3 5 2 3', 'output': ['16']}, {'input': '20 10 10 5 5', 'output': ['40']}, {'input': '10 2 3 5 5', 'output': ['11']}, {'input': '5 5 5 5 5', 'output': ['25']}, {'input': '100 10 10 100 100', 'output': ['10000']}]",
        'b00ee8d6b0774ac21a19e733ecf8120a': "[{'input': '3', 'output': ['9']}, {'input': '4', 'output': ['16']}, {'input': '10', 'output': ['100']}, {'input': '20', 'output': ['400']}, {'input': '1000', 'output': ['1000003']}]",
        'be920453fabb02e87093ed0e72972756': "[{'input': '12', 'output': ['2']}, {'input': '20', 'output': ['4']}, {'input': '35', 'output': ['7']}, {'input': '100', 'output': ['12']}, {'input': '1000', 'output': ['231']}]",
        '553bceb132fe79a128b299bc9e09118a': "[{'input': 'LLUUUR', 'output': ['OK']}, {'input': 'RRUULLDD', 'output': ['BUG']}, {'input': 'LUUUUR', 'output': ['BUG']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        'a7c8faaea19ea8bdf4482ed8c4acf808': "[{'input': '4', 'output': ['4']}, {'input': '6', 'output': ['12']}, {'input': '10', 'output': ['30']}, {'input': '20', 'output': ['120']}, {'input': '100', 'output': ['5040']}]",
        '1b292e35610de715cc299275f718a033': "[{'input': '2', 'output': ['25']}, {'input': '10', 'output': ['50']}, {'input': '100', 'output': ['500']}, {'input': '1000', 'output': ['5000']}, {'input': '2147483647', 'output': ['5432167775']}]",
        'f019491af76df7f8d3b735e99349717a': "[{'input': '4 2 100000007', 'output': ['14']}, {'input': '5 3 100000007', 'output': ['35']}, {'input': '10 4 100000007', 'output': ['169']}, {'input': '20 5 100000007', 'output': ['1048576']}, {'input': '100 10 100000007', 'output': ['1234567890']}]",
        '72b3d7f2193cdfff9bc674c63c12ebf2': "[{'input': '3000', 'output': ['1']}, {'input': '10000', 'output': ['4']}, {'input': '2520', 'output': ['0']}, {'input': '50000', 'output': ['20']}, {'input': '12345', 'output': ['5']}]",
        '9d375e775c9a50ce6f2f3fdc346eacdf': "[{'input': '2 3', 'output': ['8']}, {'input': '3 3', 'output': ['27']}, {'input': '4 4', 'output': ['256']}, {'input': '10 10', 'output': ['1048576']}, {'input': '50 50', 'output': ['1224735288']}]",
        '0d5fd2ecccc565cd9df7b318350866b4': "[{'input': '4 1 2', 'output': ['12']}, {'input': '2 1 1', 'output': ['4']}, {'input': '3 2 3', 'output': ['10']}, {'input': '5 4 5', 'output': ['21']}, {'input': '10 9 10', 'output': ['100']}]",
        'b8d69258742520bfbb90459050c614c1': "[{'input': '10 3 5 2 3', 'output': ['16']}, {'input': '100 10 50 20 3', 'output': ['500']}, {'input': '1 1 1 1 1', 'output': ['1']}, {'input': '1000 100 500 200 3', 'output': ['50000']}, {'input': '1 2 3 4 5', 'output': ['15']}]",
        'a0831519cbb276581bbab46a58baff2c': "[{'input': '3', 'output': ['9']}, {'input': '10', 'output': ['25']}, {'input': '50', 'output': ['1225']}, {'input': '100', 'output': ['31250']}, {'input': '1000', 'output': ['12345675']}]",
        'bd4288e58ffba130c210bec4d9f29a5e': "[{'input': '4 3', 'output': ['6']}, {'input': '12 15', 'output': ['3']}, {'input': '2 2', 'output': ['2']}, {'input': '10 5', 'output': ['5']}, {'input': '36 40', 'output': ['4']}]",
        '2f7816d44bdfa720760720f54fb0e3b1': "[{'input': '100010001', 'output': ['yes']}, {'input': '100', 'output': ['no']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        '3423477cc0a1968d011d3903a2441c6d': "[{'input': 'e4', 'output': ['8']}, {'input': 'a1', 'output': ['1']}, {'input': 'h8', 'output': ['1']}, {'input': 'e1', 'output': ['2']}, {'input': 'e8', 'output': ['2']}]",
        '80db3d064f45537bd7563130c38d4494': "[{'input': '12', 'output': ['2']}, {'input': '20', 'output': ['4']}, {'input': '35', 'output': ['7']}, {'input': '100', 'output': ['12']}, {'input': '1000', 'output': ['231']}]",
        'aa8a180c0397e093163d1aaa66efa1fb': "[{'input': '3000', 'output': ['1']}, {'input': '10000', 'output': ['4']}, {'input': '2342', 'output': ['2']}, {'input': '123456', 'output': ['10']}, {'input': '54321', 'output': ['3']}]",
        'b97713230ae1d58424ca27303c20f187': "[{'input': '390', 'output': ['216']}, {'input': '7', 'output': ['7']}, {'input': '1000000000', 'output': ['387420489']}, {'input': '123456789', 'output': ['216']}, {'input': '', 'output': ['']}]",
        'c3f00d09b4707b71ec10f761e41328ea': "[{'input': '12345', 'output': ['71232']}, {'input': '23456', 'output': ['65437']}, {'input': '11111', 'output': ['11111']}, {'input': '00000', 'output': ['00000']}, {'input': '99999', 'output': ['99999']}]",
        'fdb9f68abb2c3019dcbf9ee22981c4b9': "[{'input': '6 3', 'output': ['1 3']}, {'input': '10 5', 'output': ['2 8']}, {'input': '10 0', 'output': ['0 10']}, {'input': '5 2', 'output': ['1 3']}, {'input': '100 50', 'output': ['50 50']}]",
        '64a8de51f0cd1a62244b393fad5dd07d': "[{'input': '3000', 'output': ['1']}, {'input': '1000', 'output': ['0']}, {'input': '2520', 'output': ['1']}, {'input': '500000', 'output': ['50']}, {'input': '1000000', 'output': ['100']}]",
        'a71a01171806a337eb6b0f1c9f3268f4': "[{'input': '6\\n4 1 7 8 3 8\\n1', 'output': ['3']}, {'input': '10\\n1 2 3 4 5 6 7 8 9 10\\n10', 'output': ['10']}, {'input': '100\\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20\\n100', 'output': ['100']}, {'input': '1000\\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200', 'output': ['200']}, {'input': '', 'output': ['']}]",
        '59818fd9dcb02014b1f1ecbc70fab20e': "[{'input': '5', 'output': ['120']}, {'input': '10', 'output': ['3628800']}, {'input': '2', 'output': ['1']}, {'input': '50', 'output': ['35747161600']}, {'input': '', 'output': ['']}]",
        '55019f26f970076f44fd5b6f9d161b40': "[{'input': '12', 'output': ['2']}, {'input': '20', 'output': ['4']}, {'input': '35', 'output': ['7']}, {'input': '100', 'output': ['16']}, {'input': '1000', 'output': ['256']}]",
        '946191473fe8debb20ab3f4dbbde1696': "[{'input': '390', 'output': ['216']}, {'input': '7', 'output': ['7']}, {'input': '1000000000', 'output': ['387420489']}, {'input': '123456789', 'output': ['216789']}, {'input': '', 'output': ['']}]",
        '4b4808a1d50cf5b792f4e4dba57ad81f': "[{'input': 'mew', 'output': ['3']}, {'input': 'wuffuw', 'output': ['5']}, {'input': 'qqqqqqqq', 'output': ['0']}, {'input': 'abab', 'output': ['2']}, {'input': 'papicipap', 'output': ['4']}]",
        '7b81a4801fc6c454082998b70a435eae': "[{'input': 'QAQAQYSYIOIWIN', 'output': ['4']}, {'input': 'QAQQQZZYNOIWIN', 'output': ['3']}, {'input': 'QAQQAQQAQQAQ', 'output': ['5']}, {'input': 'AQQAQQAQQAQQ', 'output': ['4']}, {'input': 'QQAQQAQQAQQA', 'output': ['3']}]"
    }

    dataset = load_dataset('json', split='train', data_files=str(check_code_test_data_llama2_result_path))
    dataset.cleanup_cache_files()
    print(dataset)

    dataset = dataset.map(lambda example: repair_hidden_unit_tests(example, mapping))
    print(dataset)

    dataset.to_json(repair_code_test_data_llama2_result_path, lines=True)


def repair_code_test_data_codellama():
    check_code_test_data_codellama_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'check') / Path('codellama') / Path('check_code_test_data_codellama.jsonl')
    repair_code_test_data_codellama_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'repair') / Path('codellama') / Path('repair_code_test_data_codellama.jsonl')

    mapping = {
        'c2acdd580aea47e08a1ff2d92ec2a416': "[{'input': '2 2\\nRU', 'output': ['Yes']}, {'input': '1 2\\nRU', 'output': ['No']}, {'input': '-1 1000000000\\nLRRLU', 'output': ['Yes']}, {'input': '0 0\\nD', 'output': ['Yes']}, {'input': '', 'output': ['']}]",
        'd6624135180134ad303c18a992bf8632': "[{'input': '5 3 2\\nto head\\n0001001', 'output': ['Stowaway']}, {'input': '3 2 1\\nto tail\\n0001', 'output': ['Controller 2']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        '4576bec8d0405b7b07a9657304d115f1': "[{'input': '5 2 433416647', 'output': ['1']}, {'input': '10 3 409693891', 'output': ['2']}, {'input': '65 4 177545087', 'output': ['910726']}, {'input': '100 5 1000000007', 'output': ['1000000000']}, {'input': '', 'output': ['']}]",
        '68be7913d7ce93a0cdca60cbae812e89': "[{'input': 'xx..\\n.oo.\\nx...\\noox.', 'output': ['YES']}, {'input': 'x.ox\\nox..\\nx.o.\\noo.x', 'output': ['NO']}, {'input': 'x..x\\n..oo\\no...\\nx.xo', 'output': ['YES']}, {'input': 'o.x.\\no...\\n.x..\\nooxx', 'output': ['NO']}, {'input': 'x.x.\\n.o.o\\nx.x.\\noox.', 'output': ['YES']}]",
        '2f7816d44bdfa720760720f54fb0e3b1': "[{'input': '100010001', 'output': ['yes']}, {'input': '100', 'output': ['no']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        '41e91d84278bc1e9d5b8b84f37707640': "[{'input': '1 2 1000', 'output': ['4']}, {'input': '2 2 1000', 'output': ['45']}, {'input': '5 3 1103', 'output': ['590']}, {'input': '10 5 10000', 'output': ['1234567890']}, {'input': '', 'output': ['']}]",
        '6ef872ef7f4b5050760c2a9f2b797be2': "[{'input': '4\\n6\\n1\\n1\\n1\\n1', 'output': ['3 7']}, {'input': '1\\n10\\n5', 'output': ['15 15']}, {'input': '3\\n6\\n1\\n6\\n5', 'output': ['6 12']}, {'input': '3\\n7\\n1\\n6\\n5', 'output': ['7 13']}, {'input': '2\\n3\\n1\\n1', 'output': ['2 3']}]",
        '8d74bb2651d1a145ef41e02e6f589547': "[{'input': '047', 'output': ['4']}, {'input': '16', 'output': ['-1']}, {'input': '472747', 'output': ['7']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        '1cea85e2f66b233a93c24d60fe669bbc': "[{'input': '4', 'output': ['6']}, {'input': '6', 'output': ['12']}, {'input': '10', 'output': ['2520']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]",
        'e8f624d23e36b837e350d21df82c289f': "[{'input': '10 5', 'output': ['0 15 15 0']}, {'input': '-10 5', 'output': ['-15 0 0 15']}, {'input': '0 0', 'output': ['0 0 0 0']}, {'input': '10 -5', 'output': ['0 5 5 0']}, {'input': '-10 -5', 'output': ['-5 0 0 -5']}]",
        'a06e529109fcd598188d6765019dd515': "[{'input': '1 2 1000', 'output': ['4']}, {'input': '2 2 1000', 'output': ['45']}, {'input': '5 3 1103', 'output': ['590']}, {'input': '10 5 10000', 'output': ['1234567890']}, {'input': '', 'output': ['']}]",
        'b74d1efc8dc7c743f39b0603ef78ded1': "[{'input': 'WUBWUBABCWUB', 'output': ['ABC']}, {'input': 'WUBWEWUBAREWUBWUBTHEWUBCHAMPIONSWUBMYWUBFRIENDWUB', 'output': ['WE ARE THE CHAMPIONS MY FRIEND']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]"
    }

    dataset = load_dataset('json', split='train', data_files=str(check_code_test_data_codellama_result_path))
    dataset.cleanup_cache_files()
    print(dataset)

    dataset = dataset.map(lambda example: repair_hidden_unit_tests(example, mapping))
    print(dataset)

    dataset.to_json(repair_code_test_data_codellama_result_path, lines=True)


def repair_code_review_eval_codellama():
    code_review_eval_codellama_log_path = Path(__file__).parent.parent / Path('logs') / Path('codellama') / Path(
        'code_review_eval_codellama.log')
    with open(code_review_eval_codellama_log_path, mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        invalid_diff_tag_code_uids = []  # diff_tag = 2
        invalid_positive_diff_tag_code_uids = []  # diff_tag = 1
        invalid_negative_diff_tag_code_uids = []  # diff_tag = 0
        for i in range(len(lines)):
            diff_tag = None
            if 'code uid:' in lines[i]:
                code_uid = lines[i].split('code uid:')[-1].strip()
                for j in range(i, len(lines)):
                    if 'diff_tag:' in lines[j]:
                        diff_tag = lines[j].split('diff_tag:')[-1].strip()
                        break
                if diff_tag == '2':
                    invalid_diff_tag_code_uids.append(code_uid)
                    response_content = []
                    capture = False
                    for j in range(i, len(lines)):
                        if 'response:' in lines[j]:
                            capture = True
                            lines[j] = lines[j].split('response:')[-1].strip()
                        if 'output tokens:' in lines[j]:
                            invalid_diff_tag_response = '\n'.join(response_content).strip().lower()

                            good_content_1 = 'no review comments are required.'
                            good_content_2 = 'no review comments required.'
                            good_content_3 = 'does not require any review comments'
                            good_content_4 = 'requires no review comments'
                            good_content_5 = 'is a good quality'
                            good_content_6 = 'meets the requirements of a good quality code review'
                            good_content_7 = 'the code quality is good'
                            good_content_8 = 'the quality of the code is good'

                            poor_content_1 = 'requires review comments'
                            poor_content_2 = 'not meeting the requirements'
                            poor_content_3 = 'the quality of the code is poor'
                            poor_content_4 = 'is not a good quality'
                            poor_content_5 = 'should be reviewed with a higher level of scrutiny'
                            poor_content_6 = 'requires careful review'

                            if good_content_1 in invalid_diff_tag_response \
                                    or good_content_2 in invalid_diff_tag_response \
                                    or good_content_3 in invalid_diff_tag_response \
                                    or good_content_4 in invalid_diff_tag_response \
                                    or good_content_5 in invalid_diff_tag_response \
                                    or good_content_6 in invalid_diff_tag_response \
                                    or good_content_7 in invalid_diff_tag_response \
                                    or good_content_8 in invalid_diff_tag_response:
                                invalid_negative_diff_tag_code_uids.append(code_uid)
                            elif poor_content_1 in invalid_diff_tag_response \
                                    or poor_content_2 in invalid_diff_tag_response \
                                    or poor_content_3 in invalid_diff_tag_response \
                                    or poor_content_4 in invalid_diff_tag_response \
                                    or poor_content_5 in invalid_diff_tag_response \
                                    or poor_content_6 in invalid_diff_tag_response:
                                invalid_positive_diff_tag_code_uids.append(code_uid)
                            else:
                                print(code_uid)
                                print(invalid_diff_tag_response)
                            break
                        if capture:
                            response_content.append(lines[j].strip())
        print(len(invalid_diff_tag_code_uids))  # 217
        print(len(invalid_positive_diff_tag_code_uids))  # 6
        print(len(invalid_negative_diff_tag_code_uids))  # 209
        print(len(invalid_positive_diff_tag_code_uids) + len(invalid_negative_diff_tag_code_uids))  # 215 / 217
        # 2
        invalid_negative_diff_tag_code_uids.append('9e3e9cbe5abb4afb89ffdbb494b58f00')
        invalid_positive_diff_tag_code_uids.append('7374567a45d14fc3b004898a996490ee')

    check_code_review_eval_codellama_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'check') / Path('codellama') / Path('check_code_review_eval_codellama.jsonl')
    repair_code_review_eval_codellama_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'repair') / Path('codellama') / Path('repair_code_review_eval_codellama.jsonl')

    dataset = load_dataset('json', split='train', data_files=str(check_code_review_eval_codellama_result_path))
    dataset.cleanup_cache_files()
    print(dataset)

    dataset = dataset.map(lambda example: repair_diff_tag(example, invalid_positive_diff_tag_code_uids,
                                                          invalid_negative_diff_tag_code_uids))
    print(dataset)

    dataset.to_json(repair_code_review_eval_codellama_result_path, lines=True)


def repair_code_test_data_palm():
    check_code_test_data_palm_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'check') / Path('palm') / Path('check_code_test_data_palm.jsonl')
    repair_code_test_data_palm_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'repair') / Path('palm') / Path('repair_code_test_data_palm.jsonl')

    mapping = {
        'e40e73c16a57fbbfbcb77982030e15f0': "[{'input': '0 0 0 0 9\\n0 0 0 0 0\\n0 0 0 0 0\\n0 0 0 0 0\\n7 0 0 0 0', 'output': ['32']}, {'input': '0 43 21 18 2\\n3 0 21 11 65\\n5 2 0 1 4\\n54 62 12 0 99\\n87 64 81 33 0', 'output': ['620']}, {'input': '0 0 0 0 0\\n0 0 0 0 0\\n0 0 0 0 0\\n0 0 0 0 0\\n0 0 0 0 0', 'output': ['0']}, {'input': '1 2 3 4 5\\n1 2 3 4 5\\n1 2 3 4 5\\n1 2 3 4 5\\n1 2 3 4 5', 'output': ['100']}, {'input': '100 100 100 100 100\\n100 100 100 100 100\\n100 100 100 100 100\\n100 100 100 100 100\\n100 100 100 100 100', 'output': ['5000']}]",
        'f019491af76df7f8d3b735e99349717a': "[{'input': '4 2 100000007', 'output': ['14']}, {'input': '5 2 100000007', 'output': ['28']}, {'input': '6 2 100000007', 'output': ['56']}, {'input': '7 2 100000007', 'output': ['104']}, {'input': '8 2 100000007', 'output': ['184']}]",
        'c8e38c24e3992f4ddcb3710a098b74ea': "[{'input': '2 3\\n1 1', 'output': ['1 6']}, {'input': '3 2\\n0 0', 'output': ['1 3']}, {'input': '1 10\\n5 3', 'output': ['5 5']}, {'input': '1 10\\n1 1', 'output': ['1 1']}, {'input': '1 10\\n10 1', 'output': ['1 10']}]",
        '68be7913d7ce93a0cdca60cbae812e89': "[{'input': 'xx..\\n.oo.\\nx...\\noox.', 'output': ['YES']}, {'input': 'x.ox\\nox..\\nx.o.\\noo.x', 'output': ['NO']}, {'input': 'x..x\\n..oo\\no...\\nx.xo', 'output': ['YES']}, {'input': 'o.x.\\no...\\n.x..\\nooxx', 'output': ['NO']}, {'input': '..x.\\n..x.\\n..x.\\n..x.', 'output': ['NO']}]",
        'f149d8d76da2f6c77345920df1f528d8': "[{'input': '1 1 6 1\\n1 0 6 0\\n6 0 6 1\\n1 1 1 0', 'output': ['YES']}, {'input': '0 0 0 3\\n2 0 0 0\\n2 2 2 0\\n0 2 2 2', 'output': ['NO']}, {'input': '1 1 2 2\\n2 2 3 3\\n3 3 4 4\\n4 4 1 1', 'output': ['YES']}, {'input': '1 1 2 2\\n2 2 3 3\\n3 3 4 4\\n4 4 5 5', 'output': ['NO']}, {'input': '1 1 2 2\\n2 2 3 3\\n3 3 4 4\\n4 4 1 1', 'output': ['YES']}]",
        '4c82f84bb04eecfb71da878b973f0c1d': "[{'input': '0 0 0 0 9\\n0 0 0 0 0\\n0 0 0 0 0\\n0 0 0 0 0\\n7 0 0 0 0', 'output': ['32']}, {'input': '0 43 21 18 2\\n3 0 21 11 65\\n5 2 0 1 4\\n54 62 12 0 99\\n87 64 81 33 0', 'output': ['620']}, {'input': '0 0 0 0 0\\n0 0 0 0 0\\n0 0 0 0 0\\n0 0 0 0 0\\n0 0 0 0 0', 'output': ['0']}, {'input': '1 2 3 4 5\\n1 2 3 4 5\\n1 2 3 4 5\\n1 2 3 4 5\\n1 2 3 4 5', 'output': ['105']}, {'input': '1 2 3 4 5\\n5 4 3 2 1\\n1 2 3 4 5\\n5 4 3 2 1\\n1 2 3 4 5', 'output': ['105']}]",
        'bcc080b096cf7187cfdfd03f93787d78': "[{'input': '0 0 6 0 6 6 0 6\\n1 3 3 5 5 3 3 1', 'output': ['YES']}, {'input': '0 0 6 0 6 6 0 6\\n7 3 9 5 11 3 9 1', 'output': ['NO']}, {'input': '6 0 6 6 0 6 0 0\\n7 4 4 7 7 10 10 7', 'output': ['YES']}, {'input': '0 0 6 0 6 6 0 6\\n1 3 3 5 5 3 3 1', 'output': ['YES']}, {'input': '0 0 6 0 6 6 0 6\\n7 3 9 5 11 3 9 1', 'output': ['NO']}]",
        '8790a10c04e66b0a6a29b482288744de': "[{'input': '1 0 0 1\\n0 1 0 0\\n0 0 1 0\\n0 0 0 1', 'output': ['YES']}, {'input': '0 1 1 0\\n1 0 1 0\\n1 1 0 0\\n0 0 0 1', 'output': ['NO']}, {'input': '1 0 0 0\\n0 0 0 1\\n0 0 0 0\\n1 0 1 0', 'output': ['NO']}, {'input': '1 0 0 0\\n0 0 0 1\\n0 0 0 0\\n1 0 1 0', 'output': ['NO']}, {'input': '1 0 0 0\\n0 0 0 1\\n0 0 0 0\\n1 0 1 0', 'output': ['NO']}]",
        '1238f451970ae68c785036cde7ad10a5': "[{'input': '1 1', 'output': ['1 0']}, {'input': '2 3', 'output': ['2 0']}, {'input': '7 3', 'output': ['3 2']}, {'input': '10 10', 'output': ['5 0']}, {'input': '1 10', 'output': ['1 5']}]"
    }

    dataset = load_dataset('json', split='train', data_files=str(check_code_test_data_palm_result_path))
    dataset.cleanup_cache_files()
    print(dataset)

    dataset = dataset.map(lambda example: repair_hidden_unit_tests(example, mapping))
    print(dataset)

    dataset.to_json(repair_code_test_data_palm_result_path, lines=True)


def repair_code_test_data_starcoder():
    code_test_data_starcoder_log_path = Path(__file__).parent.parent / Path('logs') / Path('starcoder') / Path(
        'code_test_data_starcoder.log')
    with open(code_test_data_starcoder_log_path, mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        invalid_code_uids = [
            'bc06756d882b013565e396654fa6aaa9', '57ea84cc35e8283d0afea7bee5d3b93f',
            '6c7724a49b94ab93476ffe64e7a913be', 'ef40b724e511308ccea6397eaf03087d',
            '9273cd3454997f0b8121b40a8a00e7b4', 'd8354977f745cc62119a6c5a6feb579e',
            '2d711d45f1108dfb3303465c99137e62', 'ab7155132d0868c2688c3bca40a5ec9b',
            '5aae891caa5a564ec3de3f155b951614', '451f1f98e7dccb514b975b54667c2063',
            'a492909277fb2d24dea9ae7e460fd107', '3d98f298e530d472507af154e93d17c4',
            '3467947eb40378f25dab8d24d096608d', '1ee207ebdacfd721e0498e96d6c876de',
            '5fa7123cc797685036cebdd8e1fa9e49', 'c1091ef2cae42e6f8105ae9b809d9a2d',
            '5f6435b64f9a140c0c3db8739709d749', '9a271369b5ff091a0774831dd472b695',
            '15725813c7099eaa9e96d5898472bb70', '96307dff1adc6be404b8f6f5d5faa774',
            'ace9f6f64e662df70b9e0f436cf99d94', '0e5891b91b4791e582ef79fc3bf9a7a8',
            'ff77a7d647936d5f41da8fe93f71e948', '9557af7f6c0ea2ff51c70a2f5223221a',
            '7df1e10e7caf8e5bb6ad5838f3242f78', 'b00ee8d6b0774ac21a19e733ecf8120a',
            'aa3df742761205ac9901317c2c20bc5b', '6dfff265b3c6bd83bd9ea151f4eeca58',
            '47c2647bd343c3a5fb00208e095c8f0f', '49c66c9c938a33fcbde3599f2813aa8f',
            '2d9121405142039fcad3a90b70bf5304', 'dd7efa70220655828d50742116517ab1',
            'be920453fabb02e87093ed0e72972756', '590b7d2d7b94f3e78c85de87ce3a3db3',
            'fc001df465241129a674a61803f45c23', 'de5e08b66eb31d7f6acd740e6bcead6e',
            'd269e020ed015cd2345122de6f5dc57b', '214c50ce4aee708818c9fc83db32749b',
            '553bceb132fe79a128b299bc9e09118a', '1f217de1a9d57fdd6c523b5eb63cc85d',
            'c680f47b26ba2da78b2576cf0491b7df', 'b1b62f2ec77daa266df84d0fcaf895c0',
            'a7c8faaea19ea8bdf4482ed8c4acf808', '15446088bda594f735f81b1eb62a7e39',
            '6b85dd45fd3c04780a7d4eaaab6c14b8', 'c535a398d0d027358e55b75a7f3a5268',
            '7776484008ca3354d1d955d4c769f254', '60a7758c7fb2a0007efafd350013730b',
            'eefbabc60f1ffd99500f2466d5bbeea3', '9d375e775c9a50ce6f2f3fdc346eacdf',
            'd94c747071f8c8ba9a513858cbc990a7', '417a033e3f4f158962bd36111890a54a',
            '2584514af63eea42716915086f4ddff8', '92e63cdd0c37a1427f166c6d629130fd',
            'aae6408f737c7f9c77b6e86b32f2b2d0', 'b8d69258742520bfbb90459050c614c1',
            '5762822697e55f4a7c9955d5d08f326b', '03e03e151d4cf4ec2993c9a5e86acb36',
            'bd4288e58ffba130c210bec4d9f29a5e', '68be7913d7ce93a0cdca60cbae812e89',
            '4aa7bbc193aefdfc45b9c0d3829d39bf', 'a8ffdfa991647b0bfd8f37e05f1413ad',
            'b29daf920b6253282a6bc50a179553fa', 'db45c4213b4b97c426871fe91634fae0',
            '6831a065e02f0620266d90b7fe43588d', 'e13e202882a43f15406df4adf88b6686',
            'd2a4193dca89bfa582b31108d84838fe', 'b7cb47631cb0d893e0a5e8eb04107d1b',
            'bce1b585a357e9b50ee669d6fd610b94', '45b8746af8428f1f966ab97a478542ff',
            '80db3d064f45537bd7563130c38d4494', '82e24be68fd0c717c3c720b2851c3297',
            '5e64f8683dec9cfa6f6e6619a6895030', '1e893aa51d1c23c5787c90d8a946c7bb',
            'c7e0ec7560756159e9aaf42692f58f00', '36dd77c492daaa293e7cfbdd4193d67e',
            '4c82f84bb04eecfb71da878b973f0c1d', '28edecddfde5fe488a99740254e4b6bc',
            '74ffa3cbcb44042fabeac82c71c6d750', '727a5daf7d4e53929fba30c9fbea92f3',
            '135bec62ee09369bdbdfa6e2bd026117', 'aa8a180c0397e093163d1aaa66efa1fb',
            'bcc080b096cf7187cfdfd03f93787d78', 'c77115e976d5caae929be12c1e7e17e6',
            'efd03436dc3e3f98c37c9bc6d8fd4c35', 'd93eb3e0bdf2a901ba323dfb12b50002',
            '7e9453a0ace44aa00204661c417d7314', '3d0625b6d77bbb587f117badc24e0e73',
            'ebc57fb28654ca1bcb3a0a4ae117cf5b', '4af23f0ff02c7d3b490efb7c019dd1af',
            'a977cd12419716342e11683009a73d89', 'fee9375acf5a84794c8d5e2a7a1fa945',
            '7a75b9f867c3f1f974048c01133ed3e6', 'd7b49e635bf5a04ea72cb0a640b8135d',
            'c3f00d09b4707b71ec10f761e41328ea', 'fdb9f68abb2c3019dcbf9ee22981c4b9',
            '989aa3ee0033d5adac0fc9cbb0199065', '7572ba456fcd2f84062bae73e0ed31f7',
            '29bd8cc7a5eef1c20989eb05c7d3692d', 'f6c45715cdf30cfe4a69c4f286ed1e4e',
            '5810cb185e940b3920d69c59b78f90a1', '72f78d9ae9f025807e729b822077ace2',
            '6f2f01bc8e3eb2456c1a859c8ef6e3d3', '3f6a00af9736c8661d0d59781103c919',
            'e8f624d23e36b837e350d21df82c289f', '4fa49fbef2bc1a3b13d419c7ffeabf4a',
            '1232c75961b5aefb45139fa03a81cbe9', '64a8de51f0cd1a62244b393fad5dd07d',
            '3d9b561821b9d49b6ba48d5bbb08b2e1', '95cb9c03cdaa1c1fb1e06a1d9ceae682',
            '075c28eaa1bdc66e9693240308b15533', 'f6651d27030633c7d0250ee0f1525dd9',
            'f653a66480279a05542cc29804c669ee', 'ca16485ad2473309ec7f95e5ea164aa4',
            '5d47a35580bfefd1f36a6d946932b48b', '7eec0f17c590fb5fd85d790a34f8d98a',
            '502311826264200a481ebbe4cdbe20a3', 'a71a01171806a337eb6b0f1c9f3268f4',
            'd5ec3e39a7da50bf1ae1f50bd39dbf68', 'a20312e80bf4ce08b5c1c0917d811db1',
            'c7a2a21610b7bbd676b6c6db3f6c6cb0', 'b9336adcd50f1b3edf352a1219c9659b',
            '015ea30b7d0e1b1543b3e8ccc2c19604', 'd22f3f53434188ee8982353ac8c5f44b',
            '1238f451970ae68c785036cde7ad10a5', '59818fd9dcb02014b1f1ecbc70fab20e',
            '3d0b2703ee180f2eee303e4da431396b', '6f9436a329d5d3a638fb45e8375716e7',
            '25fa9c110cf15920ffad234fdbbdd06b', '20c768b19dd414a5b3f4e10cbe7b2a4e',
            '55bb7e5a85fa02f0c1918825bb463f23', 'ffcf12e402bef8d171f551c12e5bc85e',
            '7b509396aeaeb6bb60154fd40d60ccae', '759fe1bf495cee74e37b43688ae3923a',
            'b74d1efc8dc7c743f39b0603ef78ded1', 'faa620d5a241e146059c5ea1bae3a2a9',
            'c1f9c3691e5a36d411545872d8b51544', 'd62c78efb9dc6541e7ef583be9972947',
            'bba9c820b0f2b0a5076b015644d66f4a', '673ab16d6e3c18c72916134d40852e99',
            '7b81a4801fc6c454082998b70a435eae', '55019f26f970076f44fd5b6f9d161b40',
            '654b366320659b02d312390dbcc667c2', 'bd0cd59e2175057a315437451a1cd34d',
            'c3fd538eb6bdebb3dbb84f04b054ff14', '889715f9788c64eeaa5df9c316caa65b',
            'd2ef760ef34e8097365e8dc2adae51b8', 'e75dc50c8f545d9038967f6c8af8e8ec',
            'dd66e205e4ba8e2c7ada0b83a33f32c7', 'd6f0a47d0c65c3153e295eb91252bcdd',
            '7070a2585b613516b14a7f9bdba8385b', '0c1f0907f688cfeaf6f5f0c1fdb45149',
            '6641d80a5bda4ca0c4e46aa2da489db9', '431125b3842ce267420e6a80d5fe0f58',
            'e30a8a57dd6baed05c58727c914bbf11', '7839b462979f317f3f02850efbf73dbb']
        not_matched_code_uids = []
        mapping = {}
        for i in range(len(lines)):
            if 'code uid:' in lines[i]:
                code_uid = lines[i].split('code uid:')[-1].strip()
                if code_uid in invalid_code_uids:
                    response_content = []
                    capture = False
                    for j in range(i, len(lines)):
                        if 'response:' in lines[j]:
                            capture = True
                            lines[j] = lines[j].split('response:')[-1].strip()
                        if 'output tokens:' in lines[j]:
                            invalid_diff_tag_response = '\n'.join(response_content).strip().lower()
                            hidden_unit_tests = []
                            pattern_1 = r'```\s*{\s*"input":\s*"([^"]+)",\s*"output":\s*"([^"]+)"\s*}\s*```'
                            matches_1 = re.findall(pattern_1, invalid_diff_tag_response, re.DOTALL)
                            if len(matches_1) == 0:
                                pattern_2 = r'input:\s*([\d\s]+)\s*output:\s*(\d+)'
                                matches_2 = re.findall(pattern_2, invalid_diff_tag_response, re.DOTALL)
                                if len(matches_2) == 0:
                                    pattern_3 = r'"input"\s*:\s*"([^"]+)"\s*,\s*"output"\s*:\s*"([^"]+)"'
                                    matches_3 = re.findall(pattern_3, invalid_diff_tag_response, re.DOTALL)
                                    if len(matches_3) == 0:
                                        pattern_4 = r'input: "(.*?)"\noutput: "(.*?)"'
                                        matches_4 = re.findall(pattern_4, invalid_diff_tag_response, re.DOTALL)
                                        if len(matches_4) == 0:
                                            pattern_5 = r'input:\n```\n(.*?)\n```\noutput:\n```\n(.*?)\n```'
                                            matches_5 = re.findall(pattern_5, invalid_diff_tag_response, re.DOTALL)
                                            if len(matches_5) == 0:
                                                print(f'Not matched:', code_uid)
                                                not_matched_code_uids.append(code_uid)
                                            else:
                                                hidden_unit_tests = [
                                                    {'input': input_str.strip(), 'output': [output_str.strip()]}
                                                    for input_str, output_str in matches_5]
                                        else:
                                            hidden_unit_tests = [
                                                {'input': input_str.strip(), 'output': [output_str.strip()]}
                                                for input_str, output_str in matches_4]

                                    else:
                                        hidden_unit_tests = [
                                            {'input': input_str.strip(), 'output': [output_str.strip()]} for
                                            input_str, output_str in matches_3]
                                else:
                                    hidden_unit_tests = [{'input': input_str.strip(), 'output': [output_str.strip()]}
                                                         for input_str, output_str in matches_2]
                            else:
                                hidden_unit_tests = [{'input': input_str, 'output': [output_str.strip()]} for
                                                     input_str, output_str in matches_1]
                            if len(hidden_unit_tests) < 5:
                                print(f'Not enough hidden unit tests [{len(hidden_unit_tests)}/5]:', code_uid)
                                for _ in range(5 - len(hidden_unit_tests)):
                                    hidden_unit_tests.append({'input': '', 'output': ['']})
                            elif len(hidden_unit_tests) > 5:
                                hidden_unit_tests = hidden_unit_tests[:5]

                            mapping[code_uid] = str(hidden_unit_tests)

                            break
                        if capture:
                            response_content.append(lines[j].strip())

        print(not_matched_code_uids)
        mapping[
            'ab7155132d0868c2688c3bca40a5ec9b'] = "[{'input': '4\\n1 3\\n2 3\\n1 4\\n5 3', 'output': ['WIN']}, {'input': '5\\n1 2\\n2 3\\n3 4\\n4 5\\n5 1', 'output': ['FAIL']}, {'input': '4\\n1 3\\n2 4\\n1 4\\n5 3', 'output': ['FAIL']}, {'input': '4\\n1 3\\n2 3\\n1 5\\n5 3', 'output': ['WIN']}, {'input': '4\\n1 3\\n2 3\\n1 4\\n3 5', 'output': ['FAIL']}]"
        mapping[
            '6dfff265b3c6bd83bd9ea151f4eeca58'] = "[{'input': '1 5', 'output': ['30']}, {'input': '2 3', 'output': ['25']}, {'input': '3 2', 'output': ['10']}, {'input': '4 1', 'output': ['15']}, {'input': '5 1', 'output': ['20']}]"
        mapping[
            '15446088bda594f735f81b1eb62a7e39'] = "[{'input': '1 3', 'output': ['7']}, {'input': '2 2', 'output': ['9']}, {'input': '3 3', 'output': ['27']}, {'input': '4 4', 'output': ['81']}, {'input': '', 'output': ['']}]"
        mapping[
            'd94c747071f8c8ba9a513858cbc990a7'] = "[{'input': '.XX\\n...\\n.XX', 'output': ['YES']}, {'input': 'X.X\\nX..\\n...', 'output': ['NO']}, {'input': 'XX.\\n...\\nX.X', 'output': ['YES']}, {'input': 'X..\\n.X.\\nX.X', 'output': ['NO']}, {'input': 'X.X\\nX..\\n.XX', 'output': ['YES']}]"
        mapping[
            '92e63cdd0c37a1427f166c6d629130fd'] = "[{'input': '4', 'output': ['28 41']}, {'input': '7', 'output': ['47 65']}, {'input': '12', 'output': ['48 105']}, {'input': '100', 'output': ['4950 5050']}, {'input': '1000', 'output': ['499500 500500']}]"
        mapping[
            '4aa7bbc193aefdfc45b9c0d3829d39bf'] = "[{'input': '2 5 4 6 1 3 6 2 5 5 1 2 3 5 3 1 1 2 4 6 6 4 3 4', 'output': ['NO']}, {'input': '5 3 5 3 2 5 2 5 6 2 6 2 4 4 4 4 1 1 1 1 6 3 6 3', 'output': ['YES']}, {'input': '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1', 'output': ['YES']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]"
        mapping[
            'e13e202882a43f15406df4adf88b6686'] = "[{'input': '3 5', 'output': ['1']}, {'input': '6 66', 'output': ['7']}, {'input': '2 2', 'output': ['2']}, {'input': '1 1', 'output': ['0']}, {'input': '10 100', 'output': ['45']}]"
        mapping[
            '1e893aa51d1c23c5787c90d8a946c7bb'] = "[{'input': '7\\nABACABA', 'output': ['BA']}, {'input': '5\\nZZZAA', 'output': ['ZZ']}, {'input': '6\\nABACABB', 'output': ['BA']}, {'input': '6\\nABACABA', 'output': ['BA']}, {'input': '7\\nABACABBBB', 'output': ['BBB']}]"
        mapping[
            'c7e0ec7560756159e9aaf42692f58f00'] = "[{'input': '10 2\\n3 5\\n11 13', 'output': ['Full\\n2']}, {'input': '10 3\\n3 5\\n9 10\\n11 13', 'output': ['Full\\n1']}, {'input': '20 1\\n3 19', 'output': ['Hungry']}, {'input': '10 2\\n3 1\\n11 13', 'output': ['Hungry']}, {'input': '10 2\\n3 5\\n1 2', 'output': ['Hungry']}]"
        mapping[
            '74ffa3cbcb44042fabeac82c71c6d750'] = "[{'input': '5 5 2', 'output': ['First']}, {'input': '6 7 4', 'output': ['Second']}, {'input': '1 1 1', 'output': ['First']}, {'input': '10 10 5', 'output': ['Second']}, {'input': '100 100 50', 'output': ['First']}]"
        mapping[
            'ebc57fb28654ca1bcb3a0a4ae117cf5b'] = "[{'input': '3 1\\n-1 0 1', 'output': ['6']}, {'input': '2 1\\n1 0', 'output': ['1']}, {'input': '1 1\\n-1', 'output': ['2']}, {'input': '4 0\\n-1 -1 -1 1', 'output': ['15']}, {'input': '5 1\\n-1 -1 -1 -1 1', 'output': ['113']}]"
        mapping[
            'a977cd12419716342e11683009a73d89'] = "[{'input': '4 6', 'output': ['2']}, {'input': '9 7', 'output': ['6']}, {'input': '1 1', 'output': ['2']}, {'input': '10 10', 'output': ['55']}, {'input': '', 'output': ['']}]"
        mapping[
            'd7b49e635bf5a04ea72cb0a640b8135d'] = "[{'input': 'AS\\n2H 4C TH JH AD', 'output': ['YES']}, {'input': '2H\\n3D 4C AC KD AS', 'output': ['NO']}, {'input': '4D\\nAS AC AD AH 5H', 'output': ['YES']}, {'input': 'TH\\n2S 3C 4H 5D 6C', 'output': ['NO']}, {'input': '9H\\n2S 3C 4H 5D 6C', 'output': ['YES']}]"
        mapping[
            '5810cb185e940b3920d69c59b78f90a1'] = "[{'input': 'X.X\\n.X.\\nX.X', 'output': ['second']}, {'input': 'X..\\nO.O\\n.X.', 'output': ['illegal']}, {'input': 'X.O\\nO.X\\nX.X', 'output': ['the first player won']}, {'input': 'X.O\\nO.X\\nX..', 'output': ['draw']}, {'input': '.X.\\n.O.\\nX.X', 'output': ['the second player won']}]"
        mapping[
            '4fa49fbef2bc1a3b13d419c7ffeabf4a'] = "[{'input': '4 4 0\\n2 1 2', 'output': ['Yes']}, {'input': '5 6 1\\n2 7 2', 'output': ['No']}, {'input': '3 3 3\\n2 2 2', 'output': ['Yes']}, {'input': '3 3 2\\n2 2 2', 'output': ['No']}, {'input': '4 4 1\\n2 1 2', 'output': ['Yes']}]"
        mapping[
            '502311826264200a481ebbe4cdbe20a3'] = "[{'input': '4 2\\naabb', 'output': ['YES']}, {'input': '6 3\\naacaab', 'output': ['NO']}, {'input': '4 2\\nabba', 'output': ['YES']}, {'input': '5 3\\naabbcc', 'output': ['YES']}, {'input': '6 3\\nabacaba', 'output': ['NO']}]"
        mapping[
            'c7a2a21610b7bbd676b6c6db3f6c6cb0'] = "[{'input': 'alice smith', 'output': ['alicea']}, {'input': 'bob jones', 'output': ['bobby']}, {'input': 'charlie brown', 'output': ['charlieb']}, {'input': 'dennis the menace', 'output': ['dennisthemenace']}, {'input': 'eddie izzard', 'output': ['eddieizzard']}]"
        mapping[
            'b9336adcd50f1b3edf352a1219c9659b'] = "[{'input': '7\\n.j......', 'output': ['jolteon']}, {'input': '7\\n...feon', 'output': ['leafeon']}, {'input': '7\\n.l.r.o.', 'output': ['flareon']}, {'input': '6\\n.j.o.n', 'output': ['vaporeon']}, {'input': '6\\n.j.o.n.', 'output': ['umbreon']}]"
        mapping[
            '3d0b2703ee180f2eee303e4da431396b'] = "[{'input': '3 3\\n0 0\\n2 0\\n3 1\\n-2 1\\n0 3\\n2 2', 'output': ['Yes']}, {'input': '2 1\\n1 0\\n2 2\\n3 1', 'output': ['No']}, {'input': '4 4\\n0 0\\n1 1\\n2 2\\n3 3', 'output': ['Yes']}, {'input': '4 5\\n0 0\\n1 1\\n2 2\\n3 3\\n-1 -1\\n-2 -2\\n-3 -3\\n-4 -4', 'output': ['No']}, {'input': '5 5\\n0 0\\n1 1\\n2 2\\n3 3\\n4 4\\n-1 -1\\n-2 -2\\n-3 -3\\n-4 -4\\n-5 -5', 'output': ['Yes']}]"
        mapping[
            '6f9436a329d5d3a638fb45e8375716e7'] = "[{'input': '5 1 2 1 2', 'output': ['First']}, {'input': '3 3 1 1 1', 'output': ['Second']}, {'input': '4 5 3 1 5', 'output': ['Friendship']}, {'input': '10 1 10 1 1', 'output': ['First']}, {'input': '10 10 1 1 1', 'output': ['Second']}]"
        mapping[
            '25fa9c110cf15920ffad234fdbbdd06b'] = "[{'input': '0 1 1 1 1 0', 'output': ['Yes']}, {'input': '1 1 0 0 1000 1000', 'output': ['No']}, {'input': '1 2 3 4 5 6', 'output': ['Yes']}, {'input': '1 2 3 4 5 1', 'output': ['No']}, {'input': '1 1 1 1 1 1', 'output': ['Yes']}]"
        mapping[
            '55bb7e5a85fa02f0c1918825bb463f23'] = "[{'input': '3 10 3 3', 'output': ['2']}, {'input': '3 10 1 3', 'output': ['3']}, {'input': '100 100 1 1000', 'output': ['1']}, {'input': '100 100 2 1000', 'output': ['2']}, {'input': '100 100 3 1000', 'output': ['3']}]"
        mapping[
            'ffcf12e402bef8d171f551c12e5bc85e'] = "[{'input': '2\\nRB', 'output': ['G']}, {'input': '3\\nGRG', 'output': ['BR']}, {'input': '5\\nBBBBB', 'output': ['B']}, {'input': '4\\nRRRR', 'output': ['RRR']}, {'input': '6\\nBBRRRBB', 'output': ['BBB']}]"
        mapping[
            '7b509396aeaeb6bb60154fd40d60ccae'] = "[{'input': '3 3 3\\n1 1 1\\n2 2 3\\n3 3 2', 'output': ['14']}, {'input': '4 10 2\\n2 3 8\\n3 4 7', 'output': ['262']}, {'input': '3 3 3\\n1 1 1\\n2 2 2\\n3 3 3', 'output': ['18']}, {'input': '3 3 3\\n1 1 1\\n2 2 3\\n3 3 4', 'output': ['12']}, {'input': '3 3 3\\n1 1 1\\n2 2 3\\n4 4 4', 'output': ['0']}]"
        mapping[
            'b74d1efc8dc7c743f39b0603ef78ded1'] = "[{'input': 'WUBWUBABCWUB', 'output': ['ABC']}, {'input': 'WUBWEWUBAREWUBWUBTHEWUBCHAMPIONSWUBMYWUBFRIENDWUB', 'output': ['WE ARE THE CHAMPIONS MY FRIEND']}, {'input': 'WUBWUB', 'output': ['WUB WUB']}, {'input': 'WUBWUBWUBWUB', 'output': ['WUB WUB WUB WUB']}, {'input': 'WUB', 'output': ['WUB']}]"
        mapping[
            '654b366320659b02d312390dbcc667c2'] = "[{'input': '5 1 4 4 2 1', 'output': ['YES']}, {'input': '1 6 6 2 1 1', 'output': ['NO>']}, {'input': '4 1 7 4 1 2', 'output': ['YES']}, {'input': '10 11 10 2 1 1', 'output': ['NO>']}, {'input': '1 2 3 4 5 6', 'output': ['YES']}]"
        mapping[
            '889715f9788c64eeaa5df9c316caa65b'] = "[{'input': '4 6\\n10 12 10 7 5 22', 'output': ['5']}, {'input': '5 6\\n10 12 10 7 5 22', 'output': ['1']}, {'input': '6 6\\n10 12 10 7 5 22', 'output': ['0']}, {'input': '4 5\\n10 12 10 7 5', 'output': ['1']}, {'input': '5 5\\n10 12 10 7 5', 'output': ['0']}]"
        mapping[
            'd2ef760ef34e8097365e8dc2adae51b8'] = "[{'input': '2 1 2 2', 'output': ['Polycarp']}, {'input': '4 7 7 4', 'output': ['Vasiliy']}, {'input': '1 1 1 1', 'output': ['Polycarp']}, {'input': '0 0 1 1', 'output': ['Vasiliy']}, {'input': '9 9 8 8', 'output': ['Draw']}]"
        mapping[
            'd6f0a47d0c65c3153e295eb91252bcdd'] = "[{'input': '4\\n3 2 1 2', 'output': ['1 2 2 3']}, {'input': '3\\n2 3 8', 'output': ['2 3 8']}, {'input': '4\\n4 3 2 1', 'output': ['1 2 3 4']}, {'input': '4\\n1 2 3 4', 'output': ['4 3 2 1']}, {'input': '4\\n3 3 3 3', 'output': ['3 3 3 3']}]"
        mapping[
            '7839b462979f317f3f02850efbf73dbb'] = "[{'input': '3 30\\n2 2 1', 'output': ['5']}, {'input': '3 20\\n2 1 1', 'output': ['-1']}, {'input': '4 30\\n2 2 3 3', 'output': ['6']}, {'input': '4 30\\n2 2 2 4', 'output': ['7']}, {'input': '4 30\\n3 3 3 3', 'output': ['8']}]"

        print(mapping)

    check_code_test_data_starcoder_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'check') / Path('starcoder') / Path('check_code_test_data_starcoder.jsonl')
    repair_code_test_data_starcoder_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'repair') / Path('starcoder') / Path('repair_code_test_data_starcoder.jsonl')

    dataset = load_dataset('json', split='train', data_files=str(check_code_test_data_starcoder_result_path))
    dataset.cleanup_cache_files()
    print(dataset)

    dataset = dataset.map(lambda example: repair_hidden_unit_tests(example, mapping))
    print(dataset)

    dataset.to_json(repair_code_test_data_starcoder_result_path, lines=True)


def repair_code_review_eval_starcoder():
    code_review_eval_starcoder_log_path = Path(__file__).parent.parent / Path('logs') / Path('starcoder') / Path(
        'code_review_eval_starcoder.log')
    with open(code_review_eval_starcoder_log_path, mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        invalid_diff_tag_code_uids = []  # diff_tag = 2
        invalid_positive_diff_tag_code_uids = []  # diff_tag = 1
        invalid_negative_diff_tag_code_uids = []  # diff_tag = 0
        for i in range(len(lines)):
            diff_tag = None
            if 'code uid:' in lines[i]:
                code_uid = lines[i].split('code uid:')[-1].strip()
                for j in range(i, len(lines)):
                    if 'diff_tag:' in lines[j]:
                        diff_tag = lines[j].split('diff_tag:')[-1].strip()
                        break
                if diff_tag == '2':
                    invalid_diff_tag_code_uids.append(code_uid)
                    response_content = []
                    capture = False
                    for j in range(i, len(lines)):
                        if 'response:' in lines[j]:
                            capture = True
                            lines[j] = lines[j].split('response:')[-1].strip()
                        if 'output tokens:' in lines[j]:
                            invalid_diff_tag_response = '\n'.join(response_content).strip().lower()

                            good_content_1 = 'good quality'
                            good_content_2 = 'the code change looks good'
                            good_content_3 = '0'
                            good_content_4 = '0'
                            good_content_5 = '0'
                            good_content_6 = '0'
                            good_content_7 = '0'
                            good_content_8 = '0'

                            poor_content_1 = 'low quality'
                            poor_content_2 = 'poor quality'
                            poor_content_3 = 'the quality of the code change appears to be low'
                            poor_content_4 = 'the code should be reviewed'
                            poor_content_5 = 'bug'
                            poor_content_6 = 'requires a review comment'

                            if good_content_1 in invalid_diff_tag_response \
                                    or good_content_2 in invalid_diff_tag_response \
                                    or good_content_3 in invalid_diff_tag_response \
                                    or good_content_4 in invalid_diff_tag_response \
                                    or good_content_5 in invalid_diff_tag_response \
                                    or good_content_6 in invalid_diff_tag_response \
                                    or good_content_7 in invalid_diff_tag_response \
                                    or good_content_8 in invalid_diff_tag_response:
                                invalid_negative_diff_tag_code_uids.append(code_uid)
                            elif poor_content_1 in invalid_diff_tag_response \
                                    or poor_content_2 in invalid_diff_tag_response \
                                    or poor_content_3 in invalid_diff_tag_response \
                                    or poor_content_4 in invalid_diff_tag_response \
                                    or poor_content_5 in invalid_diff_tag_response \
                                    or poor_content_6 in invalid_diff_tag_response:
                                invalid_positive_diff_tag_code_uids.append(code_uid)
                            else:
                                print(code_uid)
                                print(invalid_diff_tag_response)
                            break
                        if capture:
                            response_content.append(lines[j].strip())
        print(len(invalid_diff_tag_code_uids))  # 144
        print(len(invalid_positive_diff_tag_code_uids))  # 32
        print(len(invalid_negative_diff_tag_code_uids))  # 108
        print(len(invalid_positive_diff_tag_code_uids) + len(invalid_negative_diff_tag_code_uids))  # 140 / 144
        # 2
        invalid_positive_diff_tag_code_uids.append('9c830622bbdc4f06b9828506fa5c3fc3')
        invalid_positive_diff_tag_code_uids.append('ac0cd40c64e84b49b227d5ff6743c491')

    check_code_review_eval_starcoder_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'check') / Path('starcoder') / Path('check_code_review_eval_starcoder.jsonl')
    repair_code_review_eval_starcoder_result_path = Path(__file__).parent.parent / Path('results') / Path(
        'repair') / Path('starcoder') / Path('repair_code_review_eval_starcoder.jsonl')

    dataset = load_dataset('json', split='train', data_files=str(check_code_review_eval_starcoder_result_path))
    dataset.cleanup_cache_files()
    print(dataset)

    dataset = dataset.map(lambda example: repair_diff_tag(example, invalid_positive_diff_tag_code_uids,
                                                          invalid_negative_diff_tag_code_uids))
    print(dataset)

    dataset.to_json(repair_code_review_eval_starcoder_result_path, lines=True)


def main():
    # repair_code_review_eval_wizardcoder()
    # repair_code_test_data_wizardcoder()
    # repair_code_test_data_vicuna()
    # repair_code_test_data_gpt4()
    # repair_code_smell_eval_gpt4()
    # repair_code_test_data_gpt3()
    # repair_code_smell_eval_gpt3()
    # repair_code_review_eval_gpt3()
    # repair_code_test_data_llama2()
    # repair_code_test_data_codellama()
    # repair_code_review_eval_codellama()
    # repair_code_test_data_palm()
    # repair_code_test_data_starcoder()
    # repair_code_review_eval_starcoder()
    pass


if __name__ == '__main__':
    main()
    # python scripts/repair_results.py
