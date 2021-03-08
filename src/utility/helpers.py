def get_only_files_with_extensions(files, extensions):
    extensions = tuple(extensions)
    source_files = []

    for file_name in files:
        if file_name.endswith(extensions):
            source_files.append(file_name)

    return source_files


def get_graphql_attributes(graphql_parameters):
    attributes = ""

    for parameter in graphql_parameters:
        attributes += (parameter.get("query") + "\n")

    return attributes


def is_similar(pr, min_max_source_files_changed, min_max_additions, min_max_deletions):
    if "changedSourceFiles" not in pr:
        print("did not find")
    return (
            "changedSourceFiles" in pr and
            within_range_incl(len(pr.get("changedSourceFiles")), min_max_source_files_changed) and
            within_range_incl(pr.get("additions"), min_max_additions) and
            within_range_incl(pr.get("deletions"), min_max_deletions)
    )


def within_range_incl(val, bounds):
    return bounds[0] <= val <= bounds[1]


def has_bot(pr, bot_prs):
    for bot_pr in bot_prs:
        if pr.get("createdAt") == bot_pr.get("createdAt"):
            return True
    return False


def pri():
    print("pri")