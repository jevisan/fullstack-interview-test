import os
from git import Repo

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def hello():
    return "Hello from Git wrapper api"

def build_repo_stuct(repo):
    # general info
    repo_struct = {}
    repo_struct['description'] = repo.description
    repo_struct['active_branch'] = str(repo.active_branch)

    remotes = [{"name": str(remote), "url": remote.url} for remote in repo.remotes]
    repo_struct['remotes'] = remotes

    branches = []
    for branch in repo.branches:
        curr_branch = {}
        curr_branch['name'] = str(branch)
        curr_branch['commits'] = []
        commits = list(repo.iter_commits(branch))
        for commit in commits:
            curr_commit = {}
            curr_commit['hexsha'] = str(commit.hexsha)
            curr_commit['summary'] = commit.summary
            curr_commit['author'] = commit.author.name
            curr_commit['author_email'] = commit.author.email
            curr_commit['timestamp'] = str(commit.authored_datetime)
            curr_commit['count'] = str(commit.count())
            curr_commit['size'] = commit.size
            curr_branch['commits'].append(curr_commit)
        branches.append(curr_branch)

    repo_struct['branches'] = branches

    return repo_struct


def init_repo():
    repo_path = os.path.join(BASE_DIR, ".git")
    # Repo object to interact programmatically with Git repositories
    repo = Repo(repo_path)
    if not repo.bare:
        print('Repo at {} successfully loaded.'.format(repo_path))
        struct = build_repo_stuct(repo)
        return struct
    else:
        print('Could not load repository at {}'.format(repo_path))
        return None
