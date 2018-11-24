from django.core.exceptions import ValidationError
from django import forms
import ast


class OptionalChoiceWidget(forms.MultiWidget):
    def __init__(self, widgets, attrs=None):
        widgets[1].attrs['class'] = 'form-control'
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            value = ast.literal_eval(value)
            try: # #todo -- log this situation and find out when it occurs
                return [value[0], value[1]]
            except:
                return [None, None]
        return [None, None]


class OptionalChoiceField(forms.MultiValueField):
    def __init__(self, choices, *args, **kwargs):
        fields = [
            forms.ChoiceField(choices=choices, widget=forms.RadioSelect, required=False),
            forms.CharField(required=False, widget=forms.TextInput, help_text='Other')
        ]
        self.widget = OptionalChoiceWidget(widgets=[f.widget for f in fields])
        super().__init__(required=False, fields=fields, *args, **kwargs)

    def compress(self, data_list):
        if not data_list:
            raise ValidationError('This field is required.')

        if 'other' in data_list[0]:
            if not data_list[1]:
                raise ValidationError('You must write in an answer if you select “Specified below”.')
        else:
            if data_list[1]:
                raise ValidationError('You must select “Specified below” if you would like to write in an answer.')
        return data_list[0], data_list[1]


class OptionalMultiChoiceField(forms.MultiValueField):
    def __init__(self, choices, required=False, *args, **kwargs):
        self.required = required
        fields = [
            forms.MultipleChoiceField(choices=choices, widget=forms.widgets.CheckboxSelectMultiple, required=False),
            forms.CharField(required=False, widget=forms.TextInput, help_text='Other')
        ]
        self.widget = OptionalChoiceWidget(widgets=[f.widget for f in fields])
        super().__init__(required=False, fields=fields, *args, **kwargs)

    def compress(self, data_list):
        if self.required:
            if not data_list:
                raise ValidationError('You have to select an option or enter text for this field.')
        if data_list:
            if 'other' in data_list[0]:
                if not data_list[1]:
                    raise ValidationError('You have to fill in the input if you select "Other".')
            else:
                if data_list[1]:
                    raise ValidationError('You have to select "Other" if you want to fill in the input.')
            return data_list[0], data_list[1]
        return None, None
