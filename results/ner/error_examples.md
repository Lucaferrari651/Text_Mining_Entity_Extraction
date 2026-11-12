# Real examples for each cause of error

Taken from saved predictions with a fixed seed (13). The mention in `[[double brackets]]` is the gold (or predicted) one.

## 1. The `{@name@}` markup: the Wikipedia-trained model does not find it (RoBERTa-base, TweetNER7)

- gold **COMP**: `{@England Football@}`. Wow can the {@Nazionale Italiana ⭐️⭐️⭐️⭐️@} Italian Team win the World Cup and the Euros in succession ??? C'on Cannavaro !! [[{@England Football@}]] {@Germany@} {@French Team ⭐⭐@} {{USERNAME}} {@LaLiga English@} {@Premier League@} {@Bundesliga English@} {@🎮 Major League Soccer@} {{USERNAME}}
- gold **COMP**: `{@NBA@}`. I ’m pretty sure Jerry West would n’t have minded {@Kobe Bryant@} being the NEW LOGO even if just for a season [[{@NBA@}]]
- gold **COMP**: `{@NY Working Families Party@}`. VETS in NY - This November the [[{@NY Working Families Party@}]] is in the fight of our lives . We need hundreds of thousands of voters to vote for Joe Biden on our Working Families Party ballot line . Join this training session to learn about how to organize your friends and family ! {{URL}}
- gold **PROD**: `{@Etsy@}`. Stunning , " Vintage " " Kramer of New York " Two Brooches and matc by RetroMollyTreasures {{URL}} via [[{@Etsy@}]] Stop by {{URL}} for our Labor Day weekend sale 20 % off of the entire store ! !
- gold **PROD**: `{@Breitbart News@}`. Vile Joe Biden supporters . ‘ Racism Lives Here ‘ : Trump Supporters Targeted in Coronado with Rogue Yard Signs {{URL}} via [[{@Breitbart News@}]]

## 2. A name never seen in training (WNUT-17, RoBERTa-large trained on all three sets)

- gold **PROD**: `Google Search` (not in the WNUT-17 training set). andrew mccabe fuck flynn then we fuck trump - [[Google Search]] @ StefanMolyneux @ realDonaldTrump @ DonaldJTrumpJr https://t.co/XGOEPsF0KB :
- gold **PROD**: `Hasbro chocolate frog cards` (not in the WNUT-17 training set). [ The version found in the CoS game ] ( http://i.imgur.com/LhhRTyG.jpg ) ( which has been [ confirmed to be written by Jo ] ( http://web.archive.org/web/20100310145702/ http://www.jkrowling.com/textonly/en/faq_view.cfm?id=96 ) ) did n ' t mention the Order . The version packaged with [ the [[Hasbro chocolate frog cards]] ] ( https://i.imgur.com/FHvtOW0.jpg ) ( not confirmed to be from Jo ) did . This is correctly explained in [ the Lexicon ' s updated article ] ( https://www.hp-lexicon.org/2016/12/29/famous-wizard-cards/ ) .
- gold **PROD**: `Google` (not in the WNUT-17 training set). # SEO Tip : [[Google]] considers the first lines of the page important . Put menu , headers + important text on top . # google
- gold **PROD**: `DELL Inspiron 17 R 5721 Core i 5 - 3317 U 1 . 7 GHz 6 Gb 750 Gb DVDRW 17 . 3 " Laptop` (not in the WNUT-17 training set). [[DELL Inspiron 17 R 5721 Core i 5 - 3317 U 1 . 7 GHz 6 Gb 750 Gb DVDRW 17 . 3 " Laptop]] https://t.co/SvPm1Qm5dg https://t.co/eG2GWQ5Jv7
- gold **PROD**: `java . security . PublicKey object` (not in the WNUT-17 training set). the reason why I ask is because I want to be able to create a [[java . security . PublicKey object]] with the bytes and I do n ' t know how to do that .

## 3. Same words, other label: company or product? (TweetNER7, RoBERTa-large)

- gold **COMP**, predicted **PROD**: Listen to Breanna Rubio " Bad Side " on [[IHeartradio]] , The Heat 100.9 " Stay Ready Boyz " and 103.7 Dabeat Radio {{USERNAME}} also download it on iTunes and other retailers online . Follow {{USERNAME}} {{USERNAME}} … {{URL}}
- gold **COMP**, predicted **PROD**: Fuller House Series Finale {{URL}} via [[{@TVLine.com@}]]
- gold **COMP**, predicted **PROD**: The daily {{USERNAME}} online newspaper " the view from up here " is out ! {{URL}} Stories via {{USERNAME}} {{USERNAME}} [[{@CBC Music@}]] # nationalicecreammonth # studiobell
- gold **PROD**, predicted **COMP**: The fact that 90 % of my timeline is post about # NWAEmpowerrr brings me joy . The fact that 100 % of those posts are nothing but positive makes it even better . Great job [[{@NWA@}]] {@Mickie James~Aldis@} & everyone else involved
- gold **PROD**, predicted **COMP**: Ever since Martial switched to [[Puma]] things have n’t been going our way get my boy back {@Nike@}

## 4. Right type, other boundaries (Few-NERD, RoBERTa-large)

- gold **COMP** `Armstrong Siddeley`, predicted `Armstrong Siddeley company`. The Armstrong Siddeley Python was an early British turboprop engine designed and built by the [[Armstrong Siddeley]] company in the mid-1940s .
- gold **PROD** `TRS-80 computer`, predicted `TRS-80`. Scarfman is a clone of `` Pac-Man `` written by Philip A. Oliver for the [[TRS-80 computer]] and published by The Cornsoft Group in 1981 .
- gold **PROD** `76.2mm F-34 tank gun`, predicted `F-34`. By 1942 , the [[76.2mm F-34 tank gun]] of the T-34 medium tank was found to be lacking in range and penetration compared to the German 75 mm Pak 40 anti-tank gun , new mounted on the Stug III and Panzer IV , and markedly inferior to the 88-mm gun of the Tiger I .
- gold **PROD** `U-2 ,`, predicted `U-2`. The RPVs carried deceptive signal generators that made them appear to be the size of a [[U-2 ,]] and also carried receivers and relays for the Soviet SA-2 surface-to-air missiles on Cuba .
- gold **PROD** `Flight 19`, predicted `19`. In February 1964 , Vincent Gaddis wrote an article called `` The Deadly Bermuda Triangle `` in the pulp magazine `` Argosy `` saying [[Flight 19]] and other disappearances were part of a pattern of strange events in the region .

## 5. Media organisations (BBC, newspapers) are not companies in Few-NERD: the model says COMP

- gold OTHER (`organization-media/newspaper`), predicted COMP: It was later purchased by Southam Newspapers and then [[Canwest Global Communications]] .
- gold OTHER (`organization-media/newspaper`), predicted COMP: She is known for her roles as Judy Kramer in `` Point Pleasant `` , a 2005 series on [[Fox]] , and as Marcy Bender in `` Dawson 's Creek `` .
- gold OTHER (`organization-media/newspaper`), predicted COMP: The new series is a co-production between [[Tatsunoko]] and Digital Frontier and aired from October 3 to December 26 , 2017 .
- gold OTHER (`organization-media/newspaper`), predicted COMP: An example of a copyright infringement of a creative entrepreneur is the case of S. Victor Whitmill v . [[Warner Bros. Entertainment Inc]] .
- gold OTHER (`organization-media/newspaper`), predicted COMP: [[WWRL]] and NBN were owned by the same company .
