## LLMCodeEval: An Execution-Based Multilingual Multitask Multidimensional Benchmark for Evaluating Large Language Models on Code Understanding and Generation

### 项目结构

#### 1. data

该目录下存放数据集：

* code_review_data.jsonl
* code_smell_data.jsonl
* code_test_data.jsonl
* code_summarization_data.jsonl
* code_optimization_data.jsonl
* code_translation_data.jsonl
* code_repair_data.jsonl
* program_synthesis_data.jsonl

TODO: 补全

#### 2. evaluators

该目录下存放评估LLMs的代码：

* eval_codellama.py
* eval_gpt.py
* eval_llama2.py
* eval_palm.py
* eval_starcoder.py
* eval_vicuna.py
* eval_wizardcoder.py

每个代码中包含所有任务：

* add_smell()
* add_diff_tag()
* add_review_comment()
* add_hidden_unit_tests()
* add_summarization()
* add_time_optimization()
* add_mem_optimization()
* ......

TODO: 补全

#### 3. executors

该目录下存放code_test和code_optimization的编译执行器。

TODO: 补全

#### 4. logs

该目录下存放评估LLMs的日志。

TODO: 补全

#### 5. results

该目录下存放LLMs提取出来的结果。

TODO: 补全

#### 6. scorers

该目录下存放计分LLMs结果的代码：

* score_code_review.py
* score_code_smell.py
* score_code_test.py
* score_code_summarization.jsonl
* score_code_optimization.jsonl
* score_code_translation.jsonl
* score_code_repair.jsonl
* score_program_synthesis.jsonl

TODO: 补全

#### 7. scripts

该目录下存放一些工具脚本。

---

### 项目使用

#### 1. Installation

1. `cd llm-code-eval`
2. install python>=3.9 (we only guarantee the code works on python 3.9)
3. install torch based on your cuda version
4. `pip install -r requirements.txt`
5. optional: install GNU C, GNU C++, Mono C#, Java 8 if you want to run code_test and code_optimization
   
TODO：建议把‘项目使用’下面的目录结构改为 安装，推理evaluator，打分scorer
#### 2. Inference
#### 3. Scoring
##### Code Optimization
Pipeline of evaluating LLM's performance of code optimization:
0. Install Python 3, GNU C, GNU C++, Mono C# environment on your device.
1. Run the inference scripts in the `evaluators` folder to get the inference results of the targeted model. The inference results ({time/mem}_code_opt_data_{modelname}.jsonl) will be saved in the `results/raw` folder.
2. Run `python save_opt_codes.py --code_test_data_name mem_code_opt_eval_{modelname}.jsonl --codes_dir_name {modelname}_opt_codes --opt_type mem --parse_code` and `python save_opt_codes.py --code_test_data_name time_code_opt_eval_{modelname}.jsonl --codes_dir_name {modelname}_opt_codes --opt_type time --parse_code` to save the parsed optimized codes in the `results/ans/{modelname}_opt_codes` folder.
3. Run `python test_opt_codes.py --code_test_data_name mem_code_opt_eval_{modelname}.jsonl --codes_dir_name {modelname}_opt_codes --opt_type mem` and `python test_opt_codes.py --code_test_data_name time_code_opt_eval_{modelname}.jsonl --codes_dir_name {modelname}_opt_codes --opt_type time` to execute the parsed optimized codes and get the execution time and memory usage. The performance metrics of each code snippet will be saved back to the parent folder of the code file under `results/ans/{modelname}_opt_codes`.
4. Go to `scores` folder and run `python score_code_optimization.py --codes_dir_name opt_{modelname}_codes > opt_scores/cal_{modelname}_metrics.log`. This will calculate the pass@5 and opt@5 scores of the targeted model. And these results will be placed at  `scorers/opt_scores/`.
##### Code Summarization
Go to the `scorer` folder and run `python score_code_summarization.py` to get the scores of the model inference results, the results will be palced at `scorers/summ_scores/`.
------- wyk分割线 -------
#### 2. PaLM

Replace "google_api_key" with your own Google API key.

1. For code
   review: `python evaluators/eval_palm.py --api_key google_api_key --data_load_name code_review_data.jsonl --result_save_name code_review_eval_palm.jsonl --log_file_name code_review_eval_palm.log`
2. For code
   smell: `python evaluators/eval_palm.py --api_key google_api_key --data_load_name code_smell_data.jsonl --result_save_name code_smell_eval_palm.jsonl --log_file_name code_smell_eval_palm.log`
3. For code
   test: `python evaluators/eval_palm.py --api_key google_api_key --data_load_name code_test_data.jsonl --result_save_name code_test_data_palm.jsonl --log_file_name code_test_data_palm.log`
4. For code
   summarization: `python evaluators/eval_palm.py --api_key google_api_key --data_load_name code_summarization_data.jsonl --result_save_name code_summarization_eval_palm.jsonl --log_file_name code_summarization_eval_palm.log`
5. For code
   optimization: `python evaluators/eval_palm.py --api_key google_api_key --data_load_name code_optimization_data.jsonl --result_save_name code_optimization_eval_palm.jsonl --log_file_name code_optimization_eval_palm.log`

#### 3. GPT-3.5

Replace "openai_api_key" with your own OpenAI API key.

1. For code
   review: `python evaluators/eval_gpt.py --api_key openai_api_key --model gpt-3.5-turbo-0613 --data_load_name code_review_data.jsonl --result_save_name code_review_eval_gpt3.jsonl --log_file_name code_review_eval_gpt3.log`
2. For code
   smell: `python evaluators/eval_gpt.py --api_key openai_api_key --model gpt-3.5-turbo-0613 --data_load_name code_smell_data.jsonl --result_save_name code_smell_eval_gpt3.jsonl --log_file_name code_smell_eval_gpt3.log`
3. For code
   test: `python evaluators/eval_gpt.py --api_key openai_api_key --model gpt-3.5-turbo-0613 --data_load_name code_test_data.jsonl --result_save_name code_test_data_gpt3.jsonl --log_file_name code_test_data_gpt3.log`
4. For code
   summarization: `python evaluators/eval_gpt.py --api_key openai_api_key --model gpt-3.5-turbo-0613 --data_load_name code_summarization_data.jsonl --result_save_name code_summarization_eval_gpt3.jsonl --log_file_name code_summarization_eval_gpt3.log`
5. For code
   optimization: `python evaluators/eval_gpt.py --api_key openai_api_key --model gpt-3.5-turbo-0613 --data_load_name code_optimization_data.jsonl --result_save_name code_optimization_eval_gpt3.jsonl --log_file_name code_optimization_eval_gpt3.log`

#### 4. GPT-4

Replace "openai_api_key" with your own OpenAI API key.

1. For code
   review: `python evaluators/eval_gpt.py --api_key openai_api_key --model gpt-4-0613 --data_load_name code_review_data.jsonl --result_save_name code_review_eval_gpt4.jsonl --log_file_name code_review_eval_gpt4.log`
2. For code
   smell: `python evaluators/eval_gpt.py --api_key openai_api_key --model gpt-4-0613 --data_load_name code_smell_data.jsonl --result_save_name code_smell_eval_gpt4.jsonl --log_file_name code_smell_eval_gpt4.log`
3. For code
   test: `python evaluators/eval_gpt.py --api_key openai_api_key --model gpt-4-0613 --data_load_name code_test_data.jsonl --result_save_name code_test_data_gpt4.jsonl --log_file_name code_test_data_gpt4.log`
4. For code
   summarization: `python evaluators/eval_gpt.py --api_key openai_api_key --model gpt-4-0613 --data_load_name code_summarization_data.jsonl --result_save_name code_summarization_eval_gpt4.jsonl --log_file_name code_summarization_eval_gpt4.log`
5. For code
   optimization: `python evaluators/eval_gpt.py --api_key openai_api_key --model gpt-4-0613 --data_load_name code_optimization_data.jsonl --result_save_name code_optimization_eval_gpt4.jsonl --log_file_name code_optimization_eval_gpt4.log`

#### 5. CodeLLaMA

Replace "access_token" with your own HuggingFace access token.

Replace "cache_dir" with path to a directory in which a downloaded pretrained model should be cached.

1. For code
   review: `python evaluators/eval_codellama.py --access_token access_token --cache_dir cache_dir --checkpoint codellama/CodeLlama-34b-Instruct-hf --data_load_name code_review_data.jsonl --result_save_name code_review_eval_codellama.jsonl --log_file_name code_review_eval_codellama.log`
2. For code
   smell: `python evaluators/eval_codellama.py --access_token access_token --cache_dir cache_dir --checkpoint codellama/CodeLlama-34b-Instruct-hf --data_load_name code_smell_data.jsonl --result_save_name code_smell_eval_codellama.jsonl --log_file_name code_smell_eval_codellama.log`
3. For code
   test: `python evaluators/eval_codellama.py --access_token access_token --cache_dir cache_dir --checkpoint codellama/CodeLlama-34b-Instruct-hf --data_load_name code_test_data.jsonl --result_save_name code_test_data_codellama.jsonl --log_file_name code_test_data_codellama.log`
4. For code
   summarization: `python evaluators/eval_codellama.py --access_token access_token --cache_dir cache_dir --checkpoint codellama/CodeLlama-34b-Instruct-hf --data_load_name code_summarization_data.jsonl --result_save_name code_summarization_eval_codellama.jsonl --log_file_name code_summarization_eval_codellama.log`
5. For code
   optimization: `python evaluators/eval_codellama.py --access_token access_token --cache_dir cache_dir --checkpoint codellama/CodeLlama-34b-Instruct-hf --data_load_name code_optimization_data.jsonl --result_save_name code_optimization_eval_codellama.jsonl --log_file_name code_optimization_eval_codellama.log`

#### 6. Vicuna

Replace "access_token" with your own HuggingFace access token.

Replace "cache_dir" with path to a directory in which a downloaded pretrained model should be cached.

1. For code
   review: `python evaluators/eval_vicuna.py --access_token access_token --cache_dir cache_dir --checkpoint lmsys/vicuna-13b-v1.5-16k --data_load_name code_review_data.jsonl --result_save_name code_review_eval_vicuna.jsonl --log_file_name code_review_eval_vicuna.log`
2. For code
   smell: `python evaluators/eval_vicuna.py --access_token access_token --cache_dir cache_dir --checkpoint lmsys/vicuna-13b-v1.5-16k --data_load_name code_smell_data.jsonl --result_save_name code_smell_eval_vicuna.jsonl --log_file_name code_smell_eval_vicuna.log`
3. For code
   test: `python evaluators/eval_vicuna.py --access_token access_token --cache_dir cache_dir --checkpoint lmsys/vicuna-13b-v1.5-16k --data_load_name code_test_data.jsonl --result_save_name code_test_data_vicuna.jsonl --log_file_name code_test_data_vicuna.log`
4. For code
   summarization: `python evaluators/eval_vicuna.py --access_token access_token --cache_dir cache_dir --checkpoint lmsys/vicuna-13b-v1.5-16k --data_load_name code_summarization_data.jsonl --result_save_name code_summarization_eval_vicuna.jsonl --log_file_name code_summarization_eval_vicuna.log`
5. For code
   optimization: `python evaluators/eval_vicuna.py --access_token access_token --cache_dir cache_dir --checkpoint lmsys/vicuna-13b-v1.5-16k --data_load_name code_optimization_data.jsonl --result_save_name code_optimization_eval_vicuna.jsonl --log_file_name code_optimization_eval_vicuna.log`

#### 7. LLaMA2

Replace "access_token" with your own HuggingFace access token.

Replace "cache_dir" with path to a directory in which a downloaded pretrained model should be cached.

1. For code
   review: `python evaluators/eval_llama2.py --access_token access_token --cache_dir cache_dir --checkpoint meta-llama/Llama-2-70b-chat-hf --data_load_name code_review_data.jsonl --result_save_name code_review_eval_llama2.jsonl --log_file_name code_review_eval_llama2.log`
2. For code
   smell: `python evaluators/eval_llama2.py --access_token access_token --cache_dir cache_dir --checkpoint meta-llama/Llama-2-70b-chat-hf --data_load_name code_smell_data.jsonl --result_save_name code_smell_eval_llama2.jsonl --log_file_name code_smell_eval_llama2.log`
3. For code
   test: `python evaluators/eval_llama2.py --access_token access_token --cache_dir cache_dir --checkpoint meta-llama/Llama-2-70b-chat-hf --data_load_name code_test_data.jsonl --result_save_name code_test_data_llama2.jsonl --log_file_name code_test_data_llama2.log`
4. For code
   summarization: `python evaluators/eval_llama2.py --access_token access_token --cache_dir cache_dir --checkpoint meta-llama/Llama-2-70b-chat-hf --data_load_name code_summarization_data.jsonl --result_save_name code_summarization_eval_llama2.jsonl --log_file_name code_summarization_eval_llama2.log`
5. For code
   optimization: `python evaluators/eval_llama2.py --access_token access_token --cache_dir cache_dir --checkpoint meta-llama/Llama-2-70b-chat-hf --data_load_name code_optimization_data.jsonl --result_save_name code_optimization_eval_llama2.jsonl --log_file_name code_optimization_eval_llama2.log`

#### 8. WizardCoder

Replace "access_token" with your own HuggingFace access token.

Replace "cache_dir" with path to a directory in which a downloaded pretrained model should be cached.

1. For code
   review: `python evaluators/eval_wizardcoder.py --access_token access_token --cache_dir cache_dir --checkpoint WizardLM/WizardCoder-15B-V1.0 --data_load_name code_review_data.jsonl --result_save_name code_review_eval_wizardcoder.jsonl --log_file_name code_review_eval_wizardcoder.log`
2. For code
   smell: `python evaluators/eval_wizardcoder.py --access_token access_token --cache_dir cache_dir --checkpoint WizardLM/WizardCoder-15B-V1.0 --data_load_name code_smell_data.jsonl --result_save_name code_smell_eval_wizardcoder.jsonl --log_file_name code_smell_eval_wizardcoder.log`
3. For code
   test: `python evaluators/eval_wizardcoder.py --access_token access_token --cache_dir cache_dir --checkpoint WizardLM/WizardCoder-15B-V1.0--data_load_name code_test_data.jsonl --result_save_name code_test_data_wizardcoder.jsonl --log_file_name code_test_data_wizardcoder.log`
4. For code 
   summarization: `python evaluators/eval_wizardcoder.py --access_token access_token --cache_dir cache_dir --checkpoint WizardLM/WizardCoder-15B-V1.0 --data_load_name code_summarization_data.jsonl --result_save_name code_summarization_eval_wizardcoder.jsonl --log_file_name code_summarization_eval_wizardcoder.log`
5. For code
   optimization: `python evaluators/eval_wizardcoder.py --access_token access_token --cache_dir cache_dir --checkpoint WizardLM/WizardCoder-15B-V1.0 --data_load_name code_optimization_data.jsonl --result_save_name code_optimization_eval_wizardcoder.jsonl --log_file_name code_optimization_eval_wizardcoder.log`

#### 9. StarCoder

Replace "access_token" with your own HuggingFace access token.

Replace "cache_dir" with path to a directory in which a downloaded pretrained model should be cached.

1. For code
   review: `python evaluators/eval_starcoder.py --access_token access_token --cache_dir cache_dir --checkpoint HuggingFaceH4/starchat-beta --data_load_name code_review_data.jsonl --result_save_name code_review_eval_starcoder.jsonl --log_file_name code_review_eval_starcoder.log`
2. For code
   smell: `python evaluators/eval_starcoder.py --access_token access_token --cache_dir cache_dir --checkpoint HuggingFaceH4/starchat-beta --data_load_name code_smell_data.jsonl --result_save_name code_smell_eval_starcoder.jsonl --log_file_name code_smell_eval_starcoder.log`
3. For code
   test: `python evaluators/eval_starcoder.py --access_token access_token --cache_dir cache_dir --checkpoint HuggingFaceH4/starchat-beta --data_load_name code_test_data.jsonl --result_save_name code_test_data_starcoder.jsonl --log_file_name code_test_data_starcoder.log`
4. For code
   summarization: `python evaluators/eval_starcoder.py --access_token access_token --cache_dir cache_dir --checkpoint HuggingFaceH4/starchat-beta --data_load_name code_summarization_data.jsonl --result_save_name code_summarization_eval_starcoder.jsonl --log_file_name code_summarization_eval_starcoder.log`
5. For code
   optimization: `python evaluators/eval_starcoder.py --access_token access_token --cache_dir cache_dir --checkpoint HuggingFaceH4/starchat-beta --data_load_name code_optimization_data.jsonl --result_save_name code_optimization_eval_starcoder.jsonl --log_file_name code_optimization_eval_starcoder.log`
