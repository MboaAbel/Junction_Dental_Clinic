from django import forms
from .models import mpesa_transactions


class PaymentForm(forms.ModelForm):
    class Meta:
        model = mpesa_transactions
        fields = [
        'MerchantRequestID',
        'CheckoutRequestID',
        'ResponseCode',
        'ResponseDescription',
        'CustomerMessage',
        'phone_number',
        'amount',
        'account_reference',
        'transaction_desc',
        'occassion',
        'is_finished',
        'is_successful',
        'timestamp',
        'trans_id',



        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'form-group '),
                'placeholder':field,
                'style': (
                    'width:98%;'
                    'border-radius: 8px;'
                    'resize: none;'
                    'color:  # 001100;'
                    'height: 40px;'
                    'border: 1px solid  # 4141;'
                    'background-color: transparent;'
                    ' font-family: inherit;'

                ),

            })
