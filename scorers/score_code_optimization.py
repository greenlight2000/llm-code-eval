import os
from pathlib import Path
import pandas as pd
import re
import argparse
import numpy as np

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--codes_dir_name', default='palm_opt_parse', type=str, choices=['vicuna_opt_codes', 'wizardcoder_opt_codes', 'codellama_opt_codes', 'gpt4_opt_codes', 'gpt3_opt_codes', 'starcoder_opt_codes', 'llama2_opt_codes', 'palm_opt_codes']) # same as --codes_dir_name in test_opt_codes. the codes performance will be gathered directly from './codes/{args.codes_dir_name}/{lang_cluster}/{code_uid}/codes_perf.csv'
    args = parser.parse_args()
    return args

def main():
    metrcs_df = []
    print(f'Start to evaluate optimized codes performance for {model_name}...\n')
    for lang in ['c','cpp','python','cs']:#,'cs']:#,'cs'
        for opt_type in ['mem','time']:
            perf_key = 'mean_peak_mem' if opt_type == 'mem' else 'mean_cpu_time'
            perf_unit = 'kb' if opt_type == 'mem' else 's'
            err_flag = False# 防止有些语言在test_opt_codes.py没有测试完全，没有生成codes_perf.csv
            pass_rate = 0
            success_opt_rate = 0
            lang_dir = load_dir / Path(model_name) / Path(opt_type) / Path(lang)
            src_dirs = os.listdir(lang_dir)
            for src_dir in src_dirs:
                print(f">> calculating {lang}-{src_dir} performance metrics:")
                # 判断文件是否存在
                if not os.path.exists(lang_dir / Path(src_dir) / Path('codes_perf.csv')):# or not os.path.exists(lang_dir / Path(src_dir) / Path('codes_perf2.csv')):
                    print('------------------------------------')
                    print(f"{lang}-{opt_type} is not fully tested")
                    print('------------------------------------')
                    err_flag = True
                    break
                df = pd.read_csv(lang_dir / Path(src_dir) / Path('codes_perf.csv'),index_col=0)

                unopt = df.loc['unopt']
                if opt_type == 'mem':
                    if "[" in unopt['mean_peak_mem']:
                        s = re.sub(r'\s+', ' ', unopt['mean_peak_mem'])
                        perf_li = s.replace("]","").replace("[","").strip().split(' ')
                        s = "0.00e+00"
                        num = float(s)
                        perf_li = [float(x) for x in perf_li]
                    else:
                        perf_li = [float(x) for x in unopt['mean_peak_mem'].split(',')]
                elif opt_type == 'time':
                    if "[" in unopt['mean_cpu_time']:
                        s = re.sub(r'\s+', ' ', unopt['mean_cpu_time'])
                        perf_li = s.replace("]","").replace("[","").strip().split(' ')
                        perf_li = [float(x) for x in perf_li]
                    else:
                        perf_li = [float(x) for x in unopt['mean_cpu_time'].split(',')]
                unopt_low_bound = min(perf_li)
                unopt_perf = sum(perf_li)/len(perf_li)
                unopt_perf_dev = np.std(perf_li)

                print(f"unopt {opt_type} performance: {unopt_perf}+-{unopt_perf_dev} {perf_unit}")
                
                # 获取generated code 性能，统计通过率和性能优化率
                pass_flag = False
                opt_flag = False
                for opt_idx in range(5):
                    opt = df.loc[f'opt{opt_idx}']
                    if opt['pass_rate'] == 100.0:
                        pass_flag = True
                        opt_perf = float(opt[perf_key])
                        if opt_perf < unopt_low_bound:
                            print(f'opt{opt_idx} {opt_type} performance: {opt_perf}. success to opt {unopt_perf - opt_perf} {perf_unit}, opt rate: {(unopt_perf - opt_perf) / unopt_perf}%')
                            opt_flag = True
                        else:
                            print(f'opt{opt_idx} {opt_type} performance: {opt_perf}. failed to opt')
                if pass_flag:
                    pass_rate += 1
                if opt_flag:
                    success_opt_rate += 1
            if err_flag:
                continue
            print('------------------------------------')
            print(f'{lang} {opt_type} pass_rate: {pass_rate/len(src_dirs)}')
            print(f'{lang} {opt_type} success_opt_rate: {success_opt_rate/len(src_dirs)}')
            print('------------------------------------')
            metrcs_df.append([model_name,lang,opt_type,pass_rate/len(src_dirs),success_opt_rate/len(src_dirs)])
    metrcs_df = pd.DataFrame(metrcs_df,columns=['model_name','lang','opt_type','pass_rate','success_opt_rate'])
    metrcs_df.to_csv(output_dir / Path(f'{model_name}_metrics.csv'),index=False)
if __name__ == '__main__':
    args = parse_arguments()
    model_name = args.codes_dir_name
    load_dir = Path(__file__).parent.parent / Path('codes')
    output_dir = Path(__file__).parent
    main()
# python cal_metrics.py --codes_dir_name palm_opt_parse > cal_palm_metrics.log


