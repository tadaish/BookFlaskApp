const d = new Date()

const weekday = ["Chủ Nhật","Thứ Hai","Thứ Ba","Thứ Tư","Thứ Năm","Thứ 6","Thứ Bảy"];

d.setDate(d.getDate() + 1)

var deliveryDate = document.getElementById('delivery_day')
deliveryDate.innerText = weekday[d.getDay()] + " " + d.toLocaleDateString()
