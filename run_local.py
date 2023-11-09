from space_time_pipeline.notifier import LineNotifier

noti = LineNotifier()

present_price = 10
next_price = 12

app_element = {
    "app":"test",
    "present_price": present_price,
    "next_price": next_price
}


noti.sent_message(app_element, "predict")
