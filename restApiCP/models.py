from django.db import models

# Create your models here.
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=70, default=None)
    company_address1 = models.CharField(max_length=250,default=None)
    company_address2 = models.CharField(max_length=250,default=None)
    company_phone = models.CharField(max_length=12,default=None)
    company_fax = models.CharField(max_length=15,default=None)
    company_email = models.CharField(max_length=30,default=None)
    company_npwp = models.CharField(max_length=30,default=None)
    company_apip = models.CharField(max_length=25,default=None)
    company_nib = models.CharField(max_length=25,default=None)
    company_type = models.CharField(max_length=30,default=None)
    company_AccountNo = models.CharField(max_length=20,default=None)
    company_npwpDoc = models.FileField(upload_to='upload/perusahaan/npwp/', default=None)
    company_sppkpDoc = models.FileField(upload_to='upload/perusahaan/sppkp/', default=None)

    class Meta:
        managed = False
        db_table = 'Company'

class EmployeeOwner(models.Model):
    eo_id = models.AutoField(primary_key=True)
    eo_name = models.CharField(max_length=70,default=None)
    eo_address1 = models.CharField(max_length=250,default=None)
    eo_address2 = models.CharField(max_length=250,default=None)
    eo_phone = models.CharField(max_length=12,default=None)
    eo_nik = models.CharField(max_length=15,default=None)
    eo_email = models.CharField(max_length=30,default=None)
    eo_npwp = models.CharField(max_length=30,default=None)
    eo_position_id = models.IntegerField(default=None)
    eo_company_id = models.IntegerField(default=None)
    eo_nik_img = models.ImageField(upload_to='upload/employeeowner/nik/',default=None)
    eo_npwp_img = models.ImageField(upload_to='upload/employeeowner/npwp/',default=None)
    eo_oth_img = models.ImageField(upload_to='upload/employeeowner/oth/',default=None)

    class Meta:
        managed = False
        db_table = 'EmployeeOwner'

class Position(models.Model):
    position_id = models.AutoField(primary_key=True)
    position_name = models.CharField(max_length=70,default=None)

    class Meta:
        managed = False
        db_table = 'Position'

class CostType(models.Model):
    costtype_id = models.AutoField(primary_key=True)
    costtype_code = models.CharField(max_length=10, default=None)
    costtype_name = models.CharField(max_length=70, default=None)

    class Meta:
        managed = False
        db_table = 'CostType'

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_code = models.CharField(max_length=10,default=None)
    country_codecode = models.CharField(max_length=10,default=None)
    country_name = models.CharField(max_length=70,default=None)

    class Meta:
        managed = False
        db_table = 'Country'

class FreightCost(models.Model):
    freightcost_id = models.AutoField(primary_key=True)
    region_id = models.IntegerField(default=None)
    costtype_id = models.IntegerField(default=None)
    tracktype_id = models.IntegerField(default=None)
    amount = models.DecimalField(max_digits=18, decimal_places=3,default=None)


    class Meta:
        managed = False
        db_table = 'FreightCost'

class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_code = models.CharField(max_length=10,default=None)
    region_name = models.CharField(max_length=70,default=None)

    class Meta:
        managed = False
        db_table = 'Region'

class TrackType(models.Model):
    tracktype_id = models.AutoField(primary_key=True)
    tracktype_code = models.CharField(max_length=10,default=None)
    tracktype_name = models.CharField(max_length=70,default=None)

    class Meta:
        managed = False
        db_table = 'TrackType'

class Unit(models.Model):
    unit_id = models.AutoField(primary_key=True)
    unit_code = models.CharField(max_length=10,default=None)
    unit_name = models.CharField(max_length=70,default=None)

    class Meta:
        managed = False
        db_table = 'Unit'

class PortOFLoad(models.Model):
    portofload_id = models.AutoField(primary_key=True)
    portofload_code = models.CharField(max_length=10,default=None)
    portofload_name = models.CharField(max_length=70,default=None)

    class Meta:
        managed = False
        db_table = 'PortOFLoad'

class BTKI(models.Model):
    btki_id = models.AutoField(primary_key=True)
    btki_no = models.CharField(max_length=10,default=None)
    btki_hs_code = models.CharField(max_length=12,default=None)
    btki_uraian_barang = models.CharField(max_length=500,default=None)

    class Meta:
        managed = False
        db_table = 'BTKI'

class PMD63(models.Model):
    pmd63_id = models.AutoField(primary_key=True)
    pmd63_peraturan = models.CharField(max_length=50,default=None)
    pmd63_no = models.CharField(max_length=10,default=None)
    pmd63_hs_code = models.CharField(max_length=12,default=None)
    pmd63_deskripti = models.CharField(max_length=500,default=None)

    class Meta:
        managed = False
        db_table = 'PMD63'

class PMD110(models.Model):
    pmd110_id = models.AutoField(primary_key=True)
    pmd110_peraturan = models.CharField(max_length=50,default=None)
    pmd110_kategori = models.CharField(max_length=50,default=None)
    pmd110_no = models.CharField(max_length=10,default=None)
    pmd110_hs_code = models.CharField(max_length=12,default=None)
    pmd110_deskripti = models.CharField(max_length=500,default=None)

    class Meta:
        managed = False
        db_table = 'PMD110'

class Kurs(models.Model):
    kurs_id = models.AutoField(primary_key=True)
    kurs_code = models.CharField(max_length=5,default=None)
    kurs_name = models.CharField(max_length=70,default=None)
    kurs_value = models.CharField(max_length=250,default=None)

    class Meta:
        managed = False
        db_table = 'Kurs'

class Holiday(models.Model):
    holiday_id = models.AutoField(primary_key=True)
    holiday_date = models.DateField(default=None)
    holiday_name = models.CharField(max_length=100,default=None)

    class Meta:
        managed = False
        db_table = 'Holiday'

class Forwarder(models.Model):
    forwarder_id = models.AutoField(primary_key=True)
    forwarder_name = models.CharField(max_length=70,default=None)
    forwarder_address1 = models.CharField(max_length=250,default=None)
    forwarder_address2 = models.CharField(max_length=250,default=None)
    forwarder_phone = models.CharField(max_length=12,default=None)
    forwarder_fax = models.CharField(max_length=15,default=None)
    forwarder_email = models.CharField(max_length=30,default=None)
    forwarder_npwp = models.CharField(max_length=30,default=None)
    forwarder_apip = models.CharField(max_length=25,default=None)
    forwarder_nib = models.CharField(max_length=25,default=None)
    forwarder_type = models.CharField(max_length=30,default=None)
    forwarder_AccountNo = models.CharField(max_length=20,default=None)
    forwarder_npwpDoc = models.FileField(upload_to='upload/forwarder/npwp/',default=None)
    forwarder_sppkpDoc = models.FileField(upload_to='upload/forwarder/sppkp/',default=None)

    class Meta:
        managed = False
        db_table = 'Forwarder'

class Seller(models.Model):
    seller_id = models.AutoField(primary_key=True)
    seller_name = models.CharField(max_length=70,default=None)
    seller_address1 = models.CharField(max_length=250,default=None)
    seller_address2 = models.CharField(max_length=250,default=None)
    seller_phone = models.CharField(max_length=12,default=None)
    seller_fax = models.CharField(max_length=15,default=None)
    seller_email = models.CharField(max_length=30,default=None)
    seller_npwp = models.CharField(max_length=30,default=None)
    seller_apip = models.CharField(max_length=25,default=None)
    seller_nib = models.CharField(max_length=25,default=None)
    seller_type = models.CharField(max_length=30,default=None)
    seller_AccountNo = models.CharField(max_length=20,default=None)
    seller_npwpDoc = models.FileField(upload_to='upload/seller/npwp/',default=None)
    seller_sppkpDoc = models.FileField(upload_to='upload/seller/sppkp/',default=None)

    class Meta:
        managed = False
        db_table = 'Seller'

class Shipper(models.Model):
    shipper_id = models.AutoField(primary_key=True)
    shipper_name = models.CharField(max_length=70,default=None)
    shipper_address1 = models.CharField(max_length=250,default=None)
    shipper_address2 = models.CharField(max_length=250,default=None)
    shipper_phone = models.CharField(max_length=12,default=None)
    shipper_fax = models.CharField(max_length=15,default=None)
    shipper_email = models.CharField(max_length=30,default=None)
    shipper_npwp = models.CharField(max_length=30,default=None)
    shipper_apip = models.CharField(max_length=25,default=None)
    shipper_nib = models.CharField(max_length=25,default=None)
    shipper_type = models.CharField(max_length=30,default=None)
    shipper_AccountNo = models.CharField(max_length=20,default=None)
    shipper_npwpDoc = models.FileField(upload_to='upload/shipper/npwp/',default=None)
    shipper_sppkpDoc = models.FileField(upload_to='upload/shipper/sppkp/',default=None)

    class Meta:
        managed = False
        db_table = 'Shipper'

class AuditTrail(models.Model):
    audittrail_id = models.AutoField(primary_key=True)
    audittrail_transname = models.CharField(max_length=70,default=None)
    audittrail_transid = models.IntegerField(default=None)
    audittrail_action = models.CharField(max_length=70,default=None)
    audittrail_content = models.TextField(default=None)
    audittrail_createdby = models.CharField(max_length=70,default=None)
    audittrail_createdtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'AuditTrail'

class MasterList(models.Model):
    ml_id = models.AutoField(primary_key=True)
    ml_ofonshore = models.CharField(max_length=10,default=None)
    ml_epc = models.CharField(max_length=10,default=None)
    ml_epc_item_num = models.CharField(max_length=15,default=None)
    ml_kmk_no = models.CharField(max_length=50,default=None)
    ml_oth_kmk_no = models.CharField(max_length=50,default=None)
    ml_kmk_full = models.CharField(max_length=15,default=None)
    ml_kmk_main = models.CharField(max_length=15,default=None)
    ml_kmk_sub = models.CharField(max_length=15,default=None)
    ml_item_desc = models.CharField(max_length=250,default=None)
    ml_item_spec = models.CharField(max_length=500,default=None)
    ml_oigin = models.CharField(max_length=750,default=None)
    ml_kmk_total = models.DecimalField(max_digits=18, decimal_places=2,default=None)
    ml_kmk_unit_id = models.IntegerField(default=None)
    ml_kmk_price_total = models.DecimalField(max_digits=18, decimal_places=2,default=None)
    ml_hs_code = models.CharField(max_length=20,default=None)

    class Meta:
        managed = False
        db_table = 'MasterList'

class Shipment(models.Model):
    shipment_id = models.AutoField(primary_key=True)
    company_id = models.IntegerField(default=None)
    shipper_id = models.IntegerField(default=None)
    seller_id = models.IntegerField(default=None)
    pol_id = models.IntegerField(default=None)
    ppjk_id = models.IntegerField(default=None)
    kppbc_id = models.IntegerField(default=None)
    ship_no = models.CharField(max_length=100,default=None)
    invpl_no = models.CharField(max_length=100,default=None)
    gen_desc = models.CharField(max_length=100,default=None)
    shipper_name = models.CharField(max_length=100,default=None)
    epc = models.CharField(max_length=100,default=None)
    po_no = models.CharField(max_length=100,default=None)
    bl_no = models.CharField(max_length=100,default=None)
    bl_date = models.CharField(max_length=100,default=None)
    etd_date = models.CharField(max_length=100,default=None)
    inv_date = models.CharField(max_length=100,default=None)
    inv_uni = models.CharField(max_length=100,default=None)
    inv_term = models.CharField(max_length=100,default=None)
    inv_curr = models.CharField(max_length=100,default=None)
    inv_amo = models.CharField(max_length=100,default=None)
    inv_qty = models.CharField(max_length=100,default=None)
    pod_name = models.CharField(max_length=100,default=None)
    vessel_flight = models.CharField(max_length=100,default=None)
    eta_date = models.CharField(max_length=100,default=None)
    no_pkg = models.CharField(max_length=100,default=None)
    type = models.CharField(max_length=100,default=None)
    ata_date = models.CharField(max_length=100,default=None)
    no_cntr = models.CharField(max_length=100,default=None)
    sppb_date = models.CharField(max_length=100,default=None)
    tgross_kgs = models.CharField(max_length=100,default=None)
    site_date = models.CharField(max_length=100,default=None)
    cipl_rcvdate = models.CharField(max_length=100,default=None)
    photo_rcvdate = models.CharField(max_length=100,default=None)
    bl_rcvdate = models.CharField(max_length=100,default=None)
    co_rcvdate = models.CharField(max_length=100,default=None)
    co_no = models.CharField(max_length=100,default=None)
    dpib_rcvdate = models.CharField(max_length=100,default=None)
    pibaju_no = models.CharField(max_length=100,default=None)
    skbppn_initdate = models.CharField(max_length=100,default=None)
    skbppn_signdate = models.CharField(max_length=100,default=None)
    skbppn_subdate = models.CharField(max_length=100,default=None)
    skbppn_rcvdate = models.CharField(max_length=100,default=None)
    skbppn_dlvdate = models.CharField(max_length=100,default=None)
    rcv_by = models.CharField(max_length=100,default=None)
    skbpph_initdate = models.CharField(max_length=100,default=None)
    skbpph_signdate = models.CharField(max_length=100,default=None)
    skbpph_subdate = models.CharField(max_length=100,default=None)
    skbpph_rcvdate = models.CharField(max_length=100,default=None)
    skbpph_dlvdate = models.CharField(max_length=100,default=None)
    custdoc_initdate = models.CharField(max_length=100,default=None)
    custdoc_signdate = models.CharField(max_length=100,default=None)
    custdoc_dlvdate = models.CharField(max_length=100,default=None)
    ltrreffkpp_no = models.CharField(max_length=100,default=None)
    ltrreffppjk_no = models.CharField(max_length=100,default=None)
    ltrreffbc_no = models.CharField(max_length=100,default=None)
    ins_no = models.CharField(max_length=100,default=None)
    pib_submit_date = models.CharField(max_length=100,default=None)
    kode_bill = models.CharField(max_length=100,default=None)
    ntpn = models.CharField(max_length=100,default=None)
    pibreg_date = models.CharField(max_length=100,default=None)
    pibreg_no = models.CharField(max_length=100,default=None)
    spjkm = models.CharField(max_length=100,default=None)
    sppb_no = models.CharField(max_length=100,default=None)
    bm = models.CharField(max_length=100,default=None)
    ppn = models.CharField(max_length=100,default=None)
    ppnbm = models.CharField(max_length=100,default=None)
    pph = models.CharField(max_length=100,default=None)
    denda = models.CharField(max_length=100,default=None)
    pnbp = models.CharField(max_length=100,default=None)
    pay_date = models.CharField(max_length=100,default=None)
    attachment1 = models.FileField(upload_to='upload/shipment/attachment1/',default=None)
    attachment2 = models.FileField(upload_to='upload/shipment/attachment2/',default=None)

    class Meta:
        managed = False
        db_table = 'Shipment'

class Shipment_Detail(models.Model):
    shipment_detail_id = models.AutoField(primary_key=True)
    header_id = models.IntegerField(default=None)
    kmk_no = models.CharField(max_length=100,default=None)
    kmk_item_no = models.CharField(max_length=100,default=None)
    kmk_itemm_sub = models.CharField(max_length=100,default=None)
    pib_desc = models.CharField(max_length=100,default=None)

    class Meta:
        managed = False
        db_table = 'Shipment_Detail'






    


