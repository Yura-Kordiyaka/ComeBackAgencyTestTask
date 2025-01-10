from dotenv import load_dotenv
import os


class Settings:
    def __init__(self):
        load_dotenv()
        self.BASE_URL: str = os.getenv('BASE_URL', 'https://default-url.com')
        self.CSS_SELECTOR: str = os.getenv('CSS_SELECTOR', 'default')
        self.PATH_OUTPUT_FILE: str = os.getenv('PATH_OUTPUT_FILE', 'output_data/output.csv')


settings = Settings()
