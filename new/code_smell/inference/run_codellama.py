import torch
import logging
import argparse
import warnings

from pathlib import Path
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from tenacity import retry, stop_after_attempt, wait_random_exponential


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--access_token', default=None, type=str)
    parser.add_argument('--cache_dir', default=None, type=str)
    parser.add_argument('--checkpoint', default='codellama/CodeLlama-34b-Instruct-hf',
                        choices=[
                            'codellama/CodeLlama-7b-Instruct-hf',
                            'codellama/CodeLlama-13b-Instruct-hf',
                            'codellama/CodeLlama-34b-Instruct-hf'
                        ],
                        type=str)
    args = parser.parse_args()

    return args


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text(prompt, temperature, max_new_tokens):
    inputs = tokenizer(prompt, return_tensors='pt', add_special_tokens=False).to(device)
    outputs = model.generate(
        inputs['input_ids'],
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    ).to('cpu')
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response.split('[/INST]')[-1].strip()


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def count_message_tokens(content):
    tokens = tokenizer(content)['input_ids']
    num_tokens = len(tokens)

    return num_tokens


def add_smell(example):
    id = example['id']
    lang_cluster = example['lang_cluster']
    smell_code = example['smell_code']
    source_code = example['source_code']
    user_message = f"""As an expert software developer with years of experience, please meticulously inspect the following smell code snippet and categorize it into one of the following categories:
- large class
- data class
- blob
- feature envy
- long method
The detailed information are as follows:
1. Programming language: {lang_cluster} 
2. Smell code snippet: 
```
{smell_code.strip()}
```
3. Source code containing code smells:
```
{source_code.strip()}
```
Respond only with one of the specified categories."""
    prompt = f'<s>[INST] {user_message.strip()} [/INST]'

    logging.info('sample id: ' + str(id))

    input_tokens = count_message_tokens(prompt)
    logging.info('input tokens: ' + str(input_tokens))
    if input_tokens > max_input_tokens:
        logging.warning('Over input tokens limit: ' + str(id))

    try:
        response = generate_text(
            prompt=prompt,
            temperature=temperature,
            max_new_tokens=max_new_tokens
        )
        logging.info('response: ' + str(response))

        if response is not None:
            output_tokens = count_message_tokens(response)
            logging.info('output tokens: ' + str(output_tokens))
            if output_tokens > max_new_tokens:
                logging.warning('Over output tokens limit ' + str(id))

            supported_smells = ['large class', 'long method', 'data class', 'blob', 'feature envy']
            if all(supported_smell not in response.lower() for supported_smell in supported_smells):
                logging.warning('Respond content is invalid value.')
                smell = ''
            else:
                smell = ''
                min_index = float('inf')
                for supported_smell in supported_smells:
                    first_index = response.lower().find(supported_smell)
                    if first_index != -1 and first_index < min_index:
                        min_index = first_index
                        smell = supported_smell
        else:
            logging.warning('Respond content is none.')
            smell = ''

    except Exception as e:
        logging.error('Failed to generate text: ' + e.__str__())
        smell = ''

    logging.info('smell: ' + str(smell))
    example['predicted_smell'] = smell

    return example


def main():
    load_data_path = Path(__file__).parent.parent.parent / Path('data') / Path('code_smell_data.jsonl')
    save_data_path = Path(__file__).parent / Path('results') / Path('code_smell_result_codellama.jsonl')

    dataset = load_dataset('json', split='train', data_files=str(load_data_path))
    dataset.cleanup_cache_files()
    print(dataset)

    dataset = dataset.map(add_smell)
    print(dataset)

    dataset.to_json(save_data_path, lines=True)


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    args = parse_arguments()

    log_file_path = Path(__file__).parent.parent / Path('logs') / Path('code_smell_log_codellama.log')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt='%(asctime)s - %(filename)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler = logging.FileHandler(filename=log_file_path, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Device:', device)

    tokenizer = AutoTokenizer.from_pretrained(
        args.checkpoint,
        use_fast=True,
        trust_remote_code=True,
        token=args.access_token,
        cache_dir=args.cache_dir
    )
    model = AutoModelForCausalLM.from_pretrained(
        args.checkpoint,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
        device_map='auto',
        token=args.access_token,
        cache_dir=args.cache_dir
    )
    print(f'Memory footprint: {model.get_memory_footprint() / 1e6:.2f} MB')
    temperature = 0
    max_input_tokens = tokenizer.model_max_length  # 1000000000000000019884624838656
    max_new_tokens = 1024

    main()
