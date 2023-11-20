# Code Repair (PS)

Code repair  mainly includes 3 steps, 1. inference; 2. execute; 3. validate and calculate score. 

## Data
Related data files are `data/code_repair_data.jsonl`

| Field                	   | Explanation                                          	             |
|--------------------------|--------------------------------------------------------------------|
| `id`                   	 | The local ID in the task                             	             |
| `src_uid`              	 | Unique identifier of the problem                     	             |
| `description`          	 | The original problem description in natural language 	             |
| `input_specification`  	 | Description of the form of input data                	             |
| `output_specification` 	 | Description of the form of output data               	             |
| `sample_inputs`        	 | Sample inputs                                        	             |
| `sample_outputs`       	 | Sample outputs                                       	             |
| `notes`                	 | Additional note for the problem                              	     |
| `source_code`            | Buggy code submitted by human                                      |
| `execute_outcome`         | The execute outcome of the buggy code                              |
| `lang_cluster`         	 | The programming language that buggy code used                    	 |
| `lang`                   | The specific programming language version of buggy code            |
| `difficulty`           	 | Difficulty of the problem                            	             |
| `human_solution`       	 | Accepted human solution                              	             |
| `testcases`            	 | List of testcases of the problem           	                       |

 
## Inference
#### Dependence (Could share with all other generation tasks)
1. `cd code_repair`
2. install `python>=3.9` (we use `python==3.9`)
3. install `pytorch` (we use `pytorch==2.1.1`) based on your cuda version
4. `pip install -r requirement.txt`

Here are detailed commands to run the inference:  
#### GPT3.5 & GPT4
```angular2html
python run_gpt.py
    --api_key
    your_openai_apikey
    --model
    model_specific_version
    --data_load_name
    code_repair_data.jsonl
    --candidate_num
    1
    --result_save_name
    code_repair_run_{model_name}.jsonl
    --log_file_name
    code_repair_run_{model_name}.log
```
#### PaLM 2

```angular2html
python run_palm.py
    --api_key
    your_palm_api_key
    --data_load_name
    code_repair_data.jsonl
    --candidate_num
    1
    --result_save_name
    code_repair_run_palm.jsonl
    --log_file_name
    code_repair_run_palm.log
```
#### Other open-sourced LLMs on Huggingface (CodeLLaMA, LLaMA 2, StarCoder, Vicuna, WizardCoder, etc.)
Replace ``access_token`` with your own HuggingFace access token, ``{model_name}`` with model name, choose the corresponding model checkpoint as ``your_model_ckpt``
```angular2html
python run_{model_name}.py 
    --access_token
    access_token
    --cache_dir 
    cache_dir 
    --checkpoint
    your_model_ckpt
    --data_load_name
    code_repair_data.jsonl
    --candidate_num
    1
    --result_save_name
    code_repair_run_{model_name}.jsonl
    --log_file_name
    code_repair_run_{model_name}.log
```



## Executor 
### Evironment Setup (same as program synthesis and code translation)

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

## Scorer

After the execution, we provide a *scorer* script to count the number of correct solutions around different languages and difficulties. 

Run following command to count the results generated by `{model_name}`: 

`python score_code_repair.py --result_dir your_result_dir --model_name model_name`
