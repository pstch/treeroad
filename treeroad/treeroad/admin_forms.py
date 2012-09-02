from django import forms
from models import View, ViewTemplate

class ViewForm(forms.ModelForm):
    template = forms.Field()

    class Meta:
        model = View

    def __init__(self, *args, **kwargs):
        super(ViewForm, self).__init__(*args, **kwargs)
        # Here we will redefine our test field.
        self.fields['template'] = forms.ModelChoiceField(label='Template',queryset=ViewTemplate.objects.all())
    def clean(self):
        super(forms.ModelForm, self).clean()
        template = self.cleaned_data['template']
        if template:
            self.cleaned_data['name'] = template.name
            self.cleaned_data['start'] = template.start
            self.cleaned_data['end'] = template.end
            self.cleaned_data['description'] = template.description
            self.cleaned_data['highlight'] = template.highlight
        return self.cleaned_data