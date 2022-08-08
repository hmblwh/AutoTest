# -*- encoding=utf-8 -*-
# Run Airtest in parallel on multi-device
import os
import traceback
import subprocess
import webbrowser
import time
import json
import shutil
from airtest.core.android.adb import ADB
from jinja2 import Environment, FileSystemLoader
from airtest.core.api import using
using("Main.air")
from ExcelUtility import *
from ConfigReader.ConfigReader import ConfigReader

# run_all: True - run test fully; False - continue test with the progress in data.json
def run(devices, airs, run_all=False, testCaseID=[]):
    try:
        if len(airs) == 0:
            print("There is nothing to test!!!")
        else:    
            results = load_json_data(airs[0], run_all)
            tasks = run_on_multi_device(devices, airs, results, run_all, testCaseID)
            for task in tasks:
                status = task['process'].wait()
                results['tests'][task['dev']] = run_one_report(task['air'], task['dev'])
                results['tests'][task['dev']]['status'] = status
                json.dump(results, open('data.json', "w"), indent=4)
#             run_summary(results)
    except Exception as e:
        traceback.print_exc()
        
# Run airtest on multi-device        
def run_on_multi_device(devices, airs, results, run_all, testCaseID):
    tasks = []
    c = 0
    print("device: %s" %devices)
    for i in range(len(airs)):
        if (not run_all and results['tests'].get(devices[i]) and results['tests'].get(devices[i]).get('status') == 0):
            print("Skip device %s" % devices[i])
            continue
        if i >= len(devices):
            continue
#         log_dir = get_log_dir(devices[i], airs[c])
        cmd = [
            "airtest",
            "run",
            airs[c],
            "--device",
            "Android:///" + devices[i],
#             "--log",
#             log_dir,
            "--extraData",
            testCaseID[c]
        ]
        print("List TC: %s" %testCaseID[c])
        try:
            tasks.append({
                'process': subprocess.Popen(cmd, cwd=os.getcwd()),
                'dev': devices[i],
                'air': airs[c]
            })
        except Exception as e:
            traceback.print_exc()
        c += 1
    return tasks

# Build one test report for one air script
def run_one_report(air, dev):
    try:
        log_dir = get_log_dir(dev, air)
        print("log dir == %s" %log_dir)
        log = os.path.join(log_dir, 'log.txt')
        if os.path.isfile(log):
            cmd = [
                "airtest",
                "report",
                air,
                "--log_root",
                log_dir,
                "--outfile",
                os.path.join(log_dir, 'log.html'),
                "--lang",
                "en"
            ]
            ret = subprocess.call(cmd, shell=True, cwd=os.getcwd())
            return {
                    'status': ret,
                    'path': os.path.join(log_dir, 'log.html')
                    }
        else:
            print("Report build Failed. File not found in dir %s" % log)
    except Exception as e:
        traceback.print_exc()
    return {'status': -1, 'device': dev, 'path': ''}

# Build sumary test report
def run_summary(data):
    try:
        summary = {
            'time': "%.3f" % (time.time() - data['start']),
            'success': [item['status'] for item in data['tests'].values()].count(0),
            'count': len(data['tests'])
        }
        summary.update(data)
        summary['start'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['start']))
        env = Environment(loader=FileSystemLoader(os.getcwd()),
                          trim_blocks=True)
        html = env.get_template('report_tpl.html').render(data=summary)
        with open("report.html", "w", encoding="utf-8") as f:
            f.write(html)
        webbrowser.open('report.html')
    except Exception as e:
        traceback.print_exc()

# Loading data
# if data.json exists and run_all=False, loading progress in data.json
# else return an empty data        
def load_json_data(air, run_all):
    json_file = os.path.join(os.getcwd(), 'data.json')
    if (not run_all) and os.path.isfile(json_file):
        data = json.load(open(json_file))
        data['start'] = time.time()
        return data
    else:
#         clear_log_dir(air)
        return {
            'start': time.time(),
            'script': air,
            'tests': {}
        }

# Remove folder /log    
def clear_log_dir(air):
    log = os.path.join(os.getcwd(), air, 'log')
    if os.path.exists(log):
        shutil.rmtree(log)

# Create log folder based on device name under /log/        
def get_log_dir(device, air):
    log_dir = os.path.join(air, 'log', device.replace(".", "_").replace(':', '_'))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

# Init variables here
if __name__ == '__main__':
    devices = [tmp[0] for tmp in ADB().devices()]
    data = getTestCaseNeedTest()
    arr_data =  [json.dumps(obj) for obj in data]
    print("arrData: ", arr_data)
    
    airs = []
    for i in range(len(arr_data)):
        airs.append('Main.air')
    run(devices, airs, True, arr_data)


