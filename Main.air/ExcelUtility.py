import pandas
import json
import xlsxwriter
import os
import time
import datetime

_urlTestCase = "TestCase.xls"
_sheetName = "TestCase"
tStart = ""
tEnd = ""
timeStart = datetime.datetime.now()

def generateScreenshotName(fileName, timeFail):
    return "Report\Snapshot\Device %s_%s%s_%s%s%s.png" %(fileName, timeFail.strftime("%d"), timeFail.strftime("%m"), timeFail.strftime("%H"), timeFail.strftime("%M"), timeFail.strftime("%S"))

def readExcelFile(url, sheetName):
    return pandas.read_excel(url, sheet_name = sheetName)

def readConfigTestCase(url, sheetName):
    data = readExcelFile(url, sheetName).to_json(orient = 'records')
    return data

def getTestCaseNeedTest():
    data = readConfigTestCase(_urlTestCase, _sheetName)
    data = json.loads(data)
    arrTestCase = []
    isTest = False
    for devideObj in data:
        for obj in devideObj:
#             print(obj)
            if devideObj[obj] == True:
#                 print("Device Obj: %s" %devideObj)
                isTest = True
                arrTestCase.append(devideObj)
                break
        isTest = False
    arrTestCase.sort(key=lambda x: x.get('Device'))
    return arrTestCase

def getFunctionNeedTest(fName):
    data = readConfigTestCase(_urlTestCase, fName)
    data = json.loads(data)
    arrFunction = []
    for obj in data:
        if obj["Name"] == None or not obj["Test"]:
            continue
        else:
#             print("Function Obj: %s" %obj)
            arrFunction.append(obj["Name"])
    return arrFunction

def getFileLogWriter(url):
    global file 
    file = xlsxwriter.Workbook(url)
    
def closeFileLog(url):
    file.close()
#     os.startfile(url)
    
def getSheetWriter(sheetName):
    sheet1 = file.add_worksheet(sheetName)
    return sheet1

def writeText(sheet, position, title, formatTxt):
    sheet.write(position, title, formatTxt)

def writeHeader(file, sheet):
    indexHeader = 5
    headerList = ["ID", "Description", "Status", "Reason", "Image", "Time of Error", "Interval"]
    sheet.set_column(0, 0, 5)
    sheet.set_column(1, 1, 70)
    sheet.set_column(3, 3, 40)
    sheet.set_column(4, 4, 50)
    sheet.set_column(5, 5, 20)
    sheet.set_column(6, 6, 10)
    sheet.write_row(indexHeader, 0, headerList, file.extra["formatHeader"])

def writeResultTestCase(file, sheet, rs, caseId, index):
    sheet.write(index, 0, caseId, file.extra["formatNormal"])
    sheet.write(index, 1, rs["content"], file.extra["formatDescription"])
    sheet.write(index, 2, rs["status"], file.extra["formatPass"] if rs["status"] == "Pass" else file.extra["formatFail"] )
    sheet.write(index, 3, rs["reason"], file.extra["formatDescription"])
    sheet.write_url(index, 4, "external:%s" % rs["image"], file.extra["formatDescription"])
    sheet.write(index, 5, rs["time"], file.extra["formatNormal"])
    sheet.write(index, 6, rs["interval"], file.extra["formatNormal"])

def writeLogTest(data, caseName):
    titleTestCase = caseName + " Testing Report"
    arrResult = data
    #print("arrResult %s" %arrResult)
    sheet = getSheetWriter(caseName)
    file.extra = {}

    formatHeader = file.add_format({'bg_color': '#1F497D', 'font_color': '#FFFFFF'})
    formatHeader.set_align("center")
    formatHeader.set_border(1)

    formatDescription = file.add_format()
    formatDescription.set_text_wrap()
    formatDescription.set_border(1)

    formatPass = file.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
    formatPass.set_bold()
    formatPass.set_align("center")
    formatPass.set_border(1)

    formatFail = file.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    formatFail.set_bold()
    formatFail.set_align("center")
    formatFail.set_border(1)

    formatNormal = file.add_format()
    formatNormal.set_border(1)
    formatNormal.set_align("center")
    
    formatNumFail = file.add_format({'font_color': '#FF0000'})
    formatNumFail.set_align("center")
    
    formatTextRight = file.add_format()
    formatTextRight.set_align("right")
    
    formatTitle = file.add_format({'font_color': '#1F497D'})
    formatTitle.set_bold()
    formatTitle.set_font_size(14)
    formatTitle.set_align("center")

    file.extra["formatHeader"] = formatHeader
    file.extra["formatDescription"] = formatDescription
    file.extra["formatFail"] = formatFail
    file.extra["formatPass"] = formatPass
    file.extra["formatNormal"] = formatNormal
    
    writeText(sheet, "D1", titleTestCase, formatTitle)
    writeHeader(file, sheet)
    
    caseId = 1
    startIndex = 6
    for _rs in arrResult:
        writeResultTestCase(file, sheet, _rs, caseId, startIndex)
        startIndex += 1
        caseId += 1
        
    writeText(sheet, "B3", "Fail:", formatTextRight)
    writeText(sheet, "B4", "Crash:", formatTextRight)
    writeText(sheet, "C3", "= COUNTIF(C7:C500,\"fail\")", formatNumFail)
    writeText(sheet, "C4", "= COUNTIF(C7:C500,\"crash\")", formatNumFail)
    
    writeText(sheet, "D3", "Start Time:", formatTextRight)
    writeText(sheet, "D4", "End Time:", formatTextRight)
    sheet.write("E3", tStart)
    sheet.write("E4", tEnd)

def setEndTime(end):
    global tEnd
    tEnd = end 

def setStartTime(dtStart):
    global tStart, timeStart 
    tStart = str(dtStart)[:str(dtStart).find('.')]
    timeStart = dtStart