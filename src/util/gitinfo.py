from __future__ import annotations

import git
from typing import TYPE_CHECKING

__all__ = (
    'Gitinfo'
)

if TYPE_CHECKING:
    from ..MemberCounter import MemberCounter

class Gitinfo:

    __slots__ = (
        "client",
        "commitHash"
    )
    
    def __init__(self, client: MemberCounter) -> None:
        self.client: MemberCounter = client
        # commit Hash
        git_repo = git.Repo(path = self.client.dirname, search_parent_directories = True)
        sha = git_repo.head.commit.hexsha
        self.commitHash = str(git_repo.git.rev_parse(sha, short = True)) 
