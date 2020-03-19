import urllib.parse as url_parse


def form_link(url, add_params):
    splits = list(url_parse.urlparse(url))
    query = dict(url_parse.parse_qsl(splits[4]))
    query.update(add_params)

    splits[4] = url_parse.urlencode(query)
    return url_parse.urlunparse(splits)
