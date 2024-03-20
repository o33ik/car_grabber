import pdb
from collections import namedtuple
import re
import requests
import bs4

CarData = namedtuple('CarData', 'url name price mileage vin year photo_url location engine vin_hidden')

class AutoriaGrabber:
    def grab(self, url):
        result = requests.get(url)
        page_soup = bs4.BeautifulSoup(result.text, 'lxml')
        return self.parse_cars(page_soup)

    def parse_cars(self, page_soup):
        cars = page_soup.select('.ticket-item')
        cars_data = []
        for index, car in enumerate(cars):
            try:
                url = self.parse_url(car)
                name = self.parse_name(car)
                year = self.parse_year(car)
                price = self.parse_price(car)
                mileage = self.parse_mileage(car)
                vin = self.parse_vin(car)
                vin_hidden = not self.valid_vin(vin)
                photo_url = self.parse_photo_url(car)
                location = self.parse_location(car)
                engine = self.parse_engine(car)

                car_data = CarData(name=name.strip(), url=url, price=int(price), mileage=mileage,
                                   year=int(year), photo_url=photo_url, vin=vin, location=location, engine=engine, vin_hidden=vin_hidden)
                cars_data.append(car_data)
            except Exception as e:
                print(index, e)
        return cars_data

    def parse_url(self, car):
        link = car.select_one('.ticket-title a')
        if link:
            return link.attrs['href']
    def parse_name(self, car):
        title = car.select_one('.ticket-title')
        if title:
            return title.find_all(text=True)[2].strip()
        return ''

    def parse_year(self, car):
        title = car.select_one('.ticket-title')
        if title:
            return title.find_all(text=True)[3].strip()
        return ''

    def parse_price(self, car):
        price_tag = car.select_one('.price-ticket')
        if price_tag:
            return price_tag.attrs['data-main-price'].strip()
        return ''

    def parse_mileage(self, car):
        mileage_tag = car.select_one('.js-race')
        if mileage_tag:
            mileage_raw = mileage_tag.find_all(text=True)[0].strip()
            return int(re.search(r'\d+', mileage_raw).group(0) + '000')
        return 0

    def parse_vin(self, car):
        vin_tag = car.select_one('.label-vin')
        if vin_tag:
            return vin_tag.find_all(text=True)[4].strip()
        return ''

    def valid_vin(self, vin):
        return not re.search(r'xxxx', vin)

    def parse_photo_url(self, car):
        photo_tag = car.select_one('.ticket-photo img')
        if photo_tag:
            return photo_tag.attrs['src']
        return ''

    def parse_location(self, car):
        location_tag = car.select_one('.js-location')
        if location_tag:
            return location_tag.find_all(text=True)[1].strip()
        return ''

    def parse_engine(self, car):
        engine_tag = car.select_one('.icon-fuel')
        if engine_tag:
            return engine_tag.find_parent().find_all(text=True)[0].strip()
        return ''


