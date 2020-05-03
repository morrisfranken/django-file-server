import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils.datastructures import MultiValueDict
from django.conf import settings
import django_tables2 as tables
from django.utils.html import mark_safe

from .forms import UploadForm
from . import models

class UploadsTable(tables.Table):
    delete = tables.Column("Delete", accessor='id', orderable=False)

    def render_delete(self, record):
        return mark_safe(f"<a onclick=\"delete_file('{record.id}', '{record.file.name}')\" href=\"javascript:void(0);\">&#x274C;</a>")

    def render_is_private(self, record):
        checked = "checked=1" if record.is_private else ""
        return mark_safe(f"""<input type="checkbox" {checked} onclick="set_private(this, '{record.id}');">""")

    class Meta:
        model = models.Uploads
        attrs = {'class': 'paleblue'}
        exclude = ("id", "user", )
        sequence = ('created_at', 'file', 'is_private', 'delete')

@login_required
def home(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        print(f"len = {len(files)}")
        url_list = []
        if not files:
            return HttpResponse(status=400)
        for file in files:
            print(file)
            form = UploadForm(request.POST, MultiValueDict({'file' : [file,]}))
            if form.is_valid():
                candidate = form.save(commit=False)
                candidate.user = request.user
                candidate.save()
                form.save(request.user)
                url_list.append(request.build_absolute_uri(candidate.file.url))
            else:
                return HttpResponse(status=400)
        return HttpResponse(json.dumps(url_list), content_type='application/json')
    else:
        form = UploadForm()
        upload_table = UploadsTable(models.Uploads.objects.filter(user=request.user).order_by('-created_at'))
        return render(request, 'home.html', {'form': form, 'table' : upload_table})

@login_required
def delete_file(request, file_id):
    if request.method == 'POST':
        upload = get_object_or_404(models.Uploads, id=file_id)
        if upload.user == request.user:
            upload.delete()
            return HttpResponse(status=200)
        raise PermissionDenied()


@login_required
def set_private(request, file_id):
    if request.method == 'POST':
        upload = get_object_or_404(models.Uploads, id=file_id)
        value = request.POST['private'] == "true"
        print(f"request.POST['private'] = {request.POST['private']}")
        print(f"value = {value}")
        if upload.user == request.user:
            upload.is_private = value
            upload.save(update_fields=['is_private'])
            return HttpResponse(status=200)
        raise PermissionDenied()
