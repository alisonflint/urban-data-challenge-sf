urban-data-challenge-sf
=======================

The Urban Data Challenge asks participants to help improve urban transportation
in their cities by creating apps that make creative use of public transit data.
Our goal is to create an analysis tool that integrates public transit data with
otherways of describing interest points in San Francisco.  For example, how long
does it take to get from The Mission to Outer Sunset or Chinatown?  And when one
travels from a particular stop, what kinds of businesses can they reach and in
what time?  What if they only have 30 minutes to spare for travel?  Does that
cut off the kind of businesses they can reach from some locations?  The same
could be stated for types of employment, schools, parks, or where friends are.
By integrating public transit times with data we know about the city in general,
we can get an idea of how well the public transit system is serving San
Francisco citizens.  And by finding the points it serves well and the points it
fails to serve, we can then improve it to better serve everyone.

How To Get Started
------------------

This project is built using a few core technologies.  

For the server, we use [Django][1].  For the client side, we just [Google
Maps][2] and [D3.js][3].  To get the server running, you'll minimally need to
install the following python packages for [Python 2.7][4]:

  - [django][1]
  - [numpy][5]
  - [decorator][6]

The easiest way to install all these packages is through [pip][7]:

<pre>
  pip install django
  pip install numpy
  pip install decorator
</pre>

Once you've installed all the packages, run the following commands to load up
the server:

<pre>
  cd urban_time
  python manage.py runserver
</pre>

This will load up the web server at [localhost:8000][8], which should now let
you explore the results of our work.

  [1]: https://www.djangoproject.com/
  [2]: https://developers.google.com/maps/
  [3]: http://d3js.org/
  [4]: http://www.python.org/download/releases/2.7/
  [5]: http://www.numpy.org/
  [6]: https://pypi.python.org/pypi/decorator
  [7]: https://pypi.python.org/pypi/pip
  [8]: http://localhost:8000
