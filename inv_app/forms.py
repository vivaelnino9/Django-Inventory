from django import forms
from inv_app.models import User, Inv_User
from django.utils.encoding import force_text

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class Inv_UserForm(forms.ModelForm):
    class Meta:
        model = Inv_User
        fields = ('first_name', 'last_name')

# class UploadZipForm(forms,Form):
#     zip_file = forms.FileField()
#
#     title = forms.CharField(
#         label='Title',
#         required=False,
#         help_text=''
#     )
#
#     gallery = forms.ModelChoiceField(
#         Gallery.objects.all(),
#         label='Gallery',
#         required=False,
#         help_text= /
#             'Select a gallery to add these images to. Leave this empty to'
#             'create a new gallery from the supplied title.'
#     )
#
#     def clean_zip_file(self):
#         """Open the zip file a first time, to check that it is a valid zip archive.
#         We'll open it again in a moment, so we have some duplication, but let's focus
#         on keeping the code easier to read!
#         """
#         zip_file = self.cleaned_data['zip_file']
#         try:
#             zip = zipfile.ZipFile(zip_file)
#         except BadZipFile as e:
#             raise forms.ValidationError(str(e))
#         bad_file = zip.testzip()
#         if bad_file:
#             zip.close()
#             raise forms.ValidationError('"%s" in the .zip archive is corrupt.' % bad_file)
#         zip.close()  # Close file in all cases.
#         return zip_file
#
#     def clean_title(self):
#         title = self.cleaned_data['title']
#         if title and Gallery.objects.filter(title=title).exists():
#             raise forms.ValidationError(_('A gallery with that title already exists.'))
#         return title
#
#     def clean(self):
#         cleaned_data = super(UploadZipForm, self).clean()
#         if not self['title'].errors:
#             # If there's already an error in the title, no need to add another
#             # error related to the same field.
#             if not cleaned_data.get('title', None) and not cleaned_data['gallery']:
#                 raise forms.ValidationError(
#                     _('Select an existing gallery, or enter a title for a new gallery.'))
#         return cleaned_data
#
#     def save(self, request=None, zip_file=None):
#         if not zip_file:
#             zip_file = self.cleaned_data['zip_file']
#         zip = zipfile.ZipFile(zip_file)
#         count = 1
#         if self.cleaned_data['gallery']:
#             logger.debug('Using pre-existing gallery.')
#             gallery = self.cleaned_data['gallery']
#         else:
#             logger.debug(
#                 force_text('Creating new gallery "{0}".').format(self.cleaned_data['title']))
#             )
#             # make if statement for if there is collection/category
#             gallery = Gallery.objects.create(
#                 title=self.cleaned_data['title'],
#                 slug=slugify(self.cleaned_data['title']),
#             )
#         for filename in sorted(zip.namelist()):
#             logger.debug('Reading file "{0}".'.format(filename))
#
#             if filename.startswith('__') or filename.startswith('.'):
#                 logger.debug('Ignoring file "{0}".'.format(filename))
#                 continue
#
#             if os.path.dirname(filename):
#                 logger.warning('Ignoring file "{0}" as it is in a subfolder; all images should be in the top '
#                                'folder of the zip.'.format(filename))
#                 if request:
#                     messages.warning(request,
#                                      _('Ignoring file "{filename}" as it is in a subfolder; all images should '
#                                        'be in the top folder of the zip.').format(filename=filename),
#                                      fail_silently=True)
#                 continue
#             data = zip.read(filename)
#
#             if not len(data):
#                 logger.debug('File "{0}" is empty.'.format(filename))
#                 continue
#
#             photo_title_root = self.cleaned_data['title'] if self.cleaned_data['title'] else gallery.title
