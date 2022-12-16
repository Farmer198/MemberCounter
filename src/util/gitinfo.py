import git

class Gitinfo:
    __slots__ = ("commitHash")
    
    def __init__(self) -> None:
        # commit Hash
        git_repo = git.Repo(path = "...", search_parent_directories = True)
        sha = git_repo.head.commit.hexsha
        self.commitHash = str(git_repo.git.rev_parse(sha, short = True)) 
