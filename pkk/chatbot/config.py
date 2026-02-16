# DeepSeek API Configuration
# This module imports API configuration from Django settings
from django.conf import settings

DEEPSEEK_API_KEY = settings.DEEPSEEK_API_KEY
DEEPSEEK_API_URL = settings.DEEPSEEK_API_URL

# You can get your API key from: https://platform.deepseek.com/
# Instructions:
# 1. Sign up at https://platform.deepseek.com/
# 2. Go to API Keys section
# 3. Create a new API key
# 4. Add it to your .env file as DEEPSEEK_API_KEY=your-key-here
