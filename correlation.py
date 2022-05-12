from cormodule.cor import correlate_by_one


'''
 The first parameter: .csv filepath of dependent variables
 The second parameter: list of .csv filepaths of independent variables

 NB! This may take up to several hours as complexity is O(n^2) and ML is overall pretty hard computationally
'''
correlate_by_one("datasets/rimi milk.csv", ["datasets/apple.csv", "datasets/eggs.csv", "datasets/beef.csv"])

correlate_by_one("datasets/pizza.csv", ["datasets/beef.csv"])

correlate_by_one("datasets/cake.csv", ["datasets/wheat.csv", "datasets/milk.csv"])
correlate_by_one("datasets/pizza.csv", ["datasets/wheat.csv", "datasets/pig meat.csv"])

correlate_by_one("datasets/cake.csv", ["datasets/wheat.csv", "datasets/pear.csv", "datasets/apple.csv"])
correlate_by_one("datasets/cookies.csv", ["datasets/sugar.csv", "datasets/milk.csv"])
correlate_by_one("datasets/pizza.csv", ["datasets/banana.csv", "datasets/tomatoes.csv", "datasets/chicken.csv"])




'''
 By passing allow_same parameter you can allow to have the same price values for regression variables
'''
correlate_by_one("datasets/rimi milk.csv", ["datasets/other shop milk.csv"], allow_same=True)