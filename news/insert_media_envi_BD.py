import psycopg2


print("Lancement insert BD")

# a supp
# bitcoin gaspille pas d'energie
# miner au salvador serieux

list_media_envi_ajout = [
    ['S01E01 - "Si tu imprimes des billets au Monopoly, ça fout en l’air le jeu"', 'Pendule de Satoshi', '2021-03-01 12:00:00', 'https://anchor.fm/pendulesatoshi/episodes/S01E01---Si-tu-imprimes-des-billets-au-Monopoly--a-fout-en-lair-le-jeu-e1ee6mm',
        'https://bitcoin.fr/wp-content/uploads/2022/03/Pendule-de-Satoshi.jpg'],
    ["S01E02 - L'Étalon-Or, une réserve de valeur pour couvrir des moyens de paiements plus pratiques", 'Pendule de Satoshi', '2021-03-11 12:00:00', 'https://anchor.fm/pendulesatoshi/episodes/S01E02---Ltalon-Or--une-rserve-de-valeur-pour-couvrir-des-moyens-de-paiements-plus-pratiques-e1erpvn',
        'https://bitcoin.fr/wp-content/uploads/2022/03/Pendule-de-Satoshi.jpg'],
    ["S01E03 - Les banques centrales, c'est quoi en fait?", 'Pendule de Satoshi', '2021-03-19 12:00:00', 'https://anchor.fm/pendulesatoshi/episodes/S01E03---Les-banques-centrales--cest-quoi-en-fait-e1f3444',
        'https://bitcoin.fr/wp-content/uploads/2022/03/Pendule-de-Satoshi.jpg'],
    ['S01E04 - Bienvenue dans le terrier du lapin!', 'Pendule de Satoshi', '2021-03-29 12:00:00', 'https://anchor.fm/pendulesatoshi/episodes/S01E04---Bienvenue-dans-le-terrier-du-lapin-e1foijp',
        'https://bitcoin.fr/wp-content/uploads/2022/03/Pendule-de-Satoshi.jpg'],
    ["S01E05 - Et si on reprenait l'habitude de notre souveraineté financière?", 'Pendule de Satoshi', '2021-04-05 12:00:00', 'https://anchor.fm/pendulesatoshi/episodes/S01E05---Et-si-on-reprenait-lhabitude-de-notre-souverainet-financire-e1gl91k',
        'https://bitcoin.fr/wp-content/uploads/2022/03/Pendule-de-Satoshi.jpg'],
    ['S01E06 - Petit récapitulatif. Les adresses, les portefeuilles, les clefs...', 'Pendule de Satoshi', '2021-04-11 12:00:00', 'https://anchor.fm/pendulesatoshi/episodes/S01E06---Petit-rcapitulatif--Les-adresses--les-portefeuilles--les-clefs-e1gomnj',
        'https://bitcoin.fr/wp-content/uploads/2022/03/Pendule-de-Satoshi.jpg'],
    ["S01E07 - Bitcoin, c'est pas nouveau, mais ça permet de nouvelles choses", 'Pendule de Satoshi', '2021-04-25 12:00:00', 'https://anchor.fm/pendulesatoshi/episodes/S01E07---Bitcoin--cest-pas-nouveau--mais-a-permet-de-nouvelles-choses-e1h5ve6',
        'https://bitcoin.fr/wp-content/uploads/2022/03/Pendule-de-Satoshi.jpg'],
    ["S01E08 - Tout ça n'est-ce pas juste de la spéculation en final?", 'Pendule de Satoshi', '2021-05-11 12:00:00', 'https://anchor.fm/pendulesatoshi/episodes/S01E08---Tout-a-nest-ce-pas-juste-de-la-spculation-en-final-e1i0u3a',
        'https://bitcoin.fr/wp-content/uploads/2022/03/Pendule-de-Satoshi.jpg'],
]


try:
    conn = psycopg2.connect(
        user="postgres",
        password='',
        host="localhost",
        port="5432",
        database="coincentraliz"
    )
    cur = conn.cursor()

    for media in list_media_envi_ajout:

        title_media = media[0],
        author_media = media[1],
        date_publi_media = media[2],
        url_media = media[3],
        image_media = media[4]

        print("insert")

        sql_insert_media = "INSERT INTO news_media (title, author, datepubli, url, category_environnement, thumbnail) VALUES(%s,%s,%s,%s,%s,%s)"
        # execute the INSERT statement
        val_at_insert = (title_media, author_media,
                         date_publi_media, url_media, True, image_media)

        cur.execute(sql_insert_media, val_at_insert)

        # commit the changes to the database
        conn.commit()

    # fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")
except (Exception, psycopg2.Error) as error:
    print("Erreur lors de la connexion à PostgreSQL", error)


# ['Comment le Kazakhstan est devenu une destination privilégiée des mineurs?', 'Grand Angle Crypto', '2021-08-30 12:00:00', 'https://www.youtube.com/watch?v=l86w3KJMF88', 'https://i.ytimg.com/vi/l86w3KJMF88/hq720.jpg'],
# ['Évolution du minage de Bitcoin en Chine et dans le reste du monde [Sébastien Gouspillou]', 'Grand Angle Crypto', '2021-09-28 12:00:00',
#                           'https://www.youtube.com/watch?v=tt_QFJLmlLU&t=2219s', 'https://i.ytimg.com/vi/tt_QFJLmlLU/hq720.jpg'],
#                          ['Pour en finir définitivement avec le débat “Bitcoin & écologie” [Partie 1/3]', 'Grand Angle Crypto', '2021-10-15 12:00:00',
#                              'https://www.youtube.com/watch?v=VsBnEzL5voM', 'https://i.ytimg.com/vi/VsBnEzL5voM/hqdefault.jpg'],
#                          ['Bitcoin, énergie et environnement [Partie 2/3]', 'Grand Angle Crypto', '2021-10-29 12:00:00', 'https://www.youtube.com/watch?v=jYBohnxiZVk',
#                           'https://i.ytimg.com/vi/jYBohnxiZVk/hqdefault.jpg'],
#                          ['Pour sauver la planète, commençons par changer la monnaie! [Bitcoin & écologie - partie 3/3]', 'Grand Angle Crypto', '2021-11-05 12:00:00',
#                           'https://www.youtube.com/watch?v=Xmsep3fazas', 'https://i.ytimg.com/vi/Xmsep3fazas/hqdefault.jpg'],
#                          ["L’industrie du minage crypto nécessite-t-elle d’être plus régulée?", 'Grand Angle Crypto', '2021-10-10 12:00:00', 'https://www.youtube.com/watch?v=5t4WuTuYCIY',
#                           'https://i.ytimg.com/vi/5t4WuTuYCIY/hqdefault.jpg'],
#                          ['[Podcast] Manuel de survie dans la jungle des poncifs anti-Bitcoin [Alexandre Stachtchenko]', 'Grand Angle Crypto', '2022-01-25 12:00:00',
#                           'https://www.youtube.com/watch?v=-LyjXFJ1es0', 'https://i.ytimg.com/vi/-LyjXFJ1es0/hqdefault.jpg'],
#                          ['Point de situation du minage Bitcoin en 2022 [Sébastien Gouspillou]', 'Grand Angle Crypto', '2022-01-27 12:00:00', 'https://www.youtube.com/watch?v=tCJ6gLt3y3c',
#                           'https://i.ytimg.com/vi/tCJ6gLt3y3c/hqdefault.jpg'],
#                          ['Miner du Bitcoin au Salvador?...soyons sérieux!', 'Grand Angle Crypto', '2022-04-15 12:00:00', 'https://www.youtube.com/watch?v=IdA0deViw-s&t=516s',
#                           'https://i.ytimg.com/vi/IdA0deViw-s/hqdefault.jpg'],
#                          ['Bitcoin - stop au gâchis énergétique!! ♻️', 'Grand Angle Crypto', '2022-04-02 12:00:00', 'https://www.youtube.com/watch?v=K9ntKqb7F3o',
#                           'https://i.ytimg.com/vi/K9ntKqb7F3o/hqdefault.jpg'],
#                          ['Minage et écologie, incompatible ? Avec Sébastien Gouspillou - UBP#13', 'Univers Bitcoin Podcast', '2020-07-19 12:00:00', 'https://www.youtube.com/watch?v=HaiD4BJ1B5M&t=25s',
#                           'https://i.ytimg.com/vi/HaiD4BJ1B5M/hq720.jpg'],
#                          ['Se chauffer en minant du bitcoin avec Alexandre Vinot de WisElement - UBP#48', 'Univers Bitcoin Podcast', '2021-03-21 12:00:00',
#                           'https://www.youtube.com/watch?v=dSlU3xloJCU', 'https://i.ytimg.com/vi/dSlU3xloJCU/hq720.jpg'],
#                          ["Miner les surplus d'énergie avec Bitcoin, un mariage vert 🎙 Sébastien Gouspillou - PB32", 'Parlons Bitcoin', '2021-12-15 12:00:00', 'https://www.youtube.com/watch?v=toUAfq8Xtp8&t=3s',
#                           'https://i.ytimg.com/vi/toUAfq8Xtp8/hq720.jpg'],
#                          ['Bitcoin ne gaspille pas d’énergie - GPS4', 'Parlons Bitcoin', '2022-02-04 12:00:00', 'https://www.youtube.com/watch?v=OhwrBmgPsAQ',
#                           'https://i.ytimg.com/vi/OhwrBmgPsAQ/hq720.jpg'],
#                          ['Bitcoin et énergie, baisser le coût de la chaleur grâce au minage à domicile Alex Vinot |Wise Mining', 'Parlons Bitcoin', '2021-08-11 12:00:00',
#                           'https://www.youtube.com/watch?v=X9coDXMejG0', 'https://i.ytimg.com/vi/X9coDXMejG0/hqdefault.jpg'],
#                          ['Bitcoin : unique solution à la transition énergétique ? #SébastienGouspillou', "Surfin' Bitcoin", '2021-09-15 12:00:00',
#                           'https://www.youtube.com/watch?v=An3OXqdM-7Y', 'https://i.ytimg.com/vi/An3OXqdM-7Y/hq720.jpg'],
#                          ["L'or plus 'énergivore' que Bitcoin ?! #PierreNoizat", "Surfin' Bitcoin", '2021-09-15 12:00:00', 'https://www.youtube.com/watch?v=mduJupwcuyc&t=511s',
#                           'https://i.ytimg.com/vi/mduJupwcuyc/hq720.jpg'],
#                          ["Explorons Bitcoin N°4: L'écologie", 'Découvre Bitcoin', '2021-09-11 12:00:00', 'https://www.youtube.com/watch?v=YQ-Z96hBnq4&t=11s', 'https://i.ytimg.com/vi/YQ-Z96hBnq4/hq720.jpg']
