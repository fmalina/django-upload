from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from upload.forms import handle_file, save_sizes, CropForm
from upload.models import File, get_collection_model
from PIL import Image

Col = get_collection_model()


def upload(request, pk=False):
    data = request.FILES.get('file')
    res = 'error'
    if data:
        f = File(fn=data.name[:60])
        if pk:
            col = get_object_or_404(Col, pk=pk)
            f.col = col
            if not col.is_editable_by(request.user):
                return HttpResponse('not permitted')
        f.save()
        y = handle_file(data, f)
        if y:
            c = {'id': f.id, 'path': f.path(), 'crop': ''}
            if f.col:
                c['crop'] = f.col.crop
            res = render_to_string('upload/xhr.js', c)
        else:
            f.delete()
    return HttpResponse(res)


def edit(request, pk, angle=0):
    """ Handle cropping and rotation even before signup.
    """
    f = get_object_or_404(File, pk=pk)
    if f.col:
        if not f.col.is_editable_by(request.user):
            return HttpResponse('not permitted')
    p = f.path()
    try:
        im = Image.open(p)
    except IOError:
        p = p.replace('tmp', str(f.col_id))
        im = Image.open(p)
    # pass collection defined cropping onto thumbnail
    # e.g. smart crop v. middle crop from top
    crop = ''
    if f.col:
        crop = f.col.crop()
    if angle:  # handle rotation
        im.transpose({
            '90': Image.ROTATE_90,
            '270': Image.ROTATE_270
        }[angle]).save(p)
        save_sizes(f, im)
        return render(request, 'upload/reload-thumbnails.html', {
            'img': f,
            'crop': crop
        })
    else:  # or handle cropping
        form = CropForm(request.POST or None)
        if form.is_valid():
            d = form.cleaned_data
            # get starting position and cutout size
            x, y, w, h = d['x'], d['y'], d['x']+d['width'], d['y']+d['height']
            # crop image and save
            im.crop((x, y, w, h)).save(p)
            save_sizes(f, im)
        return render(request, 'upload/crop.html', {
            'img': f,
            'crop': crop,
            'form': form
        })
