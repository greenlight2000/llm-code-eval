## Code Summarization

### 1. Installation

1. `cd code_summarization`
2. install `python>=3.9` (we only guarantee the code works on python 3.9)
3. install `torch` based on your cuda version
4. `pip install -r requirements.txt`

### 2. Inference

`cd inference`

Run the inference scripts to get the inference results of the targeted llms. The inference results `code_summ_data_{modelname}.jsonl` will be saved under the `inference/results` folder. Specifically,

#### 2.1 PaLM

Replace "google_api_key" with your own Google API key.

`python infer_palm.py --api_key google_api_key --data_load_name code_summarization_data.jsonl --result_save_name code_summ_infer_palm.jsonl --log_file_name code_summ_infer_palm.log`

#### 2.2 GPT-3.5

Replace "openai_api_key" with your own OpenAI API key.

`python infer_gpt.py --api_key openai_api_key --model gpt-3.5-turbo-0613 --data_load_name code_summarization_data.jsonl --result_save_name code_summ_infer_gpt3.jsonl --log_file_name code_summ_infer_gpt3.log`

#### 2.3 GPT-4

Replace "openai_api_key" with your own OpenAI API key.

`python infer_gpt.py --api_key openai_api_key --model gpt-4-0613 --data_load_name code_summarization_data.jsonl --result_save_name code_summ_infer_gpt4.jsonl --log_file_name code_summ_infer_gpt4.log`

#### 2.4 CodeLLaMA

Replace "access_token" with your own HuggingFace access token.

Replace "cache_dir" with path to a directory in which a downloaded pretrained model should be cached.

`python infer_codellama.py --access_token access_token --cache_dir cache_dir --checkpoint codellama/CodeLlama-34b-Instruct-hf --data_load_name code_summarization_data.jsonl --result_save_name code_summ_infer_codellama.jsonl --log_file_name code_summ_infer_codellama.log`

#### 2.5 Vicuna

Replace "access_token" with your own HuggingFace access token.

Replace "cache_dir" with path to a directory in which a downloaded pretrained model should be cached.

`python infer_vicuna.py --access_token access_token --cache_dir cache_dir --checkpoint lmsys/vicuna-13b-v1.5-16k --data_load_name code_summarization_data.jsonl --result_save_name code_summ_infer_vicuna.jsonl --log_file_name code_summ_infer_vicuna.log`

#### 2.6 LLaMA2

Replace "access_token" with your own HuggingFace access token.

Replace "cache_dir" with path to a directory in which a downloaded pretrained model should be cached.

`python infer_llama2.py --access_token access_token --cache_dir cache_dir --checkpoint meta-llama/Llama-2-70b-chat-hf --data_load_name code_summarization_data.jsonl --result_save_name code_summ_infer_llama2.jsonl --log_file_name code_summ_infer_llama2.log`

#### 2.7 WizardCoder

Replace "access_token" with your own HuggingFace access token.

Replace "cache_dir" with path to a directory in which a downloaded pretrained model should be cached.

`python infer_wizardcoder.py --access_token access_token --cache_dir cache_dir --checkpoint WizardLM/WizardCoder-15B-V1.0 --data_load_name code_summarization_data.jsonl --result_save_name code_summ_infer_wizardcoder.jsonl --log_file_name code_summ_infer_wizardcoder.log`

#### 2.8 StarCoder

Replace "access_token" with your own HuggingFace access token.

Replace "cache_dir" with path to a directory in which a downloaded pretrained model should be cached.

`python infer_starcoder.py --access_token access_token --cache_dir cache_dir --checkpoint HuggingFaceH4/starchat-beta --data_load_name code_summarization_data.jsonl --result_save_name code_summ_infer_starcoder.jsonl --log_file_name code_summ_infer_starcoder.log`

### 3. Evaluation

1. `cd ../evaluator` 
2. Run `python score_code_summarization.py` to get the scores of the targeted llm's inference results, the results will be palced at `evaluator/summ_scores/`.