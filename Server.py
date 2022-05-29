import requests


class Server:

    def __init__(self, url, header):
        self.header = header
        self.url = url

    def uploadResource(self, report_type, resource):

        r = requests.post("{}/{}".format(self.url, report_type),
                          data=resource, headers=self.header)
        if r.status_code == 201:
            print("Successfully created resources on the server")
        else:
            print("The status code is{}".format(r.status_code))

    def queryData(self, report_type, query_info):

        r = requests.get("{}/{}?{}".format(self.url, report_type, query_info),
                         headers=self.header)

        if r.status_code == 200:
            print("Successfully query the data from server")
            return r
        else:
            return print("The status code is{}. Failed to query the data".format(r.status_code))
