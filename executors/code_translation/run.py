# -*- encoding: utf-8 -*-
'''
@File    :   run.py
@Time    :   2023/09/12 11:01:21
@Author  :   Tingyu LIN 
@Version :   1.0
@Contact :   951060525@qq.com
'''

import json
import argparse
from subprocess import Popen, PIPE
import os
import os.path as osp
import time
import func_timeout
from func_timeout import func_set_timeout

@func_set_timeout(5)
def record_result(output_dict, src_uid, submission_id, difficulty, id, answer, output, outerr, errtype=None):
    output_dict[submission_id] = {}
    output_dict[submission_id]["src_uid"] = src_uid
    output_dict[submission_id]["submission_id"] = submission_id
    if difficulty:
        output_dict[submission_id]["difficulty"] = difficulty
    if id:
        output_dict[submission_id]["id"] = id
    if answer:
        output_dict[submission_id]["answer"] = answer
    if output:
        output_dict[submission_id]["output"] = output
    if outerr:
        output_dict[submission_id]["error"] = outerr
    if errtype:
        output_dict[submission_id]["errtype"] = errtype
    return output_dict


@func_set_timeout(30)
def exe_testcase(source_code, answer, input, lang, postfix, output_dict, collapse_num, total_case, wrong_case, src_uid, submission_id, difficulty,  id, tmps_dir):
    os.environ["DelphiPath"] = "C:\\Program Files (x86)\\Borland\\Delphi7\\Bin"
    os.environ["DMDPath"] = "C:\\Program Files (x86)\\DMD\\dmd2\\windows\\bin"
    os.environ["ProjectPath"] = "F:\\CodeGeneration\\code_translation"
    os.environ["ProjectTempPath"] = "F:\\CodeGeneration\\code_translation\\" + tmps_dir + "\\"
    tmps_path = "F:\\CodeGeneration\\code_translation\\" + tmps_dir + "\\"
    if not osp.exists(tmps_path):
        os.mkdir(tmps_path)

    record = 0
    err = 0
    outlog = None
    outerr = None
    errtype = None
    if lang == "d":
        p = Popen('cd "%DMDPath%"', shell=True)
        try:
            cmmond_line = '"C:\\Windows\\SysWow64\\cmd.exe" /c rdmd.exe "%ProjectPath%\\temp.d"'
            p = Popen(cmmond_line, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            p.stdin.write(input.encode())
            p.stdin.flush()
            
            output, outerr = p.communicate()
            output = output.decode()
            if outerr:
                outerr = outerr.decode()
                errtype = "RUNTIME_ERROR"
            total_case += 1

            answer = answer.replace("\r", "")
            answer = answer.replace("\r\n", "\n")
            output = output.replace("\r", "")
            output = output.replace("\r\n", "\n")
        
            output = output.replace(" ", "").lower().strip()
            answer = answer.replace(" ", "").lower().strip()
        except Exception as e:
            print(e, "执行失败 src_uid: ", src_uid)
            err = 1
            errtype = "COMPILATION_ERROR"
            output_dict["error"] = record_result(output_dict["error"], src_uid, submission_id, difficulty, id, answer, None, outerr, errtype)
            record = 1
            wrong_case += 1

    elif lang == "delphi":
        file_path = tmps_path + str(collapse_num)+ '_temp.' + postfix
        collapse_flag = 0

        with open(file_path, 'w', encoding = 'utf-8') as file:
            file.write(source_code)

        try:
            p = Popen('cd "%DelphiPath%"', shell=True)
            cmmond_line = '"C:\\Windows\\SysWow64\\cmd.exe" /c DCC32.EXE "%ProjectTempPath%' + str(collapse_num)+ '_temp.dpr"'# > "%ProjectTempPath%' + str(collapse_num)+ '_compile.log"'
            p = Popen(cmmond_line, stdout=PIPE, shell=True)
            p.wait(1)
            outlog = p.stdout.read()
            if outlog:
                outlog = outlog.decode(encoding="utf-8")
            
        except Exception as e:
            print(e, "编译出错 src_uid: ", src_uid)
            collapse_num += 1
            collapse_flag = 1
            errtype = "COMPILATION_ERROR"

        try:
            cmmond_line = '"C:\\Windows\\SysWow64\\cmd.exe" /c "%ProjectTempPath%' + str(collapse_num)+ '_temp.exe"'
            p = Popen(cmmond_line, stdin=PIPE, stdout=PIPE, shell=True)
            p.stdin.write(input.encode())
            p.stdin.flush()
            p.wait(1)

            os.remove(tmps_path + str(collapse_num)+ "_temp.exe")
            # os.remove(tmps_path + str(collapse_num)+ "_compile.log")
            # print('文件删除成功')
            
        except Exception as e:
            print(e, "执行出错 src_uid: ", src_uid)
            collapse_num += 1
            collapse_flag = 1
            if errtype is None:
                errtype = "RUNTIME_ERROR"
        
        try:
            # cmmond_line = 'type "%ProjectTempPath%' + str(collapse_num)+ '_exe.log"'
            # p = Popen(cmmond_line, stdout=PIPE, shell=True)
            # p.wait(10)
            output, outerr = p.communicate()

            if output is not None:
                output = output.decode(encoding="utf-8")
                answer = answer.replace("\r", "")
                answer = answer.replace("\r\n", "\n")
                output = output.replace("\r", "")
                output = output.replace("\r\n", "\n")
            
                output = output.replace(" ", "").lower().strip()
                answer = answer.replace(" ", "").lower().strip()
            if outerr is not None:
                outerr = outerr.decode(encoding="utf-8")
            total_case += 1
            
            # os.remove(tmps_path + str(collapse_num)+ "_exe.log")
            # print('记录删除成功')

        except Exception as e:
            print(e, '记录失败', src_uid)
            if not collapse_flag:
                collapse_num += 1
            wrong_case += 1
            err = 1
            if outerr:            
                outerr = outerr.decode(encoding="utf-8")
                if outlog:
                    outerr += outlog
            else:
                if outlog:
                    outerr = outlog
            
            if errtype is None:
                errtype = "RUNTIME_ERROR"
            output_dict["error"] = record_result(output_dict["error"], src_uid, submission_id, difficulty, id, None, None, outerr, errtype)
            record = 1

    elif lang == "perl":
        try:
            p = Popen('perl temp.pl', stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            p.stdin.write(input.encode())
            p.stdin.flush()

            output, outerr = p.communicate()
            output = output.decode(encoding="utf-8")
            if outerr:
                outerr = outerr.decode(encoding="utf-8")
                errtype = "RUNTIME_ERROR"
            total_case += 1

            answer = answer.replace("\r", "")
            answer = answer.replace("\r\n", "\n")
            output = output.replace("\r", "")
            output = output.replace("\r\n", "\n")
        
            output = output.replace(" ", "").lower().strip()
            answer = answer.replace(" ", "").lower().strip()
        except Exception as e:
            print(e, "执行失败 src_uid: ", src_uid)
            err = 1
            errtype = "COMPILATION_ERROR"
            output_dict["error"] = record_result(output_dict["error"], src_uid, submission_id, difficulty, id, None, None, outerr, errtype)
            wrong_case += 1
            collapse_num += 1
    if err ==0:
        if answer != output and output != "":
            print("-----------------answer: ", answer, "-------------------")
            print("-----------------output: ", output, "-------------------")
            print("答案错误 src_uid: ", src_uid)
            errtype = "WRONG_ANSWER"
            try:
                output_dict["wrong"] = record_result(output_dict["wrong"], src_uid, submission_id, difficulty, id, answer, output, outerr, errtype)
            except func_timeout.exceptions.FunctionTimedOut:
                print("记录结果超时")
                if outlog and lang == "delphi":
                    if outerr is not None:
                        outerr += outlog
                output_dict["error"] = record_result(output_dict["error"], src_uid, submission_id, difficulty, id, None, None, outerr, errtype)
            wrong_case += 1
            err = 1
        elif answer != output and output == "":
            print("无输出结果")
            errtype = "RUNTIME_ERROR"
            if outlog and lang == "delphi":
                if outerr is not None:
                    outerr += outlog
                else:
                    outerr = outlog
            output_dict["error"] = record_result(output_dict["error"], src_uid, submission_id, difficulty, id, None, None, outerr, errtype)
            wrong_case += 1
            err = 1
    else:
        if record == 0:
            if outlog and lang == "delphi":
                outerr += outlog
            else:
                outerr = outlog
            errtype = "RUNTIME_ERROR"
            output_dict["error"] = record_result(output_dict["error"], src_uid, submission_id, difficulty, id, None, None, outerr, errtype)
    
    return output_dict, wrong_case, err, collapse_num


@func_set_timeout(300)
def exe_question(content, testcase_content, lang, postfix, output_dict, collapse_num, tmps_dir):
    source_code = content["source_code"]
    id = None
    if "id" in content.keys():
        id = content["id"]
    src_uid = str(content["src_uid"])
    difficulty = str(content["difficulty"])
    if "code_uid" in content.keys():
        submission_id = str(content["code_uid"])
    else:
        submission_id = str(content["submission_id"])

    if source_code == "":
        print("没有源码")
        output_dict["error"] = record_result(output_dict["error"], src_uid, submission_id, difficulty, id, None, None, "No Source Code", "No_Source_Code")
        return output_dict, 1, collapse_num

    source_code = source_code.replace("\\\\", "\\")
    source_code = source_code.replace("\\r", "\r")
    source_code = source_code.replace("\\n", "\n")
    source_code = source_code.replace("\\\"", "\"")
    source_code = source_code.replace("\r", "")
    source_code = source_code.replace("\r\n", "\n")

    file_path = 'temp.' + postfix
    with open(file_path, 'w', encoding = 'utf-8') as file:
        file.write(source_code)

    testcases = testcase_content[src_uid]
    total_case = 0
    wrong_case = 0
    for testcase in testcases:
        input = testcase["input"][0]
        answer = testcase["output"][0]

        input = input.replace("\r", "")
        input = input.replace("\r\n", "\n")

        try:
            output_dict, wrong_case, err, collapse_num = exe_testcase(source_code, answer, input, lang, postfix, output_dict, collapse_num, total_case, wrong_case, src_uid, submission_id, difficulty, id, tmps_dir)
        except func_timeout.exceptions.FunctionTimedOut:
            err = 1
            wrong_case = 1
            print("运行样例超时")
            collapse_num += 1
            output_dict["error"] = record_result(output_dict["error"], src_uid, submission_id, difficulty, id, None, None, "Time Limit Exceeded", "RUNTIME_ERROR")

        if err == 1:
            wrong_case = 1
            break
    if err == 0:
        output_dict["accepted"] = record_result(output_dict["accepted"], src_uid, submission_id, difficulty, id, None, None, None, None)
    # print("total_case: ", total_case)
    # print("wrong_case: ", wrong_case)
    return output_dict, wrong_case, collapse_num


def exe_main(args):
    with open(args.testcase_path, 'r', encoding = 'utf-8') as f:
        for line in f:
            testcase_content = json.loads(line)

    jsonl_path = args.jsonl_path
    lang = jsonl_path.split(".")[0].split("_")[-1]
    if lang == "d":
        postfix = "d"
    elif lang == "delphi":
        # postfix = "pas"
        postfix = "dpr"
    elif lang == "perl":
        postfix = "pl"
    else:
        print("WRONG LANG")

    code_sum = 0
    correct_sum = 0
    output_dict = {"accepted":{}, "wrong":{}, "error":{}}
    collapse_num = 0

    with open(jsonl_path, 'r', encoding = 'utf-8') as f:
        for idx, line in enumerate(f):
            content = json.loads(line)
            try:
                output_dict, wrong_case, collapse_num = exe_question(content, testcase_content, lang, postfix, output_dict, collapse_num, args.tmps_dir)
            except func_timeout.exceptions.FunctionTimedOut:
                print("运行题目超时")
                wrong_case = 1
            
            code_sum += 1
            if wrong_case == 0:
                correct_sum += 1

            print("done: ", idx+1, " not accepted: ", idx+1 - correct_sum)

    wrong_num = len(output_dict["wrong"].keys())
    error_num = len(output_dict["error"].keys())
    print("code_sum:", code_sum, " correct_sum: ", correct_sum, " wrong_num: ", wrong_num, " error_num: ", error_num, " accurancy: ", correct_sum / code_sum)
    output_dict["info"] = {"code_sum": code_sum, "correct_sum": correct_sum, "wrong_num": wrong_num, "error_num": error_num, "accurancy": correct_sum / code_sum}
    
    # print(output_dict)
    
    with open(args.output_path, 'w', encoding = 'utf-8') as f:
        json.dump(output_dict, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--testcase_path', type=str, default = "1024_testcases.jsonl")
    parser.add_argument('--tmps_dir', type=str, default = "tiny_tmps")
    parser.add_argument('--jsonl_path', type=str, default = "submissions_re_1007_before_perl.jsonl")
    parser.add_argument('--output_path', type=str, default = "submissions_re_out_1007_before_perl.json")
    args = parser.parse_args()

    exe_main(args)

