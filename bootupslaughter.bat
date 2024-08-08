@echo off
:: Replace 'ServiceName' with the actual service names you want to disable
sc stop GamingServices
sc config GamingServices start= disabled
sc stop ServiceName2
sc config ServiceName2 start= disabled
:: Add more services as needed
