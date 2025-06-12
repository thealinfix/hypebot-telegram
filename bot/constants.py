# Image styles configuration
IMAGE_STYLES = {
    "sneakers": {
        "prompt_template": "Hyperrealistic photo of {title} sneakers, {brand} brand, studio lighting, white background, professional product photography, 8k, detailed textures --ar 1:1 --v 6",
        "style": "Hyperrealistic product photography"
    },
    "fashion": {
        "prompt_template": "High fashion editorial photo featuring {title}, {brand} collection, vogue style, dramatic lighting, luxury aesthetic, professional photography --ar 4:5 --v 6",
        "style": "High fashion editorial"
    },
    "thoughts": {
        "prompt_template": "Minimalist artistic composition representing '{topic}', abstract modern art, conceptual photography, moody lighting, thought-provoking imagery --ar 1:1 --v 6",
        "style": "Conceptual artistic"
    }
}

# Sources configuration
SOURCES = {
    "sneakernews": {
        "name": "SneakerNews",
        "url": "https://sneakernews.com",
        "style": "sneakers",
        "selectors": {
            "container": "div.post",
            "title": "h2.title",
            "link": "a",
            "image": "img"
        }
    },
    # ... другие источники
}
