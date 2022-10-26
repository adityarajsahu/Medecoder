from django.shortcuts import render, redirect
from .models import Prescription
import re
from django.http import JsonResponse
import json
from .utils import viewAnnotation

import boto3
from .utils import convert
from decouple import config
ACCESS_KEY_ID = config('ACCESS_KEY_ID')
ACCESS_SECRET_KEY = config('ACCESS_SECRET_KEY')
s3 = boto3.client('s3',aws_access_key_id = ACCESS_KEY_ID,aws_secret_access_key = ACCESS_SECRET_KEY)
s3 = boto3.client('s3',aws_access_key_id=ACCESS_KEY_ID,aws_secret_access_key= ACCESS_SECRET_KEY,)
textract = boto3.client('textract',aws_access_key_id=ACCESS_KEY_ID,aws_secret_access_key = ACCESS_SECRET_KEY, region_name='us-west-2')
BUCKET_NAME = config('BUCKET_NAME')
comprehendmedical = boto3.client('comprehendmedical', aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key = ACCESS_SECRET_KEY, region_name='us-west-2')

# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        return render(request, 'pages/homepage.html')
    else:
        return redirect('login')


def uploadPrescription(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'pages/uploadPrescription.html')
        elif request.method == 'POST':
            image = request.FILES['prescription_image']
            obj = Prescription(uploaded_by=request.user, image=image)
            obj.save()
            predictPrescription(request, obj.id)
            return redirect('singleViewPres', prescription_id=obj.id)
    else:
        return redirect('login')

def viewPrescription(request):

    if request.user.is_authenticated:
        data = {
            'prescriptions' : Prescription.objects.all(),
        }
        return render(request, 'pages/viewPrescription.html', context=data)
    else:
        return redirect('login')

def visualizeAnnotation(request, prescription_id):
    if request.user.is_authenticated:
        annotation = None
        prescription = Prescription.objects.get(id=prescription_id)
        annotation = prescription.annotation
        annotated_image, digitized_image = viewAnnotation(annotation, image_path = prescription.image.url)
        context = {
            'prescription':prescription,
            'annotated_image_uri': annotated_image,
            'digitised_image_uri': digitized_image,
        }
        return render(request, 'pages/visualise.html', context=context)
    else:
        return redirect('login')

def Prescriptions(request):

    if request.user.is_authenticated:
        return render(request, 'pages/prescriptions.html')
    else:
        return redirect('login')

# def Dashboard(request):

#     if request.user.is_authenticated:
#         return render(request, 'pages/dashboard.html')
#     else:
#         return redirect('login')
def addMedication(request, prescription_id):
    if request.user.is_authenticated:
        prescription = Prescription.objects.get(id=prescription_id)
        annotation = Prescription.objects.get(id=prescription_id).annotation
        url = prescription.image.url+"/-1"
        res = ''
        
        PROTECTED_HEALTH_INFORMATION = []
        info = {}
        Medication = {}
        med=[]
        c = []
        ph=[]
        f=[]
        test_treatment = []
        medicalCondition = []
        Anatomy = []

        if len(annotation[url]['regions']):
            for r in annotation[url]['regions']:
                res+=" "+r['region_attributes']['text']
            print("Extracted Text =====> ", res)
            result = comprehendmedical.detect_entities(Text= res)
            entities = result['Entities']
            
            # print(entities)
            for key in entities:
                
                if key['Category'] == 'PROTECTED_HEALTH_INFORMATION':
                    ph.append(key['Text'])
                    ph.append(key['Type'])
                    f.append(ph)
                    ph=[]

                elif key['Category'] == 'MEDICATION':
                    med.append(key['Text'])
                    med.append('N.A')
                    med.append('N.A.')
                    
                    dosage = -1
                    frequency = -1
                    if 'Attributes' in key:
                        for i in key['Attributes']:
                            if i['Type'] == 'DOSAGE':
                                dosage = i['Text']
                                med[1]=i['Text']
                            elif i['Type'] == 'FREQUENCY':
                                frequency =  i['Text']
                                med[2]=i['Text']
                        c.append(med)
                        med=[]

                        if key['Text'] not in Medication:
                            Medication[key['Text']] = [dosage,frequency]

                elif  key['Category'] == 'TEST_TREATMENT_PROCEDURE':
                    test_treatment.append(key['Text'])
                elif key['Category'] == 'MEDICAL_CONDITION':
                    medicalCondition.append(key['Text'])
                elif key['Category'] == 'ANATOMY':
                    Anatomy.append(key['Text'])

        prescription.medication = Medication
        prescription.save()
        context={
            'med':c,
            'protected_health_info' : f,
            'test_treatment' : test_treatment,
            'medicalCondition' : medicalCondition,
            'Anatomy' : Anatomy
        }
        print(PROTECTED_HEALTH_INFORMATION)
        print(Medication)
        return render(request, 'pages/medication.html',context=context)
    else:
        return redirect('login')

def singleView(request, prescription_id):
    if request.user.is_authenticated:
        if Prescription.objects.get(id=prescription_id).medication:
            p=True
        else:
          p=False

        prescription = Prescription.objects.get(id=prescription_id)
        annotation = Prescription.objects.get(id=prescription_id).annotation
        url = prescription.image.url+"/-1"
        extracted_text = ''
        
        for r in annotation[url]['regions']:
            extracted_text+=" "+r['region_attributes']['text']
        print("Extracted Text =====> ", extracted_text)

        context = {
            'prescription': Prescription.objects.get(id=prescription_id),
            'predicted':p,
            'extracted_text' : extracted_text
        }
        return render(request, 'pages/singleView.html', context=context)
    else:
        return redirect('login')

def annotatePrescription(request, prescription_id):
    if request.user.is_authenticated:
        context = {
            'prescription': Prescription.objects.get(id=prescription_id),
        }
        return render(request, 'annotator/via.html', context=context)
    else:
        return redirect("login")

def medication(result):
    res = ''
    for word in result:
        res += word[1]+ ' '
    comprehendmedical = boto3.client('comprehendmedical', 
                                        aws_access_key_id=ACCESS_KEY_ID,
                                        aws_secret_access_key = ACCESS_SECRET_KEY, 
                                        region_name='us-west-2')

    result = comprehendmedical.detect_entities(Text= res)
    entities = result['Entities']

def predictPrescription(request, prescription_id):
    if request.user.is_authenticated:
        image_data = Prescription.objects.get(id=prescription_id).image
        img = str(image_data)
        if img:
            response = s3.upload_file( 
                Bucket = BUCKET_NAME,
                Filename=img,
                Key = img
            )
        objs = s3.list_objects_v2(Bucket=BUCKET_NAME)['Contents']
        objs.sort(key=lambda e: e['LastModified'], reverse=True)
        first_item = list(objs[0].items())[0]
        documentName = str(first_item[1])
        # Call Amazon Textract
        with open(documentName, "rb") as document:
            response = textract.analyze_document(
                Document={
                    'Bytes': document.read(),
                },
                FeatureTypes=["FORMS"])
        preds = convert(response,img,img.split('/')[-1])
        prescription = Prescription.objects.get(id=prescription_id)
        prescription.annotation= preds
        prescription.save()
    else:
        return redirect("login")

def addAnnotation(request, prescription_id):
    prescription = Prescription.objects.get(id=prescription_id)
    annotations = request.POST['annotation']
    annotations = json.loads(annotations)
    prescription.annotation = annotations
    prescription.save()
    return JsonResponse({"abc":"dad"})