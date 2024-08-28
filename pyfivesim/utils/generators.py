def generate_full_link(
        base_url: str,
        endpoint: str,
        **kwargs
) -> str:
    url = f"{base_url}/{endpoint}"
    if kwargs:
        url += "?"
        for key, value in kwargs.items():
            if value is not None:
                url += f"{key}={value}&"
    return url.removesuffix("&")
