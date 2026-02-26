Overview:
- Download existing LLM
- Install chromadb to create a local DB instance
    - create a collection for the input to be stored
- Download an embedding model to create input into _vector embeddings_
    - long arrays of numbers that represent semantic meaning for a given sequence of text
- Enumerate over the input and embed them
- Take the vector embeddings and add them to your new collection

Retrieve:
- take in the input
- embed the input
- query the collection using the vector embedding
- parse the result

Generate:
- take the result and feed it into a separate prompt 

Errors and Resolutions:
- ollama._types.ResponseError: the input length exceeds the context length (status code: 400)
    - token max length is 512 or 256

TODOs:
- Check out persistent client, so we don't need to keep loading everything at the start of the client.
    - https://docs.trychroma.com/reference/python/client#persistentclient
    - high disk usage so keep that in mind


The default interaction for Gemma3 hallucinates, provides dead links, and does not return the ruling it based its logic off of. So building a tool that extends Gemma3 with the use of RAG to get the correct ruling according the organization for regular play.


Notes:
- generate vs chat apis
    - generate gives a one shot response to the prompt, doesn't carry over previous prompt history
        - good for generative tasks like getting keywords and such
    - chat is good for keeping context of the questions the use asks
        - need to experiment to see how quickly the data quality drops if the user "deviates" from the script