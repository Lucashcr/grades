import os

import dotenv


dotenv.load_dotenv()


DATABASE_URL = os.environ["DATABASE_URL"]
TEST_DATABASE_URL = os.environ["TEST_DATABASE_URL"]
