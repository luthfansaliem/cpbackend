from rest_framework import serializers
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


class CompanySerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('company_id',
                  'company_name',
                  'company_address1',
                  'company_address2',
                  'company_phone',
                  'company_fax',
                  'company_email',
                  'company_npwp',
                  'company_apip',
                  'company_nib',
                  'company_type',
                  'company_AccountNo',
                  'company_npwpDoc',
                  'company_sppkpDoc',)

class EmployeeOwnerSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EmployeeOwner
        fields = ('eo_id',
                  'eo_name',
                  'eo_address1',
                  'eo_address2',
                  'eo_phone',
                  'eo_nik',
                  'eo_email',
                  'eo_npwp',
                  'eo_position_id',
                  'eo_company_id',
                  'eo_nik_img',
                  'eo_npwp_img',
                  'eo_oth_img',)

class PositionSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Position
        fields = ('position_id',
                  'position_name',)

class CostTypeSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CostType
        fields = ('costtype_id',
                  'costtype_code',
                  'costtype_name',)

class CountrySerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ('country_id',
                  'country_code',
                  'country_codecode',
                  'country_name',)


class RegionSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Region
        fields = ('region_id',
                  'region_code',
                  'region_name',)

class TrackTypeSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TrackType
        fields = ('tracktype_id',
                  'tracktype_code',
                  'tracktype_name',)

class FreightCostSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FreightCost
        fields = ('freightcost_id',
                  'region_id',
                  'costtype_id',
                  'tracktype_id',
                  'amount',)

class UnitSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Unit
        fields = ('unit_id',
                  'unit_code',
                  'unit_name',)

class PortOFLoadSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PortOFLoad
        fields = ('portofload_id',
                  'portofload_code',
                  'portofload_name',)

class BTKISerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BTKI
        fields = ('btki_id',
                  'btki_no',
                  'btki_hs_code',
                  'btki_uraian_barang',)

class PMD63Serializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PMD63
        fields = ('pmd63_id',
                  'pmd63_peraturan',
                  'pmd63_no',
                  'pmd63_hs_code',
                  'pmd63_deskripti',)

class PMD110Serializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PMD110
        fields = ('pmd110_id',
                  'pmd110_peraturan',
                  'pmd110_kategori',
                  'pmd110_no',
                  'pmd110_hs_code',
                  'pmd110_deskripti',)

class KursSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Kurs
        fields = ('kurs_id',
                  'kurs_code',
                  'kurs_name',
                  'kurs_value',)

class HolidaySerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Holiday
        fields = ('holiday_id',
                  'holiday_date',
                  'holiday_name',)

class ForwarderSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Forwarder
        fields = ('forwarder_id',
                  'forwarder_name',
                  'forwarder_address1',
                  'forwarder_address2',
                  'forwarder_phone',
                  'forwarder_fax',
                  'forwarder_email',
                  'forwarder_npwp',
                  'forwarder_apip',
                  'forwarder_nib',
                  'forwarder_type',
                  'forwarder_AccountNo',
                  'forwarder_npwpDoc',
                  'forwarder_sppkpDoc',)

class SellerSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Seller
        fields = ('seller_id',
                  'seller_name',
                  'seller_address1',
                  'seller_address2',
                  'seller_phone',
                  'seller_fax',
                  'seller_email',
                  'seller_npwp',
                  'seller_apip',
                  'seller_nib',
                  'seller_type',
                  'seller_AccountNo',
                  'seller_npwpDoc',
                  'seller_sppkpDoc',)

class ShipperSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shipper
        fields = ('shipper_id',
                  'shipper_name',
                  'shipper_address1',
                  'shipper_address2',
                  'shipper_phone',
                  'shipper_fax',
                  'shipper_email',
                  'shipper_npwp',
                  'shipper_apip',
                  'shipper_nib',
                  'shipper_type',
                  'shipper_AccountNo',
                  'shipper_npwpDoc',
                  'shipper_sppkpDoc',)

class AuditTrailSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AuditTrail
        fields = ('audittrail_id',
                  'audittrail_transname',
                  'audittrail_transid',
                  'audittrail_action',
                  'audittrail_content',
                  'audittrail_createdby',
                  'audittrail_createdtime',)

class MasterListSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MasterList
        fields = ('ml_id',
                  'ml_ofonshore',
                  'ml_epc',
                  'ml_epc_item_num',
                  'ml_kmk_no',
                  'ml_oth_kmk_no',
                  'ml_kmk_full',
                  'ml_kmk_main',
                  'ml_kmk_sub',
                  'ml_item_desc',
                  'ml_item_spec',
                  'ml_oigin',
                  'ml_kmk_total',
                  'ml_kmk_unit_id',
                  'ml_kmk_price_total',
                  'ml_hs_code',)

class ShipmentSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shipment
        fields = ('shipment_id',
                  'company_id',
                  'shipper_id',
                  'seller_id',
                  'pol_id',
                  'ppjk_id',
                  'kppbc_id',
                  'ship_no',
                  'invpl_no',
                  'gen_desc',
                  'shipper_name',
                  'epc',
                  'po_no',
                  'bl_no',
                  'bl_date',
                  'etd_date',
                  'inv_date',
                  'inv_uni',
                  'inv_term',
                  'inv_curr',
                  'inv_amo',
                  'inv_qty',
                  'pod_name',
                  'vessel_flight',
                  'eta_date',
                  'no_pkg',
                  'type',
                  'ata_date',
                  'no_cntr',
                  'sppb_date',
                  'tgross_kgs',
                  'site_date',
                  'cipl_rcvdate',
                  'photo_rcvdate',
                  'bl_rcvdate',
                  'co_rcvdate',
                  'co_no',
                  'dpib_rcvdate',
                  'pibaju_no',
                  'skbppn_initdate',
                  'skbppn_signdate',
                  'skbppn_subdate',
                  'skbppn_rcvdate',
                  'skbppn_dlvdate',
                  'rcv_by',
                  'skbpph_initdate',
                  'skbpph_signdate',
                  'skbpph_subdate',
                  'skbpph_rcvdate',
                  'skbpph_dlvdate',
                  'custdoc_initdate',
                  'custdoc_signdate',
                  'custdoc_dlvdate',
                  'ltrreffkpp_no',
                  'ltrreffppjk_no',
                  'ltrreffbc_no',
                  'ins_no',
                  'pib_submit_date',
                  'kode_bill',
                  'ntpn',
                  'pibreg_date',
                  'pibreg_no',
                  'spjkm',
                  'sppb_no',
                  'bm',
                  'ppn',
                  'ppnbm',
                  'pph',
                  'denda',
                  'pnbp',
                  'pay_date',
                  'attachment1',
                  'attachment2',)

class Shipment_DetailSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shipment_Detail
        fields = ('shipment_detail_id',
                  'header_id',
                  'kmk_no',
                  'kmk_item_no',
                  'kmk_itemm_sub',
                  'pib_desc',)