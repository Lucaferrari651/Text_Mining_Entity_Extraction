# fewnerd

## fewnerd: gold COMP

**A. Profile.** 95 mentions, 92 distinct strings; lowercase-initial 0%, multi-word 59%, `{@handle@}` markup 0%, string never seen in training 51%.

**B. Annotation consistency (training split).** Strings labelled both company and product cover 6% of all COMP+PROD mentions; strings labelled COMP/PROD in some places and OTHER in others cover 15%. Examples (string: counts): london: {'OTHER': 777, 'PER': 1, 'PROD': 3, 'COMP': 1}; san francisco: {'OTHER': 204, 'COMP': 1, 'PROD': 1}; toronto: {'OTHER': 133, 'PER': 1, 'PROD': 1, 'COMP': 1}; smith: {'PER': 101, 'PROD': 2, 'OTHER': 1, 'COMP': 1}; sun: {'OTHER': 94, 'COMP': 2, 'PROD': 1, 'PER': 2}

**C. Outcome per system** (found = right span and type)

| System | group | n | found | other type | other boundaries | missed |
|---|---|---|---|---|---|---|
| RoBERTa | all | 95 | 67% | 17% | 15% | 1% |
| RoBERTa | seen in training | 47 | 72% | 17% | 9% | 2% |
| RoBERTa | unseen | 48 | 62% | 17% | 21% | 0% |
| GLiNER 0.8 | all | 95 | 55% | 4% | 15% | 26% |
| GLiNER 0.8 | seen in training | 47 | 57% | 2% | 9% | 32% |
| GLiNER 0.8 | unseen | 48 | 52% | 6% | 21% | 21% |
| LLM 8B | all | 95 | 57% | 7% | 11% | 25% |
| LLM 8B | seen in training | 47 | 66% | 9% | 2% | 23% |
| LLM 8B | unseen | 48 | 48% | 6% | 19% | 27% |

**D. Frequent strings**

- RoBERTa, gold COMP most often not found: Achille Lauro & amp ; Co , Naples (1), Radio Television Hong Kong ( RTHK ) (1), Metropolitan Railway (1), J. Alexander 's Inc . (1), Metro International (1), Will Hays (1), Broadway (1), Shaw (1)
- RoBERTa, gold COMP given another type: Will Hays -> PER (1), Broadway -> OTHER (1), Shaw -> PER (1), Tokyo Institute of Technology -> OTHER (1), Brilliant Branch -> OTHER (1), HUC -> OTHER (1)
- RoBERTa, false positives (predicted COMP, gold at that span in brackets): Google Fiber [gold: PROD] (2), Naples [gold: none] (1), Achille Lauro & amp ; Co [gold: none] (1), Abbey Road Studios [gold: OTHER] (1), BBC [gold: none] (1), Acorn Computers [gold: PROD] (1), Rocky Mountain Airways [gold: none] (1), Sony [gold: none] (1)
- GLiNER 0.8, gold COMP most often not found: Achille Lauro & amp ; Co , Naples (1), Continental Express (1), Radio Television Hong Kong ( RTHK ) (1), Westward Ho (1), MR (1), Metropolitan Railway (1), Will Hays (1), Broadway (1)
- GLiNER 0.8, gold COMP given another type: Will Hays -> PER (1), Long Island Bus -> PROD (1), Egert -> PER (1), Good Life -> PER (1)
- GLiNER 0.8, false positives (predicted COMP, gold at that span in brackets): Toyota [gold: none] (2), CBC [gold: OTHER] (2), Jade Bird [gold: none] (2), Google [gold: none] (2), Telekom [gold: none] (2), Disney [gold: none] (1), Disney-MGM Studios [gold: OTHER] (1), Dubai Metro [gold: none] (1)
- LLM 8B, gold COMP most often not found: Achille Lauro & amp ; Co , Naples (1), Toyota (1), Radio Television Hong Kong ( RTHK ) (1), Westward Ho (1), MR (1), Solidus Co . (1), American Hometown Publishing Inc . (1), J. Alexander 's Inc . (1)
- LLM 8B, gold COMP given another type: Westward Ho -> PROD (1), Will Hays -> PER (1), Air Florida -> PROD (1), Long Island Bus -> PROD (1), Mirrus -> PROD (1), Michelin -> PROD (1)
- LLM 8B, false positives (predicted COMP, gold at that span in brackets): CBC [gold: OTHER] (2), Northwestern [gold: none] (2), UTM [gold: none] (2), Serbian SuperLiga [gold: OTHER] (2), Telekom S-League [gold: OTHER] (2), Kach [gold: OTHER] (2), New England Patriots [gold: OTHER] (1), Disney-MGM Studios [gold: OTHER] (1)

**E. Examples for slides** (random gold mentions that at least one system got wrong; the gold entity is in bold)

> An additional 7.17 % shares were held by **Shenzhen Beida Jade Bird Sei-Tech** , a subsidiary ( 90 % ) of Beijing Beida Jade Bird ; an additional 7.17 % shares were held by another indirect subsidiary ( 46 % ) of Jade Bird Software : Haikou Jade Bird Yuanwang Sci-Tech Development ; the shares held by `` Jade Bird Shenzhen `` would be transferred to `` Jade Bird Haikou `` .
>
> Gold: **COMP** | RoBERTa: found | GLiNER 0.8: overlapping, other boundaries | LLM 8B: found

> An additional 7.17 % shares were held by Shenzhen Beida Jade Bird Sei-Tech , a subsidiary ( 90 % ) of Beijing Beida Jade Bird ; an additional 7.17 % shares were held by another indirect subsidiary ( 46 % ) of Jade Bird Software : Haikou Jade Bird Yuanwang Sci-Tech Development ; the shares held by `` Jade Bird Shenzhen `` would be transferred to `` **Jade Bird Haikou** `` .
>
> Gold: **COMP** | RoBERTa: found | GLiNER 0.8: overlapping, other boundaries | LLM 8B: found

> TSR awarded **Interplay Productions , Inc .** a license to use the Forgotten Realms and Planescape trademarks and associated properties for use in computer and video game products .
>
> Gold: **COMP** | RoBERTa: found | GLiNER 0.8: found | LLM 8B: overlapping, other boundaries

> On December 15 , 2005 , parent company Copa Holdings , S.A . , launched an IPO of 14 million shares on the New York Stock Exchange thus becoming the fourth Latin American airline to be traded on the exchange , after LAN Airlines of Chile and Brazilian carriers **Gol Transportes Aéreos** and TAM Airlines .
>
> Gold: **COMP** | RoBERTa: found | GLiNER 0.8: missed | LLM 8B: found


## fewnerd: gold PROD

**A. Profile.** 122 mentions, 120 distinct strings; lowercase-initial 10%, multi-word 58%, `{@handle@}` markup 0%, string never seen in training 56%.

**B. Annotation consistency (training split).** Strings labelled both company and product cover 6% of all COMP+PROD mentions; strings labelled COMP/PROD in some places and OTHER in others cover 15%. Examples (string: counts): london: {'OTHER': 777, 'PER': 1, 'PROD': 3, 'COMP': 1}; san francisco: {'OTHER': 204, 'COMP': 1, 'PROD': 1}; toronto: {'OTHER': 133, 'PER': 1, 'PROD': 1, 'COMP': 1}; smith: {'PER': 101, 'PROD': 2, 'OTHER': 1, 'COMP': 1}; sun: {'OTHER': 94, 'COMP': 2, 'PROD': 1, 'PER': 2}

**C. Outcome per system** (found = right span and type)

| System | group | n | found | other type | other boundaries | missed |
|---|---|---|---|---|---|---|
| RoBERTa | all | 122 | 68% | 11% | 16% | 5% |
| RoBERTa | seen in training | 54 | 61% | 20% | 13% | 6% |
| RoBERTa | unseen | 68 | 74% | 4% | 18% | 4% |
| GLiNER 0.8 | all | 122 | 39% | 5% | 14% | 43% |
| GLiNER 0.8 | seen in training | 54 | 31% | 9% | 9% | 50% |
| GLiNER 0.8 | unseen | 68 | 44% | 1% | 18% | 37% |
| LLM 8B | all | 122 | 46% | 2% | 13% | 39% |
| LLM 8B | seen in training | 54 | 50% | 2% | 4% | 44% |
| LLM 8B | unseen | 68 | 43% | 1% | 21% | 35% |

**D. Frequent strings**

- RoBERTa, gold PROD most often not found: Google Fiber (2), Pandas (1), Acorn Computers (1), Rocky Mountain Airways ATR 42s (1), ASW (1), AK-630 (1), CIWS (1), SS-N-22 `` Sunburn '' (1)
- RoBERTa, gold PROD given another type: Google Fiber -> COMP (2), Pandas -> OTHER (1), Acorn Computers -> COMP (1), Delaware -> OTHER (1), chloramphenicol -> OTHER (1), Arc the Lad Collection -> OTHER (1)
- RoBERTa, false positives (predicted PROD, gold at that span in brackets): Trump 1 [gold: none] (1), trump 2 [gold: none] (1), Micro [gold: none] (1), ATR 42s [gold: none] (1), UStream [gold: OTHER] (1), ASW torpedoes [gold: none] (1), AK-630 automatic CIWS cannons [gold: none] (1), SS-N-22 `` Sunburn '' supersonic [gold: none] (1)
- GLiNER 0.8, gold PROD most often not found: Google Fiber (2), Pandas (1), Acorn Computers (1), Rocky Mountain Airways ATR 42s (1), GMT 345 (1), ASW (1), AK-630 (1), CIWS (1)
- GLiNER 0.8, gold PROD given another type: Acorn Computers -> COMP (1), Flickr -> COMP (1), Panoramio -> COMP (1), Phoronix -> COMP (1), Knox -> COMP (1), Hutchins -> PER (1)
- GLiNER 0.8, false positives (predicted PROD, gold at that span in brackets): L'Oiseau Bleu [gold: PER] (2), Typhoon Lagoon [gold: none] (1), 4-wheel disc brakes [gold: none] (1), tinted windows [gold: none] (1), sports styled front and rear bumpers [gold: none] (1), hardware speech synthesis system [gold: none] (1), True Love Ways [gold: none] (1), ATR 42s [gold: none] (1)
- LLM 8B, gold PROD most often not found: Gabbiano (1), Acorn Computers (1), Rocky Mountain Airways ATR 42s (1), Beechcraft 1900Cs (1), Grand Slam bombs (1), Tallboy bombs (1), GMT355 (1), GMT 345 (1)
- LLM 8B, gold PROD given another type: Acorn Computers -> COMP (1), Hutchins -> PER (1)
- LLM 8B, false positives (predicted PROD, gold at that span in brackets): Tiger Army [gold: OTHER] (2), Super Bowl XXXVI [gold: OTHER] (1), Moneymaker Effect [gold: none] (1), Disney 's Typhoon Lagoon [gold: OTHER] (1), Messiah Evangelical Lutheran Church [gold: OTHER] (1), Holy Trinity Lutheran Church [gold: OTHER] (1), US [gold: none] (1), Cyclone Larry [gold: OTHER] (1)

**E. Examples for slides** (random gold mentions that at least one system got wrong; the gold entity is in bold)

> The United States Marine Corps also offers an online version of all the languages that Rosetta Stone offers through their **MarineNet Distance Learning** portal .
>
> Gold: **PROD** | RoBERTa: overlapping, other boundaries | GLiNER 0.8: missed | LLM 8B: missed

> Passengers who had hoped to make flights in the **Lynx** included the winners from the Axe Apollo Space Academy worldwide perfume contest , and Justin Dowd of Worcester , Massachusetts , who won Metro International 's Race for Space newspaper contest .
>
> Gold: **PROD** | RoBERTa: found | GLiNER 0.8: found | LLM 8B: missed

> Following an escort voyage to New Caledonia and Espiritu Santo , `` **Hutchins** `` arrived at Pearl Harbor on 30 May for armament alterations .
>
> Gold: **PROD** | RoBERTa: found | GLiNER 0.8: same span, other type: PER | LLM 8B: same span, other type: PER

> Popular variations include mango , banana , sugar , condensed milk , jam , **peanut butter** and Nutella roti , although egg roti ( often with sweetened condensed milk spread over the top ) is also available .
>
> Gold: **PROD** | RoBERTa: found | GLiNER 0.8: missed | LLM 8B: missed


# wnut17

## wnut17: gold COMP

**A. Profile.** 43 mentions, 42 distinct strings; lowercase-initial 19%, multi-word 21%, `{@handle@}` markup 0%, string never seen in training 98%.

**B. Annotation consistency (training split).** Strings labelled both company and product cover 2% of all COMP+PROD mentions; strings labelled COMP/PROD in some places and OTHER in others cover 1%. Examples (string: counts): itunes: {'PROD': 1, 'COMP': 3}; blackberry: {'COMP': 1, 'PROD': 1}

**C. Outcome per system** (found = right span and type)

| System | group | n | found | other type | other boundaries | missed |
|---|---|---|---|---|---|---|
| RoBERTa | all | 43 | 9% | 51% | 5% | 35% |
| RoBERTa | seen in training | 1 | 0% | 100% | 0% | 0% |
| RoBERTa | unseen | 42 | 10% | 50% | 5% | 36% |
| GLiNER 0.8 | all | 43 | 28% | 0% | 2% | 70% |
| GLiNER 0.8 | seen in training | 1 | 0% | 0% | 0% | 100% |
| GLiNER 0.8 | unseen | 42 | 29% | 0% | 2% | 69% |
| LLM 8B | all | 43 | 19% | 2% | 2% | 77% |
| LLM 8B | seen in training | 1 | 0% | 0% | 0% | 100% |
| LLM 8B | unseen | 42 | 19% | 2% | 2% | 76% |

**D. Frequent strings**

- RoBERTa, gold COMP most often not found: Reddit (2), Super Bowl (1), ELVIclothing (1), BLM (1), CBSSports (1), PT Citilink Indonesia (1), Citilink (1), CNN (1)
- RoBERTa, gold COMP given another type: Super Bowl -> OTHER (1), CBSSports -> OTHER (1), CNN -> OTHER (1), HuffPostWeird -> OTHER (1), Virgin Active -> OTHER (1), WholeFoods -> OTHER (1)
- RoBERTa, false positives (predicted COMP, gold at that span in brackets): Lowongan PT Citilink Indonesia [gold: none] (1), BCraftStorage [gold: none] (1), ELR [gold: none] (1), Snickers [gold: PROD] (1), Postmates [gold: PROD] (1), adidasanorak [gold: none] (1), DeadstockUtopia [gold: none] (1), GlennTemp [gold: none] (1)
- GLiNER 0.8, gold COMP most often not found: Reddit (2), Super Bowl (1), CBSSports (1), CNN (1), Children ' s of A is (1), HuffPostWeird (1), WholeFoods (1), FordPerformance (1)
- GLiNER 0.8, gold COMP given another type: -
- GLiNER 0.8, false positives (predicted COMP, gold at that span in brackets): Snickers [gold: PROD] (2), bap [gold: OTHER] (2), DELL [gold: none] (1), Gwynstone [gold: none] (1), GhostSec [gold: none] (1), Google [gold: OTHER] (1), http://www.google.co.nz [gold: none] (1), Xantec [gold: PROD] (1)
- LLM 8B, gold COMP most often not found: Reddit (2), Super Bowl (1), BLM (1), CBSSports (1), PT Citilink Indonesia (1), CNN (1), Children ' s of A is (1), HuffPostWeird (1)
- LLM 8B, gold COMP given another type: Foxy -> PROD (1)
- LLM 8B, false positives (predicted COMP, gold at that span in brackets): DRDO [gold: OTHER] (2), BordNaMonaLisa [gold: none] (1), DELL [gold: none] (1), Lyft [gold: PROD] (1), Citilink [gold: none] (1), Google [gold: OTHER] (1), Biomedical Laboratories [gold: none] (1), Blog Technology [gold: OTHER] (1)

**E. Examples for slides** (random gold mentions that at least one system got wrong; the gold entity is in bold)

> Even though I ' ve only been once through a reciprocal membership , I ' ll nominate **Virgin Active** at Moore Park / Zetland for you .
>
> Gold: **COMP** | RoBERTa: same span, other type: OTHER | GLiNER 0.8: found | LLM 8B: found

> @ RevAaronMarquis Based off ELR , I assume you smoke ? If so , are you one of the few **RT** employees who do ?
>
> Gold: **COMP** | RoBERTa: found | GLiNER 0.8: missed | LLM 8B: missed

> RT @ jzaffos : Hey federal scientists : @ **highcountrynews** is collecting reports of interference or intimidation . Confidential form : https://t.c…
>
> Gold: **COMP** | RoBERTa: missed | GLiNER 0.8: missed | LLM 8B: missed

> . @ keselowski currently p 5 after his first run . | @ allianceparts @ **FordPerformance**
>
> Gold: **COMP** | RoBERTa: missed | GLiNER 0.8: missed | LLM 8B: missed


## wnut17: gold PROD

**A. Profile.** 60 mentions, 56 distinct strings; lowercase-initial 28%, multi-word 35%, `{@handle@}` markup 0%, string never seen in training 100%.

**B. Annotation consistency (training split).** Strings labelled both company and product cover 2% of all COMP+PROD mentions; strings labelled COMP/PROD in some places and OTHER in others cover 1%. Examples (string: counts): itunes: {'PROD': 1, 'COMP': 3}; blackberry: {'COMP': 1, 'PROD': 1}

**C. Outcome per system** (found = right span and type)

| System | group | n | found | other type | other boundaries | missed |
|---|---|---|---|---|---|---|
| RoBERTa | all | 60 | 22% | 18% | 18% | 42% |
| RoBERTa | seen in training | 0 | - | - | - | - |
| RoBERTa | unseen | 60 | 22% | 18% | 18% | 42% |
| GLiNER 0.8 | all | 60 | 17% | 8% | 8% | 67% |
| GLiNER 0.8 | seen in training | 0 | - | - | - | - |
| GLiNER 0.8 | unseen | 60 | 17% | 8% | 8% | 67% |
| LLM 8B | all | 60 | 10% | 3% | 12% | 75% |
| LLM 8B | seen in training | 0 | - | - | - | - |
| LLM 8B | unseen | 60 | 10% | 3% | 12% | 75% |

**D. Frequent strings**

- RoBERTa, gold PROD most often not found: Snickers (2), mithril (2), ' Into the Wild ' collection (1), Instagr (1), DELL Inspiron 17 R 5721 Core i 5 - 3317 U 1 . 7 GHz 6 Gb 750 Gb DVDRW 17 . 3 " Laptop (1), Smule (1), cadillac (1), GhostSec ' s pentest labs (1)
- RoBERTa, gold PROD given another type: mithril -> OTHER (2), Smule -> OTHER (1), Xantec -> PER (1), Mjölnirs -> OTHER (1), Concorde -> OTHER (1), Snickers -> COMP (1)
- RoBERTa, false positives (predicted PROD, gold at that span in brackets): Wikipedia [gold: OTHER] (2), T- 800 [gold: PER] (1), T- 1000 [gold: none] (1), DELL Inspiron 17 R [gold: none] (1), SoundCloud [gold: none] (1), features [gold: none] (1), Quidditch [gold: none] (1), MathJax [gold: none] (1)
- GLiNER 0.8, gold PROD most often not found: SQL (2), Snickers (2), mithril (2), Gmail (1), ' Into the Wild ' collection (1), Instagr (1), DELL Inspiron 17 R 5721 Core i 5 - 3317 U 1 . 7 GHz 6 Gb 750 Gb DVDRW 17 . 3 " Laptop (1), Smule (1)
- GLiNER 0.8, gold PROD given another type: Snickers -> COMP (2), Xantec -> COMP (1), Virgo -> PER (1), Zlatan -> PER (1)
- GLiNER 0.8, false positives (predicted PROD, gold at that span in brackets): # KyState _ RYS 17 [gold: none] (2), T- 800 [gold: PER] (1), T- 1000 [gold: none] (1), Into the Wild [gold: none] (1), https://www.reddit.com/r/newzealand/comments/5t2puj/maori_stormtrooper_helmet/ [gold: none] (1), DiscoveryRidge [gold: none] (1), e-cigs [gold: none] (1), Powerful Board Game [gold: none] (1)
- LLM 8B, gold PROD most often not found: SQL (2), mathjax (2), mithril (2), Gmail (1), ' Into the Wild ' collection (1), Instagr (1), DELL Inspiron 17 R 5721 Core i 5 - 3317 U 1 . 7 GHz 6 Gb 750 Gb DVDRW 17 . 3 " Laptop (1), Smule (1)
- LLM 8B, gold PROD given another type: Lyft -> COMP (1), Zlatan -> PER (1)
- LLM 8B, false positives (predicted PROD, gold at that span in brackets): Star Trek [gold: OTHER] (3), the book [gold: none] (2), Libra [gold: none] (2), Inspiron 17 R 5721 [gold: none] (1), Apna Sangeet [gold: OTHER] (1), SoundCloud [gold: none] (1), Audiologist - B [gold: none] (1), Marengo [gold: none] (1)

**E. Examples for slides** (random gold mentions that at least one system got wrong; the gold entity is in bold)

> An old TV show with a man driving around in his **cadillac** solving problems
>
> Gold: **PROD** | RoBERTa: missed | GLiNER 0.8: found | LLM 8B: missed

> [ **Snickers** ] ( https://www.reddit.com/r/ireland/comments/3dpuxy/visiting_your_beautiful_country_this_weekend_want/ )
>
> Gold: **PROD** | RoBERTa: missed | GLiNER 0.8: same span, other type: COMP | LLM 8B: found

> Good idea , especially for someone who needs this routinely for professional reasons it might be worth buying cheap hardware . I ' d like to add two things : 1 ) " disable wifi physically " is often nigh impossible . I ' d suggest to use a cable , so you never need to connect to a **wifi network** ( then the device never contains its password ) , or perhaps even remove the wifi chip ( often fairly easy ) . And 2 ) I ' d overwrite the stick or sd card after use , not terminate processes or reboot .
>
> Gold: **PROD** | RoBERTa: missed | GLiNER 0.8: missed | LLM 8B: missed

> In the context of **FIDO U 2 F** , when is a new ephemeral key reused , or cached ?
>
> Gold: **PROD** | RoBERTa: found | GLiNER 0.8: found | LLM 8B: missed


# tweetner7

## tweetner7: gold COMP

**A. Profile.** 251 mentions, 218 distinct strings; lowercase-initial 4%, multi-word 41%, `{@handle@}` markup 44%, string never seen in training 51%.

**B. Annotation consistency (training split).** Strings labelled both company and product cover 7% of all COMP+PROD mentions; strings labelled COMP/PROD in some places and OTHER in others cover 15%. Examples (string: counts): twitter: {'COMP': 142, 'PROD': 11}; spotify: {'COMP': 103, 'PROD': 23, 'OTHER': 5}; youtube: {'COMP': 105, 'PROD': 14, 'OTHER': 2}; poshmark: {'COMP': 79, 'OTHER': 27, 'PROD': 13}; apple music: {'PROD': 42, 'OTHER': 11, 'COMP': 32}

**C. Outcome per system** (found = right span and type)

| System | group | n | found | other type | other boundaries | missed |
|---|---|---|---|---|---|---|
| RoBERTa | all | 251 | 4% | 28% | 8% | 60% |
| RoBERTa | seen in training | 123 | 5% | 37% | 7% | 51% |
| RoBERTa | unseen | 128 | 3% | 20% | 9% | 69% |
| RoBERTa | handle markup | 110 | 0% | 0% | 0% | 100% |
| RoBERTa | plain text | 141 | 7% | 50% | 13% | 29% |
| GLiNER 0.8 | all | 251 | 16% | 3% | 0% | 80% |
| GLiNER 0.8 | seen in training | 123 | 23% | 2% | 0% | 75% |
| GLiNER 0.8 | unseen | 128 | 9% | 4% | 1% | 86% |
| GLiNER 0.8 | handle markup | 110 | 15% | 1% | 0% | 84% |
| GLiNER 0.8 | plain text | 141 | 16% | 5% | 1% | 78% |
| LLM 8B | all | 251 | 22% | 5% | 1% | 73% |
| LLM 8B | seen in training | 123 | 26% | 7% | 0% | 67% |
| LLM 8B | unseen | 128 | 17% | 4% | 2% | 77% |
| LLM 8B | handle markup | 110 | 32% | 1% | 0% | 67% |
| LLM 8B | plain text | 141 | 13% | 9% | 1% | 77% |

**D. Frequent strings**

- RoBERTa, gold COMP most often not found: YouTube (5), Spotify (4), NHL (4), Twitter (3), {@FOX Sports@} (3), {@Tesla@} (2), Trance (2), {@United Nations@} (2)
- RoBERTa, gold COMP given another type: Spotify -> PROD (4), NHL -> OTHER (3), Twitter -> PROD (2), YouTube -> PROD (2), XFL -> OTHER (2), NitroEx -> PROD (2)
- RoBERTa, false positives (predicted COMP, gold at that span in brackets): Interior [gold: none] (1), NAPA [gold: OTHER] (1), BhookhaHaathi Hospitality [gold: none] (1), RUN BTS [gold: none] (1), Uber [gold: PROD] (1), Johnson [gold: none] (1), Cormann [gold: PER] (1), Australian Broadcasting Corporation [gold: none] (1)
- GLiNER 0.8, gold COMP most often not found: NHL (4), Twitter (3), {@FOX Sports@} (3), Trance (2), {@United Nations@} (2), {@Full Fact@} (2), YouTube (2), {@Al Jazeera English@} (2)
- GLiNER 0.8, gold COMP given another type: Michigan Gov . Whitmer -> PER (1), IVO -> PER (1), New Yorker -> PROD (1), {@Minister of Commerce and Industry@} -> PER (1), THE ALBUM -> PROD (1), Trumps -> PER (1)
- GLiNER 0.8, false positives (predicted COMP, gold at that span in brackets): {@Poshmark@} [gold: PROD] (3), ENHYPEN [gold: OTHER] (3), {@Etsy@} [gold: PROD] (2), Patriots [gold: OTHER] (2), KVGC [gold: none] (2), {@Battlestate Games@} [gold: PROD] (2), {@YouTube@} [gold: PROD] (2), TSLA [gold: none] (2)
- LLM 8B, gold COMP most often not found: YouTube (5), Spotify (4), NHL (4), Twitter (3), Trance (2), {@United Nations@} (2), {@Al Jazeera English@} (2), {@NOLA.com@} (2)
- LLM 8B, gold COMP given another type: Apple -> PROD (2), Flashback Future -> PROD (1), Ohio State -> PROD (1), IVO -> PER (1), youtube -> PROD (1), Taji amejua kunyonya kidole -> PROD (1)
- LLM 8B, false positives (predicted COMP, gold at that span in brackets): {@TIDAL@} [gold: PROD] (5), {@TREASURE@} [gold: OTHER] (5), {@BLACKPINKOFFICIAL@} [gold: OTHER] (3), {@BTS_twt@} [gold: OTHER] (3), Burnley [gold: OTHER] (3), {@DistroKid@} [gold: PROD] (2), {@UFC@} [gold: OTHER] (2), BTS [gold: OTHER] (2)

**E. Examples for slides** (random gold mentions that at least one system got wrong; the gold entity is in bold)

> The {@Dallas Stars@} made their coach a happy man after Game 1 of the Stanley Cup Final . Well , except for that one thing . # **NHL** {{URL}}
>
> Gold: **COMP** | RoBERTa: same span, other type: OTHER | GLiNER 0.8: missed | LLM 8B: missed

> on {@YouTube@} : NEW **MOB OF THE DEAD** SECRET FOUND : 8 YEARS LATER !! ( New Cut Audio ) {{URL}}
>
> Gold: **COMP** | RoBERTa: missed | GLiNER 0.8: missed | LLM 8B: same span, other type: PROD

> Our Travel Correspondent {@Simon Calder@} will be answering all your questions live on **Facebook** at 12 noon today ✈
>
> Gold: **COMP** | RoBERTa: same span, other type: PROD | GLiNER 0.8: missed | LLM 8B: missed

> Listen to Breanna Rubio " Bad Side " on IHeartradio , The Heat 100.9 " Stay Ready Boyz " and **103.7 Dabeat Radio** {{USERNAME}} also download it on iTunes and other retailers online . Follow {{USERNAME}} {{USERNAME}} … {{URL}}
>
> Gold: **COMP** | RoBERTa: overlapping, other boundaries | GLiNER 0.8: missed | LLM 8B: missed


## tweetner7: gold PROD

**A. Profile.** 311 mentions, 228 distinct strings; lowercase-initial 17%, multi-word 46%, `{@handle@}` markup 57%, string never seen in training 45%.

**B. Annotation consistency (training split).** Strings labelled both company and product cover 7% of all COMP+PROD mentions; strings labelled COMP/PROD in some places and OTHER in others cover 15%. Examples (string: counts): twitter: {'COMP': 142, 'PROD': 11}; spotify: {'COMP': 103, 'PROD': 23, 'OTHER': 5}; youtube: {'COMP': 105, 'PROD': 14, 'OTHER': 2}; poshmark: {'COMP': 79, 'OTHER': 27, 'PROD': 13}; apple music: {'PROD': 42, 'OTHER': 11, 'COMP': 32}

**C. Outcome per system** (found = right span and type)

| System | group | n | found | other type | other boundaries | missed |
|---|---|---|---|---|---|---|
| RoBERTa | all | 311 | 12% | 8% | 4% | 77% |
| RoBERTa | seen in training | 171 | 9% | 2% | 1% | 88% |
| RoBERTa | unseen | 140 | 16% | 14% | 7% | 63% |
| RoBERTa | handle markup | 178 | 0% | 0% | 0% | 100% |
| RoBERTa | plain text | 133 | 28% | 18% | 8% | 46% |
| GLiNER 0.8 | all | 311 | 9% | 7% | 5% | 79% |
| GLiNER 0.8 | seen in training | 171 | 1% | 10% | 1% | 88% |
| GLiNER 0.8 | unseen | 140 | 19% | 3% | 9% | 69% |
| GLiNER 0.8 | handle markup | 178 | 1% | 8% | 0% | 91% |
| GLiNER 0.8 | plain text | 133 | 20% | 5% | 11% | 64% |
| LLM 8B | all | 311 | 6% | 11% | 3% | 80% |
| LLM 8B | seen in training | 171 | 1% | 14% | 1% | 84% |
| LLM 8B | unseen | 140 | 12% | 8% | 6% | 74% |
| LLM 8B | handle markup | 178 | 1% | 18% | 0% | 81% |
| LLM 8B | plain text | 133 | 13% | 2% | 8% | 77% |

**D. Frequent strings**

- RoBERTa, gold PROD most often not found: {@YouTube@} (28), {@Yahoo@} (8), {@Google News@} (7), {@TIDAL@} (6), {@Change org Россия@} (5), {@Poshmark@} (4), {@Etsy@} (4), {@The New York Times@} (4)
- RoBERTa, gold PROD given another type: ODP Ohio South -> OTHER (1), Abdala -> OTHER (1), Wagon Train -> OTHER (1), Covid19vaccine -> OTHER (1), Turkey News -> OTHER (1), CO2 -> OTHER (1)
- RoBERTa, false positives (predicted PROD, gold at that span in brackets): Spotify [gold: COMP] (4), Twitter [gold: COMP] (2), YouTube [gold: COMP] (2), NitroEx [gold: COMP] (2), GPT-3 [gold: none] (1), Hematite [gold: none] (1), Poshmark [gold: COMP] (1), iTunes [gold: COMP] (1)
- GLiNER 0.8, gold PROD most often not found: {@YouTube@} (28), {@Yahoo@} (8), {@Google News@} (7), {@TIDAL@} (6), {@Change org Россия@} (5), {@Poshmark@} (4), {@Etsy@} (4), {@The New York Times@} (4)
- GLiNER 0.8, gold PROD given another type: {@Poshmark@} -> COMP (3), {@Etsy@} -> COMP (2), {@Battlestate Games@} -> COMP (2), {@YouTube@} -> COMP (2), Apple Music -> COMP (2), {@CD PROJEKT RED@} -> COMP (1)
- GLiNER 0.8, false positives (predicted PROD, gold at that span in brackets): AI [gold: none] (3), JIHOON BLUE HAIR [gold: none] (3), coffee [gold: none] (2), wine [gold: none] (2), IDA [gold: none] (2), Vaccine Passports [gold: none] (1), Victims Of The Beats [gold: OTHER] (1), Attack on Titan [gold: OTHER] (1)
- LLM 8B, gold PROD most often not found: {@YouTube@} (28), {@Yahoo@} (8), {@Google News@} (7), {@TIDAL@} (6), {@Change org Россия@} (5), {@Poshmark@} (4), {@Etsy@} (4), {@The New York Times@} (4)
- LLM 8B, gold PROD given another type: {@TIDAL@} -> COMP (5), {@DistroKid@} -> COMP (2), {@The New York Times@} -> COMP (2), {@VERZUZ@} -> COMP (1), {@CD PROJEKT RED@} -> COMP (1), {@Listia@} -> COMP (1)
- LLM 8B, false positives (predicted PROD, gold at that span in brackets): ENHYPEN [gold: OTHER] (3), UAE [gold: OTHER] (3), Dodgers [gold: OTHER] (2), coffee [gold: none] (2), Wonder Woman [gold: none] (2), Apple [gold: COMP] (2), Permission To Dance [gold: none] (2), The Good Times And The Bad Ones [gold: none] (2)

**E. Examples for slides** (random gold mentions that at least one system got wrong; the gold entity is in bold)

> Lifeprint 2x3 Instant Printer for iPhone . Turn Your iPhone Into an Instant-Pr .. . {{URL}} via {@Amazon@} Harry Potter Magic Photo and Video Printer for **iPhone** and Android . Your Phot
>
> Gold: **PROD** | RoBERTa: found | GLiNER 0.8: missed | LLM 8B: missed

> According to a recent IMF report , limiting global warming even to 2 ° C would require a global carbon price of at least $ 75-100 per ton of **CO2** – more than double its current level – by 2030 . Maybe {{USERNAME}} is right and we need a predictable price path to get there .
>
> Gold: **PROD** | RoBERTa: same span, other type: OTHER | GLiNER 0.8: missed | LLM 8B: missed

> Venezuela and Cuba will jointly produce “ **Abdala** ” anti-Covid vaccine {{URL}} via {@The Rio Times@}
>
> Gold: **PROD** | RoBERTa: same span, other type: OTHER | GLiNER 0.8: missed | LLM 8B: found

> Pink # facemask , # geometrical print # fitted # Reusable and # washable lycra face mask , dust home choir face mask , hairstylist mask , cosplay # EDM mask # handmade # indiebusiness # StandWithSmall {{URL}} **{@Etsy@}**
>
> Gold: **PROD** | RoBERTa: missed | GLiNER 0.8: missed | LLM 8B: same span, other type: COMP

