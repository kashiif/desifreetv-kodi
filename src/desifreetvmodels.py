
def create_channel_entry(title, url, thumbnail):
    return {
        'title': title,
        'url': url,
        'pagetype': 'channel-list',
        'thumbnail': thumbnail
    }


def create_show_entry(title, url, thumbnail):
    return {
        'title': title,
        'url': url,
        'pagetype': 'channel-show',
        'thumbnail': thumbnail
    }


def create_episode_entry(title, url, thumbnail):
    return {
        'title': title,
        'url': url,
        'pagetype': 'show-episode',
        'thumbnail': thumbnail
    }
