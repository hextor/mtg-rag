import chromadb
import ollama
import numpy as np
import getRules

# create chromadb client and collection
client = chromadb.PersistentClient()
collection = client.get_or_create_collection(name="rules")

# default size is 16?
print(collection.__sizeof__())

# store each document in a vector embedding database
# 16 means it's empty
if collection.count() == 0:
    documents = getRules.importRules()

    for i, d in enumerate(documents):
        if len(d.split(' ')) > 200:
            print(d)
            print('skipping!! 🍟🍟')
            continue
        response = ollama.embed(model="mxbai-embed-large", input=d) #, truncate=True)
        embeddings = response["embeddings"]
        collection.add(
            ids=[str(i)],
            embeddings=embeddings,
            documents=[d]
        )

def InputPrompt(inputStr):
    # take in a prompt
    # initPrompt = "Can a card with persist return to the battefield if it has wither counters?"
    # secondaryPrompt = "What if the persist card fought something and died, and didn't have counters beforehand?"
    initPrompt = inputStr

    # find rules based off the keywords and prompt
    output = ollama.generate(
        model="gemma3",
        prompt=f"Using the provided prompt, create a comma-delimited list of keywords: {initPrompt}"
    )

    print(output.response)
    keywords = output.response.rstrip()

    keywordArr = [x.strip() for x in keywords.split(',')]

    # add the initial prompt at the end
    keywordArr.append(initPrompt)

    allDocs = []

    # retrieve the data - for each keyword and the prompt
    for index, keyword in enumerate(keywordArr):
        print(f"searching keyword: {keyword}")
        prompt = keyword

        response = ollama.embed(
            model="mxbai-embed-large",
            input=prompt
        )

        np_arr = np.array(response["embeddings"])

        results = collection.query(
            query_embeddings=np_arr,
            n_results=4
        )

        data = results["documents"]

        if data is not None:
            print(data[0])
            allDocs.extend(data[0])

    # Filter through supplemental rule checks
    output = ollama.generate(
        model="gemma3",
        prompt=f"Whenever the text \"See Rule\" appears, add the rule identifier to a comma-delimited list of keywords. Only return the list. Using this data: {allDocs}."
    )

    keywords = output.response.rstrip()

    keywordArr = [x.strip() for x in keywords.split(',')]

    for index, keyword in enumerate(keywordArr):
        print(f"searching keyword: {keyword}")
        prompt = keyword

        response = ollama.embed(
            model="mxbai-embed-large",
            input=prompt
        )

        np_arr = np.array(response["embeddings"])

        results = collection.query(
            query_embeddings=np_arr,
            where_document={"$regex": f"{keyword}.+$"},
            n_results=4
        )

        data = results["documents"]

        if data is not None:
            print(data[0])
            allDocs.extend(data[0])


    # generate a response combining the prompt and data we retrieved in step 2
    output = ollama.chat(
        model="gemma3",
        messages=[{ "role": "user", "content": f"Using what you know along with thie supplementary data: {allDocs}. Respond to this prompt: {initPrompt}", "assistant": "According to the Oracle:"}],
        think=False,
        stream=False,
    )

    print(output.message.content)

    return output.message.content