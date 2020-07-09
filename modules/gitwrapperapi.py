import os
from git import Repo

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class GitWrapper():

    def __init__(self):
        self.repo_path = ""
        self.repo = None

    def get_repo_struct(self):
        return self.build_repo_stuct(self.repo)

    def init_repo(self):
        self.repo_path = os.path.join(BASE_DIR, ".git")
        # Repo object to interact programmatically with Git repositories
        self.repo = Repo(self.repo_path)
        if not self.repo.bare:
            print('Repo at {} successfully loaded.'.format(self.repo_path))
        else:
            print('Could not load repository at {}'.format(self.repo_path))
            return None

    def get_repo_branches_list(self):
        return self.repo.branches

    def get_commits_by_branch(self):
        """
        Returns dict with all branches in project and its respective commits
        excluding commits from other branches
        """
        # Workaround for exluding commits from parent branches
        # So current branch only contains its own commits
        other_shas = set()
        branch_list = self.repo.branches
        branch_list.reverse() # Trick to traverse the branches in oldest-newest order

        branches = []
        for branch in branch_list:
            curr_branch = {}
            curr_branch['name'] = str(branch)
            curr_branch['commits'] = []
            commits = list(self.repo.iter_commits(branch))
            for commit in commits:
                if commit.hexsha not in other_shas:
                    curr_commit = {}
                    curr_commit['hexsha'] = str(commit.hexsha)
                    curr_commit['summary'] = commit.summary
                    curr_commit['author'] = commit.author.name
                    curr_commit['author_email'] = commit.author.email
                    curr_commit['timestamp'] = str(commit.authored_datetime)
                    curr_commit['count'] = str(commit.count())
                    curr_commit['size'] = commit.size
                    curr_branch['commits'].append(curr_commit)
                    other_shas.add(commit.hexsha)
            branches.append(curr_branch)
        return branches

    def get_commits_of_branch(self, branch):
        """
        Returns dict with commits of specified branch
        excludes commits from other branches
        """
        branches = self.get_commits_by_branch()
        for b in branches:
            if b['name'] == branch:
                return b

    def build_repo_stuct(self, repo):
        # general info
        repo_struct = {}
        repo_struct['description'] = self.repo.description
        repo_struct['active_branch'] = str(self.repo.active_branch)
        # remotes info
        remotes = [{"name": str(remote), "url": remote.url} for remote in self.repo.remotes]
        repo_struct['remotes'] = remotes
        # repo branches
        repo_struct['branches'] = self.get_commits_by_branch()
        return repo_struct


# Testing, testing...
if __name__ == '__main__':
    gitwrapper = GitWrapper()
    gitwrapper.init_repo()
    repo_struct = gitwrapper.get_repo_struct()
    # repo_branches = gitwrapper.get_repo_branches_list()
    print(repo_struct)
    print("gitwrapper branch: " + str(gitwrapper.get_commits_of_branch('gitwrapper')))
