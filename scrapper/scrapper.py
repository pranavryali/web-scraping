import requests
from bs4 import BeautifulSoup
from fastapi import Header, HTTPException, Depends
import time
import httpx
from utils.cacheutils import updateCache
from utils.utils import countDown
from parserclass.baseparser import BaseParser
from parserclass.productclass import ProductClass
from parserclass.title import Title
from parserclass.image import Image

API_TOKEN = "testing-token"

def verifyAuthToken(apiToken):
    print("This is called")
    if apiToken != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized") 
    
class Scraper:
    def __init__(self, baseURL: str, parser: BaseParser = None, proxy: str = None):
        self.baseURL = baseURL
        self.proxy = proxy
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        self.parser = parser
        self.convertedState = 0
        self.unConvertedState = 0
        self.cachedFile = "product-list.json"
    
    async def fetchURLStatus(self, url) :
        retries = 3
        while retries > 0:
            try:
                async with httpx.AsyncClient(proxies=self.proxy) as client:
                    response = await client.get(url)
                    response.raise_for_status()
                    return response.text
            except httpx.RequestError:
                retries -= 1
                time.sleep(5)
        raise Exception(f"Failed to fetch page: {url}")

    async def scrapeWebsite(self, url,  pageNumber: int = 0):
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Internal Error scraping page {pageNumber}: {response.status_code}")
                if countDown(5):
                    return self.scrapeWebsite(pageNumber=pageNumber)
            else:
                products = []
                parserType = self.parser.parserType
                baseTagType = self.parser.baseTagType
                itemClassName = ""
                titleClass = Title()
                imageClass = Image()
                subTitleClass = Title()
                html = await self.fetchURLStatus(url)
                if type(self.parser) == ProductClass:
                    itemClassName = self.parser.className
                    titleClass = self.parser.title
                    imageClass = self.parser.image
                    subTitleClass = self.parser.subTitle
                soup = BeautifulSoup(response.content, parserType)
                items = soup.find_all(baseTagType, class_=itemClassName)

                for item in items:
                    itemName = item.find(
                        titleClass.tag, class_=titleClass.className
                    ).text.strip()
                    imageURL = None
                    imageTag = item.find(imageClass.tag, class_=imageClass.className).find('img')
                    if imageTag:
                        imageURL = imageTag['src']
                    price = item.find(subTitleClass.tag, class_= subTitleClass.className).find(subTitleClass.subTag).text.strip()
                    if imageURL != None:
                        self.convertedState += 1
                        products.append(
                            {
                                "title": itemName,
                                "product_image":imageURL,
                                "price": float(price[1:]),
                                "id": hash(itemName)
                            }
                        )
                    else:
                        print(itemName, imageURL, price)
                        self.unConvertedState += 1
                updateCache(self.cachedFile, products=products)
                return products
        except Exception as e:
            raise Exception(f"Error encountered {e}")

    def downloadImageIntoLocal(self, imageURL, path: str) -> str:
        response = requests.get(imageURL, stream=True)
        image_path = f"{path}/{imageURL.split('/')[-1]}"
        with open(image_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return image_path
    
    async def startScrapping(self,  maxPages = None,  token: str = Depends(verifyAuthToken)):
        products = []
        currentPageCount = 1
        
        while maxPages == None or currentPageCount <= maxPages:
            url = f"{self.baseURL}?page={currentPageCount}"
            try:
                pageProducts = await self.scrapeWebsite(url, currentPageCount)
                products.extend(pageProducts)
                print(f"Page {currentPageCount} scrapping done, number of products scrapped = {len(pageProducts)}")
                currentPageCount += 1
            except Exception as e:
                raise Exception(f"Error encountered {e}")
        return products
    
    