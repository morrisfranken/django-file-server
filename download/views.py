# from django.contrib.auth.decorators import login_required
# This module is meant for checking user-permissions to download certain files.
# this only works in combination with apache & XSendFile module (see current apache virtualhost file)

from os.path import join
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from sendfile import sendfile
from home.models import Uploads


@login_required
def download_private(request, localpath):
    return sendfile(request, localpath)


def download(request, download_path):
    localpath = join(settings.MEDIA_ROOT, download_path)
    upload = get_object_or_404(Uploads, file=download_path)
    print(f"download [{request.user.email if request.user.is_authenticated else 'anonymouse'} : {'private' if upload.is_private else 'public'}] {download_path}")
    if upload.is_private:
        return download_private(request, localpath)
    else:
        return sendfile(request, localpath)
