#! /usr/bin/perl
#
# Programm: Termine der nächsten Schadstoffsammeltermine der FES in Frankfurt am Main auslesen und im iCal-Format ausgeben.
#
# Parameter: -
#
# Sonstiges: Verwendet das Modul LWP: http://search.cpan.org/~gaas/libwww-perl-5.836/lib/LWP.pm
#
# Autor: Niko Wenselowski (der@nik0.de) für Frankfurt Gestalten (http://www.frankfurt-gestalten.de/)

use LWP;
use utf8; #Unicode
use Encode; #Für die Umwandlung der Seite in UTF8

my $ua = LWP::UserAgent->new;

#Adresse, wird später auch beim Event verwendet
my $url = 'http://www.muellmax.de/fes/mobil/mobil_1.php';

#Auslesen des Contents
my $r = $ua->get($url);

if($r->is_success())
{
  #Der Request war erfolgreich, wir können mit der Arbeit beginnen.

  #Gerüst des iCals bauen, in welchem die einzelnen Events stehen werden.
  print "BEGIN:VCALENDAR\r
VERSION:2.0\r
PRODID:-//Frankfurt-Gestalten.de//Frankfurt-Gestalten.de Informationssystem.//DE\r
METHOD:PUBLISH\r";

	#Encoding ist ISO-8859-1, wir bereiten uns ein Encoding-Objekt für die schnellere Verarbeitung vor
	my $encoding = find_encoding('iso-8859-1');

	#Auslesen des Inhalts ($r-content), umwandeln in UTF8 von iso-8859-1, splitten
 	my @cont = split(/\n/,$encoding->decode($r->content));

	my ($newevent, $termin, $uhrzeit, $ort, $startzeit, $endzeit);

	#Var intialisieren
	$newevent = 0;

	foreach my $line (@cont)
	{
		$line =~ s/\015\012//g; #Windows-Newline-Zeichen entfernen...
		$line =~ s/\n//g;

		if($line =~ m/class=\"mobtermin\" headers=\"termin\"/)
		{
			$newevent = 1;
			$termin = $line;

			$termin = substr($line,index($line,'<strong>') + 8,10);

			#Hier fehlt noch die Uhrzeit!
			my $ind = index($line,'<br />',2) + 6;
			$uhrzeit = substr($line,$ind,index($line,' Uhr</th>',2) - $ind);

			#Datum auseinanderbauen fuer Start- und Endzeit
			if($uhrzeit =~ m/(\d{2}.\d{2}) -(\d{2}.\d{2})/)
			{
				$startzeit = $1;
				$endzeit = $2;
			} else {
			#Keine passende Uhrzeit gefunden... :(
			}
		}
		elsif($line =~ m/class=\"mobstandort\" headers=\"standort\"/)
		{
			$newevent += 1;
			$ort = $line;

			$ort = substr($line,index($line,'headers="standort">') + 19);
			$ort =~ s/<br \/>/, /g;
			$ort =~ s/<\/td>//g;
		}

    		if($newevent == 2)
		{
			my $shortOrt = '';
			my $id = '';

			#Vorbereiten des Ortes:
			if(length($ort) < 200 && length($ort) > 0)
			{
				#Kurze Ortsangabe bauen - alles vor dem Komma gehört dazu
				if($ort =~ m/([\w\s]+),/)
				{
					$shortOrt = $1;

					$id = $shortOrt;
					$id =~ s/\W/_/g;
				}

				#Länge der Ortsangabe akzeptabel, baue Ortsangabe
				$ort = "LOCATION:Frankfurt am Main, $ort\r";
				} else {
					#Ort zu groß oder zu klein? Dann keine Angabe
					$ort = '';
					#Zufaellige Zahl fuer die Event-ID
					$id = int(rand(10000));
      				}

				#Zeitstrings zusammenbauen
				#Datum vorbereiten (in Format YYYYMMDD bringen)
				$termin =~ s/(\d{2}).(\d{2}).(\d{4})/$3$2$1/;
				#Startzeit
				$startzeit =~ s/(\d\d).(\d\d)/$1$2/;
				$startzeit = $termin . 'T' . $startzeit . '00';
				#Endzeit
				$endzeit =~ s/(\d\d).(\d\d)/$1$2/;
				$endzeit = $termin . 'T' . $endzeit . '00';

				#Einzelnes Event im iCal-Format erstellen (muss laut RFC 2445 UTF8 sein)
				print encode('utf8',"BEGIN:VEVENT\r
UID:fes-schadstoffmobil-$id-$startzeit\@frankfurt-gestalten.de\r
SUMMARY:FES: Schadstoffmobil in $shortOrt\r
DESCRIPTION: Das Schadstoffmobil der FES ermöglicht die Abgabe von Sonderabfällen. Bitte beachten Sie die Hinweise unter http://www.muellmax.de/fes/mobil/mobil_i.htm.\r
$ort
URL:$url\r
CLASS:PUBLIC\r
SEQUENCE:1\r
DTSTART;TZID=Europe/Berlin:$startzeit\r
DTEND;TZID=Europe/Berlin:$endzeit\r
END:VEVENT\r\n");

				#reset der Strings...
				$termin = '';
				$ort = '';
				$startzeit = '';
				$endzeit = '';

				$newevent = 0;
    			}
		}

		#Kalender abschließen
		print 'END:VCALENDAR';

		#Script beendet
  		exit 0;
	} else {
		#Holen des Contents war nicht erfolgreich
		exit -1;
	}

