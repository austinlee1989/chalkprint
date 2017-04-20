# Define Connection #
library(RMySQL)

drv <- dbDriver("MySQL")
mydb <- dbConnect(MySQL()
                  , user = 'root'
                  , password = 'fnwl5r'
                  , host = '127.0.0.1')

