import MySQLdb

class RestaurantDb():
  def __init__(self):
    self.conn = MySQLdb.connect(host="localhost", user = "root", passwd = "1998", db = "restaurant_bot")

  # check for the available timeslots in the mentioned date
  def check_date(self, booking_date):
    cur = self.conn.cursor()
    booking_date = booking_date[0:10]
    # check whether the date already exists
    result = cur.execute("SELECT * FROM booking WHERE date = '{0}'".format(booking_date))
    if result == 0:
      cur.execute("INSERT INTO booking(date, slot1, slot2, slot3) VALUES('{0}', JSON_ARRAY(true, true, true), JSON_ARRAY(true, true, true), JSON_ARRAY(true, true, true))".format(booking_date))
      self.conn.commit()
    # check for any free slots in the mention date
    free_timeslot = cur.execute("SELECT * FROM booking WHERE date = '{0}' AND (JSON_EXTRACT(slot1, '$[2]') OR JSON_EXTRACT(slot2, '$[2]') OR JSON_EXTRACT(slot3, '$[2]'))".format(booking_date))
    if free_timeslot != 0:
      return True
    else:
      return False

  # get the free slots in the date
  def free_slots(self, booking_date):
    cur = self.conn.cursor()
    booking_date = booking_date[0:10]
    response_obj = [{"text": {"text": ["The time slot your looking for ?"]}},{"card": {"title": "The time slot your looking for ?","buttons": []},"platform": "TELEGRAM"}]
    # check whether the slot is free
    slot1 = cur.execute("SELECT * FROM booking WHERE date = '{0}' AND JSON_EXTRACT(slot1, '$[2]')".format(booking_date))
    slot2 = cur.execute("SELECT * FROM booking WHERE date = '{0}' AND JSON_EXTRACT(slot2, '$[2]')".format(booking_date))
    slot3 = cur.execute("SELECT * FROM booking WHERE date = '{0}' AND JSON_EXTRACT(slot3, '$[2]')".format(booking_date))
    if slot1 != 0:
      response_obj[1]['card']['buttons'].append({ "text" : "5PM-6PM" })
    if slot2 != 0:
      response_obj[1]['card']['buttons'].append({ "text" : "6PM-7PM" })
    if slot3 != 0:
      response_obj[1]['card']['buttons'].append({ "text" : "7PM-8PM" })
    return response_obj

  # get the free timings in the time_slots
  def free_time(self, booking_date, start_time):
    cur = self.conn.cursor()
    start_time = int(start_time[11:13])-12
    booking_date = booking_date[0:10]
    time_slot1 = str(start_time)+':00 PM'
    time_slot2 = str(start_time)+':30 PM'
    response_obj = [{"text": {"text": ["The time your looking for ?"]}},{"card": {"title": "The time your looking for ?","buttons": []},"platform": "TELEGRAM"}]
    slots = ['slot1', 'slot2', 'slot3']
    time_period = [5,6,7]
    slot = slots[time_period.index(start_time)]
    # check whether the timing is free
    time1 = cur.execute("SELECT * FROM booking WHERE date = '{0}' AND JSON_EXTRACT({1}, '$[0]')".format(booking_date, slot))
    time2 = cur.execute("SELECT * FROM booking WHERE date = '{0}' AND JSON_EXTRACT({1}, '$[1]')".format(booking_date, slot))
    if time1 != 0:
      response_obj[1]['card']['buttons'].append({ "text" : "{0}".format(time_slot1) })
    if time2 != 0:
      response_obj[1]['card']['buttons'].append({ "text" : "{0}".format(time_slot2) })
    return response_obj

  # book the time slot
  def book_table(self, booking_date, booking_time):
    cur = self.conn.cursor()
    booking_date = booking_date[0:10]
    slots = ['slot1', 'slot2', 'slot3']
    time_period = [5,6,7]
    slot = slots[time_period.index(int(booking_time[11:13])-12)]
    timings = [0,30]
    time_slot = timings.index(int(booking_time[14:16]))
    # update the time_slot a occupied
    cur.execute("UPDATE booking SET {0} = JSON_SET({0}, '$[{2}]', false) WHERE date = '{1}'".format(slot, booking_date, time_slot))
    cur.execute("UPDATE booking SET {0} = JSON_SET({0}, '$[2]', false) WHERE date = '{1}' AND (NOT JSON_EXTRACT({0}, '$[0]')) AND (NOT JSON_EXTRACT({0}, '$[1]'))".format(slot, booking_date))
    self.conn.commit()
