def extract_title(markdown):
    blocks = markdown.split("\n")
    title = blocks[0]

    if not title.startswith("# "):
        raise Exception("No header available")

    trimmed_string = title.split(" ")[1]

    return trimmed_string
