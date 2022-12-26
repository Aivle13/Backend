from django.urls import path
from patient.views import signup, signin, hospital_srch
from patient.views import mypage
urlpatterns = [
    path('signup/', signup),
    path('signin/', signin),
    path('mypage/', mypage),
    path('hospital_srch/', hospital_srch)
]
