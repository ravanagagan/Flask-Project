from flask import Flask, render_template, request
from logging import WARNING, FileHandler
import os, os.path
from os import path
import csv, time
from datetime import datetime
from configparser import ConfigParser
header_data1 = {}

def header_data():  # Fetching header details from corresponding text-box
    header_data1 = {
        "auth": request.form.get('auth').replace(":", " "),
        "acceptlanguage": request.form.get('acceptlanguage'),
        "url": request.form.get('url'),
        "reqid": request.form.get('reqid'),
        "contenttype": request.form.get('contenttype'),
        "accept": request.form.get('accept')
    }
    print(type(header_data1))
    return header_data1

def api_type_check(data):
    if data == "SIM":
        return 1
    elif data == "getSIMState":
        return 2
    elif data == "suspendSIM":
        return 3
    elif data == "reactivateSIM":
        return 4
    elif data == "ping":
        return 5
    elif data == "updateSettings":
        return 6
    elif data == "dataPlans":
        return 7
    elif data == "attachDataPlans":
        return 8
    elif data == "getAttachedDataPlans":
        return 9
    elif data == "modifyDataPlans":
        return 10
    elif data == "changeState":
        return 11
    elif data == 'state':
        return 12
    elif data == 'sessionInfo':
        return 13
    elif data == 'dataUsgae':
        return 14
    elif data == 'sessionHistory':
        return 15
    elif data == 'list':
        return 16


def fetch_file_data(file_name):
    with open(file_name, 'r') as f:
        data = f.read()
    return int(data)


def update_file_content(file_name, sl_no):
    if os.path.exists(file_name):
        with open(file_name, 'w') as f:
            f.write(str(sl_no))
    else:
        with open(file_name, 'w') as f:
            id = 0
            f.write(str(id))


class Daimler:
    api_url = None
    def fun1(api_name, api_type, file_name, tc_status, tc_name, tc_desc, name, current_date, expected_code,
             expected_res):  # Methods for specific api's(passing all general data to function)

        if request.method == 'POST':
            parser = ConfigParser()
            parser.read('config.ini')  # reading config.ini to fetch port and other details

            sl_no = fetch_file_data(file_name)  # fetching sl_no from file
            update_file_content(file_name, sl_no + 1)  # each time updating file content

            # receiving header data to the dict
            header_data1 = header_data()  # fetching header data to dictionary
            for key in list(header_data1):
                if len(header_data1[key]) > 0:
                    print(header_data1[key])
                else:
                    header_data1.pop(key)# if length is not greater than 0 that pop that field from list

            if request.form.get("prodname_0") != None:  # fetching and handling checkbox
                qp = request.form.get("prodname_0")
            elif request.form.get("prodname_1") != None:
                qp = request.form.get("prodname_1")
            else:
                qp = ""

            qp_value = request.form['item_0']
            #  genrating api_url and storing into api_url variable
            api_url = parser.get('Daimler', 'type') + "://" + parser.get('Daimler','IP') + ":" + parser.get('Daimler',
                'port') + "/" + parser.get('Daimler', 'Name') + "/" + api_name + "?" + qp + "=" + qp_value

            #  creating list with all parameters, then writing them to the csv_file. SAME FALLOES FOR NEXT METHODS ALSO.
            fieldnames = ["sl_no", "tc_status", "tc_name", "api_type", "tc_desc", "name",
                          "current_date", "api_url", "header", "body", "expected_code", "expected_res", "api_name"]
            res = not path.exists("final_data.csv")
            with open('final_data.csv', 'a', newline="") as inFile:
                writer = csv.DictWriter(inFile, fieldnames=fieldnames, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                if res == True:
                    writer.writeheader()
                writer.writerow({"sl_no": sl_no, "tc_status": tc_status, "tc_name": tc_name, "api_type": api_type, "tc_desc": tc_desc,
                                "name": name, "current_date": current_date, "api_url": api_url, "header": header_data1, "body": None,
                                "expected_code": expected_code, "expected_res": expected_res})

    def fun2(api_name, file_name, api_type, tc_status, tc_name, tc_desc, name, current_date, expected_code,
             expected_res):
        # http: // localhost: 8080 / globetouchAPI / v1 / suspendSIM / 1234567890?trackingid = 12213123123123123
        if request.method == 'POST':
            parser = ConfigParser()
            parser.read('config.ini')
            sl_no = fetch_file_data(file_name)
            update_file_content(file_name, sl_no + 1)

            header_data1 = header_data()
            for key in list(header_data1):
                if len(header_data1[key]) > 0:
                    print(header_data1[key])
                else:
                    header_data1.pop(key)
        iccid = request.form['iccid']
        qp = "trackingid"
        qp_value = request.form["trackingid"]
        api_url = parser.get('Daimler', 'type') + "://" + parser.get('Daimler', 'IP') + ":" \
                  + parser.get('Daimler', 'port') + "/" + parser.get('Daimler', 'Name') \
                  + "/" + api_name + "/" + iccid + "?" + qp + "=" + qp_value

        fieldnames = ["sl_no", "tc_status", "tc_name", "api_type", "tc_desc", "name",
                      "current_date", "api_url", "header", "body", "expected_code", "expected_res", "api_name"]
        res = not path.exists("final_data.csv")
        with open('final_data.csv', 'a', newline="") as inFile:
            writer = csv.DictWriter(inFile, fieldnames=fieldnames, delimiter='|', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            if res == True:
                writer.writeheader()
            writer.writerow(
                {"sl_no": sl_no, "tc_status": tc_status, "tc_name": tc_name, "api_type": api_type, "tc_desc": tc_desc,
                 "name": name, "current_date": current_date, "api_url": api_url, "header": header_data1, "body": None,
                 "expected_code": expected_code, "expected_res": expected_res})

    def fun3(api_name, file_name, api_type, tc_status, tc_name, tc_desc, name, current_date, expected_code, expected_res):
        if request.method == 'POST':
            parser = ConfigParser()
            parser.read('config.ini')
            sl_no = fetch_file_data(file_name)
            update_file_content(file_name, sl_no + 1)

            header_data1 = header_data()
            for key in list(header_data1):
                if len(header_data1[key]) > 0:
                    print(header_data1[key])
                else:
                    header_data1.pop(key)
        qp = "echo"
        qp_value = request.form["echo"]
        api_url = parser.get('Daimler', 'type') + "://" + parser.get('Daimler', 'IP') + ":" \
                  + parser.get('Daimler', 'port') + "/" + parser.get('Daimler', 'Name') \
                  + "/" + api_name + "?" + qp + "=" + qp_value

        fieldnames = ["sl_no", "tc_status", "tc_name", "api_type", "tc_desc", "name",
                      "current_date", "api_url", "header", "body", "expected_code", "expected_res", "api_name"]
        res = not path.exists("final_data.csv")
        with open('final_data.csv', 'a', newline="") as inFile:
            writer = csv.DictWriter(inFile, fieldnames=fieldnames, delimiter='|', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            if res == True:
                writer.writeheader()
            writer.writerow(
                {"sl_no": sl_no, "tc_status": tc_status, "tc_name": tc_name, "api_type": api_type, "tc_desc": tc_desc,
                 "name": name, "current_date": current_date, "api_url": api_url, "header": header_data1, "body": None,
                 "expected_code": expected_code, "expected_res": expected_res})

    def fun4(api_name, file_name, api_type, tc_status, tc_name, tc_desc, name, current_date, expected_code, expected_res, body_data):
        if request.method == 'POST':
            parser = ConfigParser()
            parser.read('config.ini')
            sl_no = fetch_file_data(file_name)
            update_file_content(file_name, sl_no + 1)

            header_data1 = header_data()
            for key in list(header_data1):
                if len(header_data1[key]) > 0:
                    print(header_data1[key])
                else:
                    header_data1.pop(key)

        deviceid = request.form['deviceid']
        qp = "trackingid"
        qp_value = request.form["trackingid"]
        api_url = parser.get('Daimler', 'type') + "://" + parser.get('Daimler', 'IP') + ":" \
                  + parser.get('Daimler', 'port') + "/" + parser.get('Daimler', 'Name') \
                  + "/" + api_name + "/" + deviceid + "/settings?" + qp + "=" + qp_value
        fieldnames = ["sl_no", "tc_status", "tc_name", "api_type", "tc_desc", "name",
                      "current_date", "api_url", "header","body", "expected_code", "expected_res", "api_name"]
        res = not path.exists("final_data.csv")
        with open('final_data.csv', 'a', newline="") as inFile:
            writer = csv.DictWriter(inFile, fieldnames=fieldnames, delimiter='|', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            if res == True:
                writer.writeheader()
            writer.writerow(
                {"sl_no": sl_no, "tc_status": tc_status, "tc_name": tc_name, "api_type": api_type, "tc_desc": tc_desc,
                 "name": name, "current_date": current_date, "api_url": api_url, "header": header_data1, "body": body_data,
                 "expected_code": expected_code, "expected_res": expected_res})

class Gcontrol:
    api_url = None
    def fun1(api_name, api_type, file_name, tc_status, tc_name, tc_desc, name, current_date, expected_code, expected_res):
        if request.method == 'POST':
            parser = ConfigParser()
            parser.read('config.ini')  # reading config.ini to fetch port and other details

            sl_no = fetch_file_data(file_name)  # fetching sl_no from file
            update_file_content(file_name, sl_no + 1)  # each time updating file content

            # receiving header data to the dict
            header_data1 = header_data()  # fetching header data to dictionary
            for key in list(header_data1):
                if len(header_data1[key]) > 0:
                    print(header_data1[key])
                else:
                    header_data1.pop(key)# if length is not greater than 0 that pop that field from list

            #  genrating api_url and storing into api_url variable
            api_url = parser.get('Gcontrol', 'type') + "://" + parser.get('Gcontrol','IP') + ":" + parser.get('Gcontrol', 'port') + \
                      "/" + parser.get('Gcontrol', 'Name') + "/" + api_name

            #  creating list with all parameters, then writing them to the csv_file. SAME FALLOWS FOR NEXT METHODS ALSO.
            fieldnames = ["sl_no", "tc_status", "tc_name", "api_type", "tc_desc", "name",
                          "current_date", "api_url", "header", "body", "expected_code", "expected_res"]
            res = not path.exists("Gcontrol_Testcases.csv")
            with open('Gcontrol_Testcases.csv', 'a', newline="") as inFile:
                writer = csv.DictWriter(inFile, fieldnames=fieldnames, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                if res == True:
                    writer.writeheader()
                writer.writerow({"sl_no": sl_no, "tc_status": tc_status, "tc_name": tc_name, "api_type": api_type, "tc_desc": tc_desc,
                                "name": name, "current_date": current_date, "api_url": api_url, "header": header_data1, "body": None,
                                "expected_code": expected_code, "expected_res": expected_res})

    def fun2(api_name, file_name, api_type, tc_status, tc_name, tc_desc, name, current_date, expected_code, expected_res, body_data):
        if request.method == 'POST':
            parser = ConfigParser()
            parser.read('config.ini')
            sl_no = fetch_file_data(file_name)
            update_file_content(file_name, sl_no + 1)

            header_data1 = header_data()
            for key in list(header_data1):
                if len(header_data1[key]) > 0:
                    print(header_data1[key])
                else:
                    header_data1.pop(key)

            api_url = parser.get('Gcontrol', 'type') + "://" + parser.get('Gcontrol', 'IP') + ":" \
                      + parser.get('Gcontrol', 'port') + "/" + parser.get('Gcontrol', 'Name') + "/device/" + api_name
            fieldnames = ["sl_no", "tc_status", "tc_name", "api_type", "tc_desc", "name", "current_date", "api_url", "header", "body", "expected_code", "expected_res"]
            res = not path.exists("Gcontrol_Testcases.csv")
            with open('Gcontrol_Testcases.csv', 'a', newline="") as inFile:
                writer = csv.DictWriter(inFile, fieldnames=fieldnames, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                if res == True:
                    writer.writeheader()
                writer.writerow({"sl_no": sl_no, "tc_status": tc_status, "tc_name": tc_name, "api_type": api_type, "tc_desc": tc_desc,
                     "name": name, "current_date": current_date, "api_url": api_url, "header": header_data1,"body": body_data,
                     "expected_code": expected_code, "expected_res": expected_res})

    def fun3(api_name, api_type, file_name, tc_status, tc_name, tc_desc, name, current_date, expected_code, expected_res, body_data):
        if request.method == 'POST':
            parser = ConfigParser()
            parser.read('config.ini')  # reading config.ini to fetch port and other details

            sl_no = fetch_file_data(file_name)  # fetching sl_no from file
            update_file_content(file_name, sl_no + 1)  # each time updating file content

            # receiving header data to the dict
            header_data1 = header_data()  # fetching header data to dictionary
            for key in list(header_data1):
                if len(header_data1[key]) > 0:
                    print(header_data1[key])
                else:
                    header_data1.pop(key)  # if length is not greater than 0 that pop that field from list

            deviceid = request.form['deviceid']
            #  generating api_url and storing into api_url variable
            api_url = parser.get('Gcontrol', 'type') + "://" + parser.get('Gcontrol', 'IP') + ":" + parser.get(
                'Gcontrol', 'port') + "/" + parser.get('Gcontrol', 'Name') + "/device/" + deviceid + "/dataPlans"

            #  creating list with all parameters, then writing them to the csv_file. SAME FALLOWS FOR NEXT METHODS ALSO.
            fieldnames = ["sl_no", "tc_status", "tc_name", "api_type", "tc_desc", "name",
                          "current_date", "api_url", "header", "body", "expected_code", "expected_res"]
            res = not path.exists("Gcontrol_Testcases.csv")
            with open('Gcontrol_Testcases.csv', 'a', newline="") as inFile:
                writer = csv.DictWriter(inFile, fieldnames=fieldnames, delimiter='|', quotechar='"',
                                        quoting=csv.QUOTE_MINIMAL)
                if res == True:
                    writer.writeheader()
                writer.writerow({"sl_no": sl_no, "tc_status": tc_status, "tc_name": tc_name, "api_type": api_type, "tc_desc": tc_desc,
                                 "name": name, "current_date": current_date, "api_url": api_url, "header": header_data1, "body": None,
                                 "expected_code": expected_code, "expected_res": expected_res})

    def fun6(api_name, file_name, api_type, tc_status, tc_name, tc_desc, name, current_date, expected_code, expected_res, body_data):
        if request.method == 'POST':
            parser = ConfigParser()
            parser.read('config.ini')
            sl_no = fetch_file_data(file_name)
            update_file_content(file_name, sl_no + 1)

            header_data1 = header_data()
            for key in list(header_data1):
                if len(header_data1[key]) > 0:
                    print(header_data1[key])
                else:
                    header_data1.pop(key)
            if request.form.get("prodname_0") != None:  # fetching and handling checkbox
                qp = request.form.get("prodname_0")
            elif request.form.get("prodname_1") != None:
                qp = request.form.get("prodname_1")
            elif request.form.get("prodname_2") != None:
                qp = request.form.get("prodname_2")
            else:
                qp = ""
            qp_value = request.form['item_0']

            if api_type == 14 or api_type == 15:
                from_date = request.form['date']
                to_date = request.form.get('date1')
                api_url = parser.get('Gcontrol', 'type') + "://" + parser.get('Gcontrol', 'IP') + ":" \
                          + parser.get('Gcontrol', 'port') + "/" + parser.get('Gcontrol','Name') + "/device/" + api_name + "?" + qp + "=" + qp_value \
                          + "&fromDate=" + from_date + "&toDate=" + to_date
            else:
                api_url = parser.get('Gcontrol', 'type') + "://" + parser.get('Gcontrol', 'IP') + ":" \
                          + parser.get('Gcontrol', 'port') + "/" + parser.get('Gcontrol', 'Name') + "/device/" + api_name +"?" + qp + "=" + qp_value
            fieldnames = ["sl_no", "tc_status", "tc_name", "api_type", "tc_desc", "name", "current_date", "api_url", "header", "body", "expected_code", "expected_res"]
            res = not path.exists("Gcontrol_Testcases.csv")
            with open('Gcontrol_Testcases.csv', 'a', newline="") as inFile:
                writer = csv.DictWriter(inFile, fieldnames=fieldnames, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                if res == True:
                    writer.writeheader()
                writer.writerow({"sl_no": sl_no, "tc_status": tc_status, "tc_name": tc_name, "api_type": api_type, "tc_desc": tc_desc,
                     "name": name, "current_date": current_date, "api_url": api_url, "header": header_data1, "body": None,
                     "expected_code": expected_code, "expected_res": expected_res})

# Assigning templates and static folders path. This will change for diff users
# template_dir = os.path.abspath('C:\\Users\\gagan.v\\Desktop\\api_automation_code_today\\templates')
# static_dir = os.path.abspath('C:\\Users\\gagan.v\\Desktop\\api_automation_code_today\\static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'), static_folder=os.path.join(BASE_DIR, 'static'))

app.config['SECRET_KEY'] = '8b84744fab5ee5771f665869e269dcc4'

# Genrating log for error
if not app.debug:
    file_handler = FileHandler("python.log")
    file_handler.setLevel(WARNING)
    app.logger.addHandler(file_handler)

@app.route("/")  # home page(apihome.html) this page used to select create or execute testcase
@app.route("/home")
def Home():
    try:
        return render_template("Common/apihome.html")
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/create")  # create page(apicreate.html) this page is to select for which api we should create testcase
def Create():
    try:
        return render_template("Common/apicreate.html")
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/GC_create")  # create page(apicreate.html) this page is to select for which api we should create testcase
def GC_Create():
    try:
        return render_template("Common/GC_API_Create.html")
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/customercreate")  # take note of this decorator syntax, it's a common pattern
def CustomerCreate():  # customer selection page to create the testcases(customercreate.html) this page to select the customer to create testcase
    try:
        return render_template("Common/Customercreate.html")
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/create/get_sim_details_api")  # Test-case creation page for getSimDetails page(Get_Sim_Details.html)
def Get_Sim_Details_API():
    try:
        api_url1 = Daimler.api_url  # fetch api_url from the Daimler class
        return render_template('API/Daimler/Get_Sim_Details.html',
                               value=api_url1)  # passing api_url for Get_Sim_Details.html page
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/create/get_sim_state_api")  # Test-case creation page for getSimState page(Get_Sim_State.html)
def Get_Sim_State_API():
    try:
        return render_template('API/Daimler/Get_Sim_State.html')
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/create/suspend_sim_api")  # Test-case creation page for SuspendSim page(Suspend_Sim.html)
def Suspend():
    try:
        return render_template('API/Daimler/Suspend_Sim.html')
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/create/reactivate_sim_api")  # Test-case creation page for reactivateSim page(reactivate.html)
def Reactivate():
    try:
        return render_template('API/Daimler/Reactivate.html')
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/create/update_settings_api")  # Test-case creation page for update_settings page(UpdateSettings.html)
def Update_Settings():
    try:
        return render_template('API/Daimler/Update_Settings.html')
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/create/ping_api")  # Test-case creation page for ping page(Ping.html)
def Ping():
    try:
        return render_template('API/Daimler/Ping.html')
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/create/dataPlans")  # Test-case creation page for dataPlans page(dataPlans.html)
def dataPlans():
    try:
        return render_template('API/Gcontrol/dataPlans.html')
    except Exception as e:
        return render_template("Common/error.html")


@app.route("/create/attachDataPlans")  # Test-case creation page for ping page(attachDataPlan.html)
def attachDataPlans():
    try:
        return render_template('API/Gcontrol/attach_Data_Plan.html')
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/create/getAttachedDataPlans")  # Test-case creation page for ping page(attachDataPlan.html)
def getAttachedDataPlans():
    try:
        return render_template('API/Gcontrol/Get_Attached_Data_Plan.html')
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/create/modifyDataPlans")  # Test-case creation page for ping page(attachDataPlan.html)
def modifyDataPlans():
    try:
        return render_template('API/Gcontrol/Modify_Data_Plan.html')
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/create/changeState")  # Test-case creation page for ping page(attachDataPlan.html)
def changeState():
    try:
        return render_template('API/Gcontrol/change_state.html')
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/create/deviceState")  # Test-case creation page for ping page(attachDataPlan.html)
def deviceState():
    try:
        return render_template('API/Gcontrol/device_state.html')
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/create/sessionInfo")  # Test-case creation page for ping page(attachDataPlan.html)
def sessionInfo():
    try:
        return render_template('API/Gcontrol/session_info.html')
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/create/dataUsage")  # Test-case creation page for ping page(attachDataPlan.html)
def dataUsage():
    try:
        return render_template('API/Gcontrol/data_usage.html')
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/create/sessionHistory")  # Test-case creation page for ping page(attachDataPlan.html)
def sessionHistory():
    try:
        return render_template('API/Gcontrol/session_history.html')
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/create/deviceList")  # Test-case creation page for ping page(attachDataPlan.html)
def deviceList():
    try:
        return render_template('API/Gcontrol/device_list.html')
    except Exception as e:
        return render_template("Common/error.html")

@app.route('/create', methods=['POST'])  # fetching data from html-page fields
def save_data():
    try:
        body_data = {}
        file_name = "sl_no.txt"  # fetching sl.no from slno.txt
        tc_status = "Active"
        tc_name = request.form['tcname']  # REQUEST.FORM["NAME OF THE FIELD"] to fetch data from that field
        api_name = request.form['submit']
        api_type = api_type_check(api_name)  # calling api_type_check(line_no:20) method to obtain the api type
        print(api_type)
        tc_desc = request.form['desc']
        name = request.form['createdby']
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # now() to get current date and time
        expected_code = request.form['ec']
        expected_res = request.form['em']

        if api_type == 1 or api_type == 2:  # calling the corr methods based on the api type
            Daimler.fun1(api_name, api_type, file_name, tc_status, tc_name, tc_desc, name, current_date,
                                expected_code, expected_res)  # Here Daimler is the  class name and fun1 is method name and passing common parameters to reduce code length
        elif api_type == 3 or api_type == 4:
            Daimler.fun2(api_name, file_name, api_type, tc_status, tc_name, tc_desc, name, current_date,
                                expected_code, expected_res)
        elif api_type == 5:
            Daimler.fun3(api_name, file_name, api_type, tc_status, tc_name, tc_desc, name, current_date,
                                expected_code, expected_res)

        elif api_type == 6:
            body_data = request.form["profiledata"]  #only update_settings have profile data so obtaining data from that here
            Daimler.fun4(api_name, file_name, api_type, tc_status, tc_name, tc_desc, name, current_date,
                                expected_code, expected_res, body_data)
        elif api_type == 7:
            Gcontrol.fun1(api_name, api_type, file_name, tc_status, tc_name, tc_desc, name, current_date,
                         expected_code, expected_res)
        elif api_type == 8 or api_type == 10 or api_type == 11 or api_type == 16:
            body_data = request.form["profiledata"]
            Gcontrol.fun2(api_name, file_name, api_type, tc_status, tc_name, tc_desc, name, current_date,
                         expected_code, expected_res, body_data)
        elif api_type == 9:
            Gcontrol.fun3(api_name, api_type, file_name, tc_status, tc_name, tc_desc, name, current_date,
                          expected_code, expected_res, body_data)
        elif api_type == 12 or api_type == 13 or api_type == 14 or api_type == 15:
            Gcontrol.fun6(api_name,file_name, api_type, tc_status, tc_name, tc_desc, name, current_date,
                         expected_code, expected_res, body_data)
        else:
            pass
        return render_template("Common/Customercreate.html")
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/customerexecute")  # take note of this decorator syntax, it's a common pattern
def CustomerExecute():
    try:
        return render_template("Common/Customerexecute.html")
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/customer/execute")  # Execute page
def Execute():
    try:
        return render_template('Common/apiexecute.html')
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/Gcontrol/execute")  # Execute page
def Gcontrol_Execute():
    try:
        return render_template('Common/Gcontrol_execute.html')
    except Exception as e:
        return render_template("Common/error.html")

api_list = []
@app.route("/customer/execute/processing", methods=['GET', 'POST'])
def Processing():
    try:
        data_in_api_list = None
        if request.method == 'POST':
            file_name = "final_data.csv"
            api_names = request.form.getlist('cbg1[]')
            print(api_names)

            data_reader = csv.DictReader(open(file_name), delimiter="|")
            for row in data_reader:
                print(row['api_type'] in api_names)
                if row['api_type'] in api_names:
                    api_list.append(list(row.values()))
            data_in_api_list = len(api_list)

        return render_template('Common/processing.html', final=api_list, len_final=data_in_api_list)
    except Exception as e:
        return render_template("Common/error.html")


@app.route("/customer/execute/gcprocessing", methods=['GET', 'POST'])
def GCProcessing():
    try:
        data_in_api_list = None
        if request.method == 'POST':
            file_name = "Gcontrol_Testcases.csv"
            api_names = request.form.getlist('cbg1[]')

            data_reader = csv.DictReader(open(file_name), delimiter="|")
            print(api_names)
            for row in data_reader:
                print(row['api_type'] in api_names)
                if row['api_type'] in api_names:
                    api_list.append(list(row.values()))
            data_in_api_list = len(api_list)

        return render_template('Common/processing1.html', final=api_list, len_final=data_in_api_list)
    except Exception as e:
        return render_template("Common/error.html")


@app.route("/customer/execute/executeresult", methods=['GET', 'POST'])
def ExecuteResult():
    try:
        if request.method == 'POST':
            data_in_api_list = len(api_list)
        return render_template("Common/ExecuteResult.html", final=api_list, len_final=data_in_api_list)  #passing same list to ExecuteResult.html page
    except Exception as e:
        return render_template("Common/error.html")

@app.route("/customer/execute/executeresult/failresult", methods=['GET', 'POST'])  # fail result age to display faild testcases here u should add code sir
def FailResult():
    try:
        data_in_api_list = len(api_list)
        return render_template("Common/Failed_test_case.html", final=api_list, len_final=data_in_api_list)
    except Exception as e:
        return render_template("Common/error.html")


if __name__ == "__main__":
    app.run(debug=True)