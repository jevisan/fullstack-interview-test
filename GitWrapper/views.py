from django.shortcuts import render
from django.http import HttpResponse

from modules.gitwrapperapi import GitWrapper

def index(request):
    gitwrapper = GitWrapper()
    repo_struct = gitwrapper.init_repo()
    context = {
        'repository': repo_struct
    }
    print(repo_struct)
    # return HttpResponse("Hello world. You're in the GitWrapper index. Check the console to view repo structure :)")
    return render(request, "GitWrapper/index.html", context)
