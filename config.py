from dotenv import load_dotenv
import os
load_dotenv()

sec_key=os.getenv("secret_key")
ALGORITHM=os.getenv("Algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("access_token_expire_minutes"))