import warnings
import numpy as np

from pathlib import Path
from datasets import load_dataset


def main():
    supported_lang_clusters = ['C', 'C++', 'Java', 'Python']

    load_name_human_result = 'code_test_eval_human.jsonl'  # 96.91
    load_name_llm_results = [
        'repair_code_test_eval_codellama.jsonl',  # 81.84
        'repair_code_test_eval_gpt3.jsonl',  # 86.61
        'repair_code_test_eval_gpt4.jsonl',  # 79.08
        'repair_code_test_eval_llama2.jsonl',  # 82.7
        'repair_code_test_eval_palm.jsonl',  # 83.76
        'repair_code_test_eval_starcoder.jsonl',  # 78.56
        'repair_code_test_eval_vicuna.jsonl',  # 75.59
        'repair_code_test_eval_wizardcoder.jsonl'  # 81.83
    ]
    load_name_llm_results.append(load_name_human_result)

    for load_name_llm_result in load_name_llm_results:
        if load_name_llm_result == load_name_human_result:
            load_path_llm_result = Path(__file__).parent.parent / Path('results') / Path('raw') / Path(
                load_name_llm_result.split('_')[-1].split('.')[0]) / Path(load_name_llm_result)
        else:
            load_path_llm_result = Path(__file__).parent.parent / Path('results') / Path('repair') / Path(
                load_name_llm_result.split('_')[-1].split('.')[0]) / Path(load_name_llm_result)

        dataset_llm = load_dataset('json', split='train', data_files=str(load_path_llm_result))
        print(dataset_llm)

        lang_cluster_dataset_llms = [
            dataset_llm.filter(lambda example: example['lang_cluster'] == lang_cluster)
            for lang_cluster in supported_lang_clusters
        ]

        print('+' + '——' * 25 + '+')
        print(load_name_llm_result.split('_')[-1].split('.')[0] + ':')
        print('+' + '——' * 25 + '+')
        evaluation_metrics = []
        for index in range(len(supported_lang_clusters)):
            print('+' + '-' * 50 + '+')
            print(supported_lang_clusters[index] + ':')
            print('+' + '-' * 50 + '+')

            lang_cluster_dataset_llm = lang_cluster_dataset_llms[index]

            pass_rate = round(float(np.mean(lang_cluster_dataset_llm['pass_rate'])), 2)
            evaluation_metrics.append(pass_rate)
            print('average pass rate:', pass_rate)

            line_coverage = round(float(np.mean(lang_cluster_dataset_llm['line_coverage'])), 2)
            evaluation_metrics.append(line_coverage)
            print('average line coverage:', line_coverage)

            branch_coverage = round(float(np.mean(lang_cluster_dataset_llm['branch_coverage'])), 2)
            evaluation_metrics.append(branch_coverage)
            print('average branch coverage:', branch_coverage)

        print('evaluation metrics:', evaluation_metrics)
        overall_score = round(float(np.mean(evaluation_metrics)), 2)
        print('+' + '-' * 50 + '+')
        print('overall score:', overall_score)
        print('+' + '-' * 50 + '+')


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    main()
    # python scorers/score_code_test.py
