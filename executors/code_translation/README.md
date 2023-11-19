## Evironment Setup 

Programs written in perl, d, and delphi that need to run on windows require the following dependencies to be installed, Before running run.py, you need to check the paths in the code one by one to make sure they are what you want them to be.:

### Perl Dependencies:

Creating a conda environment named `myperl`
`conda create -n myperl python=3.8`
`conda activate myperl`
`conda install -c conda-forge perl`
Test the success of the installation
`perl -v`
`touch myscript.pl`
`perl myscript.pl`

### D Dependencies:

Download [dmd 2.105.0](https://downloads.dlang.org/releases/2.x/2.105.0/) for windows and unzip it to a suitable location. Replace `DMDPath` in run.py

### Delphi Dependencies:

Download [delphi 7](http://altd.embarcadero.com/download/delphi/d7/english/ent/delphi_7_ent_en.iso) and install it to a suitable location. Replace `DelphiPath` in run.py

***

Programs written in other languages need to be run using the ExecEval project, and the following dependencies need to be installed:

### ExecEval Dependencies:

1. [docker-ce](https://docs.docker.com/engine/install/)
2. Refer to the guidelines in the **Steps** section of the [ExecEval](https://github.com/ntunlp/ExecEval) project to start the service.

## Code Translation (ct)

The code ready for testing should be stored line by line in your\_codes.jsonl and the file should be placed in your\_codes\_dir. A typical code record is shown below and should contain at least the following keys:

```
{
    "lang_cluster": "xxx",
    "lang": "xxx",
    "source_code": "xxx",
    "src_uid": "xxx",
    "code_uid": "xxx",
    "difficulty": 800,
    "hidden_unit_tests": "[{'input': 'input1', 'output': ['output1']}, {'input': 'input2', 'output': ['output2']}]"
}
```

To run the code in perl, d, and delphi, you need to prepare your\_testcases.jsonl, which holds the testcase. The testcase and the code record correspond to each other by the same src\_uid. A typical testcase record is shown below and should contain at least the following keys:

```
{
    "src_uid1": [
        {
            "input": [
                "input1"
            ],
            "output": [
                "output1"
            ]
        },
        {
            "input": [
                "input2"
            ],
            "output": [
                "output2"
            ]
        }
    ],
    "src_uid2": [
        {
            "input": [
                "input3"
            ],
            "output": [
                "output3"
            ]
        },
        {
            "input": [
                "input4"
            ],
            "output": [
                "output4"
            ]
        }
    ]
}
```

* For all programming languages except Perl, D, and Delphi, example of most typical usage:
    `python run_execeval.py --codes_dir your_codes_dir --results_dir your_results_dir --path your_codes.jsonl`
<br>
    The results of the run are output to `your_results_dir`, forming a jsonl file, which compares the input jsonl, with each new entry adding the results of each test case run, stored in the `unittests` field
* For Perl, D, and Delphi, example of most typical usage:
    `conda activate myenv`
    `python run.py --testcase_path your_testcases.jsonl --jsonl_path your_codes.jsonl --output_path results.json`
<br>
    The results of the run are output to `results.json`, which records the results of `accepted`, `wrong`, and `error` for each key, and each output records the possible error outputs and the type of error.
