from django.contrib import admin

# Register your models here.
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



admin.site.register(Company)
admin.site.register(EmployeeOwner)
admin.site.register(Position)
admin.site.register(CostType)
admin.site.register(Country)
admin.site.register(FreightCost)
admin.site.register(Region)
admin.site.register(TrackType)
admin.site.register(Unit)
admin.site.register(PortOFLoad)
admin.site.register(BTKI)
admin.site.register(PMD63)
admin.site.register(PMD110)
admin.site.register(Kurs)
admin.site.register(Holiday)
admin.site.register(Forwarder)
admin.site.register(Seller)
admin.site.register(Shipper)
admin.site.register(AuditTrail)
admin.site.register(MasterList)
admin.site.register(Shipment)
admin.site.register(Shipment_Detail)










