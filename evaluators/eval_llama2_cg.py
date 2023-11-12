import re
import json
import torch
import logging
import argparse
import warnings

from pathlib import Path
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from tenacity import retry, stop_after_attempt, wait_random_exponential
import pandas as pd
import os

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--access_token', default=None, type=str)
    parser.add_argument('--cache_dir', default=None, type=str)
    parser.add_argument('--checkpoint', default='meta-llama/Llama-2-7b-chat-hf',
                        choices=['meta-llama/Llama-2-7b-chat-hf', 'meta-llama/Llama-2-13b-chat-hf',
                                 'meta-llama/Llama-2-70b-chat-hf'], type=str)
    parser.add_argument('--data_load_name', default='code_smell_data.jsonl',)
    parser.add_argument('--result_save_name', default='code_smell_eval_llama.jsonl')
    parser.add_argument('--log_file_name', default='code_smell_eval_llama.log'),
    parser.add_argument('--temperature', default=0.5, type=float)
    parser.add_argument('--candidate_num', default=1, type=int)
    args = parser.parse_args()

    return args

lang_cluster = ['c++', 'java', 'python', 'c', 'c#', 'ruby', 'delphi', 'go',
                'javascript', 'kotlin', 'php', 'd', 'perl', 'rust']

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text(prompt, temperature, max_new_tokens,candidate_num):
    inputs = tokenizer(prompt, return_tensors='pt', add_special_tokens=False).to(device)
    outputs = model.generate(
        inputs['input_ids'],
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        num_return_sequences=candidate_num,
        pad_token_id=tokenizer.eos_token_id
    ).to('cpu')
    responses = [tokenizer.decode(output, skip_special_tokens=True)
                 .split('[/INST]')[-1].strip().replace('</s>','')
                  for output in outputs]

    return responses


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def count_message_tokens(content):
    tokens = tokenizer(content)['input_ids']
    num_tokens = len(tokens)

    return num_tokens


env_map = {
    'c++': ['GNU C++11', 'GNU C++14', 'MS C++', 'GNU C++0x', 'GNU C++', 'MS C++ 2017', 'Clang++17 Diagnostics',
            'GNU C++17'],
    'c#': ['MS C#', 'Mono C#', '.NET Core C#'],
    'java': ['Java 11', 'Java 7', 'Java 6', 'Java 8'],
    'javascript': ['JavaScript', 'Node.js'],
    'c': ['GNU C', 'GNU C11'],
    'python': ['Python 2', 'PyPy 3', 'Python 3', 'PyPy 2'],
    'php': ['PHP'],
    'ruby': ['Ruby'],
    'kotlin': ['Kotlin'],
    'rust': ['Rust'],
    'go': ['Go'],
    'd': ['dmd 2.105.0 win32'],
    'delphi': ['Delphi7 win32'],
    'perl': ['Perl v5.20.3']
}





def add_program_synthesis(example):
    """

    Program synthesis: Generate corresponding code based on the problem description

    """


    prob_uid = example['src_uid']
    prob_desc_description = example['description']
    prob_desc_input_spec = example['input_spec']
    prob_desc_output_spec = example['output_spec']
    prob_desc_sample_inputs = example['sample_inputs']
    prob_desc_sample_outputs = example['sample_outputs']
    prob_desc_notes = example['notes']
    lang = example['lang_cluster']

    user_message = f"""As an expert code developer with years of experience, please provide the source code based on the problem description. The detailed information are as follows:
1. Problem description: {prob_desc_description}
2. Input specification: {prob_desc_input_spec}
3. Output specification: {prob_desc_output_spec}
4. Sample inputs: {prob_desc_sample_inputs}
5. Sample outputs: {prob_desc_sample_outputs}
6. Sample explanations: {prob_desc_notes}
7. Programming language: {lang} 
8. support programming language version: {env_map[lang.lower()]}
Respond should only with a string in the following JSON format:
[{{"version": specific version used in the programming language, "target code":  the code you produced in the respective programming language version."}}] """

    prompt = f'<s>[INST] {user_message.strip()} [/INST]'
    logging.info('problem src_id: ' + str(prob_uid))

    input_tokens = count_message_tokens(prompt)
    logging.info('input tokens: ' + str(input_tokens))
    if input_tokens > max_input_tokens:
        logging.warning('Over input tokens limit: ' + str(prob_uid))
    try:
        response = generate_text(
            prompt=prompt,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            candidate_num=candidate_num
        )
        logging.info('response: ' + str(response))

        if response is not None:
            program_sythesis = response
        else:
            logging.warning('Respond content is none.')
            program_sythesis = []
    except Exception as e:
        logging.error('Failed to generate text: ' + e.__str__())
        program_sythesis = []

    for i, generated_code in enumerate(program_sythesis):
        output_tokens = count_message_tokens(generated_code)
        logging.info('output tokens: ' + str(output_tokens))
        if output_tokens > max_new_tokens:
            logging.warning('Over total tokens limit ' + str(prob_uid) + ' lang: ' + str(lang))
            generated_code = ''
        logging.info('program_synthesis  in: ' + lang + ' :' + generated_code)
        example['program_synthesis_' + str(i)] = generated_code
    if len(program_sythesis) < candidate_num:
        for i in range(candidate_num - len(program_sythesis)):
            example['program_synthesis_' + str(i + len(program_sythesis))] = ''
    return example

def add_code_translation(example):
    """

    Translation: Generate corresponding code in specific language based on the given code

    """

    source_lang = example['lang_cluster']
    target_lang = example['target_lang_cluster']
    prob_uid = example['src_uid']
    source_code = example['source_code']

    user_message = f"""As an expert code developer proficient in multiple programming languages with years of experience, please translate the source code in {source_lang} to programming language {target_lang} within our supported version. 

The detailed information are as follows:
1. Target programming language: {target_lang}
2. support programming language version: {env_map[target_lang]}
3. Source code\n: {source_code}

Respond should only with a string in the following JSON format:
[{{"version": specific version used in the programming language, "target code":  the code you produced in the respective programming language version."}}] """

    prompt = f'<s>[INST] {user_message.strip()} [/INST]'
    logging.info('problem src_id: ' + str(prob_uid))

    input_tokens = count_message_tokens(prompt)
    logging.info('input tokens: ' + str(input_tokens))
    if input_tokens > max_input_tokens:
        logging.warning('Over input tokens limit: ' + str(prob_uid))
    try:
        response = generate_text(
            prompt=prompt,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            candidate_num=candidate_num
        )
        logging.info('response: ' + str(response))

        if response is not None:
            translation_outcome = response
        else:
            logging.warning('Respond content is none.')
            translation_outcome = []

    except Exception as e:
        logging.error('Failed to generate text: ' + e.__str__())
        translation_outcome = []

    for i, generated_code in enumerate(translation_outcome):
        output_tokens = count_message_tokens(generated_code)
        logging.info('output tokens: ' + str(output_tokens))
        if output_tokens > max_new_tokens:
            logging.warning('Over total tokens limit ' + str(prob_uid) + ' lang: ' + str(target_lang))
            generated_code = ''
        logging.info('code translation  in: ' + target_lang + ' :' + generated_code)
        example['code_translation_' + str(i)] = generated_code
    if len(translation_outcome) < candidate_num:
        for i in range(candidate_num-len(translation_outcome)):
            example['code_translation_' + str(i+len(translation_outcome))] = ''


    return example

def add_code_repairing(example):
    """
     Code repair: Generate corresponding code based on the problem description and buggy code

     """

    source_lang = example['lang']

    prob_uid = example['src_uid']
    source_code = example['source_code']
    prob_desc_description = example['description']
    prob_desc_input_spec = example['input_spec']
    prob_desc_output_spec = example['output_spec']
    prob_desc_sample_inputs = example['sample_inputs']
    prob_desc_sample_outputs = example['sample_outputs']
    error_msg = example['exec_outcome']
    user_message = f"""As an expert code developer with years of experience, please debug the source code in {source_lang} based on the corresponding problem description and show the correct code. 
The detailed information are shown as follows: 
1. Problem description: {prob_desc_description}
2. Input specification: {prob_desc_input_spec}
3. Output specification: {prob_desc_output_spec}        
4. Sample inputs: {prob_desc_sample_inputs}
5. Sample outputs: {prob_desc_sample_outputs}
6. Programming language: {source_lang}  
7. Buggy code :\n {source_code}
8. Error message: {error_msg}
Please note that use complex header files as little as possible. 

Respond should only with a string in the following JSON format:
[{{"version": specific version used in the programming language, "target code":  the code you produced in the respective programming language version."}}] """

    prompt = f'<s>[INST] {user_message.strip()} [/INST]'
    logging.info('problem src_id: ' + str(prob_uid))

    input_tokens = count_message_tokens(prompt)
    logging.info('input tokens: ' + str(input_tokens))
    if input_tokens > max_input_tokens:
        logging.warning('Over input tokens limit: ' + str(prob_uid))
    try:
        response = generate_text(
            prompt=prompt,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            candidate_num=candidate_num
        )
        logging.info('response: ' + str(response))

        if response is not None:
            repair_outcome = response
        else:
            logging.warning('Respond content is none.')
            repair_outcome = []

    except Exception as e:
        logging.error('Failed to generate text: ' + e.__str__())
        repair_outcome = []

    for i, generated_code in enumerate(repair_outcome):
        output_tokens = count_message_tokens(generated_code)
        logging.info('output tokens: ' + str(output_tokens))
        if output_tokens > max_new_tokens:
            logging.warning('Over total tokens limit ' + str(prob_uid) + ' lang: ' + str(source_lang))
            generated_code = ''
        logging.info('Code repairing in: ' + source_lang + ' :' + generated_code)
        example['code_repairing_'+str(i)] = generated_code

    if len(repair_outcome) < candidate_num:

        for i in range(candidate_num - len(repair_outcome)):
            example['code_repairing_' + str(i + len(repair_outcome))] = ''

    return example


def main():
    load_path = Path(__file__).parent.parent / Path('data') / Path(args.data_load_name)
    save_path = Path(__file__).parent.parent / Path('results') / Path(args.result_save_name)

    dataset = load_dataset('json', split='train', data_files=str(load_path))
    dataset.cleanup_cache_files()  # for multiple evaluation

    if 'program_synthesis' in args.data_load_name:
        dataset = dataset.map(add_program_synthesis)
    elif 'translation' in args.data_load_name:
        dataset = dataset.map(add_code_translation)
    elif 'code_debug' in args.data_load_name:
        dataset = dataset.map(add_code_repairing)
    else:
        print("please use corresponding task as file name")
    dataset.to_json(save_path, lines=True)


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    args = parse_arguments()

    log_file_path = Path(__file__).parent.parent / Path('logs') / Path(args.log_file_name)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt='%(asctime)s - %(filename)s - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
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

    # References: https://huggingface.co/blog/llama2
    # References: https://colab.research.google.com/drive/1X1z9Q6domMKl2CnEM0QGHNwidLfR4dW2?usp=sharing
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
        # load_in_4bit=True,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
        device_map='auto',
        token=args.access_token,
        cache_dir=args.cache_dir
    )
    print(f'Memory footprint: {model.get_memory_footprint() / 1e6:.2f} MB')

    max_input_tokens = tokenizer.model_max_length  # 1000000000000000019884624838656
    # The maximum numbers of tokens to generate, ignoring the number of tokens in the prompt.
    max_new_tokens = 2048
    candidate_num=args.candidate_num
    temperature = args.temperature
    main()
    # python scripts/eval_llama2.py
