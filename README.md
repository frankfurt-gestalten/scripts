# DESCRIPTION
Here are some of the scripts we use to create http://www.frankfurt-gestalten.de.
Have fun playing around with em.

## cloudmade/cloudmade-parser.pl
A script to get objects from cloudmade in a specified area. Cloudmade renders maps from openstreetmap.org and provides a API to access.
With the default setting the script searches in a area around and including Frankfurt. You can alter the searched area within the script

## events/fes-schadstoffmobil-termine.pl
A script to retrieve the next dates and locations for the hazardous substances collecting vehicle. This is service of the FES in Frankfurt.

# USAGE
## cloudmade/cloudmade-parser.pl
This script needs one or more object_types as arguments.
The possible object_types can be obtained from http://developers.cloudmade.com/wiki/geocoding-http-api/Object_Types
The output is formatted like a csv-file would be. Feel free to pipe the output into a file.

## events/fes-schadstoffmobil-termine.pl
This scripts needs no arguments.
The output is formatted like a .ics-file.

# QUESTIONS
You have any questions left? Feel free to ask.

# REMEMBER
The sripts are delivered "as is" without any warranty.
