"""BigOCast | Moein. Run the exact six-request Signal lesson example."""
from api_cache import ProductAPI, ProductStore


def main():
    app=ProductAPI(ProductStore(),3)
    try:
        for key in (42,42,17,83,42,91):
            hit=key in app.cache.nodes
            product=app.get_product(key)
            print(f'{key:2}  {"HIT " if hit else "MISS"}   {product.name:<8}  reads={len(app.store.selects)}')
        print('LRU to MRU:',[key for key,_ in app.cache.items()])
    finally:
        app.store.close()


if __name__=='__main__':
    main()
