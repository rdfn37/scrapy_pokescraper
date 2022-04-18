from asyncio.windows_events import NULL
from operator import index, indexOf
from re import I, template
from webbrowser import get
import scrapy

class PokeSpider(scrapy.Spider):
    name='poke'
    start_urls = ['https://www.serebii.net/blackwhite/gyms.shtml']

    def parse(self, response):
        # index = 0
        locations = []

        for indexGyms, gyms in enumerate(response.css('table.tab > tr > td.fooleft')):
            locations.append(gyms.css('font::text').get())
            location = gyms.css('font::text').get()
            
        for indexTabs, tabs in enumerate(response.css('table.tab > tr > td.foocontent')):
            leaderList = []

            for leaders in tabs.css('table.trainer'):
                team = []
                pokemon_imgs = leaders.css('tr')[0].xpath('.//td//a//img/@src').getall()
                pokemon_levels = leaders.css('tr')[2].css('td.level::text').getall()

                pokemon_abilities = leaders.xpath('.//tr[4]//td//a//text()').getall()
                    # pokemon_abilities.append(pokemon_ability)
                
                # pokemon_types = leaders.xpath('.//tr[4]//td//a//img/@src').getall()

                for indexPokemon, pokemons  in enumerate(leaders.css('tr')[1].xpath('.//td')):
                    pokemon_types = []
                    pokemon_moves = []
                    # pokemon_abilities = []

                    for types in leaders.xpath('.//tr[4]//td'):
                        pokemon_type = types.xpath('.//a//img/@src').getall()
                        pokemon_types.append(pokemon_type)
                    
                    for moves in leaders.xpath('.//tr[5]//td'):
                        pokemon_move = moves.xpath('.//a//text()').getall()
                        pokemon_moves.append(pokemon_move)

                    pokemon = {
                        'name': pokemons.xpath('.//a//text()').get(),
                        'img_url': 'https://www.serebii.net' + pokemon_imgs[indexPokemon - 1],
                        'level': pokemon_levels[indexPokemon - 1],
                        'type': pokemon_types[indexPokemon - 1],
                        'ability': pokemon_abilities[indexPokemon - 1],
                        'moves': pokemon_moves[indexPokemon - 1]
                    }
                    
                    if pokemon['name']:
                        team.append(pokemon)

                leader = {
                    'name': leaders.css('tr > td.foocontent::text').get(),
                    'img_url': 'https://www.serebii.net' + leaders.xpath('.//tr')[0].xpath('.//td//img/@src').get(),
                    'team': team
                }
                leaderList.append(leader)



            yield {
                'location': locations[indexTabs],
                'leader': leaderList
            }
