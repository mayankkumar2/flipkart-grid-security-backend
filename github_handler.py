from dataclasses import dataclass, asdict
from github import Github
import statistics
import os

@dataclass
class RepoStats:
    no_of_contributors: int
    weekly_activity_avg: float
    weekly_activity_stdev: float
    pr_count: int
    fork_count: int
    stargazers_count: int
    subscribers_count: int
    watchers_count: int
    closed_issues_count: int
    closed_to_open_issues_ratio: float
    contributors_popularity: float
    commits_count: int


def calc_repo_stats(repo_name: str):
    g = Github(os.getenv("GITHUB_KEY"))
    repo = g.get_repo(repo_name)

    def user_popularity(user):
        acc_stars = 0
        for repo in user.get_repos():
            if repo.fork:
                continue
            acc_stars += repo.stargazers_count
        return acc_stars
    contributor_count = 0
    commits_count = 0
    contributors_list = list()
    for act in repo.get_stats_contributors():
        contributors_list.append((act.author, act.total))
        commits_count += act.total
        contributor_count += 1

    commit_stats_activity = list()
    for act in repo.get_stats_commit_activity():
        commit_stats_activity.append(act.total)

    statistics.mean(commit_stats_activity)
    statistics.stdev(commit_stats_activity)
    popularity_index = 0

    for (user, user_contribution_count) in contributors_list:
        user_popularity_stars = user_popularity(user)
        popularity_index += (user_contribution_count /
                             commits_count) * (user_popularity_stars)
        #print(user, (user_contribution_count/commits_count) * (user_popularity_stars), user_contribution_count, user_popularity_stars)

    open_issues_count = 0
    closed_issues_count = 0
    else_count = 0
    for issue in repo.get_issues(state='all'):
        if issue.state == 'open':
            open_issues_count += 1
        elif issue.state == 'closed':
            closed_issues_count += 1
        else:
            else_count += 1
    all_pr_count = 0
    for _ in repo.get_pulls(state='all'):
        all_pr_count += 1
    return RepoStats(contributor_count,
                     statistics.mean(commit_stats_activity),
                     statistics.stdev(commit_stats_activity),
                     all_pr_count,
                     repo.forks_count,
                     repo.stargazers_count,
                     repo.subscribers_count,
                     repo.watchers_count,
                     closed_issues_count,
                     closed_issues_count/open_issues_count,
                     popularity_index,
                     commits_count)
