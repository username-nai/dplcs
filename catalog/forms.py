from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    author_name = forms.CharField(max_length=255, required=True, help_text="Separate multiple authors with commas")

    class Meta:
        model = Book
        fields = ('name', 'total_quantity', 'room_no', 'shelf_no', 'row', 'column')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
