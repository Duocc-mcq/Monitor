FROM hub.cxview.ai/people-gateway:0.1-base

COPY ./ /people-counting-heatmap-service

WORKDIR /people-counting-heatmap-service

CMD ["python", "main.py"]
