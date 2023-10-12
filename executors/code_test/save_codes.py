import re
import argparse

from tqdm import tqdm
from pathlib import Path
from collections import Counter
from datasets import load_dataset


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--code_test_data_name', default='repair_code_test_data_starcoder.jsonl',
                        choices=[
                            'repair_code_test_data_codellama.jsonl',
                            'repair_code_test_data_gpt3.jsonl',
                            'repair_code_test_data_gpt4.jsonl',
                            'repair_code_test_data_llama2.jsonl',
                            'repair_code_test_data_palm.jsonl',
                            'repair_code_test_data_starcoder.jsonl'
                            'repair_code_test_data_vicuna.jsonl',
                            'repair_code_test_data_wizardcoder.jsonl'
                        ], type=str)
    parser.add_argument('--codes_dir_name', default='starcoder_codes',
                        choices=[
                            'codellama_codes',
                            'gpt3_codes',
                            'gpt4_codes',
                            'llama2_codes',
                            'palm_codes',
                            'starcoder_codes',
                            'vicuna_codes',
                            'wizardcoder_codes'
                        ], type=str)
    args = parser.parse_args()

    return args


def main():
    supported_lang_clusters = ['c', 'cpp', 'java', 'python']
    load_path = Path(__file__).parent.parent.parent / Path('results') / Path('repair') / Path(
        args.code_test_data_name.split('_')[-1].split('.')[0]) / Path(args.code_test_data_name)
    codes_dir = Path(__file__).parent.parent / Path('code_test') / Path('codes') / Path(args.codes_dir_name)
    if not codes_dir.is_dir():
        codes_dir.mkdir(parents=True, exist_ok=True)
    for lang_cluster in supported_lang_clusters:
        lang_dir = codes_dir / Path(lang_cluster)
        if not lang_dir.is_dir():
            lang_dir.mkdir(parents=True, exist_ok=True)

    dataset = load_dataset('json', split='train', data_files=str(load_path))
    print(dataset)

    lang_counts = Counter(dataset['lang'])
    for lang, count in lang_counts.items():
        print(f'{lang}: {count}')

    lang_cluster_counts = Counter(dataset['lang_cluster'])
    for lang_cluster, count in lang_cluster_counts.items():
        print(f'{lang_cluster}: {count}')

    # save codes of four language clusters
    for example in tqdm(dataset):
        lang_cluster = example['lang_cluster']
        code_uid = example['code_uid']
        source_code = example['source_code']

        # create saved directory of four language clusters codes
        if lang_cluster == 'C':
            lang_dir = codes_dir / Path('c')
        elif lang_cluster == 'C++':
            lang_dir = codes_dir / Path('cpp')
        elif lang_cluster == 'Java':
            lang_dir = codes_dir / Path('java')
        elif lang_cluster == 'Python':
            lang_dir = codes_dir / Path('python')
        else:
            print('Language cluster not found, use default language cluster directory.')
            lang_dir = codes_dir

        file_dir = lang_dir / Path(code_uid)
        if not file_dir.is_dir():
            file_dir.mkdir(parents=True, exist_ok=True)

        # create saved path of four language clusters codes
        if lang_cluster == 'C':
            file_path = file_dir / Path('code.c')
        elif lang_cluster == 'C++':
            file_path = file_dir / Path('code.cpp')
        elif lang_cluster == 'Java':
            # find class name in the java source code
            pattern = r'public\s+(?:final\s+)?class\s+(\w+)'
            matches = re.search(pattern, source_code)
            if matches:
                class_name = matches.group(1)
            else:
                print('Class name not found, use default class name.')
                class_name = 'code'

            # if java class does not have an explicit default constructor, the compiler will generate one for it and
            # since it is implicit it may be associated with that line of code, so the possible solution is to create
            # a private constructor for the java class, since this class can no longer be instantiated outside itself,
            # jacoco no longer counts it towards its code coverage metric.
            # References: https://www.nerd.vision/post/jacoco-coverage-of-util-classes
            constructor_code = f'\n\n\tprivate {class_name}() {{}}\n'
            pattern = r'public\s+(?:final\s+)?class\s+' + class_name + r'(\s+\w+\s+\w+\s*)?(\s+//implements\s+Runnable)?\s*{'
            matches = re.search(pattern, source_code)
            if matches:
                class_definition = matches.group(0)
                source_code = source_code.replace(class_definition, class_definition + constructor_code)
            else:
                print('Class definition not found, use default source code.')

            file_path = file_dir / Path(f'{class_name}.java')
        elif lang_cluster == 'Python':
            file_path = file_dir / Path('code.py')
        else:
            print('Language cluster not found, use default language cluster path.')
            file_path = file_dir / Path('code')

        with open(file_path, mode='w', encoding='utf-8') as file:
            file.write(source_code)


if __name__ == '__main__':
    args = parse_arguments()
    main()
    # python executors/code_test/save_codes.py
