from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Select Image', required=False)
    camera_data = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    ACTION_CHOICES = [
        ('compress', 'Compress Image'),
        ('grayscale', 'Convert to Grayscale'),
    ]
    action = forms.ChoiceField(choices=ACTION_CHOICES, widget=forms.RadioSelect, initial='compress')
    
    QUALITY_CHOICES = [
        ('normal', 'Normal (Original)'),
        ('medium', 'Medium (50%)'),
        ('low', 'Low (25%)'),
    ]
    quality = forms.ChoiceField(choices=QUALITY_CHOICES, widget=forms.RadioSelect, initial='medium', required=False, label='Compression Quality')

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        camera_data = cleaned_data.get('camera_data')

        if not image and not camera_data:
            raise forms.ValidationError("Please either upload an image or capture one from the camera.")
        return cleaned_data
