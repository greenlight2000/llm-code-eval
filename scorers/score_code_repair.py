import pandas as pd
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--load_path', type=str, )
    parser.add_argument('--output_path', type=str, )
    args = parser.parse_args()
    return args

support_lang_clusters = ['C++', 'Java', 'Python', 'C', 'C#', 'Ruby',  'Go',
                'Javascript', 'Kotlin', 'PHP', 'Rust',  'd', 'perl', 'delphi',]

def valid_execfiles(exec_outcome_dir):
    exec_outcome = pd.read_json(exec_outcome_dir, lines=True)
    exec_outcome['lang_cluster'] = exec_outcome['lang_cluster'].apply(lambda x: x.lower())


    def is_correct(row):
        if all(item['exec_outcome'] == 'PASSED' for item in row['unittests']):
            return 'True'
        else:
            return 'False'

    exec_outcome['is_correct'] = exec_outcome.apply(is_correct, axis=1)

    correct_outcome = exec_outcome[exec_outcome['is_correct'] == 'True']


    for lang_cluster in support_lang_clusters:
        exec_outcome_cur = exec_outcome[exec_outcome['lang_cluster'] == lang_cluster.lower()]
        exec_num = exec_outcome_cur['src_uid'].drop_duplicates().shape[0]
        correct_outcome_cur = correct_outcome[correct_outcome['lang_cluster'] == lang_cluster.lower()]
        correct_num = correct_outcome_cur['src_uid'].drop_duplicates().shape[0]
        print(f"DSR on {lang_cluster}: {correct_num/exec_num} ")

    return exec_outcome

def main():
    processed_outcome = valid_execfiles(args.load_path)
    # Save processed outcome result
    processed_outcome.to_json(args.output_path, orient='records', lines=True)


if __name__ == '__main__':
    args = parse_arguments()
    main()


