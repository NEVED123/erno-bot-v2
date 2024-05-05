class Competition:
    def __init__(self, soup = None, name = None, date = None, location = None, link = None):
        if soup is not None:
            self.location = self.get_location(soup)
            self.link = self.get_link(soup)
            self.name = self.get_name(soup)
            self.date = self.get_date(soup)
        else:
            self.location = location
            self.link = link
            self.name = name
            self.date = date

    def get_location(self, comp):
        return comp.find(attrs={'class':'location'}).text.strip()

    def get_link(self, comp):
        return 'https://www.worldcubeassociation.org' + comp.find(attrs={'class':'competition-link'}).find('a')['href']

    def get_name(self, comp):
        return comp.find(attrs={'class':'competition-link'}).find('a').text.strip()

    def get_date(self, comp):
        return comp.find(attrs={'class':'date'}).text.strip()

    def create_announcement(self):
        return f'''Hey @everyone, the "*{self.name}*" competition has been posted on the WCA page! Here are the details: 

            **Date**: {self.date}, 
            **Location**: {self.location}
            Click [here]({self.link}) for more info!
        
            Sign-up for these competitions goes quick, so get on it!
                    '''
    
    def __eq__(self, value):
        if not isinstance(value, Competition):
            return False
        return self.name == value.name and self.date == value.date and self.location == value.location and self.link == value.link

    def __str__(self):
        return f'{self.name} {self.date} {self.location} {self.link}'