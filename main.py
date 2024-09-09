from fastapi import FastAPI
import os
from jsonconvertor.jsonutils import convertListToJson
from fastapi.responses import FileResponse
from scrapper.scrapper import Scraper
from fastapi.responses import Response
from parserclass.productclass import ProductClass, Title, Image

app = FastAPI()

baseURL = "https://dentalstall.com/shop/"

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=200)

@app.get("/")
def baseRoot():
    return {"message": "Scraper is ready!"}

@app.get("/scrape")
async def scrapeDentalProducts(limit: int = 5):
    scrapper = Scraper(
        baseURL=baseURL,
        parser=ProductClass(
            parserType='html.parser',
            baseTagType='li',
            className='product',
            title=Title(
                tag='h2',
                className='woo-loop-product__title'
            ),
            image=Image(
                tag='div',
                className='mf-product-thumbnail'
            ),
            subTitle=Title(
                tag='span',
                className='price',
                subTag='bdi'
            )
        )
    )
    productList = await scrapper.startScrapping(limit)
    
    convertListToJson(productList, "product-list.json")
    return {"message": f"Scraping completed for {limit} pages."}
