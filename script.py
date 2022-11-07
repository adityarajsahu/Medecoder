import os
import django
import cv2
import json

from prescription.models import Prescription

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MEDECODER.settings')
django.setup()

image_and_annotations = 'imageAnnotations/'
if not os.path.exists(image_and_annotations):
    os.makedirs(image_and_annotations)

records = Prescription.objects.all()
for record in records:
    image_path = str(record.image)
    img = cv2.imread(image_path)
    filename = image_path.split('/')[1]
    dir_name = filename.split('.')[0]
    # print(dir_name)

    if not os.path.exists(image_and_annotations + dir_name):
        os.makedirs(image_and_annotations + dir_name)

    # print(image_and_annotations + filename)
    save_image_path = image_and_annotations + dir_name + '/' + filename
    # print(save_path)
    cv2.imwrite(save_image_path, img)
    # print(record.annotation)

    json_response = record.annotation
    save_json_path = image_and_annotations + dir_name + '/' + dir_name + '_annotation.json'
    # print(save_json_path)
    with open(save_json_path, 'w') as file:
        json.dump(json_response, file)
