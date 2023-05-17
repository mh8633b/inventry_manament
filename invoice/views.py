from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View
from .models import LineItem, Invoice
from .forms import LineItemFormset, InvoiceForm

import pdfkit

class SellInvoiceListView(View):
    def get(self, *args, **kwargs):
        invoices = Invoice.objects.filter(invoice_type= 'SALE')
        context = {
            "invoices":invoices,
        }

        return render(self.request, 'invoice/invoice-list.html', context)
    
 
 
    def post(self, request):        
        # import pdb;pdb.set_trace()
        invoice_ids = request.POST.getlist("invoice_id")
        invoice_ids = list(map(int, invoice_ids))

        update_status_for_invoices = int(request.POST['status'])
        invoices = Invoice.objects.filter(id__in=invoice_ids)
        # import pdb;pdb.set_trace()
        if update_status_for_invoices == 0:
            invoices.update(status=False)
        else:
            invoices.update(status=True)


        return redirect('invoice:invoice-list')
    


class PurchaseInvoiceListView(View):
    def get(self, *args, **kwargs):
        invoices = Invoice.objects.filter(invoice_type= 'PURCHASE')
        context = {
            "invoices":invoices,
        }

        return render(self.request, 'invoice/purchase-invoice-list.html', context)
    
 
 
    def post(self, request):        
        # import pdb;pdb.set_trace()
        invoice_ids = request.POST.getlist("invoice_id")
        invoice_ids = list(map(int, invoice_ids))

        update_status_for_invoices = int(request.POST['status'])
        invoices = Invoice.objects.filter(id__in=invoice_ids)
        # import pdb;pdb.set_trace()
        if update_status_for_invoices == 0:
            invoices.update(status=False)
        else:
            invoices.update(status=True)


        return redirect('invoice:purchase-invoice-list')

# def createInvoice(request):
#     """
#     Invoice Generator page it will have Functionality to create new invoices, 
#     this will be protected view, only admin has the authority to read and make
#     changes here.
#     """

#     heading_message = 'Formset Demo'
#     if request.method == 'GET':
#         formset = LineItemFormset(request.GET or None)
#         form = InvoiceForm(request.GET or None)
#     elif request.method == 'POST':
#         formset = LineItemFormset(request.POST)
#         form = InvoiceForm(request.POST)
        
#         if form.is_valid():
#             invoice = Invoice.objects.create(customer=form.data["customer"],
#                     credit_amount=form.data["credit_amount"],
#                     invoice_type=form.data["invoice_type"],
#                     billing_address = form.data["billing_address"],
#                     # date=form.data["date"],
#                     # due_date=form.data["due_date"], 
#                     message=form.data["message"],
#                     )
#             # invoice.save()
            
#         if formset.is_valid():
#             # import pdb;pdb.set_trace()
#             # extract name and other data from each form and save
#             total = 0
#             for form in formset:
#                 item = form.cleaned_data.get('item')
#                 description = form.cleaned_data.get('description')
#                 quantity = form.cleaned_data.get('quantity')
#                 rate = form.cleaned_data.get('rate')
#                 if item and description and quantity and rate:
#                     amount = float(rate)*float(quantity)
#                     total += amount
#                     LineItem(customer=invoice,
#                             item=item,
#                             description=description,
#                             quantity=quantity,
#                             rate=rate,
#                             amount=amount).save()
#             invoice.total_amount = total
#             invoice.save()
#             try:
#                 generate_PDF(request, id=invoice.id)
#             except Exception as e:
#                 print(f"********{e}********")
#             return redirect('/')
#     context = {
#         "title" : "Invoice Generator",
#         "formset": formset,
#         "form": form,
#     }
#     return render(request, 'invoice/invoice-create.html', context)


def createInvoice(request):
    """
    Invoice Generator page with functionality to create new invoices.
    This is a protected view, only admin has the authority to read and make changes here.
    """

    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = LineItemFormset(request.GET or None)
        form = InvoiceForm(request.GET or None)
    elif request.method == 'POST':
        formset = LineItemFormset(request.POST)
        form = InvoiceForm(request.POST)
        
        if form.is_valid() and formset.is_valid():
            invoice = Invoice.objects.create(
                customer=form.cleaned_data['customer'],
                credit_amount=form.cleaned_data['credit_amount'],
                invoice_type=form.cleaned_data['invoice_type'],
                billing_address=form.cleaned_data['billing_address'],
                message=form.cleaned_data['message'],
            )
            
            total = 0
            for form in formset:
                item = form.cleaned_data.get('item')
                description = form.cleaned_data.get('description')
                quantity = form.cleaned_data.get('quantity')
                rate = form.cleaned_data.get('rate')
                if item and description and quantity and rate:
                    amount = float(rate) * float(quantity)
                    total += amount
                    LineItem.objects.create(
                        customer=invoice,
                        item=item,
                        description=description,
                        quantity=quantity,
                        rate=rate,
                        amount=amount
                    )
            
            invoice.total_amount = total
            invoice.save()
            
            try:
                generate_PDF(request, id=invoice.id)
            except Exception as e:
                print(f"********{e}********")
            
            return redirect('/')
    
    context = {
        "title": "Invoice Generator",
        "formset": formset,
        "form": form,
    }
    return render(request, 'invoice/invoice-create.html', context)


def updateInvoice(request, id=None):
    """
    Update existing invoice
    """

    invoice = Invoice.objects.get(id=id)
    line_items = invoice.lineitem_set.all()

    if request.method == 'GET':
        formset = LineItemFormset(initial=[
            {
                'item': line_item.item,
                'description': line_item.description,
                'quantity': line_item.quantity,
                'rate': line_item.rate
            }
            for line_item in line_items
        ])
        form = InvoiceForm(initial={
            'customer': invoice.customer,
            'credit_amount': invoice.credit_amount,
            'invoice_type': invoice.invoice_type,
            'billing_address': invoice.billing_address,
            'message': invoice.message
        })

    elif request.method == 'POST':
        formset = LineItemFormset(request.POST)
        form = InvoiceForm(request.POST)

        if form.is_valid():
            invoice.customer = form.cleaned_data['customer']
            invoice.credit_amount = form.cleaned_data['credit_amount']
            invoice.invoice_type = form.cleaned_data['invoice_type']
            invoice.billing_address = form.cleaned_data['billing_address']
            invoice.message = form.cleaned_data['message']
            invoice.save()

        if formset.is_valid():
            for i, form in enumerate(formset):
                if form.has_changed():
                    if form.cleaned_data.get('DELETE'):
                        # Handle deletion of line items
                        line_item = line_items[i]
                        line_item.delete()
                    else:
                        # Update or create line item
                        item = form.cleaned_data.get('item')
                        description = form.cleaned_data.get('description')
                        quantity = form.cleaned_data.get('quantity')
                        rate = form.cleaned_data.get('rate')
                        if item and description and quantity and rate:
                            amount = float(rate) * float(quantity)
                            if i < len(line_items):
                                # Update existing line item
                                line_item = line_items[i]
                                line_item.item_id = item.id
                                line_item.description = description
                                line_item.quantity = quantity
                                line_item.rate = rate
                                line_item.amount = amount
                                line_item.save()
                            else:
                                # Create new line item
                                LineItem.objects.create(
                                    customer=invoice,
                                    item_id=item.id,
                                    description=description,
                                    quantity=quantity,
                                    rate=rate,
                                    amount=amount
                                )

            # Calculate total amount
            total_amount = sum(line_item.amount for line_item in invoice.lineitem_set.all())
            invoice.total_amount = total_amount
            invoice.save()

            try:
                generate_PDF(request, id=invoice.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect('/')

    context = {
        "title": "Update Invoice",
        "formset": formset,
        "form": form,
        "total_amount": invoice.total_amount  # Pass total_amount to the context
    }
    return render(request, 'invoice/invoice-create.html', context)

def view_PDF(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)
    lineitem = invoice.lineitem_set.all()
    print(lineitem)

    context = {
        "company": {
            "name": "Ibrahim Services",
            "address" :"67542 Jeru, Chatsworth, CA 92145, US",
            "phone": "(818) XXX XXXX",
            "email": "contact@ibrahimservice.com",
        },
        "invoice_id": invoice.id,
        "invoice_total": invoice.total_amount,
        "customer": invoice.customer,
        "credit_amount": invoice.credit_amount,
        "date": invoice.date,
        # "due_date": invoice.due_date,
        "billing_address": invoice.billing_address,
        "message": invoice.message,
        "lineitem": lineitem,

    }
    return render(request, 'invoice/pdf_template.html', context)

def generate_PDF(request, id):
    # Use False instead of output path to save pdf to a variable

    config = pdfkit.configuration(wkhtmltopdf='C:\Program Files\wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('invoice:invoice-detail', args=[id])), False, configuration=config)
    # pdf = pdfkit.from_url(request.build_absolute_uri(reverse('invoice:invoice-detail', args=[id])), False)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response

def change_status(request):
    return redirect('invoice:invoice-list')

def view_404(request,  *args, **kwargs):
    return redirect('invoice:invoice-list')

def sell_delete_invoice(request, id):
    # get the row to delete based on its primary key
    row_to_delete = Invoice.objects.get(pk=id)

    # delete the row from the database
    
    row_to_delete.delete()

    # redirect to a success page
    return redirect('invoice:invoice-list')

def purchase_delete_invoice(request, id):
    # get the row to delete based on its primary key
    row_to_delete = Invoice.objects.get(pk=id)

    # delete the row from the database
    
    row_to_delete.delete()

    # redirect to a success page
    return redirect('invoice:purchase-invoice-list')



