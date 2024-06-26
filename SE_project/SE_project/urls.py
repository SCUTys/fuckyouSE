"""SE_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import *
from app_mainwindow import views as app_mainwindow_views
from compare import views as compare_views
from conditionfilter import views as conditionfilter_views
from detail import views as detail_views
from latestgood import views as latestgood_views
from login import views as login_views
from recenthot import views as recenthot_views
from salerank import views as salerank_views
from searchresult import views as searchresult_views
from urlsearch import views as urlsearch_views
from latesthot import views as latesthot_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("test-mainwindow/", app_mainwindow_views.test_mainwindow),
    path("compare/", compare_views.compare_mainwindow,name="compare"),
    path("conditionfilter/", conditionfilter_views.conditionfilter_window,name="conditionfilter"),

    path("detail/", detail_views.call_detail,name="detail"),
    path("detail/<phone_id>", detail_views.detail_window,name="detail_phone_id"),
    path("check_comment/", detail_views.check_comment,name="check_comment"),


    path("latestgood/", latestgood_views.latestgood_window,name="latestgood"),
    path("login/", login_views.login_window,name="login"),
    path("recenthot/", recenthot_views.recenthot_window,name="recenthot"),
    path("salerank/", salerank_views.salerank_window,name="salerank"),

    path("searchresult/", searchresult_views.call_searchresult,name="searchresult"),
    path("searchresult/<keyword>/<cookie>", searchresult_views.searchresult_window,name="searchresult_keyword_cookie"),

    path("urlsearch/", urlsearch_views.urlsearch_window,name="urlsearch"),
    path("latesthot/", latesthot_views.latesthot_window,name="latesthot"),

    ##details_url
    path("generate_WC/", detail_views.generate_WC, name='generate_WC'),
    path("generate_summary/", detail_views.generate_summary, name='generate_summary'),
    path("add_to_compare/", detail_views.add_to_compare, name='add_to_compare'),
    path("delete_compare/", compare_views.delete_compare, name='delete_compare'),
    path('check_task/', searchresult_views.check_task,name="check_task"),
    path('mycrawler/', searchresult_views.mycrawler,name="mycrawler"),

    path('call_searchresult/', searchresult_views.call_searchresult,name="call_crawler"),
    path('call_detail/', detail_views.call_detail,name="call_detail"),
    # path('',include('SE_project.urls'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
