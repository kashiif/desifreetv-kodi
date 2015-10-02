import re
import traceback
import urllib

import kodiaddonutils
import desifreetvmodels


def _fetch_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; U; en; CPU iPhone OS 4_2_1 like Mac OS X; en) AppleWebKit/533.17.9 '
                      '(KHTML, like Gecko) Version/5.0.2 Mobile/8C148a Safari/6533.18.5'
    }
    return kodiaddonutils.fetch_url(url, headers)


def fetch_channels_list():
    #TODO: load channel list by parsing page
    create_entry = desifreetvmodels.create_channel_entry
    category_url = 'http://www.desifreetv.co/category/%s/'

    channel_list = [
        {
        'title': 'Recent Episodes',
        'url': 'http://www.desifreetv.co/',
        'pagetype': 'recent-episodes',
        'thumbnail': 'http://i.imgur.com/qSzxay9.png'
        },

        create_entry('Hum TV',          category_url % 'hum-tv-dramas', 'http://i.imgur.com/SPbcdsI.png'),
        create_entry('Hum Sitaray',     category_url % 'humsitaray-dramas', 'http://i.imgur.com/GtoMqkd.png'),
        create_entry('ARY',             category_url % 'ary-dramas', 'http://i.imgur.com/Qpvx9N4.png'),
        create_entry('ARY Zindagi',     category_url % 'ary-zindagi', 'http://i.imgur.com/a1PH1wk.png'),
        create_entry('Geo TV',          category_url % 'geo-tv-dramas', 'http://i.imgur.com/YELzFHv.png'),
        create_entry('APlus',           category_url % 'a-plus', 'http://i.imgur.com/wynK0iI.png'),
        create_entry('Urdu1',           category_url % 'urdu-1', 'http://i.imgur.com/9i396WG.jpg'),
        create_entry('Ptv',             category_url % 'ptv', 'http://i.imgur.com/vJPo6xO.png'),
    ]

    return channel_list


def _fetch_list(reToMatch, indices, create_entry, params, paging_params = {}):
    url = (unicode)(urllib.unquote(params.get('url'))).decode('utf8')
    print 'url is: %s' % url

    html = _fetch_url(url)

    matches = re.findall(reToMatch, html, re.M)

    all_items = list()

    index_title = indices['title']
    index_url = indices['url']
    index_thumbnail = indices['thumbnail']

    import HTMLParser
    html_parser = HTMLParser.HTMLParser()

    thumbnail_lambda = None
    if index_thumbnail < 0:
        thumbnail_lambda = lambda m: ''
    else:
        thumbnail_lambda = lambda m: m[index_thumbnail]

    for match in matches:

        title = html_parser.unescape(match[index_title].decode('utf-8'))
        url = match[index_url]
        thumbnail = thumbnail_lambda(match)

        entry = create_entry(title, url, thumbnail)
        all_items.append(entry)

    if paging_params:
        next_page_link = _fetch_next_page_link(html)
        print 'next_page_link: %s' % next_page_link

        title = kodiaddonutils.lang(paging_params.get('title_id'))
        # a function pointer to create entry for next page item
        create_entry = paging_params.get('create_entry')

        if next_page_link:
            all_items.append(create_entry(title, next_page_link, ''))

    return {
            'html': html,
            'items': all_items
        }


def _fetch_next_page_link(html):
    reToMatch = '<li><a href="(.*)">Next Page<\/a><\/li>'

    the_iter = re.finditer(reToMatch, html, re.M)
    url = None

    for match in the_iter:
        url = match.group(1)
        break

    return url


def fetch_channel_shows(params):

    # TODO: support paging
    # show-name:3, thumbnail: 2, url: 1
    reToMatch = '(<ul class="category_images_ii term-images taxonomy-category">\s*' \
                    '<li class="category_image term_image">' \
                        '<a href="(.*)"><img src="(.*)" alt="(.*)"\s*/></a>\s*<p></p>\s*' \
                    '</li>\s*' \
                '</ul>)'

    indices = {'title': 3, 'url': 1, 'thumbnail': 2}

    paging_params = {
            'title_id': 32019,
            'create_entry': desifreetvmodels.create_channel_entry
        }

    result = _fetch_list(reToMatch, indices, desifreetvmodels.create_show_entry, params, paging_params)
    shows = result.get('items')

    return shows


def fetch_episodes(params):

    # show-name:3, thumbnail: 2, url: 1
    reToMatch = '(<div class="excrept_in">\s*<div class="thumbnail">.*\s*<img (style=".*[^"]"\s)*src="(.*)"\/><\/a><\/div>\s*' \
                '<div class="the_excrept">\s*<h2><a href="(.*)" rel="bookmark">(.*)<\/a><\/h2>)'

    indices = {'title': 4, 'url': 3, 'thumbnail': 2}

    paging_params = {
            'title_id': 32018,
            'create_entry': desifreetvmodels.create_show_entry
        }

    result =_fetch_list(reToMatch, indices, desifreetvmodels.create_episode_entry, params, paging_params)
    episodes = result.get('items')

    return episodes


def _get_daily_motion_urls(html, short):
    try:
        match =re.findall('src="(.*?(dailymotion).*?)"',html)
        playURL=match[0][0]
        print playURL
        if short:
            return [playURL]

        return [ get_resolved_url(playURL) ]
    except:
        print 'Error fetching DailyMotion stream url'
        print traceback.format_exc()
        return None


def get_resolved_url(play_url):
    import urlresolver

    stream_url = urlresolver.HostedMediaFile(play_url).resolve()
    return stream_url


def fetch_episode_sources(params):
    available_sources = {}

    url = urllib.unquote(params.get('url')).decode('utf8')
    print 'url is: %s' % url

    html = _fetch_url(url)

    urls = _get_daily_motion_urls(html, False)
    print 'video urls: %s' % urls
    if urls:
        available_sources['dailymotion'] = {'urls': urls}

    return available_sources

