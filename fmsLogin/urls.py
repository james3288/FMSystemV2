from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
                    #path('login/', include('django.contrib.auth.urls')),

                    path('menu/',views.MenuPage, name='menu'),
                    path('login/', views.LoginPage, name='login'),
                    path('logout/<str:log_out>/', views.LogoutPage, name='logout'),
                    path('logout/', views.LogoutPage, name='logout'),
                    path('',views.IndexPage, name='index'),
                    path('repair/',views.RepairPage, name='repair'),
                    path('repair_turnover/', views.RepairTurnoverPage, name='repair_turnover'),
                    path('repair_turnover_update/', views.RepairTurnoverUpdatePage, name='repair_turnover_update'),
                    path('repair_turnover_delete/<int:id>', views.RepairTurnoverRemove, name='repair_turnover_delete'),
                    path('repair_order_delete/<int:id>', views.RepairOrderRemove, name='repair_order_delete'),
                    path('repair_order_history/<str:category>/<str:item_code>', views.RepairOrderHistoryPage, name='repair_order_history'),
                    path('facilities/<str:category>/<int:page>/', views.FacilitiesPage, name='facilities'),
                    path('listoffacilities/', views.ListofFacilitiesPage, name='listoffacilities'),
                    path('create', views.Repair_Order_Create, name='repair_order_create'),
                    path('dashboard/', views.DashboardPage, name="get_dashboard"),
                    path('recent_activities/', views.RecentActivityPage, name='recent_activities'),
                    path('borrowed/<str:category>/<int:page>/', views.FacilitiesPage, name='borrowed'), 
                    path('vacant/<str:category>/<int:page>/', views.FacilitiesPage, name='vacant'), 
                    path('defective/<str:category>/<int:page>/', views.FacilitiesPage, name='defective'), 
                    path('under-repair/<str:category>/<str:item_code>', views.RepairOrderHistoryNew, name='under-repair'),
                    path('under-repair-json/<str:category>/<int:visible>/<str:item_code>/<str:search>', views.RepairOrderHistory_json, name='under_repair_json'),
                    path('served/<str:category>/<int:page>/<str:item_code>', views.FacilitiesPage_new, name='served'),
                    path('borrower_history/<str:item_code>/', views.BorrowerPage, name='borrower_history'),
                    path('main_menu/', views.MainMenuPage, name='main_menu'),
                    path('user_profile/', views.UserProfilePage, name='user_profile'),
                    path('upload/', views.UploadFacilitiesPic, name='upload_view'),
                    path('subitem_history/<str:id>', views.SubItemHistory, name='subitem_history'),
                    path('recent_activities_history/',views.RecentActivityHistory, name='recent_activities_history'),    
                    path('load_recent_activities_history/<int:visible>', views.LoadRecentActivityHistory, name='load_recent_activities_history'),
                    path('computer_maintenance/', views.ComputerMaintenanceHistory, name='computer_maintenance'),
                    path('practice/',views.Practice, name='practice'),
                    path('supplier_price_update/', views.SupplierPriceUpdate, name='supplier_price_update'),
                    path('LoadSupplierPriceUpdate/<int:visible>/<str:search>/', views.LoadSupplierPriceUpdate, name='load_supplier_price_update'),
                    path('facilities_new/<str:category>/<int:page>', views.FacilitiesPage_new, name='facilities_new'),
                    path('facilities_json/<str:category>/<int:visible>/<str:search>', views.Facilities_json, name='facilities_json'),
                ]


# handler404 = 'fmsLogin.views.handling_404'
