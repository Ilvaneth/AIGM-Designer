# Build item 11 — the seventeen part bags (data for `naming.yaml#family`)

*Approved by the owner bag by bag on 2026-10-04, each on thirty names the trial generator drew. `s` = openings, `m` = middles (`pm` = the chance a middle is used), `e` = endings, `vj` = a consonant-final part takes only a vowel-initial next part, `real_ok` = the real-name filter is off for this bag. The trial generator that measured them follows the bags.*

```python
# the 17 part bags as the owner approved them (trial data; the build writes them into naming.yaml)
BAGS={
"hard_upland":dict(group="A",s="Teg Var Bro Dras Kor Gund Brak Durn Kelv Tor Hark Vosk Grim Dolg Ruk Skar Tarn Bold Krag Varg Dreg Gorm Hest Morg Uld Bren Dak Garn Hod Jark Kest Lund Murg Nark Ord Rag Trak Vend Bard Dorn Fenk Gred Hald Yarg Zend Brod Tusk Dunk Belg Pard",
 e="rik dek gar kun vask dan rum gard bek tor ven ran dur mar sten rak lod nar brand dok gan kar mund nok rad rek ruk tan tar vad vor zak drun gren hok lak dun bor kan gost"),
"northern":dict(group="A",s="Hrol Skar Ulv Sten Sval Hild Arn Eir Frod Gun Hak Ing Jor Ket Orm Sig Ulf Yng Asg Bryn Dag Eg Grim Hall Hjal Kol Rolf Snor Styr Svein Vig Halv Hauk Isk Stig Aud Geir Gud Herj Skold Varn Thrand Svan Hroth Skef Ljot Rund Vest Alf Hrim",
 e="ulf ard vald mund hild grim leif stein vik dis run gerd var bjorn finn ald olf rid veig laug ne ar ir ur ke da la vor heid thra borg frid gunn trud lak kel fast und"),
"guttural":dict(group="A",s="Ghor Uzh Krug Zhur Mogh Ukr Grak Dhur Bozh Ghaz Khar Mazh Nagh Orgh Rukh Shag Thrag Urz Vugh Yagh Zogh Agh Brug Dugh Ghul Gruz Khor Mugh Nuzh Olg Ragh Snag Thok Ugr Vorg Zhag Azh Bugh Durz Gash Hurz Krazh Murz Narg Okh Rogh Skug Uzg Zug Drok",
 e="rak mog gam rog ra rash ak uk og ash mak dush gul nak zag bag lug gor dak rum zum thak kra sha mur gash bur nok rakh zog gath mush dug kul zar mok grum bash hak urk"),
"eastern":dict(group="A",s="Vlad Drag Mir Bor Rad Stan Yar Zor Mil Dob Gor Lub Vel Brat Kaz Lesh Nev Ost Pred Rost Slav Svet Vse Zlat Bog Chest Dal Dush Kres Lyud Sob Tver Vit Voy Zhel Bran Cher Dom Gost Mal Nar Rud Sem Vuk Zdan Bel Yel Prav Tikh",
 e="mir slav ko an ek osh imir omil ana ka ena isa ava ik in un ash ota eta il ilo oy uta ovan ost ich enko ila ina ora ush yan omir oslav gost bor vit rad mil dan"),
"liquid_coast":dict(group="B",s="Sar Il Yes Vel Or Tol Am Mer Lis Nav El Ol Sen Mar Rien Ves Thal Ful Ire Ose Un Cal Dev Arv Bel Len Mal Nel Ral Sol Tir Val Alm Erl Ilv Orl Ren Vir Lar Nar Ser Tal Ulm Vas Yel Ar Sel Mur Lor",
 e="ven me ra une mis van mar eli lin wen ne dra ro les ri nia sel mir the na ris lan len mel nar ren rin sen val var vel lar lis lun nel ral ron rel sar mon"),
"nasal_round":dict(group="B",s="Um Dom Wun Bun Bem Nem Bow Mon On Nom Mun Bon Lom Hum Num Om Un Bol Mol Nol Dun Lum Rum Nab Wam Won Lun Mau Nau Bor Mor Nor Wor Wen Men Ben Ban Nan Man Dum",m="a o u e",pm=0.6,
 e="ben ra an du nam or wan do mo no bu ma na bo wo mun bun wun dun lun man ban nan wen men dom nom lom rum num mur nur bur da ba la ro lo"),
"airy":dict(group="B",s="Hath Ish Thew Whel Eir Shean Hal Thal Heth Ath Eth Ith Hael Whin Shal Thir Hesh Hean Whar Hir Sheth Thel Hew Ael Eath Whis Shir Thun Hav Hesp Phal Pheth Fael Hiar Wheth Whal Hoth Thav Shav Hain Thain Whain Shain Heil Theil Sheil Shor Heath Thaw Ehl",
 e="en ara wa an ath nor eth ir al ean ein eir ith ar el is as ael wen win wan hal hel thal thel ren rin ran lan len lin nan nen sha tha rha wha or il in"),
"open_isle":dict(group="B",s="Ka La Ma Na Ha Ke Le Me Ne He Ki Li Mi Ni Hi Ko Lo Mo No Ho Ku Lu Mu Nu Hu Pa Pe Pi Po Pu Wa We Wi Ta Te Ti To Tu Ala Iko Ula Ema Ono Aka Ile Umi Oha Eki",
 m="la na ka ma ha li ni ki mi lo no ko mo lu nu ku",pm=1.0,
 e="lani koa ni la na ka ma ha lo no ko mo lu nu ku mu hi li ki mi nui lea kea loa noa mea kai lei nai hau lau mau pua hua lua kua"),
"sung":dict(group="C",s="Il Sae Tha Lor Ae Ith Nim Ser Val Myr An Or Er Lath Tir Gal Hal Is Ny Ul Vae Rin Sil Eth Mel Ael Cal Fin Lae Nae Rae Tae Ves Yl El Ol Ir Aer Ien Lin Mir Thir Sael Fael Lyth Nith Ryl Syl Thal Var",
 m="a i ra la thi ri sa ne ve lo ma di na li re the",pm=0.7,
 e="el van nith the ras lis reth mir nel thir dil ros lian ael ath eth ion ien ys yth ran rel sar sel thel thas vel ven lar las len lor mar nar nys rien ris"),
"courtly":dict(group="C",s="Aur Val Lies Ott Sab Sol Ser Marc Vit Flor Clar Dom Fab Gal Hort Laur Oct Pell Quint Rem Sev Tib Urs Ven Aem Bell Dec Fulv Gratt Hil Liv Man Nerv Ors Pont Ruf Sil Tert Varr Drus Mer Tull Vesp Ant Cal Per Luc",
 e="elan orin ander avien ellin enne oran idan estin ovar essan antin ellar ioran amond esco ando etto ivar alis oris anis enor adin asto irand ellon uvian arese ian ius ia ina ora ane ard ona ene ilo"),
"antique":dict(group="C",s="Phaed Lyk Dem Arist Kall Nik Xen Pher Hipp Eur Agath Alk Andr Chrys Epin Glauk Iph Leont Men Myr Nest Olymp Pel Phil Sophr Tel Thras Zen Akr Bas Dor Eud Gorg Hek Kor Mel Pan Pyrr Sthen Tim Xanth Eum Ast Kleom Polyd Herm Amph Eup Lamp Prax",
 e="os eon andra ides ippos okles on as ias eus ylos anor arete ione ope yra esta athe emon enes imos odoros ophon ais ene ia is ys aon archos edon ikos agoras andros"),
"rustic":dict(group="D",real_ok=True,s="Tam Dun Mab Hob Wat Bram Peg Net Odd Gam Hal Jop Kit Lam Ned Pim Ros Syb Tib Wen Had Col Bart Dob Fenn Alf Bess Cob Dag Ebb Gil Hew Jem Kem Lob Mag Nan Ott Pell Sam Tod Ull Wig Yan Ab Bax Cad Dill Hod Rudd",
 e="sin stan bot kin ley wick by lin mund ric win ard ett ling den sey mer low cot son kins ock et en er ert old ward ick itt ot"),
"misty_vale":dict(group="D",s="Gwen Gwyl Rhod Bryn Cad Em Gar Glyn Hyw Iol Llew Mad Mor Ner Pryd Rhi Tal Tud Aer Bed Car Cer Cyn Del Dyf Elid Gwal Gwer Heil Id Ith Llyr Mael Med Mer Nyf Pen Rhun Seis Tang Trah Ys Arth Bleid Dew Gruff Mab Rhydd Tegw Ang",
 e="wyn wen an edd ydd og ys yr ian ion eth ach in on ael awg fan fyl goch ig lyn mor nwy od or ri ros wal wy yn eg en iad ain aeth ell ern arn"),
"old_isle":dict(group="D",vj=True,s="Aed Con Fer Dair Eog Fiach Mur Ruad Tad Cath Diar Eim Fael Lorc Mid Muir Niam Orl Sorch Tuath Ail Bres Ech Fedl Lon Nem Scath Teth Uath Art Bec Cel Cuan Derm Donn Flann Garb Ler Cair Dall Eber Glas Ibar Ness Rath Brid Corm Sen Tig Uis",
 e="an agh ell ach in ald id ech en ar oc og eth ic il ain aid uin ol al ed ir os anach elan oran ilin uagh"),
"sibilant":dict(group="E",vj=True,s="Seth Ash Zis Syl Iss Thes Sath Zesh Sith Yth Ass Esh Sas Zeth Thass Shis Saph Zal Sel Ser Shel This Zir Syr Yss Sais Zais Sheth Soth Zoth Hass Vess Vash Nass Nesh Liss Tash Rass Resh Aths Eths Oss Uss Zash Thish Soss Yesh Zyth Shal Zar",
 e="is ael ith eth al an as ys ia ir or il ara ira era yra arin eris iral ulis oran aris enis yrith alis onis uan iar ethan ilar ovar"),
"lake_folk":dict(group="E",vj=True,s="Ai Il Kaar Tuuk Vai Lem Aht Jou Kul Lou Tap Ukk Vel Aat Eel Hei Iiv Juk Kaup Lau Mat Oll Paav Reij Sep Tuom Urh Vil Ant Ees Hann Ilm Jorm Kal Lass Mik Nii Osk Pek Rai Sak Tau Veik Sin Tel Kyl Suv Aam Hel Tor",
 e="nen kka ri ro no la li ja nna tti kko ppo sto mo vi ni ski lmi ras nu tar kki lla ana ina ukka ikki aro eri ilo amo onen inen anen ari ola ula eli uri ikko akka ukko onna etti appo aski elmi aras inu atar illa"),
"old_mountain":dict(group="E",vj=True,s="Etx Aitz Ur Arr Bel Gar Har Ib Ir Itz Laz Mend Och Otx Zub Zum Aran Bid Gor Jaur Kem Lor Mun Nab Oih Sor Txom Xab Zal Agirr Alts Ber Ech Elk Goik Ibarr Larr Mark Orm Sarr Urd Uzt Zeb Ard Ezk Olab Erren Izt Ond Uga",
 e="arri oitz egi eta aga uri alde ondo erri ain une ola ko txo tza zar berri gain buru iz az oz itz atz utz ene ane ia ar or ur"),
}
```

## The trial generator (the join and shape rules the measurement used)

```python
import sys, random, re, math
sys.path.insert(0, r"C:\Users\armag\Desktop\Campaign-Designer\.claude\skills\dnd\scripts")
import design_names as dn
from final_bags import BAGS
V = set("aeiouy")


def join(a, b, vj):
    if a[-1] == b[0]:
        b = b[1:]
    if not b or (a[-1] in V and b[0] in V):
        return None
    if vj and a[-1] not in V and b[0] not in V:
        return None
    return a + b


def make(rng, f):
    S = f["s"].split(); M = f.get("m", "").split(); E = f["e"].split(); vj = f.get("vj", False)
    w = rng.choice(S)
    if M and rng.random() < f.get("pm", 0):
        w = join(w, rng.choice(M), vj)
        if not w:
            return None
    w = join(w, rng.choice(E), vj)
    low = (w or "").lower()
    if not w or len(w) < 5 or re.search(r"[^aeiouy]{4}", low) or re.search(r"(..).?\1", low) or re.search(r"(...).*\1", low):
        return None
    return w


def run(f, seed, n):
    rng = random.Random(seed)
    caps = {"ending": max(2, math.ceil(n * 0.12)), "opening": max(2, math.ceil(n * 0.15))}
    out = []; t = 0
    while len(out) < n and t < 8000:
        t += 1
        w = make(rng, f)
        if w and dn.acceptable(w, {"forbidden_clusters": [], "onsets": []}, out, caps, "person"):
            out.append(w)
    return out


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    for k, f in BAGS.items():
        got = [len(run(f, sd, N)) for sd in range(20)]
        a = set(run(f, 1, N)); b = set(run(f, 2, N))
        print(f"{k:13} {f['group']} parts {len(f['s'].split())}+{len(f.get('m','').split())}+{len(f['e'].split())} | {N} names over 20 seeds: min {min(got)} | two births share {len(a&b)}")
    for k in sys.argv[2:]:
        print(k, ":", ", ".join(run(BAGS[k], 3, 60)[:15])); print("   ", ", ".join(run(BAGS[k], 4, 60)[:15]))
```
