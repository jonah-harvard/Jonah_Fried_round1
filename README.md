# satireVcomp1


## Description
In this script, I scrape [the Satire V website](http://www.satirev.org/us?page=0#.Xk2jtBNKh27). First, I look through the front page to find the all of the links to articles, and then scrape each article for its text. Once all the text has been collected, I use a simple markov chain trained on the collected text to generate new text.


## Usage
Simply run `python scrape.py` to scrape just the first page's articles. If you want to scrape more articles, use `python scrape.py ind1 ind2` and the articles on pages with an index in \[ind1, ind2) will be scraped.

## Packages 
This script uses the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup) package and the [requests](https://2.python-requests.org/en/latest/user/install/#install) package. 
