import scraper
import cullCyclists
import simulate
import solver

if __name__ == '__main__':

    scraper.ScrapePCS()
    scraper.ScrapeVelogames()
    cullCyclists.CullCyclists()
    simulate.RunTour()
    solver.Solve()
