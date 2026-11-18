import mimetypes
import os
import re

from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.http import FileResponse, Http404, HttpResponse
from django.utils._os import safe_join

CHUNK = 8 * 1024 * 1024  # отдаём не больше 8 МБ за один запрос


def serve_media(request, path):
    """Отдаёт файлы из MEDIA_ROOT с поддержкой Range, чтобы работала перемотка трека."""
    try:
        full = safe_join(settings.MEDIA_ROOT, path)
    except SuspiciousFileOperation:
        raise Http404
    if not os.path.isfile(full):
        raise Http404

    size = os.path.getsize(full)
    ctype = mimetypes.guess_type(full)[0] or 'application/octet-stream'
    m = re.match(r'bytes=(\d*)-(\d*)$', request.headers.get('Range', ''))

    if m and (m.group(1) or m.group(2)):
        if m.group(1):
            start = int(m.group(1))
            end = int(m.group(2)) if m.group(2) else size - 1
        else:
            start = max(size - int(m.group(2)), 0)
            end = size - 1
        if start >= size or start > end:
            resp = HttpResponse(status=416)
            resp['Content-Range'] = f'bytes */{size}'
            return resp
        end = min(end, size - 1, start + CHUNK - 1)
        with open(full, 'rb') as f:
            f.seek(start)
            data = f.read(end - start + 1)
        resp = HttpResponse(data, status=206, content_type=ctype)
        resp['Content-Range'] = f'bytes {start}-{end}/{size}'
        resp['Content-Length'] = str(len(data))
    else:
        resp = FileResponse(open(full, 'rb'), content_type=ctype)
    resp['Accept-Ranges'] = 'bytes'
    return resp
