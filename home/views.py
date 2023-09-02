from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Nerf, Video, ExportTest, ExportUrl, ApiKey
from django.contrib import messages
from .forms import NerfCreateForm, NerfEditForm, ApiKeyCreatForm
from lumaapi import LumaClient
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from home.tasks import down, get_urls, create_capture
from django.contrib.auth.models import User
from accounts.models import Accounts
# /


@login_required
def home(request):
    all_nerfs = Nerf.objects.filter(user_id=request.user.id).order_by("-id")

    nerfs = []
    for nerf in all_nerfs:
        nrf = []
        nrf.append(nerf)
        if(nerf.status == True):
            nrf.append(ExportTest.objects.get(nerf_id = nerf.id))
        else:
            continue
        nerfs.append(nrf)

    data = {
        'nerfs': nerfs,
        'title': 'Home',
        'exports': nerfs
    }

    for nerf in nerfs:
        print(nerf[0])
        print(nerf[1])
        print('---------')

    # for nerf in all_nerfs:
    #     print(exports[f'{nerf.id}'].thumb.url)
    return render(request, 'home.html', context=data)


# /view
# @login_required
def view(request, nerf_id):
    nerf_data = Nerf.objects.filter(id=nerf_id)

    if (nerf_data.count() != 0):
        nerf_data = nerf_data[0]
        video_data = Video.objects.get(
            id=Nerf.objects.get(id=nerf_id).video_id)
        export_data = ExportTest.objects.get(nerf_id=nerf_id)

        urls = ExportUrl.objects.get(nerf_id=nerf_id)
        data = {
            'nerf': nerf_data,
            'title': video_data.title,
            'video': video_data.video,
            'export': export_data
        }

        return render(request, 'view.html', context=data)
    else:
        messages.success(
            request, f'You are looking for a page that does not exists!', extra_tags='danger')
        return redirect('home')

# /delete


@login_required
def delete(request, nerf_id):
    nerf = Nerf.objects.get(id=nerf_id)
    if (request.user.id == nerf.user_id):
        Nerf.objects.get(id=nerf_id).delete()
        messages.success(
            request, f'The {Nerf.objects.get(id = nerf_id).title} has been deleted successfully', extra_tags='success')
    else:
        messages.success(
            request, f'You are not the owner of this capture.', extra_tags='danger')

    return redirect('home')

# /create


@login_required
def create(request):
    if request.method == 'POST':
        acc = Accounts.objects.get(user = request.user)
        if(acc.charge >= 1):
            #allowed to create
            form = NerfCreateForm(request.POST, request.FILES)

            if (form.is_valid()):
                cd = form.cleaned_data
                video = form.save()

                nerf = Nerf.objects.create(
                    video_id=video.pk, title=cd['title'], user_id=request.user.id)

                apikeys = ApiKey.objects.filter(active=True)
                apikey = apikeys[0]

                # #call the api and create the capture by video, this func should be done ASYNCHRONOUS
                create_capture.delay(apikey.key, video.video.path, nerf.pk)

                #Getting a working apikey
                if (apikey.remaining > 1):
                    apikey.remaining = apikey.remaining - 1
                    apikey.save()
                elif (apikey.remaining <= 1):
                    apikey.active = False
                    apikey.remaining = apikey.remaining - 1
                    apikey.save()


                messages.success(request, 'Created successfully, you will receive an email when your 3D is ready.',
                                extra_tags='success')
                return JsonResponse({'success': 'true'})
        else :
            messages.success(request, "You don't have enough credit",
                                extra_tags='danger')
            form = NerfCreateForm()
            return JsonResponse({'success': 'false'})
    else:
        form = NerfCreateForm()

    return render(request, 'create.html', context={'form': form})


# /edit
@login_required
def edit(request, nerf_id):
    nerf_instance = Nerf.objects.get(id=nerf_id)
    if request.method == 'POST':
        form = NerfEditForm(request.POST, instance=nerf_instance)
        if (form.is_valid()):
            form.save()
            messages.success(
                request, 'Your Nerf updated successfully', extra_tags='success')
            return (redirect('view', nerf_id))
    else:
        form = NerfEditForm(instance=nerf_instance)

    return render(request, 'edit.html', context={'form': form, 'nerf_title': nerf_instance.title})


# /down
def download_url(request, nerf_id):
    exporturl_instance = ExportUrl.objects.get(nerf_id=nerf_id)
    nerf_instance = Nerf.objects.get(id=nerf_id)

    image_url = exporturl_instance.thumb
    file1_url = exporturl_instance.low_model
    file2_url = exporturl_instance.med_model
    file3_url = exporturl_instance.high_model

    down.delay(nerf_id, nerf_instance.title)

    return JsonResponse({'data': 'success'})


@login_required
def add_key(request):
    # check if it's admin
    if (request.user.id == 1):
        # check if filled the form
        if request.method == 'POST':
            form = ApiKeyCreatForm(request.POST)
            if (form.is_valid()):
                cd = form.cleaned_data
                apis = ApiKey.objects.filter(key=cd['key'])
                if (apis.count() == 0):
                    form.save()
                    messages.success(
                        request, 'Your Nerf updated successfully', extra_tags='success')
                else:
                    messages.success(
                        request, 'Key exists!!', extra_tags='danger')
                return (redirect('addkey'))
        else:
            form = ApiKeyCreatForm()

        return render(request, 'apikeyadd.html', context={'form': form})

    # error if not admin
    else:
        messages.success(
            request, 'Your Nerf updated successfully', extra_tags='danger')
        return (redirect('view'))


def dtv(request):
    return render(request, 'denitte.html')

def view_wall_ar(request,wall_id):
    exports = ExportTest.objects.all()
    img1 = exports[0].thumb.url
    img2 = exports[1].thumb.url
    img3 = exports[2].thumb.url

    data = {
        'image1' : img1,
        'image2' : img2,
        'image3' : img3,
        'model1' : exports[0].low_glb.url,
        'model2' : exports[1].low_glb.url,
        'model3' : exports[2].low_glb.url
    }
    return render(request, 'pictureframe.html', context=data)
##############################################################################################################


def get_credits(api_key):
    client = LumaClient(api_key)
    return (client.credits())
