import warnings
import numpy as np

from pathlib import Path
from datasets import load_dataset
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def main():
    average = 'weighted'
    supported_lang_clusters = ['C#', 'Java']
    supported_smells = ['large class', 'long method', 'data class', 'blob', 'feature envy', '']

    load_name_human_result = 'code_smell_eval_human.jsonl'
    load_name_llm_results = [
        'repair_code_smell_eval_codellama.jsonl',  # 35.91
        'repair_code_smell_eval_gpt3.jsonl',  # 36.8
        'repair_code_smell_eval_gpt4.jsonl',  # 33.53
        'repair_code_smell_eval_llama2.jsonl',  # 38.17
        'repair_code_smell_eval_palm.jsonl',  # 34.32
        'repair_code_smell_eval_starcoder.jsonl',  # 27.16
        'repair_code_smell_eval_vicuna.jsonl',  # 36.21
        'repair_code_smell_eval_wizardcoder.jsonl'  # 46.94
    ]

    load_path_human_result = Path(__file__).parent.parent / Path('results') / Path('raw') / Path(
        load_name_human_result.split('_')[-1].split('.')[0]) / Path(load_name_human_result)

    dataset_human = load_dataset('json', split='train', data_files=str(load_path_human_result))
    print(dataset_human)

    lang_cluster_dataset_humans = [
        dataset_human.filter(lambda example: example['lang_cluster'] == lang_cluster)
        for lang_cluster in supported_lang_clusters
    ]

    for load_name_llm_result in load_name_llm_results:
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

            lang_cluster_dataset_human = lang_cluster_dataset_humans[index]
            lang_cluster_dataset_llm = lang_cluster_dataset_llms[index]
            smells_human = lang_cluster_dataset_human['smell']
            smells_llm = lang_cluster_dataset_llm['smell']

            accuracy = round(accuracy_score(y_true=smells_human, y_pred=smells_llm) * 100, 2)
            evaluation_metrics.append(accuracy)
            print('accuracy score:', accuracy)

            precision = round(precision_score(y_true=smells_human, y_pred=smells_llm, labels=supported_smells,
                                              average=average) * 100, 2)
            evaluation_metrics.append(precision)
            print('average precision score:', precision)

            recall = round(
                recall_score(y_true=smells_human, y_pred=smells_llm, labels=supported_smells, average=average) * 100,
                2)
            evaluation_metrics.append(recall)
            print('average recall score:', recall)

            f1 = round(
                f1_score(y_true=smells_human, y_pred=smells_llm, labels=supported_smells, average=average) * 100, 2)
            evaluation_metrics.append(f1)
            print('average f1 score:', f1)

        print('evaluation metrics:', evaluation_metrics)
        overall_score = round(float(np.mean(evaluation_metrics)), 2)
        print('+' + '-' * 50 + '+')
        print('overall score:', overall_score)
        print('+' + '-' * 50 + '+')


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    main()
    # python scorers/score_code_smell.py
