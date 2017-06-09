import ConfigParser,string,os,sys
import ast

cf = ConfigParser.ConfigParser()
cf.read("test.conf")

hostname = ast.literal_eval(cf.get("host","hostname"))

print (type(hostname))
print hostname