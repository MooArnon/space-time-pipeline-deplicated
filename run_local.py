from pipeline import BeautifulSoupEngine

if __name__ == "__main__":
    bs_engine = BeautifulSoupEngine()
    price = bs_engine.scrape()
    print(f"THE PRICE IS {price}")