CronTrigger
-----------
syntax
^^^^^^
- extended crontab-like syntax.

- A cron-expression have 6 or 7 whitespace-separated fields, in the following
  order:

  * seconds. 0-59

  * minutes. 0-59

  * hours. 0-23

  * day-of-month. 0-31

  * month. 0-11, JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC.

  * day-of-week. 1-7 (1=Sunday), SUN, MON, TUE, WED, THU, FRI, SAT.

  * year (optional)

- Each field can be any combination of the following
  
  * a single value 
   
  * a range of values (``a-b``) 
   
  * a comma separated list of values (``a,b,c``)

  * ``*`` means "for every possible value".

  * ``a/b`` means every b-th unit starting at a. For example, ``3/20`` at
    minute field means every 20th minute starting from minute 3, a.k.a.
    ``3,23,43``.  ``*/35`` means every 35th minute starting from minute 0,
    a.k.a. ``0,35``.

  * ``?`` allowed for the day-of-month and day-of-week fields. means “no
    specific value”. useful when you need to specify something in one of the
    two fields, but not the other.

  * ``L`` allowed for the day-of-month and day-of-week fields. short-hand for
    “last”.
    
    - in the day-of-month field means “the last day of the month”, You can also
      specify an offset from the last day of the month, such as “L-3” which
      would mean the third-to-last day (倒数第三天) of the calendar month. When
      using the ‘L ’ option, it is important not to specify lists, or ranges of
      values, as you’ll get confusing/unexpected results.

    - in the day-of-week field by itself, it simply means “7” or “SAT”. 

    - if used in the day-of-week field after another value, it means “the last
      xxx day of the month”, for example “6L” or “FRIL” both mean “the last
      friday of the month”.

  * ``W`` allowed for the day-of-month field. specify the weekday
    (Monday-Friday) nearest the given day. E.g., “15W” as the value for the
    day-of-month field, the meaning is: “the nearest weekday to the 15th of the
    month”.

  * ``#`` allowed for the day-of-week field. specify “the nth” XXX weekday of
    the month. E.g., “6#3” or “FRI#3” in the day-of-week field means “the third
    Friday of the month”.
