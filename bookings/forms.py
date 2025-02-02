from django import forms
from .models import Booking






class ReceptionBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'nerd',
            'appointment_ok',
            'doctor',
            'patient',
             'status',
            'appointment_date',
            'appointment_time',
            'symptoms',
            'diagnosis',
            'medications',
            'notes',
            
           

        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'form-group '),
                'value':field,
                'placeholder': field,
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
