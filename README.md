Uber Coding Challenge
=====================

<h2>Bicycle Parking</h2>

A service providing the nearest bicycle parkings for a given location and the directions to the chosen parking.<br/>
The data is provided by <a href="http://www.datasf.org/">DataSF</a>: <a href="https://data.sfgov.org/Transportation/Bicycle-Parking-Public-/w969-5mn4">Bicycle Parking</a>

<h3>Technical Choices</h3>
For this coding challenge, I chose to implement a back-end with a minimal front end using the Django web framework and the Google Maps API. This is the first Django and Python application that I have written. The reasons for choosing this framework and language were
<ol>
<li>Most of Uber's back-end uses Python.</li>
<li>Learning new technologies and languages is always good.</li>
<li>A better idea of what the engineering tasks at Uber might be like.</li>
<li>Different web framework and language, but analogous concepts and patterns to Ruby on Rails.</li>
<li>Django has a good community with good documentation.</li>
</ol>

<h4>Files with Code I Wrote</h4>
<ul>
<li>bike_parkings/googlemaps.py</li>
<li>bike_parkings/models.py</li>
<li>bike_parkings/views.py</li>
<li>bike_parkings/urls.py</li>
<li>bike_parkings/tests.py</li>
<li>bike_parkings/admin.py</li>
<li>bike_parkings/templates/bike_parkings/base.html</li>
<li>bike_parkings/templates/bike_parkings/index.html</li>
<li>bike_parkings/templates/bike_parkings/nearest_locations.html</li>
<li>bike_parkings/templates/bike_parkings/directions.html</li>
<li>bike_parkings/scripts/load_bicycle_parking_data.py</li>
</ul>

<h4>Potential Improvements and Trade-offs</h4>
<ol>
<li>Better Error Handling: Rather than just an 'OK' or 'ERROR' status that is returned with the GeographicalCoordinates and Directions objects, the statuses can be more descriptive and used to better help the client display to users what problem they encountered, ie invalid address, no possible route, etc</li>
<li>Making the Front-End an App: To have a user facing interface, without building a single page application, the Django view renders the web pages, instead of returning JSON objects. By making the front-end an application that can receive and parse JSON, I can improve the API to return JSON and be more platform agnostic.</li>
<li>Delegating the Google Maps API Requests to the Client: Rather than having the back-end request the address to geographical coordinates translation and directions from Google, it could be possible to have the front-end do these requests to reduce the server load. The client would take an address, request the geographical coordinates from Google, and then send those coordinates to the back-end. The back-end would return a list of the nearest bike parkings. The client would let the user pick which parking and request the directions from Google.</li>
<li>More Precise Start Address and End Address on Directions Page: Currently, the back-end requests directions from the Google Maps Directions API using geographical coordinates for the start and end locations since these were used to calculate the nearest bike parking locations. When Google returns the directions, the start address and end address might not exactly match the addresses the user saw and could cause for some confusion, ie 576 Natoma St -> geographical coordinates -> 572 Natoma St.</li>
</ol>

<h3>Other Links</h3>
<p>Other Code Sample: <a href="https://github.com/sarahtran/programming_problems">GitHub</a></p>
<p>Public Profile: <a href="https://www.linkedin.com/pub/sarah-tran/25/779/13a">LinkedIn</a></p>
