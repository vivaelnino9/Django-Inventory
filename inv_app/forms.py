from django import forms
from inv_app.models import User, Inv_User
from photologue.models import Photo
from photologue.forms import UploadZipForm as UploadZipForm


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class Inv_UserForm(forms.ModelForm):
    class Meta:
        model = Inv_User
        fields = ('first_name', 'last_name')

class UploadPhotoZipForm(UploadZipForm):
    zip_file = forms.FileField()
    title = forms.CharField(label= 'Title',
                            max_length=250,
                            required=True,
                            help_text='All uploaded photos will be given a title made up of this title + a '
                                        'sequential number.')
    caption = forms.CharField(label= 'Caption',
                              required=False,
                              help_text= 'Caption will be added to all photos.')
    is_public = forms.BooleanField(label='Is public',
                                   initial=True,
                                   required=False,
                                   help_text= 'Uncheck this to make the uploaded '
                                               'photographs private.')
    def clean_zip_file(self):
        """Open the zip file a first time, to check that it is a valid zip archive.
        We'll open it again in a moment, so we have some duplication, but let's focus
        on keeping the code easier to read!
        """
        zip_file = self.cleaned_data['zip_file']
        try:
            zip = zipfile.ZipFile(zip_file)
        except BadZipFile as e:
            raise forms.ValidationError(str(e))
        bad_file = zip.testzip()
        if bad_file:
            zip.close()
            raise forms.ValidationError('"%s" in the .zip archive is corrupt.' % bad_file)
        zip.close()  # Close file in all cases.
        return zip_file
    def clean_title(self):
        title = self.cleaned_data['title']
        if title and Photo.objects.filter(title=title).exists():
            raise forms.ValidationError(_('A photo with that title already exists.'))
        return title
    def clean(self):
        cleaned_data = super(UploadPhotoZipForm, self).clean()
        if not self['title'].errors:
            # If there's already an error in the title, no need to add another
            # error related to the same field.
            if not cleaned_data.get('title', None):
                raise forms.ValidationError(('Enter a title for the new photo.'))
        return cleaned_data
    def save(self, request=None, zip_file=None):
        if not zip_file:
            zip_file = self.cleaned_data['zip_file']
        zip = zipfile.ZipFile(zip_file)
        count = 1
            # photo.sites.add(current_site)
        for filename in sorted(zip.namelist()):

            logger.debug('Reading file "{0}".'.format(filename))

            if filename.startswith('__') or filename.startswith('.'):
                logger.debug('Ignoring file "{0}".'.format(filename))
                continue

            if os.path.dirname(filename):
                logger.warning('Ignoring file "{0}" as it is in a subfolder; all images should be in the top '
                               'folder of the zip.'.format(filename))
                if request:
                    messages.warning(request,'Ignoring file "{filename}" as it is in a subfolder; all images should '
                                       'be in the top folder of the zip.'.format(filename=filename),
                                     fail_silently=True)
                continue

            data = zip.read(filename)

            if not len(data):
                logger.debug('File "{0}" is empty.'.format(filename))
                continue

            photo_title_root = self.cleaned_data['title'] if self.cleaned_data['title'] else photo.title

            # A photo might already exist with the same slug. So it's somewhat inefficient,
            # but we loop until we find a slug that's available.
            while True:
                photo_title = ' '.join([photo_title_root, str(count)])
                slug = slugify(photo_title)
                if Photo.objects.filter(slug=slug).exists():
                    count += 1
                    continue
                break

            photo = Photo(title=photo_title,
                          slug=slug,
                          caption=self.cleaned_data['caption'],
                          is_public=self.cleaned_data['is_public'])

            # Basic check that we have a valid image.
            try:
                file = BytesIO(data)
                image = Image.open(file)
                image.verify()
            except Exception:
                # Pillow (or PIL) doesn't recognize it as an image.
                # If a "bad" file is found we just skip it.
                # But we do flag this both in the logs and to the user.
                logger.error('Could not process file "{0}" in the .zip archive.'.format(filename))
                if request:
                    messages.warning(request, 'Could not process file "{0}" in the .zip archive.'.format(
                                         filename),
                                     fail_silently=True)
                continue

            contentfile = ContentFile(data)
            photo.image.save(filename, contentfile)
            photo.save()
            photo.sites.add(current_site)
            count += 1

        zip.close()

        if request:
            messages.success(request,'The photos have been added',fail_silently=True)
