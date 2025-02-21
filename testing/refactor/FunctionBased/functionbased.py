from urllib.parse import urlparse
from platforms.youtube import download_youtube_to_wav
from platforms.nrk import download_nrk_to_wav
#from download_to_wav import download_to_wav
from domains.youtubedomains import youtube_domains
from domains.nrkdomains import nrk_domains

"""
DOMAIN_HANDLERS is a dictionary that maps domain names to a 
set containing the platform name and the corresponding handler function.
To add support for a new platform, add a new entry to this dictionary.
Make a set for the excpected domains for the platform 
and make a function to download/convert it to wav.
"""

DOMAIN_HANDLERS = {
    **{domain: ("YouTube", download_youtube_to_wav) for domain in youtube_domains},
    **{domain: ("NRK", download_youtube_to_wav) for domain in nrk_domains},
}

def inputHandler(link: str):
    """
    Takes a link as argument 
    Determines the platform of the link by parsing the domain
    Calls download_to_wav with the link and the platform as arguments
    """
    #TODO: 
    # check if video is already dowloaded and processed in ElastiSearch

    # Parse the link
    parsed_url = urlparse(link)
    domain = parsed_url.netloc

    # Retrieve the corresponding platform and handler function
    platform, handler = DOMAIN_HANDLERS.get(domain, ("Other", None))

    #TODO: should make a check if the video is live or static,
    #      probably different handlers for live and static videos

    if handler:
        handler(link, platform)
    else:
        print(f"Unsupported platform for domain: {domain}")

    print(f"Domain: {domain}")
    print(f"Platform: {platform}")
    print(link)

#inputHandler("https://www.youtube.com/watch?v=VgsC_aBquUE")
inputHandler("https://www.youtube.com/watch?v=-dqpCSBPy0k&t=5s")