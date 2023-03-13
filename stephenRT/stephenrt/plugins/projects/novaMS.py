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
import sys
import websockets

if sys.platform == "win32":
    from Cryptodome.Cipher import AES
else:
    from Crypto.Cipher import AES
import base64
import time
import uuid
import requests
import json
import asyncio

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


def get_report_url(s, host, reportId, testPlanId, accessKey, secretKey):
    url = host + "/track/share/generate/expired"
    # url = host + f"/share/test/plan/case/list/all/{testPlan_id}"
    # body = {"customData": reportId, "shareType": "PLAN_DB_REPORT", "lang": None}
    body = {"customData": reportId, "createTime": 0, "createUserId": "admin", "updateTime": 0,
            "shareType": "PLAN_DB_REPORT", "lang": None, "id": testPlan_id}
    s = setHeaders(s, accessKey, secretKey)  # 设置请求头
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
    try:
        result = json.loads(r)["data"][0]
    except:
        print("result错误, r: ", r)
    print(json.dumps(result))
    response = {}
    for i in result["apiAllCases"]:
        if str(i["num"]) == "100001002":
            response["interfaceReport"] = i["reportId"]
            break
    response["测试计划"] = result["name"]
    response["caseCount"] = result["caseCount"]
    response["executeRate"] = result["executeRate"]
    response["apiScenarioData"] = result["apiResult"]["apiScenarioData"]
    # response["errorCase"] = [x["name"] for x in result["scenarioAllCases"] if x["lastResult"] == "ERROR"]
    response["apiScenarioStepData"] = result["apiResult"]["apiScenarioStepData"]
    response["scenarioFailureCases"] = result["scenarioFailureCases"]
    response["failName"] = [x["name"] for x in response["scenarioFailureCases"]]
    passRate = "{:.2%}".format(result["passRate"])
    response["场景通过率"] = f'{passRate} [{result["caseCount"] - len(response["failName"])}/{result["caseCount"]}]'
    response["startTime"] = result["startTime"]
    response["endTime"] = result["endTime"]
    response["失败场景"] = "\n"

    for i in response["failName"]:
        response["失败场景"] = response["失败场景"] + "-   " + i + "\n"
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
        report_url = get_report_url(s, host, data, projectId, access_key, secret_key)  # 获取测试报告
    msg = "API TEST EXECUTE SUCCESS：\n{}".format(report_url)
    print(msg)
    return [data, msg]


def api_cover(s, num, projectId):
    """
    已经录入的api合计
    :param s:
    :param num:
    :param projectId:
    :return:
    """
    url = host + f"/api/api/definition/list/1/{num}"
    payload = json.dumps({
        "components": [
            {
                "key": "id",
                "name": "MsTableSearchInput",
                "label": "ID",
                "operator": {
                    "options": [
                        {
                            "label": "commons.adv_search.operators.like",
                            "value": "like"
                        },
                        {
                            "label": "commons.adv_search.operators.not_like",
                            "value": "not like"
                        }
                    ]
                }
            },
            {
                "key": "name",
                "name": "MsTableSearchInput",
                "label": "commons.name",
                "operator": {
                    "value": "like",
                    "options": [
                        {
                            "label": "commons.adv_search.operators.like",
                            "value": "like"
                        },
                        {
                            "label": "commons.adv_search.operators.not_like",
                            "value": "not like"
                        }
                    ]
                }
            },
            {
                "key": "method",
                "name": "MsTableSearchSelect",
                "label": "api_test.definition.api_type",
                "operator": {
                    "options": [
                        {
                            "label": "commons.adv_search.operators.in",
                            "value": "in"
                        },
                        {
                            "label": "commons.adv_search.operators.not_in",
                            "value": "not in"
                        }
                    ]
                },
                "options": [
                    {
                        "text": "GET",
                        "value": "GET"
                    },
                    {
                        "text": "POST",
                        "value": "POST"
                    },
                    {
                        "text": "PUT",
                        "value": "PUT"
                    },
                    {
                        "text": "PATCH",
                        "value": "PATCH"
                    },
                    {
                        "text": "DELETE",
                        "value": "DELETE"
                    },
                    {
                        "text": "OPTIONS",
                        "value": "OPTIONS"
                    },
                    {
                        "text": "HEAD",
                        "value": "HEAD"
                    },
                    {
                        "text": "CONNECT",
                        "value": "CONNECT"
                    }
                ],
                "props": {
                    "multiple": True
                }
            },
            {
                "key": "path",
                "name": "MsTableSearchInput",
                "label": "api_test.definition.api_path",
                "operator": {
                    "value": "like",
                    "options": [
                        {
                            "label": "commons.adv_search.operators.like",
                            "value": "like"
                        },
                        {
                            "label": "commons.adv_search.operators.not_like",
                            "value": "not like"
                        }
                    ]
                }
            },
            {
                "key": "status",
                "name": "MsTableSearchSelect",
                "label": "commons.status",
                "operator": {
                    "options": [
                        {
                            "label": "commons.adv_search.operators.in",
                            "value": "in"
                        },
                        {
                            "label": "commons.adv_search.operators.not_in",
                            "value": "not in"
                        }
                    ]
                },
                "options": [
                    {
                        "value": "Prepare",
                        "label": "test_track.plan.plan_status_prepare"
                    },
                    {
                        "value": "Underway",
                        "label": "test_track.plan.plan_status_running"
                    },
                    {
                        "value": "Completed",
                        "label": "test_track.plan.plan_status_completed"
                    }
                ],
                "props": {
                    "multiple": True
                }
            },
            {
                "key": "tags",
                "name": "MsTableSearchInput",
                "label": "commons.tag",
                "operator": {
                    "value": "like",
                    "options": [
                        {
                            "label": "commons.adv_search.operators.like",
                            "value": "like"
                        },
                        {
                            "label": "commons.adv_search.operators.not_like",
                            "value": "not like"
                        }
                    ]
                }
            },
            {
                "key": "updateTime",
                "name": "MsTableSearchDateTimePicker",
                "label": "commons.update_time",
                "operator": {
                    "options": [
                        {
                            "label": "commons.adv_search.operators.between",
                            "value": "between"
                        },
                        {
                            "label": "commons.adv_search.operators.gt",
                            "value": "gt"
                        },
                        {
                            "label": "commons.adv_search.operators.lt",
                            "value": "lt"
                        }
                    ]
                }
            },
            {
                "key": "createTime",
                "name": "MsTableSearchDateTimePicker",
                "label": "commons.create_time",
                "operator": {
                    "options": [
                        {
                            "label": "commons.adv_search.operators.between",
                            "value": "between"
                        },
                        {
                            "label": "commons.adv_search.operators.gt",
                            "value": "gt"
                        },
                        {
                            "label": "commons.adv_search.operators.lt",
                            "value": "lt"
                        }
                    ]
                }
            },
            {
                "key": "creator",
                "name": "MsTableSearchSelect",
                "label": "test_track.plan.plan_principal",
                "operator": {
                    "options": [
                        {
                            "label": "commons.adv_search.operators.in",
                            "value": "in"
                        },
                        {
                            "label": "commons.adv_search.operators.not_in",
                            "value": "not in"
                        },
                        {
                            "label": "commons.adv_search.operators.current_user",
                            "value": "current user"
                        }
                    ]
                },
                "options": {
                    "url": "/user/project/member/list",
                    "labelKey": "name",
                    "valueKey": "id"
                },
                "props": {
                    "multiple": True
                }
            },
            {
                "key": "moduleIds",
                "name": "MsTableSearchNodeTree",
                "label": "test_track.case.module",
                "operator": {
                    "value": "in",
                    "options": [
                        {
                            "label": "commons.adv_search.operators.in",
                            "value": "in"
                        },
                        {
                            "label": "commons.adv_search.operators.not_in",
                            "value": "not in"
                        }
                    ]
                },
                "options": {
                    "url": "/api/module/list",
                    "type": "GET",
                    "params": {
                        "protocol": "HTTP"
                    }
                }
            },
            {
                "key": "followPeople",
                "name": "MsTableSearchSelect",
                "label": "commons.follow_people",
                "operator": {
                    "options": [
                        {
                            "label": "commons.adv_search.operators.in",
                            "value": "in"
                        },
                        {
                            "label": "commons.adv_search.operators.current_user",
                            "value": "current user"
                        }
                    ]
                },
                "options": {
                    "url": "/user/ws/current/member/list",
                    "labelKey": "name",
                    "valueKey": "id"
                },
                "props": {
                    "multiple": True
                }
            }
        ],
        "filters": {
            "status": [
                "Prepare",
                "Underway",
                "Completed"
            ]
        },
        "orders": [],
        "versionId": None,
        "selectAll": False,
        "unSelectIds": [],
        "moduleIds": [],
        "projectId": projectId,
        "protocol": "HTTP",
        "selectThisWeedData": False,
        "apiCaseCoverage": None,
        "apiCoverage": "covered",
        "scenarioCoverage": None
    })
    r = s.post(url, data=payload)
    if r.status_code != 200:
        return "count api error"
    else:
        response = r.content.decode()
        response = json.loads(response)["data"]["listObject"]
        response = [x["path"] for x in response]
        return response

def get_interfaceList(s, id="e68c1c89-cbc0-41c7-9bc6-4be664093744"):
    """
    interfacelist 已经cover的route
    :param s:
    :param id:
    :return:
    """
    url = host + f"/track/api/definition/report/get/{id}"
    payload = {}
    r = s.get(url, json=payload)
    if r.status_code != 200:
        print(r)
    else:
        response = r.content.decode()
        response = json.loads(response)["data"]["content"]
        response = json.loads(response)["responseResult"]["body"]
        response = json.loads(response)["data"]["routeDictNoDomain"]
        response = list(response.values())
        return response


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
envId = "daead9c9-4679-44e2-921d-28bb8015bf18"  # 按顺序取会变
# print(json.dumps(env))
# envId = env["id"]
testPlan_id = "cb29ef0f-6fd7-439f-9df4-75a8d7a930a2"

if __name__ == '__main__':
    # result = exec_run(access_key, secret_key, host, projectId, envId, testPlan_id)
    # report_id = result[0]
    # reportDb(s, report_id)

    # a = get_report_url(s, host, "edc1fd5c-0c84-4fef-8a55-42bdce01a410", testPlan_id)
    # print(a)
    reportId = "73e87743-80b5-472b-81c6-508c226624b2"
    # db = reportDb(s, "73e87743-80b5-472b-81c6-508c226624b2")
    # print(db)
    # a = get_interfaceList(s)
    # print(a)
    #
    # r = api_cover(s, 200, projectId)
    # print(json.dumps(r))
    # print(len(r))
    apis = get_interfaceList(s)
    apiCover = api_cover(s, 200, projectId)
    print(apiCover)
    apiNot = list(set(apis) ^ set(apiCover))
    print(apiNot)