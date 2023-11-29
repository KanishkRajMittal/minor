import FCMManager as fcm
tokens = ["eb-GTGGgRUOzuiFlPC1EXL:APA91bG6RnoxXJjnr0HrVEMJ4MZQVBI-O51JhClhjRqyYyH9L2ilXVrdprPUR0nkKaXoIpvAd3dQ-9eKQwD1CZX_2u-XYIgQkyJHuFdfQq2KpdmHwpW7flX2Qv_g2tBvA6wE28aph80O"]
# fcm.sendPush(title,description,tokens)
fcm.sendPush("Reminder", "Have you solved today's problem?", tokens)