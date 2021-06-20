FROM python:3.8

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        cmake \
        build-essential \
        gcc \
        g++ \
        bzip2 \
        unzip
        
        
# Install chromeDriver
RUN wget -q "https://chromedriver.storage.googleapis.com/91.0.4472.101/chromedriver_linux64.zip" \
-O /tmp/chromedriver.zip \
&& unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
&& rm /tmp/chromedriver.zip

RUN wget -q "https://drive.google.com/file/d/1v0btrXDubpSKz8DWf8DwHfKiRR9w-tFh/view?usp=sharing"

# install chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
	
CMD gunicorn --bind 0.0.0.0:$PORT wsgi
