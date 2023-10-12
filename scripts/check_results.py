from pathlib import Path
from datasets import load_dataset


def check_smell(example):
    code_uid = example['code_uid']
    smell = example['smell']
    if smell not in expected_smells:
        print('Unexpected code smell value occurred:', code_uid)
        example['smell'] = ''

    return example


def check_diff_tag(example):
    code_uid = example['code_uid']
    diff_tag = example['diff_tag']
    if diff_tag not in expected_diff_tags:
        print('Unexpected diff tag value occurred:', code_uid)
        example['diff_tag'] = 2

    return example


def check_review_comment(example):
    code_uid = example['code_uid']
    review_comment = example['review_comment']
    if not isinstance(review_comment, str):
        print('Unexpected review comment value occurred:', code_uid)
        example['review_comment'] = ''

    return example


def check_hidden_unit_tests(example):
    code_uid = example['code_uid']
    hidden_unit_tests = eval(example['hidden_unit_tests'])
    num_hidden_unit_tests = len(hidden_unit_tests)
    if not isinstance(hidden_unit_tests, list):
        print('Unexpected hidden unit tests value occurred:', code_uid)
        example[
            'hidden_unit_tests'] = "[{'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}, {'input': '', 'output': ['']}]"
    if num_hidden_unit_tests < 5:
        print(f'Not enough hidden unit tests [{num_hidden_unit_tests}/5]:', code_uid)
        for _ in range(5 - num_hidden_unit_tests):
            hidden_unit_tests.append({'input': '', 'output': ['']})
        example['hidden_unit_tests'] = str(hidden_unit_tests)
    elif num_hidden_unit_tests > 5:
        example['hidden_unit_tests'] = str(hidden_unit_tests[:5])

    return example


def main():
    load_name_code_review_eval_results = [
        # 'code_review_eval_codellama.jsonl',
        # 'code_review_eval_gpt3.jsonl',
        # 'code_review_eval_gpt4.jsonl',
        # 'code_review_eval_llama2.jsonl',
        # 'code_review_eval_palm.jsonl',
        'code_review_eval_starcoder.jsonl',
        # 'code_review_eval_vicuna.jsonl',
        # 'code_review_eval_wizardcoder.jsonl'
    ]
    load_name_code_smell_eval_results = [
        # 'code_smell_eval_codellama.jsonl',
        # 'code_smell_eval_gpt3.jsonl',
        # 'code_smell_eval_gpt4.jsonl',
        # 'code_smell_eval_llama2.jsonl',
        # 'code_smell_eval_palm.jsonl',
        'code_smell_eval_starcoder.jsonl',
        # 'code_smell_eval_vicuna.jsonl',
        # 'code_smell_eval_wizardcoder.jsonl'
    ]
    load_name_code_test_data_results = [
        # 'code_test_data_codellama.jsonl',
        # 'code_test_data_gpt3.jsonl',
        # 'code_test_data_gpt4.jsonl',
        # 'code_test_data_llama2.jsonl',
        # 'code_test_data_palm.jsonl',
        'code_test_data_starcoder.jsonl',
        # 'code_test_data_vicuna.jsonl',
        # 'code_test_data_wizardcoder.jsonl'
    ]

    print('Code review:')
    for load_name_code_review_eval_result in load_name_code_review_eval_results:
        llm_name = load_name_code_review_eval_result.split('_')[-1].split('.')[0]
        print(llm_name + ':')
        load_path_code_review_result = Path(__file__).parent.parent / Path('results') / Path('raw') / Path(
            llm_name) / Path(load_name_code_review_eval_result)
        save_path_code_review_result = Path(__file__).parent.parent / Path('results') / Path('check') / Path(
            llm_name) / Path('check_' + load_name_code_review_eval_result)
        dataset = load_dataset('json', split='train', data_files=str(load_path_code_review_result))
        dataset.cleanup_cache_files()
        dataset = dataset.map(check_diff_tag)
        dataset = dataset.map(check_review_comment)
        dataset.to_json(save_path_code_review_result, lines=True)

    print('Code smell:')
    for load_name_code_smell_eval_result in load_name_code_smell_eval_results:
        llm_name = load_name_code_smell_eval_result.split('_')[-1].split('.')[0]
        print(llm_name + ':')
        load_path_code_smell_result = Path(__file__).parent.parent / Path('results') / Path('raw') / Path(
            llm_name) / Path(load_name_code_smell_eval_result)
        save_path_code_smell_result = Path(__file__).parent.parent / Path('results') / Path('check') / Path(
            llm_name) / Path('check_' + load_name_code_smell_eval_result)
        dataset = load_dataset('json', split='train', data_files=str(load_path_code_smell_result))
        dataset.cleanup_cache_files()
        dataset = dataset.map(check_smell)
        dataset.to_json(save_path_code_smell_result, lines=True)

    print('Code test:')
    for load_name_code_test_data_result in load_name_code_test_data_results:
        llm_name = load_name_code_test_data_result.split('_')[-1].split('.')[0]
        print(llm_name + ':')
        load_path_code_test_result = Path(__file__).parent.parent / Path('results') / Path('raw') / Path(
            llm_name) / Path(load_name_code_test_data_result)
        save_path_code_test_result = Path(__file__).parent.parent / Path('results') / Path('check') / Path(
            llm_name) / Path('check_' + load_name_code_test_data_result)
        dataset = load_dataset('json', split='train', data_files=str(load_path_code_test_result))
        dataset.cleanup_cache_files()
        dataset = dataset.map(check_hidden_unit_tests)
        dataset.to_json(save_path_code_test_result, lines=True)


if __name__ == '__main__':
    expected_smells = ['large class', 'long method', 'data class', 'blob', 'feature envy', '']
    expected_diff_tags = [0, 1, 2]
    main()
    # python scripts/check_results.py
