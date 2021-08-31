from django import forms


class ShippingForm(forms.Form):
    firstname = forms.CharField(max_length=250, required=True)
    lastname = forms.CharField(max_length=250, required=True)
    address = forms.CharField(max_length=1000, required=True)
    phone = forms.CharField(max_length=250, required=True)
    city = forms.CharField(max_length=250, required=True)
    zipcode = forms.CharField(max_length=250, required=True)


class CommentForm(forms.Form):
    content = forms.CharField()
    stars = forms.CharField()
