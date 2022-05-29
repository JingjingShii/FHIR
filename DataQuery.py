from Data import Data
from Server import Server
import json
import csv
import datetime

test_code = {
    "exome": ["LP248469-1", "Whole exome sequence analysis"],
    "whole genome": ["LP248470-9", "Whole genome sequence analysis"],
    "panel": ["LP7838-8", "PANEL.UA"],
    "wgs": ["LP248470-9", "Whole genome sequence analysis"],
    "gene panel": ["LP70592-8", "PANEL.HL7.GENETICS"]
}

diagnosis_code = {
    "Gitelman's syndrome": ["707756004", "Gitelman syndrome"],
    "Distal renal tubular acidosis": ["236461000", "Distal renal tubular acidosis"],
    "Sjogren syndrome": ["83901003", "Sjögren's syndrome"],
    "IgA glomerulonephritis": ["236407003", "IgA nephropathy"],
    "gitelman syndrome": ["707756004", "Gitelman syndrome"],
    "bartter syndrome": ["707742001", "Bartter syndrome"],
    "familial nephrotic syndrome": ["783614008",
                                    "Familial steroid-resistant nephrotic syndrome with sensorineural deafness"],
    "distal renal tubular acidosis": ["236461000", "Distal renal tubular acidosis"]
}

# Generate resources from json format
file = open('input1.json')

data = json.load(file)

for item in data:
    patient_id = item["patientId"]
    test_type = item["test_type"]
    test_date = item["test_date"]
    code = test_code[test_type]

    if (item['differentialDiagnosis'] == []):
        diagnosis = item['confirmedDiagnosis']
        diag_code = [diagnosis_code[diagnosis]]
        conclusion = diag_code[0][1]
        data = Data(patient_id, test_date, code, conclusion, diag_code)
        r = Data.to_fhir(data)

    else:
        diagnosis = item['differentialDiagnosis']
        conclusion = ""
        diag_code = []
        for ele in diagnosis:
            diag_code.append(diagnosis_code[ele])

        data = Data(patient_id, test_date, code, conclusion, diag_code)
        r = Data.to_fhir(data)

    with open('{}.json'.format(patient_id), 'w') as outfile:
        json.dump(r, outfile)

# Generate resource from csv format
with open('input2.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        if (row[0] != "stud_num"):
            patient_id = row[1]
            test_type = row[2]
            test_date = row[3]

            test_date = datetime.datetime.strptime(test_date, '%d/%m/%y').strftime('%y-%m-%d')
            # assume all the years start with 20
            test_date = "20" + str(test_date)
            code = test_code[test_type]

            if (row[-1] == ""):

                diagnosis = [row[4], row[5], row[6]]
                conclusion = ""
                diag_code = []
                for ele in diagnosis:
                    if ele != "":
                        diag_code.append(diagnosis_code[ele])

                data = Data(patient_id, test_date, code, conclusion, diag_code)
                r = data.to_fhir()


            else:
                diagnosis = row[-1]
                diag_code = [diagnosis_code[diagnosis]]
                conclusion = diag_code[0][1]

                data = Data(patient_id, test_date, code, conclusion, diag_code)
                r = data.to_fhir()

            with open('{}.json'.format(patient_id), 'w') as outfile:
                json.dump(r, outfile)

#---------------------------------------------------------------------
# example about query the data from server
r = json.load("A0001.json")
headers={"Content-Type":"json"}
s = Server("http://localhost:8000", headers)
# upload the resource to server
s.uploadResource("DiagnosticReport", r)
# query the data from server
s.queryData("DiagnosticReport", "conclusion=Gitelman syndrome")
