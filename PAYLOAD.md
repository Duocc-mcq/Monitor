## Box Payload
### Dữ liệu đếm vào cửa / vào quầy / ngoài đường / routemap / heatmap từ box
```json
{
    "box_id": "2e5e8861-75ed-4c5a-b6ec-ddb89b04e8c7",
    "cam_id": "17052f6b-00a0-4562-9574-5d291b5fd6de",
    "scale": [73, 41],
    "shape": [1280, 720],
    "data": [
      {
        "obj_id": 1,
        "roi_id": "529bc44f-caa1-48cc-89bd-5d7579210069",
        "route_id": "72b40cbb-d7a9-41ec-95d9-bb037be2ced9",
        "line_id": "babc6c99-aab6-4c19-97c0-a714d70cedb6",
        "x": 100,
        "y": 130
      },
      {
        "obj_id": 2,
        "roi_id": "529bc44f-caa1-48cc-89bd-5d7579210069",
        "route_id": "72b40cbb-d7a9-41ec-95d9-bb037be2ced9",
        "line_id": "babc6c99-aab6-4c19-97c0-a714d70cedb6",
        "x": 224,
        "y": 374
      }
    ]
    "timestamp": "2021-05-17T17:55:53.917Z"
}
```

### Ghi chú
- Box:
    - detect
    - tracking
    - counting

- Gateway:
    - Counting:
        - Gửi dữ liệu realtime
        - Gửi qua kafka
    - Heatmap:
        - Tích lũy
        - Gửi qua kafka


## Gateway Payload
### Dữ liệu ra/vào cửa (entry)
```json
{
    "type": "entry",
    "box_id": "2e5e8861-75ed-4c5a-b6ec-ddb89b04e8c7",
    "cam_id": "17052f6b-00a0-4562-9574-5d291b5fd6de",
    "zone_id": "8965361b-9e11-43e3-bfaa-b0b8b723a801",
    "timestamp": 1620638629
}
```

### Dữ liệu routemap (route)
```json
{
    "type": "route",
    "box_id": "2e5e8861-75ed-4c5a-b6ec-ddb89b04e8c7",
    "cam_id": "17052f6b-00a0-4562-9574-5d291b5fd6de",
    "route_id": "8965361b-9e11-43e3-bfaa-b0b8b723a801",
    "timestamp": 1620638629
}
```

### Dữ liệu vào quầy / ngoài đường (stall)
```json
{
    "type": "stall",
    "box_id": "2e5e8861-75ed-4c5a-b6ec-ddb89b04e8c7",
    "cam_id": "17052f6b-00a0-4562-9574-5d291b5fd6de",
    "zone_id": "529bc44f-caa1-48cc-89bd-5d7579210069",
    "dwell_time": 10,
    "timestamp": 1620638629
}
```


### Dữ liệu heatmap
```json
{
    "type": "heatmap",
    "box_id": "2e5e8861-75ed-4c5a-b6ec-ddb89b04e8c7",
    "cam_id": "17052f6b-00a0-4562-9574-5d291b5fd6de",
    "data": 
    [
      {"index": [11, 10], "dwell_time": 20},
      {"index": [73, 41], "dwell_time": 3},
      {"index": [4, 2], "dwell_time": 38},
      {"index": [9, 13], "dwell_time": 1},
      {"index": [14, 17], "dwell_time": 24},
      {"index": [16, 25], "dwell_time": 10}
    ],
    "timestamp": 1620638629
}
```