# Spidering-Web-Tool
Use the command ```scrapy startproject webspider``` to create scrapy project

# Setup and Installation
Clone the repository:

``` Bash
git clone https://github.com/wanghui070404/Spidering-Web-Tool.git
```

Navigate to the Scrapy project directory:
This is the directory containing the scrapy.cfg file.

```
cd Spidering-Web-Tool/webspider
```
Install dependencies:
It is highly recommended to use a virtual environment.


# Install Scrapy framework
```
pip install Scrapy
```
# How to run Spidering-Web-Tool using Scrapy
1. Use the command to redirect to folder containing executed file: 
```
cd ...//Spidering-Web-Tool//webspider//webspider//spiders
```
2. Use the command to run spidering tool:
```
scrapy crawl myspider -a start_url="url you want to crawl" -o result.json
```
