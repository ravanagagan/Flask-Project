from flask import Flask, render_template, request
from logging import WARNING, FileHandler
import os
import csv
import time
from datetime import datetime
from configparser import ConfigParser


def header_data():
    header_data1 = {
        "auth": request.form.get('auth'),
        "acceptlanguage": request.form.get('acceptlanguage'),
        "url": request.form.get('url'),
        "reqid": request.form.get('reqid'),
        "contenttype": request.form.get('contenttype'),
        "accept": request.form.get('accept')
    }
    return header_data1


def api_type_check(data):
    if data == "getSIMDetails":
        return 1
    elif data == "getSIMState":
        return 2
    elif data == "suspendSIM":
        return 3
    elif data == "reactivateSIM":
        return 4
    elif data == "ping":
        return 5
    else:
        return 6


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


class api_automation:
    api_url = None

    def fun1(api_name, api_type, file_name, tc_status, tc_name, tc_desc, name, current_date, expected_code,
             expected_res):

        if request.method == 'POST':
            parser = ConfigParser()
            parser.read('config.ini')
            sl_no = fetch_file_data(file_name)
            update_file_content(file_name, sl_no + 1)

            # receiving header data  to the dict
            header_data1 = header_data()
            for key in list(header_data1):
                if len(header_data1[key]) > 0:
                    print(header_data1[key])
                else:
                    header_data1.pop(key)

            if request.form.get("prodname_0") != None:
                qp = request.form.get("prodname_0")
            elif request.form.get("prodname_1") != None:
                qp = request.form.get("prodname_1")
            else:
                qp = ""

            qp_value = request.form['item_0']

            api_url = parser.get('API_Automation', 'type') + "://" + parser.get('API_Automation',
                                                                                'IP') + ":" + parser.get(
                'API_Automation',
                'port') \
                      + "/" + parser.get('API_Automation', 'Name') + "/" + api_name + "?" + qp + "=" + qp_value

            expected_code = request.form['ec']
            expected_res = request.form['em']

            fieldnames = ['sl_no', 'tc_status', 'tc_name', 'api_type', 'tc_desc', 'name',
                          'current_date', 'api_url', 'auth', 'expected_code', 'expected_res', 'api_name']
            print(fieldnames[11])
            with open('final_data.csv', 'a') as inFile:
                writer = csv.DictWriter(inFile, fieldnames=fieldnames, delimiter='|', quotechar='"',
                                        quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    {'sl_no': sl_no, 'tc_status': tc_status, 'tc_name': tc_name, 'api_type': api_type,
                     'tc_desc': tc_desc,
                     'name': name, 'current_date': current_date, 'api_url': api_url, 'auth': header_data1,
                     'expected_code': expected_code, 'expected_res': expected_res, 'api_name': api_name})

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
        api_url = parser.get('API_Automation', 'type') + "://" + parser.get('API_Automation', 'IP') + ":" \
                  + parser.get('API_Automation', 'port') + "/" + parser.get('API_Automation', 'Name') \
                  + "/" + api_name + "/" + iccid + "?" + qp + "=" + qp_value

        fieldnames = ['sl_no', 'tc_status', 'tc_name', 'api_type', 'tc_desc', 'name',
                      'current_date', 'api_url', 'auth', 'expected_code', 'expected_res', 'api_name']
        with open('final_data.csv', 'a') as inFile:
            writer = csv.DictWriter(inFile, fieldnames=fieldnames, delimiter='|', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                {'sl_no': sl_no, 'tc_status': tc_status, 'tc_name': tc_name, 'api_type': api_type, 'tc_desc': tc_desc,
                 'name': name, 'current_date': current_date, 'api_url': api_url, 'auth': header_data1,
                 'expected_code': expected_code, 'expected_res': expected_res, 'api_name': api_name})

    def fun3(api_name, file_name, api_type, tc_status, tc_name, tc_desc, name, current_date, expected_code,
             expected_res):
        # http: // localhost: 8080 / globetouchAPI / v1 / ping?echo = asdasd
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
        api_url = parser.get('API_Automation', 'type') + "://" + parser.get('API_Automation', 'IP') + ":" \
                  + parser.get('API_Automation', 'port') + "/" + parser.get('API_Automation', 'Name') \
                  + "/" + api_name + "?" + qp + "=" + qp_value

        fieldnames = ['sl_no', 'tc_status', 'tc_name', 'api_type', 'tc_desc', 'name',
                      'current_date', 'api_url', 'header', 'expected_code', 'expected_res', 'api_name']
        with open('final_data.csv', 'a') as inFile:
            writer = csv.DictWriter(inFile, fieldnames=fieldnames, delimiter='|', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                {'sl_no': sl_no, 'tc_status': tc_status, 'tc_name': tc_name, 'api_type': api_type, 'tc_desc': tc_desc,
                 'name': name, 'current_date': current_date, 'api_url': api_url, 'header': header_data1,
                 'expected_code': expected_code, 'expected_res': expected_res, 'api_name': api_name})

    def fun4(api_name, file_name, api_type, tc_status, tc_name, tc_desc, name, current_date, expected_code,
             expected_res, body_data):
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
        api_url = parser.get('API_Automation', 'type') + "://" + parser.get('API_Automation', 'IP') + ":" \
                  + parser.get('API_Automation', 'port') + "/" + parser.get('API_Automation', 'Name') \
                  + "/" + api_name + "/" + deviceid + "/settings?" + qp + "=" + qp_value
        fieldnames = ['sl_no', 'tc_status', 'tc_name', 'api_type', 'tc_desc', 'name',
                      'current_date', 'api_url', 'header', 'body', 'expected_code', 'expected_res', 'api_name']
        with open('final_data.csv', 'a') as inFile:
            writer = csv.DictWriter(inFile, fieldnames=fieldnames, delimiter='|', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                {'sl_no': sl_no, 'tc_status': tc_status, 'tc_name': tc_name, 'api_type': api_type, 'tc_desc': tc_desc,
                 'name': name, 'current_date': current_date, 'api_url': api_url, 'header': header_data1,
                 'body': body_data,
                 'expected_code': expected_code, 'expected_res': expected_res, 'api_name': api_name})


template_dir = os.path.abspath('C:\\Users\\gagan.v\\Desktop\\api_automation_code\\templates')
static_dir = os.path.abspath('C:\\Users\\gagan.v\\Desktop\\api_automation_code\\static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

app.config['SECRET_KEY'] = '8b84744fab5ee5771f665869e269dcc4'

common_path = "C:\\Users\\gagan.v\\Desktop\\api_automation_code\\templates\\Common\\"

if not app.debug:
    file_handler = FileHandler("python.log")
    file_handler.setLevel(WARNING)
    app.logger.addHandler(file_handler)


@app.route("/")
@app.route("/home")
def Home():
    try:
        return render_template("Common/apihome.html")
    except Exception as e:
        return render_template("Common/error.html")


@app.route("/create")
def Create():
    try:
        return render_template("Common/apicreate.html")
    except Exception as e:
        return render_template("Common/error.html")


@app.route("/customercreate")  # take note of this decorator syntax, it's a common pattern
def CustomerCreate():
    try:
        return render_template("Common/Customercreate.html")
    except Exception as e:
        return render_template("Common/error.html")


@app.route("/create/get_sim_details_api")
def Get_Sim_Details_API():
    try:

        api_url1 = api_automation.api_url
        return render_template('API/Daimler/Get_Sim_Details.html', value=api_url1)
    except Exception as e:
        return render_template("Common/error.html")


@app.route("/create/get_sim_state_api")
def Get_Sim_State_API():
    try:

        return render_template('API/Daimler/Get_Sim_State.html')
    except Exception as e:
        return render_template("Common/error.html")


@app.route("/create/suspend_sim_api")
def Suspend():
    try:
        return render_template('API/Daimler/Suspend_Sim.html')
    except Exception as e:
        return render_template("Common/error.html")


@app.route("/create/reactivate_sim_api")
def Reactivate():
    try:

        return render_template('API/Daimler/Reactivate.html')
    except Exception as e:
        return render_template("Common/error.html")


@app.route("/create/update_settings_api")
def Update_Settings():
    try:

        return render_template('API/Daimler/Update_Settings.html')
    except Exception as e:
        return render_template("Common/error.html")


@app.route("/create/ping_api")
def Ping():
    try:

        return render_template('API/Daimler/Ping.html', )
    except Exception as e:
        return render_template("Common/error.html")


@app.route('/create', methods=['POST'])
def save_data():
    try:
        file_name = "sl_no.txt"
        tc_status = "Active"
        tc_name = request.form['tcname']
        api_name = request.form['submit']
        api_type = api_type_check(api_name)
        tc_desc = request.form['desc']
        name = request.form['createdby']
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        expected_code = request.form['ec']
        expected_res = request.form['em']
        if api_type == 1 or api_type == 2:
            api_automation.fun1(api_name, api_type, file_name, tc_status, tc_name, tc_desc, name, current_date,
                                expected_code, expected_res)
        elif api_type == 3 or api_type == 4:
            api_automation.fun2(api_name, file_name, api_type, tc_status, tc_name, tc_desc, name, current_date,
                                expected_code, expected_res)
        elif api_type == 5:
            api_automation.fun3(api_name, file_name, api_type, tc_status, tc_name, tc_desc, name, current_date,
                                expected_code, expected_res)
            print("ping")
        elif api_type == 6:
            body_data = {}
            body_data = request.form["profiledata"]
            api_automation.fun4(api_name, file_name, api_type, tc_status, tc_name, tc_desc, name, current_date,
                                expected_code, expected_res, body_data)
        else:
            pass
        with open('final_data.csv') as input, open('final_data1.csv', 'w', newline='') as output:
            writer = csv.writer(output)
            for row in csv.reader(input):
                if any(field.strip() for field in row):
                    writer.writerow(row)

        with open('final_data1.csv') as input, open('final_data.csv', 'w', newline='') as output:
            writer = csv.writer(output)
            for row in csv.reader(input):
                if any(field.strip() for field in row):
                    writer.writerow(row)
        os.remove('final_data1.csv')
        time.sleep(1)
        return render_template("Common/apicreate.html")
    except Exception as e:
        return render_template("Common/error.html")


@app.route("/customer/execute")
def Execute():
    try:

        return render_template('Common/apiexecute.html', )
    except Exception as e:
        return render_template("Common/error.html")


api_list = []


@app.route("/customer/execute/processing", methods=['GET', 'POST'])
def Processing():
    try:
        if request.method == 'POST':
            file_name = "final_data.csv"
            api_names = request.form.getlist('cbg1[]')

            with open(file_name, 'r') as f:
                Reader = csv.reader(f, delimiter="|")
                data = list(Reader)
                len_of_list = len(data)
            print(api_names)

            for j in range(0, len(api_names)):
                for i in range(0, len_of_list):
                    if api_names[j] == data[i][11]:
                        api_name = list(data[i])
                        api_list.append(api_name)

            for i in api_list:
                print(i)
                print(i[0])

            data_in_api_list = len(api_list)
            time.sleep(1)

        return render_template('Common/processing.html', final=api_list, len_final=data_in_api_list)
    except Exception as e:
        return render_template("Common/error.html")


@app.route("/customer/execute/executeresult", methods=['GET', 'POST'])
def ExecuteResult():
    try:
        if request.method == 'POST':
            data_in_api_list = len(api_list)
        return render_template("Common/ExecuteResult.html", final=api_list, len_final=data_in_api_list)
    except Exception as e:
        return render_template("Common/error.html")


@app.route("/customer/execute/executeresult/failresult", methods=['GET', 'POST'])
def FailResult():
    try:
        data_in_api_list = len(api_list)
        return render_template("Common/Failed_test_case.html", final=api_list, len_final=data_in_api_list)
    except Exception as e:
        return render_template("Common/error.html")


@app.route("/customerexecute")  # take note of this decorator syntax, it's a common pattern
def CustomerExecute():
    try:
        return render_template("Common/Customerexecute.html")
    except Exception as e:
        return render_template("Common/error.html")


if __name__ == "__main__":
    # port = 5000
    # url = "http://127.0.0.1:{0}".format(port)
    #
    # threading.Timer(1.25, lambda: webbrowser.open(url))
    app.run(debug=True)