import Scraper
import CullCyclists
import Simulate
import Solver

if __name__ == '__main__':

    Scraper.ScrapePCS()
    Scraper.ScrapeVelogames()
    CullCyclists.CullCyclists()
    Simulate.RunTour()
    
