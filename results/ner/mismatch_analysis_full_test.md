# fewnerd

## fewnerd: gold COMP

**A. Profile.** 3903 mentions, 3189 distinct strings; lowercase-initial 1%, multi-word 61%, `{@handle@}` markup 0%, string never seen in training 45%.

**B. Annotation consistency (training split).** Strings labelled both company and product cover 6% of all COMP+PROD mentions; strings labelled COMP/PROD in some places and OTHER in others cover 15%. Examples (string: counts): london: {'OTHER': 777, 'PER': 1, 'PROD': 3, 'COMP': 1}; san francisco: {'OTHER': 204, 'COMP': 1, 'PROD': 1}; toronto: {'OTHER': 133, 'PER': 1, 'PROD': 1, 'COMP': 1}; smith: {'PER': 101, 'PROD': 2, 'OTHER': 1, 'COMP': 1}; sun: {'OTHER': 94, 'COMP': 2, 'PROD': 1, 'PER': 2}

**C. Outcome per system** (found = right span and type)

| System | group | n | found | other type | other boundaries | missed |
|---|---|---|---|---|---|---|
| RoBERTa | all | 3903 | 69% | 19% | 10% | 1% |
| RoBERTa | seen in training | 2134 | 70% | 21% | 7% | 1% |
| RoBERTa | unseen | 1769 | 68% | 16% | 14% | 1% |
| GLiNER 0.8 | all | 3903 | 64% | 5% | 9% | 22% |
| GLiNER 0.8 | seen in training | 2134 | 66% | 5% | 6% | 23% |
| GLiNER 0.8 | unseen | 1769 | 61% | 5% | 12% | 22% |

**D. Frequent strings**

- RoBERTa, gold COMP most often not found: BBC (11), NBC (7), ABC (7), McDonald (4), McDonnell Douglas (3), LIRR (3), Inc . (3), GAP (3)
- RoBERTa, gold COMP given another type: BBC -> OTHER (10), NBC -> OTHER (6), ABC -> OTHER (5), LIRR -> OTHER (3), IHOP -> OTHER (2), Burgess -> PER (2)
- RoBERTa, false positives (predicted COMP, gold at that span in brackets): Apple [gold: none] (7), CBS [gold: OTHER] (6), NVIDIA [gold: OTHER] (6), McDonald [gold: none] (4), Fox [gold: OTHER] (4), Nike [gold: none] (4), Apple [gold: PROD] (3), McDonald 's [gold: none] (3)
- GLiNER 0.8, gold COMP most often not found: BBC (7), McDonald (5), ABC (5), BR (4), Hollywood (4), RSC (3), Macy 's (3), Westward Ho (3)
- GLiNER 0.8, gold COMP given another type: Burgess -> PER (2), Alias -> PROD (2), Wavefront -> PROD (2), Alias/Wavefront -> PROD (2), Kroenke -> PER (2), Gollancz -> PER (2)
- GLiNER 0.8, false positives (predicted COMP, gold at that span in brackets): Ford [gold: none] (23), Disney [gold: none] (21), The company [gold: none] (18), British Rail [gold: none] (17), Apple [gold: none] (17), Google [gold: none] (16), Boeing [gold: none] (15), Microsoft [gold: none] (15)

**E. Examples for slides** (random gold mentions that at least one system got wrong; the gold entity is in bold)

> In 2018 , Mitchell was stripped of his records by Twin Galaxies and banned from submitting new scores after **Twin Galaxies** concluded that Mitchell had illicitly used emulators to achieve his scores .
>
> Gold: **COMP** | RoBERTa: same span, other type: OTHER | GLiNER 0.8: found

> From the second half of 2005 to the summer of 2006 , **UP** unveiled a new set of six EMD SD70ACe locomotives in `` Heritage Colors , '' painted in schemes reminiscent of railroads acquired by the Union Pacific Corporation since the 1980s .
>
> Gold: **COMP** | RoBERTa: found | GLiNER 0.8: missed

> The Evelyn Nordhoff Bindery was the continuation of **Evelyn Hunter Nordhoff 's Elephant Bindery** at 39 Washington Place in New York City .
>
> Gold: **COMP** | RoBERTa: overlapping, other boundaries | GLiNER 0.8: missed

> The new aircraft can seat up to 68 passengers and was the second aircraft to be painted in the **Flybe** livery .
>
> Gold: **COMP** | RoBERTa: same span, other type: PROD | GLiNER 0.8: found


## fewnerd: gold PROD

**A. Profile.** 6232 mentions, 5428 distinct strings; lowercase-initial 7%, multi-word 60%, `{@handle@}` markup 0%, string never seen in training 58%.

**B. Annotation consistency (training split).** Strings labelled both company and product cover 6% of all COMP+PROD mentions; strings labelled COMP/PROD in some places and OTHER in others cover 15%. Examples (string: counts): london: {'OTHER': 777, 'PER': 1, 'PROD': 3, 'COMP': 1}; san francisco: {'OTHER': 204, 'COMP': 1, 'PROD': 1}; toronto: {'OTHER': 133, 'PER': 1, 'PROD': 1, 'COMP': 1}; smith: {'PER': 101, 'PROD': 2, 'OTHER': 1, 'COMP': 1}; sun: {'OTHER': 94, 'COMP': 2, 'PROD': 1, 'PER': 2}

**C. Outcome per system** (found = right span and type)

| System | group | n | found | other type | other boundaries | missed |
|---|---|---|---|---|---|---|
| RoBERTa | all | 6232 | 70% | 8% | 13% | 8% |
| RoBERTa | seen in training | 2642 | 79% | 10% | 5% | 6% |
| RoBERTa | unseen | 3590 | 64% | 7% | 20% | 9% |
| GLiNER 0.8 | all | 6232 | 35% | 6% | 16% | 43% |
| GLiNER 0.8 | seen in training | 2642 | 37% | 9% | 11% | 42% |
| GLiNER 0.8 | unseen | 3590 | 33% | 4% | 19% | 44% |

**D. Frequent strings**

- RoBERTa, gold PROD most often not found: rice (5), AI (4), Liberty Bell (3), Apple (3), R101 (3), SSRIs (3), Victory (3), Liberty (3)
- RoBERTa, gold PROD given another type: Liberty Bell -> OTHER (3), Apple -> COMP (3), R101 -> OTHER (3), SSRIs -> OTHER (3), Lormetazepam -> OTHER (3), Sinpar -> COMP (3)
- RoBERTa, false positives (predicted PROD, gold at that span in brackets): PC [gold: none] (6), V8 [gold: none] (4), Facebook [gold: none] (4), RMS [gold: none] (4), German [gold: none] (4), Ethernet [gold: none] (3), SAR [gold: none] (3), Twitter [gold: none] (3)
- GLiNER 0.8, gold PROD most often not found: Linux (14), Windows (12), Wii (11), YouTube (9), PC (7), Unix (7), Android (7), Twitter (5)
- GLiNER 0.8, gold PROD given another type: Apple -> COMP (3), TENEX -> COMP (3), Microsoft -> COMP (3), Mercury -> COMP (3), Ferrari -> COMP (3), Hudson -> COMP (3)
- GLiNER 0.8, false positives (predicted PROD, gold at that span in brackets): DDT [gold: OTHER] (4), The Winston [gold: OTHER] (4), Christmas lights [gold: none] (4), methotrexate [gold: OTHER] (4), Wii controller [gold: none] (4), clonazepam [gold: OTHER] (4), Liberty ships [gold: none] (4), hamburgers [gold: none] (4)

**E. Examples for slides** (random gold mentions that at least one system got wrong; the gold entity is in bold)

> In 2010 , as part of the Windows Live `` Wave 4 '' release , Windows Live Web Messenger is integrated into all Windows Live web services ' headers , allowing users to sign into the **Messenger** service via the web browser on any Windows Live properties .
>
> Gold: **PROD** | RoBERTa: found | GLiNER 0.8: missed

> Fuzzball routers were the first modern routers on the **Internet** .
>
> Gold: **PROD** | RoBERTa: missed | GLiNER 0.8: missed

> Kagura 's character was also part of Bandai 's `` **∞ Puti Puti Petit Moe** `` , a series of key chains featuring characters voiced by Rie Kugimiya which simulate Kugimiya 's voice .
>
> Gold: **PROD** | RoBERTa: same span, other type: OTHER | GLiNER 0.8: missed

> **libsndfile** is used , for example , by audio-editing software such as Audacity and Adobe Audition and the MP3 encoder LAME .
>
> Gold: **PROD** | RoBERTa: missed | GLiNER 0.8: missed


# wnut17

## wnut17: gold COMP

**A. Profile.** 66 mentions, 60 distinct strings; lowercase-initial 17%, multi-word 21%, `{@handle@}` markup 0%, string never seen in training 98%.

**B. Annotation consistency (training split).** Strings labelled both company and product cover 2% of all COMP+PROD mentions; strings labelled COMP/PROD in some places and OTHER in others cover 1%. Examples (string: counts): itunes: {'PROD': 1, 'COMP': 3}; blackberry: {'COMP': 1, 'PROD': 1}

**C. Outcome per system** (found = right span and type)

| System | group | n | found | other type | other boundaries | missed |
|---|---|---|---|---|---|---|
| RoBERTa | all | 66 | 8% | 56% | 6% | 30% |
| RoBERTa | seen in training | 1 | 0% | 100% | 0% | 0% |
| RoBERTa | unseen | 65 | 8% | 55% | 6% | 31% |
| GLiNER 0.8 | all | 66 | 30% | 3% | 3% | 64% |
| GLiNER 0.8 | seen in training | 1 | 0% | 0% | 0% | 100% |
| GLiNER 0.8 | unseen | 65 | 31% | 3% | 3% | 63% |

**D. Frequent strings**

- RoBERTa, gold COMP most often not found: Reddit (3), CNN (2), airbnb (2), Fox News (2), CVS (1), Great Southern Television (1), CBC Manitoba (1), NHL (1)
- RoBERTa, gold COMP given another type: CNN -> OTHER (2), Fox News -> OTHER (2), Great Southern Television -> OTHER (1), CBC Manitoba -> OTHER (1), BuzzFeed -> OTHER (1), CBC -> OTHER (1)
- RoBERTa, false positives (predicted COMP, gold at that span in brackets): Snickers [gold: PROD] (2), Mirai [gold: PROD] (1), ELR [gold: none] (1), DeadstockUtopia [gold: none] (1), GlennTemp [gold: none] (1), adidasanorak [gold: none] (1), OriginalSoleog Indoor Super [gold: none] (1), Lowongan PT Citilink Indonesia [gold: none] (1)
- GLiNER 0.8, gold COMP most often not found: Reddit (3), CNN (2), CBC Manitoba (1), NHL (1), BuzzFeed (1), CBC (1), reddit (1), Internode (1)
- GLiNER 0.8, gold COMP given another type: Coleman -> PER (1), Prompto -> PER (1)
- GLiNER 0.8, false positives (predicted COMP, gold at that span in brackets): Snickers [gold: PROD] (4), PSG [gold: OTHER] (2), bap [gold: OTHER] (2), Bordeaux [gold: OTHER] (1), Fragrant [gold: OTHER] (1), Glenn Greenwald [gold: PER] (1), Leyonhjelm [gold: PER] (1), MU [gold: OTHER] (1)

**E. Examples for slides** (random gold mentions that at least one system got wrong; the gold entity is in bold)

> Questions Not Answers | **Box of Crayons** https://t.co/CXafSHeWPV https://t.co/9kvP5sokij
>
> Gold: **COMP** | RoBERTa: missed | GLiNER 0.8: missed

> @ microgravitylab I saw an actual child wearing a **Foxy** shirt during my last overnight shift I startled my coworker with how hard I laughed
>
> Gold: **COMP** | RoBERTa: same span, other type: PER | GLiNER 0.8: overlapping, other boundaries

> I just wrote a fucking novel regarding **BLM** ' s use of blanket statements [ here .
>
> Gold: **COMP** | RoBERTa: overlapping, other boundaries | GLiNER 0.8: found

> [ Aah , the old **Reddit** deatharoo ] ( https://www.reddit.com/r/newzealand/comments/5m9mam/kia_ora_rbrasil_cultural_exchange_with_rbrasil/dc3dgin/?context=3 )
>
> Gold: **COMP** | RoBERTa: missed | GLiNER 0.8: missed


## wnut17: gold PROD

**A. Profile.** 127 mentions, 117 distinct strings; lowercase-initial 28%, multi-word 45%, `{@handle@}` markup 0%, string never seen in training 98%.

**B. Annotation consistency (training split).** Strings labelled both company and product cover 2% of all COMP+PROD mentions; strings labelled COMP/PROD in some places and OTHER in others cover 1%. Examples (string: counts): itunes: {'PROD': 1, 'COMP': 3}; blackberry: {'COMP': 1, 'PROD': 1}

**C. Outcome per system** (found = right span and type)

| System | group | n | found | other type | other boundaries | missed |
|---|---|---|---|---|---|---|
| RoBERTa | all | 127 | 27% | 15% | 16% | 43% |
| RoBERTa | seen in training | 2 | 0% | 0% | 0% | 100% |
| RoBERTa | unseen | 125 | 27% | 15% | 16% | 42% |
| GLiNER 0.8 | all | 127 | 23% | 9% | 8% | 60% |
| GLiNER 0.8 | seen in training | 2 | 50% | 0% | 0% | 50% |
| GLiNER 0.8 | unseen | 125 | 22% | 10% | 8% | 60% |

**D. Frequent strings**

- RoBERTa, gold PROD most often not found: Snickers (3), mithril (2), p 12 format (2), epipen (1), Quickloot (1), Zlatan (1), Concorde (1), BLD (1)
- RoBERTa, gold PROD given another type: Snickers -> COMP (2), mithril -> OTHER (2), epipen -> OTHER (1), Concorde -> OTHER (1), BLD -> OTHER (1), Centrelink -> OTHER (1)
- RoBERTa, false positives (predicted PROD, gold at that span in brackets): COM [gold: none] (4), TLS [gold: none] (2), Wikipedia [gold: OTHER] (2), Cavani [gold: PER] (1), AmA [gold: none] (1), Lost RC [gold: none] (1), Reddit [gold: OTHER] (1), Mirror HD [gold: none] (1)
- GLiNER 0.8, gold PROD most often not found: Snickers (4), mithril (2), SQL (2), p 12 format (2), Nexus 6 (2), Quickloot (1), Zlatan (1), Concorde (1)
- GLiNER 0.8, gold PROD given another type: Snickers -> COMP (4), Zlatan -> PER (1), Xantec -> COMP (1), Authy -> COMP (1), Mirai -> COMP (1), Google -> COMP (1)
- GLiNER 0.8, false positives (predicted PROD, gold at that span in brackets): Aquarius [gold: none] (2), # KyState _ RYS 17 [gold: none] (2), best-quality winter clothing [gold: none] (1), pre-fabricated insulated shelters [gold: none] (1), Lost RC plane [gold: none] (1), Velvet [gold: PER] (1), Shiba Inu [gold: none] (1), AA Mirror HD [gold: none] (1)

**E. Examples for slides** (random gold mentions that at least one system got wrong; the gold entity is in bold)

> 3 weeks from now a **Centrelink** recipient kills himself .
>
> Gold: **PROD** | RoBERTa: same span, other type: OTHER | GLiNER 0.8: missed

> Good idea , especially for someone who needs this routinely for professional reasons it might be worth buying cheap hardware . I ' d like to add two things : 1 ) " disable wifi physically " is often nigh impossible . I ' d suggest to use a cable , so you never need to connect to a **wifi network** ( then the device never contains its password ) , or perhaps even remove the wifi chip ( often fairly easy ) . And 2 ) I ' d overwrite the stick or sd card after use , not terminate processes or reboot .
>
> Gold: **PROD** | RoBERTa: missed | GLiNER 0.8: missed

> Nexus 6 P | Nexus 6 Sleeve Shop : https://t.co/Rg2eopRpWB | # Nexus 6 P # **Nexus 6** # Nexus 6 PSleeve # Nexus 6 PCover # Nexus 6 PLeather # Nexus 6 PCase
>
> Gold: **PROD** | RoBERTa: found | GLiNER 0.8: missed

> Possible anomaly in **Cryptonomicon**
>
> Gold: **PROD** | RoBERTa: missed | GLiNER 0.8: missed


# tweetner7

## tweetner7: gold COMP

**A. Profile.** 1091 mentions, 806 distinct strings; lowercase-initial 5%, multi-word 39%, `{@handle@}` markup 43%, string never seen in training 53%.

**B. Annotation consistency (training split).** Strings labelled both company and product cover 7% of all COMP+PROD mentions; strings labelled COMP/PROD in some places and OTHER in others cover 15%. Examples (string: counts): twitter: {'COMP': 142, 'PROD': 11}; spotify: {'COMP': 103, 'PROD': 23, 'OTHER': 5}; youtube: {'COMP': 105, 'PROD': 14, 'OTHER': 2}; poshmark: {'COMP': 79, 'OTHER': 27, 'PROD': 13}; apple music: {'PROD': 42, 'OTHER': 11, 'COMP': 32}

**C. Outcome per system** (found = right span and type)

| System | group | n | found | other type | other boundaries | missed |
|---|---|---|---|---|---|---|
| RoBERTa | all | 1091 | 4% | 29% | 7% | 60% |
| RoBERTa | seen in training | 515 | 3% | 35% | 5% | 57% |
| RoBERTa | unseen | 576 | 5% | 23% | 9% | 64% |
| RoBERTa | handle markup | 470 | 0% | 0% | 0% | 100% |
| RoBERTa | plain text | 621 | 7% | 51% | 12% | 30% |
| GLiNER 0.8 | all | 1091 | 21% | 3% | 1% | 75% |
| GLiNER 0.8 | seen in training | 515 | 21% | 1% | 1% | 77% |
| GLiNER 0.8 | unseen | 576 | 21% | 4% | 2% | 73% |
| GLiNER 0.8 | handle markup | 470 | 23% | 1% | 0% | 77% |
| GLiNER 0.8 | plain text | 621 | 20% | 4% | 2% | 74% |

**D. Frequent strings**

- RoBERTa, gold COMP most often not found: Twitter (14), Ohio State (14), {@Amazon@} (13), Spotify (13), YouTube (13), NHL (11), NBA (8), {@MTV@} (7)
- RoBERTa, gold COMP given another type: Ohio State -> OTHER (14), Twitter -> PROD (13), Spotify -> PROD (13), NHL -> OTHER (10), YouTube -> PROD (8), NBA -> OTHER (6)
- RoBERTa, false positives (predicted COMP, gold at that span in brackets): Apple Music [gold: PROD] (5), RetroMollyTreasures [gold: none] (2), HYBE [gold: none] (2), Popin [gold: none] (1), Afro [gold: none] (1), Australian Broadcasting Corporation [gold: none] (1), Disney [gold: OTHER] (1), Walmart [gold: OTHER] (1)
- GLiNER 0.8, gold COMP most often not found: Twitter (13), Ohio State (13), NHL (11), YouTube (9), NBA (8), {@NBA@} (6), {@MTV@} (6), {@United Nations@} (6)
- GLiNER 0.8, gold COMP given another type: New Yorker -> PROD (1), IVO -> PER (1), BTS -> PER (1), United We Eat -> PROD (1), AADITYA -> PER (1), Uncle Ben -> PER (1)
- GLiNER 0.8, false positives (predicted COMP, gold at that span in brackets): {@Poshmark@} [gold: PROD] (9), ENHYPEN [gold: OTHER] (8), Poshmark [gold: none] (7), {@Netflix@} [gold: PROD] (6), {@UFC@} [gold: OTHER] (5), Amazon [gold: none] (5), Apple Music [gold: PROD] (5), UFC [gold: none] (4)

**E. Examples for slides** (random gold mentions that at least one system got wrong; the gold entity is in bold)

> " MNL 48 continues to be in the Top 5 of the MYX Daily Top 10 chart , which one is your favorite ? Tag {{USERNAME}} & {@MNL48@} on Twitter using # MNLMYX with the name of the music video and why you love it . " # MNL48 • **{@MNL48@}** {{URL}}
>
> Gold: **COMP** | RoBERTa: missed | GLiNER 0.8: missed

> MTN fiber is the internet of choice for social distancing . Been reliable this far . **{@MTN Ghana@}** aye ooo !! # StopTheSpread # SocialDistancing # COVID19Ghana
>
> Gold: **COMP** | RoBERTa: missed | GLiNER 0.8: found

> New Year ’s Resolutions for the Planet . In December , ⁦ {@The New York Times@} ⁩ asked the readers of our newsletter ClimateFwd : and our **Twitter** followers what they were planning on doing differently in 2021 . via {@The New York Times@} ⁦ {@Fridays For Future@} ⁩ ⁦⁦ {@Bill McKibben@} {{URL}}
>
> Gold: **COMP** | RoBERTa: same span, other type: PROD | GLiNER 0.8: missed

> **NHL** : Trade targets ? Best lines ? The future of Adam Lowry , Paul Stastny and Mark Scheifele ? Jets mailbag .. . {{URL}} {@Murat Ates@} {@The Athletic NHL@}
>
> Gold: **COMP** | RoBERTa: same span, other type: OTHER | GLiNER 0.8: missed


## tweetner7: gold PROD

**A. Profile.** 1192 mentions, 672 distinct strings; lowercase-initial 11%, multi-word 49%, `{@handle@}` markup 65%, string never seen in training 38%.

**B. Annotation consistency (training split).** Strings labelled both company and product cover 7% of all COMP+PROD mentions; strings labelled COMP/PROD in some places and OTHER in others cover 15%. Examples (string: counts): twitter: {'COMP': 142, 'PROD': 11}; spotify: {'COMP': 103, 'PROD': 23, 'OTHER': 5}; youtube: {'COMP': 105, 'PROD': 14, 'OTHER': 2}; poshmark: {'COMP': 79, 'OTHER': 27, 'PROD': 13}; apple music: {'PROD': 42, 'OTHER': 11, 'COMP': 32}

**C. Outcome per system** (found = right span and type)

| System | group | n | found | other type | other boundaries | missed |
|---|---|---|---|---|---|---|
| RoBERTa | all | 1192 | 8% | 6% | 5% | 81% |
| RoBERTa | seen in training | 740 | 5% | 3% | 2% | 90% |
| RoBERTa | unseen | 452 | 12% | 11% | 9% | 67% |
| RoBERTa | handle markup | 771 | 0% | 0% | 0% | 100% |
| RoBERTa | plain text | 421 | 22% | 17% | 14% | 48% |
| GLiNER 0.8 | all | 1192 | 8% | 8% | 3% | 82% |
| GLiNER 0.8 | seen in training | 740 | 4% | 9% | 1% | 86% |
| GLiNER 0.8 | unseen | 452 | 13% | 6% | 6% | 75% |
| GLiNER 0.8 | handle markup | 771 | 1% | 9% | 0% | 90% |
| GLiNER 0.8 | plain text | 421 | 19% | 6% | 8% | 67% |

**D. Frequent strings**

- RoBERTa, gold PROD most often not found: {@YouTube@} (130), {@Yahoo@} (33), {@Google News@} (23), {@Etsy@} (15), {@The New York Times@} (14), {@TIDAL@} (14), {@Daily Mail Online@} (13), {@Poshmark@} (13)
- RoBERTa, gold PROD given another type: Apple Music -> COMP (5), Bitcoin -> OTHER (3), Daily Insanity -> OTHER (2), Turkey News -> OTHER (1), Monteverdi-programme -> OTHER (1), VineWitch -> OTHER (1)
- RoBERTa, false positives (predicted PROD, gold at that span in brackets): Twitter [gold: COMP] (13), Spotify [gold: COMP] (13), YouTube [gold: COMP] (8), Twitch [gold: COMP] (3), Star Wars [gold: OTHER] (2), watermelon sugar [gold: OTHER] (2), AKUMA [gold: PER] (2), KUMA [gold: PER] (2)
- GLiNER 0.8, gold PROD most often not found: {@YouTube@} (130), {@Yahoo@} (33), {@Google News@} (23), {@Etsy@} (15), {@The New York Times@} (14), {@TIDAL@} (14), {@Daily Mail Online@} (13), {@Poshmark@} (13)
- GLiNER 0.8, gold PROD given another type: {@Poshmark@} -> COMP (9), {@Netflix@} -> COMP (6), Apple Music -> COMP (5), Spotify -> COMP (4), {@Etsy@} -> COMP (4), {@YouTube@} -> COMP (3)
- GLiNER 0.8, false positives (predicted PROD, gold at that span in brackets): drivers license [gold: OTHER] (5), Charm City Kings [gold: OTHER] (3), JIHOON BLUE HAIR [gold: none] (3), AI [gold: none] (3), coffee [gold: none] (2), app [gold: none] (2), Watermelon Sugar [gold: OTHER] (2), Umbrellas [gold: OTHER] (2)

**E. Examples for slides** (random gold mentions that at least one system got wrong; the gold entity is in bold)

> Mike Perry feels ' like a dumbass' following 90-second loss at UFC 245 **{@MMA Junkie@}** {{URL}}
>
> Gold: **PROD** | RoBERTa: missed | GLiNER 0.8: missed

> Marenostrum is set to return again this year to rock # Fuengirola 's Sohail Castle with a packed season of concerts including classical , **rock** , flamenco , rap , indie and pop music . {{USERNAME}} has the details {{URL}}
>
> Gold: **PROD** | RoBERTa: missed | GLiNER 0.8: missed

> Vile Joe Biden supporters . ‘ Racism Lives Here ‘ : Trump Supporters Targeted in Coronado with Rogue Yard Signs {{URL}} via **{@Breitbart News@}**
>
> Gold: **PROD** | RoBERTa: missed | GLiNER 0.8: missed

> Chris Brown - Forever ( Official Music Video ) {{URL}} via **{@YouTube@}** “ OLD IS GOLD ”
>
> Gold: **PROD** | RoBERTa: missed | GLiNER 0.8: missed

