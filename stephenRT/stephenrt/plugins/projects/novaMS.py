#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/3/2 18:02
# @Author   : StephenZ
# @Site     :
# @File     : tool_ms.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2023
# @Licence  :     <@2022>

from Crypto.Cipher import AES
import base64
import time
import uuid
import requests
import json

if __name__ == '__main__':
    from local_config import *
else:
    from .local_config import *

def aesEncrypt(text, secretKey, iv):
    BS = AES.block_size  # 这个等于16
    mode = AES.MODE_CBC

    def pad(s): return s + (BS - len(s) % BS) * \
                       chr(BS - len(s) % BS)

    cipher = AES.new(secretKey.encode('UTF-8'), mode, iv.encode('UTF-8'))
    encrypted = cipher.encrypt(pad(text).encode('UTF-8'))
    # 通过aes加密后，再base64加密
    b_encrypted = base64.b64encode(encrypted)
    return b_encrypted


def setHeaders(s, accessKey, secretKey):
    """
    生成签名，并设置到 header
    :param s:
    :param accessKey:
    :param secretKey:
    :return:
    """
    timeStamp = int(round(time.time() * 1000))
    combox_key = accessKey + '|' + str(uuid.uuid4()) + '|' + str(timeStamp)
    signature = aesEncrypt(combox_key, secretKey, accessKey)
    # print(signature.decode('UTF-8'))
    header = {'Content-Type': 'application/json', 'ACCEPT': 'application/json', 'accessKey': accessKey,
              'signature': signature.decode('UTF-8'), 'Connection': 'close'}
    s.headers.update(header)
    return s


def get_projects(s):
    route = "/project/listAll/4effac3b-c150-11ec-bfc2-0242ac1e0a03"  # 获取项目信息
    url = host + "/api" + route
    # print(url)
    r = s.get(url)
    result = r.content.decode("utf-8")
    return result


def project_info(s, name):
    projects = get_projects(s)
    # print(projects)
    for project in json.loads(projects)["data"]:
        if project["name"] == name:
            # print(project)
            return project


def env(s, projectId):
    url = host + "/api" + f"/environment/list/{projectId}"
    # print(url)
    data = s.get(url).content.decode("utf-8")
    envs = json.loads(data)["data"]
    return envs


def post_method(s):
    route = "projects/listAll"
    url = host + "/api" + route
    # print(url)
    payload = {}
    r = s.post(url, payload)
    print(r.content.decode("utf-8"))



# 获取运行环境id
def get_test_plan_env(s, host, projectId, name):
    # xx
    url = host + "/api/environment/list/{}".format(projectId)
    r = s.get(url)
    # print(r.content)
    data = r.json().get("data")
    if data:
        for dat in data:
            if dat.get("name") == name:
                return dat.get("id")
    else:
        print("没有data值")


# 测试报告
def get_report_url_abundon(s, host, customData):
    url = host + "/api/share/info/generateShareInfoWithExpired"

    body = {"customData": customData, "shareType": "PLAN_DB_REPORT", "lang": None}
    r = s.post(url, json=body).content
    print(r)
    if r:
        data = r.json().get("data")
        if data:
            shareUrl = data.get("shareUrl")
            report_url = host + "/sharePlanReport" + shareUrl
            return report_url
    else:
        print("没有返回值...")


def get_report_url(s, host, reportId, testPlanId):
    url = host + "/track/share/generate/expired"
    # url = host + f"/share/test/plan/case/list/all/{testPlan_id}"
    # body = {"customData": reportId, "shareType": "PLAN_DB_REPORT", "lang": None}
    body = {"customData": reportId, "createTime": 0, "createUserId": "admin", "updateTime": 0,
            "shareType": "PLAN_DB_REPORT", "lang": None, "id": testPlan_id}
    result = s.post(url, json=body).content.decode()
    print("报告result：", result)
    shareUrl = json.loads(result)["data"]["shareUrl"]
    middle = "/track/share-plan-report"
    result = host + middle + shareUrl
    print(result)
    return result

def share_report(s, projectId):
    url = host + f"/track/project_application/get/{projectId}/TRACK_SHARE_REPORT_TIME"
    r = s.get(url)
    response = r.content.decode()
    print(response)

def reportDb(s, reportId):
    url = host + f"/api/test/plan/report/db/{reportId}"
    r = s.get(url).content.decode()
    result = json.loads(r)["data"][0]
    print(json.dumps(result))
    response = {}
    response["caseCount"] = result["caseCount"]
    response["executeRate"] = result["executeRate"]
    response["passRate"] = "{:.2%}".format(result["passRate"])
    response["name"] = result["name"]
    response["apiScenarioData"] = result["apiResult"]["apiScenarioData"][0]
    # response["errorCase"] = [x["name"] for x in result["scenarioAllCases"] if x["lastResult"] == "ERROR"]
    response["scenarioFailureCases"] = result["scenarioFailureCases"]
    response["failName"] = [x["name"] for x in response["scenarioFailureCases"]]
    response["startTime"] = result["startTime"]
    response["endTime"] = result["endTime"]
    response["failCase"] = "    \n".join(response["failName"])
    print(json.dumps(response))
    return response


def test_plan_run(s, host, testPlanId, projectId, envId, userId="admin"):
    url = host + "/track/test/plan/run"
    body = {
        "mode": "serial",
        "reportType": "iddReport",
        "onSampleError": False,
        "runWithinResourcePool": False,
        "resourcePoolId": None,
        "envMap": {
            projectId: envId
        },
        "testPlanId": testPlanId,
        "projectId": projectId,
        "userId": userId,
        "triggerMode": "MANUAL",
        "environmentType": "JSON",
        "environmentGroupId": "",
        "requestOriginator": "TEST_PLAN",
        "retryEnable": False,
        "retryNum": 1,
        "browser": "CHROME",
        "headlessEnabled": False,
        "executionWay": "RUN",
        "testPlanDefaultEnvMap": {
            "e3de5c72-ff21-4517-99c4-efe82304dc97": [
                "daead9c9-4679-44e2-921d-28bb8015bf18",
                "58d9b5c6-07e3-4e08-80fb-32792ab91a3a"
            ]
        }
    }

    r = s.post(url, json=body).content
    return r


def exec_run(accessKey, secretKey, host, projectId, envId, testPlan_id):
    s = requests.session()
    s = setHeaders(s, accessKey, secretKey)  # 设置请求头
    # testPlanId = get_test_plan(s,host,projectId,testPlanName) #获取测试计划id，这里可以直接写testPlanId，这里采用调Api获取的形式
    # r = test_plan_run(s, host, testPlanId, projectId, envId).decode()
    r = test_plan_run(s, host, testPlan_id, projectId, envId)
    if json.loads(r)["success"] == True:
        data = json.loads(r)["data"]
    if data:
        report_url = get_report_url(s, host, data, projectId)  # 获取测试报告
    msg = "API TEST EXECUTE SUCCESS:\n{}".format(report_url)
    print(msg)
    return [data, msg]

access_key = pgsql["msAccess"]
secret_key = pgsql["msSecret"]
host = "http://10.10.10.8:8081"
workspace_id = "4effac3b-c150-11ec-bfc2-0242ac1e0a03"
# projectId = "e3de5c72-ff21-4517-99c4-efe82304dc97"
timeMill = int(round(time.time() * 1000))

combox_key = access_key + '|' + str(uuid.uuid4()) + '|' + str(timeMill)
signature = aesEncrypt(combox_key, secret_key, access_key)
# print(signature)

header = {'Content-Type': 'application/json', 'ACCEPT': 'application/json', 'accessKey': access_key,
          'signature': signature.decode('UTF-8'), 'Connection': 'close'}

name = "内网-测试服-66-标准"

s = requests.session()
s = setHeaders(s, access_key, secret_key)
## 操作
project = project_info(s, "MatchNova")
projectId = project["id"]
env = env(s, projectId)[0]
envId = env["id"]
testPlan_id = "cb29ef0f-6fd7-439f-9df4-75a8d7a930a2"

if __name__ == '__main__':
    # result = exec_run(access_key, secret_key, host, projectId, envId, testPlan_id)
    # report_id = result[0]
    # reportDb(s, report_id)

    a = get_report_url(s, host, "edc1fd5c-0c84-4fef-8a55-42bdce01a410", testPlan_id)
    print(a)