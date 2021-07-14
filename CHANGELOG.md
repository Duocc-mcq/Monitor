# Changelog


## [2.2.1] - 2021-06-17
**BoxVersion == 2.2.0**
### Added
- Filter mutation point

### Changed

### Fixed
- Fix bug counting: Box gửi data 2 lần counting cho 1 obj_id - Kiểm tra, lọc data

## [2.2.0] - 2021-06-08
**BoxVersion == 2.2.0**
### Added

- nvanalytics functions
### Changed

- All data payload
### Fixed


## [v2.1.0](https://git.meditech.vn/hoang.nguyentien/people-counting-heatmap-service/-/tags/release%2Fv2.1) (2021-04-17)


**Implemented enhancements:**

- Cập nhật chức năng routemap
- Thay thuật toán norfair bằng sort
- Xóa +7 khi lấy timestamp từ box
- Cải thiện thuật toán dự đoán hướng của người
- Chuẩn hóa các điểm đột biến của bản đồ nhiệt

**Fixed bugs:**

- [Cần sửa để đẩy staging routemap](https://git.meditech.vn/hoang.nguyentien/people-counting-heatmap-service/issues/2)

**Closed issues:**

- [Cần sửa để đẩy staging routemap](https://git.meditech.vn/hoang.nguyentien/people-counting-heatmap-service/issues/2)


## [v2.0.0](https://git.meditech.vn/hoang.nguyentien/people-counting-heatmap-service/-/tags/release%2Fv2.0) (2021-04-13)


**Implemented enhancements:**

- Nâng cấp phiên bản gateway pc-hm lên 2.0.
- Nâng cấp deepstream core trên box lên 2.0
- Thêm log kiểm tra kết nối kafka
- Chia hàm đếm ra/vào và hàm đếm trong quầy

**Fixed bugs:**

**Closed issues:**

## [v1.0.0](https://git.meditech.vn/hoang.nguyentien/people-counting-heatmap-service/-/tags/release%2Fv1.0) (2021-04-08)

**Implemented enhancements:**

- Đổi tên biến môi trường CONSUMER_TOPIC -> RECEIVE_BOX_TOPIC
- Đổi tên biến môi trường GROUP_ID -> RECEIVE_GROUP_ID
- Đổi tên biến môi trường PC_TOPIC -> SEND_COUNT_TOPIC
- Đổi tên biến môi trường BUCKET -> HEATMAP_BUCKET
- Thay đổi cách đọc dữ liệu đầu vào gửi từ dưới box thành dạng json
- Cập nhật tracking theo batch
- Cải thiện thuật toán dự đoán hướng sử dụng kalman filter và dự đoán theo thời gian (timestamp)
- Cập nhật đếm trong zone theo timestamp
- Thêm log lỗi qua telegram
- Thêm chức năng tự cập nhật config thay đổi từ dashboard


**Fixed bugs:**

**Closed issues:**
