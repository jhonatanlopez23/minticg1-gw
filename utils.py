import bson


def clean_path(path):
    parts = path.split("/")
    for idx, part in enumerate(parts):
        if bson.ObjectId.is_valid(part):
            parts[idx] = '?'
    return "/".join(parts)
