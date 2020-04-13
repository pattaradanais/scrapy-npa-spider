from scrapinghub import ScrapinghubClient

apikey = "32eacac2e8b641599accac499c4d555c"
client = ScrapinghubClient(apikey)
project = client.get_project(437374)

def run_spider():
    try:
        project.jobs.run('spider')
        return "Start scraping"
    except:
        return "Error: Can't start scraping"

def job_state():
    return project.jobs.list()[0]['state']