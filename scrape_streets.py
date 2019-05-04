import requests
from bs4 import BeautifulSoup

all_streets = []
for i in range(2, 371):
    print(f'{i} / 370')
    url = 'http://www.praha.cz/ulice-v-praze/strana-' + str(i)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    streets = soup.findAll('a')
    streets = filter(lambda s:
                     s.has_attr('href') and
                     len(s.attrs) == 1 and
                     s.attrs['href'].startswith('/ulice-v-praze') and
                     s.text.strip() != '' and
                     not s.text.strip().isnumeric() and
                     not 'strana' in s.attrs['href']
                     , streets)
    streets = list(map(lambda s: s.text.strip().lower(), streets))
    all_streets += streets

with open('data/streets.txt', 'w') as f:
    f.write('\n'.join(all_streets))
