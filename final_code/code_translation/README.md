# Code Translation


## Data
The code translation dataset is located in `data/code_translation_data.jsonl`. The fields of the data are explained below:

| Field                	          | Explanation                                          	                  |
|---------------------------------|-------------------------------------------------------------------------|
| `id`                   	        | The local ID in the task                             	                  |
| `src_uid`              	        | Unique identifier of the problem                     	                  |
| `source_code`                   | Buggy code submitted by human                                           |
| `source_lang_cluster`         	 | The programming language that source code used                   	      |
| `target_lang_cluster`         	 | The programming language that target code should be                     |
| `difficulty`           	        | Difficulty of the problem                            	                  |
| `testcases`            	        | List of testcases of the coding problem           	                     |



## Dependence (Could share with all other generation tasks)
1. `cd code_translation`
2. install `python>=3.9` (we use `python==3.9`)
3. install `pytorch` (we use `pytorch==2.1.1`) based on your cuda version
4. `pip install -r requirement.txt`



## Inference
Run the inference scripts to get the inference results of the targeted LLMs. The inference results `code_translation_result_{model_name}.jsonl` will be saved under the `inference/results` folder. The inference logs `code_translation_log_{model_name}.log` will be saved under the `inference/logs` folder.

### Closed-sourced LLMs

We provide the following closed-sourced LLMs inference scripts for you:


| Model Name | Model Version      | Script Name  |
| ---------- | ------------------ | ------------ |
| PaLM 2     | text-bison-001     | run_palm2.py |
| GPT-4      | gpt-4-0613         | run_gpt.py   |
| GPT-3.5    | gpt-3.5-turbo-0613 | run_gpt.py   |

For PaLM 2, you can run the following command by replacing `google_api_key` with your own Google API key. 

```angular2html
python run_palm.py
    --api_key your_palm_api_key
    --data_load_name code_translation_data.jsonl
    --candidate_num 1
    --result_save_name code_translation_run_palm.jsonl
    --log_file_name code_translation_run_palm.log
```

For GPT-4 and GPT-3.5, you can run the following command by replacing `openai_api_key` with your own OpenAI API key, `model_version` with specific model version.

```angular2html
python run_gpt.py
    --api_key your_openai_apikey
    --model model_specific_version
    --data_load_name code_translation_data.jsonl
    --candidate_num 1
    --result_save_name code_translation_run_{model_name}.jsonl
    --log_file_name code_translation_run_{model_name}.log
```


### Open-sourced LLMs

We provide the following open-sourced LLMs inference scripts for you:


| Model Name  | Model Checkpoint                    | Script Name        |
| ----------- | ----------------------------------- | ------------------ |
| Code LLaMA  | codellama/CodeLlama-34b-Instruct-hf | run_codellama.py   |
| LLaMA 2     | meta-llama/Llama-2-70b-chat-hf      | run_llama2.py      |
| StarCoder   | HuggingFaceH4/starchat-beta         | run_starcoder.py   |
| Vicuna      | lmsys/vicuna-13b-v1.5-16k           | run_vicuna.py      |
| WizardCoder | WizardLM/WizardCoder-15B-V1.0       | run_wizardcoder.py |

For HuggingFace models, you can run the following command by replacing `huggingface_access_token` with your own HuggingFace access token, `cache_dir` with path to a directory in which a downloaded pretrained model and tokenizer should be cached, `model_checkpoint` with specific model checkpoint.


```angular2html
python run_{model_name}.py 
    --access_token access_token
    --cache_dir cache_dir 
    --checkpoint your_model_ckpt
    --data_load_name code_translation_data.jsonl
    --candidate_num 1
    --result_save_name code_translation_run_{model_name}.jsonl
    --log_file_name code_translation_run_{model_name}.log
```



## Executor 
### Evironment Setup (same as code repair and program synthesis)

Programs written in Perl, D, and Delphi that need to run on **Windows** require the following dependencies to be installed:

#### Perl Dependencies:

Create a conda environment named `myenv`
```
conda create -n myenv python=3.8
conda activate myenv
conda install -c conda-forge perl
```
Validate the correctness of installation
```
perl -v
touch myscript.pl
perl myscript.pl
```
#### D Dependencies:

Download [dmd 2.105.0](https://downloads.dlang.org/releases/2.x/2.105.0/) for windows and unzip it to a suitable location. Replace `d_path` in run.py

#### Delphi Dependencies:

Download [delphi 7](http://altd.embarcadero.com/download/delphi/d7/english/ent/delphi_7_ent_en.iso) and install it to a suitable location. Replace `delphi_path` in run.py

***

Programs written in **other languages** need to be run using the ExecEval project, and the following dependencies need to be installed:

### ExecEval Dependencies:

1. [docker-ce](https://docs.docker.com/engine/install/)
2. Refer to the guidelines in the **Steps** section of the [ExecEval](https://github.com/ntunlp/ExecEval) project to start the service.


The code ready for testing should be stored line by line in your\_codes.jsonl and the file should be placed in your\_codes\_dir. A typical code record is shown below and should contain at least the following keys:

```
{
    "lang_cluster": "{model_name}",
    "lang": "{model_name}",
    "source_code": "{model_name}",
    "src_uid": "{model_name}",
    "difficulty": 800,
    "testcases": "[{'input': 'input1', 'output': ['output1']}, {'input': 'input2', 'output': ['output2']}]"
}
```


* For all programming languages except Perl, D, and Delphi, example of most typical usage:
    `python run_execeval.py --codes_dir your_codes_dir --results_dir your_results_dir --code_filename your_codes.jsonl`
<br>
    The results of the run are output to `your_results_dir`, forming a jsonl file, which compares the input jsonl, with each new entry adding the results of each test case run, stored in the `testcases`
* For Perl, D, and Delphi, example of most typical usage:
    `conda activate myenv`
    `python run.py  --code_path your_codes_{program_language}.jsonl --output_path result/results.json --cmd_path your_cmd_path `
<br>
    Please change the `--code_path` with `perl/d/delphi`. The execute results are saved to `--output_path`, which records the results of `accepted`, `wrong`, and `error` for each key, and each output records the possible error outputs and the type of error.

## Evaluation

After the execution, we provide a *scorer* script to count the number of correct solutions around different languages and difficulties. 

Run following command to count the results generated by `{model_name}`: 

`python score_code_translation.py --result_dir your_result_dir --model_name model_name`

It will export two sheets for Easy and Hard problems count by different languages.