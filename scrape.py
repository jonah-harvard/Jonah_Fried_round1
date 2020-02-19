import requests
from bs4 import BeautifulSoup
import re
import sys
from collections import defaultdict
from random import randint
import pickle

SITE = "http://www.satirev.org"


def check_status(code):
    "exits the program if page couldn't be reached"
    if code != 200:
        print("failed to retrieve page")
        exit(1)


if __name__ == "__main__":
    # Command line args. Defaults to taking just first page. If there is one arg then
    # Takes pages 0-arg. If there are two args, takes pages arg1-arg2.
    if len(sys.argv) == 1:
        page_min = 0
        page_max = 1
    elif len(sys.argv) == 2:
        page_min = 0
        page_max = int(sys.argv[1])
    else:
        page_min = int(sys.argv[1])
        page_max = int(sys.argv[2])

    article_texts = []  # we build up a list of all the paragraphs in each article
    for page_num in range(page_min, page_max):
        print("processing page index:", page_num)
        # get all the links on a front page tab
        request = requests.get(f"{SITE}/us?page={page_num}#.Xk2RKxNKh25")
        check_status(request.status_code)
        soup = BeautifulSoup(request.content, "html.parser")
        # convert them to proper links
        links = [
            article.find("a")["href"] for article
            in soup.find_all("div", id=re.compile("node-*"))
        ]
        for link in links:
            article_page = requests.get(SITE + link)  # get an article
            check_status(request.status_code)
            article_soup = BeautifulSoup(article_page.content, "html.parser")
            article_texts.append("\n".join([
                p.text for p
                in article_soup.find("div", id="article-content").find_all("p")
            ]))
    # get a list of all the words in all the articles
    words = re.split("[ \n\t,.;:\"'!?]", "\n".join(article_texts).lower())

    # propogate the markov chain
    markov = defaultdict(lambda: (0, defaultdict(int)))
    for ind, word in enumerate(words[:-1]):
        appearences, word_distribution = markov[word]
        word_distribution[words[ind+1]] += 1
        markov[word] = (appearences+1, word_distribution)

    # use the markov chain to predict text
    generated_text = ["the"]
    for _ in range(400):
        last_word = generated_text[-1]
        appearences, word_distribution = markov[last_word]
        dart = randint(0, appearences)
        for word, weight in word_distribution.items():
            dart -= weight
            if dart <= 0:
                generated_text.append(word)
                break

# you should pickle the markov chain for later use

    print(len(generated_text))
    with open("./output.txt", "w") as f:
        f.write(" ".join(generated_text))
