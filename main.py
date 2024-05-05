import sys
import os
from scrapper import ScrapeTopResults


# curl \
# -A "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0" \
# "https://www.google.com/complete/search?client=chrome&q=pledge" \
# | grep "g Ww4FFb vt6azd tF2Cxc asEBEc" \
# > search-response
#
# search auto-suggestions
# extract the people also asked questions for each search result
# extract the related searches for each search result
# extract the top 5 results for each search
# result container selector: div.g.Ww4FFb.vt6azd.tF2Cxc.asEBEc
# result links selector: a[jsname="UWckNb"]
# extract the following for each top result:
#   - meta description
#   - meta keywords
#   - schema mark up
#   - canonical tag
#   - header tag
#   - image alt description
#   - xml sitemap
#   - robots.txt
#   - html structure
#   - keyword density

def invalid_topic_file():
    print('Invalid topic file. Read help menu for more')
    sys.exit(1)


def load_topics(topic_path: str):
    if len(topic_path) > 0 and os.path.isfile(topic_path) is False:
        invalid_topic_file()
    topics = []
    with open(topic_path, 'r+') as topic_file:
        lines = [line.strip().split(',') for line in topic_file.readlines()]
        topics = [topic.strip() for row in lines for topic in row if len(topic) > 1]
    if len(topics) < 1:
        invalid_topic_file()
    return topics


def usage():
    print('''This is the help menu for Topic Authority Generator!

    -h          Shows this menu

    -t [path]   A text file (.txt) containing comma separated list of
                topics to generate topic authority''')


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1 and args[1] == '-k' and 2 < len(args):
        topics = load_topics(topic_path=args[2])
        print('[*] Topic/s loaded')
        print(f'topics: {topics}')
        ScrapeTopResults().search_topics(topics)
    else:
        usage()
