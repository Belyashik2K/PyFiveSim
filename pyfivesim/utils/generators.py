def generate_full_link(
        base_url: str,
        endpoint: str,
        **query_params: str | int | None
) -> str:
    url = f"{base_url}/{endpoint}"
    if query_params:
        url += "?"
        for param, value in query_params.items():
            if value is not None:
                url += f"{param}={value}&"
    return url.removesuffix("&")
