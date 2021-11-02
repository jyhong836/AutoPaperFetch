"""Automatically search and download papers from conference.

python paper_fetcher.py federated --download
"""
import os
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import arxiv
from fuzzywuzzy import fuzz
import argparse


class NeurIPSPaperSearch(object):
    venue = 'NeurIPS'
    year = 2021
    accepted_paper_url = 'https://nips.cc/Conferences/2021/AcceptedPapersInitial'

    def __init__(self) -> None:
        self.all_paper_titles = None

    def cache_all_titles(self):
        html_text = requests.get(self.accepted_paper_url).text
        soup = BeautifulSoup(html_text, 'html.parser')

        all_paper_titles = [bold_txt.text for bold_txt in soup.find_all('b')]
        for p in all_paper_titles[:2]:
            print(f" Drop: {p}")
        all_paper_titles = all_paper_titles[2:]  # remove two
        print(f'Found {len(all_paper_titles)} papers in {self.venue}{self.year}')
        self.all_paper_titles = all_paper_titles

    def find(self, keyword, return_titles=True):
        print(f"Search for papers with keyword: {keyword}")
        cnt = 0
        freq_cnt = defaultdict(int)
        matched_papers = []
        for p in self.all_paper_titles:
            if keyword in p.lower():
                # print(p)
                if return_titles:
                    matched_papers.append(p)
                else:
                    matched_papers.append(Paper(p))
                cnt += 1
                for w in p.split(' '):
                    freq_cnt[w] += 1
        print(f"Found {cnt} papers with keyword: {keyword}")
        # sorted_keywords = [k for k, v in sorted(freq_cnt.items(), key=lambda item: item[1], reverse=True)]
        # print(f"keywords")
        # for kw in sorted_keywords[1:]:
        #     if freq_cnt[kw] < 2:
        #         break
        #     print(f"  {kw} {freq_cnt[kw]}")
        return matched_papers


class Paper(object):
    def __init__(self, title) -> None:
        self.title = title

        self.arxiv_ver = None
        self.arxiv_match_rate = None

    @property
    def has_arxiv(self):
        return self.arxiv_ver is not None

    def find_arxiv(self, verbose=True) -> str:
        if verbose:
            print(f"Search for {self.title}")
        search = arxiv.Search(
            query=self.title,
            max_results=3,
            sort_by=arxiv.SortCriterion.Relevance
        )
        for result in search.results():
            fuzz_rat = fuzz.ratio(
                *sorted((result.title.lower(), self.title.lower()), key=lambda s: len(s)))
            if fuzz_rat > 50:
                if verbose:
                    print(f" Matched:", result.title)
                if verbose:
                    print(f" fuzz ratio: {fuzz_rat}")
                # ArxivPaper(self.title, result, fuzz_rat)
                self.arxiv_ver = result
                self.arxiv_match_rate = fuzz_rat
                return result.title
        else:
            if verbose:
                print(f"Not found paper: {self.title}")
            return None

    def download(self, to_dir="~/Downloads"):
        if self.arxiv_ver is None:
            return
        to_dir = os.path.expanduser(to_dir)
        self.arxiv_ver.download_pdf(dirpath=to_dir)


def main(args):
    from tqdm import tqdm
    # from time import sleep

    search = NeurIPSPaperSearch()
    search.cache_all_titles()
    matched_papers = search.find(args.keyword, return_titles=False)

    print("Search arxiv")
    cnt_arxiv = 0
    for p in tqdm(matched_papers, desc='ArXiv'):
        if p.has_arxiv:
            r = True
        else:
            r = p.find_arxiv(verbose=False)
        if r is not None:
            cnt_arxiv += 1
        # sleep(0.1)
    print(f"Found {cnt_arxiv} out of {len(matched_papers)} papers in arxiv")

    if args.download:
        downalod_dir = f'~/Downloads/neurips2021/{args.keyword}'
        downalod_dir = os.path.expanduser(downalod_dir)
        if not os.path.exists(downalod_dir):
            print(f"create {downalod_dir}")
            os.makedirs(downalod_dir)
        for p in tqdm(matched_papers, desc='download'):
            if not p.has_arxiv:
                continue
            p.download(to_dir=downalod_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Automatically search and download papers from conference.")
    parser.add_argument('keyword', type=str,
                        help='download pdf files if available on ArXiv.')
    parser.add_argument('--download', action='store_true',
                        help='download pdf files if available on ArXiv.')
    args = parser.parse_args()

    main(args)