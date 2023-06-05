import re
import json
import bs4 as bs
import requests

base_url = 'https://paroles2chansons.lemonde.fr'
singer_page_base = '/paroles-'

# Get the url of the page of a singer


def get_singer_page_url(singer: str, index: int) -> str:
    return base_url + singer_page_base + singer + '-p{}'.format(index)

# Get the singer page


def get_singer_page(singer: str, index: int) -> str:
    return requests.get(get_singer_page_url(singer, index)).content.decode('utf-8')

# Get the song page


def get_song_page(url: str) -> str:
    return requests.get(base_url + url).content.decode('utf-8')

# Get singer's song links


def get_song_links(singer: str, max_pages=5) -> list:
    song_links = []
    # for index in [1]:
    for index in range(1, max_pages + 1):
        print("url: ", get_singer_page_url(singer, index))
        soup = bs.BeautifulSoup(get_singer_page(singer, index), 'html.parser')
        # print("soup: ", soup)
        # find all div tags with class 'small'
        song_uls = soup.select('div.small')
        # print("song_uls: ", song_uls)
        song_links += [(a.get('href'), a.get_text())
                       for a in song_uls[0].find_all('a')]
    return song_links


# clean lyrics
pattern = re.compile(r'\s+')  # match one or more whitespace characters


def clean_lyrics(lyrics: list) -> list:
    clean_lyrics = []
    for lyric in lyrics:
        if lyric != '':
            lyric = "".join(re.split("\s+", lyric, flags=re.UNICODE))
        if lyric != '' and lyric != ' ':
            clean_lyrics.append(lyric)
    return clean_lyrics

    # return [" ".join(re.split("\s+", lyric, flags=re.UNICODE)) for lyric in lyrics if lyric != '' and lyric != ' ']

# Get lyrics of a song


def get_lyrics(url: str) -> list:
    print('title: ', url)
    soup = bs.BeautifulSoup(get_song_page(url), 'html.parser')
    # print('soup: ', soup)
    lyrics = soup.find_all(
        'div', class_='border block-spacing-medium text-center')
    print('lyrics: ', len(lyrics))
    return clean_lyrics(lyrics[0].get_text().split('\n'))


# temp json data
data = {}

# reset data


def reset_temp_data():
    data.clear()


def save_lyrics(singer: str, title: str, lyrics: list):
    if singer not in data:
        data[singer] = {title: lyrics}
    else:
        data[singer][title] = lyrics


# open json file

# write lyrics to json file


def write_lyrics_to_json(data: dict, singer: str):
    json.dump(data, open('{}_lyrics.json'.format(
        singer), 'w'), ensure_ascii=False)

# Get lyrics of all songs of a singer


def get_all_lyrics(singer: str, max_pages=5):
    songs = get_song_links(singer, max_pages)  # [:2]
    for (url, title) in songs:
        save_lyrics(singer, title, get_lyrics(url)[:-1])
    write_lyrics_to_json(data, singer)


# set singer name and max pages to scrape
singer_data = [('alpha-wann', 3), ('vald', 5), ('nekfeu', 4)]


def run():
    # for each singer
    for (singer, max_pages) in singer_data:
        # get all lyrics
        get_all_lyrics(singer, max_pages)

        # display the length of the json file
        print('len: ', len(str(data)))

        # reset temp data
        reset_temp_data()

    print('done !')


# run()


def de_unicode_json():
    document = {}
    for (singer, _) in singer_data:
        with open("{}_lyrics.json".format(singer), "r", encoding="utf-8") as input:
            document.update(json.load(input))

    for singer in document:
        songs = document[singer]
        for title in songs:
            lyrics = songs[title]
            # remove space at the end of the line
            lyrics = [lyric if lyric[-1] != ' ' else lyric[:-1]
                      for lyric in lyrics if "[" not in lyric and "]" not in lyric]
            songs[title] = lyrics
        document[singer] = songs

    with open("cleaned_lyrics.json", "w", encoding="utf-8") as output:
        json.dump(document, output, ensure_ascii=False)

    print('len: ', len(str(document)))
    print('done !')


# de_unicode_json()


# convert to usable data format
def convert_to_usable_data_format():
    document = {}
    data = ''

    for (singer, _) in singer_data:
        with open("cleaned_lyrics.json".format(singer), "r", encoding="utf-8") as input:
            document.update(json.load(input))

    for singer in document:
        songs = document[singer]
        for title in songs:
            lyrics = songs[title]
            # write lines to data
            data += '{} \n{} \n'.format(title, '\n'.join((lyrics)) + ".")

    with open("usable_data.txt", "w", encoding="utf-8") as output:
        output.write(data)

    print('len: ', len(str(data)))
    print('done !')


convert_to_usable_data_format()


# convert to usable data format
def convert_to_usable_data_format_per_singer():
    document = {}
    data = ''

    with open("cleaned_lyrics.json", "r", encoding="utf-8") as input:
        document.update(json.load(input))

    for singer in document:
        songs = document[singer]
        for title in songs:
            lyrics = songs[title]
            # write lines to data
            data += '{} \n{} \n'.format(title, '\n'.join((lyrics)) + ".")

        with open("usable_data_{}.txt".format(singer), "w", encoding="utf-8") as output:
            output.write(data)

        print('singer: {}, len: {}'.format(singer, len(str(data))))
        print('done !')

        # reset data
        data = ''


# convert_to_usable_data_format_per_singer()
