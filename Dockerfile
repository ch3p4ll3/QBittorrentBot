FROM python:3.7-slim
RUN mkdir /code
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN ln -sf /usr/share/zoneinfo/Europe/Rome /etc/localtime
RUN echo "Europe/Rome" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata
ENV TZ=Europe/Rome
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "/code/main.py" ]
