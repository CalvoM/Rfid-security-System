import ibm_boto3
from ibm_botocore.client import Config
import sys
from PyQt4.QtGui import QApplication
from ImageDisplay import ImageDisplay

class IbmCosPic():
    
    def __init__(self):
        self.api_key                ="QjdqyfGUkNSkfyl_vra0ZeZAQ5gtlrFTgCz23HtqumMU"
        self.service_instance_id    ="crn:v1:bluemix:public:iam-identity::a/7a60e8eb91e143b592776e8f81207d4f::serviceid:ServiceId-bd09d987-58c3-4756-8ba6-f79a863249ce"
        self.auth_endpoint          ="https://iam.bluemix.net/oidc/token"
        self.service_endpoint       ="https://s3-api.us-geo.objectstorage.softlayer.net"
        self.cos                    =ibm_boto3.resource('s3',ibm_api_key_id=self.api_key,ibm_service_instance_id=self.service_instance_id,ibm_auth_endpoint=self.auth_endpoint,config=Config(signature_version='oauth'),endpoint_url=self.service_endpoint)
        
        
    def ibm_upload_pic(self,bucket_name,pic_name):
        self.cos.Object(bucket_name,pic_name).upload_file(pic_name)
    
    def ibm_download_pic(self,bucket_name,pic_name):
        self.pic_obj=self.cos.Object(bucket_name,pic_name).get()['Body'].read()
        with open('one.jpg','wb') as picFile:
            picFile.write(self.pic_obj)
        App=QApplication(sys.argv)
        Window=ImageDisplay('one.jpg')
        sys.exit(App.exec_())