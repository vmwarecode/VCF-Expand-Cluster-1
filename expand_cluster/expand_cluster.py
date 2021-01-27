#Expand Cluster
#Adds given host into a cluster
import sys
import os
sys.path.append(os.path.abspath(__file__ + '/../../'))
from Utils.utils import Utils
import pprint

class ExpandCluster:
    def __init__(self):
        print('Expand Cluster')
        self.utils = Utils(sys.argv)
        self.hostname = sys.argv[1]
        self.cluster_id = sys.argv[4]

    def expand_cluster(self):
        data = self.utils.read_input(os.path.abspath(__file__ +'/../')+'/expand_cluster_spec.json')
        validate_cluster_url =  'https://'+self.hostname+'/v1/clusters/'+self.cluster_id+'/validations'
        print ('Validating the input....')
        response = self.utils.post_request(data,validate_cluster_url)
        if(response['resultStatus'] != 'SUCCEEDED'):
            print ('Validation Failed.')
            exit(1)
        
        expand_cluster_url = 'https://'+self.hostname + '/v1/clusters/'+self.cluster_id
        response = self.utils.patch_request(url=expand_cluster_url,payload=data)
        task_id = response['id']
        url = 'https://'+self.hostname+'/v1/tasks/'+task_id
        print ('Cluster expansion finished with status: ' + self.utils.poll_on_id(url,True))

if __name__== "__main__":
    ExpandCluster().expand_cluster()
