#! /usr/bin/perl
#
# Programm: Termine der nächsten Sitzungen der Ortsbeiräte der Stadt Frankfurt am Main aus dem Dokumentensystem Parlis auslesen und im iCal-Format ausgeben.
#
# Parameter:
#		-Optional die Nummer eines bestimmten Ortsbeirats (OB), um nur den Termin diesen OB zu bekommen.
#
# Sonstiges: Verwendet das Modul LWP: http://search.cpan.org/~gaas/libwww-perl-5.836/lib/LWP.pm
#
# Autor: Niko Wenselowski (der@nik0.de) für Frankfurt Gestalten (http://www.frankfurt-gestalten.de/)

use LWP;
use utf8;
use Encode;

#Variable für Debug-Ausgaben.
my $debug = 0;

#Es gibt 16 Ortsbeiräte, deshalb ein Array von 1 bis 16.
my @range = 1..16;

if($#ARGV > -1)
{
	#Wenn wir einen Parameter haben, dann handelt es sich dabei um den Wunsch einen Kalender für einen einzelnen OB zu bekommen.
	@range = shift(@ARGV);
}

#Gerüst des iCals bauen, in welchem die einzelnen Events stehen werden.
print "BEGIN:VCALENDAR\r
VERSION:2.0\r
PRODID:-//Frankfurt-Gestalten.de//Frankfurt-Gestalten.de Informationssystem.//DE\r
METHOD:PUBLISH\r
";

#Schleife für die Ortsteile
for (@range)
{
	#URL festlegen, von der gelesen wird. (Parlis)
	my $url = "http://www.stvv.frankfurt.de/PARLISLINK/DDW?W=DOK_NAME=\'TO-O-$_\'";
	my $ua = LWP::UserAgent->new;

	#Auslesen des Contents
	my $r = $ua->get($url);

	if($r->is_success())
	{
		#Der Request war erfolgreich, wir können mit der Arbeit beginnen.

		#Inhalt der Seite auslesen, umwandeln in UTF8
		my $content = decode('iso-8859-1',$r->content());

		#Nur den Teil mit den relevanten Informationen rausfiltern
		$content = substr($content, index($content,'Einladung') + 9,index($content,'Alle interessierten B') - (index($content,'Einladung') + 9));

		#Viel RegExp-Magic ;)
		$content =~ s/<(.*?)>//gi; #HTML Tags entfernen
		$content =~ s/&nbsp;/ /gi; #&nbsp; ersetzen
		$content =~ s/[\s]{2,}/ /g; #Mehrere hintereinander liegende Leerzeichen durch ein einzelnes ersetzen
		$content =~ s/\015|\012//g; #Steuerzeichen (CR & LF) entfernen
		$content =~ s/&quot;/"/g; #HTML-Notation für Quotation-Marks durch Anführungszeichen ersetzen

		if($content =~ m/zur (\d+)\. Sitzung des Ortsbeirates (\d+) am \w+\, dem (\d+)\. (\w+) (\d{4}), (\d{1,2})\.(\d{2}) Uhr,(.*)/)
		{
			#Die Dokumente folgen dem gleichen Satzaufbau, weshalb explizit nach diesem gesucht wird. Wird er gefunden, so können die Infos ausgelesen werden
			print "-Sitzungs: $1\n-OB: $2\n-Tag: $3\n-Monat: $4 - " . &getMonth($4) . "\n-Jahr: $5\n-Stunde: $6\n-Minute: $7\n-Ort: $8\n" if($debug);

			#Monat bzw. Tag zweistellig ausgeben
			my $monat = sprintf("%02d", &getMonth($4));
			my $tag = sprintf("%02d", $3);

			#Datumsstring bauen
			my $daystring = $5 . $monat . $tag . 'T' . $6 . $7 . '00';

			#Einzelnes Event im iCal-Format erstellen
			print encode('utf8',"BEGIN:VEVENT\r
UID:ob$2-sitzung-$1-$5$monat$tag\@frankfurt-gestalten.de\r
SUMMARY:Ortsbeirat $2: $1. Sitzung\r
DESCRIPTION: Die $1. Sitzung des Ortsbeirates $2\r
LOCATION:Frankfurt am Main,$8\r
URL:$url\r
CLASS:PUBLIC\r
SEQUENCE:1\r
DTSTART;TZID=Europe/Berlin:$daystring\r
END:VEVENT\r\n");
		} else {
			#Es passt nicht das RegEx, wir machen nichts
			print "Inhalt passt nicht zur regular expression.\n" if($debug);
		}
	}
}

#Kalender abschließen
print "END:VCALENDAR\r\n";

#Programm beenden
exit 0;

#Aus dem String Monat ne passende Zahl machen
sub getMonth
{
	my $monat = shift;

	if($monat =~ m/Januar/i) { return 1; }
	elsif($monat =~ m/Februar/i) { return 2; }
	elsif($monat =~ m/März/i) { return 3; }
	elsif($monat =~ m/April/i) { return 4; }
	elsif($monat =~ m/Mai/i) { return 5; }
	elsif($monat =~ m/Juni/i) { return 6; }
	elsif($monat =~ m/Juli/i) { return 7; }
	elsif($monat =~ m/August/i) { return 8; }
	elsif($monat =~ m/September/i) { return 9; }
	elsif($monat =~ m/Oktober/i) { return 10; }
	elsif($monat =~ m/November/i) { return 11; }
	elsif($monat =~ m/Dezember/i) { return 12; }
	else {
		return 0; #Kein passender Monat
	}
}
