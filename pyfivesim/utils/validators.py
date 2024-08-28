from pyfivesim.models.guest.prices import (
    ProductWithOperators,
    OperatorWithPrice,
    Price,
)


def validate_api_key(method):
    async def wrapper(self, *args, **kwargs):
        if not self._api_key:
            raise ValueError("API key is required for this method")
        return await method(self, *args, **kwargs)

    return wrapper

def validate_operators_in_model(data: dict, field: str) -> dict:
    products = list()
    for service, operators in data.items():
        if not isinstance(operators, dict):
            continue
        product = ProductWithOperators(name=service, operators=[])
        for operator, info in operators.items():
            product.operators.append(OperatorWithPrice(name=operator, operator_info=Price(**info)))
        products.append(product)
    data[field] = products
    return data