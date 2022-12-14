from django import forms
from .models import CommentText

class SearchForm(forms.Form):
    component_choices =(
        ("", ""),
        ("LEC", "LEC"),
        ("LAB", "LAB"),
        ("STO", "STO"),
        ("IND", "IND")
    )

    semester_choices =(
        ("",""),
        (1228, "Fall 2022"),
        (1231, "January 2023"),
        (1332, "Spring 2023"),
    )

    day_choices =(
        ("Mo", "Monday"),
        ("Tu", "Tuesday"),
        ("We", "Wednesday"),
        ("Th", "Thursday"),
        ("Fr", "Friday")
    )

    full_choices =(
        ("", ""),
        ("Yes", "Yes"),
        ("No", "No"),
    )

    mnemonic = forms.CharField(max_length=4, required=True, widget=forms.TextInput(attrs={'placeholder': 'CS'}))
    course_num = forms.CharField(max_length=4, required=True, widget=forms.TextInput(attrs={'placeholder': '1110'}))
    semester = forms.ChoiceField(choices=semester_choices, required=False)
    component = forms.ChoiceField(choices=component_choices, required=False)
    credits = forms.CharField(max_length=1, required=False, widget=forms.TextInput(attrs={'placeholder': '3'}))
    include_full_classes = forms.ChoiceField(choices=full_choices, required=False)
    days = forms.MultipleChoiceField(choices=day_choices, widget=forms.CheckboxSelectMultiple, required=False)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentText
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'style': 'widtch:150px; height:30px'}),
        }
