import json
from flask import Flask, render_template
from backend.news.propertynews import scrape_property_news
from backend.news.khaleejtimes import scrape_khaleej_news
from backend.news.dailynewsegypt import scrape_dailyegypt_news
from backend.news.googlenews import scrape_google_news
from backend.properties.competitornews import scrape_competitor_news
from backend.properties.properties import scrape_properties

from flask import Flask, render_template, jsonify, request

# ... existing imports ...

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def home():
    return "App is running. Hit /scrape to trigger scraping."

@app.route("/scrape", methods=["GET"])
def index():
    if request.method != "GET":
        return "", 200

    uae_articles = scrape_khaleej_news() + scrape_property_news()
    egypt_articles = scrape_dailyegypt_news()

    countries = ["saudi", "iran", "iraq", "kuwait", "qatar"]
    rest_articles = []
    for country in countries:
        query = f"{country}"
        rest_articles += scrape_google_news(query)

    aldar_properties = scrape_properties("https://www.bayut.com/companies/aldar-properties-104861/")
    emaar_properties = scrape_properties("https://www.bayut.com/s/emaar-properties-sale-dubai/")
    nakheel_properties = scrape_properties("https://www.bayut.com/s/nakheel-properties-sale-dubai/")
    damac_properties = scrape_properties("https://www.bayut.com/s/damac-properties-sale-dubai/")

    aldar_news = scrape_competitor_news("aldar-properties")
    emaar_news = scrape_competitor_news("emaar-properties")
    damac_news = scrape_competitor_news("damac-properties")
    nakheel_news = scrape_competitor_news("nakheel")

    competitors = [
        {"name": "Aldar", "news": aldar_news, "properties": aldar_properties, "logos": ["aldar.jpg", "aldar2.jpg"]},
        {"name": "Emaar", "news": emaar_news, "properties": emaar_properties, "logos": ["emaar1.jpg", "emaar2.jpg"]},
        {"name": "DAMAC", "news": damac_news, "properties": damac_properties, "logos": ["damac1.jpg", "damac2.jpg"]},
        {"name": "Nakheel", "news": nakheel_news, "properties": nakheel_properties, "logos": ["nakheel1.png", "nakheel2.jpg"]}
    ]

    return render_template("index.html", 
                           country1_articles=uae_articles, 
                           country2_articles=egypt_articles, 
                           country3_articles=rest_articles, 
                           competitors=competitors)



