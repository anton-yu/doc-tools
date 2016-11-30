#!/usr/bin/python
import datetime
import calendar 
import re

def main():
  input = "capsules.tsv"

  ## use this to output all listings into one file ## 
  outfl = "listings.txt"
  outfile = open("listings.txt", "w") 

  ## generate series pages 
  mondays = open("mondays.shtml", "w")
  tuesdays = open("tuesdays.shtml", "w")
  wednesdays = open("wednesdays.shtml", "w")
  thursdays1 = open("thursdays-1.shtml", "w")
  thursdays2 = open("thursdays-2.shtml", "w") 
  fridays = open("fridays.shtml", "w")
  saturdays = open("saturdays.shtml", "w")
  sundays = open("sundays.shtml", "w")
  pages = {0: ("Mondays", mondays), 1: ("Tuesdays", tuesdays), 2: ("Wednesdays", wednesdays), 3: ("Thursdays 1", thursdays1), 3.2: ("Thursdays 2", thursdays2), 4: ("Fridays", fridays), 5: ("Saturdays", saturdays), 6: ("Sundays", sundays)}

  for dow in pages:
    page = pages[dow]
    page[1].write('<html>\n\n<h2 style="text-align:center">%s</h2>' % page[0])

  loc = "Max Palevsky Cinema, Ida Noyes Hall"
  cred = "Presented by Doc Films" 
  price = "General $5, free with quarterly pass ($30)"

  thurs2 = 0
  quarter = ""

  with open(input) as infile:
    for line in infile: # grab info from capsules spreadsheet
      vals = line.split('\t')
      title = vals[0]
      director = vals[9]
      year = vals[10]
      capsule = vals[11]
      runtime = "%sm" % vals[12]
      format = vals[13]
      date = vals[14]
      times = vals[15:] # in cases of multiple screenings

      if capsule == "":
        continue

      # find dow from date
      date_split = date.split('/')
      d = datetime.date(int(date_split[2]), int(date_split[0]), int(date_split[1]))
      dow_num = d.weekday() # day of the week as an int, where Monday is 0 and Sunday is 6
      dow = calendar.day_name[dow_num]

      # format multiple screening times (for Wednesday, Friday, Saturday titles)
      if dow_num == 2: 
        screen_times = "%s @ %s %s" % (date, times[0], times[1])
      elif dow_num == 4 or dow_num == 5:
        screen_times = "%s @ %s %s <br>\n%s @ %s" % (date, times[0], times[1], times[3], times[4])
      else: 
        screen_times = "%s @ %s" % (date, times[0])
 
      # format quarter and dates for film still ref on series pages
      img_date = "%s-%s-%s" % (year, date_split[0].zfill(2), date_split[1].zfill(2))

      if quarter == "": # this will only run once 
        month = int(date_split[0])
        if month < 3:
          quarter = "winter"
        elif month < 6:
          quarter = "spring"
        elif month < 9:
          quarter = "summer"
        else:
          quarter = "fall" 

      # italicize all strings within _underscores_
      capsule_italic = re.sub(r'_([^_]*)_', r'<i>\1</i>', capsule)

      # take into account thursday 2 for series pages
      if dow_num == 3: 
        if thurs2 == 0:
          thurs2 = 1
        else:
          thurs2 = 0
          dow_num = 3.2 

      screening = """
        <h4 style="text-align:center;" id="showtime">
        {screening_times}
        </h4>
        <h4 style="text-align:center;" id="film title">
          <i>{title}</i>
          </h4>
          <p style="text-align:center;" id="film still">
          <img src="/dev/images/{year}/{quarter}/{date}.jpg" width="100%">
        </p>
         <p style="text-align:center; font-size 14px;" id="capsule">
        <i>({director}, {year})</i> <b>&middot;</b>
        {capsule}
        <p style="text-align:center;" id="runtime/format">
        <b>runtime:</b> {runtime}
         <b>format:</b> {format}
            </p>&nbsp;</p>"""

      formatting = {
        "title": title,
        "year": year,
        "director": director,
        "runtime": runtime,
        "capsule": capsule_italic,
        "format": format,
        "date": img_date,
        "screening_times": screen_times,
        "quarter": quarter
      }

      page = pages[dow_num]
      page[1].write(screening.format(**formatting))

      outfile.write("%s\n%s\n%s\n%s (%s, %s, %s, %s)\n%s\n%s\n\n" % (title, screen_times, loc, capsule, director, year, runtime, format, price, cred))

  outfile.close()

  for dow in pages:
    page = pages[dow]
    page[1].write('<p><a href="/dev/calendar/"">back to the calendar</a></p>\n</div><!--End page container -->\n<!--#include virtual="/dev/includes-new/inc_footer.shtml" -->\n</html>')
    page[1].close()

if __name__ == '__main__':
    main()
