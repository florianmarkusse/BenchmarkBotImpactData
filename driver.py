from utility import file_management
from utility import helpers
from mining.graphql import pull_requests
from mining.rest import changed_files

# Get projects to collect PR data for
projects = file_management.get_projects_to_mine()

# Get token for GitHub API
token = file_management.get_token()

# Get the GraphQL parameters, containing seach parameters and description
graphql_parameters = file_management.get_graphql_parameters()

for project in projects:

    owner = project.get("owner")
    repo = project.get("repo")
    botQuery = project.get("botQuery")
    allQuery = project.get("allQuery")

    bot_prs = pull_requests.get_prs(
        owner,
        repo,
        botQuery,
        helpers.get_graphql_attributes(graphql_parameters),
        token
    )

    number_source_files_changed = []
    additions = []
    deletions = []

    # Add which files were changed in this PR.
    # In GraphQL it is only possible to get the number of files changed which includes documentation files
    # which is undesirable to get like to like comparison of PRs with bot usage and without bot usage.
    for bot_pr in bot_prs:

        bot_pr["changedFiles"] = changed_files.get_all_changed_files(
            owner, repo, bot_pr.get("number")
        )
        if isinstance(bot_pr.get("changedFiles"), list):
            bot_pr["changedSourceFiles"] = helpers.get_only_files_with_extensions(
                bot_pr.get("changedFiles"),
                file_management.get_extensions()
            )
            number_source_files_changed.append(
                len(
                    bot_pr.get("changedSourceFiles")
                )
            )

        additions.append(bot_pr.get("additions"))
        deletions.append(bot_pr.get("deletions"))

    print(additions)
    print(len(additions))

    print(deletions)
    print(len(deletions))

    print(number_source_files_changed)
    print(len(number_source_files_changed))

    print(bot_prs[0])

    print(len(bot_prs))
