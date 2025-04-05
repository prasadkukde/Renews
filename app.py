import os
from flask import Flask, render_template, jsonify, request

# News scrapers
from backend.news.propertynews import scrape_property_news
from backend.news.khaleejtimes import scrape_khaleej_news
from backend.news.dailynewsegypt import scrape_dailyegypt_news
from backend.news.googlenews import scrape_google_news

# Property scrapers
from backend.properties.competitornews import scrape_competitor_news
from backend.properties.properties import scrape_properties

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
# def home():
#     return "App is running. Hit /scrape to trigger scraping."

# @app.route("/scrape", methods=["GET"])
def index():
    # UAE and Egypt news
    uae_articles = scrape_khaleej_news() + scrape_property_news()
    egypt_articles = scrape_dailyegypt_news()

    # Regional news from Google News
    countries = ["saudi", "iran", "iraq", "kuwait", "qatar"]
    rest_articles = []
    for country in countries:
        rest_articles += scrape_google_news(country)

    # Helper to scrape a competitor's data
    def get_competitor_data(name, url, logos):
        return {
            "name": name,
            "news": scrape_competitor_news(name.lower().replace(" ", "-")),
            "properties": scrape_properties(url),
            "logos": logos
        }

    # Competitor sections
    competitors = [
        get_competitor_data("Aldar", "https://www.bayut.com/companies/aldar-properties-104861/", ["aldar.jpg", "aldar2.jpg"]),
        get_competitor_data("Emaar", "https://www.bayut.com/s/emaar-properties-sale-dubai/", ["emaar1.jpg", "emaar2.jpg"]),
        get_competitor_data("DAMAC", "https://www.bayut.com/s/damac-properties-sale-dubai/", ["damac1.jpg", "damac2.jpg"]),
        get_competitor_data("Nakheel", "https://www.bayut.com/s/nakheel-properties-sale-dubai/", ["nakheel1.png", "nakheel2.jpg"]),
    ]

    return render_template(
        "index.html",
        country1_articles=uae_articles,
        country2_articles=egypt_articles,
        country3_articles=rest_articles,
        competitors=competitors
    )

# Required for Render or any cloud service to detect and bind the correct port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
