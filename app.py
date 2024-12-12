from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Route:
    def __init__(self, start_state, end_state):
        self.start_state = start_state
        self.end_state = end_state

    def __str__(self):
        return f"{self.start_state} to {self.end_state}"

class Vehicle:
    def __init__(self, name, price, vehicle_type, routes):
        self.name = name
        self.price = price
        self.vehicle_type = vehicle_type
        self.routes = routes

    def __str__(self):
        return f"{self.name} - {self.price:,.0f} Naira ({self.vehicle_type} Bus)"

class BusBoardingSystem:
    def __init__(self):
        self.routes = [
            Route("Lagos", "Abuja"),
            Route("Lagos", "Ibandan"),
            Route("Lagos", "Ilorin"),
            Route("Lagos", "Oshogbo"),
        ]

        self.vehicles = [
            Vehicle("Luxury Car", 15000, "Day", self.routes),
            Vehicle("Standard Car", 10000, "Day", self.routes),
            Vehicle("Luxury Bus", 8000, "Night", self.routes),
            Vehicle("Standard Bus", 17000, "Night", self.routes),
        ]

    def get_vehicles(self, vehicle_type):
        return [vehicle for vehicle in self.vehicles if vehicle.vehicle_type == vehicle_type]

    def get_routes(self):
        return self.routes

    def book_vehicle(self, vehicle, route):
        return f"You have successfully booked the {vehicle.name} from {route} for {vehicle.price:,.0f} Naira."

system = BusBoardingSystem()

@app.route('/')
def index():
    routes = system.get_routes()
    return render_template('index.html', routes=routes)

@app.route('/book', methods=['POST'])
def book():
    route_choice = int(request.form['route_choice'])
    selected_route = system.routes[route_choice - 1]

    time_of_day = request.form['time_of_day']
    vehicles = system.get_vehicles(time_of_day)

    return render_template('vehicles.html', vehicles=vehicles, route=selected_route, time_of_day=time_of_day)

@app.route('/confirm', methods=['POST'])
def confirm():
    route_choice = int(request.form['route_choice'])
    vehicle_choice = int(request.form['vehicle_choice'])
    
    selected_route = system.routes[route_choice - 1]
    selected_vehicle = system.vehicles[vehicle_choice - 1]

    message = system.book_vehicle(selected_vehicle, selected_route)
    return render_template('confirmation.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)