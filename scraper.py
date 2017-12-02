import scraperwiki
import urlparse
import lxml.html
# scrape_table function: gets passed an individual page to scrape
# where is root coming from?
def scrape_table(root):
    rows = root.cssselect("table.data tr")  # selects all <tr> blocks within <table class="data">
    for row in rows: # where do row and rows come from? 
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td") #In the row use cssselect to select for td
        if table_cells: 
            record['Artist'] = table_cells[0].text
            record['Album'] = table_cells[1].text
            record['Released'] = table_cells[2].text
            record['Sales m'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["Artist"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.next")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)
base_url = 'https://paulbradshaw.github.io/'
starting_url = urlparse.urljoin(base_url, 'scraping-for-everyone/webpages/example_table_1.html')
scrape_and_look_for_next_link(starting_url)
