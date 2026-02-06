FROM python:3.9-slim

# প্রয়োজনীয় টুলস ইনস্টল
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    unzip \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# গুগল ক্রোম ইনস্টল করার জন্য নতুন ও নিরাপদ পদ্ধতি
RUN curl -fSsL https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor | tee /usr/share/keyrings/google-chrome.gpg > /dev/null \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# বট রান করা
CMD ["python", "main.py"]
