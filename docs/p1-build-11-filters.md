# Build item 11 — the generator's filters (data for `naming.yaml#blacklist`)

*Written by the development tab, 2026-10-04. Two new lists. A generated candidate that equals an entry (case-insensitive, whole name) is dropped inside the generator and the next one is drawn; nothing here reaches the door. The owner sees the lists' sizes and the count each bag loses, not the lists. Both lists grow at the audit: the development tab reads the per-bag samples the build reports and adds what slipped through.*

## `blacklist.real_given` — real given names and plain words a person bag can spell

Applies to every person and god bag except a bag with `real_ok: true` (the rustic bag; owner: a real English name suits a villager).

```text
aaron abel adam adrian agnes aidan alan albert alex alfred alice alina alma amanda amber amos amy andor andre andrea
andrew angus anna anton antti arne arnold arthur arvid astrid aud audun
barbara bart bartley basil bella ben bernard bertha bjorn bogdan boris brad bram branda brandon branko brenda brendan
brian brigid bruno bryn
cadell caitlin calvin cara carl carla carmen carol cathal cecil celia cian ciaran clara claudia conan connor conrad cormac
dag dagmar dalia damon dan dana daniel darko david dawn dean declan delia della dermot diana dirk dmitri dolan donald
donnan doris dorian douglas dragan dusan dylan
eamon edgar edith edmund edna edwin egil einar elena elin elina elise ella ellen elmer elsa elvin emil emilia emlyn emma
eneko eogan eoghan eric erik erin erlend ernest esther ethan eugene eva evan evelyn evert
fabian felix fergus fiona flannan flora florin frank frans freya frida
gabriel gareth garrett gavin gawain geir george gerald gilbert glenn glyn goran gordon gorka grace graham greta gudrun
gunnar gustav gwen gwilym gwyn
hakon haldor halvard hank hannah hans harald harold harriet harvey hector hedda heikki helen helena helga hendrik henrik
henry herbert herman hilda holger hugo
ian ida igor ilmari ilona imre ines inga ingmar ingrid ingvar irene iris irma isaac isabel isak ivan ivar
jacob jalmari jan jana janet jarl jason jasper joel johan john jonas joost jorge joseph judith jukka julia julian julius
kaarlo kalina kalle kara karen karin karl kasimir katarina kate kathleen keith kelvin kenneth ketil kevin kieran kim kira
klaus koen kurt
lara lars lassi laura lauri lea leif lena leo leon leona leonard leonidas lilian linda linus lionel lisa livia lola
lorcan lorna louis lucas lucia lucius ludmila luis luka luther lydia
madeline magnus malcolm marc marcel marcus maria marian marin marina marius mark marko marta martin mary matilda matti
maurice max maya megan melina melvin mervyn micah mikael mikko mila milan milena miles milo mira miriam miroslav mona
morgan moses murdoch myra
nadia nancy naomi natalia nathan neil nell nestor niall nico nigel nikias nikita nikola nils nina noel nolan nora norman
octavia odette olaf olav oleg olga olin oliver olivia omar orla oscar oskar osmund oswald otto owen
paavo pablo patrick paul paula pavel pedro pekka percy peter petra philip philon pieter
quentin quinn
radko rafael ragnar ralph ramon randal raul raymond rebecca regina reidar rene rhoda rhys richard rita robert robin
roderick roger roland rolf roman rona ronald rory rosa rosalind ross rowena roy ruben rufus rune rupert ruth ryan
sabina sabin sally salma samuel sandra sara sarah saul sean selma senan seppo serena sergei seth sigrid sigurd silvia
simon sirin sonia sonja sophia stanislav stefan stella sten steven stig susan svanhild sven svetlana sylvia
tamara tania tapio tara tegan teodor teresa thea thelma theo thomas tilda timon timothy tobias tomas tone tore torvald
trevor tristan tuukka tyra
ulf ulla ulrik una unai ursula
vadim valentin valeria valter vanessa vasil vera verner veronica victor vidar viktor vilma vincent viola violet virgil
vivian vlad vladimir
walter wanda warren wayne wendy werner wilbur wilfred willem william wilma winston
xabier xenia xenophon
yara yuri yvonne
zdenka zelda zenon zlatan zoran
```

Plain English words and other things a bag has spelled or can spell (seen in the trials or one join away):

```text
heathen lonely lone nasa elsa vesa heaven demon demos lemon melon salon satan titan vegan pagan human woman
hallmark hallway landmark denmark marker market mental rental dental sandal vandal scandal mortal mortar portal
normal formal thermal carnal banal anal moron boring boron baron bacon beacon bison raven arson parson person
mason masonry harlot varlet merlin martin kremlin goblin gremlin vermin sermon salmon solemn column garlic
garland dorsal morsel tinsel tassel vessel vassal rascal pascal lykia prydain lydia media mania malaria hernia
mentor tumor rumor humor tenor minor manor major donor honor error terror horror mirror
kokulu kelime makine makina tekila kuleli pulluk kaleli hamile halime hakime nalini kolonya malina kamila
```

## `blacklist.real_places` — famous real places a compound can spell

Applies to every pooled place, region, inn and site name (public and secret stocks). Only the famous ones: an obscure real village (Oakham, Thornbury, Ashford) passes, by the owner's ruling.

```text
oxford cambridge newport newcastle newhaven newmarket newton newbury blackpool blackburn bradford bedford stratford
stafford hereford hertford guildford chelmsford watford dartford ashford redford milford medford
bristol brighton boston london lincoln lancaster leicester manchester winchester chester rochester dorchester
colchester gloucester worcester exeter dover durham derby kingston kingsbridge kensington kent
plymouth portsmouth bournemouth weymouth falmouth yarmouth dartmouth monmouth
liverpool blackwater blackwood hollywood holywood greenwood sherwood redwood westwood eastwood
greenland iceland ireland england scotland holland finland poland portland cleveland maryland oakland
westminster southampton northampton wolverhampton hampton hampstead halstead
edinburgh pittsburgh hamburg salzburg strasbourg
whitehall whitechapel whitby whitehaven redhill redbridge redcliff sandhurst
stonehenge stonehaven glastonbury canterbury salisbury shrewsbury tewkesbury banbury sudbury
windsor woodstock wimbledon waterloo wakefield sheffield springfield greenfield mansfield lichfield smallville
northfield southfield westfield eastfield highgate highbury highland lowland midland
longford longbridge longmont deepwater coldwater clearwater stillwater sweetwater bridgewater
riverside lakeside seaside sunnyside brookside
silverstone silverton goldstone goldfield ironbridge ironside coalville
rockford rockport rockville rockwell stockholm stockton stockport
winterfell riverrun highgarden casterly dragonstone sunspear
ravenholm ravenhurst rivendell gondor rohan mordor waterdeep neverwinter baldur silverymoon daggerford greenest
phandalin saltmarsh barovia
```

(The fictional entries at the end are also in `blacklist.exact` or its neighbours today; listing them here costs nothing and keeps the compound generator from spelling them.)

## What the build reports for the audit

For each of the seventeen bags, a file of 200 generated names (fixed seed) under the scratch output of the summary, plus the count the two lists dropped per bag over 2,000 draws; for the place generator, 200 compounds from a fixed seed and the count dropped. The development tab reads the samples (the owner does not need to) and extends the lists before the commit.

## Added at the audit of build 11a (2026-10-04)

The development tab read the 3,069 sample names the build drew (seventeen bags, up to 200 each). What slipped through, to add to the lists:

Real given names, mythic names and names from known books (to `real_given`):

```text
ishan
europe philia aristides androkles iphis pelope kallippos alkimos lykias xanthia aristeus hermokles menia olympas
tullia fulvius antenor laurene silene rufius
milosh radana tikhomir vseslav bratoslav mileta zdanko vitko zorko dragomil gostomir lubimir lyudomir zlatimir milik
torsten
reija raimo ilmatar heikko heili
arwen vesna
moran cynan cariad merion aeryn
morana
halvor gunhild hallveig yngvar svanborg svandis gudbjorn gudlaug asgard ingleif egfrid arngerd hildrun gunstein hrothmund jorstein dagolf gunleif
donnell ailin
irune sarria goiko araneta
tamaki
```

Plain words (see the split below):

```text
koran naval males marne fulan penys pellet pardun
```

**The split.** `real_given` holds two different things: real names, which the rustic bag may spell (owner: a real English name suits a villager), and plain words, which no bag should spell (the rustic sample holds "Pellet"). The plain-words block of this file, with the words above, becomes its own list `blacklist.plain_words`, applied to every bag, `real_ok` or not; `real_given` keeps the names and stays off for a `real_ok` bag.

