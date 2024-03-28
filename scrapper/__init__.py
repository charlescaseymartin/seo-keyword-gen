from selenium.webdriver import Firefox

# search auto-suggestions
# extract the people also asked questions for each search result
# extract the related searches for each search result
# extract the top 5 results for each search
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

def search_topics(browser: Firefox, topics: list[str]):
    print('[*] Starting search')
    print(f'topics {topics}')
