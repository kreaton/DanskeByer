#!/usr/bin/env python3
"""Generates towns.json, sights.json and denmark.json for the Danske Byer game.

Usage: gen_data.py <out-dir> [natural-earth-countries.geojson]
The map outline (denmark.json) is only rebuilt when the Natural Earth file is given.

Area is the part of the country a town is on. Jylland is a peninsula, so it is "i Jylland";
the others are islands, so it is "på Sjælland / Fyn / Bornholm / Lolland-Falster / Mors".
"""
import json, math, sys, pathlib

OUT = pathlib.Path(sys.argv[1])
NE = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else None
TOWN_COUNT = 75
AREAS = {"Jylland", "Sjælland", "Fyn", "Bornholm", "Lolland-Falster", "Mors"}

# id, name, population (rounded, ca.), lat, lon, region, area, wiki(en), description, clue
# Towns 51-75 use Danmarks Statistik BY1, 1 January 2026. Towns in Greater Copenhagen's
# suburban belt (Lillerød, Værløse, Dragør …) are counted as part of København and left out.
T = [
("koebenhavn","København",1408600,55.6761,12.5800,"Hovedstaden","Sjælland","Copenhagen",
 "Danmarks hovedstad og største by. Kongefamilien bor på Amalienborg, og byen er fuld af spændende steder som Tivoli, Nyhavn og Den Lille Havfrue. Tallet gælder hele hovedstadsområdet, ikke kun selve kommunen.",
 "Danmarks hovedstad. Her bor kongefamilien på Amalienborg, og her ligger Tivoli, Nyhavn og en lille havfrue på en sten."),
("aarhus","Aarhus",300000,56.1629,10.2039,"Midtjylland","Jylland","Aarhus",
 "Danmarks næststørste by og den største i Jylland. Her ligger Den Gamle By med små gamle huse, og kunstmuseet ARoS med en regnbue på taget.",
 "Jyllands største by og Danmarks næststørste. Her ligger en hel gammel by som museum, og et kunstmuseum med en farvet regnbue på taget."),
("odense","Odense",182000,55.3959,10.3883,"Syddanmark","Fyn","Odense",
 "Fyns hovedby og Danmarks tredjestørste by. Eventyrdigteren H.C. Andersen blev født her i 1805. Du kan besøge hans barndomshjem og museum.",
 "Hovedbyen på Fyn. Her blev eventyrdigteren H.C. Andersen født i 1805, og han skrev om Den grimme ælling og Klods-Hans."),
("aalborg","Aalborg",120000,57.0488,9.9217,"Nordjylland","Jylland","Aalborg",
 "Nordjyllands største by ved Limfjorden. Man kan køre under fjorden i Limfjordstunnelen eller over den på broerne. Byen har også en stor zoologisk have.",
 "Nordjyllands største by. Den ligger ved en lang fjord, og man kan køre i en tunnel under vandet for at komme til den anden side."),
("esbjerg","Esbjerg",72000,55.4760,8.4590,"Syddanmark","Jylland","Esbjerg",
 "En stor havneby ved Vesterhavet. Herfra sejler færger til øen Fanø, og ved havnen står de fire store hvide mænd 'Mennesket ved Havet'.",
 "En stor havneby ved Vesterhavet. Der står fire kæmpestore, hvide mænd og kigger ud over havet, og en færge sejler til øen Fanø."),
("horsens","Horsens",64000,55.8607,9.8503,"Midtjylland","Jylland","Horsens",
 "Byen ved Horsens Fjord. Her lå et stort fængsel, som i dag er museum og koncertsted.",
 "En by ved en fjord i Østjylland. Et stort gammelt fængsel er blevet til museum, og der holdes koncerter derinde."),
("randers","Randers",63000,56.4607,10.0364,"Midtjylland","Jylland","Randers",
 "Byen ligger ved Gudenåen, Danmarks længste å. Her kan du besøge Randers Regnskov med aber, papegøjer og krokodiller.",
 "En by ved Danmarks længste å. Her findes en regnskov under tag, hvor man kan se aber og papegøjer."),
("kolding","Kolding",62000,55.4904,9.4722,"Syddanmark","Jylland","Kolding",
 "Her ligger slottet Koldinghus, som brændte i 1808 og senere blev bygget op igen. I dag er det et museum.",
 "Her ligger et gammelt kongeslot, som brændte i 1808 og senere blev bygget op igen som museum."),
("vejle","Vejle",60000,55.7090,9.5357,"Syddanmark","Jylland","Vejle",
 "En by i bunden af Vejle Fjord. I havnen står Fjordenhus, en bygning der står ude i vandet, og boligblokkene Bølgen ligner bølger.",
 "En by i bunden af en lang fjord. I havnen står en kunstnerbygning ude i vandet, og nogle boligblokke er formet som bølger."),
("roskilde","Roskilde",53000,55.6415,12.0803,"Sjælland","Sjælland","Roskilde",
 "Her ligger Roskilde Domkirke, hvor mange danske konger og dronninger er begravet, og Vikingeskibsmuseet med rigtige vikingeskibe. Hver sommer er der Roskilde Festival.",
 "Her ligger en domkirke på verdensarvslisten, hvor mange konger er begravet, og et museum med vikingeskibe. Hver sommer holdes en kæmpe musikfestival."),
("herning","Herning",51000,56.1396,8.9732,"Midtjylland","Jylland","Herning",
 "En by i Midtjylland, som voksede op omkring fabrikker der lavede strikvarer og tøj. I dag er der messecenter, store koncerter og kunstmuseet HEART.",
 "En by midt i Jylland, som i gamle dage var kendt for fabrikker med strikvarer og tøj. I dag er der en stor messe- og koncerthal."),
("silkeborg","Silkeborg",50000,56.1697,9.5451,"Midtjylland","Jylland","Silkeborg",
 "Byen ligger i Søhøjlandet, omgivet af søer og skov. På museet ligger Tollundmanden, en mand der er over 2.000 år gammel og blev fundet i en mose.",
 "En by midt i et land af søer og skove. På museet ligger en mand, der er over 2.000 år gammel og blev fundet i en mose."),
("helsingoer","Helsingør",47000,56.0361,12.6136,"Hovedstaden","Sjælland","Helsingør",
 "Her ligger Kronborg Slot, hvor Shakespeares skuespil Hamlet foregår. Fra byen kan man se over til Sverige, som kun er fire kilometer væk.",
 "Her ligger et slot, hvor Shakespeares Hamlet foregår. Man kan se over til Sverige, som kun er fire kilometer væk."),
("naestved","Næstved",44000,55.2299,11.7609,"Sjælland","Sjælland","Næstved",
 "Sydsjællands største by ved åen Suså. Tæt på ligger kostskolen Herlufsholm, som blev grundlagt i 1565.",
 "Sydsjællands største by, ved en å der hedder Suså. I nærheden ligger en meget gammel kostskole."),
("viborg","Viborg",42000,56.4532,9.4020,"Midtjylland","Jylland","Viborg, Denmark",
 "En af Danmarks ældste byer, med en stor domkirke og søer lige midt i byen.",
 "En af Danmarks ældste byer, med en stor domkirke og søer lige midt i byen."),
("fredericia","Fredericia",41000,55.5657,9.7527,"Syddanmark","Jylland","Fredericia",
 "En fæstningsby, som kong Frederik 3. lod bygge i 1650. Man kan stadig gå på de gamle volde. Byen ligger ved Lillebælt.",
 "En by med volde og grave rundt om sig, bygget som fæstning af kong Frederik 3. i 1650 ved Lillebælt."),
("koege","Køge",41000,55.4580,12.1821,"Sjælland","Sjælland","Køge",
 "En gammel havneby syd for København. I 1677 vandt admiral Niels Juel et stort søslag over svenskerne i Køge Bugt.",
 "En gammel havneby syd for København. Her vandt admiral Niels Juel i 1677 et stort søslag mod svenskerne."),
("holstebro","Holstebro",37000,56.3601,8.6165,"Midtjylland","Jylland","Holstebro",
 "En vestjysk by ved Storåen, kendt for kunst og skulpturer på mange pladser og for det internationale teater Odin Teatret.",
 "En vestjysk by ved en å, hvor der står kunst og skulpturer på mange gader og pladser."),
("hilleroed","Hillerød",36000,55.9279,12.3011,"Hovedstaden","Sjælland","Hillerød",
 "Her ligger Frederiksborg Slot, et stort slot bygget på tre små øer i en sø. I dag er det Det Nationalhistoriske Museum.",
 "Her ligger et stort slot, som er bygget på tre små øer i en sø, og som i dag er et museum."),
("slagelse","Slagelse",34000,55.4028,11.3546,"Sjælland","Sjælland","Slagelse",
 "Tæt på byen ligger Trelleborg, en vikingeborg fra omkring år 980, formet som en perfekt rund cirkel.",
 "I nærheden ligger en vikingeborg, som er omkring 1.000 år gammel og formet som en perfekt rund cirkel."),
("holbaek","Holbæk",28000,55.7175,11.7167,"Sjælland","Sjælland","Holbæk",
 "En hyggelig havneby i Nordvestsjælland ved en fjordarm af Isefjorden.",
 "En havneby i Nordvestsjælland ved en fjordarm af Isefjorden."),
("svendborg","Svendborg",27500,55.0598,10.6068,"Syddanmark","Fyn","Svendborg",
 "En by på Sydfyn, hvor der i mange år blev bygget skibe. Man kan sejle eller køre over broen til øen Tåsinge, hvor Valdemars Slot ligger.",
 "En by på Sydfyn ved et smalt sund, hvor man i mange år byggede skibe. Over sundet er der en bro til øen Tåsinge."),
("soenderborg","Sønderborg",27000,54.9094,9.7921,"Syddanmark","Jylland","Sønderborg",
 "En by på øen Als i Sønderjylland. Her ligger et gammelt slot ved sundet, og tæt på ligger Dybbøl, hvor der var et stort slag i 1864.",
 "En by på en ø i Sønderjylland. Her ligger et gammelt slot ved sundet, og tæt på lå et stort slag i 1864."),
("hjoerring","Hjørring",26000,57.4642,9.9822,"Nordjylland","Jylland","Hjørring",
 "Vendsyssels hovedby, helt oppe i Nordjylland. I nærheden ligger Rubjerg Knude Fyr, som blev flyttet i 2019, fordi en sanddyne var ved at sluge det.",
 "Hovedbyen i Vendsyssel, helt oppe nordpå. I nærheden ligger et fyr, som er blevet flyttet, fordi en sanddyne var ved at sluge det."),
("frederikshavn","Frederikshavn",23000,57.4407,10.5366,"Nordjylland","Jylland","Frederikshavn",
 "En havneby helt oppe i Nordjylland, hvor store færger sejler til Sverige og Norge. Tæt på ligger Råbjerg Mile, en kæmpe vandresanddyne.",
 "En havneby øverst i Jylland, hvor store færger sejler til Sverige og Norge."),
("haderslev","Haderslev",22000,55.2494,9.4909,"Syddanmark","Jylland","Haderslev",
 "En by i Sønderjylland ved en lang smal fjord. Byen har en stor domkirke og en dam midt i byen.",
 "En by i Sønderjylland ved en lang smal fjord, med en stor domkirke og en dam midt i byen."),
("ringsted","Ringsted",21000,55.4430,11.7900,"Sjælland","Sjælland","Ringsted",
 "En by midt på Sjælland. Sankt Bendts Kirke er gravkirke for mange middelalderkonger og -dronninger, og byen er et vigtigt sted, hvor tog mødes.",
 "En by midt på Sjælland med en kirke, hvor mange konger og dronninger fra middelalderen blev begravet."),
("skanderborg","Skanderborg",20400,56.0449,9.9276,"Midtjylland","Jylland","Skanderborg",
 "En by ved en stor sø med et gammelt slot. Hver sommer holdes musikfestivalen Smukfest i skoven ved byen.",
 "En by ved en stor sø med et gammelt slot. Hver sommer holdes der en musikfestival i skoven."),
("skive","Skive",20100,56.5667,9.0333,"Midtjylland","Jylland","Skive, Denmark",
 "En by ved en fjord i Nordvestjylland. Tæt på ligger Spøttrup Borg, en rigtig middelalderborg med voldgrav.",
 "En by ved en fjord i Nordvestjylland. Tæt på ligger en rigtig middelalderborg med voldgrav."),
("nyborg","Nyborg",18000,55.3120,10.7890,"Syddanmark","Fyn","Nyborg",
 "En by på Fyns østkyst med et meget gammelt kongeslot. Før Storebæltsbroen åbnede i 1998, sejlede færgerne herfra til Sjælland.",
 "En by på Fyns østkyst med et meget gammelt kongeslot. Før broen kom i 1998, sejlede færger herfra til Sjælland."),
("solroed","Solrød Strand",18000,55.5300,12.2200,"Sjælland","Sjælland","Solrød Strand",
 "En by ved en lang sandstrand syd for København. Mange bor her og tager toget til hovedstaden.",
 "En by ved en lang sandstrand syd for København. Mange bor her og tager toget ind til hovedstaden."),
("frederikssund","Frederikssund",17600,55.8400,12.0700,"Hovedstaden","Sjælland","Frederikssund",
 "Hver sommer opfører byen Vikingespillet, hvor frivillige klæder sig ud som vikinger. Byen ligger ved Roskilde Fjord.",
 "Hver sommer spiller byen et stort vikingespil, hvor mennesker klæder sig ud som vikinger. Byen ligger ved en fjord nordvest for København."),
("ikast","Ikast",16800,56.1392,9.1578,"Midtjylland","Jylland","Ikast",
 "En by i Midtjylland, der er vokset op omkring tekstilfabrikker. Fodboldklubben FC Midtjylland blev dannet af klubber fra Ikast og Herning.",
 "En by i Midtjylland, hvor der i gamle dage var mange tekstilfabrikker. En stor fodboldklub har rødder her."),
("middelfart","Middelfart",16700,55.5063,9.7309,"Syddanmark","Fyn","Middelfart",
 "Her krydser to store broer Lillebælt over til Jylland. I vandet kan man se marsvin, så byen kaldes også Marsvinebyen.",
 "Her krydser to store broer det smalle farvand Lillebælt over til Jylland, og i vandet kan man se marsvin."),
("nykoebing-f","Nykøbing Falster",16700,54.7690,11.8760,"Sjælland","Lolland-Falster","Nykøbing Falster",
 "Hovedbyen på øen Falster ved Guldborgsund. Fra Sjælland kommer man hertil over den lange Storstrømsbro.",
 "Hovedbyen på en ø syd for Sjælland. Man kommer hertil over en meget lang bro."),
("kalundborg","Kalundborg",16700,55.6795,11.0876,"Sjælland","Sjælland","Kalundborg",
 "En by i Vestsjælland med Vor Frue Kirke, en middelalderkirke med fem tårne. Færger sejler herfra til øen Samsø.",
 "En by i Vestsjælland med en middelalderkirke med hele fem tårne. Færger sejler herfra til øen Samsø."),
("aabenraa","Aabenraa",16500,55.0443,9.4175,"Syddanmark","Jylland","Aabenraa",
 "En by ved en fjord i Sønderjylland, ikke langt fra den tyske grænse.",
 "En by ved en fjord i Sønderjylland, ikke langt fra den tyske grænse."),
("korsoer","Korsør",14300,55.3300,11.1400,"Sjælland","Sjælland","Korsør",
 "En by på Sjællands vestkyst, hvor Storebæltsbroen begynder. Her ligger også en gammel fæstning, som skulle beskytte mod fjender.",
 "En by på Sjællands vestkyst, hvor en kæmpebro over Storebælt begynder. Her ligger også en gammel fæstning."),
("varde","Varde",14300,55.6213,8.4800,"Syddanmark","Jylland","Varde, Denmark",
 "En by i Vestjylland ved Varde Å. I nærheden ligger forlystelsesparken Varde Sommerland med vandrutsjebaner.",
 "En by i Vestjylland ved en å. I nærheden ligger en stor sommerland-forlystelsespark med vandrutsjebaner."),
("grenaa","Grenaa",14100,56.4150,10.8800,"Midtjylland","Jylland","Grenaa",
 "En by på Djursland ved Kattegat. Her ligger akvariet Kattegatcentret, og færgen til øen Anholt sejler herfra.",
 "En by på Djursland ved Kattegat. Her ligger et stort akvarium, og færgen til øen Anholt sejler herfra."),
("roenne","Rønne",13700,55.1005,14.7066,"Hovedstaden","Bornholm","Rønne",
 "Bornholms største by, langt ude i Østersøen. På øen er der borgruinen Hammershus og flere runde kirker. Færger sejler til Sverige og Køge.",
 "Den største by på en ø langt mod øst i Østersøen. Øen har runde kirker og en stor borgruin, og færger sejler herfra til Sverige."),
("odder","Odder",13500,55.9700,10.1500,"Midtjylland","Jylland","Odder",
 "En by i Østjylland mellem Aarhus og Horsens. Tæt på ligger havnen i Hou, hvor færgen sejler til øen Samsø.",
 "En by i Østjylland mellem to store byer. Tæt på er der en havn, hvor færgen sejler til øen Samsø."),
("thisted","Thisted",13500,56.9558,8.6948,"Nordjylland","Jylland","Thisted",
 "En by i Thy i Nordvestjylland. Her kan man surfe i bølgerne ved Cold Hawaii og besøge Nationalpark Thy, Danmarks første nationalpark.",
 "En by i Nordvestjylland. I nærheden kan man surfe i bølgerne ved Cold Hawaii og besøge Danmarks første nationalpark."),
("hedensted","Hedensted",13500,55.7700,9.7000,"Midtjylland","Jylland","Hedensted",
 "En by i Østjylland mellem Horsens og Vejle, som voksede op omkring jernbanen. I kommunen ligger også badebyen Juelsminde.",
 "En by i Østjylland mellem to større byer, som voksede op omkring jernbanen. I kommunen ligger også en badeby."),
("broenderslev","Brønderslev",12900,57.2700,9.9400,"Nordjylland","Jylland","Brønderslev",
 "En by i Vendsyssel i Nordjylland, omkring 25 kilometer nord for Aalborg.",
 "En by i Vendsyssel i Nordjylland, omkring 25 kilometer nord for Aalborg."),
("frederiksvaerk","Frederiksværk",12800,55.9700,12.0200,"Hovedstaden","Sjælland","Frederiksværk",
 "I gamle dage blev der støbt kanoner her. Tæt på ligger Arresø, som er Danmarks største sø.",
 "I gamle dage blev der støbt kanoner her, og tæt på ligger Danmarks største sø."),
("haslev","Haslev",12600,55.3500,11.9700,"Sjælland","Sjælland","Haslev",
 "En by på Sydsjælland. I nærheden ligger Faxe Kalkbrud, et kæmpe hul fyldt med fossiler fra dengang, der var hav.",
 "En by på Sydsjælland. I nærheden ligger et kæmpe kalkbrud fyldt med fossiler fra dengang, der var hav."),
("hobro","Hobro",12400,56.6400,9.7900,"Nordjylland","Jylland","Hobro",
 "En by ved bunden af Mariager Fjord. Tæt på ligger Fyrkat, en 1.000 år gammel rund vikingeborg.",
 "En by ved bunden af en fjord i Nordjylland. Tæt på ligger en 1.000 år gammel rund vikingeborg."),
("nakskov","Nakskov",12200,54.8300,11.1500,"Sjælland","Lolland-Falster","Nakskov",
 "Den største by på øen Lolland, ved en fjord. Byen var i mange år kendt for et stort skibsværft, og på Lolland dyrkes mange sukkerroer.",
 "Den største by på øen Lolland, ved en fjord. Der lå i mange år et stort skibsværft, og på øen dyrkes mange sukkerroer."),
("vordingborg","Vordingborg",12100,55.0080,11.9100,"Sjælland","Sjælland","Vordingborg",
 "En by på Sydsjælland med Gåsetårnet, et højt tårn med en guldgås på toppen. I nærheden ligger de hvide kridtklinter Møns Klint.",
 "En by på Sydsjælland med et højt tårn med en guldgås på toppen. I nærheden ligger de hvide kridtklinter på Møn."),
# ---- 51-75 (Svær) ----
("jyllinge","Jyllinge",10900,55.7514,12.1050,"Sjælland","Sjælland","Jyllinge",
 "En by ved Roskilde Fjord nord for Roskilde. Den var engang et lille fiskerleje, og i dag ligger der en stor lystbådehavn.",
 "En by ved en fjord nord for en domkirkeby. Den var engang et lille fiskerleje, og i dag ligger der mange lystbåde i havnen."),
("vejen","Vejen",10400,55.4813,9.1376,"Syddanmark","Jylland","Vejen",
 "En by i Sydjylland mellem Kolding og Esbjerg. Foran Vejen Kunstmuseum står en stor, uhyggelig trold af bronze, lavet af billedhuggeren Niels Hansen Jacobsen.",
 "En by i Sydjylland mellem Kolding og Esbjerg. Foran kunstmuseet står en stor, uhyggelig trold af bronze."),
("lystrup","Lystrup",10100,56.2378,10.2367,"Midtjylland","Jylland","Lystrup",
 "En by lige nord for Aarhus. Mange familier bor her og tager letbanen ind til storbyen.",
 "En by lige nord for Danmarks næststørste by. Mange familier bor her og tager letbanen ind til storbyen."),
("helsinge","Helsinge",9900,56.0225,12.1980,"Hovedstaden","Sjælland","Helsinge",
 "En by i Nordsjælland, ikke langt fra Gribskov, en af Danmarks største skove, og de lange badestrande ved Kattegat.",
 "En by i Nordsjælland, ikke langt fra en af Danmarks største skove og de lange badestrande ved Kattegat."),
("struer","Struer",9800,56.4919,8.5937,"Midtjylland","Jylland","Struer",
 "En by ved Limfjorden i Vestjylland. Her ligger Bang & Olufsen, som laver flotte fjernsyn og højttalere.",
 "En by ved Limfjorden i Vestjylland. Her ligger en kendt fabrik, som laver flotte fjernsyn og højttalere."),
("stoevring","Støvring",9800,56.8853,9.8370,"Nordjylland","Jylland","Støvring",
 "En by syd for Aalborg. Tæt på ligger Rold Skov og Rebild Bakker, hvor der hvert år den 4. juli holdes en stor amerikansk fest.",
 "En by syd for Aalborg. Tæt på ligger en stor skov og nogle bakker, hvor der hvert år den 4. juli holdes en amerikansk fest."),
("ringkoebing","Ringkøbing",9800,56.0900,8.2440,"Midtjylland","Jylland","Ringkøbing",
 "En gammel købstad ved Ringkøbing Fjord, tæt på Vesterhavet. På fjorden kan man sejle og surfe.",
 "En gammel købstad ved en stor fjord tæt på Vesterhavet. På fjorden kan man sejle og surfe."),
("humlebaek","Humlebæk",9800,55.9620,12.5340,"Hovedstaden","Sjælland","Humlebæk",
 "En by ved Øresund mellem København og Helsingør. Her ligger kunstmuseet Louisiana med skulpturer i en have ned til vandet.",
 "En by ved Øresund. Her ligger et kendt kunstmuseum med skulpturer i en have helt ned til vandet."),
("grindsted","Grindsted",9800,55.7570,9.1050,"Syddanmark","Jylland","Grindsted",
 "En by i Sydvestjylland, kun ti kilometer fra Billund, hvor Legoland og lufthavnen ligger.",
 "En by i Sydvestjylland, kun ti kilometer fra byen hvor Legoland og en stor lufthavn ligger."),
("beder-malling","Beder-Malling",9500,56.0500,10.2000,"Midtjylland","Jylland","Malling, Denmark",
 "To landsbyer syd for Aarhus, som er vokset sammen til én by. Tæt på ligger Moesgaard Museum og skoven ned til Aarhus Bugt.",
 "To landsbyer syd for Aarhus, som er vokset sammen til én by. Tæt på ligger et stort museum om oldtiden og vikingerne."),
("galten-skovby","Galten-Skovby",9400,56.1560,9.9100,"Midtjylland","Jylland","Galten, Denmark",
 "To byer vest for Aarhus, som er vokset sammen. De ligger på vejen mellem Aarhus og Silkeborg.",
 "To byer vest for Aarhus, som er vokset sammen til én. De ligger på vejen mellem Aarhus og Silkeborg."),
("saeby","Sæby",9000,57.3340,10.5160,"Nordjylland","Jylland","Sæby",
 "En hyggelig havneby ved Kattegat syd for Frederikshavn. Tæt på ligger Voergaard Slot med voldgrav.",
 "En hyggelig havneby ved Kattegat syd for Frederikshavn. Tæt på ligger et gammelt slot med voldgrav."),
("fredensborg","Fredensborg",8900,55.9750,12.4040,"Hovedstaden","Sjælland","Fredensborg",
 "Her ligger Fredensborg Slot ved Esrum Sø. Kongefamilien bor her om foråret og efteråret.",
 "Her ligger et kongeslot ved en stor sø i Nordsjælland. Kongefamilien bor her om foråret og efteråret."),
("nykoebing-m","Nykøbing Mors",8900,56.7950,8.8600,"Nordjylland","Mors","Nykøbing Mors",
 "Hovedbyen på øen Mors midt i Limfjorden. På øen findes moler, en slags ler, hvor man kan finde fossiler af fisk og insekter.",
 "Hovedbyen på en ø midt i Limfjorden. På øen findes en slags ler, hvor man kan finde fossiler af fisk og insekter."),
("nivaa","Nivå",8800,55.9330,12.5050,"Hovedstaden","Sjælland","Nivå",
 "En by ved Nivå Bugt ved Øresund i Nordsjælland. Her lå engang et stort teglværk, hvor man brændte mursten, og den gamle ringovn står der endnu.",
 "En by ved en bugt ved Øresund i Nordsjælland. Her lå engang et stort teglværk, hvor man brændte mursten."),
("aars","Aars",8700,56.8030,9.5180,"Nordjylland","Jylland","Aars",
 "En by i Himmerland i Nordjylland. Ved museet står Aars-stenen, en runesten fra vikingetiden.",
 "En by i Himmerland i Nordjylland. Ved museet står en runesten fra vikingetiden."),
("hinnerup","Hinnerup",8600,56.2660,10.0640,"Midtjylland","Jylland","Hinnerup",
 "En by nordvest for Aarhus, som er vokset meget, fordi mange gerne vil bo tæt på både storbyen og naturen.",
 "En by nordvest for Aarhus, som er vokset meget, fordi mange gerne vil bo tæt på både storbyen og naturen."),
("loegten-skoedstrup","Løgten-Skødstrup",8600,56.2700,10.3000,"Midtjylland","Jylland","Løgten",
 "To landsbyer nordøst for Aarhus ved Aarhus Bugt, som er vokset sammen til én by.",
 "To landsbyer nordøst for Aarhus ved bugten, som er vokset sammen til én by."),
("hundested","Hundested",8600,55.9650,11.8530,"Hovedstaden","Sjælland","Hundested",
 "En havneby yderst på Halsnæs, hvor færgen sejler over Isefjorden. Polarforskeren Knud Rasmussen boede her, og hans hus er i dag museum.",
 "En havneby i Nordsjælland, hvor en færge sejler over Isefjorden. En berømt polarforsker boede her, og hans hus er i dag museum."),
("hoerning","Hørning",8600,56.0870,10.0370,"Midtjylland","Jylland","Hørning",
 "En by mellem Aarhus og Skanderborg, hvor både motorvejen og jernbanen kører forbi.",
 "En by mellem Aarhus og Skanderborg, hvor både motorvejen og jernbanen kører forbi."),
("hadsten","Hadsten",8600,56.3280,10.0490,"Midtjylland","Jylland","Hadsten",
 "En by ved Lilleåen nord for Aarhus, på jernbanen mellem Aarhus og Randers.",
 "En by ved en lille å nord for Aarhus, på jernbanen mellem Aarhus og Randers."),
("soroe","Sorø",8400,55.4320,11.5560,"Sjælland","Sjælland","Sorø",
 "En by ved Sorø Sø med den gamle skole Sorø Akademi. I klosterkirken ligger Absalon begravet – ham der grundlagde København.",
 "En by ved en sø midt på Sjælland med en gammel kostskole. I klosterkirken ligger Absalon begravet – ham der grundlagde København."),
("ribe","Ribe",8400,55.3280,8.7610,"Syddanmark","Jylland","Ribe",
 "Danmarks ældste by, fra vikingetiden. Her ligger Ribe Domkirke, og om aftenen går en vægter rundt i gaderne og synger.",
 "Danmarks ældste by, fra vikingetiden. Den har en stor domkirke, og om aftenen går en vægter rundt i gaderne og synger."),
("svenstrup","Svenstrup",8000,56.9740,9.8500,"Nordjylland","Jylland","Svenstrup, Aalborg Municipality",
 "En by lige syd for Aalborg, på jernbanen mod Hobro og Aarhus.",
 "En by lige syd for Aalborg, på jernbanen mod Hobro og Aarhus."),
("skjern","Skjern",7800,55.9500,8.5000,"Midtjylland","Jylland","Skjern, Denmark",
 "En by ved Skjern Å, den å i Danmark med mest vand. Ådalen er lavet om til vild natur igen, med mange fugle.",
 "En by ved den å i Danmark, der har mest vand. Ådalen er lavet om til vild natur igen, med mange fugle."),
]

# id, name, nearTown, place, lat, lon, description, wiki(en)
S = [
("tivoli","Tivoli","koebenhavn","København",55.6736,12.5681,"En gammel forlystelsespark midt i hovedstaden med rutsjebaner, blomster og lys om aftenen. Den åbnede i 1843.","Tivoli Gardens"),
("havfruen","Den Lille Havfrue","koebenhavn","København",55.6929,12.5993,"En lille bronzestatue af en havfrue, der sidder på en sten i vandet. Den er lavet efter H.C. Andersens eventyr.","The Little Mermaid (statue)"),
("nyhavn","Nyhavn","koebenhavn","København",55.6798,12.5910,"En gammel havn med farverige huse, gamle skibe og mange caféer.","Nyhavn"),
("amalienborg","Amalienborg","koebenhavn","København",55.6841,12.5934,"Fire palæer omkring en stor plads, hvor kongefamilien bor. Man kan se vagtskiftet.","Amalienborg"),
("rundetaarn","Rundetårn","koebenhavn","København",55.6813,12.5758,"Et tårn fra 1600-tallet, hvor man går op i en skråtstillet snegang i stedet for trapper.","Round Tower, Copenhagen"),
("kronborg","Kronborg Slot","helsingoer","Helsingør",56.0390,12.6212,"Renæssanceslottet, hvor Shakespeares Hamlet foregår. Det er på UNESCOs verdensarvsliste.","Kronborg"),
("frederiksborg","Frederiksborg Slot","hilleroed","Hillerød",55.9358,12.3009,"Et kæmpe slot på tre øer i Slotssøen. I dag er det Det Nationalhistoriske Museum.","Frederiksborg Palace"),
("roskilde-domkirke","Roskilde Domkirke","roskilde","Roskilde",55.6430,12.0817,"En stor teglstenskirke, hvor næsten alle danske konger og dronninger er begravet. Den er på UNESCOs verdensarvsliste.","Roskilde Cathedral"),
("vikingeskibe","Vikingeskibsmuseet","roskilde","Roskilde",55.6522,12.0794,"Et museum med rigtige vikingeskibe, der blev sænket i fjorden for omkring 1.000 år siden.","Viking Ship Museum, Roskilde"),
("legoland","Legoland","grindsted","Billund",55.7352,9.1270,"En forlystelsespark bygget af millioner af legoklodser. Den ligger i Billund, hvor Lego er opfundet.","Legoland Billund Resort"),
("moesgaard","Moesgaard Museum","aarhus","Aarhus",56.0834,10.2327,"Et arkæologisk museum med en skrå græsklædt tagflade, hvor du kan se Grauballemanden, en over 2.000 år gammel mand fra en mose.","Moesgaard Museum"),
("aros","ARoS Kunstmuseum","aarhus","Aarhus",56.1531,10.2003,"Et stort kunstmuseum med en regnbue på taget, som du kan gå rundt i.","ARoS Aarhus Kunstmuseum"),
("gamle-by","Den Gamle By","aarhus","Aarhus",56.1585,10.2118,"En hel by med gamle huse, hvor man kan opleve, hvordan danskerne boede og levede for mange år siden.","Den Gamle By"),
("hc-andersen","H.C. Andersens Hus","odense","Odense",55.3961,10.3877,"Museum om eventyrdigteren H.C. Andersen i huset, hvor han blev født og voksede op.","Hans Christian Andersen Museum"),
("odense-zoo","Odense Zoo","odense","Odense",55.3847,10.4273,"En af Danmarks bedste zoologiske haver med blandt andet løver, elefanter og pingviner.","Odense Zoo"),
("jelling","Jellingstenene","vejle","Jelling",55.7561,9.4194,"To store runesten fra vikingetiden. Den ene kaldes Danmarks fødselsattest, fordi der første gang står 'Danmark' på den. På UNESCOs verdensarvsliste.","Jelling stones"),
("ribe-domkirke","Ribe Domkirke","ribe","Ribe",55.3279,8.7615,"En stor romansk kirke i Danmarks ældste by, Ribe. Man kan gå op i tårnet og se over marsken.","Ribe Cathedral"),
("mennesket","Mennesket ved Havet","esbjerg","Esbjerg",55.4660,8.4180,"Fire kæmpestore hvide mænd, der sidder ved vandet og kigger ud over Vesterhavet.","Men at Sea"),
("grenen","Grenen","frederikshavn","Skagen",57.7449,10.6320,"Danmarks nordligste spids, hvor Skagerrak og Kattegat mødes. Man kan stå med en fod i hvert hav.","Grenen"),
("raabjerg-mile","Råbjerg Mile","frederikshavn","Skagen",57.6580,10.4850,"En kæmpe sanddyne, der langsomt vandrer hen over landskabet.","Råbjerg Mile"),
("moens-klint","Møns Klint","vordingborg","Møn",54.9680,12.5440,"Høje, hvide kridtklinter, der rejser sig op fra Østersøen. Der kan findes fossiler på stranden.","Møns Klint"),
("egeskov","Egeskov Slot","svendborg","Kværndrup",55.1750,10.4784,"Et vandslot fra 1500-tallet omgivet af voldgrav, med have, labyrint og en samling af veteranbiler og fly.","Egeskov Castle"),
("soenderborg-slot","Sønderborg Slot","soenderborg","Sønderborg",54.9114,9.7855,"Et slot ved Als Sund. I dag er der museum om de store slag i Sønderjylland.","Sønderborg Castle"),
("dybboel","Dybbøl Banke","soenderborg","Sønderborg",54.9140,9.7400,"Her stod et stort slag i 1864 mellem Danmark og Preussen. Du kan se den gamle mølle og skanserne.","Battle of Dybbøl"),
("rubjerg","Rubjerg Knude Fyr","hjoerring","Lønstrup",57.4430,9.7739,"Et fyr på en høj klint ved Vesterhavet, som i 2019 blev flyttet 70 meter, fordi en sanddyne var ved at begrave det.","Rubjerg Knude Lighthouse"),
("himmelbjerget","Himmelbjerget","silkeborg","Ry",56.1000,9.6833,"Et højt punkt (147 meter) med udsigt over søerne og skovene rundt om Silkeborg. Der står et tårn på toppen.","Himmelbjerget"),
("museum-jorn","Museum Jorn","silkeborg","Silkeborg",56.1717,9.5493,"Et kunstmuseum med værker af den danske kunstner Asger Jorn.","Museum Jorn"),
("hammershus","Hammershus","roenne","Bornholm",55.2686,14.7570,"Nordeuropas største borgruin, oppe på en klippe ved havet i Nordbornholm.","Hammershus"),
("zoo-aalborg","Aalborg Zoo","aalborg","Aalborg",57.0415,9.8982,"En stor zoologisk have med mange dyr, blandt andet elefanter, løver og tigre.","Aalborg Zoo"),
("koldinghus","Koldinghus","kolding","Kolding",55.4939,9.4772,"Et kongeslot, der brændte i 1808. Ruinen blev bygget op igen, og i dag er der museum.","Koldinghus"),
("fjordenhus","Fjordenhus","vejle","Vejle",55.7088,9.5430,"En bygning af kunstneren Olafur Eliasson, der står helt ude i vandet i havnen.","Fjordenhus"),
("faengslet","Fængslet","horsens","Horsens",55.8634,9.8446,"Et gammelt statsfængsel, der i dag er museum og koncertsted.","Horsens State Prison"),
("trelleborg","Trelleborg","slagelse","Slagelse",55.3918,11.2637,"En rund vikingeborg fra omkring år 980 med volde og gamle langhuse, som er genskabt.","Trelleborg (Slagelse)"),
("nyborg-slot","Nyborg Slot","nyborg","Nyborg",55.3127,10.7873,"Et af Danmarks ældste kongeslotte, bygget i 1100-tallet. Her mødtes Danehoffet, som var en slags tidlig rigsdag.","Nyborg Castle"),
("valdemars-slot","Valdemars Slot","svendborg","Tåsinge",55.0150,10.6370,"Et slot fra 1600-tallet bygget af Christian 4. til hans søn Valdemar Christian.","Valdemars Castle"),
("vor-frue","Vor Frue Kirke","kalundborg","Kalundborg",55.6797,11.0855,"En middelalderkirke med fem tårne bygget i form af et kors.","Church of Our Lady, Kalundborg"),
("faxe-kalkbrud","Faxe Kalkbrud","haslev","Faxe",55.2570,12.1300,"Et kæmpestort kalkbrud, hvor man kan finde fossiler af koraller og søpindsvin.","Faxe Quarry"),
("spoettrup","Spøttrup Borg","skive","Skive",56.6334,8.6500,"Den bedst bevarede middelalderborg i Danmark med voldgrav, ridderhal og museum.","Spøttrup Castle"),
("fyrkat","Fyrkat","hobro","Hobro",56.6321,9.8074,"En rund vikingeborg fra omkring år 980, ligesom Trelleborg. Man kan se et genskabt langhus.","Fyrkat"),
("kattegatcentret","Kattegatcentret","grenaa","Grenaa",56.4130,10.8860,"Et stort akvarium med hajer, sæler og fisk fra de danske farvande.","Kattegatcentret"),
("gaasetaarnet","Gåsetårnet","vordingborg","Vordingborg",55.0085,11.9087,"Et tårn fra 1300-tallet med en guldgås på toppen, bygget af kong Valdemar Atterdag.","Goose Tower"),
("lillebaelt","Lillebæltsbroerne","middelfart","Middelfart",55.5150,9.7015,"To store broer, en gammel fra 1935 og en ny fra 1970, der forbinder Fyn og Jylland.","Little Belt Bridge"),
("regnskov","Randers Regnskov","randers","Randers",56.4578,10.0398,"En tropisk regnskov under tag med aber, krokodiller, slanger og frøer.","Randers Regnskov"),
("louisiana","Louisiana","humlebaek","Humlebæk",55.9690,12.5430,"Et kunstmuseum i en stor have ned til Øresund, med skulpturer man kan gå rundt imellem og et børnehus, hvor man selv kan lave kunst.","Louisiana Museum of Modern Art"),
("fredensborg-slot","Fredensborg Slot","fredensborg","Fredensborg",55.9770,12.4030,"Et hvidt kongeslot ved Esrum Sø, hvor kongefamilien bor om foråret og efteråret. Slotshaven er åben for alle.","Fredensborg Palace"),
("nationalpark-thy","Nationalpark Thy","thisted","Thy",57.0000,8.4000,"Danmarks første nationalpark med klitter, hede og vilde dyr. Her kan man også surfe ved Cold Hawaii.","Thy National Park"),
]

def die(m): print("ERROR:", m); sys.exit(1)

ids = [t[0] for t in T]
if len(T) != TOWN_COUNT or len(set(ids)) != TOWN_COUNT: die(f"expected {TOWN_COUNT} unique towns, got {len(T)}")
for t in T:
    # "Nykøbing Falster" -> nykøbing; "Beder-Malling" -> beder, malling
    for part in t[1].split()[0].split("-"):
        if part.lower() in t[9].lower(): die(f"clue leaks name: {t[0]}: {t[9]}")
    if t[6] not in AREAS: die(f"unknown area {t[6]} for {t[0]}")
    if not (54.5 < t[3] < 57.8 and 8.0 < t[4] < 15.2): die(f"out of bounds {t[0]}")

# Sort by population (ties keep list order), rank them.
order = sorted(range(len(T)), key=lambda i: (-T[i][2], i))
towns = []
for rank, i in enumerate(order, 1):
    t = T[i]
    towns.append(dict(id=t[0], rank=rank, name=t[1], population=t[2], lat=t[3], lon=t[4],
                      region=t[5], area=t[6], wiki=t[7], description=t[8], clue=t[9]))
sights = []
for s in S:
    if s[2] and s[2] not in ids: die(f"sight {s[0]} bad town {s[2]}")
    sights.append(dict(id=s[0], name=s[1], nearTownId=s[2] or None, place=s[3], lat=s[4], lon=s[5], description=s[6], wiki=s[7]))

(OUT/"towns.json").write_text(json.dumps(towns, ensure_ascii=False, indent=1), encoding="utf-8")
(OUT/"sights.json").write_text(json.dumps(sights, ensure_ascii=False, indent=1), encoding="utf-8")

# ---- map outline ----
if NE is None:
    print("towns", len(towns), "sights", len(sights), "(map not rebuilt)")
    print("top10:", [t["name"] for t in towns[:10]])
    print("50-51:", [t["name"] for t in towns[49:51]], "last:", towns[-1]["name"])
    sys.exit(0)
LON0, LAT0 = 7.9, 57.85           # top-left
LON1, LAT1 = 15.3, 54.5           # bottom-right
K = 300.0                          # px per degree of latitude
KX = K * math.cos(math.radians(56.0))
W, H = (LON1-LON0)*KX, (LAT0-LAT1)*K
d = json.load(open(NE))
geom = next(f for f in d["features"] if f["properties"]["ADM0_A3"] == "DNK")["geometry"]
polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
parts = []
for poly in polys:
    for ring in poly:
        pts = [((lo-LON0)*KX, (LAT0-la)*K) for lo, la in ring]
        # drop tiny islets (< ~4 px extent) to keep it clean
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        if max(xs)-min(xs) < 3 and max(ys)-min(ys) < 3: continue
        parts.append("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z")
shape = dict(width=round(W,1), height=round(H,1), lon0=LON0, lat0=LAT0, kx=round(KX,4), ky=K, path="".join(parts))
(OUT/"denmark.json").write_text(json.dumps(shape), encoding="utf-8")
print("towns", len(towns), "sights", len(sights), "map", shape["width"], shape["height"], len(shape["path"]), "bytes")
print("top10:", [t["name"] for t in towns[:10]])
print("top25 last:", [t["name"] for t in towns[:25]][-5:])
