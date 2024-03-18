from fastapi import APIRouter, Header, Cookie, Form
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
from typing import Optional, List
from custom_log import log
import time

router = APIRouter(
    prefix ='/product',
    tags=['product']
)

products = ['watch', 'camera', 'phone']

async def time_consuming_functionality():
    time.sleep(5)
    return 'ok'

@router.get('/all')
async def get_all_products():
    await time_consuming_functionality()
    #return products
    data = " ".join(products)
    response = Response(content=data, media_type="text/plain")
    response.set_cookie(key='test_cookie', value='test_cookie_value')
    log("MyAPI", "Call to get all products.")
    return response

@router.post('/new')
def create_product(name: str = Form(...)):
    products.append(name)
    return products

@router.get('/withheader')
def get_products(response: Response,
                 custom_header: List[Optional[str]] = Header(None),
                 test_cookie: Optional[str] = Cookie(None)
                 ):
    if custom_header:
        response.headers['custom_response_header'] = ", ".join(custom_header)
    return {
        'data': products,
        'custome_header': custom_header,
        'my_cookies': test_cookie
    }

@router.get('{id}', responses={
    200: {
        "content": {
            "text/html": {
                "example": "<div>Product</div>"
            }
        },
        "description": "Returns the HTML for an object"
    },
    404: {
        "content": {
            "text/plain": {
                "example": "Product not available"
            }
        },
        "description": "A clear text error message"
    }
})
def get_product(id: int):
    if id >= len(products):
        out = "Product not available"
        return PlainTextResponse(status_code=404, content=out, media_type="text/plain")
    else:
        product = products[id]
        out = f"""
        <head>
            <style>
            .product {{
                width: 500px;
                height: 30px;
                border: 2px inset green;
                backrground-color: lightblue;
                text-align: center;
            }}
            </style>
        </head>
        <div class="product">{product}</div>
        """
        return HTMLResponse(content = out, media_type="text/html")