FROM python:3.8
  
COPY . .
ENV DEBIAN_FRONTEND noninteractive
RUN python3 -m pip install --upgrade pip==21.1.2
RUN pip3 install -r requirements.txt
RUN apt-get update -y
RUN apt install libgl1-mesa-glx -y
RUN echo "Asia/Ho_Chi_Minh" > /etc/timezone \
    && rm -f /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata
ENTRYPOINT ["python3","main.py"]
