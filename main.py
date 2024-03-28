import sys
import os
import scrapper

def invalid_topic_file():
    print('Invalid topic file. Read help menu for more')
    sys.exit(1)

def load_topics(topic_path:str):
    if len(topic_path) > 0 and os.path.isfile(topic_path) == False:
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
        scrapper.search_topics(topics)
    else:
        usage()
