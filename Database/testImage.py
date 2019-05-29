from wand.display import display
from wand.image import Image
with Image('ProfPic1.jpg') as img:
     display(img)

# import boto3
# from io import BytesIO
# import matplotlib.image as mpimg
# import matplotlib.pyplot as plt

# resource = boto3.resource('s3', region_name='us-east-2')
# bucket = resource.Bucket('sentinel-s2-l1c')

# image_object = bucket.Object('tiles/10/S/DG/2015/12/7/0/B01.jp2')
# image = mpimg.imread(BytesIO(image_object.get()['Body'].read()), 'jp2')

# plt.figure(0)
# plt.imshow(image)