import requests
from bs4 import BeautifulSoup

class Page:
    def __init__(self, title, parent=None):
        self.title = title
        self.parent = parent
        
    def __eq__(self, p2):
        return self.title == p2.title
        
class Queue:
    def __init__(self, elements=[]):
        self.elements = elements
        
    def pop(self):
        return self.elements.pop()
        
    def insert(self, index, element):
        self.elements.insert(index, element)
        
def main(start, end):
    base_URL = "https://en.wikipedia.org/wiki/"
    current = Page(start)
    solution = []
    LIFO = Queue([current])
    while LIFO:
        P = LIFO.pop()
        URL = base_URL + P.title
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        links = soup.find_all('a', href=lambda href: href and '/wiki/' in href.lower())
        
        for l in links:
            title = ((l['href'].split('/wiki/')[1]).split('#')[0]).split('&')[0]
            
            if title == end:
                parent = P.parent
                solution.append(Page(end, P))
                solution.append(P)
                while parent is not None and parent.title is not None:
                    solution.append(P.parent)
                    print(P.parent.title)
                    parent = P.parent.parent
                LIFO = None
                break
                
            LIFO.insert(0, Page(title, P))

    for link in solution[::-1]:
        print("Visited /wiki/" + str(link.title))


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--starting_page', '-s', help="Wikipedia page to start searching from")
    parser.add_argument('--finishing_page', '-f', default="Kevin_Bacon", help="Wikipedia page to search for, default is Kevin_Bacon")
    
    args = parser.parse_args()
    
    main(args.starting_page, args.finishing_page)
