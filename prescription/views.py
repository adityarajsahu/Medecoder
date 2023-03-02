from django.shortcuts import render, redirect
from numpy import array
from .models import Prescription, Approval, CustomerPrescription
from django.http import JsonResponse
import json
from .utils import viewAnnotation, scrapeMedicineImage, sendTextWhatsapp

import boto3
from .utils import convert,calculateConfidence,isSimilarImage,convertJson,CustomerConvert
from decouple import config
from PIL import Image
import img2pdf
import os

from fpdf import FPDF
import cv2




from django.contrib.auth import get_user_model
User = get_user_model()


ACCESS_KEY_ID = config('ACCESS_KEY_ID')
ACCESS_SECRET_KEY = config('ACCESS_SECRET_KEY')
s3 = boto3.client('s3',aws_access_key_id = ACCESS_KEY_ID,aws_secret_access_key = ACCESS_SECRET_KEY)
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
             
            prescriptionList = Prescription.objects.all()
            obj = Prescription(uploaded_by=request.user, image=image)
            obj.save()

            flag = False
            flagItem = ""
            
            for i in range(len(prescriptionList) - 1):
                if(isSimilarImage(prescriptionList[i].image, obj.image)):
                    flag = True
                    flagItem = prescriptionList[i]
                    break
            
            # print(flagItem)
            if flag:
                # print("asuchi")
                obj.annotation = convertJson((str(obj.image).split("/"))[1],flagItem.annotation)
                obj.save()
            else:
                # print("else asila")
                predictPrescription(request, obj.id)

            users = list(User.objects.all())
            for user in users: 
                x = Approval(prescription = obj,checkedBy = user)
                x.save()


            return redirect('singleViewPres', prescription_id=obj.id)
    else:
        return redirect('login')

def viewPrescription(request):

    if request.user.is_authenticated:
        search = ""
        result =  Prescription.objects.all()
        prescriptions_containing_search = []
        if 'search' in request.POST:
            search = request.POST['search'].lower()
            for prescription in result:
                if search in (str(prescription.annotation).lower() + prescription.uploaded_by.username.lower()):
                    prescriptions_containing_search.append(prescription)
        else:
            prescriptions_containing_search = result
        data = {
            'prescriptions' : prescriptions_containing_search,
            'searched' : search
        }
        return render(request, 'pages/viewPrescription.html', context=data)
    else:
        return redirect('login')

digitised_prescriptionImage_dir ='DigitizedPrescriptionImage/'
digitised_prescriptionImagePdf_dir ='DigitizedPrescriptionImagePdf/'
digitised_prescriptionPdf_dir = 'DigitizedPrescriptionPdf/'

def visualizeAnnotation(request, prescription_id):

    if request.user.is_authenticated:

        prescription = Prescription.objects.get(id=prescription_id)
        annotations = prescription.annotation
        annotated_image, digitized_image,x = viewAnnotation(annotations, image_path = prescription.image.url)
        
        # create directories if do not exist
        if not os.path.exists(digitised_prescriptionImage_dir):
            os.makedirs(digitised_prescriptionImage_dir)

        if not os.path.exists(digitised_prescriptionImagePdf_dir):
            os.makedirs(digitised_prescriptionImagePdf_dir)

        if not os.path.exists(digitised_prescriptionPdf_dir):
            os.makedirs(digitised_prescriptionPdf_dir)

        #img2pdf Code
        url = prescription.image.url
        url = url.split('/')[-1]
        im = Image.fromarray(x)
        im.save(os.path.join(digitised_prescriptionImage_dir+str(url)))
        pdfdata = img2pdf.convert(digitised_prescriptionImage_dir+url)
        file = open(digitised_prescriptionImagePdf_dir + url.split('.')[0]+'.pdf','wb')
        file.write(pdfdata)
        file.close()

        prescription.digitzedImagePdf = digitised_prescriptionImagePdf_dir + url.split('.')[0]+'.pdf'
        prescription.save()

        #fpdf code

        img = cv2.imread(str(prescription.image))
        height, width = img.shape[0], img.shape[1]

        pdf = FPDF('P','mm',[width,height])
        pdf.add_page()
        for annotation in annotations[prescription.image.url+"/-1"]['regions']:
            height_of_box = annotation["shape_attributes"]["height"]
            width_of_box = annotation["shape_attributes"]["width"]
            fontScale = height_of_box / width_of_box
            if fontScale > 0.5:
                fontScale = 1.5
            else:
                fontScale = 1
            pdf.set_font("Arial", size = 64*fontScale)
            pdf.set_xy(annotation['shape_attributes']['x'],annotation['shape_attributes']['y']/1.33)
            pdf.cell(annotation['shape_attributes']['width'], annotation['shape_attributes']['height'], txt = annotation['region_attributes']['text'])            
        pdf.output(digitised_prescriptionPdf_dir + url.split('.')[0]+'.pdf')  


        prescription.digitzedPdf = digitised_prescriptionPdf_dir + url.split('.')[0]+'.pdf'
        prescription.save()

        ############################

        context = {
            'prescription': prescription,
            'annotated_image_uri': annotated_image,
            'digitised_image_uri': digitized_image,
            'digitised_image_uri_pdf' : prescription.digitzedImagePdf.url,
            'digitised_pdf_uri' : prescription.digitzedPdf.url
            # 'pdf_path' : os.path.join(digitised_prescriptionPdf_dir ,  url.split('.')[0]+'.pdf'),
            # 'pdf_name' : url.split('.')[0]+'.pdf'
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
            # print("Extracted Text =====> ", res)
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
        # print(PROTECTED_HEALTH_INFORMATION)
        # print(Medication)
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
        confidence = 0
        for r in annotation[url]['regions']:
            confidence += r['region_attributes']['confidence']
        
        if len(annotation[url]['regions']):
            confidence /= len(annotation[url]['regions'])

        context = {
            'prescription': Prescription.objects.get(id=prescription_id),
            'predicted':p,
            'overall_confidence': round(confidence,2)
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

        # print(response)
        preds = convert(response,img,img.split('/')[-1])
        # print(preds)
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

def deletePrescription(request, prescription_id):
    if request.user.is_authenticated:
        search = None
        prescription = Prescription.objects.get(id=prescription_id)
        if request.user == prescription.uploaded_by:
            prescription.delete()
        return redirect( "home")
    else:
        return redirect('login')


def viewApproval(request):

    if request.user.is_authenticated:
            result =  Approval.objects.filter(checkedBy = request.user)
            context = {
                'fetchedApprovals' : result,
          }
            return render(request, 'pages/viewApproval.html', context=context)
    else:
        return redirect('login')

def processApproval(request,prescription_id):

    if request.user.is_authenticated:
        prescription = Prescription.objects.get(id=prescription_id)
        annotations = prescription.annotation
        annotated_image, digitized_image,x = viewAnnotation(annotations, image_path = prescription.image.url)
        c = 0

        listAnnotations = []
        for annotation in annotations[prescription.image.url+"/-1"]['regions']:
            c+=1
            listAnnotations.append(annotation['region_attributes']['text'])
        
        context = {
            'annotated_image_uri': annotated_image,
            'digitised_image_uri': digitized_image,
            'noOfAnnotations' : c,
            'prescription_id' : prescription_id,
            'listAnnotations' : listAnnotations
        }
        
        return render(request, 'pages/approvalPage.html', context=context)
    else:
        return redirect('login')

# def updateApproval(request,prescription_id):
#     if request.user.is_authenticated:
#         prescription = Prescription.objects.get(id=prescription_id)
#         approval = Approval.objects.get(prescription = prescription,checkedBy = request.user)
        
#         approval.status = "Reviewed"

#         correctAnnotations = request.POST['correctAnnotations']
#         noOfAnnotations = request.POST['noOfAnnotations']

#         ratio = int(correctAnnotations) / int(noOfAnnotations)

#         print(ratio, "------>")

#         prescription.confidence = calculateConfidence(prescription.noChecked,prescription.confidence,ratio)

#         prescription.noChecked = prescription.noChecked + 1


#         approval.save()
#         prescription.save()

#         # result =  Approval.objects.filter(checkedBy = request.user)

#         # context = {
#         #         'fetchedApprovals' : result
#         #     }
#         # return render(request, 'pages/viewApproval.html', context=context)
#         return redirect('approvals')
#     else:
#         return redirect('login')



def updateApproval(request,prescription_id):
    if request.user.is_authenticated:
        prescription = Prescription.objects.get(id=prescription_id)
        approval = Approval.objects.get(prescription = prescription,checkedBy = request.user)

        correctAnnotations = request.POST['correctAnnotations']
        noOfAnnotations = request.POST['noOfAnnotations']
        ratio = int(correctAnnotations) / int(noOfAnnotations)

        if approval.status == "Reviewed":
            prescription.confidence = calculateConfidence(prescription.noChecked,prescription.confidence,ratio)
            
        else :
            approval.status = "Reviewed"
            prescription.confidence = calculateConfidence(prescription.noChecked,prescription.confidence,ratio)
            prescription.noChecked = prescription.noChecked + 1

        approval.save()
        prescription.save()

        return redirect('approvals')
    else:
        return redirect('login')

def dashboard(request):
    # if request.user.is_authenticated:
        return render(request, 'pages/dashboard.html')
    # else:
    #     return redirect('login')

def customerView(request):
    if request.user.is_authenticated:

        return render(request,'pages/uploadCustomer.html')
    else:
        return redirect('login')

def customerUploadForm(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            phoneNumber = request.POST['phoneNumber']
            image = request.FILES['prescription_image']
            obj = CustomerPrescription(uploaded_by=request.user, image=image, phoneNumber = int(phoneNumber))
            obj.save()

            predictCustomerPrescription(request, obj.id)

            prescription = CustomerPrescription.objects.get(id=obj.id)
            annotation = CustomerPrescription.objects.get(id=obj.id).annotation
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

            print(c, "----->")

            medicineList = c
            
            medicineImageUrl = []
            for medicine in medicineList:
                img_url, name = scrapeMedicineImage(medicine)
                medicineImageUrl.append([img_url, name])
            
            for image in medicineImageUrl:
                sendTextWhatsapp(phoneNumber, image[1], image[0])
            context = {
                "phoneNumber" : phoneNumber,
                "medicine_data": medicineImageUrl,

            }
            return render(request,'pages/sentToWhatsapp.html', context= context)
        else:
            return redirect('customerView')
    else:
        return redirect('login')


def predictCustomerPrescription(request, prescription_id):
    if request.user.is_authenticated:
        image_data = CustomerPrescription.objects.get(id=prescription_id).image
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

        preds = CustomerConvert(response,img,img.split('/')[-1])
        prescription = CustomerPrescription.objects.get(id=prescription_id)
        prescription.annotation= preds
        prescription.save()
    else:
        return redirect("login")