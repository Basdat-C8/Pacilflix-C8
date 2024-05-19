# forms.py
from django import forms

class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=[('bank', 'Transfer Bank'), ('credit', 'Kartu Kredit'), ('ewallet', 'E-Wallet')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )
