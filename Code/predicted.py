import mongoimport

mongoimport.mongoimport("./Data/predicted.csv", "big-data-machine-learning", "predictions", 
"mongodb+srv://mbergamin:ba6t32ms78tf@big-data-project.g26gj.mongodb.net/?retryWrites=true&w=majority")