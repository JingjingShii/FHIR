
class Data:
    def __init__(self, patient_id, test_date, code, conclusion, diag_code):
        self.patient_id = patient_id
        self.test_date = test_date
        self.code = code,
        self.conclusion = conclusion
        self.diag_code = diag_code

    def template(self, codeList):
        conclusioncode_template = {
                    "system": "http://snomed.info/sct",
                    "code": codeList[0],
                    "display": codeList[1]
                }
        return conclusioncode_template

    def to_fhir(self):

        conclusionCode = []

        for item in self.diag_code:
            conclusionCode.append(self.template(item))

        # assume all diagnostic services are Genetics (GE)
        report = {
            "resourceType": "DiagnosticReport",
            "id": "{}".format(self.patient_id),
            "status": "final",
            "subject": {
                "reference": "Patient/{}".format(self.patient_id)
            },
            "effectiveDateTime": self.test_date,
            "category": [{
                "coding": [{
                    "system": "http://hl7.org/fhir/v2/0074",
                    "code": "GE",
                    "display": "Genetics"}]
            }],
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": self.code[0][0],
                    "display": self.code[0][1]}]
            },
            "conclusion": self.conclusion,
            "conclusionCode": [
                {
                    "coding":conclusionCode
                }
            ]
        }

        url = report['resourceType'] + "/" + report['id']

        out = {
            "resourceType": "Bundle",
            "type": "collection",
            "entry": [{'resource': report, 'request': {'method': 'PUT', 'url': url}}]}

        return out
