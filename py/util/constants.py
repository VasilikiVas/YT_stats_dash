from enum import Enum

# CONSTANTS -------------------------------------------------------------------

class Topic(Enum):
    gaming = "gaming"
    education = "education"
    science = "science-technology"
    animals = "pets-animals"
    # sports = "sports"
    autos = "autos-vehicles"
    # music = "music"
    # news = "news-politics"
    blogs = "people-blogs"
    comedy = "comedy"
    entertainment = "entertainment"
    howto = "howto-style"

CHANNEL_LIST_URL    = "https://dz.youtubers.me/{geography}/{topic}/top-1000-youtube-channels/en"
CHANNEL_STATS_URL   = "https://dz.youtubers.me/{name}/youtuber-stats/en"
CHANNEL_URL         = "https://dz.youtubers.me/{name}/youtube?lang=en"
THUMBNAIL_URL       = "http://img.youtube.com/vi/{id}/maxresdefault.jpg" # 1280x720
ALT_THUMBNAIL_URL   = "https://i.ytimg.com/vi/{id}/{res}default.jpg"

THUMBNAIL_PATH = "../../thumbnails"
THUMBNAIL_WIDTH = 480
THUMBNAIL_HEIGHT = 360

class ThumbnailURL(Enum):
    default = ALT_THUMBNAIL_URL.format(id="{id}", res="")   # 120x90
    medium  = ALT_THUMBNAIL_URL.format(id="{id}", res="mq") # 320x180
    high    = ALT_THUMBNAIL_URL.format(id="{id}", res="hq") # 480x360
    max     = THUMBNAIL_URL                                 # 1280x720

def channel_list_URL(topic: Topic=Topic.gaming, geography: str="global"):
    """Return URL for scraping list of channels"""
    return CHANNEL_LIST_URL.format(geography=geography, topic=topic.value)

def thumbnail_URL(id, quality: ThumbnailURL=ThumbnailURL.default):
    """Return URL for thumbnail"""
    return quality.value.format(id=id)

if __name__ == "__main__":
    print(channel_list_URL())
    print(thumbnail_URL(id="mb_MpGnS8XQ"))
