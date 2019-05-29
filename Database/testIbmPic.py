import ibm_boto3
from ibm_botocore.client import Config
import json
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from io import BytesIO,StringIO
from PyQt5.QtWidgets import QApplication
from ImageDisplay import ImgDisp

api_key="QjdqyfGUkNSkfyl_vra0ZeZAQ5gtlrFTgCz23HtqumMU"
service_instance_id = 'crn:v1:bluemix:public:cloud-object-storage:global:a/7a60e8eb91e143b592776e8f81207d4f:a4edf4d5-13ea-4e79-965f-0c882c015b71::'
auth_endpoint = 'https://iam.bluemix.net/oidc/token'
service_endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'

file=BytesIO()
cos=ibm_boto3.resource('s3',ibm_api_key_id=api_key,ibm_service_instance_id=service_instance_id,ibm_auth_endpoint=auth_endpoint,config=Config(signature_version='oauth'),endpoint_url=service_endpoint)
# cos.Object('personpictures','Calvin').put(Body='ProfPic.jpg')
pic_obj=cos.Object('personpictures','Calvin').get()['Body'].read()
# image=mpimg.imread(BytesIO(pic_obj),'jpg')
# print(picture)
# plt.figure()
# plt.show(image)
print(pic_obj.decode('utf-8'))
j=json.loads(pic_obj.decode('utf-8'))
print(j)
App=QApplication(sys.argv)
window=ImgDisp(j)
App.exec_()


# for bucket in cos.Bucket('personpictures').objects.all():
#     print(bucket)