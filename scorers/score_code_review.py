import warnings
import evaluate
import numpy as np

from pathlib import Path
from datasets import load_dataset
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def main():
    average = 'weighted'
    supported_lang_clusters = ['C', 'C#', 'C++', 'Go', 'Java', 'Javascript', 'PHP', 'Python', 'Ruby']
    supported_diff_tags = [0, 1, 2]

    load_name_human_result = 'code_review_eval_human.jsonl'
    load_name_llm_results = [
        'repair_code_review_eval_codellama.jsonl',  # 42.41
        'repair_code_review_eval_gpt3.jsonl',  # 39.97
        'repair_code_review_eval_gpt4.jsonl',  # 41.37
        'repair_code_review_eval_llama2.jsonl',  # 41.77
        'repair_code_review_eval_palm.jsonl',  # 40.79
        'repair_code_review_eval_starcoder.jsonl',  # 39.28
        'repair_code_review_eval_vicuna.jsonl',  # 41.92
        'repair_code_review_eval_wizardcoder.jsonl'  # 38.29
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
            diff_tags_human = lang_cluster_dataset_human['diff_tag']
            diff_tags_llm = lang_cluster_dataset_llm['diff_tag']

            accuracy = round(accuracy_score(y_true=diff_tags_human, y_pred=diff_tags_llm) * 100, 2)
            evaluation_metrics.append(accuracy)
            print('accuracy score:', accuracy)

            precision = round(precision_score(y_true=diff_tags_human, y_pred=diff_tags_llm, labels=supported_diff_tags,
                                              average=average) * 100, 2)
            evaluation_metrics.append(precision)
            print('average precision score:', precision)

            recall = round(
                recall_score(y_true=diff_tags_human, y_pred=diff_tags_llm, labels=supported_diff_tags,
                             average=average) * 100,
                2)
            evaluation_metrics.append(recall)
            print('average recall score:', recall)

            f1 = round(
                f1_score(y_true=diff_tags_human, y_pred=diff_tags_llm, labels=supported_diff_tags,
                         average=average) * 100, 2)
            evaluation_metrics.append(f1)
            print('average f1 score:', f1)

            positive_diff_tag_dataset_human = lang_cluster_dataset_human.filter(
                lambda example: example['diff_tag'] == 1)
            positive_diff_tag_dataset_llm = lang_cluster_dataset_llm.filter(
                lambda example: example['code_uid'] in positive_diff_tag_dataset_human['code_uid'])
            positive_diff_tag_review_comments_human = positive_diff_tag_dataset_human['review_comment']
            positive_diff_tag_review_comments_llm = positive_diff_tag_dataset_llm['review_comment']

            bleu_results = bleu_metric.compute(predictions=positive_diff_tag_review_comments_llm,
                                               references=positive_diff_tag_review_comments_human)
            bleu = round(bleu_results['bleu'] * 100, 2)
            evaluation_metrics.append(bleu)
            print('bleu score:', bleu)

            rouge_results = rouge_metric.compute(predictions=positive_diff_tag_review_comments_llm,
                                                 references=positive_diff_tag_review_comments_human)
            rouge = round(rouge_results['rougeL'] * 100, 2)
            evaluation_metrics.append(rouge)
            print('rouge score:', rouge)

            bertscore_results = bertscore_metric.compute(predictions=positive_diff_tag_review_comments_llm,
                                                         references=positive_diff_tag_review_comments_human, lang='en')
            bertscore = round(np.mean(bertscore_results['f1']) * 100, 2)  # macro average
            evaluation_metrics.append(bertscore)
            print('bert score:', bertscore)

        print('evaluation metrics:', evaluation_metrics)
        overall_score = round(float(np.mean(evaluation_metrics)), 2)
        print('+' + '-' * 50 + '+')
        print('overall score:', overall_score)
        print('+' + '-' * 50 + '+')


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    # References: https://huggingface.co/spaces/evaluate-metric/bleu
    bleu_metric = evaluate.load('bleu')
    # References: https://huggingface.co/spaces/evaluate-metric/rouge
    rouge_metric = evaluate.load('rouge')
    # References: https://huggingface.co/spaces/evaluate-metric/bertscore
    bertscore_metric = evaluate.load('bertscore')
    main()
    # python scorers/score_code_review.py
