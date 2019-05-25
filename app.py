from flask import Flask, jsonify, make_response, request
from database import RestaurantDb
from process import send_email

#  initialize the flask app
app = Flask(__name__)

# default route
@app.route('/', methods=['GET', 'POST'])
def index():
	# return response
	return make_response(jsonify(results()))

# function for responses
def results():
	req = request.get_json(force=True)
	action = req['queryResult']['action']

	# get_response of the user to book a table
	if action == 'get_response':
		user_response = req['queryResult']['queryText']
		negative_response = ['NO', 'no', 'No', 'NAH', 'nah', 'Nah']
		if user_response in negative_response:
			# Reply for negative response
			return {"fulfillmentMessages": [{"text": { "text": [ "Thank you for your response !" ] }, "platform": "TELEGRAM" }, { "text": { "text": [ "Thank you for your response !" ] } } ] }
		# Reply for positive response
		return {"fulfillmentMessages": [{"text": {"text": ["The date your looking for ?"]}},{"text": {"text": ["The date your looking for ?"]},"platform": "TELEGRAM"}]}
	
	# get_date for booking a table
	elif action == 'get_date':
		booking_date = req['queryResult']['outputContexts'][1]['parameters']['date']
		db = RestaurantDb()
		# check whether the date is free or not
		if db.check_date(booking_date):
			response_obj = db.free_slots(booking_date)
			# returns the available timeslots in the date
			return {"fulfillmentMessages": response_obj }
		else:
			return {"fulfillmentMessages": [{"text": {"text": ["Every slots are filled in the mentioned date, can you try someother day ?"]}},{"text": {"text": ["Every slots are filled in the mentioned date, can you try someother day ?"]},"platform": "TELEGRAM"}]}
	
	# get_timeslots of the mentioned date
	elif action == 'get_timeslots':
		booking_date = req['queryResult']['outputContexts'][1]['parameters']['date']
		start_time = req['queryResult']['parameters']['time-period']['startTime']
		db = RestaurantDb()
		response_obj = db.free_time(booking_date, start_time)
		#returns the available timings in the timeslots
		return {"fulfillmentMessages": response_obj }
	
	# get_time for booking a table
	elif action == 'get_time':
		booking_date = req['queryResult']['outputContexts'][2]['parameters']['date']
		booking_time = req['queryResult']['outputContexts'][1]['parameters']['time']
		user_response = req['queryResult']['queryText']
		db = RestaurantDb()
		db.book_table(booking_date, booking_time)
		# bookings a spot in the timings and ask for email for confirmation
		return {"fulfillmentMessages": [{"text": {"text": ["Can I have your Email Id for confirming your reservation!"]}},{"text": {"text": ["Can I have your Email Id for confirming your reservation!"]},"platform": "TELEGRAM"}]}
	
	# get_email for the confirmation
	elif action == 'get_email':
		booking_date = req['queryResult']['outputContexts'][0]['parameters']['date']
		booking_time = req['queryResult']['outputContexts'][0]['parameters']['time']
		booking_email = req['queryResult']['outputContexts'][0]['parameters']['email']
		# sending booking confirmation to the mail
		send_email(booking_date, booking_time, booking_email)
		return {"fulfillmentMessages": [{"text": {"text": ["Your reservation is completed successfully and a confirmation is send to your email address"]}},{"text": {"text": ["Your reservation is completed successfully and a confirmation is send to your email address"]},"platform": "TELEGRAM"}]}

# run the app
if __name__ == '__main__':
  app.run()
