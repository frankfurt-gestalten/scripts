#! /usr/bin/perl
#
# This program uses the API from cloudmade to get points in a specified area.
#
# Use: cloudmade-parser.pl <object_type> <number of objects>
#	-The object_type can be obtained from http://developers.cloudmade.com/wiki/geocoding-http-api/Object_Types
#	-Remeber to insert your API key before running this
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
if($#ARGV < 1)
{
  #less than 2 arguments, here is something missing!

  #give user some help about the usage:
  print 'halp here!';

  #exit the program
  exit -1;
}

#--PREPARE SCRIPT--
#Values for OSM tags can be found at http://developers.cloudmade.com/wiki/geocoding-http-api/Object_Types
my $object_type = shift(@ARGV);
my $wantedresults = shift(@ARGV)];

#Prepare vars for the processing
my $realResults = 0;
my $loopRuns = 0;
my $emptyRun = 0;

#Prepare encoding-object for faster en/decode
my $enc = find_encoding('utf8');
#--END PREPARE SCRIPT--

while(($emptyRun < 2) && ($realResults < $wantedresults))
{
  my $skipResults = ($loopRuns * $wantedresults);
  my $actualResults = $realResults;

  getPoints("http://geocoding.cloudmade.com/$cmAPIkey/geocoding/v2/find.js?bbox=$latitudeStart,$longitudeStart,$latitudeEnd,$longitudeEnd&object_type=$object_type&skip=$skipResults&results=$wantedresults");

  if($actualResults == $realResults)
  {
    #no results were found
    $emptyRun++;
    print "no results during loop - $emptyRun\n" if $debug;
  } else {
    #reset variable if results were found
    $emptyRun = 0;
  }

  $loopRuns++;
}

if($emptyRun == 2)
{
  #Search was aborted because of too much empty runs and we inform our user about it.
  print "Only found $realResults instead of your requested $wantedresults - sorry.\n";
}

#finished
exit 0;


sub getPoints
{
  my ($json_url) = @_;
  my $browser = LWP::UserAgent->new();

  eval
  {
    # download the json page:
    print "Getting json $json_url\n" if $debug;
    #$browser->get( $json_url );
    my $content = $browser->get($json_url)->content();
    my $json = new JSON;

    # these are some nice json options to relax restrictions a bit:
    my $json_text = $json->allow_nonref->utf8->relaxed->escape_slash->loose->allow_singlequote->allow_barekey->decode($content);

    # iterate over each episode in the JSON structure:
    foreach my $feature(@{$json_text->{features}})
    {
      #Do we still need more results?
      if($realResults < $wantedresults)
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
    }
  };

  if($@)
  {
    #Tell the user about problems
    print $enc->encode("[[JSON ERROR]] JSON parser crashed! $@\n");
  }
}
