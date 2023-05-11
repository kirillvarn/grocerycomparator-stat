from cor import correlate_by_one
"""
 The first parameter: .csv filepath of dependent variables
 The second parameter: list of .csv filepaths of independent variables

 NB! This may take up to several hours as complexity is O(n^2) and ML is overall pretty hard computationally
"""
# correlate_by_one("datasets/pizza.csv", ["datasets/beef.csv"])
# correlate_by_one("datasets/pizza.csv", ["datasets/beef.csv"], model="lasso")
# correlate_by_one("datasets/pizza.csv", ["datasets/beef.csv"], model="ridge")

# correlate_by_one("datasets/pizza.csv", ["datasets/wheat.csv"])
# correlate_by_one("datasets/pizza.csv", ["datasets/wheat.csv"], model="lasso")
# correlate_by_one("datasets/pizza.csv", ["datasets/wheat.csv"], model="ridge")

# correlate_by_one("datasets/pizza.csv", ["datasets/wheat.csv", "datasets/beef.csv"])
# correlate_by_one("datasets/pizza.csv", ["datasets/wheat.csv", "datasets/beef.csv"], model="lasso")
# correlate_by_one("datasets/pizza.csv", ["datasets/wheat.csv", "datasets/beef.csv"], model="ridge")

# correlate_by_one("datasets/cake.csv", ["datasets/milk.csv"])
# correlate_by_one("datasets/cake.csv", ["datasets/milk.csv"], model="lasso")
# correlate_by_one("datasets/cake.csv", ["datasets/milk.csv"], model="ridge")

# correlate_by_one("datasets/cake.csv", ["datasets/wheat.csv"])
# correlate_by_one("datasets/cake.csv", ["datasets/wheat.csv"], model="lasso")
# correlate_by_one("datasets/cake.csv", ["datasets/wheat.csv"], model="ridge")

# correlate_by_one("datasets/cake.csv", ["datasets/milk.csv", "datasets/wheat.csv"])
# correlate_by_one("datasets/cake.csv", ["datasets/milk.csv", "datasets/wheat.csv"], model="lasso")
# correlate_by_one("datasets/cake.csv", ["datasets/milk.csv", "datasets/wheat.csv"], model="ridge")

# correlate_by_one("datasets/cake.csv", ["datasets/pear.csv", "datasets/apple.csv", "datasets/wheat.csv"])
correlate_by_one("datasets/cake.csv", ["datasets/pear.csv", "datasets/apple.csv", "datasets/wheat.csv"], model="lasso")
correlate_by_one("datasets/cake.csv", ["datasets/pear.csv", "datasets/apple.csv", "datasets/wheat.csv"], model="ridge")


