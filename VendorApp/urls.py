from django.urls import path
from .views import *

urlpatterns = [
    # Link to the Home Page
    path('', homePage, name='homePage'),

    # Vendor Page
    path('vendors/', vendorPage, name='vendorPage'),
    # POST request - Create a new vendor
    path('api/vendors/', vendorHandler, name='addVendor'),
    # GET request - Get the list of vendors
    path('api/vendors/', vendorHandler, name='getAllVendors'),
    # GET request - Get specific vendors details
    path('api/vendors/<str:vendor_id>', vendorHandler, name='getVendor'),
    # PUT request - Update a vendor's details
    path('api/vendors/<str:vendor_id>', vendorHandler, name='updateVendor'),
    # DELETE request - Delete a vendor
    path('api/vendors/<str:vendor_id>', vendorHandler, name='deleteVendor'),

    # Purchase Order Page
    path('purchase_orders/', purchaseOrderPage, name='purchaseOrderPage'),
    # POST request - Create a new purchase order
    path('api/purchase_orders/', purchaseOrderHandler, name='addPurchaseOrder'),
    # GET request - Get the list of purchase orders
    path('api/purchase_orders/', purchaseOrderHandler,
         name='getAllPurchaseOrders'),
    # GET request - Get specific purchase orders details
    path('api/purchase_orders/<str:po_id>',
         purchaseOrderHandler, name='getPurchaseOrder'),
    # PUT request - Update a purchase order's details
    path('api/purchase_orders/<str:po_id>',
         purchaseOrderHandler, name='updatePurchaseOrder'),
    # DELETE request - Delete a purchase order
    path('api/purchase_orders/<str:po_id>',
         purchaseOrderHandler, name='deletePurchaseOrder'),
    # POST Request - Acknowledge a Purchase Order
    path('api/purchase_orders/<str:po_id>/acknowledge/',
         acknowledgeOrder, name='acknowledgeOrder'),


    # Performance History Page
    path('performance_history/', performanceHistoryPage,
         name="performanceHistoryPage"),
    # GET Request - Get the performance history chart of a particular vendor
    path('api/vendors/performance/',
         getPerformance, name="getPerformance")
]
