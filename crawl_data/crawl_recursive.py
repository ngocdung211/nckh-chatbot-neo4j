from langchain_community.document_loaders import RecursiveUrlLoader
import re
from langchain_core.load import dumpd, dumps, load, loads

from bs4 import BeautifulSoup
import json

num = 0
def bs4_extractor(html: str) -> str:
    # Initialize BeautifulSoup with a valid parser
    soup = BeautifulSoup(html, "html.parser")  # Alternatively, use "lxml" or "html5lib" if installed

    # Find the first element with the class 'irs-blog-single-col'
    target_element = soup.find(class_="irs-blog-single-col")

    if target_element:
        # Extract text from the target element
        text = target_element.get_text(separator=' ', strip=True)
        # Replace multiple whitespace characters with a single space
        cleaned_text = re.sub(r'\s+', ' ', text)
        # print(cleaned_text)

        return cleaned_text
    else:
        # Handle the case where the element isn't found
        return ""

loader = RecursiveUrlLoader(
    "https://fit.haui.edu.vn/vn",

    max_depth=15,
    # use_async=False,
    # extractor=None,
    # metadata_extractor=None,
    # exclude_dirs=(),
    # timeout=10,
    # check_response_status=True,
    continue_on_failure=True,
    extractor=bs4_extractor,
    # prevent_outside=True,
    # base_url=None,
    # ...
)

docs = loader.load()
print(docs[0].metadata)
dict_representation = dumpd(docs)


with open('fit.json', 'w', encoding="utf-8") as file:
    json.dump(dict_representation, file, indent=4, ensure_ascii=False)


