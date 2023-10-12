import warnings
import tiktoken

from pathlib import Path
from datasets import load_dataset


def count_tokens(content):
    encoding = tiktoken.get_encoding('cl100k_base')
    num_tokens = len(encoding.encode(content))

    return num_tokens


def accumulate_code_review_tokens(example):
    lang_cluster = example['lang_cluster']
    old_code = example['old_code']
    diff_hunk = example['diff_hunk']
    content = lang_cluster + old_code + diff_hunk

    global code_review_total_tokens
    code_review_total_tokens += count_tokens(content)

    return example


def accumulate_code_smell_tokens(example):
    lang_cluster = example['lang_cluster']
    smell_code = example['smell_code']
    source_code = example['source_code']
    content = lang_cluster + smell_code + source_code

    global code_smell_total_tokens
    code_smell_total_tokens += count_tokens(content)

    return example


def accumulate_code_test_tokens(example):
    prob_desc_description = example['prob_desc_description']
    prob_desc_time_limit = example['prob_desc_time_limit']
    prob_desc_memory_limit = example['prob_desc_memory_limit']
    prob_desc_input_spec = example['prob_desc_input_spec']
    prob_desc_output_spec = example['prob_desc_output_spec']
    prob_desc_sample_inputs = example['prob_desc_sample_inputs']
    prob_desc_sample_outputs = example['prob_desc_sample_outputs']
    prob_desc_notes = example['prob_desc_notes']
    source_code = example['source_code']
    lang_cluster = example['lang_cluster']
    num_hidden_unit_tests = example['num_hidden_unit_tests']
    content = prob_desc_description + prob_desc_time_limit + prob_desc_memory_limit + \
              prob_desc_input_spec + prob_desc_output_spec + prob_desc_sample_inputs + \
              prob_desc_sample_outputs + str(prob_desc_notes) + source_code + \
              lang_cluster + str(num_hidden_unit_tests)

    global code_test_total_tokens
    code_test_total_tokens += count_tokens(content)

    return example


def main():
    load_name_datas = [
        'code_review_data.jsonl',
        'code_smell_data.jsonl',
        'code_test_data.jsonl'
    ]

    for load_name_data in load_name_datas:
        load_path_data = Path(__file__).parent.parent / Path('data') / Path(load_name_data)
        dataset = load_dataset('json', split='train', data_files=str(load_path_data))
        dataset.cleanup_cache_files()  # for multiple count

        if load_name_data == 'code_review_data.jsonl':
            dataset = dataset.map(accumulate_code_review_tokens)
            print('Code review:')
            print('total samples:', len(dataset))
            print('total tokens:', code_review_total_tokens)
            print('average tokens/sample:', code_review_total_tokens / len(dataset))
        elif load_name_data == 'code_smell_data.jsonl':
            dataset = dataset.map(accumulate_code_smell_tokens)
            print('Code smell:')
            print('total samples:', len(dataset))
            print('total tokens:', code_smell_total_tokens)
            print('average tokens/sample:', code_smell_total_tokens / len(dataset))
        elif load_name_data == 'code_test_data.jsonl':
            dataset = dataset.map(accumulate_code_test_tokens)
            print('Code test:')
            print('total samples:', len(dataset))
            print('total tokens:', code_test_total_tokens)
            print('average tokens/sample:', code_test_total_tokens / len(dataset))


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    code_review_total_tokens = 0
    code_smell_total_tokens = 0
    code_test_total_tokens = 0
    main()
    # python scripts/count_tokens.py
