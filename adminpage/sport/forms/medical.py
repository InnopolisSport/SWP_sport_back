from django import forms


class MedicalGroupReferenceForm(forms.Form):
    references = forms.ImageField(widget=forms.FileInput(attrs={"multiple": True}))
    student_comment = forms.CharField(
        widget=forms.Textarea,
        max_length=1024,
        label="Comments (optional)",
        required=False,
        empty_value='-'
    )
