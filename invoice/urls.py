from django.contrib import admin
from django.urls import path
from .views import SellInvoiceListView, PurchaseInvoiceListView, createInvoice, updateInvoice, generate_PDF, view_PDF ,sell_delete_invoice, purchase_delete_invoice

app_name = 'invoice'
urlpatterns = [
    path('', SellInvoiceListView.as_view(), name="invoice-list"),
    path('purchase/', PurchaseInvoiceListView.as_view(), name="purchase-invoice-list"),
    path('create/', createInvoice, name="invoice-create"),
    path('update/<id>', updateInvoice, name='invoice-update'),
    path('invoice-detail/<id>', view_PDF, name='invoice-detail'),
    path('invoice-download/<id>', generate_PDF, name='invoice-download'),
    path('sell-invoice-delete/<id>', sell_delete_invoice, name='sell-delete-invoice'),
    path('purchase-invoice-delete/<id>', purchase_delete_invoice, name='purchase-delete-invoice'),
    
]
