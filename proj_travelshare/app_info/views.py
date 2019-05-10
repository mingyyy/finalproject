import requests
from mimi import SHERPA_API_KEY


def visa_info(request):
    cs = request.POST.get("citizenship")
    d = request.POST.get("destination")
    lan = "en"
    path = f"https://requirements-api.sandbox.joinsherpa.com/v2/entry-requirements?citizenship=" \
        f"{cs}&destination={d}&language={lan}&key={SHERPA_API_KEY}"
    download = requests.get(path).json()
    for k, v in download.items():
        print(v)

