SABRE QUESTIONS:
* We see the consortium rates are showing in SRW but not on the search results in our app. We need to figure out how to get those rates to show up in our search results and auto apply to our bookings if possible.
* Question about how to keep counts updated during filtering for hotel
	* We want to be able to get the counts to show in our own UI
* Sort for Air.
	* O and D (Origin and Destination) pairs are grouped by airport code. When selecting a flight by region instead of airport the flights are grouped by airport, and we want them to return a flattened list so sorting by price works with multiple airports.
* Can't seem to pay for a seat on the createBooking api call.
	* Booking fails when selecting seats that require payment (comfort+ etc). We can select the seat, but the booking fails. Do we need to provide payment in the api to make this work?
	* Bargin finder max is the api.
* Does Sabre have a way to provide a heads up on what would happen on a cancellation action?
	* Is it void? Will it be refunded, etc?
	* 
* When we do exchanges, do we include the original ticket in the exchange? Or is it a new ticket? If it's a new ticket, how do we handle the original ticket? Do we need to void it or cancel it separately? We need to understand the flow of exchanges and cancellations to ensure we're handling them correctly in our system.
	* We don't know how this works at all
* JLaw opened a ticket and they are looking into it. 
	* Case #09210656 -- HotelDetails request is not showing availability as would be expected considering getHotelAvailability requests return a given location.

Carla Cianelli, our technical contact at Sabre, knows more about air, not as much about hotel, etc.