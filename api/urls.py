
from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter
from organization import views as organizationView
from users import views as usersView
from event import views as EventView


organizationrouter = DefaultRouter()
organizationrouter.register('organization', organizationView.OrganizationViewSet,
                            basename='organization')
organizationrouter.register('organizationportifolio',organizationView.OrganizationPortifolioViewSet,
                            basename='organizationportifolio')
organizationrouter.register('organizationschedule',organizationView.OrganizationScheduleViewSet,
                            basename='organizationschedule')
organizationrouter.register('featurecategory',organizationView.FeatureCategoryViewSet)
organizationrouter.register('feature',organizationView.FeatureViewSet)
organizationrouter.register('plan',organizationView.PlanViewSet)
organizationrouter.register('customplan',organizationView.CustomPlanViewSet)
organizationrouter.register('webpagetemplate',organizationView.OrganizationWebPageTemplateViewSet)
organizationrouter.register('ecardtemplate',organizationView.OrganizationEcardTemplateViewSet)
organizationrouter.register('organizationwebpage',organizationView.OrganizationWebpageViewSet)
organizationrouter.register('organizationecard',organizationView.OrganizationEcardViewSet)


userrouter = DefaultRouter()

userrouter.register('organizationuser',usersView.OrganizationUserViewSet,basename='organizationuser')
userrouter.register('affiliate',usersView.AffiliateViewSet,basename='affiliate')
userrouter.register('customer',usersView.CustomerViewSet,basename='customer')
userrouter.register('employee',usersView.EmployeeViewSet,basename='employee')
userrouter.register('marketer',usersView.MarketerViewSet,basename='marketer')


eventrouter = DefaultRouter()

eventrouter.register('event',EventView.EventViewSet,basename='event')
eventrouter.register('eventschedule',EventView.OrganizationEventScheduleViewSet,basename='eventschedule')
eventrouter.register('album',EventView.AlbumViewSet,basename='album')
eventrouter.register('albumimage',EventView.AlbumImageViewSet,basename='albumimage')
eventrouter.register('albumface',EventView.AlbumFaceViewSet,basename='albumface')
eventrouter.register('stream',EventView.EventStreamViewSet,basename='eventstream')
eventrouter.register('transaction',EventView.EventTransactionViewSet,basename='eventtransaction')
eventrouter.register('webpagetemplate',EventView.EventWebPageTemplateViewSet)
eventrouter.register('invitationtemplate',EventView.EventInvitationTemplateViewSet)
eventrouter.register('digitalinvitationtemplate',EventView.DigitalInvitationTemplateViewSet)
eventrouter.register('eventwebpage',EventView.EventWebpageViewSet)
eventrouter.register('eventinvitation',EventView.EventInvitationViewSet)
eventrouter.register('eventwish',EventView.EventWishViewSet)
eventrouter.register('eventpayremainder',EventView.EventpaymentRemainderViewSet)
eventrouter.register('digitalinvitation',EventView.DigitalInvitationViewSet)
eventrouter.register('digitalinvitationlog',EventView.DigitalInvitationLogViewSet,basename='invitationlog')
eventrouter.register('targetedaudient',EventView.TargetedAudientViewSet)



urlpatterns = [
    path('', include(organizationrouter.urls)),
    path('users/',include(userrouter.urls)),
    path('organizationevents/',include(eventrouter.urls)),
    path('getotp/',usersView.SendOtp.as_view()),
    path('verifyotp/',usersView.VerifyOtp.as_view()),
    path('organization/info',organizationView.OrganizationInfoViewSet.as_view()),
    path('organizationevents/eventscheduler',EventView.EventShedule.as_view()),
    path('organization/schedule',organizationView.ScheduleView.as_view()),
    path('organization/view',organizationView.OrganizationViewsSet.as_view()),
    path('organizationevents/eventinfo',EventView.EventInfoViewSet.as_view()),
    
]
