import os
import re
import argparse
import subprocess

from pathlib import Path
from datasets import load_dataset


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--code_test_data_name', default='repair_code_test_data_starcoder.jsonl',
                        choices=[
                            'repair_code_test_data_codellama.jsonl',
                            'repair_code_test_data_gpt3.jsonl',
                            'repair_code_test_data_gpt4.jsonl',
                            'repair_code_test_data_llama2.jsonl',
                            'repair_code_test_data_palm.jsonl',
                            'repair_code_test_data_starcoder.jsonl'
                            'repair_code_test_data_vicuna.jsonl',
                            'repair_code_test_data_wizardcoder.jsonl'
                        ], type=str)
    parser.add_argument('--codes_dir_name', default='starcoder_codes',
                        choices=[
                            'codellama_codes',
                            'gpt3_codes',
                            'gpt4_codes',
                            'llama2_codes',
                            'palm_codes',
                            'starcoder_codes',
                            'vicuna_codes',
                            'wizardcoder_codes'
                        ], type=str)
    parser.add_argument('--temp_save_name', default='starcoder_data',
                        choices=[
                            'codellama_data',
                            'gpt3_data',
                            'gpt4_data',
                            'llama2_data',
                            'palm_data',
                            'starcoder_data',
                            'vicuna_data',
                            'wizardcoder_data'
                        ], type=str)
    args = parser.parse_args()

    return args


def execute_command(command, input=None):
    if input is not None:
        input = input.replace('\r\n', '\n')
    try:
        # References: https://stackoverflow.com/questions/66480855/python-subprocess-run-timeout-behaving-differently-on-windows-vs-linux
        outcome = subprocess.run(command, input=input, capture_output=True, text=True, timeout=20, shell=False)
    except Exception as e:
        print('Error occurred while executing command:', e)
        outcome = subprocess.CompletedProcess(args=command, returncode=-1, stdout='', stderr=str(e))
    return outcome


def add_pass_rate(example):
    lang_cluster = example['lang_cluster']
    code_uid = example['code_uid']
    source_code = example['source_code']
    hidden_unit_tests = eval(example['hidden_unit_tests'])
    num_hidden_unit_tests = len(hidden_unit_tests)

    # LLM failed to generate hidden unit tests
    if num_hidden_unit_tests == 0:
        print('Failed to generate hidden unit tests:', code_uid)
        example['pass_rate'] = 0.00
    else:
        if lang_cluster == 'C':
            os.chdir(f'codes/{args.codes_dir_name}/c/{code_uid}')
            print(os.getcwd())

            compile_command = 'gcc -fprofile-arcs -ftest-coverage -fPIC -O0 code.c -o code'
            outcome = execute_command(compile_command)
            print(outcome)

            num_passed = 0
            for index, hidden_unit_test in enumerate(hidden_unit_tests):
                input = hidden_unit_test['input']
                output = hidden_unit_test['output']

                test_command = 'code'
                outcome = execute_command(test_command, input)
                print(outcome)

                is_passed = True if outcome.returncode == 0 and (
                        outcome.stdout in output or outcome.stdout.rstrip() in output or outcome.stdout.replace('\n',
                                                                                                                '\r\n') in output or outcome.stdout.replace(
                    '\n', '\r\n').rstrip() in output) else False
                if is_passed is True:
                    num_passed += 1
                print(is_passed)

                coverage_command = f'gcovr --json test-{index}.json'
                outcome = execute_command(coverage_command)
                print(outcome)

            pass_rate = round(100. * num_passed / num_hidden_unit_tests, 2)
            print(f'Pass rate: {pass_rate}% [{num_passed}/{num_hidden_unit_tests}]')

            line_coverage_report_text_command = 'gcovr --add-tracefile "test-*.json" --txt'
            outcome = execute_command(line_coverage_report_text_command)
            print(outcome.stdout)

            branch_coverage_report_text_command = 'gcovr --add-tracefile "test-*.json" --branches --txt'
            outcome = execute_command(branch_coverage_report_text_command)
            print(outcome.stdout)

            coverage_report_json_command = 'gcovr --add-tracefile "test-*.json" --json-summary coverage.json'
            outcome = execute_command(coverage_report_json_command)
            print(outcome)

            coverage_report_html_command = 'gcovr --add-tracefile "test-*.json" --html-details coverage.html'
            outcome = execute_command(coverage_report_html_command)
            print(outcome)

            os.chdir('../../../..')
            print(os.getcwd())

            example['pass_rate'] = pass_rate

        elif lang_cluster == 'C++':
            os.chdir(f'codes/{args.codes_dir_name}/cpp/{code_uid}')
            print(os.getcwd())

            compile_command = 'g++ -fprofile-arcs -ftest-coverage -fPIC -O0 code.cpp -o code'
            outcome = execute_command(compile_command)
            print(outcome)

            num_passed = 0
            for index, hidden_unit_test in enumerate(hidden_unit_tests):
                input = hidden_unit_test['input']
                output = hidden_unit_test['output']

                test_command = 'code'
                outcome = execute_command(test_command, input)
                print(outcome)

                is_passed = True if outcome.returncode == 0 and (
                        outcome.stdout in output or outcome.stdout.rstrip() in output or outcome.stdout.replace('\n',
                                                                                                                '\r\n') in output or outcome.stdout.replace(
                    '\n', '\r\n').rstrip() in output) else False
                if is_passed is True:
                    num_passed += 1
                print(is_passed)

                coverage_command = f'gcovr --json test-{index}.json'
                outcome = execute_command(coverage_command)
                print(outcome)

            pass_rate = round(100. * num_passed / num_hidden_unit_tests, 2)
            print(f'Pass rate: {pass_rate}% [{num_passed}/{num_hidden_unit_tests}]')

            line_coverage_report_text_command = 'gcovr --add-tracefile "test-*.json" --txt'
            outcome = execute_command(line_coverage_report_text_command)
            print(outcome.stdout)

            branch_coverage_report_text_command = 'gcovr --add-tracefile "test-*.json" --branches --txt'
            outcome = execute_command(branch_coverage_report_text_command)
            print(outcome.stdout)

            coverage_report_json_command = 'gcovr --add-tracefile "test-*.json" --json-summary coverage.json'
            outcome = execute_command(coverage_report_json_command)
            print(outcome)

            coverage_report_html_command = 'gcovr --add-tracefile "test-*.json" --html-details coverage.html'
            outcome = execute_command(coverage_report_html_command)
            print(outcome)

            os.chdir('../../../..')
            print(os.getcwd())

            example['pass_rate'] = pass_rate

        elif lang_cluster == 'Java':
            os.chdir(f'codes/{args.codes_dir_name}/java/{code_uid}')
            print(os.getcwd())

            # find class name in the java source code
            pattern = r'public\s+(?:final\s+)?class\s+(\w+)'
            matches = re.search(pattern, source_code)
            if matches:
                class_name = matches.group(1)
            else:
                print('Class name not found, use default class name.')
                class_name = 'code'

            compile_command = f'javac {class_name}.java'
            outcome = execute_command(compile_command)
            print(outcome)

            num_passed = 0
            for index, hidden_unit_test in enumerate(hidden_unit_tests):
                input = hidden_unit_test['input']
                output = hidden_unit_test['output']

                test_command = f'java -javaagent:../../../../jars/jacocoagent.jar=destfile=test.exec,append=true {class_name}'
                outcome = execute_command(test_command, input)
                print(outcome)

                is_passed = True if outcome.returncode == 0 and (
                        outcome.stdout in output or outcome.stdout.rstrip() in output or outcome.stdout.replace('\n',
                                                                                                                '\r\n') in output or outcome.stdout.replace(
                    '\n', '\r\n').rstrip() in output) else False
                if is_passed is True:
                    num_passed += 1
                print(is_passed)

            pass_rate = round(100. * num_passed / num_hidden_unit_tests, 2)
            print(f'Pass rate: {pass_rate}% [{num_passed}/{num_hidden_unit_tests}]')

            coverage_report_csv_command = 'java -jar ../../../../jars/jacococli.jar report test.exec --classfiles . --sourcefiles . --csv coverage.csv'
            outcome = execute_command(coverage_report_csv_command)
            print(outcome)

            coverage_report_html_command = 'java -jar ../../../../jars/jacococli.jar report test.exec --classfiles . --sourcefiles . --html coverage'
            outcome = execute_command(coverage_report_html_command)
            print(outcome)

            os.chdir('../../../..')
            print(os.getcwd())

            example['pass_rate'] = pass_rate

        elif lang_cluster == 'Python':
            os.chdir(f'codes/{args.codes_dir_name}/python/{code_uid}')
            print(os.getcwd())

            num_passed = 0
            for index, hidden_unit_test in enumerate(hidden_unit_tests):
                input = hidden_unit_test['input']
                output = hidden_unit_test['output']

                test_command = 'python code.py'
                outcome = execute_command(test_command, input)
                print(outcome)

                is_passed = True if outcome.returncode == 0 and (
                        outcome.stdout in output or outcome.stdout.rstrip() in output or outcome.stdout.replace('\n',
                                                                                                                '\r\n') in output or outcome.stdout.replace(
                    '\n', '\r\n').rstrip() in output) else False
                if is_passed is True:
                    num_passed += 1
                print(is_passed)

                coverage_command = f'coverage run --branch --append code.py'
                outcome = execute_command(coverage_command, input)
                print(outcome)

            pass_rate = round(100. * num_passed / num_hidden_unit_tests, 2)
            print(f'Pass rate: {pass_rate}% [{num_passed}/{num_hidden_unit_tests}]')

            coverage_report_text_command = 'coverage report --format=text --show-missing --precision=2'
            outcome = execute_command(coverage_report_text_command)
            print(outcome.stdout)

            coverage_report_json_command = 'coverage json -o coverage.json'
            outcome = execute_command(coverage_report_json_command)
            print(outcome)

            coverage_report_html_command = 'coverage html -d coverage'
            outcome = execute_command(coverage_report_html_command)
            print(outcome)

            os.chdir('../../../..')
            print(os.getcwd())

            example['pass_rate'] = pass_rate

    return example


def main():
    load_path = Path(__file__).parent.parent.parent / Path('results') / Path('repair') / Path(
        args.code_test_data_name.split('_')[-1].split('.')[0]) / Path(args.code_test_data_name)
    save_path = Path(__file__).parent.parent / Path('code_test') / Path('data') / Path(args.temp_save_name)

    dataset = load_dataset('json', split='train', data_files=str(load_path))
    print(dataset)

    dataset = dataset.map(add_pass_rate)
    print(dataset)

    dataset.save_to_disk(save_path)


if __name__ == '__main__':
    args = parse_arguments()
    main()
    # python executors/code_test/test_codes.py
