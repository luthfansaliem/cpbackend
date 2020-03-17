from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Company
from .models import EmployeeOwner
from .models import Position
from .models import CostType
from .models import Country
from .models import FreightCost
from .models import Region
from .models import TrackType
from .models import Unit
from .models import PortOFLoad
from .models import BTKI
from .models import PMD63
from .models import PMD110
from .models import Kurs
from .models import Holiday
from .models import Forwarder
from .models import Seller
from .models import Shipper
from .models import AuditTrail
from .models import MasterList
from .models import Shipment
from .models import Shipment_Detail

from .serializers import CompanySerializers
from .serializers import EmployeeOwnerSerializers
from .serializers import PositionSerializers
from .serializers import CostTypeSerializers
from .serializers import CountrySerializers
from .serializers import FreightCostSerializers
from .serializers import RegionSerializers
from .serializers import TrackTypeSerializers
from .serializers import UnitSerializers
from .serializers import PortOFLoadSerializers
from .serializers import BTKISerializers
from .serializers import PMD63Serializers
from .serializers import PMD110Serializers
from .serializers import KursSerializers
from .serializers import HolidaySerializers
from .serializers import ForwarderSerializers
from .serializers import SellerSerializers
from .serializers import ShipperSerializers
from .serializers import AuditTrailSerializers
from .serializers import MasterListSerializers
from .serializers import ShipmentSerializers
from .serializers import Shipment_DetailSerializers



from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.conf import settings
import os
from django.db import connection



class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def retrieve_company(request):
    if request.method == 'GET':
        products = Company.objects.all()
        serializer = CompanySerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Company"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_company(request, get_id):
    if request.method == 'GET':
        products = Company.objects.filter(company_id=get_id)
        serializer = CompanySerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Company"}, status=status.HTTP_400_BAD_REQUEST)
        
def create_company(request):
    if request.method == 'POST' and len(request.FILES) != 0:   
        insert = Company(
            company_name = request.POST['company_name'],
            company_address1=request.POST['company_address1'],
            company_address2=request.POST['company_address2'],
            company_phone=request.POST['company_phone'],
            company_fax=request.POST['company_fax'],
            company_email=request.POST['company_email'],
            company_npwp=request.POST['company_npwp'],
            company_apip=request.POST['company_apip'],
            company_nib=request.POST['company_nib'],
            company_type=request.POST['company_type'],
            company_AccountNo=request.POST['company_AccountNo'],
            company_npwpDoc=request.FILES['company_npwpDoc'],
            company_sppkpDoc=request.FILES['company_sppkpDoc'],
        )
        
        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Company',
            audittrail_transid= insert.company_id,
            audittrail_action= 'Create',
            audittrail_content= {
                "company_id": insert.company_id,
                "company_name": insert.company_name,
                "company_address1": insert.company_address1,
                "company_address2": insert.company_address2,
                "company_phone": insert.company_phone,
                "company_fax": insert.company_fax,
                "company_email": insert.company_email,
                "company_npwp": insert.company_npwp,
                "company_apip": insert.company_apip,
                "company_nib": insert.company_nib,
                "company_type": insert.company_type,
                "company_AccountNo": insert.company_AccountNo,
                "company_npwpDoc": insert.company_npwpDoc,
                "company_sppkpDoc": insert.company_sppkpDoc
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new Company has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new Company"}, status=status.HTTP_400_BAD_REQUEST)
                 
            

def update_company(request, update_id):
    ubah = Company.objects.get(company_id=update_id)
    if request.method == 'POST':
        if len(request.FILES) != 0:
            #buat delete gambar di folder
            npwp_path = str(ubah.company_npwpDoc)
            sppkp_path = str(ubah.company_sppkpDoc)

            #buat update data di db dan update gambar di folder
            ubah.company_name = request.POST['company_name']
            ubah.company_address1=request.POST['company_address1']
            ubah.company_address2=request.POST['company_address2']
            ubah.company_phone=request.POST['company_phone']
            ubah.company_fax=request.POST['company_fax']
            ubah.company_email=request.POST['company_email']
            ubah.company_npwp=request.POST['company_npwp']
            ubah.company_apip=request.POST['company_apip']
            ubah.company_nib=request.POST['company_nib']
            ubah.company_type = request.POST['company_type']
            ubah.company_AccountNo = request.POST['company_AccountNo']
            ubah.company_npwpDoc = request.FILES['company_npwpDoc']
            ubah.company_sppkpDoc = request.FILES['company_sppkpDoc']

            if npwp_path !='' and sppkp_path !='':
                try:
                    os.unlink(npwp_path)
                    os.unlink(sppkp_path)
                except(Exception)as e:
                    print('Exception',e)
                    pass

            if ubah:
                try:
                    ubah.save()
                except(Exception)as e:
                    print('Exception',e)
                    pass

            insertAuditTrail = AuditTrail(
                audittrail_transname = 'Company',
                audittrail_transid= ubah.company_id,
                audittrail_action= 'Update',
                audittrail_content= {
                    "company_id": ubah.company_id,
                    "company_name": ubah.company_name,
                    "company_address1": ubah.company_address1,
                    "company_address2": ubah.company_address2,
                    "company_phone": ubah.company_phone,
                    "company_fax": ubah.company_fax,
                    "company_email": ubah.company_email,
                    "company_npwp": ubah.company_npwp,
                    "company_apip": ubah.company_apip,
                    "company_nib": ubah.company_nib,
                    "company_type": ubah.company_type,
                    "company_AccountNo": ubah.company_AccountNo,
                    "company_npwpDoc": ubah.company_npwpDoc,
                    "company_sppkpDoc": ubah.company_sppkpDoc
                },
                audittrail_createdby='admin',
                audittrail_createdtime=datetime.now(),
                )

            if insertAuditTrail:
                try:
                    insertAuditTrail.save()
                    return JSONResponse({"status": True, "message": "Company has been updated"}, status=status.HTTP_201_CREATED)
                except(Exception)as e:
                    print('Exception',e)
                    pass        
                return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
            return JSONResponse({"status": False, "message": "failed to update Company"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            ubah.company_name = request.POST['company_name']
            ubah.company_address1=request.POST['company_address1']
            ubah.company_address2=request.POST['company_address2']
            ubah.company_phone=request.POST['company_phone']
            ubah.company_fax=request.POST['company_fax']
            ubah.company_email=request.POST['company_email']
            ubah.company_npwp=request.POST['company_npwp']
            ubah.company_apip=request.POST['company_apip']
            ubah.company_nib=request.POST['company_nib']
            ubah.company_type = request.POST['company_type']
            ubah.company_AccountNo = request.POST['company_AccountNo']

            if ubah:
                try:
                    ubah.save()
                except(Exception)as e:
                    print('Exception',e)
                    pass

            insertAuditTrail = AuditTrail(
                audittrail_transname = 'Company',
                audittrail_transid= ubah.company_id,
                audittrail_action= 'Update',
                audittrail_content= {
                    "company_id": ubah.company_id,
                    "company_name": ubah.company_name,
                    "company_address1": ubah.company_address1,
                    "company_address2": ubah.company_address2,
                    "company_phone": ubah.company_phone,
                    "company_fax": ubah.company_fax,
                    "company_email": ubah.company_email,
                    "company_npwp": ubah.company_npwp,
                    "company_apip": ubah.company_apip,
                    "company_nib": ubah.company_nib,
                    "company_type": ubah.company_type,
                    "company_AccountNo": ubah.company_AccountNo,
                    "company_npwpDoc": ubah.company_npwpDoc,
                    "company_sppkpDoc": ubah.company_sppkpDoc
                },
                audittrail_createdby='admin',
                audittrail_createdtime=datetime.now(),
                )

            if insertAuditTrail:
                try:
                    insertAuditTrail.save()
                    return JSONResponse({"status": True, "message": "Company has been updated"}, status=status.HTTP_201_CREATED)
                except(Exception)as e:
                    print('Exception',e)
                    pass        
                return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
            return JSONResponse({"status": False, "message": "failed to update Company"}, status=status.HTTP_400_BAD_REQUEST)

def delete_company(request, delete_id):
    if request.method == 'GET':
        hapus = Company.objects.get(company_id=delete_id)

        npwp_path = str(hapus.company_npwpDoc)
        sppkp_path = str(hapus.company_sppkpDoc)

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Company',
            audittrail_transid= hapus.company_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "company_id": hapus.company_id,
                "company_name": hapus.company_name,
                "company_address1": hapus.company_address1,
                "company_address2": hapus.company_address2,
                "company_phone": hapus.company_phone,
                "company_fax": hapus.company_fax,
                "company_email": hapus.company_email,
                "company_npwp": hapus.company_npwp,
                "company_apip": hapus.company_apip,
                "company_nib": hapus.company_nib,
                "company_type": hapus.company_type,
                "company_AccountNo": hapus.company_AccountNo,
                "company_npwpDoc": hapus.company_npwpDoc,
                "company_sppkpDoc": hapus.company_sppkpDoc
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if npwp_path !='' and sppkp_path !='':
            try:
                os.unlink(npwp_path)
                os.unlink(sppkp_path)
            except(Exception)as e:
                print('Exception',e)
                pass
        
        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "Company has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete Company"}, status=status.HTTP_400_BAD_REQUEST)

##eo
def retrieve_eo(request):
    if request.method == 'GET':
        products = EmployeeOwner.objects.all()
        serializer = EmployeeOwnerSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data EmployeeOwner"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_eo(request, get_id):
    if request.method == 'GET':
        products = EmployeeOwner.objects.filter(eo_id=get_id)
        serializer = EmployeeOwnerSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data EmployeeOwner"}, status=status.HTTP_400_BAD_REQUEST)

def create_eo(request):
    if request.method == 'POST' and len(request.FILES) != 0:
        insert = EmployeeOwner(
            eo_name = request.POST['eo_name'],
            eo_address1=request.POST['eo_address1'],
            eo_address2=request.POST['eo_address2'],
            eo_phone=request.POST['eo_phone'],
            eo_nik=request.POST['eo_nik'],
            eo_email=request.POST['eo_email'],
            eo_npwp=request.POST['eo_npwp'],
            eo_position_id=request.POST['eo_position_id'],
            eo_company_id=request.POST['eo_company_id'],
            eo_nik_img=request.FILES['eo_nik_img'],
            eo_npwp_img=request.FILES['eo_npwp_img'],
            eo_oth_img=request.FILES['eo_oth_img'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'EmployeeOwner',
            audittrail_transid= insert.eo_id,
            audittrail_action= 'Create',
            audittrail_content= {
                    "eo_id": insert.eo_id,
                    "eo_name": insert.eo_name,
                    "eo_address1": insert.eo_address1,
                    "eo_address2": insert.eo_address2,
                    "eo_phone": insert.eo_phone,
                    "eo_nik": insert.eo_nik,
                    "eo_email": insert.eo_email,
                    "eo_npwp": insert.eo_npwp,
                    "eo_position_id": insert.eo_position_id,
                    "eo_company_id": insert.eo_company_id,
                    "eo_nik_img": insert.eo_nik_img,
                    "eo_npwp_img": insert.eo_npwp_img,
                    "eo_oth_img": insert.eo_oth_img
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new EmployeeOwner has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new EmployeeOwner"}, status=status.HTTP_400_BAD_REQUEST)

def update_eo(request, update_id):
    ubah = EmployeeOwner.objects.get(eo_id=update_id)
    if request.method == 'POST':
        if len(request.FILES) != 0:
            #buat delete gambar di folder
            nik_path = str(ubah.eo_nik_img)
            npwp_path = str(ubah.eo_npwp_img)
            oth_path = str(ubah.eo_oth_img)

            #buat update data di db dan update gambar di folder
            ubah.eo_name = request.POST['eo_name']
            ubah.eo_address1=request.POST['eo_address1']
            ubah.eo_address2=request.POST['eo_address2']
            ubah.eo_phone=request.POST['eo_phone']
            ubah.eo_nik=request.POST['eo_nik']
            ubah.eo_email=request.POST['eo_email']
            ubah.eo_npwp=request.POST['eo_npwp']
            ubah.eo_position_id=request.POST['eo_position_id']
            ubah.eo_company_id=request.POST['eo_company_id']
            ubah.eo_nik_img = request.FILES['eo_nik_img']
            ubah.eo_npwp_img = request.FILES['eo_npwp_img']
            ubah.eo_oth_img = request.FILES['eo_oth_img']

            if nik_path != '' and npwp_path !='' and oth_path !='':
                try:
                    os.unlink(nik_path)
                    os.unlink(npwp_path)
                    os.unlink(oth_path)
                except(Exception)as e:
                    print('Exception',e)
                    pass

            if ubah:
                try:
                    ubah.save()
                except(Exception)as e:
                    print('Exception',e)
                    pass

            insertAuditTrail = AuditTrail(
                audittrail_transname = 'EmployeeOwner',
                audittrail_transid= ubah.eo_id,
                audittrail_action= 'Update',
                audittrail_content= {
                    "eo_id": ubah.eo_id,
                    "eo_name": ubah.eo_name,
                    "eo_address1": ubah.eo_address1,
                    "eo_address2": ubah.eo_address2,
                    "eo_phone": ubah.eo_phone,
                    "eo_nik": ubah.eo_nik,
                    "eo_email": ubah.eo_email,
                    "eo_npwp": ubah.eo_npwp,
                    "eo_position_id": ubah.eo_position_id,
                    "eo_company_id": ubah.eo_company_id,
                    "eo_nik_img": ubah.eo_nik_img,
                    "eo_npwp_img": ubah.eo_npwp_img,
                    "eo_oth_img": ubah.eo_oth_img
                },
                audittrail_createdby='admin',
                audittrail_createdtime=datetime.now(),
                )

            if insertAuditTrail:
                try:
                    insertAuditTrail.save()
                    return JSONResponse({"status": True, "message": "EmployeeOwner has been updated"}, status=status.HTTP_201_CREATED)
                except(Exception)as e:
                    print('Exception',e)
                    pass        
                return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
            return JSONResponse({"status": False, "message": "failed to update EmployeeOwner"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            ubah.eo_name = request.POST['eo_name']
            ubah.eo_address1=request.POST['eo_address1']
            ubah.eo_address2=request.POST['eo_address2']
            ubah.eo_phone=request.POST['eo_phone']
            ubah.eo_nik=request.POST['eo_nik']
            ubah.eo_email=request.POST['eo_email']
            ubah.eo_npwp=request.POST['eo_npwp']
            ubah.eo_position_id=request.POST['eo_position_id']
            ubah.eo_company_id=request.POST['eo_company_id']

            if ubah:
                try:
                    ubah.save()
                except(Exception)as e:
                    print('Exception',e)
                    pass

            insertAuditTrail = AuditTrail(
                audittrail_transname = 'EmployeeOwner',
                audittrail_transid= ubah.eo_id,
                audittrail_action= 'Update',
                audittrail_content= {
                    "eo_id": ubah.eo_id,
                    "eo_name": ubah.eo_name,
                    "eo_address1": ubah.eo_address1,
                    "eo_address2": ubah.eo_address2,
                    "eo_phone": ubah.eo_phone,
                    "eo_nik": ubah.eo_nik,
                    "eo_email": ubah.eo_email,
                    "eo_npwp": ubah.eo_npwp,
                    "eo_position_id": ubah.eo_position_id,
                    "eo_company_id": ubah.eo_company_id,
                    "eo_nik_img": ubah.eo_nik_img,
                    "eo_npwp_img": ubah.eo_npwp_img,
                    "eo_oth_img": ubah.eo_oth_img
                },
                audittrail_createdby='admin',
                audittrail_createdtime=datetime.now(),
                )

            if insertAuditTrail:
                try:
                    insertAuditTrail.save()
                    return JSONResponse({"status": True, "message": "EmployeeOwner has been updated"}, status=status.HTTP_201_CREATED)
                except(Exception)as e:
                    print('Exception',e)
                    pass        
                return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
            return JSONResponse({"status": False, "message": "failed to update EmployeeOwner"}, status=status.HTTP_400_BAD_REQUEST)
    

def delete_eo(request, delete_id):
    if request.method == 'GET':
        hapus = EmployeeOwner.objects.filter(eo_id=delete_id)
        nik_path = str(hapus.eo_nik_img)
        npwp_path = str(hapus.eo_npwp_img)
        oth_path = str(hapus.eo_oth_img)

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'EmployeeOwner',
            audittrail_transid= hapus.eo_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "eo_id": hapus.eo_id,
                "eo_name": hapus.eo_name,
                "eo_address1": hapus.eo_address1,
                "eo_address2": hapus.eo_address2,
                "eo_phone": hapus.eo_phone,
                "eo_nik": hapus.eo_nik,
                "eo_email": hapus.eo_email,
                "eo_npwp": hapus.eo_npwp,
                "eo_position_id": hapus.eo_position_id,
                "eo_company_id": hapus.eo_company_id,
                "eo_nik_img": hapus.eo_nik_img,
                "eo_npwp_img": hapus.eo_npwp_img,
                "eo_oth_img": hapus.eo_oth_img
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if nik_path !='' and npwp_path !='' and oth_path !='':
            try:
                os.unlink(nik_path)
                os.unlink(npwp_path)
                os.unlink(oth_path)
            except(Exception)as e:
                print('Exception',e)
                pass
        
        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "EmployeeOwner has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete EmployeeOwner"}, status=status.HTTP_400_BAD_REQUEST)
##position
def retrieve_position(request):
    if request.method == 'GET':
        products = Position.objects.all()
        serializer = PositionSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Position"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_position(request, get_id):
    if request.method == 'GET':
        products = Position.objects.filter(position_id=get_id)
        serializer = PositionSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Position"}, status=status.HTTP_400_BAD_REQUEST)

def create_position(request):
    if request.method == 'POST':
        insert = Position(
            position_name=request.POST['position_name'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Position',
            audittrail_transid= insert.position_id,
            audittrail_action= 'Create',
            audittrail_content= {
                    "position_id": insert.position_id,
                    "position_name": insert.position_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new Position has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new Position"}, status=status.HTTP_400_BAD_REQUEST)

def update_position(request, update_id):
    if request.method == 'POST':
        ubah = Position.objects.get(position_id=update_id)
        ubah.position_name = request.POST['position_name']
        
        if ubah:
            try:
                ubah.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Position',
            audittrail_transid= ubah.position_id,
            audittrail_action= 'Update',
            audittrail_content= {
                "position_id": ubah.position_id,
                "position_name": ubah.position_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )
        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "Position has been updated"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to update Position"}, status=status.HTTP_400_BAD_REQUEST)

def delete_position(request, delete_id):
    if request.method == 'GET':
        hapus = Position.objects.filter(position_id=delete_id)
        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Position',
            audittrail_transid= hapus.position_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "position_id": hapus.position_id,
                "position_name": hapus.position_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "Position has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete Position"}, status=status.HTTP_400_BAD_REQUEST)

##costtype
def retrieve_costtype(request):
    if request.method == 'GET':
        products = CostType.objects.all()
        serializer = CostTypeSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data CostType"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_costtype(request, get_id):
    if request.method == 'GET':
        products = CostType.objects.filter(costtype_id=get_id)
        serializer = CostTypeSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data CostType"}, status=status.HTTP_400_BAD_REQUEST)

def create_costtype(request):
    if request.method == 'POST':
        insert = CostType(
            costtype_code=request.POST['costtype_code'],
            costtype_name=request.POST['costtype_name'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'CostType',
            audittrail_transid= insert.costtype_id,
            audittrail_action= 'Create',
            audittrail_content= {
                    "costtype_id": insert.costtype_id,
                    "costtype_code": insert.costtype_code,
                    "costtype_name": insert.costtype_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new CostType has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new CostType"}, status=status.HTTP_400_BAD_REQUEST)

def update_costtype(request, update_id):
    if request.method == 'POST':
        ubah = CostType.objects.get(costtype_id=update_id)
        ubah.costtype_code = request.POST['costtype_code']
        ubah.costtype_name = request.POST['costtype_name']

        if ubah:
            try:
                ubah.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'CostType',
            audittrail_transid= ubah.costtype_id,
            audittrail_action= 'Update',
            audittrail_content= {
                "costtype_id": ubah.costtype_id,
                "costtype_code": ubah.costtype_code,
                "costtype_name": ubah.costtype_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )
        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "CostType has been updated"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to update CostType"}, status=status.HTTP_400_BAD_REQUEST)

def delete_costtype(request, delete_id):
    if request.method == 'GET':
        hapus = CostType.objects.filter(costtype_id=delete_id)

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'CostType',
            audittrail_transid= hapus.costtype_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "costtype_id": hapus.costtype_id,
                "costtype_code": hapus.costtype_code,
                "costtype_name": hapus.costtype_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "CostType has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete CostType"}, status=status.HTTP_400_BAD_REQUEST)

##country
def retrieve_country(request):
    if request.method == 'GET':
        products = Country.objects.all()
        serializer = CountrySerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Country"}, status=status.HTTP_400_BAD_REQUEST)


def retrievebyId_country(request, get_id):
    if request.method == 'GET':
        products = Country.objects.filter(country_id=get_id)
        serializer = CountrySerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Country"}, status=status.HTTP_400_BAD_REQUEST)

def create_country(request):
    if request.method == 'POST':
        insert = Country(
            country_code=request.POST['country_code'],
            country_codecode=request.POST['country_codecode'],
            country_name=request.POST['country_name'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Country',
            audittrail_transid= insert.country_id,
            audittrail_action= 'Create',
            audittrail_content= {
                    "country_id": insert.country_id,
                    "country_code": insert.country_code,
                    "country_codecode": insert.country_codecode,
                    "country_name": insert.country_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new Country has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new Country"}, status=status.HTTP_400_BAD_REQUEST)


def update_country(request, update_id):
    if request.method == 'POST':
        ubah = Country.objects.get(country_id=update_id)
        ubah.country_code=request.POST['country_code']
        ubah.country_codecode=request.POST['country_codecode']
        ubah.country_name=request.POST['country_name']

        if ubah:
            try:
                ubah.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Country',
            audittrail_transid= ubah.country_id,
            audittrail_action= 'Update',
            audittrail_content= {
                "country_id": insert.country_id,
                "country_code": insert.country_code,
                "country_codecode": insert.country_codecode,
                "country_name": insert.country_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )
        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "Country has been updated"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to update Country"}, status=status.HTTP_400_BAD_REQUEST)


def delete_country(request, delete_id):
    if request.method == 'GET':
        hapus = Country.objects.filter(country_id=delete_id)

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Country',
            audittrail_transid= hapus.country_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "country_id": hapus.country_id,
                "country_code": hapus.country_code,
                "country_codecode": hapus.country_codecode,
                "country_name": hapus.country_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "Country has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete Country"}, status=status.HTTP_400_BAD_REQUEST)

##region
def retrieve_region(request):
    if request.method == 'GET':
        products = Region.objects.all()
        serializer = RegionSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Region"}, status=status.HTTP_400_BAD_REQUEST)


def retrievebyId_region(request, get_id):
    if request.method == 'GET':
        products = Region.objects.filter(region_id=get_id)
        serializer = RegionSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Region"}, status=status.HTTP_400_BAD_REQUEST)


def create_region(request):
    if request.method == 'POST':
        insert = Region(
            region_code=request.POST['region_code'],
            region_name=request.POST['region_name'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Region',
            audittrail_transid= insert.region_id,
            audittrail_action= 'Create',
            audittrail_content= {
                    "region_id": insert.region_id,
                    "region_code": insert.region_code,
                    "region_name": insert.region_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new Region has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new Region"}, status=status.HTTP_400_BAD_REQUEST)

def update_region(request, update_id):
    if request.method == 'POST':
        ubah = Region.objects.get(region_id=update_id)
        ubah.region_code=request.POST['region_code']
        ubah.region_name=request.POST['region_name']
        if ubah:
            try:
                ubah.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Region',
            audittrail_transid= ubah.region_id,
            audittrail_action= 'Update',
            audittrail_content= {
                "region_id": ubah.region_id,
                "region_code": ubah.region_code,
                "region_name": ubah.region_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )
        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "Region has been updated"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to update Region"}, status=status.HTTP_400_BAD_REQUEST)

def delete_region(request, delete_id):
    if request.method == 'GET':
        hapus = Region.objects.filter(region_id=delete_id)
        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Region',
            audittrail_transid= hapus.region_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "region_id": hapus.region_id,
                "region_code": hapus.region_code,
                "region_name": hapus.region_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "Region has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete Region"}, status=status.HTTP_400_BAD_REQUEST)

##tracktype
def retrieve_tracktype(request):
    if request.method == 'GET':
        products = TrackType.objects.all()
        serializer = TrackTypeSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data TrackType"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_tracktype(request, get_id):
    if request.method == 'GET':
        products = TrackType.objects.filter(tracktype_id=get_id)
        serializer = TrackTypeSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data TrackType"}, status=status.HTTP_400_BAD_REQUEST)

def create_tracktype(request):
    if request.method == 'POST':
        insert = TrackType(
            tracktype_code=request.POST['tracktype_code'],
            tracktype_name=request.POST['tracktype_name'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'TrackType',
            audittrail_transid= insert.tracktype_id,
            audittrail_action= 'Create',
            audittrail_content= {
                    "tracktype_id": insert.tracktype_id,
                    "tracktype_code": insert.tracktype_code,
                    "tracktype_name": insert.tracktype_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new TrackType has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new TrackType"}, status=status.HTTP_400_BAD_REQUEST)


def update_tracktype(request, update_id):
    if request.method == 'POST':
        ubah = TrackType.objects.get(tracktype_id=update_id)
        ubah.tracktype_code=request.POST['tracktype_code']
        ubah.tracktype_name=request.POST['tracktype_name']
        if ubah:
            try:
                ubah.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'TrackType',
            audittrail_transid= ubah.tracktype_id,
            audittrail_action= 'Update',
            audittrail_content= {
                "tracktype_id": ubah.tracktype_id,
                "tracktype_code": ubah.tracktype_code,
                "tracktype_name": ubah.tracktype_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )
        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "TrackType has been updated"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to update TrackType"}, status=status.HTTP_400_BAD_REQUEST)


def delete_tracktype(request, delete_id):
    if request.method == 'GET':
        hapus = TrackType.objects.filter(tracktype_id=delete_id)
        insertAuditTrail = AuditTrail(
            audittrail_transname = 'TrackType',
            audittrail_transid= hapus.tracktype_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "tracktype_id": hapus.tracktype_id,
                "tracktype_code": hapus.tracktype_code,
                "tracktype_name": hapus.tracktype_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "TrackType has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete TrackType"}, status=status.HTTP_400_BAD_REQUEST)

##freightcost
def retrieve_freightcost(request):
    if request.method == 'GET':
        products = FreightCost.objects.all()
        serializer = FreightCostSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data FreightCost"}, status=status.HTTP_400_BAD_REQUEST)


def retrievebyId_freightcost(request, get_id):
    if request.method == 'GET':
        products = FreightCost.objects.filter(freightcost_id=get_id)
        serializer = FreightCostSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data FreightCost"}, status=status.HTTP_400_BAD_REQUEST)

def create_freightcost(request):
    if request.method == 'POST':
        insert = FreightCost(
            region_id=request.POST['region_id'],
            costtype_id=request.POST['costtype_id'],
            tracktype_id=request.POST['tracktype_id'],
            amount=request.POST['amount'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'FreightCost',
            audittrail_transid= insert.freightcost_id,
            audittrail_action= 'Create',
            audittrail_content= {
                    "freightcost_id": insert.freightcost_id,
                    "region_id": insert.region_id,
                    "costtype_id": insert.costtype_id,
                    "tracktype_id": insert.tracktype_id,
                    "amount": insert.amount,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new FreightCost has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new FreightCost"}, status=status.HTTP_400_BAD_REQUEST)

def update_freightcost(request, update_id):
    if request.method == 'POST':
        ubah = FreightCost.objects.get(freightcost_id=update_id)
        ubah.region_id=request.POST['region_id']
        ubah.costtype_id=request.POST['costtype_id']
        ubah.tracktype_id=request.POST['tracktype_id']
        ubah.amount=request.POST['amount']

        if ubah:
            try:
                ubah.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'FreightCost',
            audittrail_transid= ubah.freightcost_id,
            audittrail_action= 'Update',
            audittrail_content= {
                "freightcost_id": ubah.freightcost_id,
                "region_id": ubah.region_id,
                "costtype_id": ubah.costtype_id,
                "tracktype_id": ubah.tracktype_id,
                "amount": ubah.amount,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )
        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "FreightCost has been updated"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to update FreightCost"}, status=status.HTTP_400_BAD_REQUEST)

def delete_freightcost(request, delete_id):
    if request.method == 'GET':
        hapus = FreightCost.objects.filter(freightcost_id=delete_id)
        insertAuditTrail = AuditTrail(
            audittrail_transname = 'FreightCost',
            audittrail_transid= hapus.freightcost_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "freightcost_id": hapus.freightcost_id,
                "region_id": hapus.region_id,
                "costtype_id": hapus.costtype_id,
                "tracktype_id": hapus.tracktype_id,
                "amount": hapus.amount,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "FreightCost has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete FreightCost"}, status=status.HTTP_400_BAD_REQUEST)

##unit
def retrieve_unit(request):
    if request.method == 'GET':
        products = Unit.objects.all()
        serializer = UnitSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Unit"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_unit(request, get_id):
    if request.method == 'GET':
        products = Unit.objects.filter(unit_id=get_id)
        serializer = UnitSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Unit"}, status=status.HTTP_400_BAD_REQUEST)

def create_unit(request):
    if request.method == 'POST':
        insert = Unit(
            unit_code=request.POST['unit_code'],
            unit_name=request.POST['unit_name'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Unit',
            audittrail_transid= insert.unit_id,
            audittrail_action= 'Create',
            audittrail_content= {
                    "unit_id": insert.unit_id,
                    "unit_code": insert.unit_code,
                    "unit_name": insert.unit_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new Unit has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new Unit"}, status=status.HTTP_400_BAD_REQUEST)


def update_unit(request, update_id):
    if request.method == 'POST':
        ubah = Unit.objects.get(unit_id=update_id)
        ubah.unit_code=request.POST['unit_code']
        ubah.unit_name=request.POST['unit_name']
        if ubah:
            try:
                ubah.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Unit',
            audittrail_transid= ubah.unit_id,
            audittrail_action= 'Update',
            audittrail_content= {
                "unit_id": ubah.unit_id,
                "unit_code": ubah.unit_code,
                "unit_name": ubah.unit_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )
        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "Unit has been updated"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to update Unit"}, status=status.HTTP_400_BAD_REQUEST)


def delete_unit(request, delete_id):
    if request.method == 'GET':
        hapus = Unit.objects.filter(unit_id=delete_id)
        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Unit',
            audittrail_transid= hapus.unit_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "unit_id": hapus.unit_id,
                "unit_code": hapus.unit_code,
                "unit_name": hapus.unit_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "Unit has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete Unit"}, status=status.HTTP_400_BAD_REQUEST)

##portofload
def retrieve_portofload(request):
    if request.method == 'GET':
        products = PortOFLoad.objects.all()
        serializer = PortOFLoadSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data PortOFLoad"}, status=status.HTTP_400_BAD_REQUEST)


def retrievebyId_portofload(request, get_id):
    if request.method == 'GET':
        products = PortOFLoad.objects.filter(portofload_id=get_id)
        serializer = PortOFLoadSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data PortOFLoad"}, status=status.HTTP_400_BAD_REQUEST)

def create_portofload(request):
    if request.method == 'POST':
        insert = PortOFLoad(
            portofload_code=request.POST['portofload_code'],
            portofload_name=request.POST['portofload_name'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'PortOFLoad',
            audittrail_transid= insert.portofload_id,
            audittrail_action= 'Create',
            audittrail_content= {
                    "portofload_id": insert.portofload_id,
                    "portofload_code": insert.portofload_code,
                    "portofload_name": insert.portofload_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new PortOFLoad has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new PortOFLoad"}, status=status.HTTP_400_BAD_REQUEST)

def update_portofload(request, update_id):
    if request.method == 'POST':
        ubah = PortOFLoad.objects.get(portofload_id=update_id)
        ubah.portofload_code=request.POST['portofload_code']
        ubah.portofload_name=request.POST['portofload_name']

        if ubah:
            try:
                ubah.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'PortOFLoad',
            audittrail_transid= ubah.portofload_id,
            audittrail_action= 'Update',
            audittrail_content= {
                "portofload_id": ubah.portofload_id,
                "portofload_code": ubah.portofload_code,
                "portofload_name": ubah.portofload_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )
        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "PortOFLoad has been updated"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to update PortOFLoad"}, status=status.HTTP_400_BAD_REQUEST)

def delete_portofload(request, delete_id):
    if request.method == 'GET':
        hapus = PortOFLoad.objects.filter(portofload_id=delete_id)
        insertAuditTrail = AuditTrail(
            audittrail_transname = 'PortOFLoad',
            audittrail_transid= hapus.portofload_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "portofload_id": hapus.portofload_id,
                "portofload_code": hapus.portofload_code,
                "portofload_name": hapus.portofload_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "PortOFLoad has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete PortOFLoad"}, status=status.HTTP_400_BAD_REQUEST)

##btki
def retrieve_btki(request):
    if request.method == 'GET':
        products = BTKI.objects.all()
        serializer = BTKISerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data BTKI"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_btki(request, get_id):
    if request.method == 'GET':
        products = BTKI.objects.filter(btki_id=get_id)
        serializer = BTKISerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data BTKI"}, status=status.HTTP_400_BAD_REQUEST)

def create_btki(request):
    if request.method == 'POST':
        insert = BTKI(
            btki_no=request.POST['btki_no'],
            btki_hs_code=request.POST['btki_hs_code'],
            btki_uraian_barang=request.POST['btki_uraian_barang'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'BTKI',
            audittrail_transid= insert.btki_id,
            audittrail_action= 'Create',
            audittrail_content= {
                    "btki_id": insert.btki_id,
                    "btki_no": insert.btki_no,
                    "btki_hs_code": insert.btki_hs_code,
                    "btki_uraian_barang": insert.btki_uraian_barang,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new BTKI has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new BTKI"}, status=status.HTTP_400_BAD_REQUEST)

def update_btki(request, update_id):
    if request.method == 'POST':
        ubah = BTKI.objects.get(btki_id=update_id)
        ubah.btki_no=request.POST['btki_no']
        ubah.btki_hs_code=request.POST['btki_hs_code']
        ubah.btki_uraian_barang=request.POST['btki_uraian_barang']

        if ubah:
            try:
                ubah.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'BTKI',
            audittrail_transid= ubah.btki_id,
            audittrail_action= 'Update',
            audittrail_content= {
                "btki_id": ubah.btki_id,
                "btki_no": ubah.btki_no,
                "btki_hs_code": ubah.btki_hs_code,
                "btki_uraian_barang": ubah.btki_uraian_barang,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )
        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "BTKI has been updated"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to update BTKI"}, status=status.HTTP_400_BAD_REQUEST)

def delete_btki(request, delete_id):
    if request.method == 'GET':
        hapus = BTKI.objects.filter(btki_id=delete_id)
        insertAuditTrail = AuditTrail(
            audittrail_transname = 'BTKI',
            audittrail_transid= hapus.btki_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "btki_id": hapus.btki_id,
                "btki_no": hapus.btki_no,
                "btki_hs_code": hapus.btki_hs_code,
                "btki_uraian_barang": hapus.btki_uraian_barang,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "BTKI has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete BTKI"}, status=status.HTTP_400_BAD_REQUEST)

##pmd63
def retrieve_pmd63(request):
    if request.method == 'GET':
        products = PMD63.objects.all()
        serializer = PMD63Serializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data PMD63"}, status=status.HTTP_400_BAD_REQUEST)


def retrievebyId_pmd63(request, get_id):
    if request.method == 'GET':
        products = PMD63.objects.filter(pmd63_id=get_id)
        serializer = PMD63Serializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data PMD63"}, status=status.HTTP_400_BAD_REQUEST)

def create_pmd63(request):
    if request.method == 'POST':
        insert = PMD63(
            pmd63_peraturan=request.POST['pmd63_peraturan'],
            pmd63_no=request.POST['pmd63_no'],
            pmd63_hs_code=request.POST['pmd63_hs_code'],
            pmd63_deskripti=request.POST['pmd63_deskripti'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'PMD63',
            audittrail_transid= insert.pmd63_id,
            audittrail_action= 'Create',
            audittrail_content= {
                    "pmd63_id": insert.pmd63_id,
                    "pmd63_peraturan": insert.pmd63_peraturan,
                    "pmd63_no": insert.pmd63_no,
                    "pmd63_hs_code": insert.pmd63_hs_code,
                    "pmd63_deskripti": insert.pmd63_deskripti,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new PMD63 has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new PMD63"}, status=status.HTTP_400_BAD_REQUEST)

def update_pmd63(request, update_id):
    if request.method == 'POST':
        ubah = PMD63.objects.get(pmd63_id=update_id)
        ubah.pmd63_peraturan=request.POST['pmd63_peraturan']
        ubah.pmd63_no=request.POST['pmd63_no']
        ubah.pmd63_hs_code=request.POST['pmd63_hs_code']
        ubah.pmd63_deskripti=request.POST['pmd63_deskripti']

        if ubah:
            try:
                ubah.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'PMD63',
            audittrail_transid= ubah.pmd63_id,
            audittrail_action= 'Update',
            audittrail_content= {
                "pmd63_id": ubah.pmd63_id,
                "pmd63_peraturan": ubah.pmd63_peraturan,
                "pmd63_no": ubah.pmd63_no,
                "pmd63_hs_code": ubah.pmd63_hs_code,
                "pmd63_deskripti": ubah.pmd63_deskripti,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )
        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "PMD63 has been updated"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to update PMD63"}, status=status.HTTP_400_BAD_REQUEST)

def delete_pmd63(request, delete_id):
    if request.method == 'GET':
        hapus = PMD63.objects.filter(pmd63_id=delete_id)
        insertAuditTrail = AuditTrail(
            audittrail_transname = 'PMD63',
            audittrail_transid= hapus.pmd63_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "pmd63_id": hapus.pmd63_id,
                "pmd63_peraturan": hapus.pmd63_peraturan,
                "pmd63_no": hapus.pmd63_no,
                "pmd63_hs_code": hapus.pmd63_hs_code,
                "pmd63_deskripti": hapus.pmd63_deskripti,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "PMD63 has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete PMD63"}, status=status.HTTP_400_BAD_REQUEST)

##pmd110
def retrieve_pmd110(request):
    if request.method == 'GET':
        products = PMD110.objects.all()
        serializer = PMD110Serializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data PMD110"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_pmd110(request, get_id):
    if request.method == 'GET':
        products = PMD110.objects.filter(pmd110_id=get_id)
        serializer = PMD110Serializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data PMD110"}, status=status.HTTP_400_BAD_REQUEST)

def create_pmd110(request):
    if request.method == 'POST':
        insert = PMD110(
            pmd110_peraturan=request.POST['pmd110_peraturan'],
            pmd110_kategori=request.POST['pmd110_kategori'],
            pmd110_no=request.POST['pmd110_no'],
            pmd110_hs_code=request.POST['pmd110_hs_code'],
            pmd110_deskripti=request.POST['pmd110_deskripti'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'PMD110',
            audittrail_transid= insert.pmd110_id,
            audittrail_action= 'Create',
            audittrail_content= {
                    "pmd110_id": insert.pmd110_id,
                    "pmd110_peraturan": insert.pmd110_peraturan,
                    "pmd110_kategori": insert.pmd110_kategori,
                    "pmd110_no": insert.pmd110_no,
                    "pmd110_hs_code": insert.pmd110_hs_code,
                    "pmd110_deskripti": insert.pmd110_deskripti,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new PMD110 has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new PMD110"}, status=status.HTTP_400_BAD_REQUEST)

def update_pmd110(request, update_id):
    if request.method == 'POST':
        ubah = PMD110.objects.get(pmd110_id=update_id)
        ubah.pmd110_peraturan=request.POST['pmd110_peraturan']
        ubah.pmd110_kategori=request.POST['pmd110_kategori']
        ubah.pmd110_no=request.POST['pmd110_no']
        ubah.pmd110_hs_code=request.POST['pmd110_hs_code']
        ubah.pmd110_deskripti=request.POST['pmd110_deskripti']

        if ubah:
            try:
                ubah.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'PMD110',
            audittrail_transid= ubah.pmd110_id,
            audittrail_action= 'Update',
            audittrail_content= {
                "pmd110_id": ubah.pmd110_id,
                "pmd110_peraturan": ubah.pmd110_peraturan,
                "pmd110_kategori": ubah.pmd110_kategori,
                "pmd110_no": ubah.pmd110_no,
                "pmd110_hs_code": ubah.pmd110_hs_code,
                "pmd110_deskripti": ubah.pmd110_deskripti,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )
        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "PMD110 has been updated"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to update PMD110"}, status=status.HTTP_400_BAD_REQUEST)

def delete_pmd110(request, delete_id):
    if request.method == 'GET':
        hapus = PMD110.objects.filter(pmd110_id=delete_id)
        insertAuditTrail = AuditTrail(
            audittrail_transname = 'PMD110',
            audittrail_transid= hapus.pmd110_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "pmd110_id": hapus.pmd110_id,
                "pmd110_peraturan": hapus.pmd110_peraturan,
                "pmd110_kategori": hapus.pmd110_kategori,
                "pmd110_no": hapus.pmd110_no,
                "pmd110_hs_code": hapus.pmd110_hs_code,
                "pmd110_deskripti": hapus.pmd110_deskripti,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "PMD110 has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete PMD110"}, status=status.HTTP_400_BAD_REQUEST)

##kurs
def retrieve_kurs(request):
    if request.method == 'GET':
        products = Kurs.objects.all()
        serializer = KursSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Kurs"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_kurs(request, get_id):
    if request.method == 'GET':
        products = Kurs.objects.filter(kurs_id=get_id)
        serializer = KursSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Kurs"}, status=status.HTTP_400_BAD_REQUEST)

def create_kurs(request):
    if request.method == 'POST':
        insert = Kurs(
            kurs_code=request.POST['kurs_code'],
            kurs_name=request.POST['kurs_name'],
            kurs_value=request.POST['kurs_value'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Kurs',
            audittrail_transid= insert.kurs_id,
            audittrail_action= 'Create',
            audittrail_content= {
                    "kurs_id": insert.kurs_id,
                    "kurs_code": insert.kurs_code,
                    "kurs_name": insert.kurs_name,
                    "kurs_value": insert.kurs_value,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new Kurs has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new Kurs"}, status=status.HTTP_400_BAD_REQUEST)

def update_kurs(request, update_id):
    if request.method == 'POST':
        ubah = Kurs.objects.get(kurs_id=update_id)
        ubah.kurs_code=request.POST['kurs_code']
        ubah.kurs_name=request.POST['kurs_name']
        ubah.kurs_value=request.POST['kurs_value']

        if ubah:
            try:
                ubah.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Kurs',
            audittrail_transid= ubah.kurs_id,
            audittrail_action= 'Update',
            audittrail_content= {
                "kurs_id": ubah.kurs_id,
                "kurs_code": ubah.kurs_code,
                "kurs_name": ubah.kurs_name,
                "kurs_value": ubah.kurs_value,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )
        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "Kurs has been updated"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to update Kurs"}, status=status.HTTP_400_BAD_REQUEST)

def delete_kurs(request, delete_id):
    if request.method == 'GET':
        hapus = Kurs.objects.filter(kurs_id=delete_id)
        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Kurs',
            audittrail_transid= hapus.kurs_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "kurs_id": hapus.kurs_id,
                "kurs_code": hapus.kurs_code,
                "kurs_name": hapus.kurs_name,
                "kurs_value": hapus.kurs_value,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "Kurs has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete Kurs"}, status=status.HTTP_400_BAD_REQUEST)

##holiday
def retrieve_holiday(request):
    if request.method == 'GET':
        products = Holiday.objects.all()
        serializer = HolidaySerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Holiday"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_holiday(request, get_id):
    if request.method == 'GET':
        products = Holiday.objects.filter(holiday_id=get_id)
        serializer = HolidaySerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Holiday"}, status=status.HTTP_400_BAD_REQUEST)

def create_holiday(request):
    if request.method == 'POST':
        insert = Holiday(
            holiday_date=request.POST['holiday_date'],
            holiday_name=request.POST['holiday_name'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Holiday',
            audittrail_transid= insert.holiday_id,
            audittrail_action= 'Create',
            audittrail_content= {
                    "holiday_id": insert.holiday_id,
                    "holiday_date": insert.holiday_date,
                    "holiday_name": insert.holiday_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new Holiday has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new Holiday"}, status=status.HTTP_400_BAD_REQUEST)

def update_holiday(request, update_id):
    if request.method == 'POST':
        ubah = Holiday.objects.get(holiday_id=update_id)
        ubah.holiday_date=request.POST['holiday_date']
        ubah.holiday_name=request.POST['holiday_name']
        
        if ubah:
            try:
                ubah.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Holiday',
            audittrail_transid= ubah.holiday_id,
            audittrail_action= 'Update',
            audittrail_content= {
                "holiday_id": ubah.holiday_id,
                "holiday_date": ubah.holiday_date,
                "holiday_name": ubah.holiday_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )
        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "Holiday has been updated"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to update Holiday"}, status=status.HTTP_400_BAD_REQUEST)

def delete_holiday(request, delete_id):
    if request.method == 'GET':
        hapus = Holiday.objects.filter(holiday_id=delete_id)
        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Holiday',
            audittrail_transid= hapus.holiday_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "holiday_id": hapus.holiday_id,
                "holiday_date": hapus.holiday_date,
                "holiday_name": hapus.holiday_name,
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "Holiday has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete Holiday"}, status=status.HTTP_400_BAD_REQUEST)

##forwarder
def retrieve_forwarder(request):
    if request.method == 'GET':
        products = Forwarder.objects.all()
        serializer = ForwarderSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Forwarder"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_forwarder(request, get_id):
    if request.method == 'GET':
        products = Forwarder.objects.filter(forwarder_id=get_id)
        serializer = ForwarderSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Forwarder"}, status=status.HTTP_400_BAD_REQUEST)
        
def create_forwarder(request):
    if request.method == 'POST' and len(request.FILES) != 0:
        insert = Forwarder(
            forwarder_name = request.POST['forwarder_name'],
            forwarder_address1=request.POST['forwarder_address1'],
            forwarder_address2=request.POST['forwarder_address2'],
            forwarder_phone=request.POST['forwarder_phone'],
            forwarder_fax=request.POST['forwarder_fax'],
            forwarder_email=request.POST['forwarder_email'],
            forwarder_npwp=request.POST['forwarder_npwp'],
            forwarder_apip=request.POST['forwarder_apip'],
            forwarder_nib=request.POST['forwarder_nib'],
            forwarder_type=request.POST['forwarder_type'],
            forwarder_AccountNo=request.POST['forwarder_AccountNo'],
            forwarder_npwpDoc=request.FILES['forwarder_npwpDoc'],
            forwarder_sppkpDoc=request.FILES['forwarder_sppkpDoc'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Forwarder',
            audittrail_transid= insert.forwarder_id,
            audittrail_action= 'Create',
            audittrail_content= {
                "forwarder_id": insert.forwarder_id,
                "forwarder_name": insert.forwarder_name,
                "forwarder_address1": insert.forwarder_address1,
                "forwarder_address2": insert.forwarder_address2,
                "forwarder_phone": insert.forwarder_phone,
                "forwarder_fax": insert.forwarder_fax,
                "forwarder_email": insert.forwarder_email,
                "forwarder_npwp": insert.forwarder_npwp,
                "forwarder_apip": insert.forwarder_apip,
                "forwarder_nib": insert.forwarder_nib,
                "forwarder_type": insert.forwarder_type,
                "forwarder_AccountNo": insert.forwarder_AccountNo,
                "forwarder_npwpDoc": insert.forwarder_npwpDoc,
                "forwarder_sppkpDoc": insert.forwarder_sppkpDoc
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new Forwarder has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new Forwarder"}, status=status.HTTP_400_BAD_REQUEST)

def update_forwarder(request, update_id):
    ubah = Forwarder.objects.get(forwarder_id=update_id)
    if request.method == 'POST':
        if len(request.FILES) != 0:
            #buat delete gambar di folder
            npwp_path = str(ubah.forwarder_npwpDoc)
            sppkp_path = str(ubah.forwarder_sppkpDoc)

            #buat update data di db dan update gambar di folder
            ubah.forwarder_name = request.POST['forwarder_name']
            ubah.forwarder_address1=request.POST['forwarder_address1']
            ubah.forwarder_address2=request.POST['forwarder_address2']
            ubah.forwarder_phone=request.POST['forwarder_phone']
            ubah.forwarder_fax=request.POST['forwarder_fax']
            ubah.forwarder_email=request.POST['forwarder_email']
            ubah.forwarder_npwp=request.POST['forwarder_npwp']
            ubah.forwarder_apip=request.POST['forwarder_apip']
            ubah.forwarder_nib=request.POST['forwarder_nib']
            ubah.forwarder_type = request.POST['forwarder_type']
            ubah.forwarder_AccountNo = request.POST['forwarder_AccountNo']
            ubah.forwarder_npwpDoc = request.FILES['forwarder_npwpDoc']
            ubah.forwarder_sppkpDoc = request.FILES['forwarder_sppkpDoc']

            if npwp_path !='' and sppkp_path !='':
                try:
                    os.unlink(npwp_path)
                    os.unlink(sppkp_path)
                except(Exception)as e:
                    print('Exception',e)
                    pass

            if ubah:
                try:
                    ubah.save()
                except(Exception)as e:
                    print('Exception',e)
                    pass

            insertAuditTrail = AuditTrail(
                audittrail_transname = 'Forwarder',
                audittrail_transid= ubah.forwarder_id,
                audittrail_action= 'Update',
                audittrail_content= {
                    "forwarder_id": ubah.forwarder_id,
                    "forwarder_name": ubah.forwarder_name,
                    "forwarder_address1": ubah.forwarder_address1,
                    "forwarder_address2": ubah.forwarder_address2,
                    "forwarder_phone": ubah.forwarder_phone,
                    "forwarder_fax": ubah.forwarder_fax,
                    "forwarder_email": ubah.forwarder_email,
                    "forwarder_npwp": ubah.forwarder_npwp,
                    "forwarder_apip": ubah.forwarder_apip,
                    "forwarder_nib": ubah.forwarder_nib,
                    "forwarder_type": ubah.forwarder_type,
                    "forwarder_AccountNo": ubah.forwarder_AccountNo,
                    "forwarder_npwpDoc": ubah.forwarder_npwpDoc,
                    "forwarder_sppkpDoc": ubah.forwarder_sppkpDoc
                },
                audittrail_createdby='admin',
                audittrail_createdtime=datetime.now(),
                )
            if insertAuditTrail:
                try:
                    insertAuditTrail.save()
                    return JSONResponse({"status": True, "message": "Forwarder has been updated"}, status=status.HTTP_201_CREATED)
                except(Exception)as e:
                    print('Exception',e)
                    pass        
                return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
            return JSONResponse({"status": False, "message": "failed to update Forwarder"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            ubah.forwarder_name = request.POST['forwarder_name']
            ubah.forwarder_address1=request.POST['forwarder_address1']
            ubah.forwarder_address2=request.POST['forwarder_address2']
            ubah.forwarder_phone=request.POST['forwarder_phone']
            ubah.forwarder_fax=request.POST['forwarder_fax']
            ubah.forwarder_email=request.POST['forwarder_email']
            ubah.forwarder_npwp=request.POST['forwarder_npwp']
            ubah.forwarder_apip=request.POST['forwarder_apip']
            ubah.forwarder_nib=request.POST['forwarder_nib']
            ubah.forwarder_type = request.POST['forwarder_type']
            ubah.forwarder_AccountNo = request.POST['forwarder_AccountNo']

            if ubah:
                try:
                    ubah.save()
                except(Exception)as e:
                    print('Exception',e)
                    pass

            insertAuditTrail = AuditTrail(
                audittrail_transname = 'Forwarder',
                audittrail_transid= ubah.forwarder_id,
                audittrail_action= 'Update',
                audittrail_content= {
                    "forwarder_id": ubah.forwarder_id,
                    "forwarder_name": ubah.forwarder_name,
                    "forwarder_address1": ubah.forwarder_address1,
                    "forwarder_address2": ubah.forwarder_address2,
                    "forwarder_phone": ubah.forwarder_phone,
                    "forwarder_fax": ubah.forwarder_fax,
                    "forwarder_email": ubah.forwarder_email,
                    "forwarder_npwp": ubah.forwarder_npwp,
                    "forwarder_apip": ubah.forwarder_apip,
                    "forwarder_nib": ubah.forwarder_nib,
                    "forwarder_type": ubah.forwarder_type,
                    "forwarder_AccountNo": ubah.forwarder_AccountNo,
                    "forwarder_npwpDoc": ubah.forwarder_npwpDoc,
                    "forwarder_sppkpDoc": ubah.forwarder_sppkpDoc
                },
                audittrail_createdby='admin',
                audittrail_createdtime=datetime.now(),
                )
            if insertAuditTrail:
                try:
                    insertAuditTrail.save()
                    return JSONResponse({"status": True, "message": "Forwarder has been updated"}, status=status.HTTP_201_CREATED)
                except(Exception)as e:
                    print('Exception',e)
                    pass        
                return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
            return JSONResponse({"status": False, "message": "failed to update Forwarder"}, status=status.HTTP_400_BAD_REQUEST)

def delete_forwarder(request, delete_id):
    if request.method == 'GET':
        hapus = Forwarder.objects.filter(forwarder_id=delete_id)
        npwp_path = str(hapus.forwarder_npwpDoc)
        sppkp_path = str(hapus.forwarder_sppkpDoc)

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Forwarder',
            audittrail_transid= hapus.forwarder_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "forwarder_id": hapus.forwarder_id,
                "forwarder_name": hapus.forwarder_name,
                "forwarder_address1": hapus.forwarder_address1,
                "forwarder_address2": hapus.forwarder_address2,
                "forwarder_phone": hapus.forwarder_phone,
                "forwarder_fax": hapus.forwarder_fax,
                "forwarder_email": hapus.forwarder_email,
                "forwarder_npwp": hapus.forwarder_npwp,
                "forwarder_apip": hapus.forwarder_apip,
                "forwarder_nib": hapus.forwarder_nib,
                "forwarder_type": hapus.forwarder_type,
                "forwarder_AccountNo": hapus.forwarder_AccountNo,
                "forwarder_npwpDoc": hapus.forwarder_npwpDoc,
                "forwarder_sppkpDoc": hapus.forwarder_sppkpDoc
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if npwp_path !='' and sppkp_path !='':
            try:
                os.unlink(npwp_path)
                os.unlink(sppkp_path)
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "Forwarder has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete Forwarder"}, status=status.HTTP_400_BAD_REQUEST)

##seller
def retrieve_seller(request):
    if request.method == 'GET': 
        products = Seller.objects.all()
        serializer = SellerSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Seller"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_seller(request, get_id):
    if request.method == 'GET':
        products = Seller.objects.filter(seller_id=get_id)
        serializer = SellerSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Seller"}, status=status.HTTP_400_BAD_REQUEST)
        
def create_seller(request):
    if request.method == 'POST' and len(request.FILES) != 0:
        insert = Seller(
            seller_name = request.POST['seller_name'],
            seller_address1=request.POST['seller_address1'],
            seller_address2=request.POST['seller_address2'],
            seller_phone=request.POST['seller_phone'],
            seller_fax=request.POST['seller_fax'],
            seller_email=request.POST['seller_email'],
            seller_npwp=request.POST['seller_npwp'],
            seller_apip=request.POST['seller_apip'],
            seller_nib=request.POST['seller_nib'],
            seller_type=request.POST['seller_type'],
            seller_AccountNo=request.POST['seller_AccountNo'],
            seller_npwpDoc=request.FILES['seller_npwpDoc'],
            seller_sppkpDoc=request.FILES['seller_sppkpDoc'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Seller',
            audittrail_transid= insert.seller_id,
            audittrail_action= 'Create',
            audittrail_content= {
                "seller_id": insert.seller_id,
                "seller_name": insert.seller_name,
                "seller_address1": insert.seller_address1,
                "seller_address2": insert.seller_address2,
                "seller_phone": insert.seller_phone,
                "seller_fax": insert.seller_fax,
                "seller_email": insert.seller_email,
                "seller_npwp": insert.seller_npwp,
                "seller_apip": insert.seller_apip,
                "seller_nib": insert.seller_nib,
                "seller_type": insert.seller_type,
                "seller_AccountNo": insert.seller_AccountNo,
                "seller_npwpDoc": insert.seller_npwpDoc,
                "seller_sppkpDoc": insert.seller_sppkpDoc
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new Seller has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new Seller"}, status=status.HTTP_400_BAD_REQUEST)

def update_seller(request, update_id):
    ubah = Seller.objects.get(seller_id=update_id)
    if request.method == 'POST':
        if len(request.FILES) != 0:
            #buat delete gambar di folder
            npwp_path = str(ubah.seller_npwpDoc)
            sppkp_path = str(ubah.seller_sppkpDoc)

            #buat update data di db dan update gambar di folder
            ubah.seller_name = request.POST['seller_name']
            ubah.seller_address1=request.POST['seller_address1']
            ubah.seller_address2=request.POST['seller_address2']
            ubah.seller_phone=request.POST['seller_phone']
            ubah.seller_fax=request.POST['seller_fax']
            ubah.seller_email=request.POST['seller_email']
            ubah.seller_npwp=request.POST['seller_npwp']
            ubah.seller_apip=request.POST['seller_apip']
            ubah.seller_nib=request.POST['seller_nib']
            ubah.seller_type = request.POST['seller_type']
            ubah.seller_AccountNo = request.POST['seller_AccountNo']
            ubah.seller_npwpDoc = request.FILES['seller_npwpDoc']
            ubah.seller_npwpDoc = request.FILES['seller_npwpDoc']

            if npwp_path !='' and sppkp_path !='':
                try:
                    os.unlink(npwp_path)
                    os.unlink(sppkp_path)
                except(Exception)as e:
                    print('Exception',e)
                    pass

            if ubah:
                try:
                    ubah.save()
                except(Exception)as e:
                    print('Exception',e)
                    pass

            insertAuditTrail = AuditTrail(
                audittrail_transname = 'Seller',
                audittrail_transid= ubah.seller_id,
                audittrail_action= 'Update',
                audittrail_content= {
                    "seller_id": ubah.seller_id,
                    "seller_name": ubah.seller_name,
                    "seller_address1": ubah.seller_address1,
                    "seller_address2": ubah.seller_address2,
                    "seller_phone": ubah.seller_phone,
                    "seller_fax": ubah.seller_fax,
                    "seller_email": ubah.seller_email,
                    "seller_npwp": ubah.seller_npwp,
                    "seller_apip": ubah.seller_apip,
                    "seller_nib": ubah.seller_nib,
                    "seller_type": ubah.seller_type,
                    "seller_AccountNo": ubah.seller_AccountNo,
                    "seller_npwpDoc": ubah.seller_npwpDoc,
                    "seller_sppkpDoc": ubah.seller_sppkpDoc
                },
                audittrail_createdby='admin',
                audittrail_createdtime=datetime.now(),
                )
            if insertAuditTrail:
                try:
                    insertAuditTrail.save()
                    return JSONResponse({"status": True, "message": "Seller has been updated"}, status=status.HTTP_201_CREATED)
                except(Exception)as e:
                    print('Exception',e)
                    pass        
                return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
            return JSONResponse({"status": False, "message": "failed to update Seller"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            ubah.seller_name = request.POST['seller_name']
            ubah.seller_address1=request.POST['seller_address1']
            ubah.seller_address2=request.POST['seller_address2']
            ubah.seller_phone=request.POST['seller_phone']
            ubah.seller_fax=request.POST['seller_fax']
            ubah.seller_email=request.POST['seller_email']
            ubah.seller_npwp=request.POST['seller_npwp']
            ubah.seller_apip=request.POST['seller_apip']
            ubah.seller_nib=request.POST['seller_nib']
            ubah.seller_type = request.POST['seller_type']
            ubah.seller_AccountNo = request.POST['seller_AccountNo']

            if ubah:
                try:
                    ubah.save()
                except(Exception)as e:
                    print('Exception',e)
                    pass

            insertAuditTrail = AuditTrail(
                audittrail_transname = 'Seller',
                audittrail_transid= ubah.seller_id,
                audittrail_action= 'Update',
                audittrail_content= {
                    "seller_id": ubah.seller_id,
                    "seller_name": ubah.seller_name,
                    "seller_address1": ubah.seller_address1,
                    "seller_address2": ubah.seller_address2,
                    "seller_phone": ubah.seller_phone,
                    "seller_fax": ubah.seller_fax,
                    "seller_email": ubah.seller_email,
                    "seller_npwp": ubah.seller_npwp,
                    "seller_apip": ubah.seller_apip,
                    "seller_nib": ubah.seller_nib,
                    "seller_type": ubah.seller_type,
                    "seller_AccountNo": ubah.seller_AccountNo,
                    "seller_npwpDoc": ubah.seller_npwpDoc,
                    "seller_sppkpDoc": ubah.seller_sppkpDoc
                },
                audittrail_createdby='admin',
                audittrail_createdtime=datetime.now(),
                )
            if insertAuditTrail:
                try:
                    insertAuditTrail.save()
                    return JSONResponse({"status": True, "message": "Seller has been updated"}, status=status.HTTP_201_CREATED)
                except(Exception)as e:
                    print('Exception',e)
                    pass        
                return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
            return JSONResponse({"status": False, "message": "failed to update Seller"}, status=status.HTTP_400_BAD_REQUEST)

def delete_seller(request, delete_id):
    if request.method == 'GET':
        hapus = Seller.objects.filter(seller_id=delete_id)
        npwp_path = str(hapus.seller_npwpDoc)
        sppkp_path = str(hapus.seller_sppkpDoc)

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Forwarder',
            audittrail_transid= hapus.seller_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "seller_id": hapus.seller_id,
                "seller_name": hapus.seller_name,
                "seller_address1": hapus.seller_address1,
                "seller_address2": hapus.seller_address2,
                "seller_phone": hapus.seller_phone,
                "seller_fax": hapus.seller_fax,
                "seller_email": hapus.seller_email,
                "seller_npwp": hapus.seller_npwp,
                "seller_apip": hapus.seller_apip,
                "seller_nib": hapus.seller_nib,
                "seller_type": hapus.seller_type,
                "seller_AccountNo": hapus.seller_AccountNo,
                "seller_npwpDoc": hapus.seller_npwpDoc,
                "seller_sppkpDoc": hapus.seller_sppkpDoc
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if npwp_path !='' and sppkp_path !='':
            try:
                os.unlink(npwp_path)
                os.unlink(sppkp_path)
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "Seller has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete Seller"}, status=status.HTTP_400_BAD_REQUEST)

##shipper
def retrieve_shipper(request):
    if request.method == 'GET': 
        products = Shipper.objects.all()
        serializer = ShipperSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Shipper"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_shipper(request, get_id):
    if request.method == 'GET':
        products = Shipper.objects.filter(shipper_id=get_id)
        serializer = ShipperSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Shipper"}, status=status.HTTP_400_BAD_REQUEST)
        
def create_shipper(request):
    if request.method == 'POST' and len(request.FILES) != 0:
        insert = Shipper(
            shipper_name = request.POST['shipper_name'],
            shipper_address1=request.POST['shipper_address1'],
            shipper_address2=request.POST['shipper_address2'],
            shipper_phone=request.POST['shipper_phone'],
            shipper_fax=request.POST['shipper_fax'],
            shipper_email=request.POST['shipper_email'],
            shipper_npwp=request.POST['shipper_npwp'],
            shipper_apip=request.POST['shipper_apip'],
            shipper_nib=request.POST['shipper_nib'],
            shipper_type=request.POST['shipper_type'],
            shipper_AccountNo=request.POST['shipper_AccountNo'],
            shipper_npwpDoc=request.FILES['shipper_npwpDoc'],
            shipper_sppkpDoc=request.FILES['shipper_sppkpDoc'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Shipper',
            audittrail_transid= insert.shipper_id,
            audittrail_action= 'Create',
            audittrail_content= {
                "shipper_id": insert.shipper_id,
                "shipper_name": insert.shipper_name,
                "shipper_address1": insert.shipper_address1,
                "shipper_address2": insert.shipper_address2,
                "shipper_phone": insert.shipper_phone,
                "shipper_fax": insert.shipper_fax,
                "shipper_email": insert.shipper_email,
                "shipper_npwp": insert.shipper_npwp,
                "shipper_apip": insert.shipper_apip,
                "shipper_nib": insert.shipper_nib,
                "shipper_type": insert.shipper_type,
                "shipper_AccountNo": insert.shipper_AccountNo,
                "shipper_npwpDoc": insert.shipper_npwpDoc,
                "shipper_sppkpDoc": insert.shipper_sppkpDoc
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new Shipper has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new Shipper"}, status=status.HTTP_400_BAD_REQUEST)

def update_shipper(request, update_id):
    ubah = Shipper.objects.get(shipper_id=update_id)
    if request.method == 'POST':
        if len(request.FILES) != 0:
            #buat delete gambar di folder
            npwp_path = str(ubah.shipper_npwpDoc)
            sppkp_path = str(ubah.shipper_sppkpDoc)

            #buat update data di db dan update gambar di folder
            ubah.shipper_name = request.POST['shipper_name']
            ubah.shipper_address1=request.POST['shipper_address1']
            ubah.shipper_address2=request.POST['shipper_address2']
            ubah.shipper_phone=request.POST['shipper_phone']
            ubah.shipper_fax=request.POST['shipper_fax']
            ubah.shipper_email=request.POST['shipper_email']
            ubah.shipper_npwp=request.POST['shipper_npwp']
            ubah.shipper_apip=request.POST['shipper_apip']
            ubah.shipper_nib=request.POST['shipper_nib']
            ubah.shipper_type = request.POST['shipper_type']
            ubah.shipper_AccountNo = request.POST['shipper_AccountNo']
            ubah.shipper_npwpDoc = request.FILES['shipper_npwpDoc']
            ubah.shipper_npwpDoc = request.FILES['shipper_npwpDoc']

            if npwp_path !='' and sppkp_path !='':
                try:
                    os.unlink(npwp_path)
                    os.unlink(sppkp_path)
                except(Exception)as e:
                    print('Exception',e)
                    pass

            if ubah:
                try:
                    ubah.save()
                except(Exception)as e:
                    print('Exception',e)
                    pass

            insertAuditTrail = AuditTrail(
                audittrail_transname = 'Shipper',
                audittrail_transid= ubah.shipper_id,
                audittrail_action= 'Update',
                audittrail_content= {
                    "shipper_id": ubah.shipper_id,
                    "shipper_name": ubah.shipper_name,
                    "shipper_address1": ubah.shipper_address1,
                    "shipper_address2": ubah.shipper_address2,
                    "shipper_phone": ubah.shipper_phone,
                    "shipper_fax": ubah.shipper_fax,
                    "shipper_email": ubah.shipper_email,
                    "shipper_npwp": ubah.shipper_npwp,
                    "shipper_apip": ubah.shipper_apip,
                    "shipper_nib": ubah.shipper_nib,
                    "shipper_type": ubah.shipper_type,
                    "shipper_AccountNo": ubah.shipper_AccountNo,
                    "shipper_npwpDoc": ubah.shipper_npwpDoc,
                    "shipper_sppkpDoc": ubah.shipper_sppkpDoc
                },
                audittrail_createdby='admin',
                audittrail_createdtime=datetime.now(),
                )
            if insertAuditTrail:
                try:
                    insertAuditTrail.save()
                    return JSONResponse({"status": True, "message": "Shipper has been updated"}, status=status.HTTP_201_CREATED)
                except(Exception)as e:
                    print('Exception',e)
                    pass        
                return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
            return JSONResponse({"status": False, "message": "failed to update Shipper"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            ubah.shipper_name = request.POST['shipper_name']
            ubah.shipper_address1=request.POST['shipper_address1']
            ubah.shipper_address2=request.POST['shipper_address2']
            ubah.shipper_phone=request.POST['shipper_phone']
            ubah.shipper_fax=request.POST['shipper_fax']
            ubah.shipper_email=request.POST['shipper_email']
            ubah.shipper_npwp=request.POST['shipper_npwp']
            ubah.shipper_apip=request.POST['shipper_apip']
            ubah.shipper_nib=request.POST['shipper_nib']
            ubah.shipper_type = request.POST['shipper_type']
            ubah.shipper_AccountNo = request.POST['shipper_AccountNo']

            if ubah:
                try:
                    ubah.save()
                except(Exception)as e:
                    print('Exception',e)
                    pass

            insertAuditTrail = AuditTrail(
                audittrail_transname = 'Shipper',
                audittrail_transid= ubah.shipper_id,
                audittrail_action= 'Update',
                audittrail_content= {
                    "shipper_id": ubah.shipper_id,
                    "shipper_name": ubah.shipper_name,
                    "shipper_address1": ubah.shipper_address1,
                    "shipper_address2": ubah.shipper_address2,
                    "shipper_phone": ubah.shipper_phone,
                    "shipper_fax": ubah.shipper_fax,
                    "shipper_email": ubah.shipper_email,
                    "shipper_npwp": ubah.shipper_npwp,
                    "shipper_apip": ubah.shipper_apip,
                    "shipper_nib": ubah.shipper_nib,
                    "shipper_type": ubah.shipper_type,
                    "shipper_AccountNo": ubah.shipper_AccountNo,
                    "shipper_npwpDoc": ubah.shipper_npwpDoc,
                    "shipper_sppkpDoc": ubah.shipper_sppkpDoc
                },
                audittrail_createdby='admin',
                audittrail_createdtime=datetime.now(),
                )
            if insertAuditTrail:
                try:
                    insertAuditTrail.save()
                    return JSONResponse({"status": True, "message": "Shipper has been updated"}, status=status.HTTP_201_CREATED)
                except(Exception)as e:
                    print('Exception',e)
                    pass        
                return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
            return JSONResponse({"status": False, "message": "failed to update Shipper"}, status=status.HTTP_400_BAD_REQUEST)

def delete_shipper(request, delete_id):
    if request.method == 'GET':
        hapus = Shipper.objects.filter(shipper_id=delete_id)
        npwp_path = str(hapus.shipper_npwpDoc)
        sppkp_path = str(hapus.shipper_sppkpDoc)

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Shipper',
            audittrail_transid= hapus.shipper_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "shipper_id": hapus.shipper_id,
                "shipper_name": hapus.shipper_name,
                "shipper_address1": hapus.shipper_address1,
                "shipper_address2": hapus.shipper_address2,
                "shipper_phone": hapus.shipper_phone,
                "shipper_fax": hapus.shipper_fax,
                "shipper_email": hapus.shipper_email,
                "shipper_npwp": hapus.shipper_npwp,
                "shipper_apip": hapus.shipper_apip,
                "shipper_nib": hapus.shipper_nib,
                "shipper_type": hapus.shipper_type,
                "shipper_AccountNo": hapus.shipper_AccountNo,
                "shipper_npwpDoc": hapus.shipper_npwpDoc,
                "shipper_sppkpDoc": hapus.shipper_sppkpDoc
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if npwp_path !='' and sppkp_path !='':
            try:
                os.unlink(npwp_path)
                os.unlink(sppkp_path)
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "Shipper has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete Shipper"}, status=status.HTTP_400_BAD_REQUEST)

##audittrail
def retrieve_audittrail(request):
    if request.method == 'GET': 
        products = AuditTrail.objects.all()
        serializer = AuditTrailSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Seller"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_audittrail(request, get_id):
    if request.method == 'GET':
        products = AuditTrail.objects.filter(audittrail_id=get_id)
        serializer = AuditTrailSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Seller"}, status=status.HTTP_400_BAD_REQUEST)
        
def create_audittrail(request):
    if request.method == 'POST':
        insert = AuditTrail(
            audittrail_transname = request.POST['audittrail_transname'],
            audittrail_transid=request.POST['audittrail_transid'],
            audittrail_action=request.POST['audittrail_action'],
            audittrail_content=request.POST['audittrail_content'],
            audittrail_createdby=request.POST['audittrail_createdby'],
            audittrail_createdtime=datetime.now(),
        )

        if insert:
            try:
                insert.save()
                return JSONResponse({"status": True, "message": "new AuditTrail has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new AuditTrail"}, status=status.HTTP_400_BAD_REQUEST)

def update_audittrail(request, update_id):
    if request.method == 'POST':
        ubah = AuditTrail.objects.filter(audittrail_id=update_id)

        if ubah:
            try:
                ubah.update(
                        audittrail_transname = request.POST['audittrail_transname'],
                        audittrail_transid=request.POST['audittrail_transid'],
                        audittrail_action=request.POST['audittrail_action'],
                        audittrail_content=request.POST['audittrail_content'],
                        audittrail_createdby=request.POST['audittrail_createdby'],
                        audittrail_createdtime=datetime.now(),
                    )
                return JSONResponse({"status": True, "message": "AuditTrail has been updated"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to update AuditTrail"}, status=status.HTTP_400_BAD_REQUEST)

def delete_audittrail(request, delete_id):
    if request.method == 'GET':
        hapus = AuditTrail.objects.filter(audittrail_id=delete_id)

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "AuditTrail has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete AuditTrail"}, status=status.HTTP_400_BAD_REQUEST)

##masterlist
def retrieve_masterlist(request):
    if request.method == 'GET': 
        products = MasterList.objects.all()
        serializer = MasterListSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data MasterList"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_masterlist(request, get_id):
    if request.method == 'GET':
        products = MasterList.objects.filter(ml_id=get_id)
        serializer = MasterListSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data MasterList"}, status=status.HTTP_400_BAD_REQUEST)
        
def create_masterlist(request):
    if request.method == 'POST':
        insert = MasterList(
            ml_ofonshore = request.POST['ml_ofonshore'],
            ml_epc=request.POST['ml_epc'],
            ml_epc_item_num=request.POST['ml_epc_item_num'],
            ml_kmk_no=request.POST['ml_kmk_no'],
            ml_oth_kmk_no=request.POST['ml_oth_kmk_no'],
            ml_kmk_full=request.POST['ml_kmk_full'],
            ml_kmk_main = request.POST['ml_kmk_main'],
            ml_kmk_sub=request.POST['ml_kmk_sub'],
            ml_item_desc=request.POST['ml_item_desc'],
            ml_item_spec=request.POST['ml_item_spec'],
            ml_oigin=request.POST['ml_oigin'],
            ml_kmk_total=request.POST['ml_kmk_total'],
            ml_kmk_unit_id=request.POST['ml_kmk_unit_id'],
            ml_kmk_price_total=request.POST['ml_kmk_price_total'],
            ml_hs_code=request.POST['ml_hs_code'],
        )

        if insert:
            try:
                insert.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'MasterList',
            audittrail_transid= insert.ml_id,
            audittrail_action= 'Create',
            audittrail_content= {
                "ml_id": insert.ml_id,
                "ml_ofonshore": insert.ml_ofonshore,
                "ml_epc": insert.ml_epc,
                "ml_epc_item_num": insert.ml_epc_item_num,
                "ml_kmk_no": insert.ml_kmk_no,
                "ml_oth_kmk_no": insert.ml_oth_kmk_no,
                "ml_kmk_full": insert.ml_kmk_full,
                "ml_kmk_main": insert.ml_kmk_main,
                "ml_kmk_sub": insert.ml_kmk_sub,
                "ml_item_desc": insert.ml_item_desc,
                "ml_item_spec": insert.ml_item_spec,
                "ml_oigin": insert.ml_oigin,
                "ml_kmk_total": insert.ml_kmk_total,
                "ml_kmk_unit_id": insert.ml_kmk_unit_id,
                "ml_kmk_price_total": insert.ml_kmk_price_total,
                "ml_hs_code": insert.ml_hs_code
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "new MasterList has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new MasterList"}, status=status.HTTP_400_BAD_REQUEST)

def update_masterlist(request, update_id):
    if request.method == 'POST':
        ubah = MasterList.objects.get(ml_id=update_id)
        ubah.ml_ofonshore=request.POST['ml_ofonshore']
        ubah.ml_epc=request.POST['ml_epc']
        ubah.ml_epc_item_num=request.POST['ml_epc_item_num']
        ubah.ml_kmk_no=request.POST['ml_kmk_no']
        ubah.ml_oth_kmk_no=request.POST['ml_oth_kmk_no']
        ubah.ml_kmk_full=request.POST['ml_kmk_full']
        ubah.ml_kmk_main=request.POST['ml_kmk_main']
        ubah.ml_kmk_sub=request.POST['ml_kmk_sub']
        ubah.ml_item_desc=request.POST['ml_item_desc']
        ubah.ml_item_spec=request.POST['ml_item_spec']
        ubah.ml_oigin=request.POST['ml_oigin']
        ubah.ml_kmk_total=request.POST['ml_kmk_total']
        ubah.ml_kmk_unit_id=request.POST['ml_kmk_unit_id']
        ubah.ml_kmk_price_total=request.POST['ml_kmk_price_total']
        ubah.ml_hs_code=request.POST['ml_hs_code']

        if ubah:
            try:
                ubah.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'MasterList',
            audittrail_transid= ubah.ml_id,
            audittrail_action= 'Update',
            audittrail_content= {
                "ml_id": ubah.ml_id,
                "ml_ofonshore": ubah.ml_ofonshore,
                "ml_epc": ubah.ml_epc,
                "ml_epc_item_num": ubah.ml_epc_item_num,
                "ml_kmk_no": ubah.ml_kmk_no,
                "ml_oth_kmk_no": ubah.ml_oth_kmk_no,
                "ml_kmk_full": ubah.ml_kmk_full,
                "ml_kmk_main": ubah.ml_kmk_main,
                "ml_kmk_sub": ubah.ml_kmk_sub,
                "ml_item_desc": ubah.ml_item_desc,
                "ml_item_spec": ubah.ml_item_spec,
                "ml_oigin": ubah.ml_oigin,
                "ml_kmk_total": ubah.ml_kmk_total,
                "ml_kmk_unit_id": ubah.ml_kmk_unit_id,
                "ml_kmk_price_total": ubah.ml_kmk_price_total,
                "ml_hs_code": ubah.ml_hs_code
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )
        if insertAuditTrail:
            try:
                insertAuditTrail.save()
                return JSONResponse({"status": True, "message": "MasterList has been updated"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to update MasterList"}, status=status.HTTP_400_BAD_REQUEST)

def delete_masterlist(request, delete_id):
    if request.method == 'GET':
        hapus = MasterList.objects.filter(ml_id=delete_id)
        insertAuditTrail = AuditTrail(
            audittrail_transname = 'MasterList',
            audittrail_transid= hapus.ml_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "ml_id": hapus.ml_id,
                "ml_ofonshore": hapus.ml_ofonshore,
                "ml_epc": hapus.ml_epc,
                "ml_epc_item_num": hapus.ml_epc_item_num,
                "ml_kmk_no": hapus.ml_kmk_no,
                "ml_oth_kmk_no": hapus.ml_oth_kmk_no,
                "ml_kmk_full": hapus.ml_kmk_full,
                "ml_kmk_main": hapus.ml_kmk_main,
                "ml_kmk_sub": hapus.ml_kmk_sub,
                "ml_item_desc": hapus.ml_item_desc,
                "ml_item_spec": hapus.ml_item_spec,
                "ml_oigin": hapus.ml_oigin,
                "ml_kmk_total": hapus.ml_kmk_total,
                "ml_kmk_unit_id": hapus.ml_kmk_unit_id,
                "ml_kmk_price_total": hapus.ml_kmk_price_total,
                "ml_hs_code": hapus.ml_hs_code
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "MasterList has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete MasterList"}, status=status.HTTP_400_BAD_REQUEST)

##shipment
def retrieve_shipment(request):
    if request.method == 'GET': 
        products = Shipment.objects.all()
        serializer = ShipmentSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Shipment"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_shipment(request, get_id):
    if request.method == 'GET':
        products = Shipment.objects.filter(shipment_id=get_id)
        serializer = ShipmentSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Shipment"}, status=status.HTTP_400_BAD_REQUEST)
        
def create_shipment(request):
    if request.method == 'POST':
        if len(request.FILES) != 0:
            insert = Shipment(
            company_id=request.POST['company_id'],
            shipper_id=request.POST['shipper_id'],
            seller_id=request.POST['seller_id'],
            pol_id=request.POST['pol_id'],
            ppjk_id=request.POST['ppjk_id'],
            kppbc_id = request.POST['kppbc_id'],
            ship_no=request.POST['ship_no'],
            invpl_no=request.POST['invpl_no'],
            gen_desc=request.POST['gen_desc'],
            shipper_name=request.POST['shipper_name'],
            epc=request.POST['epc'],
            po_no=request.POST['po_no'],
            bl_no=request.POST['bl_no'],
            bl_date=request.POST['bl_date'],
            etd_date = request.POST['etd_date'],
            inv_date=request.POST['inv_date'],
            inv_uni=request.POST['inv_uni'],
            inv_term=request.POST['inv_term'],
            inv_curr=request.POST['inv_curr'],
            inv_amo=request.POST['inv_amo'],
            inv_qty = request.POST['inv_qty'],
            pod_name=request.POST['pod_name'],
            vessel_flight=request.POST['vessel_flight'],
            eta_date=request.POST['eta_date'],
            no_pkg=request.POST['no_pkg'],
            type=request.POST['type'],
            ata_date=request.POST['ata_date'],
            no_cntr=request.POST['no_cntr'],
            sppb_date=request.POST['sppb_date'],
            tgross_kgs = request.POST['tgross_kgs'],
            site_date=request.POST['site_date'],
            cipl_rcvdate=request.POST['cipl_rcvdate'],
            photo_rcvdate=request.POST['photo_rcvdate'],
            bl_rcvdate=request.POST['bl_rcvdate'],
            co_rcvdate=request.POST['co_rcvdate'],
            co_no = request.POST['co_no'],
            dpib_rcvdate=request.POST['dpib_rcvdate'],
            pibaju_no=request.POST['pibaju_no'],
            skbppn_initdate=request.POST['skbppn_initdate'],
            skbppn_signdate=request.POST['skbppn_signdate'],
            skbppn_subdate=request.POST['skbppn_subdate'],
            skbppn_rcvdate=request.POST['skbppn_rcvdate'],
            skbppn_dlvdate=request.POST['skbppn_dlvdate'],
            rcv_by=request.POST['rcv_by'],
            skbpph_initdate=request.POST['skbppn_initdate'],
            skbpph_signdate=request.POST['skbppn_signdate'],
            skbpph_subdate=request.POST['skbppn_subdate'],
            skbpph_rcvdate=request.POST['skbppn_rcvdate'],
            skbpph_dlvdate=request.POST['skbppn_dlvdate'],
            custdoc_initdate=request.POST['custdoc_initdate'],
            custdoc_signdate = request.POST['custdoc_signdate'],
            custdoc_dlvdate=request.POST['custdoc_dlvdate'],
            ltrreffkpp_no=request.POST['ltrreffkpp_no'],
            ltrreffppjk_no=request.POST['ltrreffppjk_no'],
            ltrreffbc_no=request.POST['ltrreffbc_no'],
            ins_no=request.POST['ins_no'],
            pib_submit_date=request.POST['pib_submit_date'],
            kode_bill=request.POST['kode_bill'],
            ntpn=request.POST['ntpn'],
            pibreg_date=request.POST['pibreg_date'],
            pibreg_no=request.POST['pibreg_no'],
            spjkm=request.POST['spjkm'],
            sppb_no=request.POST['sppb_no'],
            bm=request.POST['bm'],
            ppn=request.POST['ppn'],
            ppnbm = request.POST['ppnbm'],
            pph=request.POST['pph'],
            denda=request.POST['denda'],
            pnbp=request.POST['pnbp'],
            pay_date=request.POST['pay_date'],
            attachment1=request.FILES['attachment1'],
            attachment2=request.FILES['attachment2'],
            )

            if insert:
                try:
                    insert.save()
                except(Exception)as e:
                    print('Exception',e)
                    pass

            insert_detail = Shipment_Detail.objects.create(
                    header_id=insert.shipment_id,
                    kmk_no=request.POST['kmk_no'],
                    kmk_item_no=request.POST['kmk_item_no'],
                    kmk_itemm_sub=request.POST['kmk_itemm_sub'],
                    pib_desc=request.POST['pib_desc'],
                )

            if insert_detail:
                insertAuditTrail = AuditTrail(
                    audittrail_transname = 'Shipment',
                    audittrail_transid= insert.shipment_id,
                    audittrail_action= 'Create',
                    audittrail_content= {
                        "shipment_id": insert.shipment_id,
                        "company_id": insert.company_id,
                        "shipper_id": insert.shipper_id,
                        "seller_id": insert.seller_id,
                        "pol_id": insert.pol_id,
                        "ppjk_id": insert.ppjk_id,
                        "kppbc_id": insert.kppbc_id,
                        "ship_no": insert.ship_no,
                        "invpl_no": insert.invpl_no,
                        "gen_desc": insert.gen_desc,
                        "shipper_name": insert.shipper_name,
                        "epc": insert.epc,
                        "po_no": insert.po_no,
                        "bl_no": insert.bl_no,
                        "bl_date": insert.bl_date,
                        "etd_date": insert.etd_date,
                        "inv_date": insert.inv_date,
                        "inv_uni": insert.inv_uni,
                        "inv_term": insert.inv_term,
                        "inv_curr": insert.inv_curr,
                        "inv_amo": insert.inv_amo,
                        "inv_qty": insert.inv_qty,
                        "pod_name": insert.pod_name,
                        "vessel_flight": insert.vessel_flight,
                        "eta_date": insert.eta_date,
                        "no_pkg": insert.no_pkg,
                        "type": insert.type,
                        "ata_date": insert.ata_date,
                        "no_cntr": insert.no_cntr,
                        "sppb_date": insert.sppb_date,
                        "tgross_kgs": insert.tgross_kgs,
                        "site_date": insert.site_date,
                        "cipl_rcvdate": insert.cipl_rcvdate,
                        "photo_rcvdate": insert.photo_rcvdate,
                        "bl_rcvdate": insert.bl_rcvdate,
                        "co_rcvdate": insert.co_rcvdate,
                        "co_no": insert.co_no,
                        "dpib_rcvdate": insert.dpib_rcvdate,
                        "pibaju_no": insert.pibaju_no,
                        "skbppn_initdate": insert.skbppn_initdate,
                        "skbppn_signdate": insert.skbppn_signdate,
                        "skbppn_subdate": insert.skbppn_subdate,
                        "skbppn_rcvdate": insert.skbppn_rcvdate,
                        "skbppn_dlvdate": insert.skbppn_dlvdate,
                        "rcv_by": insert.rcv_by,
                        "skbpph_initdate": insert.skbpph_initdate,
                        "skbpph_signdate": insert.skbpph_signdate,
                        "skbpph_subdate": insert.skbpph_subdate,
                        "skbpph_rcvdate": insert.skbpph_rcvdate,
                        "skbpph_dlvdate": insert.skbpph_dlvdate,
                        "custdoc_initdate": insert.custdoc_initdate,
                        "custdoc_signdate": insert.custdoc_signdate,
                        "custdoc_dlvdate": insert.custdoc_dlvdate,
                        "ltrreffkpp_no": insert.ltrreffkpp_no,
                        "ltrreffppjk_no": insert.ltrreffppjk_no,
                        "ltrreffbc_no": insert.ltrreffbc_no,
                        "ins_no": insert.ins_no,
                        "pib_submit_date": insert.pib_submit_date,
                        "kode_bill": insert.kode_bill,
                        "ntpn": insert.ntpn,
                        "pibreg_date": insert.pibreg_date,
                        "pibreg_no": insert.pibreg_no,
                        "spjkm": insert.spjkm,
                        "sppb_no": insert.sppb_no,
                        "bm": insert.bm,
                        "ppn": insert.ppn,
                        "ppnbm": insert.ppnbm,
                        "pph": insert.pph,
                        "denda": insert.denda,
                        "pnbp": insert.pnbp,
                        "pay_date": insert.pay_date,
                        "attachment1": insert.attachment1,
                        "attachment2": insert.attachment2
                    },
                    audittrail_createdby='admin',
                    audittrail_createdtime=datetime.now(),
                    )
                if insertAuditTrail:
                    try:
                        insertAuditTrail.save()
                        return JSONResponse({"status": True, "message": "new Shipment has been created"}, status=status.HTTP_201_CREATED)
                    except(Exception)as e:
                        print('Exception',e)
                        pass        
                    return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
                return JSONResponse({"status": False, "message": "failed to create new Shipment"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            insert = Shipment(
                company_id=request.POST['company_id'],
                shipper_id=request.POST['shipper_id'],
                seller_id=request.POST['seller_id'],
                pol_id=request.POST['pol_id'],
                ppjk_id=request.POST['ppjk_id'],
                kppbc_id = request.POST['kppbc_id'],
                ship_no=request.POST['ship_no'],
                invpl_no=request.POST['invpl_no'],
                gen_desc=request.POST['gen_desc'],
                shipper_name=request.POST['shipper_name'],
                epc=request.POST['epc'],
                po_no=request.POST['po_no'],
                bl_no=request.POST['bl_no'],
                bl_date=request.POST['bl_date'],
                etd_date = request.POST['etd_date'],
                inv_date=request.POST['inv_date'],
                inv_uni=request.POST['inv_uni'],
                inv_term=request.POST['inv_term'],
                inv_curr=request.POST['inv_curr'],
                inv_amo=request.POST['inv_amo'],
                inv_qty = request.POST['inv_qty'],
                pod_name=request.POST['pod_name'],
                vessel_flight=request.POST['vessel_flight'],
                eta_date=request.POST['eta_date'],
                no_pkg=request.POST['no_pkg'],
                type=request.POST['type'],
                ata_date=request.POST['ata_date'],
                no_cntr=request.POST['no_cntr'],
                sppb_date=request.POST['sppb_date'],
                tgross_kgs = request.POST['tgross_kgs'],
                site_date=request.POST['site_date'],
                cipl_rcvdate=request.POST['cipl_rcvdate'],
                photo_rcvdate=request.POST['photo_rcvdate'],
                bl_rcvdate=request.POST['bl_rcvdate'],
                co_rcvdate=request.POST['co_rcvdate'],
                co_no = request.POST['co_no'],
                dpib_rcvdate=request.POST['dpib_rcvdate'],
                pibaju_no=request.POST['pibaju_no'],
                skbppn_initdate=request.POST['skbppn_initdate'],
                skbppn_signdate=request.POST['skbppn_signdate'],
                skbppn_subdate=request.POST['skbppn_subdate'],
                skbppn_rcvdate=request.POST['skbppn_rcvdate'],
                skbppn_dlvdate=request.POST['skbppn_dlvdate'],
                rcv_by=request.POST['rcv_by'],
                skbpph_initdate=request.POST['skbppn_initdate'],
                skbpph_signdate=request.POST['skbppn_signdate'],
                skbpph_subdate=request.POST['skbppn_subdate'],
                skbpph_rcvdate=request.POST['skbppn_rcvdate'],
                skbpph_dlvdate=request.POST['skbppn_dlvdate'],
                custdoc_initdate=request.POST['custdoc_initdate'],
                custdoc_signdate = request.POST['custdoc_signdate'],
                custdoc_dlvdate=request.POST['custdoc_dlvdate'],
                ltrreffkpp_no=request.POST['ltrreffkpp_no'],
                ltrreffppjk_no=request.POST['ltrreffppjk_no'],
                ltrreffbc_no=request.POST['ltrreffbc_no'],
                ins_no=request.POST['ins_no'],
                pib_submit_date=request.POST['pib_submit_date'],
                kode_bill=request.POST['kode_bill'],
                ntpn=request.POST['ntpn'],
                pibreg_date=request.POST['pibreg_date'],
                pibreg_no=request.POST['pibreg_no'],
                spjkm=request.POST['spjkm'],
                sppb_no=request.POST['sppb_no'],
                bm=request.POST['bm'],
                ppn=request.POST['ppn'],
                ppnbm = request.POST['ppnbm'],
                pph=request.POST['pph'],
                denda=request.POST['denda'],
                pnbp=request.POST['pnbp'],
                pay_date=request.POST['pay_date'],
                )

            if insert:
                try:
                    insert.save()
                except(Exception)as e:
                    print('Exception',e)
                    pass
            insert_detail = Shipment_Detail(
                header_id=insert.shipment_id,
                kmk_no=request.POST['kmk_no'],
                kmk_item_no=request.POST['kmk_item_no'],
                kmk_itemm_sub=request.POST['kmk_itemm_sub'],
                pib_desc=request.POST['pib_desc'],
            )

            if insert_detail:
                try:
                    insert_detail.save()
                except(Exception)as e:
                    print('Exception',e)
                    pass

            insertAuditTrail = AuditTrail(
                audittrail_transname = 'Shipment',
                audittrail_transid= insert.shipment_id,
                audittrail_action= 'Create',
                audittrail_content= {
                    "shipment_id": insert.shipment_id,
                    "company_id": insert.company_id,
                    "shipper_id": insert.shipper_id,
                    "seller_id": insert.seller_id,
                    "pol_id": insert.pol_id,
                    "ppjk_id": insert.ppjk_id,
                    "kppbc_id": insert.kppbc_id,
                    "ship_no": insert.ship_no,
                    "invpl_no": insert.invpl_no,
                    "gen_desc": insert.gen_desc,
                    "shipper_name": insert.shipper_name,
                    "epc": insert.epc,
                    "po_no": insert.po_no,
                    "bl_no": insert.bl_no,
                    "bl_date": insert.bl_date,
                    "etd_date": insert.etd_date,
                    "inv_date": insert.inv_date,
                    "inv_uni": insert.inv_uni,
                    "inv_term": insert.inv_term,
                    "inv_curr": insert.inv_curr,
                    "inv_amo": insert.inv_amo,
                    "inv_qty": insert.inv_qty,
                    "pod_name": insert.pod_name,
                    "vessel_flight": insert.vessel_flight,
                    "eta_date": insert.eta_date,
                    "no_pkg": insert.no_pkg,
                    "type": insert.type,
                    "ata_date": insert.ata_date,
                    "no_cntr": insert.no_cntr,
                    "sppb_date": insert.sppb_date,
                    "tgross_kgs": insert.tgross_kgs,
                    "site_date": insert.site_date,
                    "cipl_rcvdate": insert.cipl_rcvdate,
                    "photo_rcvdate": insert.photo_rcvdate,
                    "bl_rcvdate": insert.bl_rcvdate,
                    "co_rcvdate": insert.co_rcvdate,
                    "co_no": insert.co_no,
                    "dpib_rcvdate": insert.dpib_rcvdate,
                    "pibaju_no": insert.pibaju_no,
                    "skbppn_initdate": insert.skbppn_initdate,
                    "skbppn_signdate": insert.skbppn_signdate,
                    "skbppn_subdate": insert.skbppn_subdate,
                    "skbppn_rcvdate": insert.skbppn_rcvdate,
                    "skbppn_dlvdate": insert.skbppn_dlvdate,
                    "rcv_by": insert.rcv_by,
                    "skbpph_initdate": insert.skbpph_initdate,
                    "skbpph_signdate": insert.skbpph_signdate,
                    "skbpph_subdate": insert.skbpph_subdate,
                    "skbpph_rcvdate": insert.skbpph_rcvdate,
                    "skbpph_dlvdate": insert.skbpph_dlvdate,
                    "custdoc_initdate": insert.custdoc_initdate,
                    "custdoc_signdate": insert.custdoc_signdate,
                    "custdoc_dlvdate": insert.custdoc_dlvdate,
                    "ltrreffkpp_no": insert.ltrreffkpp_no,
                    "ltrreffppjk_no": insert.ltrreffppjk_no,
                    "ltrreffbc_no": insert.ltrreffbc_no,
                    "ins_no": insert.ins_no,
                    "pib_submit_date": insert.pib_submit_date,
                    "kode_bill": insert.kode_bill,
                    "ntpn": insert.ntpn,
                    "pibreg_date": insert.pibreg_date,
                    "pibreg_no": insert.pibreg_no,
                    "spjkm": insert.spjkm,
                    "sppb_no": insert.sppb_no,
                    "bm": insert.bm,
                    "ppn": insert.ppn,
                    "ppnbm": insert.ppnbm,
                    "pph": insert.pph,
                    "denda": insert.denda,
                    "pnbp": insert.pnbp,
                    "pay_date": insert.pay_date,
                    "attachment1": insert.attachment1,
                    "attachment2": insert.attachment2
                },
                audittrail_createdby='admin',
                audittrail_createdtime=datetime.now(),
            )

            if insertAuditTrail:
                try:
                    insertAuditTrail.save()
                    return JSONResponse({"status": True, "message": "new Shipment has been created"}, status=status.HTTP_201_CREATED)
                except(Exception)as e:
                    print('Exception',e)
                    pass        
                return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
            return JSONResponse({"status": False, "message": "failed to create new Shipment"}, status=status.HTTP_400_BAD_REQUEST)        
        
def update_shipment(request, update_shipment_id,update_shipment_detail_id):
    ubah_shipment = Shipment.objects.get(shipment_id=update_shipment_id)
    ubah_detail = Shipment_Detail.objects.get(header_id=update_shipment_id, shipment_detail_id=update_shipment_detail_id)

    if request.method == 'POST':
        if len(request.FILES) != 0:
            attachment1_path = str(ubah_shipment.attachment1)
            attachment2_path = str(ubah_shipment.attachment2)
            #ubah shipment 
            ubah_shipment.company_id=request.POST['company_id']
            ubah_shipment.shipper_id=request.POST['shipper_id']
            ubah_shipment.seller_id=request.POST['seller_id']
            ubah_shipment.pol_id=request.POST['pol_id']
            ubah_shipment.ppjk_id=request.POST['ppjk_id']
            ubah_shipment.kppbc_id = request.POST['kppbc_id']
            ubah_shipment.ship_no=request.POST['ship_no']
            ubah_shipment.invpl_no=request.POST['invpl_no']
            ubah_shipment.gen_desc=request.POST['gen_desc']
            ubah_shipment.shipper_name=request.POST['shipper_name']
            ubah_shipment.epc=request.POST['epc']
            ubah_shipment.po_no=request.POST['po_no']
            ubah_shipment.bl_no=request.POST['bl_no']
            ubah_shipment.bl_date=request.POST['bl_date']
            ubah_shipment.etd_date = request.POST['etd_date']
            ubah_shipment.inv_date=request.POST['inv_date']
            ubah_shipment.inv_uni=request.POST['inv_uni']
            ubah_shipment.inv_term=request.POST['inv_term']
            ubah_shipment.inv_curr=request.POST['inv_curr']
            ubah_shipment.inv_amo=request.POST['inv_amo']
            ubah_shipment.inv_qty = request.POST['inv_qty']
            ubah_shipment.pod_name=request.POST['pod_name']
            ubah_shipment.vessel_flight=request.POST['vessel_flight']
            ubah_shipment.eta_date=request.POST['eta_date']
            ubah_shipment.no_pkg=request.POST['no_pkg']
            ubah_shipment.type=request.POST['type']
            ubah_shipment.ata_date=request.POST['ata_date']
            ubah_shipment.no_cntr=request.POST['no_cntr']
            ubah_shipment.sppb_date=request.POST['sppb_date']
            ubah_shipment.tgross_kgs = request.POST['tgross_kgs']
            ubah_shipment.site_date=request.POST['site_date']
            ubah_shipment.cipl_rcvdate=request.POST['cipl_rcvdate']
            ubah_shipment.photo_rcvdate=request.POST['photo_rcvdate']
            ubah_shipment.bl_rcvdate=request.POST['bl_rcvdate']
            ubah_shipment.co_rcvdate=request.POST['co_rcvdate']
            ubah_shipment.co_no = request.POST['co_no']
            ubah_shipment.dpib_rcvdate=request.POST['dpib_rcvdate']
            ubah_shipment.pibaju_no=request.POST['pibaju_no']
            ubah_shipment.skbppn_initdate=request.POST['skbppn_initdate']
            ubah_shipment.skbppn_signdate=request.POST['skbppn_signdate']
            ubah_shipment.skbppn_subdate=request.POST['skbppn_subdate']
            ubah_shipment.skbppn_rcvdate=request.POST['skbppn_rcvdate']
            ubah_shipment.skbppn_dlvdate=request.POST['skbppn_dlvdate']
            ubah_shipment.rcv_by=request.POST['rcv_by']
            ubah_shipment.skbpph_initdate=request.POST['skbppn_initdate']
            ubah_shipment.skbpph_signdate=request.POST['skbppn_signdate']
            ubah_shipment.skbpph_subdate=request.POST['skbppn_subdate']
            ubah_shipment.skbpph_rcvdate=request.POST['skbppn_rcvdate']
            ubah_shipment.skbpph_dlvdate=request.POST['skbppn_dlvdate']
            ubah_shipment.custdoc_initdate=request.POST['custdoc_initdate']
            ubah_shipment.custdoc_signdate = request.POST['custdoc_signdate']
            ubah_shipment.custdoc_dlvdate=request.POST['custdoc_dlvdate']
            ubah_shipment.ltrreffkpp_no=request.POST['ltrreffkpp_no']
            ubah_shipment.ltrreffppjk_no=request.POST['ltrreffppjk_no']
            ubah_shipment.ltrreffbc_no=request.POST['ltrreffbc_no']
            ubah_shipment.ins_no=request.POST['ins_no']
            ubah_shipment.pib_submit_date=request.POST['pib_submit_date']
            ubah_shipment.kode_bill=request.POST['kode_bill']
            ubah_shipment.ntpn=request.POST['ntpn']
            ubah_shipment.pibreg_date=request.POST['pibreg_date']
            ubah_shipment.pibreg_no=request.POST['pibreg_no']
            ubah_shipment.spjkm=request.POST['spjkm']
            ubah_shipment.sppb_no=request.POST['sppb_no']
            ubah_shipment.bm=request.POST['bm']
            ubah_shipment.ppn=request.POST['ppn']
            ubah_shipment.ppnbm = request.POST['ppnbm']
            ubah_shipment.pph=request.POST['pph']
            ubah_shipment.denda=request.POST['denda']
            ubah_shipment.pnbp=request.POST['pnbp']
            ubah_shipment.pay_date=request.POST['pay_date']
            ubah_shipment.attachment1=request.FILES['attachment1']
            ubah_shipment.attachment2=request.FILES['attachment2']	

            #ubah detail
            ubah_detail.kmk_no = request.POST['kmk_no_old']
            ubah_detail.kmk_item_no = request.POST['kmk_item_no_lama']
            ubah_detail.kmk_itemm_sub = request.POST['kmk_itemm_sub_lama']
            ubah_detail.pib_desc = request.POST['pib_desc_lama']

            #tambah detail
            insert_detail = Shipment_Detail(
                header_id = ubah_shipment.shipment_id,
                kmk_no=request.POST['kmk_no_new'],
                kmk_item_no=request.POST['kmk_item_no_baru'],
                kmk_itemm_sub=request.POST['kmk_itemm_sub_baru'],
                pib_desc=request.POST['pib_desc_baru'],
            )

            if attachment1_path !='' and attachment2_path != '':
                try:
                    os.unlink(attachment1_path)
                    os.unlink(attachment2_path)
                except(Exception)as e:
                    print('Exception',e)
                    pass

            if ubah_shipment:
                try:
                    ubah_shipment.save()
                except(Exception)as e:
                    print('Exception',e)
                    pass

            if request.POST['kmk_no_new'] != '':
                if insert_detail:
                    try:
                        insert_detail.save()
                    except(Exception)as e:
                        print('Exception',e)
                        pass
                if ubah_detail:
                    try:
                        ubah_detail.save()
                    except(Exception)as e:
                        print('Exception',e)
                        pass
            else:
                if ubah_detail:
                    try:
                        ubah_detail.save()
                    except(Exception)as e:
                        print('Exception',e)
                        pass

            insertAuditTrail = AuditTrail(
                audittrail_transname = 'Shipment',
                audittrail_transid= ubah_shipment.shipment_id,
                audittrail_action= 'Update',
                audittrail_content= {
                    "shipment_id": ubah_shipment.shipment_id,
                    "company_id": ubah_shipment.company_id,
                    "shipper_id": ubah_shipment.shipper_id,
                    "seller_id": ubah_shipment.seller_id,
                    "pol_id": ubah_shipment.pol_id,
                    "ppjk_id": ubah_shipment.ppjk_id,
                    "kppbc_id": ubah_shipment.kppbc_id,
                    "ship_no": ubah_shipment.ship_no,
                    "invpl_no": ubah_shipment.invpl_no,
                    "gen_desc": ubah_shipment.gen_desc,
                    "shipper_name": ubah_shipment.shipper_name,
                    "epc": ubah_shipment.epc,
                    "po_no": ubah_shipment.po_no,
                    "bl_no": ubah_shipment.bl_no,
                    "bl_date": ubah_shipment.bl_date,
                    "etd_date": ubah_shipment.etd_date,
                    "inv_date": ubah_shipment.inv_date,
                    "inv_uni": ubah_shipment.inv_uni,
                    "inv_term": ubah_shipment.inv_term,
                    "inv_curr": ubah_shipment.inv_curr,
                    "inv_amo": ubah_shipment.inv_amo,
                    "inv_qty": ubah_shipment.inv_qty,
                    "pod_name": ubah_shipment.pod_name,
                    "vessel_flight": ubah_shipment.vessel_flight,
                    "eta_date": ubah_shipment.eta_date,
                    "no_pkg": ubah_shipment.no_pkg,
                    "type": ubah_shipment.type,
                    "ata_date": ubah_shipment.ata_date,
                    "no_cntr": ubah_shipment.no_cntr,
                    "sppb_date": ubah_shipment.sppb_date,
                    "tgross_kgs": ubah_shipment.tgross_kgs,
                    "site_date": ubah_shipment.site_date,
                    "cipl_rcvdate": ubah_shipment.cipl_rcvdate,
                    "photo_rcvdate": ubah_shipment.photo_rcvdate,
                    "bl_rcvdate": ubah_shipment.bl_rcvdate,
                    "co_rcvdate": ubah_shipment.co_rcvdate,
                    "co_no": ubah_shipment.co_no,
                    "dpib_rcvdate": ubah_shipment.dpib_rcvdate,
                    "pibaju_no": ubah_shipment.pibaju_no,
                    "skbppn_initdate": ubah_shipment.skbppn_initdate,
                    "skbppn_signdate": ubah_shipment.skbppn_signdate,
                    "skbppn_subdate": ubah_shipment.skbppn_subdate,
                    "skbppn_rcvdate": ubah_shipment.skbppn_rcvdate,
                    "skbppn_dlvdate": ubah_shipment.skbppn_dlvdate,
                    "rcv_by": ubah_shipment.rcv_by,
                    "skbpph_initdate": ubah_shipment.skbpph_initdate,
                    "skbpph_signdate": ubah_shipment.skbpph_signdate,
                    "skbpph_subdate": ubah_shipment.skbpph_subdate,
                    "skbpph_rcvdate": ubah_shipment.skbpph_rcvdate,
                    "skbpph_dlvdate": ubah_shipment.skbpph_dlvdate,
                    "custdoc_initdate": ubah_shipment.custdoc_initdate,
                    "custdoc_signdate": ubah_shipment.custdoc_signdate,
                    "custdoc_dlvdate": ubah_shipment.custdoc_dlvdate,
                    "ltrreffkpp_no": ubah_shipment.ltrreffkpp_no,
                    "ltrreffppjk_no": ubah_shipment.ltrreffppjk_no,
                    "ltrreffbc_no": ubah_shipment.ltrreffbc_no,
                    "ins_no": ubah_shipment.ins_no,
                    "pib_submit_date": ubah_shipment.pib_submit_date,
                    "kode_bill": ubah_shipment.kode_bill,
                    "ntpn": ubah_shipment.ntpn,
                    "pibreg_date": ubah_shipment.pibreg_date,
                    "pibreg_no": ubah_shipment.pibreg_no,
                    "spjkm": ubah_shipment.spjkm,
                    "sppb_no": ubah_shipment.sppb_no,
                    "bm": ubah_shipment.bm,
                    "ppn": ubah_shipment.ppn,
                    "ppnbm": ubah_shipment.ppnbm,
                    "pph": ubah_shipment.pph,
                    "denda": ubah_shipment.denda,
                    "pnbp": ubah_shipment.pnbp,
                    "pay_date": ubah_shipment.pay_date,
                    "attachment1": ubah_shipment.attachment1,
                    "attachment2": ubah_shipment.attachment2
                },
                audittrail_createdby='admin',
                audittrail_createdtime=datetime.now(),
                )
            if insertAuditTrail:
                try:
                    insertAuditTrail.save()
                    return JSONResponse({"status": True, "message": "Shipment has been updated"}, status=status.HTTP_201_CREATED)
                except(Exception)as e:
                    print('Exception',e)
                    pass        
                return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
            return JSONResponse({"status": False, "message": "failed to update Shipment"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            ubah_shipment = Shipment.objects.get(shipment_id=update_shipment_id)
            ubah_detail = Shipment_Detail.objects.get(header_id=update_shipment_id, shipment_detail_id=update_shipment_detail_id)
            
            #ubah shipment 
            ubah_shipment.company_id=request.POST['company_id']
            ubah_shipment.shipper_id=request.POST['shipper_id']
            ubah_shipment.seller_id=request.POST['seller_id']
            ubah_shipment.pol_id=request.POST['pol_id']
            ubah_shipment.ppjk_id=request.POST['ppjk_id']
            ubah_shipment.kppbc_id = request.POST['kppbc_id']
            ubah_shipment.ship_no=request.POST['ship_no']
            ubah_shipment.invpl_no=request.POST['invpl_no']
            ubah_shipment.gen_desc=request.POST['gen_desc']
            ubah_shipment.shipper_name=request.POST['shipper_name']
            ubah_shipment.epc=request.POST['epc']
            ubah_shipment.po_no=request.POST['po_no']
            ubah_shipment.bl_no=request.POST['bl_no']
            ubah_shipment.bl_date=request.POST['bl_date']
            ubah_shipment.etd_date = request.POST['etd_date']
            ubah_shipment.inv_date=request.POST['inv_date']
            ubah_shipment.inv_uni=request.POST['inv_uni']
            ubah_shipment.inv_term=request.POST['inv_term']
            ubah_shipment.inv_curr=request.POST['inv_curr']
            ubah_shipment.inv_amo=request.POST['inv_amo']
            ubah_shipment.inv_qty = request.POST['inv_qty']
            ubah_shipment.pod_name=request.POST['pod_name']
            ubah_shipment.vessel_flight=request.POST['vessel_flight']
            ubah_shipment.eta_date=request.POST['eta_date']
            ubah_shipment.no_pkg=request.POST['no_pkg']
            ubah_shipment.type=request.POST['type']
            ubah_shipment.ata_date=request.POST['ata_date']
            ubah_shipment.no_cntr=request.POST['no_cntr']
            ubah_shipment.sppb_date=request.POST['sppb_date']
            ubah_shipment.tgross_kgs = request.POST['tgross_kgs']
            ubah_shipment.site_date=request.POST['site_date']
            ubah_shipment.cipl_rcvdate=request.POST['cipl_rcvdate']
            ubah_shipment.photo_rcvdate=request.POST['photo_rcvdate']
            ubah_shipment.bl_rcvdate=request.POST['bl_rcvdate']
            ubah_shipment.co_rcvdate=request.POST['co_rcvdate']
            ubah_shipment.co_no = request.POST['co_no']
            ubah_shipment.dpib_rcvdate=request.POST['dpib_rcvdate']
            ubah_shipment.pibaju_no=request.POST['pibaju_no']
            ubah_shipment.skbppn_initdate=request.POST['skbppn_initdate']
            ubah_shipment.skbppn_signdate=request.POST['skbppn_signdate']
            ubah_shipment.skbppn_subdate=request.POST['skbppn_subdate']
            ubah_shipment.skbppn_rcvdate=request.POST['skbppn_rcvdate']
            ubah_shipment.skbppn_dlvdate=request.POST['skbppn_dlvdate']
            ubah_shipment.rcv_by=request.POST['rcv_by']
            ubah_shipment.skbpph_initdate=request.POST['skbppn_initdate']
            ubah_shipment.skbpph_signdate=request.POST['skbppn_signdate']
            ubah_shipment.skbpph_subdate=request.POST['skbppn_subdate']
            ubah_shipment.skbpph_rcvdate=request.POST['skbppn_rcvdate']
            ubah_shipment.skbpph_dlvdate=request.POST['skbppn_dlvdate']
            ubah_shipment.custdoc_initdate=request.POST['custdoc_initdate']
            ubah_shipment.custdoc_signdate = request.POST['custdoc_signdate']
            ubah_shipment.custdoc_dlvdate=request.POST['custdoc_dlvdate']
            ubah_shipment.ltrreffkpp_no=request.POST['ltrreffkpp_no']
            ubah_shipment.ltrreffppjk_no=request.POST['ltrreffppjk_no']
            ubah_shipment.ltrreffbc_no=request.POST['ltrreffbc_no']
            ubah_shipment.ins_no=request.POST['ins_no']
            ubah_shipment.pib_submit_date=request.POST['pib_submit_date']
            ubah_shipment.kode_bill=request.POST['kode_bill']
            ubah_shipment.ntpn=request.POST['ntpn']
            ubah_shipment.pibreg_date=request.POST['pibreg_date']
            ubah_shipment.pibreg_no=request.POST['pibreg_no']
            ubah_shipment.spjkm=request.POST['spjkm']
            ubah_shipment.sppb_no=request.POST['sppb_no']
            ubah_shipment.bm=request.POST['bm']
            ubah_shipment.ppn=request.POST['ppn']
            ubah_shipment.ppnbm = request.POST['ppnbm']
            ubah_shipment.pph=request.POST['pph']
            ubah_shipment.denda=request.POST['denda']
            ubah_shipment.pnbp=request.POST['pnbp']
            ubah_shipment.pay_date=request.POST['pay_date']
            ubah_shipment.attachment1=request.POST['attachment1']
            ubah_shipment.attachment2=request.POST['attachment2']	

            #ubah detail
            ubah_detail.kmk_no = request.POST['kmk_no_old']
            ubah_detail.kmk_item_no = request.POST['kmk_item_no_lama']
            ubah_detail.kmk_itemm_sub = request.POST['kmk_itemm_sub_lama']
            ubah_detail.pib_desc = request.POST['pib_desc_lama']

            #tambah detail
            insert_detail = Shipment_Detail(
                header_id = ubah_shipment.shipment_id,
                kmk_no=request.POST['kmk_no_new'],
                kmk_item_no=request.POST['kmk_item_no_baru'],
                kmk_itemm_sub=request.POST['kmk_itemm_sub_baru'],
                pib_desc=request.POST['pib_desc_baru'],
            )


            if ubah_shipment:
                try:
                    ubah_shipment.save()
                except(Exception)as e:
                    print('Exception',e)
                    pass

            if request.POST['kmk_no_new'] != '':
                if insert_detail:
                    try:
                        insert_detail.save()
                    except(Exception)as e:
                        print('Exception',e)
                        pass
                if ubah_detail:
                    try:
                        ubah_detail.save()
                    except(Exception)as e:
                        print('Exception',e)
                        pass
            else:
                if ubah_detail:
                    try:
                        ubah_detail.save()
                    except(Exception)as e:
                        print('Exception',e)
                        pass

            insertAuditTrail = AuditTrail(
                audittrail_transname = 'Shipment',
                audittrail_transid= ubah_shipment.shipment_id,
                audittrail_action= 'Update',
                audittrail_content= {
                    "shipment_id": ubah_shipment.shipment_id,
                    "company_id": ubah_shipment.company_id,
                    "shipper_id": ubah_shipment.shipper_id,
                    "seller_id": ubah_shipment.seller_id,
                    "pol_id": ubah_shipment.pol_id,
                    "ppjk_id": ubah_shipment.ppjk_id,
                    "kppbc_id": ubah_shipment.kppbc_id,
                    "ship_no": ubah_shipment.ship_no,
                    "invpl_no": ubah_shipment.invpl_no,
                    "gen_desc": ubah_shipment.gen_desc,
                    "shipper_name": ubah_shipment.shipper_name,
                    "epc": ubah_shipment.epc,
                    "po_no": ubah_shipment.po_no,
                    "bl_no": ubah_shipment.bl_no,
                    "bl_date": ubah_shipment.bl_date,
                    "etd_date": ubah_shipment.etd_date,
                    "inv_date": ubah_shipment.inv_date,
                    "inv_uni": ubah_shipment.inv_uni,
                    "inv_term": ubah_shipment.inv_term,
                    "inv_curr": ubah_shipment.inv_curr,
                    "inv_amo": ubah_shipment.inv_amo,
                    "inv_qty": ubah_shipment.inv_qty,
                    "pod_name": ubah_shipment.pod_name,
                    "vessel_flight": ubah_shipment.vessel_flight,
                    "eta_date": ubah_shipment.eta_date,
                    "no_pkg": ubah_shipment.no_pkg,
                    "type": ubah_shipment.type,
                    "ata_date": ubah_shipment.ata_date,
                    "no_cntr": ubah_shipment.no_cntr,
                    "sppb_date": ubah_shipment.sppb_date,
                    "tgross_kgs": ubah_shipment.tgross_kgs,
                    "site_date": ubah_shipment.site_date,
                    "cipl_rcvdate": ubah_shipment.cipl_rcvdate,
                    "photo_rcvdate": ubah_shipment.photo_rcvdate,
                    "bl_rcvdate": ubah_shipment.bl_rcvdate,
                    "co_rcvdate": ubah_shipment.co_rcvdate,
                    "co_no": ubah_shipment.co_no,
                    "dpib_rcvdate": ubah_shipment.dpib_rcvdate,
                    "pibaju_no": ubah_shipment.pibaju_no,
                    "skbppn_initdate": ubah_shipment.skbppn_initdate,
                    "skbppn_signdate": ubah_shipment.skbppn_signdate,
                    "skbppn_subdate": ubah_shipment.skbppn_subdate,
                    "skbppn_rcvdate": ubah_shipment.skbppn_rcvdate,
                    "skbppn_dlvdate": ubah_shipment.skbppn_dlvdate,
                    "rcv_by": ubah_shipment.rcv_by,
                    "skbpph_initdate": ubah_shipment.skbpph_initdate,
                    "skbpph_signdate": ubah_shipment.skbpph_signdate,
                    "skbpph_subdate": ubah_shipment.skbpph_subdate,
                    "skbpph_rcvdate": ubah_shipment.skbpph_rcvdate,
                    "skbpph_dlvdate": ubah_shipment.skbpph_dlvdate,
                    "custdoc_initdate": ubah_shipment.custdoc_initdate,
                    "custdoc_signdate": ubah_shipment.custdoc_signdate,
                    "custdoc_dlvdate": ubah_shipment.custdoc_dlvdate,
                    "ltrreffkpp_no": ubah_shipment.ltrreffkpp_no,
                    "ltrreffppjk_no": ubah_shipment.ltrreffppjk_no,
                    "ltrreffbc_no": ubah_shipment.ltrreffbc_no,
                    "ins_no": ubah_shipment.ins_no,
                    "pib_submit_date": ubah_shipment.pib_submit_date,
                    "kode_bill": ubah_shipment.kode_bill,
                    "ntpn": ubah_shipment.ntpn,
                    "pibreg_date": ubah_shipment.pibreg_date,
                    "pibreg_no": ubah_shipment.pibreg_no,
                    "spjkm": ubah_shipment.spjkm,
                    "sppb_no": ubah_shipment.sppb_no,
                    "bm": ubah_shipment.bm,
                    "ppn": ubah_shipment.ppn,
                    "ppnbm": ubah_shipment.ppnbm,
                    "pph": ubah_shipment.pph,
                    "denda": ubah_shipment.denda,
                    "pnbp": ubah_shipment.pnbp,
                    "pay_date": ubah_shipment.pay_date,
                    "attachment1": ubah_shipment.attachment1,
                    "attachment2": ubah_shipment.attachment2
                },
                audittrail_createdby='admin',
                audittrail_createdtime=datetime.now(),
                )
            if insertAuditTrail:
                try:
                    insertAuditTrail.save()
                    return JSONResponse({"status": True, "message": "Shipment has been updated"}, status=status.HTTP_201_CREATED)
                except(Exception)as e:
                    print('Exception',e)
                    pass        
                return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
            return JSONResponse({"status": False, "message": "failed to update Shipment"}, status=status.HTTP_400_BAD_REQUEST)

def delete_shipment(request, delete_id):
    hapus = Shipment.objects.get(shipment_id=delete_id)
    hapus_detail = Shipment_Detail.objects.filter(header_id=delete_id)
    if request.method == 'GET':
        attachment1_path = str(hapus.attachment1)
        attachment2_path = str(hapus.attachment2)

        insertAuditTrail = AuditTrail(
            audittrail_transname = 'Shipment',
            audittrail_transid= hapus.shipment_id,
            audittrail_action= 'Delete',
            audittrail_content= {
                "shipment_id": hapus.shipment_id,
                "company_id": hapus.company_id,
                "shipper_id": hapus.shipper_id,
                "seller_id": hapus.seller_id,
                "pol_id": hapus.pol_id,
                "ppjk_id": hapus.ppjk_id,
                "kppbc_id": hapus.kppbc_id,
                "ship_no": hapus.ship_no,
                "invpl_no": hapus.invpl_no,
                "gen_desc": hapus.gen_desc,
                "shipper_name": hapus.shipper_name,
                "epc": hapus.epc,
                "po_no": hapus.po_no,
                "bl_no": hapus.bl_no,
                "bl_date": hapus.bl_date,
                "etd_date": hapus.etd_date,
                "inv_date": hapus.inv_date,
                "inv_uni": hapus.inv_uni,
                "inv_term": hapus.inv_term,
                "inv_curr": hapus.inv_curr,
                "inv_amo": hapus.inv_amo,
                "inv_qty": hapus.inv_qty,
                "pod_name": hapus.pod_name,
                "vessel_flight": hapus.vessel_flight,
                "eta_date": hapus.eta_date,
                "no_pkg": hapus.no_pkg,
                "type": hapus.type,
                "ata_date": hapus.ata_date,
                "no_cntr": hapus.no_cntr,
                "sppb_date": hapus.sppb_date,
                "tgross_kgs": hapus.tgross_kgs,
                "site_date": hapus.site_date,
                "cipl_rcvdate": hapus.cipl_rcvdate,
                "photo_rcvdate": hapus.photo_rcvdate,
                "bl_rcvdate": hapus.bl_rcvdate,
                "co_rcvdate": hapus.co_rcvdate,
                "co_no": hapus.co_no,
                "dpib_rcvdate": hapus.dpib_rcvdate,
                "pibaju_no": hapus.pibaju_no,
                "skbppn_initdate": hapus.skbppn_initdate,
                "skbppn_signdate": hapus.skbppn_signdate,
                "skbppn_subdate": hapus.skbppn_subdate,
                "skbppn_rcvdate": hapus.skbppn_rcvdate,
                "skbppn_dlvdate": hapus.skbppn_dlvdate,
                "rcv_by": hapus.rcv_by,
                "skbpph_initdate": hapus.skbpph_initdate,
                "skbpph_signdate": hapus.skbpph_signdate,
                "skbpph_subdate": hapus.skbpph_subdate,
                "skbpph_rcvdate": hapus.skbpph_rcvdate,
                "skbpph_dlvdate": hapus.skbpph_dlvdate,
                "custdoc_initdate": hapus.custdoc_initdate,
                "custdoc_signdate": hapus.custdoc_signdate,
                "custdoc_dlvdate": hapus.custdoc_dlvdate,
                "ltrreffkpp_no": hapus.ltrreffkpp_no,
                "ltrreffppjk_no": hapus.ltrreffppjk_no,
                "ltrreffbc_no": hapus.ltrreffbc_no,
                "ins_no": hapus.ins_no,
                "pib_submit_date": hapus.pib_submit_date,
                "kode_bill": hapus.kode_bill,
                "ntpn": hapus.ntpn,
                "pibreg_date": hapus.pibreg_date,
                "pibreg_no": hapus.pibreg_no,
                "spjkm": hapus.spjkm,
                "sppb_no": hapus.sppb_no,
                "bm": hapus.bm,
                "ppn": hapus.ppn,
                "ppnbm": hapus.ppnbm,
                "pph": hapus.pph,
                "denda": hapus.denda,
                "pnbp": hapus.pnbp,
                "pay_date": hapus.pay_date,
                "attachment1": hapus.attachment1,
                "attachment2": hapus.attachment2
            },
            audittrail_createdby='admin',
            audittrail_createdtime=datetime.now(),
            )

        if insertAuditTrail:
            try:
                insertAuditTrail.save()
            except(Exception)as e:
                print('Exception',e)
                pass

        if hapus_detail:
            try:
                hapus_detail.delete()
            except(Exception)as e:
                print('Exception',e)
                pass

        if attachment1_path !='' and attachment2_path != '':
            try:
                os.unlink(attachment1_path)
                os.unlink(attachment2_path)
            except(Exception)as e:
                print('Exception',e)
                pass
        
        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "Shipment has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete Shipment"}, status=status.HTTP_400_BAD_REQUEST)

##shipment_detail
def retrieve_shipment_detail(request):
    if request.method == 'GET': 
        products = Shipment_Detail.objects.all()
        serializer = Shipment_DetailSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Shipment_Detail"}, status=status.HTTP_400_BAD_REQUEST)

def retrievebyId_shipment_detail(request, get_id):
    if request.method == 'GET':
        products = Shipment_Detail.objects.filter(shipment_detail_id=get_id)
        serializer = Shipment_DetailSerializers(products, many=True)
        if products:
            return JSONResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return JSONResponse({"status": False, "message": "you don't have data Shipment_Detail"}, status=status.HTTP_400_BAD_REQUEST)
        
def create_shipment_detail(request):
    if request.method == 'POST':
        insert = Shipment_Detail(
            header_id = request.POST['header_id'],
            kmk_no=request.POST['kmk_no'],
            kmk_item_no=request.POST['kmk_item_no'],
            kmk_itemm_sub=request.POST['kmk_itemm_sub'],
            pib_desc=request.POST['pib_desc'],
        )

        if insert:
            try:
                insert.save()
                return JSONResponse({"status": True, "message": "new Shipment_Detail has been created"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to create new Shipment_Detail"}, status=status.HTTP_400_BAD_REQUEST)

def update_shipment_detail(request, update_id):
    if request.method == 'POST':
        ubah = Shipment_Detail.objects.filter(shipment_detail_id=update_id)

        if ubah:
            try:
                ubah.update(
                        header_id = request.POST['header_id'],
                        kmk_no=request.POST['kmk_no'],
                        kmk_item_no=request.POST['kmk_item_no'],
                        kmk_itemm_sub=request.POST['kmk_itemm_sub'],
                        pib_desc=request.POST['pib_desc'],
                    )
                return JSONResponse({"status": True, "message": "Shipment_Detail has been updated"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to update Shipment_Detail"}, status=status.HTTP_400_BAD_REQUEST)

def delete_shipment_detail(request, delete_id):
    if request.method == 'GET':
        hapus = Shipment_Detail.objects.filter(shipment_detail_id=delete_id)

        if hapus:
            try:
                hapus.delete()
                return JSONResponse({"status": True, "message": "Shipment_Detail has been deleted"}, status=status.HTTP_201_CREATED)
            except(Exception)as e:
                print('Exception',e)
                pass        
            return JSONResponse({"status": False, "message": "Bad String"}, status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({"status": False, "message": "failed to delete Shipment_Detail"}, status=status.HTTP_400_BAD_REQUEST)

def getNewEntries(request):
    if request.method == 'GET':
        c = connection.cursor()
        try:
            #call store procedure
            c.callproc('dashboard_get_newentries')
            data = c.fetchall()
            if data:
                return JSONResponse({"status": True, "data": data}, status=status.HTTP_200_OK)
            return JSONResponse({"status": False, "message": "you don't have new entries data"}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            c.close()

def getCount(request):
    if request.method == 'GET':
        c = connection.cursor()
        try:
            #call store procedure
            c.callproc('dashboard_get_count')
            data = c.fetchall()
            if data:
                return JSONResponse({"status": True, "data": data}, status=status.HTTP_200_OK)
            return JSONResponse({"status": False, "message": "you don't have count data"}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            c.close()