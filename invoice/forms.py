from django import forms
from django.forms import formset_factory
from .models import Invoice , Items, LineItem


class InvoiceForm(forms.Form):   



    INVOICE_TYPE = (
            ('SALE' , 'Sale'),
            ('PURCHASE' , 'Purchase')
    )

    invoice_type = forms.ChoiceField(
            choices=INVOICE_TYPE,
            label='Invoice Type',
            widget=forms.Select(attrs={
                'class': 'form-control input',
                'placeholder': 'Select invoice type',
            })
    )


        # fields = ['customer', 'message']
    customer = forms.CharField(
        label='Cusomter',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Customer/Company Name',
            'rows':1
        })
    )


    credit_amount = forms.DecimalField(
        label='Credit Amount',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control input rate',
            'placeholder': 'Credit Amount'
        })
    )

    
    billing_address = forms.CharField(
        label='Billing Address',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '',
            'rows':1
        })
    )


    message = forms.CharField(
        label='Message/Note',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'message',
            'rows':1
        })
    )

class LineItemForm(forms.Form):
    
    item = forms.ModelChoiceField(
        label='Product',
        queryset=Items.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control input',
            'placeholder': 'Product',
            'style': 'width:200px',
        })
    )
    description = forms.CharField(
        label='Description',
        # required=False,
        
        widget=forms.TextInput(attrs={
            'class': 'form-control input',
            'placeholder': 'Enter Book Name here',
            "rows":1
        })
    )
    quantity = forms.IntegerField(
        label='Qty',
        widget=forms.TextInput(attrs={
            'class': 'form-control input quantity',
            'placeholder': 'Quantity'
        }) #quantity should not be less than one
    )

    rate = forms.DecimalField(
        label='Rate',
        widget=forms.TextInput(attrs={
            'class': 'form-control input rate',
            'placeholder': 'Rate'
        })
    )
    # amount = forms.DecimalField(
    #     disabled = True,
    #     label='Amount $',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control input',
    #     })
    # )
    
LineItemFormset = formset_factory(LineItemForm, extra=1)