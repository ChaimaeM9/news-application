from django.shortcuts import render
from newapp import settings
import requests
from django.http import HttpResponse
from django.http import JsonResponse


def Home(request):
    page = request.GET.get('page', 1)
    search = request.GET.get('search', None)

    if search is None:
        # get the top news
        url ="https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format("us", 1, settings.API_KEY)
    else:
        # get the search query
        url ="https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(search, "popularity", page, settings.API_KEY)

    r = requests.get(url=url)
    data = r.json()
    if data["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")
    data = data["articles"]
    context = {
        "success": True,
        "data": [],
        "search": search,
    }

    # separating data
    for i in data:
        context["data"].append({
            "title": i["title"],
            "description": i["description"],
            "url": i["url"],
            "image": "" if i["urlToImage"] is None else i["urlToImage"],
            "publishedAt": i["publishedAt"],
        })

    return render(request, 'index.html', context=context)

def loadcontent(request):
    try:
        page = request.GET.get('page', 1)
        search = request.GET.get('search', None)
        # url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
        #     "Technology","popularity",page,settings.API_KEY
        # )
        if search is None or search=="top":
            url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
                "us",page,settings.API_KEY
            )
        else:
            url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
                search,"popularity",page,settings.API_KEY
            )
        print("url:",url)
        r = requests.get(url=url)

        data = r.json()
        if data["status"] != "ok":
            return JsonResponse({"success":False})
        data = data["articles"]
        context = {
            "success": True,
            "data": [],
            "search": search,
        }
        for i in data:
            context["data"].append({
                "title": i["title"],
                "description":  "" if i["description"] is None else i["description"],
                "url": i["url"],
                "image": " " if i["urlToImage"] is None else i["urlToImage"],
                "publishedAt": i["publishedAt"]
            })

        return JsonResponse(context)

    except Exception as e:
        return JsonResponse({"success": False})