import git

class Gitinfo:
    __slots__ = ("client", "commitHash")
    
    def __init__(self, client) -> None:
        self.client = client
        # commit Hash
        git_repo = git.Repo(path = self.client.dirname, search_parent_directories = True)
        sha = git_repo.head.commit.hexsha
        self.commitHash = str(git_repo.git.rev_parse(sha, short = True)) 
