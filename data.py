# -----------------------------------------------------------------------
#                              Mock Data
# -----------------------------------------------------------------------

venue1 = Venue(name="The Musical Hop", address="1015 Folsom Street", city="San Francisco", state="CA",
               phone="123-123-1234", website="https://www.themusicalhop.com",
               facebook_link="https://www.facebook.com/TheMusicalHop", seeking_talent=True,
               seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
               image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60")
venuegenre = VenueGenre(name="Jazz")
venue1.genres.append(venuegenre)
venuegenre = VenueGenre(name="Reggae")
venue1.genres.append(venuegenre)
venuegenre = VenueGenre(name="Swing")
venue1.genres.append(venuegenre)
venuegenre = VenueGenre(name="Classical")
venue1.genres.append(venuegenre)
venuegenre = VenueGenre(name="Folk")
venue1.genres.append(venuegenre)

venue2 = Venue(name="The Dueling Pianos Bar", address="335 Delancey Street", city="New York", state="NY",
               phone="914-003-1132", website="https://www.theduelingpianos.com",
               facebook_link="https://www.facebook.com/theduelingpianos", seeking_talent=False,
               image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80")
venuegenre = VenueGenre(name="Classical")
venue2.genres.append(venuegenre)
venuegenre = VenueGenre(name="R&B")
venue2.genres.append(venuegenre)
venuegenre = VenueGenre(name="Hip-Hop")
venue2.genres.append(venuegenre)

venue3 = Venue(name="Park Square Live Music & Coffee", address="34 Whiskey Moore Ave", city="San Francisco", state="CA",
               phone="415-000-1234", website="https://www.parksquarelivemusicandcoffee.com",
               facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee", seeking_talent=False,
               image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80")
venuegenre = VenueGenre(name="Rock n Roll")
venue3.genres.append(venuegenre)
venuegenre = VenueGenre(name="Jazz")
venue3.genres.append(venuegenre)
venuegenre = VenueGenre(name="Classical")
venue3.genres.append(venuegenre)
venuegenre = VenueGenre(name="Folk")
venue3.genres.append(venuegenre)
## -----------------------------------------------
artist1 = Artist(name="Guns N Petals", city="San Francisco", state="CA", phone="326-123-5000",
                 website="https://www.gunsnpetalsband.com", facebook_link="https://www.facebook.com/GunsNPetals",
                 seeking_venue=True,
                 seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
                 image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80")
artistgenre = ArtistGenre(name="Rock n Roll")
artist1.genres.append(artistgenre)

artist2 = Artist(name="Matt Quevedo", city="New York", state="NY", phone="300-400-5000",
                 facebook_link="https://www.facebook.com/mattquevedo923251523", seeking_venue=False,
                 image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80")
artistgenre = ArtistGenre(name="Jazz")
artist2.genres.append(artistgenre)

artist3 = Artist(name="The Wild Sax Band", city="San Francisco", state="CA", phone="432-325-5432",
                 seeking_venue=False,
                 image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80")
artistgenre = ArtistGenre(name="Classical")
artist3.genres.append(artistgenre)
artistgenre = ArtistGenre(name="Jazz")
artist3.genres.append(artistgenre)
# -----------------------------------------------
show1 = Show(start_time='2019-05-21 21:30:00')
show1.venue = venue1
show1.artist = artist1

show2 = Show(start_time='2019-06-15 23:00:00')
show2.venue = venue3
show2.artist = artist2

show3 = Show(start_time='2035-04-01 20:00:00')
show3.venue = venue3
show3.artist = artist3

show4 = Show(start_time='2035-04-08 20:00:00')
show4.venue = venue3
show4.artist = artist3

show5 = Show(start_time='2035-04-15 20:00:00')
show5.venue = venue3
show5.artist = artist3