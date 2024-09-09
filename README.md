# Web Scraping Project

This project is designed for web scraping a website and extracting data from it. 

## Running the Project Locally

To run this project locally, follow these steps:

1. **Clone the Repository**

   First, clone the repository to your local machine:
   ```sh
   git clone https://github.com/pranavryali/web-scrapping.git
2. **Install all the dependencies**

    First install latest version of python
    Install flask
    ```sh
    pip install flask
    ```
    Install uvicorn
   ```sh
   pip install uvicorn
   ```
   Install httpx
    ```sh
    pip install httpx
    ```
   Install BeautifulSoup
   ```sh
   pip install bs4
   ```
3. **Overview of the project**

   We initially take a url of the website which we want to scrape and then start the flask API and the routes which we want to perform.
   Here for simplicity we have done all the things locally.
   Once we scrapped the data we save it into the json file and update the user about the scrapping status.
   We have added the cache here, this is used because we dont want to update the json file if the price(one of the value which we are storing in the json) is not updated.
4. **Process of Scrapping**

   Once we hit the API (locally)
   ```sh
   /scrape
   ```
   We start the process of scrapping, we have added the checks on auth key to be on safer side. We can add proxy as well to the API.
   Once the process is started we take the html content and get the data which is needed for our purpose. For this part i have taken the title, product-image and the price of a product on the website.
   Once we get the data for that particular page, we confirm the user that scrapping for that page is done and the number of items we scrapped.
   Then if the user has mentioned the number of pages that needs to be scrapped then we perform the same operation on all the pages and get the data.
   At the end we inform the user that scrapping has been done for all the pages and the products are updated in the local json file
5. **Run the project**

   To run this project, after you install all the dependencies needed according to the step2 mentioned above, run the below cmd

   ```sh
   python -m uvicorn main:app --reload
   ```

   
    
