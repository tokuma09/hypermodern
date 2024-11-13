import textwrap
import requests

API_URL = 'https://en.wikipedia.org/api/rest_v1/page/random/summary'

def main():
    with requests.get(API_URL) as response:
        data = response.json()
    print(data['title'], end='\n\n')
    print(textwrap.fill(data['extract'], 80))


if __name__ == '__main__':
    main()
