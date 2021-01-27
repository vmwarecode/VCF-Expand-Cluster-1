import json
import time
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Utils:
    def __init__(self, args):
        if len(args) < 4:
             print ("Refer documentation for correct usage.")
             exit(0)
        self.hostname = args[1]
        self.username = args[2]
        self.password = args[3]
        self.header = {'Content-Type': 'application/json'}
        self.token_url = 'https://'+ self.hostname +'/v1/tokens'
        self.get_token()
    
    def get_token(self):
        payload = {"username": self.username,"password": self.password}
        response = self.post_request(payload=payload,url=self.token_url)
        token = response['accessToken']
        self.header['Authorization'] = 'Bearer ' + token
    
    def get_request(self,url):
        self.get_token()
        response = requests.get(url, headers=self.header,verify=False)
        if(response.status_code == 200):
            data = json.loads(response.text)
        else:
            print ("Error reaching the server.")
            exit(1)
        return data

    def post_request(self,payload,url):
        response = requests.post(url, headers=self.header, json=payload,verify=False)
        if(response.status_code == 200 or response.status_code == 202):
            data = json.loads(response.text)
            return data
        else:
            print ("Error reaching the server.")
            print (response.text)
            exit(1)
    
    def patch_request(self,payload,url):
        response = requests.patch(url, headers=self.header, json=payload,verify=False)
        if(response.status_code == 202):
            data = json.loads(response.text)
            return data
        elif(response.status_code == 200):
            return
        else:
            print ("Error reaching the server from patch.")
            print (response.text)
            exit(1)

    def poll_on_id(self,url,task):
        key = ''
        if(task):
            key = 'status'
        else:
            key = 'executionStatus'
        status = self.get_request(url)[key]
        while(status in ['In Progress','IN_PROGRESS','Pending']):
            response = self.get_request(url)
            status = response[key]
            time.sleep(10)
        if(task):
            return status
        if(status == 'COMPLETED'):
            return response['resultStatus']
        else:
            print ('Operation failed')
            exit(1)
    
    def delete_request(self,payload,url):
        response = requests.delete(url,json=payload,headers=self.header,verify=False)
        if(response.status_code == 202):
            data = json.loads(response.text)
            return data
        else:
            print ("Error reaching the server.")
            print (response.text)
            exit(1)
    
    def read_input(self, file):
        with open(file) as json_file:
            data = json.load(json_file)
        return data
