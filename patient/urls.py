from django.urls import path
from patient.views import signup, signin, hospital_srch

urlpatterns = [
    path('signup/', signup),
    path('signin/', signin),
    path('hospital_srch/', hospital_srch),
]
