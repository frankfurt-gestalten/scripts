#! /usr/bin/perl
#
# This program uses the API from cloudmade to get points in a specified area.
#
# Use: cloudmade-parser.pl <object_types> 
#	-The object_types can be obtained from http://developers.cloudmade.com/wiki/geocoding-http-api/Object_Types
#	-You can give a list of object types and the script will try to get as many points as possible for it
#
# Autor: Niko Wenselowski (der@nik0.de) for Frankfurt Gestalten (http://www.frankfurt-gestalten.de/)

use strict;
use utf8;
use Encode;
#Modules for the web-stuff
use LWP;
use JSON -support_by_pp;

#the Key for the cloudmade API - get your own from http://www.cloudmade.com/user/show
my $cmAPIkey = '---INSERT YOUR KEY HERE---';


#Variables for the square in which we search
#Right now this covers Frankfurt/Main, Germany
my $latitudeStart = '50.1964';
my $longitudeStart = '8.5983';
my $latitudeEnd = '50.067';
my $longitudeEnd = '8.8259';

my $debug = 0;
#--- no need to change anything beyond this point ---

#Check for Arguments
if($#ARGV == -1)
{
  #we need at least one argument

  #give user some help about the usage:
  print "Use: cloudmade-parser.pl <object_types>
\t-The object_types can be obtained from http://developers.cloudmade.com/wiki/geocoding-http-api/Object_Types
\t-You can give a list of object types and the script will try to get as many points as possible for it\n";

  #exit the program
  exit -1;
}

#--PREPARE SCRIPT--
#Values for OSM tags can be found at http://developers.cloudmade.com/wiki/geocoding-http-api/Object_Types

#Prepare vars for the processing
my $realResults = 0;
my $resultsPerQuery = 100; #process 100 objects with each run. 100 worked pretty well for me.

#Prepare encoding-object for faster en/decode
my $enc = find_encoding('utf8');


#write the header for the csv
print "Name;Latitude;Longitude\n";
#--END PREPARE SCRIPT--

while(@ARGV)
{
  my $object_type = shift(@ARGV);

  #(re)setting the vars for every object
  my $emptyRuns = 0;
  my $numberOfLoopRuns = 0;
  my $doLoop = 1;
  
  print "\nLooking for: $object_type\n" if $debug;

  while($doLoop)
  {
    my $skipResults = $numberOfLoopRuns * $resultsPerQuery;
    my $tmpResults = 0;
    
    if( ($skipResults + $resultsPerQuery) <= 1000 )
    {
      #Idee: Liste zurückgeben. Über die iterieren.
      #Dann kann man auch die Anzahl der Items wieder beliebig genau machen.
      $tmpResults = getPoints("http://geocoding.cloudmade.com/$cmAPIkey/geocoding/v2/find.js?bbox=$latitudeStart,$longitudeStart,$latitudeEnd,$longitudeEnd&object_type=$object_type&skip=$skipResults&results=$resultsPerQuery");
    } else {
      #Cloudmade won't let us skip that many objects, so we need a workaround...
      #This is a bug that has been reported. See this thread for more information: http://support.cloudmade.com/forums/general/posts/1732/show?page=1
      $doLoop = 0;
    }

    $realResults += $tmpResults;

    if($tmpResults == 0)
    {
      $emptyRuns++;
    } else {
      #don't forget to reset 
      $emptyRuns = 0;
    }
    
    if(($emptyRuns > 2))
    {
      #Went through the loop too
      print "Quitting the search for $object_type\n" if $debug;
      $doLoop = 0;
    }

    $numberOfLoopRuns++;
  }
}

print "\nFound $realResults points\n" if $debug;

#finished
exit 0;



sub getPoints
{
  my ($json_url) = @_;
  my $browser = LWP::UserAgent->new();
  my $realResults = 0;

  eval
  {
    # download the json page:
    print "\nGetting json $json_url\n" if $debug;
    #$browser->get( $json_url );
    my $content = $browser->get($json_url)->content();
    my $json = new JSON;

    # these are some nice json options to relax restrictions a bit:
    my $json_text = $json->allow_nonref->utf8->relaxed->escape_slash->loose->allow_singlequote->allow_barekey->decode($content);

    # iterate over each episode in the JSON structure:
    foreach my $feature(@{$json_text->{features}})
    {
      #We only want single points
      if($feature->{centroid}->{type} eq 'POINT')
      {
	print $enc->encode($realResults . ";") if($debug);

	#print what we got
	print $enc->encode($feature->{properties}->{name}. ";" . $feature->{centroid}->{coordinates}[0] . ";" . $feature->{centroid}->{coordinates}[1] . "\n");

	#yay, we got a result :)
	$realResults++;
      } else {
	print $enc->encode('kein Punkt!') if($debug);
      }
    }
  };

  if($@)
  {
    #Tell the user about problems
    print $enc->encode("[[JSON ERROR]] JSON parser crashed! $@\n");
  }

  return $realResults;
}