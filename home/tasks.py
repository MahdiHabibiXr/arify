from celery import shared_task
from django.core.files.base import ContentFile
from .models import ExportTest, Nerf, ExportUrl, Video
import requests
from lumaapi import LumaClient
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import Accounts


@shared_task
def add(x, y):
    return x + y


@shared_task
def down(nerf_id):

    exporturl_instance = ExportUrl.objects.get(nerf_id=nerf_id)
    urls = [
        exporturl_instance.thumb,
        exporturl_instance.low_model,
        exporturl_instance.med_model,
        exporturl_instance.high_model
    ]

    if (ExportTest.objects.filter(nerf_id=nerf_id).count() == 0):
        export = ExportTest.objects.create(nerf_id=nerf_id)
        nerf = Nerf.objects.get(id=nerf_id)
        title = nerf.title

        export.thumb.save(f"{title}-{nerf_id}-thumb.png",
                          ContentFile(requests.get(urls[0]).content))
        export.low_glb.save(f"{title}-{nerf_id}-low.glb",
                            ContentFile(requests.get(urls[1]).content))
        export.med_glb.save(f"{title}-{nerf_id}-med.glb",
                            ContentFile(requests.get(urls[2]).content))

        # Finalize nerf status
        nerf.file_id = export.pk
        nerf.status = True
        nerf.save()

        # send notifcation maile
        user = User.objects.get(id=nerf.user_id)
        send_email.delay(
            'واقعیت افزوده شما آماده است',
            f'مدل سه بعدی شما به نام {nerf.title} با موفقیت استخراج شد. از صفحه اصلی می‌توانید آن را مشاهده کنید',
            user.email
        )

        account = Accounts.objects.get(user = user)
        account.charge = account.charge - 1
        account.save()


@shared_task
def get_urls(nerf_id):
    if (ExportUrl.objects.filter(nerf_id=nerf_id).count() == 0):
        nerf = Nerf.objects.get(id=nerf_id)
        status = get_status(nerf.apikey, nerf.slug)

        thum_url = str(status['latestRun']['artifacts'][0]).split()[
            1].replace(',', '').replace("'", '')
        model1_url = str(status['latestRun']['artifacts'][6]).split()[
            1].replace(',', '').replace("'", '')
        model2_url = str(status['latestRun']['artifacts'][7]).split()[
            1].replace(',', '').replace("'", '')
        model3_url = str(status['latestRun']['artifacts'][8]).split()[
            1].replace(',', '').replace("'", '')

        export = ExportUrl.objects.create(
            nerf_id=nerf_id, thumb=thum_url, low_model=model1_url, med_model=model2_url, high_model=model3_url)


@shared_task
def create_capture(api_key, video_path, nerf_id):
    client = LumaClient(api_key)

    nerf_obj = Nerf.objects.get(id=nerf_id)
    slug = client.submit(video_path, nerf_obj.title)

    print(slug)
    nerf_obj.slug = slug
    nerf_obj.apikey = api_key
    nerf_obj.save()


def get_status(api_key, slug):
    url = f"https://webapp.engineeringlumalabs.com/api/v2/capture/{slug}"
    payload = {}
    headers = {
        'Authorization': f'luma-api-key={api_key}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return (response.json())


@shared_task
def update_status():
    nerfs = Nerf.objects.filter(status=False)
    for nerf in nerfs:
        exp_url = ExportUrl.objects.filter(nerf_id=nerf.pk)
        if (nerf.slug != '' and exp_url.count() == 0):  # if(uploaded to luma & doesn't have url)
            stat = get_status(nerf.apikey, nerf.slug)
            if (stat['latestRun']['currentStage'] == 'Done'):
                if (exp_url.count() == 0):
                    get_urls.delay(nerf.pk)
                    down.delay(nerf.pk)


@shared_task
def send_email(sbj, msg, receiver):
    send_mail(
        sbj,  # subject
        msg,  # message
        "arifygroup@gmail.com",  # from
        [receiver],  # to
        fail_silently=False,
    )
