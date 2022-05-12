# grocerycomparator-stat
Statistics/ML library for Grocerycomparator app

using Cython for ML and Python for everything else


45 dates of products from 5 Estonian groceries -- Maxima, Prisma, Selver, Coop, and Rimi

Datasets folders containts product prices by the categories in .csv format.

If you want, you can get the data from the server youself, there is roughly 46,000 products for every day starting from 6th of March and till 5th of May (~2mil of total records).

In the 'fetch.py' file, there are SQL queries to the database -- you can use whatever query you feel like using. For instance, to get all entries from Rimi and Prisma market, that contain 'banana' you simply:

```
"SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND name ILIKE '%%banaan%%' AND (shop_name == 'prisma' OR shop_name == 'rimi');"
```

\"%s\" -- stands for "%s" in the actual query, just avoiding a lot of string concatenations with +

%%banaan%% -- python's pcyopg2 interpeters single % as a query parameter (like %s we declared before)

NB! The product names should be in estonian!
