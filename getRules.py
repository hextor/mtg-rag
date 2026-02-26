
# each line skipped should be ignored if they appear elswewhere, since we don't care about the header logic
def importRules():
    start_reading = False
    target_string = "Credits\n"

    documents = []
    skip_text = []

    join_string = False

    with open('./MagicCompRules20260116.txt', encoding="utf-8") as f:
        for line in f:
            if start_reading:
                if line not in skip_text:
                    if 'Example' in line:
                        documents.append(line.rstrip())
                    elif len(documents) > 0 and documents[-1] != '' and line.rstrip() != '' and line not in skip_text:
                        documents[-1] = documents[-1] + " " + line.rstrip()
                    else:
                        documents.append(line.rstrip())
            else:
                if line.rstrip() != '':
                    skip_text.append(line)
            if target_string in line:
                skip_text.append(line)
                start_reading = True
        
        documents = list(filter(None, documents))

    return documents
