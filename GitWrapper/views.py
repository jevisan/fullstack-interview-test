from django.shortcuts import render
from django.http import HttpResponse

from modules.gitwrapperapi import init_repo

def index(request):
    repo_struct = init_repo()
    print(repo_struct)
    return HttpResponse("Hello world. You're in the GitWrapper index. Check the console to view repo structure :)")
