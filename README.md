# sajinboard
Linkki sivustolle: [sajinboard](https://sajinboard.herokuapp.com/ "sajinboard")
# Kuvaus
Web-sovellus kuvien jakamiseen. Sivustolle voi lisätä kuvia ja keskustella niistä.

# Toiminnallisuudet

- Käyttäjä voi luoda tunnuksen ja kirjautua sisään tai ulos.
- Käyttäjä pystyy selaamaan listaa kuvista aiheen valittuaan.
- Käyttäjällä on mahdollisuus tuoda esille seuraava kuva satunnaisesti sivuston kaikista kuvista.
- Käyttäjä voi lisätä kuvan sivustolle.
- Halutessaan käyttäjä pystyy lisäämään (tai poistamaan) kommentin esillä olevalle kuvalle.
- Halutessaan käyttäjä voi tykätä kuvasta.
- Käyttäjä voi tykätä kuvassa olevasta kommentista?
- Käyttäjällä pystyy halutessaan lisäämään (tai poistamaan) kuvan seurattujen kuvien listalle.
- Kun käyttäjä haluaa hän saa poistettua tunnuksensa.

- Ylläpitäjä voi poistaa minkä tahansa tunnuksen.
- Ylläpitäjä pystyy poistamaan muiden kuvia ja kommentteja.

# Välipalautus 1
- Käyttäjä voi nyt luoda tunnuksen, kirjautua sisään ja ulos.

# Välipalautus 2
- Kirjautunut käyttäjä voi lisätä kuvan tietoineen sovellukseen.
- Käyttäjä voi katsoa satunnaisesti valittuja kuvia.

# Sovelluksen käyttö
Osa sivun toiminnoista vaatii Javascriptin sallimista.

### Käyttäjätunnukset

Sivustolle voi luoda käyttäjätunnuksen Sign up-painikkeesta. Näin aukeavalla sivulla on syötettävä 6-20 merkin pituinen käyttäjätunnus, sähköpostiosoite, 8-20 merkin pituinen salasana ja sama salasana uudelleen. Sisään kirjautuminen onnistuu etusivulla jonne pääsee Sign in-painikkeesta. Ulos kirjautuminen onnistuu Log out-painikkeesta.

### Käyttäjätiedot

Itse lataamia kuvia pääsee tarkastelemaan My uploads-painikkeen kautta. Klikkaamalla ladatun kuvan nimeä aukeaa kuvaa vastaava sivu. Omia käyttäjätietoja voi tarkastella painamalla My profile-painiketta ja näin auki olevalla sivulla voi poistaa tunnuksensa delete this account-painikkeella.

Ylläpitäjä pääsee User list-painikkeella sivulle, jolla on listattuna kaikki sivustolle rekisteröityneet käyttäjät tietoineen ja tällä sivulla roskakori-kuvaketta klikkaamalla voi poistaa kyseisen käyttäjän ja käyttäjän Id-numeroa klikkaamalla voi tehdä käyttäjästä ylläpitäjän tai poistaa ylläpitäjän oikeudet. Jos poistaa vahingossa omat ylläpitäjän oikeudet ne voi antaa itselleen takaisin saman istunnon yhteydessä.

### Kuvien lataaminen

Upload-painikkeella pääsee kuvalataukseen, jossa kuvalle on annettava max 10 merkin pituinen otsikko, valittava kategoria valikosta ja maksimissaan 2MB kokoinen jpg tai png tiedosto omalta koneelta.

### Kuvien selailu

Sivustolle ladattuja kuvia pääsee katselemaan Search-painikkeen kautta joko aihekohtaisesti tai random painikkeella, jota painamalla aukeaa satunnaisesti valittu kuva sivuston kaikkien kuvien joukosta. Kuvien selaamiseen ei tarvitse olla sisäänkirjautunut, mutta osa toiminnoista on varattu vain sisään kirjautuneille. 

Listan tietyn kategorian kuvista pääsee näkemään klikkaamalla kategorian painiketta. Klikkaamalla kuvan korttia pääsee kuvan sivulle. Kuvan sivulla sisäänkirjautunut käyttäjä voi tykätä kuvasta klikkaamalla Like-painiketta. Kuvan lataaja tai ylläpitäjä voi muuttaa kuvan otsikkoa Edit-painikkeella ja/tai poistaa kuvan Delete image-painikkeella sivustolta.

Kirjautunut käyttäjä voi myös kommentoida kuvaa Enter comment here-osiossa ja painaa Send-painiketta kommentin tallentamiseksi. Kommentin kirjoittanut käyttäjä tai ylläpitäjä voi poistaa kommentin Delete-painikkeella.


# Testaus

- Valmis normaali käyttäjätunnus:test123 salasana:testi123, ja ylläpitäjän tunnus:admin salasana:admin sähköposteina käytetty testi@testi.com, admin@admin.com ja samaa sähköpostia / tunnusta ei saa käyttää kahdesti.
