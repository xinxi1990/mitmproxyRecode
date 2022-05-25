import os
import time
import json
import csv
import sys
import requests
from deepdiff import DeepDiff
from jinja2 import Environment, PackageLoader

"""
接口用例流量录制
python3 cli_replay.py /Users/xinxi/Documents/zhihu/mitmproxyRecode/20220524230852-case.csv
"""

currentPath = os.path.abspath(os.path.dirname(__file__))

casePath = sys.argv[1]

print(casePath)


def read_case():
    case_data = []
    csv.field_size_limit(500 * 1024 * 1024)
    csv_read = csv.reader(open(casePath))
    for index, item in enumerate(csv_read):
        if index != 0:
            case_data.append(item)
    return case_data


def base_requests():
    """
    基础请求磊
    :return:
    """
    caseList = read_case()
    apiNameList = []
    apiTimeList = []
    successes = 0
    failures = 0
    skipped = 0
    if len(caseList) > 0:
        for case in caseList:
            request_url = case[0]
            request_headers = eval(case[1])
            request_method = case[2]
            old_response_data = case[4]
            if request_method == 'GET':
                r = requests.request(method=request_method, url=request_url, headers=request_headers)
                now_response_data = r.json()

                print('********************* Requests URL: {} *********************'.format(r.url))
                diff_data = DeepDiff(now_response_data, eval(old_response_data), ignore_order=True)  # diff 返回数据
                case.append(json.dumps(eval(old_response_data), indent=4, ensure_ascii=False))
                case.append(json.dumps(r.json(), indent=4, ensure_ascii=False))
                case.append(json.dumps(diff_data, indent=4, ensure_ascii=False))
                apiNameList.append(r.url)
                apiTimeList.append(r.elapsed.total_seconds())
                if r.status_code == 200:
                    successes = successes + 1
                else:
                    failures = failures + 1
        create_report(caseList, apiNameList, apiTimeList, successes, failures, skipped)


def create_report(records, apiNameList, apiTimeList, successes, failures, skipped):
    """
    生成测试报告
    :return:
    """
    reportFolder = os.path.join(currentPath, 'reports')
    if not os.path.exists(reportFolder):
        os.makedirs(reportFolder)
    report_path = os.path.join(reportFolder, "CaseReport{}.html".format(time.strftime("%Y%m%d%H%M%S")))
    try:
        env = Environment(loader=PackageLoader('resources', 'templates'))
        template = env.get_template("template.html")
        html_content = template.render(html_report_name="接口测试报告", records=records, apiNameList=apiNameList,
                                       apiTimeList=apiTimeList,successes=successes,failures=failures,skipped=skipped)
        with open(report_path, "wb") as f:
            f.write(html_content.encode("utf-8"))
            print('报告地址: {}'.format(report_path))
    except Exception as e:
        print(e)


base_requests()
