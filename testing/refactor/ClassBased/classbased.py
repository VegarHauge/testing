from urllib.parse import urlparse
from ..FunctionBased.platforms.youtube import download_youtube_to_wav
from ..FunctionBased.platforms.nrk import download_nrk_to_wav
from domainsets import YOUTUBE_DOMAINS, NRK_DOMAINS

class PlatformHandler:
    """Manages platform-specific video downloading logic."""

    def __init__(self):
        self.domain_handlers = {}
        self._register_platforms()  # Register platforms on initialization

    def _register_platforms(self):
        """Registers all supported platforms and their handlers."""
        platform_data = {
            "YouTube": {
                "domains": YOUTUBE_DOMAINS,
                "handler": download_youtube_to_wav, #static handler
            },
            "NRK": {
                "domains": NRK_DOMAINS,
                "statichandler": download_nrk_to_wav, #static handler
                #"livehandler": live_nrk_to_wav, #live handler
            },
        }

        for platform, data in platform_data.items():
            self.register_platform(data["domains"], platform, data["handler"])

    def register_platform(self, domains, platform_name, handler):
        """Registers a platform with its associated domains and handler."""
        for domain in domains:
            self.domain_handlers[domain] = (platform_name, handler)

    def handle_input(self, link: str):
        """Processes a video link, determining the platform and invoking the handler."""
        # TODO: Implement a check if the video is already downloaded in Elasticsearch

        # Parse the link
        parsed_url = urlparse(link)
        domain = parsed_url.netloc

        # Retrieve the corresponding platform and handler function
        platform, handler = self.domain_handlers.get(domain, ("Other", None))

        # TODO: Implement logic to check if video is live or static
        if handler:
            handler(link, platform)
        else:
            print(f"Unsupported platform for domain: {domain}")

        print(f"Domain: {domain}")
        print(f"Platform: {platform}")
        print(link)

# Initialize the handler
platform_handler = PlatformHandler()

# Example Usage
platform_handler.handle_input("https://www.youtube.com/watch?v=VgsC_aBquUE")
platform_handler.handle_input("https://tv.nrk.no/serie/nytt-paa-nytt/sesong/2025/episode/MUHH50000525")
