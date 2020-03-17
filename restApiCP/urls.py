from django.conf.urls import url
from . import views

urlpatterns = [
    ##company
    url(r'^company/retrieve/$', views.retrieve_company),
    url(r'^company/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_company),
    url(r'^company/create/$', views.create_company),
    url(r'^company/update/(?P<update_id>[0-9]+)$', views.update_company),
    url(r'^company/delete/(?P<delete_id>[0-9]+)$', views.delete_company),

    ##EmployeeOwner
    url(r'^eo/retrieve/$', views.retrieve_eo),
    url(r'^eo/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_eo),
    url(r'^eo/create/$', views.create_eo),
    url(r'^eo/update/(?P<update_id>[0-9]+)$', views.update_eo),
    url(r'^eo/delete/(?P<delete_id>[0-9]+)$', views.delete_eo),

    ##position
    url(r'^position/retrieve/$', views.retrieve_position),
    url(r'^position/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_position),
    url(r'^position/create/$', views.create_position),
    url(r'^position/update/(?P<update_id>[0-9]+)$', views.update_position),
    url(r'^position/delete/(?P<delete_id>[0-9]+)$', views.delete_position),

    ##costtype
    url(r'^costtype/retrieve/$', views.retrieve_costtype),
    url(r'^costtype/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_costtype),
    url(r'^costtype/create/$', views.create_costtype),
    url(r'^costtype/update/(?P<update_id>[0-9]+)$', views.update_costtype),
    url(r'^costtype/delete/(?P<delete_id>[0-9]+)$', views.delete_costtype),

    ##country
    url(r'^country/retrieve/$', views.retrieve_country),
    url(r'^country/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_country),
    url(r'^country/create/$', views.create_country),
    url(r'^country/update/(?P<update_id>[0-9]+)$', views.update_country),
    url(r'^country/delete/(?P<delete_id>[0-9]+)$', views.delete_country),

    ##region
    url(r'^region/retrieve/$', views.retrieve_region),
    url(r'^region/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_region),
    url(r'^region/create/$', views.create_region),
    url(r'^region/update/(?P<update_id>[0-9]+)$', views.update_region),
    url(r'^region/delete/(?P<delete_id>[0-9]+)$', views.delete_region),

    ##tracktype
    url(r'^tracktype/retrieve/$', views.retrieve_tracktype),
    url(r'^tracktype/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_tracktype),
    url(r'^tracktype/create/$', views.create_tracktype),
    url(r'^tracktype/update/(?P<update_id>[0-9]+)$', views.update_tracktype),
    url(r'^tracktype/delete/(?P<delete_id>[0-9]+)$', views.delete_tracktype),

    ##freightcost
    url(r'^freightcost/retrieve/$', views.retrieve_freightcost),
    url(r'^freightcost/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_freightcost),
    url(r'^freightcost/create/$', views.create_freightcost),
    url(r'^freightcost/update/(?P<update_id>[0-9]+)$', views.update_freightcost),
    url(r'^freightcost/delete/(?P<delete_id>[0-9]+)$', views.delete_freightcost),

    ##unit
    url(r'^unit/retrieve/$', views.retrieve_unit),
    url(r'^unit/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_unit),
    url(r'^unit/create/$', views.create_unit),
    url(r'^unit/update/(?P<update_id>[0-9]+)$', views.update_unit),
    url(r'^unit/delete/(?P<delete_id>[0-9]+)$', views.delete_unit),

    ##portofload
    url(r'^portofload/retrieve/$', views.retrieve_portofload),
    url(r'^portofload/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_portofload),
    url(r'^portofload/create/$', views.create_portofload),
    url(r'^portofload/update/(?P<update_id>[0-9]+)$', views.update_portofload),
    url(r'^portofload/delete/(?P<delete_id>[0-9]+)$', views.delete_portofload),

    ##btki
    url(r'^btki/retrieve/$', views.retrieve_btki),
    url(r'^btki/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_btki),
    url(r'^btki/create/$', views.create_btki),
    url(r'^btki/update/(?P<update_id>[0-9]+)$', views.update_btki),
    url(r'^btki/delete/(?P<delete_id>[0-9]+)$', views.delete_btki),

    ##pmd63
    url(r'^pmd63/retrieve/$', views.retrieve_pmd63),
    url(r'^pmd63/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_pmd63),
    url(r'^pmd63/create/$', views.create_pmd63),
    url(r'^pmd63/update/(?P<update_id>[0-9]+)$', views.update_pmd63),
    url(r'^pmd63/delete/(?P<delete_id>[0-9]+)$', views.delete_pmd63),

    ##pmd110
    url(r'^pmd110/retrieve/$', views.retrieve_pmd110),
    url(r'^pmd110/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_pmd110),
    url(r'^pmd110/create/$', views.create_pmd110),
    url(r'^pmd110/update/(?P<update_id>[0-9]+)$', views.update_pmd110),
    url(r'^pmd110/delete/(?P<delete_id>[0-9]+)$', views.delete_pmd110),

    ##kurs
    url(r'^kurs/retrieve/$', views.retrieve_kurs),
    url(r'^kurs/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_kurs),
    url(r'^kurs/create/$', views.create_kurs),
    url(r'^kurs/update/(?P<update_id>[0-9]+)$', views.update_kurs),
    url(r'^kurs/delete/(?P<delete_id>[0-9]+)$', views.delete_kurs),

    ##holiday
    url(r'^holiday/retrieve/$', views.retrieve_holiday),
    url(r'^holiday/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_holiday),
    url(r'^holiday/create/$', views.create_holiday),
    url(r'^holiday/update/(?P<update_id>[0-9]+)$', views.update_holiday),
    url(r'^holiday/delete/(?P<delete_id>[0-9]+)$', views.delete_holiday),

    ##forwarder
    url(r'^forwarder/retrieve/$', views.retrieve_forwarder),
    url(r'^forwarder/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_forwarder),
    url(r'^forwarder/create/$', views.create_forwarder),
    url(r'^forwarder/update/(?P<update_id>[0-9]+)$', views.update_forwarder),
    url(r'^forwarder/delete/(?P<delete_id>[0-9]+)$', views.delete_forwarder),

    ##seller
    url(r'^seller/retrieve/$', views.retrieve_seller),
    url(r'^seller/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_seller),
    url(r'^seller/create/$', views.create_seller),
    url(r'^seller/update/(?P<update_id>[0-9]+)$', views.update_seller),
    url(r'^seller/delete/(?P<delete_id>[0-9]+)$', views.delete_seller),

    ##shipper
    url(r'^shipper/retrieve/$', views.retrieve_shipper),
    url(r'^shipper/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_shipper),
    url(r'^shipper/create/$', views.create_shipper),
    url(r'^shipper/update/(?P<update_id>[0-9]+)$', views.update_shipper),
    url(r'^shipper/delete/(?P<delete_id>[0-9]+)$', views.delete_shipper),

    ##audittrail
    url(r'^audittrail/retrieve/$', views.retrieve_audittrail),
    url(r'^audittrail/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_audittrail),
    url(r'^audittrail/create/$', views.create_audittrail),
    url(r'^audittrail/update/(?P<update_id>[0-9]+)$', views.update_audittrail),
    url(r'^audittrail/delete/(?P<delete_id>[0-9]+)$', views.delete_audittrail),

    ##masterlist
    url(r'^masterlist/retrieve/$', views.retrieve_masterlist),
    url(r'^masterlist/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_masterlist),
    url(r'^masterlist/create/$', views.create_masterlist),
    url(r'^masterlist/update/(?P<update_id>[0-9]+)$', views.update_masterlist),
    url(r'^masterlist/delete/(?P<delete_id>[0-9]+)$', views.delete_masterlist),

    ##shipment
    url(r'^shipment/retrieve/$', views.retrieve_shipment),
    url(r'^shipment/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_shipment),
    url(r'^shipment/create/$', views.create_shipment),
    url(r'^shipment/update/(?P<update_shipment_id>[0-9]+)/(?P<update_shipment_detail_id>[0-9]+)$', views.update_shipment),
    url(r'^shipment/delete/(?P<delete_id>[0-9]+)$', views.delete_shipment),

    ##shipment_detail
    url(r'^shipment_detail/retrieve/$', views.retrieve_shipment_detail),
    url(r'^shipment_detail/retrievebyId/(?P<get_id>[0-9]+)$', views.retrievebyId_shipment_detail),
    url(r'^shipment_detail/create/$', views.create_shipment_detail),
    url(r'^shipment_detail/update/(?P<update_id>[0-9]+)$', views.update_shipment_detail),
    url(r'^shipment_detail/delete/(?P<delete_id>[0-9]+)$', views.delete_shipment_detail),

    #call store procedure
    url(r'^dashboard/getNewEntries/$', views.getNewEntries),
    url(r'^dashboard/getCount/$', views.getCount),
]
