# PC-HM Gateway Service

Gateway service nhận dữ liệu counting dưới box thực hiện tích lũy và tổng hợp.
- Dữ liệu counting/heatmap gửi sang backend.

## TODO

- [ ] Xử lý khi camera thay đổi chức năng, cam bị xóa (k có data) khỏi hệ thống

## Configuration

| Var                 | Description                       | Default             |
| ------------------- | --------------------------------- | ------------------- |
| BOOTSTRAP_SERVER    | Kafka server                      | 192.168.30.201:9092 |
| RECEIVE_BOX_TOPIC   | Topic dữ liệu gateway nhận từ box | nvdsanalytics       |
| RECEIVE_GROUP_ID    | Group id của gateway nhận từ box  | uuid()              |
| SEND_COUNT_TOPIC    | Topic push counting data          | test                |
| SEND_HEATMAP_TOPIC  | Topic push heatmap data           | test                |
| SEND_ROUTEMAP_TOPIC | Topic push routemap data          | test                |

## API description

- [Payload](https://git.meditech.vn/hoang.nguyentien/people-counting-heatmap-service/blob/dev/improve_core/PAYLOAD.md)

## Deployment

```bash
# ENV config in services/README.md
docker run -itd --net=host --name people-gateway \
  --shm-size=10.05gb \
  -v /tmp/logs:/people-counting-heatmap-service/logs \
  hub.iview.vn/people-gateway:2.2.2
```

## Development

```bash
docker build -t hub.cxview.ai/people-gateway:0.1-base -f Dockerfile.base .

docker run --gpus all -itd --net=host --name people-gateway-base \
  --shm-size=10.05gb \
  -v /mnt/sda2/ExternalHardrive/edge-ai/people-counting-heatmap-service:/people-counting-heatmap-service \
  hub.cxview.ai/people-gateway:0.1-base

docker build -t hub.iview.vn/people-gateway:x.y.z -f Dockerfile .
```

## Latest Changelogs - 2.2.2
BoxVersion = 2.2.1

### Added

### Changed

- Ignore centroid not in roi of heatmap
- Remove shape config
### Fixed


## Contributing

- [thaint](https://git.meditech.vn/thai.nt2901)
- [hoangnt](https://git.meditech.vn/hoang.nguyentien)

## Authors

- [hoangnt](https://git.meditech.vn/hoang.nguyentien)

